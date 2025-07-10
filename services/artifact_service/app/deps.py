from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional, Dict, Any
import redis
import logging
from datetime import datetime, timedelta
import time

from .database import get_db_session
from .config import settings

logger = logging.getLogger(__name__)
security = HTTPBearer()

# Rate limiting storage
rate_limit_storage = {}

def get_redis_client() -> redis.Redis:
    """Get Redis client."""
    try:
        client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            socket_connect_timeout=settings.REDIS_TIMEOUT,
            socket_timeout=settings.REDIS_TIMEOUT
        )
        # Test connection
        client.ping()
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis connection failed"
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    redis_client: redis.Redis = Depends(get_redis_client)
) -> Dict[str, Any]:
    """Get current user from JWT token."""
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        
        # Extract user information
        user_id = payload.get("user_id")
        tenant_id = payload.get("tenant_id")
        role = payload.get("role")
        
        if not user_id or not tenant_id or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Check if user is active in Redis (optional session management)
        user_key = f"user_session:{tenant_id}:{user_id}"
        if redis_client.exists(user_key):
            # Update last activity
            redis_client.expire(user_key, settings.SESSION_TIMEOUT)
        
        return {
            "user_id": user_id,
            "tenant_id": tenant_id,
            "role": role,
            "permissions": get_user_permissions(role)
        }
        
    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )

def get_user_permissions(role: str) -> list:
    """Get user permissions based on role."""
    permissions_map = {
        "Owner": [
            "artifact:create", "artifact:read", "artifact:update", "artifact:delete",
            "artifact_link:create", "artifact_link:read", "artifact_link:update", "artifact_link:delete",
            "artifact:admin", "artifact_link:admin"
        ],
        "Admin": [
            "artifact:create", "artifact:read", "artifact:update", "artifact:delete",
            "artifact_link:create", "artifact_link:read", "artifact_link:update", "artifact_link:delete"
        ],
        "Editor": [
            "artifact:create", "artifact:read", "artifact:update",
            "artifact_link:create", "artifact_link:read", "artifact_link:update"
        ],
        "Viewer": [
            "artifact:read", "artifact_link:read"
        ]
    }
    return permissions_map.get(role, [])

def check_permission(user: Dict[str, Any], required_permission: str):
    """Check if user has required permission."""
    user_permissions = user.get("permissions", [])
    
    # Admin permissions override all
    if "artifact:admin" in user_permissions or "artifact_link:admin" in user_permissions:
        return True
    
    # Check specific permission
    if required_permission not in user_permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required: {required_permission}, Role: {user.get('role', 'Unknown')}"
        )

def rate_limit_dependency(
    request: Request,
    redis_client: redis.Redis = Depends(get_redis_client),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Rate limiting dependency."""
    user_id = current_user["user_id"]
    tenant_id = current_user["tenant_id"]
    
    # Create rate limit keys
    user_key = f"rate_limit:user:{tenant_id}:{user_id}"
    tenant_key = f"rate_limit:tenant:{tenant_id}"
    
    current_time = int(time.time())
    
    try:
        # Check user rate limit (100 requests per minute)
        user_requests = redis_client.get(user_key)
        if user_requests and int(user_requests) >= 100:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="User rate limit exceeded"
            )
        
        # Check tenant rate limit (1000 requests per hour)
        tenant_requests = redis_client.get(tenant_key)
        if tenant_requests and int(tenant_requests) >= 1000:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Tenant rate limit exceeded"
            )
        
        # Increment counters
        pipe = redis_client.pipeline()
        pipe.incr(user_key)
        pipe.expire(user_key, 60)  # 1 minute
        pipe.incr(tenant_key)
        pipe.expire(tenant_key, 3600)  # 1 hour
        pipe.execute()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Rate limiting error: {e}")
        # Continue without rate limiting if Redis fails
        pass

def get_db_with_rate_limit(
    db: Session = Depends(get_db_session),
    rate_limit = Depends(rate_limit_dependency)
) -> Session:
    """Get database session with rate limiting."""
    return db

def get_current_user_with_rate_limit(
    current_user: Dict[str, Any] = Depends(get_current_user),
    rate_limit = Depends(rate_limit_dependency)
) -> Dict[str, Any]:
    """Get current user with rate limiting."""
    return current_user

def get_redis_with_rate_limit(
    redis_client: redis.Redis = Depends(get_redis_client),
    rate_limit = Depends(rate_limit_dependency)
) -> redis.Redis:
    """Get Redis client with rate limiting."""
    return redis_client

# Optional dependencies for different permission levels
def require_artifact_admin(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Require artifact admin permissions."""
    check_permission(current_user, "artifact:admin")
    return current_user

def require_artifact_link_admin(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Require artifact link admin permissions."""
    check_permission(current_user, "artifact_link:admin")
    return current_user

def require_artifact_write(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Require artifact write permissions."""
    check_permission(current_user, "artifact:create")
    return current_user

def require_artifact_link_write(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Require artifact link write permissions."""
    check_permission(current_user, "artifact_link:create")
    return current_user

def require_artifact_read(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Require artifact read permissions."""
    check_permission(current_user, "artifact:read")
    return current_user

def require_artifact_link_read(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Require artifact link read permissions."""
    check_permission(current_user, "artifact_link:read")
    return current_user 