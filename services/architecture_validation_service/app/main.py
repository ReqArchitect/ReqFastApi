from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
from datetime import datetime
import os

from app.database import init_db
from app.routes import router
from app.deps import get_redis_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Architecture Validation Service",
    description="Validates and scores tenant-specific architecture models for alignment, traceability, and completeness",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request logging"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        # Log response
        process_time = (time.time() - start_time) * 1000
        logger.info(f"Response: {response.status_code} - {process_time:.2f}ms")
        
        return response

app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    try:
        # Initialize database
        init_db()
        logger.info("Database initialized successfully")
        
        # Test Redis connection
        redis_client = get_redis_client()
        redis_client.ping()
        logger.info("Redis connection established")
        
        logger.info("Architecture Validation Service started successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Architecture Validation Service shutting down")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Architecture Validation Service",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Redis connection
        redis_client = get_redis_client()
        redis_client.ping()
        
        return {
            "status": "healthy",
            "service": "architecture_validation_service",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "dependencies": {
                "redis": "connected",
                "database": "connected"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "architecture_validation_service",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

@app.get("/metrics")
async def get_metrics():
    """Get service metrics"""
    return {
        "validation_cycles_total": 0,
        "validation_issues_total": 0,
        "validation_rules_active": 0,
        "validation_exceptions_total": 0,
        "average_maturity_score": 0.0,
        "uptime_seconds": 0,
        "requests_total": 0,
        "errors_total": 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 