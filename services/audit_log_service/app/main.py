
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from typing import List
from datetime import datetime
import logging
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.get("/health")
def health():
    return {"status": "ok"}

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
