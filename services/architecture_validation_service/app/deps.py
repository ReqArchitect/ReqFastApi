import jwt
import redis
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
import os
import logging

logger = logging.getLogger(__name__)

# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "REPLACE_WITH_REAL_SECRET")
ALGORITHM = "HS256"

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Security scheme
security = HTTPBearer()

def get_redis_client() -> redis.Redis:
    """Get Redis client"""
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        # Test connection
        redis_client.ping()
        return redis_client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis connection failed"
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get current user from JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract user information
        user_id = payload.get("user_id")
        tenant_id = payload.get("tenant_id")
        role = payload.get("role", "Viewer")
        
        if not user_id or not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id or tenant_id"
            )
        
        return {
            "user_id": user_id,
            "tenant_id": tenant_id,
            "role": role,
            "jwt_payload": payload
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        logger.error(f"Token validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed"
        )

def require_role(required_roles: list):
    """Dependency to require specific roles"""
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {required_roles}, User role: {user_role}"
            )
        return current_user
    return role_checker

def require_admin_or_owner():
    """Dependency to require Admin or Owner role"""
    return require_role(["Admin", "Owner"])

def get_validation_service(
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis_client)
):
    """Get validation service instance"""
    from app.services import ValidationService
    return ValidationService(db, redis_client) 