from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from datetime import datetime
from typing import List
import uuid

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- DB session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Security helpers ---
def require_admin(request: Request):
    role = request.headers.get("X-Role")
    if role not in ("Owner", "Admin"):
        raise HTTPException(status_code=403, detail="Insufficient role")

def validate_tenant(request: Request, tenant_id: str):
    req_tenant = request.headers.get("X-Tenant-ID")
    if req_tenant != tenant_id:
        raise HTTPException(status_code=403, detail="Tenant mismatch")

# --- Endpoints ---
@app.get("/billing/tenant/{tenant_id}", response_model=schemas.TenantBillingProfile)
def get_billing_profile(tenant_id: str, db: Session = Depends(get_db), request: Request = None):
    require_admin(request)
    validate_tenant(request, tenant_id)
    profile = db.query(models.TenantBillingProfile).filter_by(tenant_id=tenant_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.post("/billing/usage_report")
def usage_report(report: dict, db: Session = Depends(get_db)):
    # Compare usage to plan limits, emit events if needed (stub)
    print(f"USAGE REPORT: {report}")
    return {"status": "received"}

@app.post("/billing/trigger_alerts")
def trigger_alerts(data: dict, db: Session = Depends(get_db)):
    # Evaluate limits, emit BillingEvent if needed (stub)
    print(f"TRIGGER ALERTS: {data}")
    return {"status": "alerts evaluated"}

@app.post("/billing/upgrade_plan")
def upgrade_plan(data: dict, db: Session = Depends(get_db), request: Request = None):
    require_admin(request)
    tenant_id = data.get("tenant_id")
    plan_id = data.get("plan_id")
    validate_tenant(request, tenant_id)
    profile = db.query(models.TenantBillingProfile).filter_by(tenant_id=tenant_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile.plan_id = plan_id
    db.commit()
    # Emit BillingEvent (stub)
    print(f"UPGRADE: {tenant_id} to {plan_id}")
    return {"status": "upgraded"}

@app.get("/billing/plans", response_model=List[schemas.SubscriptionPlan])
def get_plans(db: Session = Depends(get_db)):
    return db.query(models.SubscriptionPlan).all()
