from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import jwt
import redis
import os
from dotenv import load_dotenv

from .database import SessionLocal
from .models import BusinessProcess, ProcessStep, ProcessLink

load_dotenv()

# Redis connection
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    decode_responses=True
)

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        tenant_id: str = payload.get("tenant_id")
        role: str = payload.get("role", "viewer")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {
            "user_id": user_id,
            "tenant_id": tenant_id,
            "role": role
        }
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_business_process(db: Session, business_process_id: str, tenant_id: str):
    business_process = db.query(BusinessProcess).filter(
        BusinessProcess.id == business_process_id,
        BusinessProcess.tenant_id == tenant_id
    ).first()
    
    if not business_process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business process not found"
        )
    
    return business_process

def get_process_step(db: Session, step_id: str, tenant_id: str):
    step = db.query(ProcessStep).join(BusinessProcess).filter(
        ProcessStep.id == step_id,
        BusinessProcess.tenant_id == tenant_id
    ).first()
    
    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process step not found"
        )
    
    return step

def get_process_link(db: Session, link_id: str, tenant_id: str):
    link = db.query(ProcessLink).join(BusinessProcess).filter(
        ProcessLink.id == link_id,
        BusinessProcess.tenant_id == tenant_id
    ).first()
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process link not found"
        )
    
    return link

def check_permissions(user: dict, required_role: str = "viewer"):
    role_hierarchy = {
        "owner": 4,
        "admin": 3,
        "editor": 2,
        "viewer": 1
    }
    
    user_role_level = role_hierarchy.get(user.get("role", "viewer"), 0)
    required_role_level = role_hierarchy.get(required_role, 0)
    
    if user_role_level < required_role_level:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

def require_owner(user: dict = Depends(get_current_user)):
    check_permissions(user, "owner")
    return user

def require_admin(user: dict = Depends(get_current_user)):
    check_permissions(user, "admin")
    return user

def require_editor(user: dict = Depends(get_current_user)):
    check_permissions(user, "editor")
    return user

def require_viewer(user: dict = Depends(get_current_user)):
    check_permissions(user, "viewer")
    return user 