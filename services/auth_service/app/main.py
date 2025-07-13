
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models
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

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
import redis
import secrets
from app.models import Invitation
from app.schemas import (
    LoginRequest, LoginResponse, SignupRequest, SignupResponse, UserProfile,
    InviteRequest, InviteResponse, AcceptInviteRequest, AcceptInviteResponse,
    RoleInfo, ErrorResponse, LogoutResponse
)

# --- CORS for frontend integration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Redis for audit logging ---
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def log_redis_event(event_type, payload):
    try:
        redis_client.publish(event_type, payload)
    except Exception:
        pass

# --- Rate limiting (simple in-memory, per-IP) ---
from fastapi import Request
from collections import defaultdict
RATE_LIMITS = defaultdict(list)  # {ip: [timestamps]}
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX = 10  # max requests per window

def check_rate_limit(ip, action):
    now = time.time()
    window = RATE_LIMITS[(ip, action)]
    window[:] = [t for t in window if now - t < RATE_LIMIT_WINDOW]
    if len(window) >= RATE_LIMIT_MAX:
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
    window.append(now)

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

# --- Session-Oriented Endpoints ---
@app.post("/auth/login", response_model=LoginResponse, responses={401: {"model": ErrorResponse}})
def login_ui(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request.client.host, "login")
    user = db.query(models.User).filter_by(email=data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        return ErrorResponse(status_code=401, message="Invalid credentials", hint="Check email and password", field="password")
    token, _, expires_at = create_access_token(user.user_id, user.tenant_id, user.role)
    user_profile = {
        "id": user.user_id,
        "name": user.name or user.email,
        "email": user.email,
        "tenant_id": user.tenant_id,
        "role": user.role
    }
    log_redis_event("auth.login", f"{{'user_id': '{user.user_id}', 'tenant_id': '{user.tenant_id}'}}")
    return LoginResponse(token=token, expires_at=expires_at, user=user_profile)

@app.post("/auth/signup", response_model=SignupResponse, responses={400: {"model": ErrorResponse}})
def signup_ui(data: SignupRequest, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request.client.host, "signup")
    # Only allow default role Viewer
    role = "Viewer"
    tenant_id = str(uuid.uuid4()) if data.tenant_name else "default"
    user_id = str(uuid.uuid4())
    user = models.User(
        user_id=user_id,
        email=data.email,
        name=data.name,
        hashed_password=hash_password(data.password),
        role=role,
        tenant_id=tenant_id
    )
    try:
        db.add(user)
        db.commit()
    except IntegrityError:
        db.rollback()
        return ErrorResponse(status_code=400, message="Email already registered", hint="Use a different email", field="email")
    token, _, expires_at = create_access_token(user.user_id, user.tenant_id, user.role)
    user_profile = {
        "id": user.user_id,
        "name": user.name,
        "email": user.email,
        "tenant_id": user.tenant_id,
        "role": user.role
    }
    log_redis_event("auth.signup", f"{{'user_id': '{user.user_id}', 'tenant_id': '{user.tenant_id}'}}")
    return SignupResponse(token=token, expires_at=expires_at, user=user_profile, tenant_created=bool(data.tenant_name))

@app.get("/auth/user", response_model=UserProfile, responses={401: {"model": ErrorResponse}})
def get_user_profile(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth_header.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter_by(user_id=payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Permissions can be derived from role
    permissions = [f"can_{user.role.lower()}"]
    return UserProfile(
        id=user.user_id,
        name=user.name or user.email,
        email=user.email,
        tenant_id=user.tenant_id,
        role=user.role,
        permissions=permissions,
        created_at=user.created_at
    )

@app.post("/auth/logout", response_model=LogoutResponse)
def logout_ui(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth_header.split(" ", 1)[1]
    revoked_tokens.add(token)
    log_redis_event("auth.logout", f"{{'token': '{token}'}}")
    return LogoutResponse(message="Logged out successfully", timestamp=datetime.utcnow())

@app.post("/auth/invite", response_model=InviteResponse, responses={400: {"model": ErrorResponse}})
def invite_user(data: InviteRequest, request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth_header.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    inviter = db.query(models.User).filter_by(user_id=payload["user_id"]).first()
    if not inviter:
        raise HTTPException(status_code=404, detail="Inviter not found")
    if inviter.role not in ["Owner", "Admin"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    invite_token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=7)
    invitation = Invitation(
        invite_token=invite_token,
        email=data.email,
        role=data.role,
        tenant_id=inviter.tenant_id,
        invited_by=inviter.user_id,
        message=data.message,
        expires_at=expires_at
    )
    try:
        db.add(invitation)
        db.commit()
    except IntegrityError:
        db.rollback()
        return ErrorResponse(status_code=400, message="Invite already exists", field="email")
    log_redis_event("auth.invite", f"{{'invite_id': '{invitation.invite_id}', 'tenant_id': '{invitation.tenant_id}'}}")
    return InviteResponse(
        invite_id=invitation.invite_id,
        invite_token=invitation.invite_token,
        expires_at=invitation.expires_at,
        email=invitation.email
    )

@app.post("/auth/accept-invite", response_model=AcceptInviteResponse, responses={400: {"model": ErrorResponse}})
def accept_invite(data: AcceptInviteRequest, db: Session = Depends(get_db)):
    invitation = db.query(Invitation).filter_by(invite_token=data.invite_token, is_accepted=False).first()
    if not invitation or invitation.expires_at < datetime.utcnow():
        return ErrorResponse(status_code=400, message="Invalid or expired invitation", field="invite_token")
    user_id = str(uuid.uuid4())
    user = models.User(
        user_id=user_id,
        email=invitation.email,
        name=data.name,
        hashed_password=hash_password(data.password),
        role=invitation.role,
        tenant_id=invitation.tenant_id
    )
    try:
        db.add(user)
        invitation.is_accepted = True
        db.commit()
    except IntegrityError:
        db.rollback()
        return ErrorResponse(status_code=400, message="User already exists", field="email")
    token, _, expires_at = create_access_token(user.user_id, user.tenant_id, user.role)
    user_profile = {
        "id": user.user_id,
        "name": user.name,
        "email": user.email,
        "tenant_id": user.tenant_id,
        "role": user.role
    }
    log_redis_event("auth.accept_invite", f"{{'user_id': '{user.user_id}', 'tenant_id': '{user.tenant_id}'}}")
    return AcceptInviteResponse(token=token, expires_at=expires_at, user=user_profile)

@app.get("/auth/roles", response_model=List[RoleInfo])
def get_roles_ui():
    return [
        RoleInfo(
            name="Owner",
            description="Full access to all tenant resources and settings.",
            capabilities=["Manage users", "Configure tenant", "Access all data"],
            permissions=["owner:all"]
        ),
        RoleInfo(
            name="Admin",
            description="Manage users and resources, but not tenant settings.",
            capabilities=["Manage users", "Access most data"],
            permissions=["admin:manage", "admin:view"]
        ),
        RoleInfo(
            name="Editor",
            description="Edit and create resources, but cannot manage users.",
            capabilities=["Edit data", "Create resources"],
            permissions=["editor:edit", "editor:create"]
        ),
        RoleInfo(
            name="Viewer",
            description="Read-only access to resources.",
            capabilities=["View data"],
            permissions=["viewer:view"]
        )
    ]
