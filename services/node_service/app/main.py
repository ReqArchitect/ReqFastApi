from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
import os
from datetime import datetime

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

# Prometheus metrics
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from .config import settings
from .database import init_db, check_db_connection
from .deps import get_redis_client

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
    'node_service_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'node_service_request_duration_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)

# OpenTelemetry setup
def setup_telemetry():
    """Setup OpenTelemetry tracing."""
    if not settings.OTEL_ENABLED:
        return
    
    try:
        # Set up the tracer provider
        provider = TracerProvider()
        trace.set_tracer_provider(provider)
        
        # Set up the OTLP exporter
        otlp_exporter = OTLPSpanExporter(endpoint=settings.OTEL_ENDPOINT)
        
        # Add the BatchSpanProcessor to the tracer
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        
        # Instrument FastAPI
        FastAPIInstrumentor.instrument_app(
            app,
            tracer_provider=provider,
            service_name=settings.OTEL_SERVICE_NAME,
            service_version=settings.OTEL_SERVICE_VERSION
        )
        
        # Instrument SQLAlchemy
        SQLAlchemyInstrumentor().instrument()
        
        # Instrument Redis
        RedisInstrumentor().instrument()
        
        logger.info("OpenTelemetry instrumentation enabled")
    except Exception as e:
        logger.error(f"Failed to setup OpenTelemetry: {e}")

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
    
    # Setup telemetry
    setup_telemetry()
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")

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

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Request/Response middleware for metrics
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware to collect metrics."""
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate latency
    latency = time.time() - start_time
    
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
    
    return response

# Error handling middleware
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }
    
    # Check database connection
    try:
        db_healthy = check_db_connection()
        health_status["database"] = "healthy" if db_healthy else "unhealthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["database"] = "unhealthy"
    
    # Check Redis connection
    try:
        redis_client = get_redis_client()
        redis_client.ping()
        health_status["redis"] = "healthy"
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        health_status["redis"] = "unhealthy"
    
    # Determine overall health
    overall_health = all([
        health_status["database"] == "healthy",
        health_status["redis"] == "healthy"
    ])
    
    status_code = 200 if overall_health else 503
    health_status["status"] = "healthy" if overall_health else "unhealthy"
    
    return JSONResponse(
        status_code=status_code,
        content=health_status
    )

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    if not settings.PROMETHEUS_ENABLED:
        return JSONResponse(
            status_code=404,
            content={"detail": "Metrics endpoint disabled"}
        )
    
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
        "description": settings.API_DOCS_DESCRIPTION,
        "archimate": {
            "version": settings.ARCHIMATE_VERSION,
            "layer": settings.ARCHIMATE_LAYER,
            "element": settings.ARCHIMATE_ELEMENT
        },
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

# Include routers
from .routes import router as node_router
app.include_router(node_router)

# Maintenance mode check
@app.middleware("http")
async def maintenance_mode_middleware(request: Request, call_next):
    """Middleware to handle maintenance mode."""
    if settings.MAINTENANCE_MODE and request.url.path not in ["/health", "/metrics"]:
        return JSONResponse(
            status_code=503,
            content={
                "detail": settings.MAINTENANCE_MESSAGE,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    return await call_next(request)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info(f"{settings.APP_NAME} started successfully")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"API documentation: {'enabled' if settings.API_DOCS_ENABLED else 'disabled'}")

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