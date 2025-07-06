from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine
from datetime import datetime
from typing import List
import uuid
import redis
import json
import requests
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Redis pub/sub setup (for demo)
REDIS_URL = "redis://localhost:6379/0"
r = redis.Redis.from_url(REDIS_URL)

# --- DB session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Security helpers ---
def validate_source(request: Request):
    # In production, validate service identity (e.g., mTLS, API key)
    service = request.headers.get("X-Service-Name")
    if not service:
        raise HTTPException(status_code=401, detail="Missing service identity")
    return service

def emit_audit_event(event_type, details=None):
    print(f"AUDIT: {event_type=} {details=}")
    # Integrate with audit_log_service

# --- Endpoints ---
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "event_bus"}

@app.post("/event_bus/publish")
def publish_event(event: schemas.Event, request: Request, db: Session = Depends(get_db)):
    source_service = validate_source(request)
    event_id = event.event_id or str(uuid.uuid4())
    db_event = models.Event(
        event_id=event_id,
        event_type=event.event_type,
        payload=event.payload,
        source_service=source_service,
        timestamp=datetime.utcnow()
    )
    db.add(db_event)
    db.commit()
    # Publish to Redis
    r.publish(event.event_type, json.dumps(event.payload))
    emit_audit_event("publish", event.event_type)
    # Deliver to subscribers
    subs = db.query(models.Subscription).filter_by(event_type=event.event_type).all()
    for sub in subs:
        try:
            resp = requests.post(sub.callback_url, json=event.payload, timeout=5)
            if resp.status_code != 200:
                raise Exception(f"Non-200: {resp.status_code}")
        except Exception as e:
            # Retry with backoff (demo: 1 retry)
            time.sleep(2)
            try:
                requests.post(sub.callback_url, json=event.payload, timeout=5)
            except Exception as e2:
                emit_audit_event("delivery_failed", str(e2))
    return {"status": "published", "event_id": event_id}

@app.get("/event_bus/subscriptions", response_model=List[schemas.Subscription])
def list_subscriptions(db: Session = Depends(get_db)):
    return db.query(models.Subscription).all()

@app.post("/event_bus/subscribe", response_model=schemas.Subscription)
def subscribe(sub: schemas.Subscription, request: Request, db: Session = Depends(get_db)):
    validate_source(request)
    db_sub = models.Subscription(
        id=sub.id or str(uuid.uuid4()),
        event_type=sub.event_type,
        subscriber_service=sub.subscriber_service,
        callback_url=sub.callback_url,
        created_at=datetime.utcnow()
    )
    db.add(db_sub)
    db.commit()
    emit_audit_event("subscribe", sub.event_type)
    return db_sub

@app.post("/event_bus/unsubscribe")
def unsubscribe(sub: schemas.Subscription, request: Request, db: Session = Depends(get_db)):
    validate_source(request)
    db_sub = db.query(models.Subscription).filter_by(id=sub.id).first()
    if db_sub:
        db.delete(db_sub)
        db.commit()
        emit_audit_event("unsubscribe", sub.event_type)
    return {"status": "unsubscribed"}
