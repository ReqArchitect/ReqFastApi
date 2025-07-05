from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from typing import List
import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dummy auth context for demo (replace with real auth in prod)
def get_auth_context(request: Request):
    # In production, extract tenant_id, user_id, and role from JWT or session
    tenant_id = request.headers.get("X-Tenant-ID")
    user_id = request.headers.get("X-User-ID")
    role = request.headers.get("X-Role")
    if not tenant_id or not user_id or not role:
        raise HTTPException(status_code=401, detail="Missing auth context")
    return {"tenant_id": tenant_id, "user_id": user_id, "role": role}

# Security check
def require_admin(ctx):
    if ctx["role"] not in ("Owner", "Admin"):
        raise HTTPException(status_code=403, detail="Insufficient role")

def emit_audit_event(db, tenant_id, user_id, event_type, details=None):
    event = models.AuditEvent(
        tenant_id=tenant_id,
        user_id=user_id,
        event_type=event_type,
        event_time=datetime.datetime.utcnow(),
        details=details or ""
    )
    db.add(event)
    db.commit()

@app.get("/usage/tenant/{tenant_id}", response_model=schemas.UsageMetrics)
def get_usage_metrics(tenant_id: str, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    if tenant_id != ctx["tenant_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    metrics = db.query(models.UsageMetrics).filter_by(tenant_id=tenant_id).first()
    if not metrics:
        raise HTTPException(status_code=404, detail="No usage metrics found")
    emit_audit_event(db, tenant_id, ctx["user_id"], "fetch_usage_metrics")
    return metrics

@app.get("/usage/system_health", response_model=schemas.SystemStats)
def get_system_health(db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    stats = db.query(models.SystemStats).order_by(models.SystemStats.collected_at.desc()).first()
    if not stats:
        raise HTTPException(status_code=404, detail="No system stats found")
    emit_audit_event(db, ctx["tenant_id"], ctx["user_id"], "fetch_system_health")
    return stats

@app.get("/usage/activity/{tenant_id}", response_model=List[schemas.AuditEvent])
def get_audit_events(tenant_id: str, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    if tenant_id != ctx["tenant_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    events = db.query(models.AuditEvent).filter_by(tenant_id=tenant_id).order_by(models.AuditEvent.event_time.desc()).limit(50).all()
    emit_audit_event(db, tenant_id, ctx["user_id"], "fetch_audit_events")
    return events
