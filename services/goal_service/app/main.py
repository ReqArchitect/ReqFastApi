from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from .routes import router
from .database import SessionLocal, engine
from .models import Base
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import time
import logging
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import uuid

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Goal Service",
    description="Microservice for managing ArchiMate 3.2 Goal elements",
    version="1.0.0"
)

# Logging setup
class JsonLogFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%fZ"),
            "service": "goal_service",
            "version": "1.0.0",
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, 'extra') and isinstance(record.extra, dict):
            log.update(record.extra)
        return json.dumps(log)

handler = logging.StreamHandler()
handler.setFormatter(JsonLogFormatter())
logger = logging.getLogger("goal_service")
logger.setLevel(logging.INFO)
logger.handlers = [handler]

# Prometheus metrics
REQUESTS_TOTAL = Counter(
    "goal_service_requests_total",
    "Total requests",
    ["method", "route", "status"]
)
REQUEST_LATENCY = Histogram(
    "goal_service_request_latency_seconds_bucket",
    "Request latency",
    ["method", "route"]
)
ERRORS_TOTAL = Counter(
    "goal_service_errors_total",
    "Total errors",
    ["method", "route"]
)

# OpenTelemetry tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer("goal_service")
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)
FastAPIInstrumentor.instrument_app(app)

start_time = time.time()
total_requests = 0
total_errors = 0

@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    global total_requests, total_errors
    start = time.time()
    route = request.url.path
    method = request.method
    
    # Extract correlation ID and tenant info
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    tenant_id = request.headers.get("X-Tenant-ID", "unknown")
    user_id = request.headers.get("X-User-ID", "unknown")
    
    # Start tracing span
    with tracer.start_as_current_span(f"{method} {route}") as span:
        span.set_attribute("tenant_id", tenant_id)
        span.set_attribute("user_id", user_id)
        span.set_attribute("correlation_id", correlation_id)
        
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            status_code = 500
            total_errors += 1
            ERRORS_TOTAL.labels(method=method, route=route).inc()
            logger.error(json.dumps({
                "error": str(e),
                "route": route,
                "method": method,
                "tenant_id": tenant_id,
                "user_id": user_id,
                "correlation_id": correlation_id
            }))
            raise
        
        latency = time.time() - start
        REQUESTS_TOTAL.labels(method=method, route=route, status=str(status_code)).inc()
        REQUEST_LATENCY.labels(method=method, route=route).observe(latency)
        total_requests += 1
        
        # Structured log
        logger.info(json.dumps({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
            "service": "goal_service",
            "version": "1.0.0",
            "tenant_id": tenant_id,
            "user_id": user_id,
            "correlation_id": correlation_id,
            "route": route,
            "method": method,
            "status_code": status_code,
            "latency_ms": int(latency * 1000)
        }))
        
        response.headers["X-Correlation-ID"] = correlation_id
        return response

@app.get("/metrics", include_in_schema=False)
async def metrics():
    """Prometheus metrics endpoint"""
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint"""
    uptime = time.time() - start_time
    error_rate = (total_errors / total_requests) if total_requests else 0.0
    
    # Check database connection
    db_connected = False
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_connected = True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
    
    return {
        "service": "goal_service",
        "version": "1.0.0",
        "status": "healthy",
        "uptime": f"{uptime:.2f}s",
        "total_requests": total_requests,
        "error_rate": error_rate,
        "database_connected": db_connected,
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with service information"""
    return {
        "service": "goal_service",
        "version": "1.0.0",
        "description": "Microservice for managing ArchiMate 3.2 Goal elements",
        "documentation": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }

# Include the router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 