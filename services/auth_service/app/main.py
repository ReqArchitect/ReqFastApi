
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine
from datetime import datetime, timedelta
from passlib.hash import bcrypt
import jwt
import uuid
import os
import time
from typing import List

from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "REPLACE_ME")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# In-memory token blacklist for demo
revoked_tokens = set()

ROLES = ["Owner", "Admin", "Editor", "Viewer"]

# --- Auth Logic ---
def create_access_token(user_id, tenant_id, role):
    issued_at = datetime.utcnow()
    expires_at = issued_at + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user_id": user_id,
        "tenant_id": tenant_id,
        "role": role,
        "iat": int(issued_at.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, issued_at, expires_at

def verify_password(plain, hashed):
    return bcrypt.verify(plain, hashed)

def hash_password(plain):
    return bcrypt.hash(plain)

def emit_audit_event(user_id, tenant_id, event_type):
    print(f"AUDIT: {user_id=} {tenant_id=} {event_type=}")
    # Integrate with audit_log_service

# --- Endpoints ---
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "auth_service",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": get_uptime(),
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database_connected": check_database_connection()
    }

@app.get("/metrics")
def get_metrics():
    """Prometheus-style metrics endpoint"""
    return {
        "auth_uptime_seconds": get_uptime(),
        "auth_logins_total": getattr(app.state, 'login_count', 0),
        "auth_logouts_total": getattr(app.state, 'logout_count', 0),
        "auth_tokens_issued": getattr(app.state, 'tokens_issued', 0),
        "auth_tokens_revoked": getattr(app.state, 'tokens_revoked', 0)
    }

def get_uptime() -> float:
    """Get service uptime in seconds"""
    if not hasattr(app.state, 'start_time'):
        app.state.start_time = time.time()
    return time.time() - app.state.start_time

def check_database_connection() -> bool:
    """Check if database connection is working"""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception:
        return False

@app.post("/auth/login", response_model=schemas.AuthToken)
def login(data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token, issued_at, expires_at = create_access_token(user.user_id, user.tenant_id, user.role)
    db_token = models.AuthToken(
        token=token,
        issued_at=issued_at,
        expires_at=expires_at,
        user_id=user.user_id,
        tenant_id=user.tenant_id,
        role=user.role
    )
    db.add(db_token)
    db.commit()
    emit_audit_event(user.user_id, user.tenant_id, "login")
    return schemas.AuthToken.from_orm(db_token)

@app.post("/auth/logout")
def logout(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth_header.split(" ", 1)[1]
    revoked_tokens.add(token)
    # Optionally remove from DB
    emit_audit_event("unknown", "unknown", "logout")
    return {"status": "logged out"}

@app.get("/auth/me", response_model=schemas.User)
def me(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth_header.split(" ", 1)[1]
    if token in revoked_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter_by(user_id=payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.User.from_orm(user)

@app.post("/auth/refresh", response_model=schemas.AuthToken)
def refresh(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth_header.split(" ", 1)[1]
    if token in revoked_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter_by(user_id=payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_token, issued_at, expires_at = create_access_token(user.user_id, user.tenant_id, user.role)
    db_token = models.AuthToken(
        token=new_token,
        issued_at=issued_at,
        expires_at=expires_at,
        user_id=user.user_id,
        tenant_id=user.tenant_id,
        role=user.role
    )
    db.add(db_token)
    db.commit()
    emit_audit_event(user.user_id, user.tenant_id, "refresh")
    return schemas.AuthToken.from_orm(db_token)

@app.get("/auth/roles", response_model=List[str])
def get_roles():
    return ROLES
