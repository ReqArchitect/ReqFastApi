
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from typing import List
from datetime import datetime
import logging
import os
import time
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "audit_log_service",
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
        "audit_log_uptime_seconds": get_uptime(),
        "audit_log_requests_total": getattr(app.state, 'request_count', 0),
        "audit_log_events_total": getattr(app.state, 'events_logged', 0),
        "audit_log_errors_total": getattr(app.state, 'errors_total', 0)
    }

def get_uptime() -> float:
    """Get service uptime in seconds"""
    if not hasattr(app.state, 'start_time'):
        app.state.start_time = time.time()
    return time.time() - app.state.start_time

def check_database_connection() -> bool:
    """Check if database connection is working"""
    try:
        db = next(database.get_db())
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception:
        return False

@app.post("/audit/log", response_model=schemas.AuditLogCreate)
def create_audit_log(log: schemas.AuditLogCreate, db: Session = Depends(database.get_db)):
    db_log = models.AuditLog(
        timestamp=datetime.utcnow(),
        service=log.service,
        event_type=log.event_type,
        payload=log.payload
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    logging.info(f"Audit event: {log.service} - {log.event_type} - {log.payload}")
    return log

@app.get("/audit/logs", response_model=List[schemas.AuditLogCreate])
def list_audit_logs(db: Session = Depends(database.get_db)):
    logs = db.query(models.AuditLog).all()
    return [schemas.AuditLogCreate(
        service=log.service,
        event_type=log.event_type,
        payload=log.payload
    ) for log in logs]
