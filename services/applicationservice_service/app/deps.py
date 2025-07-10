from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from typing import Optional
import jwt
import redis
import logging
from functools import wraps

from .database import get_db_session
from .config import settings

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Redis client
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

def get_redis_client():
    """Get Redis client instance."""
    return redis_client

def get_db():
    """Get database session."""
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()

def verify_jwt_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token expired")
        return None
    except jwt.JWTError as e:
        logger.error(f"JWT verification failed: {e}")
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Get current authenticated user from JWT token."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header"
        )
    
    token = credentials.credentials
    payload = verify_jwt_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Extract required claims
    tenant_id = payload.get("tenant_id")
    user_id = payload.get("user_id")
    role = payload.get("role")
    
    if not all([tenant_id, user_id, role]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing required claims in token"
        )
    
    return {
        "tenant_id": tenant_id,
        "user_id": user_id,
        "role": role,
        "email": payload.get("email"),
        "permissions": payload.get("permissions", [])
    }

async def check_permissions(user: dict, required_permission: str):
    """Check if user has required permission."""
    user_role = user.get("role", "").lower()
    user_permissions = user.get("permissions", [])
    
    # Role-based permission mapping
    role_permissions = {
        "owner": [
            "application_service:create", "application_service:read", 
            "application_service:update", "application_service:delete",
            "application_service:admin"
        ],
        "admin": [
            "application_service:create", "application_service:read", 
            "application_service:update", "application_service:delete"
        ],
        "editor": [
            "application_service:create", "application_service:read", 
            "application_service:update"
        ],
        "viewer": [
            "application_service:read"
        ]
    }
    
    # Check if user has the required permission
    has_permission = (
        required_permission in user_permissions or
        required_permission in role_permissions.get(user_role, [])
    )
    
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required: {required_permission}, Role: {user_role}"
        )

def require_owner_role(user: dict = Depends(get_current_user)):
    """Require owner role for endpoint access."""
    if user.get("role", "").lower() != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Owner role required"
        )
    return user

def require_admin_role(user: dict = Depends(get_current_user)):
    """Require admin or owner role for endpoint access."""
    user_role = user.get("role", "").lower()
    if user_role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or owner role required"
        )
    return user

def require_editor_role(user: dict = Depends(get_current_user)):
    """Require editor, admin, or owner role for endpoint access."""
    user_role = user.get("role", "").lower()
    if user_role not in ["owner", "admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Editor, admin, or owner role required"
        )
    return user

# Rate limiting decorator
def rate_limit(max_requests: int, window_seconds: int):
    """Rate limiting decorator."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract user info for rate limiting
            user = kwargs.get('current_user')
            if not user:
                return await func(*args, **kwargs)
            
            user_id = user.get("user_id")
            tenant_id = user.get("tenant_id")
            
            # Create rate limit key
            rate_limit_key = f"rate_limit:{tenant_id}:{user_id}:{func.__name__}"
            
            # Check current request count
            current_count = redis_client.get(rate_limit_key)
            if current_count and int(current_count) >= max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds."
                )
            
            # Increment request count
            pipe = redis_client.pipeline()
            pipe.incr(rate_limit_key)
            pipe.expire(rate_limit_key, window_seconds)
            pipe.execute()
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Health check dependency
def get_health_status():
    """Get health status for the service."""
    try:
        # Check database connection
        db = get_db_session()
        db.execute("SELECT 1")
        db.close()
        
        # Check Redis connection
        redis_client.ping()
        
        return {
            "status": "healthy",
            "database": "connected",
            "redis": "connected",
            "timestamp": "2024-01-15T10:30:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2024-01-15T10:30:00Z"
        } 