from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
import os
from datetime import datetime
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import REGISTRY
import redis

# Import local modules
from .database import init_db, engine
from .routes import router
from .models import Base

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'assessment_service_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'assessment_service_http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

ASSESSMENT_OPERATIONS = Counter(
    'assessment_service_assessment_operations_total',
    'Total assessment operations',
    ['operation', 'status']
)

ASSESSMENT_LINK_OPERATIONS = Counter(
    'assessment_service_assessment_link_operations_total',
    'Total assessment link operations',
    ['operation', 'status']
)

# OpenTelemetry setup
def setup_telemetry():
    """Setup OpenTelemetry tracing"""
    try:
        # Initialize tracer provider
        trace.set_tracer_provider(TracerProvider())
        tracer = trace.get_tracer(__name__)
        
        # Setup OTLP exporter
        otlp_endpoint = os.getenv("OTLP_ENDPOINT", "http://localhost:4317")
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        
        # Setup batch processor
        span_processor = BatchSpanProcessor(otlp_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)
        
        # Instrument FastAPI
        FastAPIInstrumentor.instrument()
        
        # Instrument SQLAlchemy
        SQLAlchemyInstrumentor().instrument(engine=engine)
        
        # Instrument Redis
        RedisInstrumentor().instrument()
        
        logger.info("OpenTelemetry tracing configured successfully")
    except Exception as e:
        logger.warning(f"Failed to setup OpenTelemetry: {str(e)}")

# Redis setup
def setup_redis():
    """Setup Redis connection"""
    try:
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        redis_db = int(os.getenv("REDIS_DB", "0"))
        
        redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True
        )
        
        # Test connection
        redis_client.ping()
        logger.info("Redis connection established successfully")
        return redis_client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        return None

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Assessment Service...")
    
    # Setup telemetry
    setup_telemetry()
    
    # Setup Redis
    redis_client = setup_redis()
    app.state.redis = redis_client
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
    
    logger.info("Assessment Service started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Assessment Service...")
    if redis_client:
        redis_client.close()
    logger.info("Assessment Service shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="Assessment Service",
    description="ArchiMate 3.2 Assessment element management service for the Implementation & Migration Layer",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Request/Response middleware for metrics and logging
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware for metrics collection and request logging"""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Process request
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
        logger.error(f"Error processing request {request.method} {request.url}: {str(e)}")
        raise

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
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
    """Health check endpoint"""
    try:
        # Check database connection
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        # Check Redis connection
        redis_status = "connected" if app.state.redis and app.state.redis.ping() else "disconnected"
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "assessment_service",
            "version": "1.0.0",
            "database": "connected",
            "redis": redis_status
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "assessment_service",
            "version": "1.0.0",
            "error": str(e)
        }

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(REGISTRY)

# Include routers
app.include_router(router, prefix="/api/v1", tags=["assessments"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Assessment Service",
        "version": "1.0.0",
        "description": "ArchiMate 3.2 Assessment element management service",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }

# Export version for other modules
__version__ = "1.0.0"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    ) 