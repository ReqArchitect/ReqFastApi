from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional, Dict, Any
import uuid
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# JWT configuration
SECRET_KEY = "your-secret-key-here"  # In production, use environment variable
ALGORITHM = "HS256"

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Extract and validate JWT token to get current user"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract user information
        user_id = payload.get("user_id")
        tenant_id = payload.get("tenant_id")
        role = payload.get("role")
        
        if not user_id or not tenant_id or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        return {
            "id": uuid.UUID(user_id),
            "tenant_id": uuid.UUID(tenant_id),
            "role": role,
            "permissions": _get_user_permissions(role)
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

def get_current_tenant(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Extract tenant information from current user"""
    return {
        "id": current_user["tenant_id"],
        "name": "Default Tenant"  # In production, fetch from database
    }

def require_permission(current_user: Dict[str, Any], required_permission: str):
    """Check if user has required permission"""
    user_permissions = current_user.get("permissions", [])
    
    if required_permission not in user_permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required: {required_permission}, Role: {current_user.get('role', 'Unknown')}"
        )

def _get_user_permissions(role: str) -> list:
    """Get user permissions based on role"""
    role_permissions = {
        "Owner": [
            "work_package:create",
            "work_package:read",
            "work_package:update",
            "work_package:delete",
            "work_package:create_link",
            "work_package:read_link",
            "work_package:update_link",
            "work_package:delete_link"
        ],
        "Admin": [
            "work_package:create",
            "work_package:read",
            "work_package:update",
            "work_package:delete",
            "work_package:create_link",
            "work_package:read_link",
            "work_package:update_link",
            "work_package:delete_link"
        ],
        "Editor": [
            "work_package:create",
            "work_package:read",
            "work_package:update",
            "work_package:create_link",
            "work_package:read_link",
            "work_package:update_link"
        ],
        "Viewer": [
            "work_package:read",
            "work_package:read_link"
        ]
    }
    
    return role_permissions.get(role, []) 