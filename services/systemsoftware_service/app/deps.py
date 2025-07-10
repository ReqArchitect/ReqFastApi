from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import redis
import jwt
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from .database import get_db_session
from .config import settings

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Redis client
redis_client = None

def get_redis_client() -> redis.Redis:
    """Get Redis client instance."""
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
    return redis_client

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
) -> Dict[str, Any]:
    """Get current authenticated user from JWT token."""
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Extract user information from token
        user_id = payload.get("user_id")
        tenant_id = payload.get("tenant_id")
        role = payload.get("role")
        
        if not user_id or not tenant_id or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        
        return {
            "user_id": user_id,
            "tenant_id": tenant_id,
            "role": role,
            "permissions": get_user_permissions(role)
        }
        
    except jwt.PyJWTError as e:
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
    role_permissions = {
        "Owner": [
            "system_software:create", "system_software:read", "system_software:update", "system_software:delete",
            "software_link:create", "software_link:read", "software_link:update", "software_link:delete"
        ],
        "Admin": [
            "system_software:create", "system_software:read", "system_software:update", "system_software:delete",
            "software_link:create", "software_link:read", "software_link:update", "software_link:delete"
        ],
        "Editor": [
            "system_software:create", "system_software:read", "system_software:update",
            "software_link:create", "software_link:read", "software_link:update"
        ],
        "Viewer": [
            "system_software:read",
            "software_link:read"
        ]
    }
    
    return role_permissions.get(role, [])

async def check_permission(user: Dict[str, Any], required_permission: str) -> bool:
    """Check if user has required permission."""
    user_permissions = user.get("permissions", [])
    
    if required_permission not in user_permissions:
        logger.warning(f"Permission denied: {user['user_id']} attempted {required_permission}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required: {required_permission}, Role: {user['role']}"
        )
    
    return True

async def rate_limit(request: Request, redis_client: redis.Redis = Depends(get_redis_client)):
    """Rate limiting middleware."""
    client_ip = request.client.host
    user_id = getattr(request.state, 'user_id', 'anonymous')
    
    # Rate limit keys
    ip_key = f"rate_limit:ip:{client_ip}"
    user_key = f"rate_limit:user:{user_id}"
    
    try:
        # Check IP-based rate limit (1000 requests per hour)
        ip_count = redis_client.get(ip_key)
        if ip_count and int(ip_count) > 1000:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded for IP address"
            )
        
        # Check user-based rate limit (100 requests per minute)
        user_count = redis_client.get(user_key)
        if user_count and int(user_count) > 100:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded for user"
            )
        
        # Increment counters
        pipe = redis_client.pipeline()
        pipe.incr(ip_key)
        pipe.expire(ip_key, 3600)  # 1 hour
        pipe.incr(user_key)
        pipe.expire(user_key, 60)   # 1 minute
        pipe.execute()
        
    except redis.RedisError as e:
        logger.error(f"Redis error in rate limiting: {e}")
        # Continue without rate limiting if Redis is unavailable
        pass

async def get_tenant_context(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Get tenant context for multi-tenancy."""
    return {
        "tenant_id": user["tenant_id"],
        "user_id": user["user_id"],
        "role": user["role"]
    }

def validate_tenant_access(tenant_id: str, user: Dict[str, Any]) -> bool:
    """Validate that user has access to the specified tenant."""
    return user["tenant_id"] == tenant_id

async def require_admin_role(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require admin or owner role."""
    if user["role"] not in ["Admin", "Owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required"
        )
    return user

async def require_owner_role(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require owner role."""
    if user["role"] != "Owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Owner role required"
        )
    return user

def get_db_with_tenant(db: Session = Depends(get_db_session), 
                       tenant_context: Dict[str, Any] = Depends(get_tenant_context)) -> Session:
    """Get database session with tenant context."""
    return db

async def validate_system_software_access(
    system_software_id: str,
    user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
) -> bool:
    """Validate that user has access to the specified system software."""
    from .models import SystemSoftware
    
    system_software = db.query(SystemSoftware).filter(
        SystemSoftware.id == system_software_id,
        SystemSoftware.tenant_id == user["tenant_id"]
    ).first()
    
    if not system_software:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System software not found"
        )
    
    return True

async def validate_software_link_access(
    link_id: str,
    user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
) -> bool:
    """Validate that user has access to the specified software link."""
    from .models import SoftwareLink, SystemSoftware
    
    software_link = db.query(SoftwareLink).join(SystemSoftware).filter(
        SoftwareLink.id == link_id,
        SystemSoftware.tenant_id == user["tenant_id"]
    ).first()
    
    if not software_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Software link not found"
        )
    
    return True

def log_audit_event(
    event_type: str,
    resource_type: str,
    resource_id: str,
    user: Dict[str, Any],
    details: Optional[Dict[str, Any]] = None
):
    """Log audit event."""
    audit_data = {
        "event_type": event_type,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "user_id": user["user_id"],
        "tenant_id": user["tenant_id"],
        "role": user["role"],
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {}
    }
    
    logger.info(f"Audit event: {audit_data}")
    
    # Could also send to external audit service
    # audit_service.send_event(audit_data)

async def validate_input_data(data: Dict[str, Any], validation_rules: Dict[str, Any]) -> bool:
    """Validate input data against rules."""
    for field, rules in validation_rules.items():
        if field in data:
            value = data[field]
            
            # Type validation
            if "type" in rules and not isinstance(value, rules["type"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid type for {field}"
                )
            
            # Range validation
            if "min" in rules and value < rules["min"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{field} must be >= {rules['min']}"
                )
            
            if "max" in rules and value > rules["max"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{field} must be <= {rules['max']}"
                )
            
            # Length validation
            if "min_length" in rules and len(str(value)) < rules["min_length"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{field} must be at least {rules['min_length']} characters"
                )
            
            if "max_length" in rules and len(str(value)) > rules["max_length"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{field} must be at most {rules['max_length']} characters"
                )
    
    return True 