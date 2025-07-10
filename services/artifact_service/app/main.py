from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
import uuid
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

from .config import settings
from .database import init_db, check_db_connection
from .routes import router as artifact_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'artifact_service_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'artifact_service_request_duration_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)

# OpenTelemetry setup
if settings.OTEL_ENABLED:
    try:
        # Create tracer provider
        resource = Resource.create({
            "service.name": settings.OTEL_SERVICE_NAME,
            "service.version": settings.OTEL_SERVICE_VERSION,
            "deployment.environment": settings.ENVIRONMENT
        })
        
        trace_provider = TracerProvider(resource=resource)
        
        # Create OTLP exporter
        otlp_exporter = OTLPSpanExporter(endpoint=settings.OTEL_ENDPOINT)
        
        # Add span processor
        trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        
        # Set global tracer provider
        trace.set_tracer_provider(trace_provider)
        
        logger.info("OpenTelemetry tracing enabled")
    except Exception as e:
        logger.warning(f"Failed to initialize OpenTelemetry: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    # Check database connection
    if not check_db_connection():
        logger.error("Database connection check failed")
        raise RuntimeError("Database connection failed")
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Application shutdown initiated")

# Create FastAPI app
app = FastAPI(
    title=settings.API_DOCS_TITLE,
    description=settings.API_DOCS_DESCRIPTION,
    version=settings.API_DOCS_VERSION,
    docs_url="/docs" if settings.API_DOCS_ENABLED else None,
    redoc_url="/redoc" if settings.API_DOCS_ENABLED else None,
    openapi_url="/openapi.json" if settings.API_DOCS_ENABLED else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# OpenTelemetry instrumentation
if settings.OTEL_ENABLED:
    try:
        FastAPIInstrumentor.instrument_app(app)
        SQLAlchemyInstrumentor()
        RedisInstrumentor()
        logger.info("OpenTelemetry instrumentation enabled")
    except Exception as e:
        logger.warning(f"Failed to enable OpenTelemetry instrumentation: {e}")

# Request/Response middleware
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    """Middleware for request/response logging and metrics."""
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    # Add request ID to request state
    request.state.request_id = request_id
    
    # Log request
    logger.info(f"Request {request_id}: {request.method} {request.url}")
    
    try:
        response = await call_next(request)
        
        # Calculate latency
        latency = time.time() - start_time
        
        # Log response
        logger.info(f"Response {request_id}: {response.status_code} ({latency:.3f}s)")
        
        # Record metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(latency)
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{latency:.3f}s"
        
        return response
        
    except Exception as e:
        # Log error
        logger.error(f"Request {request_id} failed: {e}")
        
        # Record error metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=500
        ).inc()
        
        # Return error response
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "request_id": request_id
            }
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if not settings.HEALTH_CHECK_ENABLED:
        return {"status": "disabled"}
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "checks": {}
    }
    
    # Database health check
    try:
        db_healthy = check_db_connection()
        health_status["checks"]["database"] = "healthy" if db_healthy else "unhealthy"
        if not db_healthy:
            health_status["status"] = "unhealthy"
    except Exception as e:
        health_status["checks"]["database"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Redis health check
    try:
        from .deps import get_redis_client
        redis_client = get_redis_client()
        redis_client.ping()
        health_status["checks"]["redis"] = "healthy"
    except Exception as e:
        health_status["checks"]["redis"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # OpenTelemetry health check
    if settings.OTEL_ENABLED:
        try:
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span("health_check") as span:
                span.set_attribute("health.check", True)
            health_status["checks"]["opentelemetry"] = "healthy"
        except Exception as e:
            health_status["checks"]["opentelemetry"] = f"error: {str(e)}"
    
    return health_status

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    if not settings.PROMETHEUS_ENABLED:
        return {"status": "disabled"}
    
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "docs": "/docs" if settings.API_DOCS_ENABLED else None,
        "health": "/health",
        "metrics": "/metrics" if settings.PROMETHEUS_ENABLED else None
    }

# Include artifact routes
app.include_router(artifact_router, prefix="/api/v1")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Endpoint not found",
            "path": str(request.url),
            "request_id": getattr(request.state, "request_id", "unknown")
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handle 500 errors."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "request_id": getattr(request.state, "request_id", "unknown")
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} starting up")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"API docs: {'enabled' if settings.API_DOCS_ENABLED else 'disabled'}")
    logger.info(f"Metrics: {'enabled' if settings.PROMETHEUS_ENABLED else 'disabled'}")
    logger.info(f"OpenTelemetry: {'enabled' if settings.OTEL_ENABLED else 'disabled'}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info(f"{settings.APP_NAME} shutting down")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS if not settings.DEBUG else 1
    ) 