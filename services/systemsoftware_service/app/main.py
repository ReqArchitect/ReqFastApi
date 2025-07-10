from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
import traceback
from typing import Dict, Any

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Prometheus metrics
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import REGISTRY

from .config import settings
from .database import init_db, check_db_connection
from .routes import router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(settings.LOG_FILE) if settings.LOG_FILE else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'systemsoftware_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'systemsoftware_http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# OpenTelemetry setup
def setup_telemetry():
    """Setup OpenTelemetry tracing."""
    if not settings.OTEL_ENABLED:
        return
    
    try:
        # Create tracer provider
        resource = Resource.create({
            "service.name": settings.OTEL_SERVICE_NAME,
            "service.version": settings.OTEL_SERVICE_VERSION,
            "deployment.environment": settings.ENVIRONMENT
        })
        
        provider = TracerProvider(resource=resource)
        
        # Add OTLP exporter if endpoint is configured
        if settings.OTEL_ENDPOINT:
            otlp_exporter = OTLPSpanExporter(endpoint=settings.OTEL_ENDPOINT)
            provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        
        # Set the global tracer provider
        trace.set_tracer_provider(provider)
        
        logger.info("OpenTelemetry tracing configured successfully")
        
    except Exception as e:
        logger.error(f"Failed to setup OpenTelemetry: {e}")

# Application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting System Software Service...")
    
    # Setup telemetry
    setup_telemetry()
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    # Check database connection
    if not check_db_connection():
        logger.error("Database connection check failed")
        raise RuntimeError("Database connection failed")
    
    logger.info("System Software Service started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down System Software Service...")

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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.DEBUG else ["localhost", "127.0.0.1"]
)

# Request/Response middleware for metrics and logging
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware for metrics collection and request logging."""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    try:
        response = await call_next(request)
        
        # Record metrics
        duration = time.time() - start_time
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=str(request.url.path),
            status=response.status_code
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=str(request.url.path)
        ).observe(duration)
        
        # Log response
        logger.info(f"Response: {request.method} {request.url} - {response.status_code} ({duration:.3f}s)")
        
        return response
        
    except Exception as e:
        # Record error metrics
        duration = time.time() - start_time
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=str(request.url.path),
            status=500
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=str(request.url.path)
        ).observe(duration)
        
        # Log error
        logger.error(f"Request failed: {request.method} {request.url} - {str(e)}")
        logger.error(traceback.format_exc())
        
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    health_status = {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": time.time()
    }
    
    # Check database connection
    if not check_db_connection():
        health_status["status"] = "unhealthy"
        health_status["database"] = "disconnected"
    else:
        health_status["database"] = "connected"
    
    # Check Redis connection
    try:
        from .deps import get_redis_client
        redis_client = get_redis_client()
        redis_client.ping()
        health_status["redis"] = "connected"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["redis"] = "disconnected"
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    return JSONResponse(content=health_status, status_code=status_code)

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    if not settings.METRICS_ENABLED:
        return JSONResponse(content={"detail": "Metrics disabled"}, status_code=404)
    
    return Response(
        content=generate_latest(REGISTRY),
        media_type=CONTENT_TYPE_LATEST
    )

# Readiness check endpoint
@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    readiness_status = {
        "status": "ready",
        "service": settings.APP_NAME,
        "checks": {}
    }
    
    # Database readiness
    if check_db_connection():
        readiness_status["checks"]["database"] = "ready"
    else:
        readiness_status["status"] = "not_ready"
        readiness_status["checks"]["database"] = "not_ready"
    
    # Redis readiness
    try:
        from .deps import get_redis_client
        redis_client = get_redis_client()
        redis_client.ping()
        readiness_status["checks"]["redis"] = "ready"
    except Exception:
        readiness_status["status"] = "not_ready"
        readiness_status["checks"]["redis"] = "not_ready"
    
    status_code = 200 if readiness_status["status"] == "ready" else 503
    return JSONResponse(content=readiness_status, status_code=status_code)

# Liveness check endpoint
@app.get("/live")
async def liveness_check():
    """Liveness check endpoint."""
    return JSONResponse(content={
        "status": "alive",
        "service": settings.APP_NAME,
        "timestamp": time.time()
    })

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return JSONResponse(content={
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "System Software Service for managing ArchiMate 3.2 System Software elements",
        "documentation": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    })

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={"detail": "Not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Include routes
app.include_router(router, prefix="/api/v1")

# Instrument FastAPI with OpenTelemetry
if settings.OTEL_ENABLED:
    try:
        FastAPIInstrumentor.instrument_app(app)
        logger.info("FastAPI instrumented with OpenTelemetry")
    except Exception as e:
        logger.error(f"Failed to instrument FastAPI: {e}")

# Instrument SQLAlchemy with OpenTelemetry
if settings.OTEL_ENABLED:
    try:
        from .database import engine
        SQLAlchemyInstrumentor().instrument(engine=engine)
        logger.info("SQLAlchemy instrumented with OpenTelemetry")
    except Exception as e:
        logger.error(f"Failed to instrument SQLAlchemy: {e}")

# Instrument Redis with OpenTelemetry
if settings.OTEL_ENABLED:
    try:
        from .deps import get_redis_client
        redis_client = get_redis_client()
        RedisInstrumentor().instrument(redis_client)
        logger.info("Redis instrumented with OpenTelemetry")
    except Exception as e:
        logger.error(f"Failed to instrument Redis: {e}")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info(f"Shutting down {settings.APP_NAME}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.HOT_RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    ) 