from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
import httpx
import asyncio
import time
import logging
from datetime import datetime
import os
import uuid
from typing import Optional

# Import enhanced modules
from app.routing import resolve_service, get_service_config, get_service_health_summary, get_service_metrics
from app.middleware import (
    AuthMiddleware, 
    RBACMiddleware, 
    RateLimitMiddleware, 
    LoggingMiddleware, 
    IdentityForwardingMiddleware
)
from app.observability import observability_manager
from app.service_registry import service_registry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enhanced middleware stack
middlewares = [
    Middleware(LoggingMiddleware),
    Middleware(AuthMiddleware),
    Middleware(RBACMiddleware),
    Middleware(RateLimitMiddleware, default_limit_per_minute=100),
    Middleware(IdentityForwardingMiddleware),
]

app = FastAPI(
    title="ReqArchitect Gateway Service",
    description="Enhanced API Gateway with dynamic routing, RBAC enforcement, and observability",
    version="2.0.0",
    middleware=middlewares
)

# Initialize app state
if not hasattr(app.state, 'start_time'):
    app.state.start_time = time.time()
if not hasattr(app.state, 'request_count'):
    app.state.request_count = 0
if not hasattr(app.state, 'error_count'):
    app.state.error_count = 0
if not hasattr(app.state, 'active_connections'):
    app.state.active_connections = 0

@app.get("/health")
def health():
    """Enhanced health check with service registry integration"""
    try:
        # Get service health summary
        health_summary = get_service_health_summary()
        
        return {
            "status": health_summary["overall_status"],
            "service": "gateway_service",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime": get_uptime(),
            "version": "2.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "service_health": health_summary
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "degraded",
            "service": "gateway_service",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime": get_uptime(),
            "version": "2.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "error": str(e)
        }

@app.get("/gateway-health")
def gateway_health():
    """Gateway-specific health endpoint with detailed service status"""
    try:
        health_summary = get_service_health_summary()
        service_metrics = get_service_metrics()
        
        return {
            "status": health_summary["overall_status"],
            "service": "gateway_service",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime": get_uptime(),
            "version": "2.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "service_health": health_summary,
            "service_metrics": service_metrics,
            "circuit_breaker_status": {
                "open_services": health_summary["services"],
                "healthy_count": health_summary["healthy_count"],
                "unhealthy_count": health_summary["unhealthy_count"]
            }
        }
    except Exception as e:
        logger.error(f"Gateway health check failed: {e}")
        return {
            "status": "degraded",
            "service": "gateway_service",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime": get_uptime(),
            "version": "2.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "error": str(e)
        }

@app.get("/metrics")
def get_metrics():
    """Enhanced Prometheus-style metrics endpoint"""
    try:
        service_metrics = get_service_metrics()
        observability_metrics = observability_manager.get_metrics()
        
        return {
            "gateway_uptime_seconds": get_uptime(),
            "gateway_requests_total": getattr(app.state, 'request_count', 0),
            "gateway_errors_total": getattr(app.state, 'error_count', 0),
            "gateway_active_connections": getattr(app.state, 'active_connections', 0),
            "service_metrics": service_metrics,
            "observability_metrics": observability_metrics
        }
    except Exception as e:
        logger.error(f"Metrics collection failed: {e}")
        return {
            "gateway_uptime_seconds": get_uptime(),
            "gateway_requests_total": getattr(app.state, 'request_count', 0),
            "gateway_errors_total": getattr(app.state, 'error_count', 0),
            "gateway_active_connections": getattr(app.state, 'active_connections', 0),
            "gateway_metrics_error": str(e)
        }

def get_uptime() -> float:
    """Get service uptime in seconds"""
    return time.time() - app.state.start_time

async def proxy_request_with_retry(
    request: Request, 
    target_url: str, 
    service_key: str,
    config: any,
    context: any
) -> Response:
    """
    Proxy request with retry logic and fault tolerance.
    
    Args:
        request: Original request
        target_url: Target service URL
        service_key: Service identifier
        config: Service configuration
        context: Request context for observability
        
    Returns:
        Proxied response
    """
    max_retries = config.retry_policy.get("max_retries", 3)
    backoff_ms = config.retry_policy.get("backoff_ms", 1000)
    timeout_ms = config.timeout_ms
    
    for attempt in range(max_retries + 1):
        try:
            # Log service proxy attempt
            observability_manager.log_service_proxy(context, service_key, target_url)
            
            # Prepare headers
            headers = dict(request.headers)
            headers["X-User-ID"] = getattr(request.state, "user_id", "")
            headers["X-Tenant-ID"] = getattr(request.state, "tenant_id", "")
            headers["X-Role"] = getattr(request.state, "role", "")
            headers["X-Request-ID"] = context.request_id
            headers["X-Correlation-ID"] = context.correlation_id
            
            # Remove host header to avoid conflicts
            headers.pop("host", None)
            
            # Forward request with timeout
            async with httpx.AsyncClient(timeout=timeout_ms / 1000.0) as client:
                start_time = time.time()
                
                # Trace service call
                async with observability_manager.trace_service_call(context, service_key, target_url):
                    response = await client.request(
                        method=request.method,
                        url=target_url,
                        headers=headers,
                        content=await request.body(),
                        params=request.query_params
                    )
                
                response_time = (time.time() - start_time) * 1000
                
                # Log service response
                observability_manager.log_service_response(context, service_key, response.status_code, response_time)
                
                # Return successful response
                return Response(
                    content=response.content,
                    status_code=response.status_code,
                    headers=dict(response.headers)
                )
                
        except httpx.TimeoutException:
            logger.warning(f"Timeout on attempt {attempt + 1} for {service_key}: {target_url}")
            if attempt == max_retries:
                raise HTTPException(status_code=504, detail=f"Service {service_key} timeout after {max_retries + 1} attempts")
            
        except httpx.HTTPStatusError as e:
            # Handle specific HTTP errors
            if e.response.status_code in [503, 504] and attempt < max_retries:
                logger.warning(f"Service {service_key} returned {e.response.status_code}, retrying...")
                await asyncio.sleep(backoff_ms / 1000.0 * (attempt + 1))
                continue
            else:
                # Return the error response
                return Response(
                    content=e.response.content,
                    status_code=e.response.status_code,
                    headers=dict(e.response.headers)
                )
                
        except Exception as e:
            logger.error(f"Unexpected error proxying to {service_key}: {e}")
            if attempt == max_retries:
                raise HTTPException(status_code=502, detail=f"Service {service_key} error: {str(e)}")
            
            await asyncio.sleep(backoff_ms / 1000.0 * (attempt + 1))
    
    # Should not reach here, but just in case
    raise HTTPException(status_code=502, detail=f"Service {service_key} failed after {max_retries + 1} attempts")

@app.get("/services")
def list_services():
    """List all available services and their status"""
    try:
        health_summary = get_service_health_summary()
        service_list = []
        
        for service_key, health in health_summary["services"].items():
            service_config = service_registry.get_service_config(service_key)
            if service_config:
                service_list.append({
                    "service_key": service_key,
                    "service_name": service_config.service_name,
                    "base_path": service_config.base_path,
                    "status": health["status"],
                    "last_check": health["last_check"],
                    "response_time_ms": health["response_time_ms"],
                    "consecutive_failures": health["consecutive_failures"]
                })
        
        return {
            "services": service_list,
            "total_services": len(service_list),
            "healthy_services": health_summary["healthy_count"],
            "unhealthy_services": health_summary["unhealthy_count"],
            "overall_status": health_summary["overall_status"]
        }
    except Exception as e:
        logger.error(f"Failed to list services: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve service list")

@app.get("/services/{service_key}/health")
def get_service_health(service_key: str):
    """Get health status for a specific service"""
    try:
        health = service_registry.health_status.get(service_key)
        if not health:
            raise HTTPException(status_code=404, detail=f"Service {service_key} not found")
        
        service_config = service_registry.get_service_config(service_key)
        
        return {
            "service_key": service_key,
            "service_name": service_config.service_name if service_config else "unknown",
            "status": health.status.value,
            "last_check": health.last_check.isoformat(),
            "response_time_ms": health.response_time_ms,
            "consecutive_failures": health.consecutive_failures,
            "error_message": health.error_message
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get service health for {service_key}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve service health")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def dynamic_proxy(request: Request, path: str):
    """
    Enhanced dynamic proxy with service registry integration.
    
    Routes requests to appropriate microservices based on service catalog.
    """
    try:
        # Increment request counter
        app.state.request_count += 1
        app.state.active_connections += 1
        
        # Create observability context
        context = observability_manager.create_request_context(
            method=request.method,
            path=f"/{path}",
            user_id=getattr(request.state, "user_id", None),
            tenant_id=getattr(request.state, "tenant_id", None),
            service_target=None  # Will be determined
        )
        
        # Store context in request state for middleware access
        request.state.observability_context = context
        
        # Resolve service using enhanced routing
        service_info = get_service_config(f"/{path}")
        if not service_info:
            app.state.error_count += 1
            raise HTTPException(status_code=404, detail=f"No service found for path: /{path}")
        
        service_key, config = service_info
        
        # Update context with service target
        context.service_target = service_key
        
        # Check if service is healthy
        if not service_registry.is_service_healthy(service_key):
            app.state.error_count += 1
            raise HTTPException(
                status_code=503, 
                detail=f"Service {service_key} is currently unavailable"
            )
        
        # Build target URL
        target_url = f"{config.internal_url}/{path}"
        
        # Proxy request with retry logic
        response = await proxy_request_with_retry(request, target_url, service_key, config, context)
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        app.state.error_count += 1
        logger.error(f"Unexpected error in dynamic proxy: {e}")
        raise HTTPException(status_code=500, detail="Internal gateway error")
    finally:
        app.state.active_connections -= 1

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
