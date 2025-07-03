import time
import logging
import json
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from .routes import router
from .services import get_service_version
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import uuid

app = FastAPI(title="Architecture Suite Service", version=get_service_version())

# Logging setup
class JsonLogFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%fZ"),
            "service": "architecture_suite",
            "version": "1.0.0",
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, 'extra') and isinstance(record.extra, dict):
            log.update(record.extra)
        return json.dumps(log)

handler = logging.StreamHandler()
handler.setFormatter(JsonLogFormatter())
logger = logging.getLogger("architecture_suite")
logger.setLevel(logging.INFO)
logger.handlers = [handler]

# Prometheus metrics
REQUESTS_TOTAL = Counter(
    "architecture_suite_requests_total",
    "Total requests",
    ["method", "route", "status"]
)
REQUEST_LATENCY = Histogram(
    "architecture_suite_request_latency_seconds_bucket",
    "Request latency",
    ["method", "route"]
)
ERRORS_TOTAL = Counter(
    "architecture_suite_errors_total",
    "Total errors",
    ["method", "route"]
)

# OpenTelemetry tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer("architecture_suite")
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)
FastAPIInstrumentor.instrument_app(app)

start_time = time.time()
total_requests = 0
total_errors = 0

@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    import time
    global total_requests, total_errors
    start = time.time()
    route = request.url.path
    method = request.method
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
            "service": "architecture_suite",
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
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health", tags=["Health"])
async def health():
    uptime = time.time() - start_time
    error_rate = (total_errors / total_requests) if total_requests else 0.0
    return {
        "service": "architecture_suite",
        "version": get_service_version(),
        "uptime": f"{uptime:.2f}s",
        "total_requests": total_requests,
        "error_rate": error_rate
    }

app.include_router(router)
