from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional
import redis
import logging
from datetime import datetime, timedelta

from .database import get_db_session
from .config import settings

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Rate limiting
class RateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
    
    async def check_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """Check rate limit for a given key."""
        try:
            current = self.redis_client.get(key)
            if current is None:
                self.redis_client.setex(key, window, 1)
                return True
            elif int(current) < limit:
                self.redis_client.incr(key)
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            return True  # Allow if Redis is unavailable

def get_redis_client() -> redis.Redis:
    """Get Redis client."""
    try:
        client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
        # Test connection
        client.ping()
        return client
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cache service unavailable"
        )

def get_rate_limiter(redis_client: redis.Redis = Depends(get_redis_client)) -> RateLimiter:
    """Get rate limiter instance."""
    return RateLimiter(redis_client)

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token and return user information."""
    try:
        payload = jwt.decode(
            credentials.credentials,
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
        
        # Extract required claims
        tenant_id = payload.get("tenant_id")
        user_id = payload.get("user_id")
        role = payload.get("role")
        
        if not all([tenant_id, user_id, role]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims"
            )
        
        return {
            "tenant_id": tenant_id,
            "user_id": user_id,
            "role": role,
            "permissions": payload.get("permissions", [])
        }
    except JWTError as e:
        logger.error(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

async def get_current_user(token_data: dict = Depends(verify_token)) -> dict:
    """Get current authenticated user."""
    return token_data

async def check_permissions(user: dict, required_permission: str) -> None:
    """Check if user has required permission."""
    user_role = user.get("role", "")
    user_permissions = user.get("permissions", [])
    
    # Define role-based permissions
    role_permissions = {
        "Owner": [
            "node:create", "node:read", "node:update", "node:delete",
            "node_link:create", "node_link:read", "node_link:update", "node_link:delete"
        ],
        "Admin": [
            "node:create", "node:read", "node:update", "node:delete",
            "node_link:create", "node_link:read", "node_link:update", "node_link:delete"
        ],
        "Editor": [
            "node:create", "node:read", "node:update",
            "node_link:create", "node_link:read", "node_link:update"
        ],
        "Viewer": [
            "node:read",
            "node_link:read"
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

async def check_rate_limit(
    request: Request,
    rate_limiter: RateLimiter = Depends(get_rate_limiter)
) -> None:
    """Check rate limit for the request."""
    # Get client IP
    client_ip = request.client.host
    
    # Check tenant-level rate limit
    tenant_key = f"rate_limit:tenant:{client_ip}"
    if not await rate_limiter.check_rate_limit(tenant_key, 1000, 3600):  # 1000 requests per hour
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded for tenant"
        )
    
    # Check user-level rate limit
    user_key = f"rate_limit:user:{client_ip}"
    if not await rate_limiter.check_rate_limit(user_key, 100, 60):  # 100 requests per minute
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded for user"
        )

def get_db() -> Session:
    """Get database session."""
    return get_db_session()

# Optional dependencies for endpoints that don't require authentication
async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """Get current user if authenticated, otherwise None."""
    if not credentials:
        return None
    
    try:
        return await verify_token(credentials)
    except HTTPException:
        return None

# Health check dependencies
def get_health_dependencies():
    """Get dependencies for health check endpoints."""
    return {
        "database": get_db,
        "redis": get_redis_client
    } 