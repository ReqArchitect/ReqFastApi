from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine
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
    tenant_id = request.headers.get("X-Tenant-ID")
    user_id = request.headers.get("X-User-ID")
    role = request.headers.get("X-Role")
    if not tenant_id or not user_id or not role:
        raise HTTPException(status_code=401, detail="Missing auth context")
    return {"tenant_id": tenant_id, "user_id": user_id, "role": role}

def require_admin(ctx):
    if ctx["role"] not in ("Owner", "Admin"):
        raise HTTPException(status_code=403, detail="Insufficient role")

# Event emitters (stub)
def emit_alert_event(tenant_id, alert_type):
    print(f"NOTIFY: {tenant_id=} {alert_type=}")
    # Integrate with notification_service and audit_log_service

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "analytics"}

@app.get("/analytics/tenant/{tenant_id}/monthly", response_model=List[schemas.TenantUsageSnapshot])
def get_usage_trends(tenant_id: str, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    if tenant_id != ctx["tenant_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(models.TenantUsageSnapshot).filter_by(tenant_id=tenant_id).order_by(models.TenantUsageSnapshot.date.asc()).all()

@app.get("/analytics/alerts/{tenant_id}", response_model=List[schemas.BillingAlert])
def get_billing_alerts(tenant_id: str, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    if tenant_id != ctx["tenant_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(models.BillingAlert).filter_by(tenant_id=tenant_id, resolved=False).all()

@app.post("/analytics/alerts/resolve/{alert_id}", response_model=schemas.BillingAlert)
def resolve_billing_alert(alert_id: int, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    alert = db.query(models.BillingAlert).filter_by(id=alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    if alert.tenant_id != ctx["tenant_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    require_admin(ctx)
    alert.resolved = True
    db.commit()
    db.refresh(alert)
    emit_alert_event(alert.tenant_id, f"resolve_{alert.alert_type}")
    return alert
