from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional, List
import os
from functools import wraps

# Security configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

# Permission mapping
PERMISSIONS = {
    "Owner": [
        "assessment:create", "assessment:read", "assessment:update", "assessment:delete",
        "assessment_link:create", "assessment_link:read", "assessment_link:update", "assessment_link:delete"
    ],
    "Admin": [
        "assessment:create", "assessment:read", "assessment:update", "assessment:delete",
        "assessment_link:create", "assessment_link:read", "assessment_link:update", "assessment_link:delete"
    ],
    "Editor": [
        "assessment:create", "assessment:read", "assessment:update",
        "assessment_link:create", "assessment_link:read", "assessment_link:update"
    ],
    "Viewer": [
        "assessment:read",
        "assessment_link:read"
    ]
}

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token and return user information"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        tenant_id: str = payload.get("tenant_id")
        role: str = payload.get("role")
        
        if user_id is None or tenant_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {
            "user_id": user_id,
            "tenant_id": tenant_id,
            "role": role,
            "permissions": PERMISSIONS.get(role, [])
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(user: dict = Depends(verify_token)) -> dict:
    """Get current authenticated user"""
    return user

def require_permissions(required_permissions: List[str]):
    """Decorator to require specific permissions"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            user_permissions = current_user.get("permissions", [])
            
            # Check if user has all required permissions
            for permission in required_permissions:
                if permission not in user_permissions:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Insufficient permissions. Required: {', '.join(required_permissions)}, Role: {current_user.get('role', 'Unknown')}"
                    )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def require_role(required_role: str):
    """Decorator to require specific role"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            user_role = current_user.get("role")
            if user_role != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient role. Required: {required_role}, Current: {user_role}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def require_tenant_access():
    """Decorator to ensure tenant access"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            tenant_id = current_user.get("tenant_id")
            if not tenant_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Tenant access required"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Utility functions for permission checking
def has_permission(user: dict, permission: str) -> bool:
    """Check if user has specific permission"""
    user_permissions = user.get("permissions", [])
    return permission in user_permissions

def has_role(user: dict, role: str) -> bool:
    """Check if user has specific role"""
    user_role = user.get("role")
    return user_role == role

def is_owner_or_admin(user: dict) -> bool:
    """Check if user is owner or admin"""
    user_role = user.get("role")
    return user_role in ["Owner", "Admin"]

def can_manage_assessments(user: dict) -> bool:
    """Check if user can manage assessments"""
    return has_permission(user, "assessment:create") and has_permission(user, "assessment:update")

def can_delete_assessments(user: dict) -> bool:
    """Check if user can delete assessments"""
    return has_permission(user, "assessment:delete")

def can_manage_assessment_links(user: dict) -> bool:
    """Check if user can manage assessment links"""
    return has_permission(user, "assessment_link:create") and has_permission(user, "assessment_link:update")

def can_delete_assessment_links(user: dict) -> bool:
    """Check if user can delete assessment links"""
    return has_permission(user, "assessment_link:delete") 