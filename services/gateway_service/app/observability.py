import logging
import time
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import json
from contextlib import asynccontextmanager

# OpenTelemetry imports (would be installed via requirements.txt)
try:
    from opentelemetry import trace
    from opentelemetry.trace import Status, StatusCode
    from opentelemetry.trace.span import Span
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    trace = None
    Status = None
    StatusCode = None
    Span = None

logger = logging.getLogger(__name__)

@dataclass
class RequestContext:
    """Request context for observability"""
    request_id: str
    correlation_id: str
    user_id: Optional[str]
    tenant_id: Optional[str]
    service_target: Optional[str]
    method: str
    path: str
    start_time: float
    end_time: Optional[float] = None
    status_code: Optional[int] = None
    latency_ms: Optional[float] = None
    error_message: Optional[str] = None

class ObservabilityManager:
    """Centralized observability management for gateway service"""
    
    def __init__(self):
        self.tracer = None
        self._setup_opentelemetry()
        self._setup_logging()
    
    def _setup_opentelemetry(self):
        """Setup OpenTelemetry tracing if available"""
        if not OPENTELEMETRY_AVAILABLE:
            logger.warning("OpenTelemetry not available, tracing disabled")
            return
        
        try:
            # Setup tracer provider
            provider = TracerProvider()
            
            # Setup Jaeger exporter (configure via environment)
            jaeger_host = "localhost"  # Would be from env
            jaeger_port = 6831  # Would be from env
            jaeger_exporter = JaegerExporter(
                agent_host_name=jaeger_host,
                agent_port=jaeger_port,
            )
            
            # Add span processor
            provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
            
            # Set global tracer provider
            trace.set_tracer_provider(provider)
            
            # Get tracer
            self.tracer = trace.get_tracer(__name__)
            
            logger.info("OpenTelemetry tracing initialized")
            
        except Exception as e:
            logger.error(f"Failed to setup OpenTelemetry: {e}")
            self.tracer = None
    
    def _setup_logging(self):
        """Setup structured logging"""
        # Configure JSON logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def create_request_context(
        self,
        method: str,
        path: str,
        user_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        service_target: Optional[str] = None
    ) -> RequestContext:
        """Create request context for observability"""
        request_id = str(uuid.uuid4())
        correlation_id = str(uuid.uuid4())
        
        return RequestContext(
            request_id=request_id,
            correlation_id=correlation_id,
            user_id=user_id,
            tenant_id=tenant_id,
            service_target=service_target,
            method=method,
            path=path,
            start_time=time.time()
        )
    
    def log_request_start(self, context: RequestContext):
        """Log request start"""
        log_data = {
            "event": "request_start",
            "request_id": context.request_id,
            "correlation_id": context.correlation_id,
            "method": context.method,
            "path": context.path,
            "user_id": context.user_id,
            "tenant_id": context.tenant_id,
            "service_target": context.service_target,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Request started: {json.dumps(log_data)}")
    
    def log_request_end(self, context: RequestContext, status_code: int, error_message: Optional[str] = None):
        """Log request end with metrics"""
        context.end_time = time.time()
        context.status_code = status_code
        context.latency_ms = (context.end_time - context.start_time) * 1000
        context.error_message = error_message
        
        log_data = {
            "event": "request_end",
            "request_id": context.request_id,
            "correlation_id": context.correlation_id,
            "method": context.method,
            "path": context.path,
            "user_id": context.user_id,
            "tenant_id": context.tenant_id,
            "service_target": context.service_target,
            "status_code": status_code,
            "latency_ms": round(context.latency_ms, 2),
            "error_message": error_message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if status_code >= 400:
            logger.error(f"Request failed: {json.dumps(log_data)}")
        else:
            logger.info(f"Request completed: {json.dumps(log_data)}")
    
    def log_service_proxy(self, context: RequestContext, target_service: str, target_url: str):
        """Log service proxy attempt"""
        log_data = {
            "event": "service_proxy",
            "request_id": context.request_id,
            "correlation_id": context.correlation_id,
            "service_target": target_service,
            "target_url": target_url,
            "user_id": context.user_id,
            "tenant_id": context.tenant_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Proxying to service: {json.dumps(log_data)}")
    
    def log_service_response(self, context: RequestContext, target_service: str, status_code: int, latency_ms: float):
        """Log service response"""
        log_data = {
            "event": "service_response",
            "request_id": context.request_id,
            "correlation_id": context.correlation_id,
            "service_target": target_service,
            "status_code": status_code,
            "latency_ms": round(latency_ms, 2),
            "user_id": context.user_id,
            "tenant_id": context.tenant_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Service response: {json.dumps(log_data)}")
    
    def log_rbac_decision(self, context: RequestContext, service: str, method: str, allowed: bool, role: str):
        """Log RBAC decision"""
        log_data = {
            "event": "rbac_decision",
            "request_id": context.request_id,
            "correlation_id": context.correlation_id,
            "service": service,
            "method": method,
            "allowed": allowed,
            "role": role,
            "user_id": context.user_id,
            "tenant_id": context.tenant_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if allowed:
            logger.info(f"RBAC access granted: {json.dumps(log_data)}")
        else:
            logger.warning(f"RBAC access denied: {json.dumps(log_data)}")
    
    def log_health_check(self, service: str, status: str, response_time_ms: Optional[float] = None, error: Optional[str] = None):
        """Log health check result"""
        log_data = {
            "event": "health_check",
            "service": service,
            "status": status,
            "response_time_ms": response_time_ms,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if status == "healthy":
            logger.info(f"Health check passed: {json.dumps(log_data)}")
        else:
            logger.warning(f"Health check failed: {json.dumps(log_data)}")
    
    def log_circuit_breaker(self, service: str, action: str, consecutive_failures: int):
        """Log circuit breaker events"""
        log_data = {
            "event": "circuit_breaker",
            "service": service,
            "action": action,  # "open", "close", "half_open"
            "consecutive_failures": consecutive_failures,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.warning(f"Circuit breaker event: {json.dumps(log_data)}")
    
    @asynccontextmanager
    async def trace_request(self, context: RequestContext):
        """Context manager for request tracing"""
        if not self.tracer:
            yield
            return
        
        span_name = f"{context.method} {context.path}"
        
        with self.tracer.start_as_current_span(span_name) as span:
            # Add attributes to span
            span.set_attribute("http.method", context.method)
            span.set_attribute("http.url", context.path)
            span.set_attribute("http.request_id", context.request_id)
            span.set_attribute("http.correlation_id", context.correlation_id)
            
            if context.user_id:
                span.set_attribute("user.id", context.user_id)
            if context.tenant_id:
                span.set_attribute("tenant.id", context.tenant_id)
            if context.service_target:
                span.set_attribute("service.target", context.service_target)
            
            try:
                yield span
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise
            else:
                span.set_status(Status(StatusCode.OK))
    
    @asynccontextmanager
    async def trace_service_call(self, context: RequestContext, target_service: str, target_url: str):
        """Context manager for service call tracing"""
        if not self.tracer:
            yield
            return
        
        span_name = f"service_proxy.{target_service}"
        
        with self.tracer.start_as_current_span(span_name) as span:
            # Add attributes to span
            span.set_attribute("service.name", target_service)
            span.set_attribute("http.url", target_url)
            span.set_attribute("http.request_id", context.request_id)
            span.set_attribute("http.correlation_id", context.correlation_id)
            
            if context.user_id:
                span.set_attribute("user.id", context.user_id)
            if context.tenant_id:
                span.set_attribute("tenant.id", context.tenant_id)
            
            try:
                yield span
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise
            else:
                span.set_status(Status(StatusCode.OK))
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics for monitoring"""
        # This would integrate with Prometheus or similar
        # For now, return basic metrics structure
        return {
            "gateway_requests_total": 0,  # Would be from counter
            "gateway_requests_duration_seconds": 0.0,  # Would be from histogram
            "gateway_requests_failed_total": 0,  # Would be from counter
            "gateway_service_calls_total": 0,  # Would be from counter
            "gateway_service_calls_duration_seconds": 0.0,  # Would be from histogram
            "gateway_service_calls_failed_total": 0,  # Would be from counter
            "gateway_rbac_denials_total": 0,  # Would be from counter
            "gateway_circuit_breaker_open_total": 0,  # Would be from counter
            "gateway_health_checks_total": 0,  # Would be from counter
            "gateway_health_checks_failed_total": 0,  # Would be from counter
        }

# Global observability manager instance
observability_manager = ObservabilityManager() 