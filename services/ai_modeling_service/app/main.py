
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine
from typing import List
from datetime import datetime
import json
import time
import os

from dotenv import load_dotenv
load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_auth_context(request: Request):
    tenant_id = request.headers.get("X-Tenant-ID")
    user_id = request.headers.get("X-User-ID")
    if not tenant_id or not user_id:
        raise HTTPException(status_code=401, detail="Missing auth context")
    return {"tenant_id": tenant_id, "user_id": user_id}

def emit_audit_event(tenant_id, user_id, event_type, details=None):
    print(f"AUDIT: {tenant_id=} {user_id=} {event_type=} {details=}")
    # Integrate with audit_log_service

def rate_limit(user_id):
    # Stub: In production, implement real rate limiting
    return

def prompt_template(input_type, input_text):
    # Stub: Use docx prompt templates in production
    return f"Generate ArchiMate elements for {input_type}: {input_text}"

def call_llm(prompt):
    # Stub: Replace with real LLM call
    # Simulate output
    if "goal" in prompt.lower():
        return {"layer": "Strategy", "elements": [{"type": "Goal", "name": "OptimizeSupplyChain"}]}
    if "initiative" in prompt.lower():
        return {"layer": "Business", "elements": [{"type": "Initiative", "name": "DigitalOps2025"}]}
    return {"layer": "Business", "elements": [{"type": "Capability", "name": "DefaultCapability"}]}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai_modeling_service",
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
        "ai_modeling_uptime_seconds": get_uptime(),
        "ai_modeling_requests_total": getattr(app.state, 'request_count', 0),
        "ai_modeling_generations_total": getattr(app.state, 'generation_count', 0),
        "ai_modeling_feedback_total": getattr(app.state, 'feedback_count', 0)
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

@app.post("/ai_modeling/generate", response_model=schemas.ModelingOutput)
def generate_modeling(input: schemas.ModelingInput, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    rate_limit(input.user_id)
    prompt = prompt_template(input.input_type, input.input_text)
    llm_response = call_llm(prompt)
    # Store input
    db_input = models.ModelingInput(
        tenant_id=input.tenant_id,
        user_id=input.user_id,
        input_type=input.input_type,
        input_text=input.input_text,
        created_at=datetime.utcnow()
    )
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    # Store output
    trace = f"@source:{input.input_type}:{input.input_text[:32]}"
    db_output = models.ModelingOutput(
        input_id=db_input.id,
        layer=llm_response["layer"],
        elements=llm_response["elements"],
        traceability=trace,
        created_at=datetime.utcnow()
    )
    db.add(db_output)
    db.commit()
    db.refresh(db_output)
    emit_audit_event(input.tenant_id, input.user_id, "generate_modeling", trace)
    return schemas.ModelingOutput.from_orm(db_output)

@app.get("/ai_modeling/history/{user_id}", response_model=List[schemas.ModelingOutput])
def get_history(user_id: str, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    if user_id != ctx["user_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    outputs = db.query(models.ModelingOutput).join(models.ModelingInput, models.ModelingOutput.input_id == models.ModelingInput.id).filter(models.ModelingInput.user_id == user_id).all()
    return [schemas.ModelingOutput.from_orm(o) for o in outputs]

@app.post("/ai_modeling/feedback")
def submit_feedback(feedback: schemas.ModelingFeedback, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    if feedback.user_id != ctx["user_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    db_feedback = models.ModelingFeedback(
        output_id=feedback.output_id,
        user_id=feedback.user_id,
        rating=feedback.rating,
        comments=feedback.comments,
        created_at=datetime.utcnow()
    )
    db.add(db_feedback)
    db.commit()
    emit_audit_event(ctx["tenant_id"], ctx["user_id"], "submit_feedback", str(feedback.rating))
    return {"status": "ok"}
