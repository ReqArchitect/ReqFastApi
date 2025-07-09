from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from .models import Requirement, RequirementLink
from .services import get_requirement, get_requirement_link
from .database import SessionLocal
from uuid import UUID
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "REPLACE_ME")
ALGORITHM = "HS256"

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_tenant(request: Request) -> UUID:
    """Extract tenant_id from JWT token"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = auth_header.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        tenant_id = payload.get("tenant_id")
        if not tenant_id:
            raise HTTPException(status_code=401, detail="Missing tenant_id in token")
        return UUID(tenant_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(request: Request) -> UUID:
    """Extract user_id from JWT token"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = auth_header.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Missing user_id in token")
        return UUID(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_role(request: Request) -> str:
    """Extract role from JWT token"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = auth_header.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
        if not role:
            raise HTTPException(status_code=401, detail="Missing role in token")
        return role
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def rbac_check(permission: str):
    """RBAC permission checker"""
    def checker(request: Request, role: str = Depends(get_current_role)):
        # Define permission matrix
        permissions = {
            "requirement:create": ["Owner", "Admin", "Editor"],
            "requirement:read": ["Owner", "Admin", "Editor", "Viewer"],
            "requirement:update": ["Owner", "Admin", "Editor"],
            "requirement:delete": ["Owner", "Admin"],
            "requirement_link:create": ["Owner", "Admin", "Editor"],
            "requirement_link:read": ["Owner", "Admin", "Editor", "Viewer"],
            "requirement_link:update": ["Owner", "Admin", "Editor"],
            "requirement_link:delete": ["Owner", "Admin"],
            "traceability:read": ["Owner", "Admin", "Editor", "Viewer"],
            "impact:read": ["Owner", "Admin", "Editor", "Viewer"]
        }
        
        if permission not in permissions:
            raise HTTPException(status_code=500, detail=f"Unknown permission: {permission}")
        
        if role not in permissions[permission]:
            raise HTTPException(
                status_code=403, 
                detail=f"Insufficient permissions. Required: {permission}, Role: {role}"
            )
        
        return role
    
    return checker 