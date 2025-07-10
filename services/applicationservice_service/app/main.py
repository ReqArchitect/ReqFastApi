from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import logging
import uvicorn
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

from .config import settings
from .routes import router
from .deps import get_health_status
from .database import engine
import os

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# OpenTelemetry setup
def setup_telemetry():
    """Setup OpenTelemetry tracing."""
    if settings.OTEL_ENABLED:
        try:
            # Create tracer provider
            tracer_provider = TracerProvider()
            trace.set_tracer_provider(tracer_provider)
            
            # Create OTLP exporter
            otlp_exporter = OTLPSpanExporter(endpoint=settings.OTEL_ENDPOINT)
            
            # Add span processor
            tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
            
            # Instrument FastAPI
            FastAPIInstrumentor.instrument_app(app)
            
            # Instrument SQLAlchemy
            SQLAlchemyInstrumentor().instrument(engine=engine)
            
            # Instrument Redis
            RedisInstrumentor().instrument()
            
            logger.info("OpenTelemetry tracing enabled")
        except Exception as e:
            logger.warning(f"Failed to setup OpenTelemetry: {e}")

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    setup_telemetry()
    
    # Health check
    try:
        health_status = get_health_status()
        if health_status["status"] == "healthy":
            logger.info("Service health check passed")
        else:
            logger.warning(f"Service health check failed: {health_status}")
    except Exception as e:
        logger.error(f"Health check failed: {e}")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")

# Create FastAPI app
app = FastAPI(
    title=settings.API_DOCS_TITLE,
    description=settings.API_DOCS_DESCRIPTION,
    version=settings.API_DOCS_VERSION,
    debug=settings.DEBUG,
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
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Request/Response middleware for logging and timing
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log request details and timing."""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
    
    # Add timing header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return get_health_status()

# Metrics endpoint
@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Metrics endpoint for Prometheus."""
    if not settings.METRICS_ENABLED:
        return {"detail": "Metrics disabled"}
    
    # Basic metrics - could be enhanced with Prometheus client
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy",
        "timestamp": time.time()
    }

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Application Service API for ArchiMate 3.2",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }

# Include application routes
app.include_router(router)

# Additional utility endpoints

@app.get("/info", tags=["Info"])
async def service_info():
    """Get service information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Application Service API for managing ArchiMate 3.2 Application Service elements",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "features": [
            "CRUD operations for Application Services",
            "Service link management",
            "Performance analysis and scoring",
            "Impact mapping and dependency analysis",
            "Business alignment assessment",
            "Technical debt analysis",
            "Compliance status tracking",
            "Redis event emission",
            "OpenTelemetry tracing",
            "Multi-tenancy support",
            "RBAC with JWT authentication"
        ],
        "archimate_layer": "Application Layer",
        "archimate_element": "Application Service",
        "archimate_version": "3.2"
    }

@app.get("/capabilities", tags=["Capabilities"])
async def service_capabilities():
    """Get service capabilities."""
    return {
        "core_features": {
            "application_service_management": {
                "description": "Full CRUD operations for Application Service elements",
                "endpoints": [
                    "POST /application-services/",
                    "GET /application-services/",
                    "GET /application-services/{service_id}",
                    "PUT /application-services/{service_id}",
                    "DELETE /application-services/{service_id}"
                ]
            },
            "service_link_management": {
                "description": "Manage relationships between application services and other elements",
                "endpoints": [
                    "POST /application-services/{service_id}/links",
                    "GET /application-services/{service_id}/links",
                    "GET /application-services/links/{link_id}",
                    "PUT /application-services/links/{link_id}",
                    "DELETE /application-services/links/{link_id}"
                ]
            },
            "analysis_and_insights": {
                "description": "Comprehensive analysis capabilities",
                "endpoints": [
                    "GET /application-services/{service_id}/impact-map",
                    "GET /application-services/{service_id}/performance-score",
                    "GET /application-services/{service_id}/analysis"
                ]
            },
            "domain_specific_queries": {
                "description": "Specialized queries for common use cases",
                "endpoints": [
                    "GET /application-services/by-type/{service_type}",
                    "GET /application-services/by-status/{status}",
                    "GET /application-services/by-capability/{capability_id}",
                    "GET /application-services/by-performance/{performance_threshold}",
                    "GET /application-services/active",
                    "GET /application-services/critical"
                ]
            },
            "enumeration_endpoints": {
                "description": "Get available values for dropdowns and validation",
                "endpoints": [
                    "GET /application-services/service-types",
                    "GET /application-services/statuses",
                    "GET /application-services/business-criticalities",
                    "GET /application-services/business-values",
                    "GET /application-services/delivery-channels",
                    "GET /application-services/authentication-methods",
                    "GET /application-services/deployment-models",
                    "GET /application-services/scaling-strategies",
                    "GET /application-services/security-levels",
                    "GET /application-services/data-classifications",
                    "GET /application-services/link-types",
                    "GET /application-services/relationship-strengths",
                    "GET /application-services/dependency-levels",
                    "GET /application-services/interaction-frequencies",
                    "GET /application-services/interaction-types",
                    "GET /application-services/data-flow-directions",
                    "GET /application-services/performance-impacts"
                ]
            }
        },
        "archimate_integration": {
            "layer": "Application Layer",
            "element_type": "Application Service",
            "relationships": [
                "realizes Application Function",
                "supports Business Process",
                "enables Capability",
                "consumes Data Object",
                "produces Data Object",
                "requires Application Function",
                "triggers Business Process"
            ],
            "properties": [
                "service_type",
                "delivery_channel",
                "authentication_method",
                "latency_target_ms",
                "availability_target_pct",
                "business_criticality",
                "business_value",
                "security_level",
                "deployment_model",
                "scaling_strategy"
            ]
        },
        "observability": {
            "health_checks": "/health",
            "metrics": "/metrics",
            "tracing": "OpenTelemetry integration",
            "logging": "Structured logging with configurable levels",
            "monitoring": "Performance and availability metrics"
        },
        "security": {
            "authentication": "JWT-based authentication",
            "authorization": "Role-based access control (RBAC)",
            "multi_tenancy": "Tenant isolation",
            "rate_limiting": "Configurable rate limiting per user/tenant",
            "input_validation": "Pydantic schema validation"
        },
        "event_integration": {
            "redis_events": "Real-time event emission",
            "event_types": [
                "application_service_created",
                "application_service_updated",
                "application_service_deleted",
                "service_link_created",
                "service_link_updated",
                "service_link_deleted"
            ]
        }
    }

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    ) 