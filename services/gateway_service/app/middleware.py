import time
import jwt
import logging
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from app.rbac import rbac_validator, RBACContext
from app.observability import observability_manager, RequestContext
from app.routing import get_service_config

logger = logging.getLogger(__name__)

# JWT configuration
SECRET_KEY = "REPLACE_WITH_REAL_SECRET"
ALGORITHM = "HS256"

# In-memory rate limit store (for demo)
rate_limit_store = defaultdict(list)

class AuthMiddleware(BaseHTTPMiddleware):
    """Enhanced authentication middleware with JWT decoding and identity forwarding"""
    
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for health checks and metrics
        if request.url.path in ["/health", "/metrics", "/gateway-health"]:
            response = await call_next(request)
            return response
        
        # Extract and validate JWT token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
        
        token = auth_header.split(" ", 1)[1]
        try:
            # Decode JWT token (no regeneration)
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            # Extract user information
            user_id = payload.get("user_id")
            tenant_id = payload.get("tenant_id")
            role = payload.get("role", "Viewer")
            
            if not user_id or not tenant_id:
                raise HTTPException(status_code=401, detail="Invalid token: missing user_id or tenant_id")
            
            # Store in request state for downstream use
            request.state.user_id = user_id
            request.state.tenant_id = tenant_id
            request.state.role = role
            request.state.jwt_payload = payload
            
            logger.debug(f"JWT decoded successfully for user {user_id} (tenant: {tenant_id}, role: {role})")
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            logger.error(f"JWT decoding error: {e}")
            raise HTTPException(status_code=401, detail="Token validation failed")
        
        response = await call_next(request)
        return response

class RBACMiddleware(BaseHTTPMiddleware):
    """Non-intrusive RBAC enforcement middleware"""
    
    async def dispatch(self, request: Request, call_next):
        # Skip RBAC for health checks and metrics
        if request.url.path in ["/health", "/metrics", "/gateway-health"]:
            response = await call_next(request)
            return response
        
        # Get user context
        user_id = getattr(request.state, "user_id", None)
        tenant_id = getattr(request.state, "tenant_id", None)
        role = getattr(request.state, "role", "Viewer")
        
        if not user_id or not tenant_id:
            raise HTTPException(status_code=401, detail="Missing user context")
        
        # Create RBAC context
        rbac_context = rbac_validator.create_context(user_id, tenant_id, role)
        
        # Determine target service from path
        path = request.url.path
        service_info = get_service_config(path)
        
        if service_info:
            service_key, config = service_info
            
            # Check if RBAC is required for this service
            if config.rbac_required:
                # Extract service name from service key
                service_name = service_key.replace("_", "")
                
                # Validate permission
                has_permission = rbac_validator.validate_request_permission(
                    rbac_context, service_name, request.method
                )
                
                # Log RBAC decision
                observability_manager.log_rbac_decision(
                    RequestContext(
                        request_id="",  # Will be set by observability
                        correlation_id="",
                        user_id=user_id,
                        tenant_id=tenant_id,
                        service_target=service_name,
                        method=request.method,
                        path=path,
                        start_time=time.time()
                    ),
                    service_name,
                    request.method,
                    has_permission,
                    role
                )
                
                if not has_permission:
                    raise HTTPException(
                        status_code=403, 
                        detail=f"Insufficient permissions. Required: {service_name}:{request.method.lower()}, Role: {role}"
                    )
        
        response = await call_next(request)
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Enhanced rate limiting middleware with service-specific limits"""
    
    def __init__(self, app, default_limit_per_minute=100):
        super().__init__(app)
        self.default_limit_per_minute = default_limit_per_minute

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        user_id = getattr(request.state, "user_id", None)
        
        if not user_id:
            response = await call_next(request)
            return response
        
        # Get service-specific rate limit
        service_info = get_service_config(path)
        rate_limit = self.default_limit_per_minute
        
        if service_info:
            service_key, config = service_info
            rate_limit = config.rate_limit.get("requests_per_minute", self.default_limit_per_minute)
        
        # Apply rate limiting
        now = time.time()
        window = 60  # 1 minute window
        timestamps = rate_limit_store[user_id]
        
        # Remove old timestamps
        rate_limit_store[user_id] = [t for t in timestamps if now - t < window]
        
        if len(rate_limit_store[user_id]) >= rate_limit:
            logger.warning(f"Rate limit exceeded for user {user_id}: {len(rate_limit_store[user_id])} requests in {window}s")
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        rate_limit_store[user_id].append(now)
        
        response = await call_next(request)
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    """Enhanced logging middleware with structured logging and observability"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Create request context for observability
        context = observability_manager.create_request_context(
            method=request.method,
            path=str(request.url.path),
            user_id=getattr(request.state, "user_id", None),
            tenant_id=getattr(request.state, "tenant_id", None),
            service_target=None  # Will be determined during routing
        )
        
        # Log request start
        observability_manager.log_request_start(context)
        
        try:
            # Process request with tracing
            async with observability_manager.trace_request(context):
                response = await call_next(request)
                
                # Log request end
                observability_manager.log_request_end(context, response.status_code)
                
                return response
                
        except Exception as e:
            # Log request failure
            observability_manager.log_request_end(context, 500, str(e))
            raise
        finally:
            # Calculate and log latency
            latency = (time.time() - start_time) * 1000
            logger.info(f"{request.method} {request.url.path} {getattr(response, 'status_code', 500)} {latency:.2f}ms")

class IdentityForwardingMiddleware(BaseHTTPMiddleware):
    """Middleware to forward identity information to downstream services"""
    
    async def dispatch(self, request: Request, call_next):
        # Forward identity headers to downstream services
        headers = dict(request.headers)
        
        # Add identity headers
        if hasattr(request.state, "user_id"):
            headers["X-User-ID"] = request.state.user_id
        if hasattr(request.state, "tenant_id"):
            headers["X-Tenant-ID"] = request.state.tenant_id
        if hasattr(request.state, "role"):
            headers["X-Role"] = request.state.role
        if hasattr(request.state, "jwt_payload"):
            # Forward original JWT token
            headers["X-JWT-Payload"] = str(request.state.jwt_payload)
        
        # Add correlation headers for tracing
        if hasattr(request.state, "request_id"):
            headers["X-Request-ID"] = request.state.request_id
        if hasattr(request.state, "correlation_id"):
            headers["X-Correlation-ID"] = request.state.correlation_id
        
        # Update request headers
        request._headers = headers
        
        response = await call_next(request)
        return response
