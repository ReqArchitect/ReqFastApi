from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine
from typing import List

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
    # In production, extract tenant_id and user_id from JWT or session
    tenant_id = request.headers.get("X-Tenant-ID")
    user_id = request.headers.get("X-User-ID")
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Missing tenant context")
    return {"tenant_id": tenant_id, "user_id": user_id}

# Event emitter stub
def emit_audit_event(tenant_id, user_id, step, value):
    # Integrate with audit_log_service here
    print(f"AUDIT: {tenant_id=} {user_id=} {step=} {value=}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "onboarding_state"}

@app.get("/onboarding/state/{user_id}", response_model=schemas.OnboardingStatus)
def get_onboarding_state(user_id: str, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    record = db.query(models.OnboardingStatus).filter_by(user_id=user_id, tenant_id=ctx["tenant_id"]).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return schemas.OnboardingStatus(
        tenant_id=record.tenant_id,
        user_id=record.user_id,
        configure_capabilities=record.configure_capabilities,
        create_initiative=record.create_initiative,
        invite_teammates=record.invite_teammates,
        explore_traceability=record.explore_traceability,
        completed=record.completed
    )

@app.post("/onboarding/state/{user_id}", response_model=schemas.OnboardingStatus)
def update_onboarding_state(user_id: str, update: schemas.OnboardingStatusUpdate, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    record = db.query(models.OnboardingStatus).filter_by(user_id=user_id, tenant_id=ctx["tenant_id"]).first()
    if not record:
        # Create new record if not exists
        record = models.OnboardingStatus(tenant_id=ctx["tenant_id"], user_id=user_id)
        db.add(record)
    changed = False
    for step in ["configure_capabilities", "create_initiative", "invite_teammates", "explore_traceability"]:
        val = getattr(update, step)
        if val is not None and getattr(record, step) != val:
            setattr(record, step, val)
            emit_audit_event(ctx["tenant_id"], user_id, step, val)
            changed = True
    db.commit()
    db.refresh(record)
    # Optionally trigger frontend confetti/toast if completed
    if record.completed and changed:
        emit_audit_event(ctx["tenant_id"], user_id, "completed", True)
    return schemas.OnboardingStatus(
        tenant_id=record.tenant_id,
        user_id=record.user_id,
        configure_capabilities=record.configure_capabilities,
        create_initiative=record.create_initiative,
        invite_teammates=record.invite_teammates,
        explore_traceability=record.explore_traceability,
        completed=record.completed
    )

@app.get("/onboarding/state/tenant/{tenant_id}", response_model=List[schemas.OnboardingStatus])
def list_onboarding_states(tenant_id: str, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    # Only allow access if tenant matches auth context
    if tenant_id != ctx["tenant_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    records = db.query(models.OnboardingStatus).filter_by(tenant_id=tenant_id).all()
    return [
        schemas.OnboardingStatus(
            tenant_id=r.tenant_id,
            user_id=r.user_id,
            configure_capabilities=r.configure_capabilities,
            create_initiative=r.create_initiative,
            invite_teammates=r.invite_teammates,
            explore_traceability=r.explore_traceability,
            completed=r.completed
        ) for r in records
    ]
