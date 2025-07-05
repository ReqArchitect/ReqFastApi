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
def get_auth_context(request: Request):
    user_id = request.headers.get("X-User-ID")
    tenant_id = request.headers.get("X-Tenant-ID")
    if not user_id or not tenant_id:
        raise HTTPException(status_code=401, detail="Missing auth context")
    return {"user_id": user_id, "tenant_id": tenant_id}

# --- Endpoints ---
@app.post("/feedback/submit", response_model=schemas.Feedback)
def submit_feedback(fb: schemas.Feedback, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    if not (1 <= fb.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be 1-5")
    if fb.user_id != ctx["user_id"] or fb.tenant_id != ctx["tenant_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    fb_id = fb.feedback_id or str(uuid.uuid4())
    db_fb = models.Feedback(
        feedback_id=fb_id,
        user_id=fb.user_id,
        tenant_id=fb.tenant_id,
        context_type=fb.context_type,
        context_id=fb.context_id,
        rating=fb.rating,
        comment=fb.comment,
        timestamp=datetime.utcnow()
    )
    db.add(db_fb)
    db.commit()
    # Emit event to event_bus_service (stub)
    print(f"AUDIT: feedback submitted {fb.context_type} {fb.context_id}")
    return db_fb

@app.get("/feedback/context/{context_id}", response_model=List[schemas.Feedback])
def get_feedback_for_context(context_id: str, db: Session = Depends(get_db)):
    return db.query(models.Feedback).filter_by(context_id=context_id).order_by(models.Feedback.timestamp.desc()).all()

@app.get("/feedback/user/{user_id}", response_model=List[schemas.Feedback])
def get_user_feedback(user_id: str, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    if user_id != ctx["user_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(models.Feedback).filter_by(user_id=user_id).order_by(models.Feedback.timestamp.desc()).all()

@app.get("/feedback/summary/{context_id}", response_model=schemas.FeedbackSummary)
def get_feedback_summary(context_id: str, db: Session = Depends(get_db)):
    feedbacks = db.query(models.Feedback).filter_by(context_id=context_id).all()
    if not feedbacks:
        return schemas.FeedbackSummary(context_type="", context_id=context_id, average_rating=0.0, total_feedback=0)
    avg = sum(f.rating for f in feedbacks) / len(feedbacks)
    return schemas.FeedbackSummary(
        context_type=feedbacks[0].context_type,
        context_id=context_id,
        average_rating=avg,
        total_feedback=len(feedbacks)
    )
