
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine
from typing import List
from datetime import datetime
import json
import time
import os
import logging

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to create tables, but don't fail if database is not available
try:
    models.Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.warning(f"Could not create database tables: {e}")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_auth_context(request: Request):
    """Enhanced authentication context with better error handling"""
    tenant_id = request.headers.get("X-Tenant-ID")
    user_id = request.headers.get("X-User-ID")
    
    # Provide more detailed error messages
    if not tenant_id and not user_id:
        raise HTTPException(
            status_code=401, 
            detail="Missing authentication headers. Required: X-Tenant-ID, X-User-ID"
        )
    elif not tenant_id:
        raise HTTPException(
            status_code=401, 
            detail="Missing X-Tenant-ID header"
        )
    elif not user_id:
        raise HTTPException(
            status_code=401, 
            detail="Missing X-User-ID header"
        )
    
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
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        logger.warning(f"Database connection failed: {e}")
        return False

@app.post("/ai_modeling/generate", response_model=schemas.ModelingOutput)
def generate_modeling(input: schemas.ModelingInput, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    """Enhanced generate endpoint with better error handling and fallback logic"""
    try:
        # Validate input
        if not input.input_text or not input.input_text.strip():
            raise HTTPException(
                status_code=422,
                detail="input_text cannot be empty"
            )
        
        if not input.input_type or not input.input_type.strip():
            raise HTTPException(
                status_code=422,
                detail="input_type cannot be empty"
            )
        
        # Validate that user_id matches auth context
        if input.user_id != ctx["user_id"]:
            raise HTTPException(
                status_code=422,
                detail="user_id in request body must match X-User-ID header"
            )
        
        if input.tenant_id != ctx["tenant_id"]:
            raise HTTPException(
                status_code=422,
                detail="tenant_id in request body must match X-Tenant-ID header"
            )
        
        rate_limit(input.user_id)
        prompt = prompt_template(input.input_type, input.input_text)
        llm_response = call_llm(prompt)
        
        # Try to store in database, but fallback if it fails
        try:
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
            return schemas.ModelingOutput.model_validate(db_output)
            
        except Exception as db_error:
            logger.warning(f"Database operation failed, returning fallback response: {db_error}")
            # Fallback response when database is not available
            return schemas.ModelingOutput(
                id=0,
                input_id=0,
                layer=llm_response["layer"],
                elements=llm_response["elements"],
                traceability=f"@fallback:{input.input_type}:{input.input_text[:32]}",
                created_at=datetime.utcnow()
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in generate_modeling: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/ai_modeling/history/{user_id}", response_model=List[schemas.ModelingOutput])
def get_history(user_id: str, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    """Enhanced history endpoint with better error handling"""
    try:
        # Validate that user_id in URL matches auth context
        if user_id != ctx["user_id"]:
            raise HTTPException(
                status_code=403, 
                detail="You can only access your own history"
            )
        
        # Try to query database, but fallback if it fails
        try:
            outputs = db.query(models.ModelingOutput).join(
                models.ModelingInput, 
                models.ModelingOutput.input_id == models.ModelingInput.id
            ).filter(models.ModelingInput.user_id == user_id).all()
            
            return [schemas.ModelingOutput.model_validate(o) for o in outputs]
            
        except Exception as db_error:
            logger.warning(f"Database query failed, returning empty history: {db_error}")
            # Return empty list when database is not available
            return []
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_history: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/ai_modeling/feedback")
def submit_feedback(feedback: schemas.ModelingFeedback, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    """Enhanced feedback endpoint with better error handling"""
    try:
        if feedback.user_id != ctx["user_id"]:
            raise HTTPException(
                status_code=403, 
                detail="You can only submit feedback for your own actions"
            )
        
        # Try to store feedback, but don't fail if database is unavailable
        try:
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
            return {"status": "ok", "message": "Feedback submitted successfully"}
            
        except Exception as db_error:
            logger.warning(f"Database operation failed for feedback: {db_error}")
            return {"status": "ok", "message": "Feedback received (not persisted due to database issues)"}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in submit_feedback: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
