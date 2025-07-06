from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine
from datetime import datetime
from typing import List
import uuid
import requests
import re

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- DB session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Template rendering ---
def render_template(content: str, context: dict) -> str:
    def replacer(match):
        key = match.group(1)
        return str(context.get(key, f"{{{{{key}}}}}"))
    return re.sub(r"{{\s*(\w+)\s*}}", replacer, content)

# --- Endpoints ---
@app.post("/notifications/send", response_model=schemas.Notification)
def send_notification(n: schemas.Notification, db: Session = Depends(get_db), request: Request = None):
    # Validate sender (stub)
    n_id = n.notification_id or str(uuid.uuid4())
    db_n = models.Notification(
        notification_id=n_id,
        user_id=n.user_id,
        tenant_id=n.tenant_id,
        channel=n.channel,
        message=n.message,
        event_type=n.event_type,
        delivered=False,
        timestamp=datetime.utcnow()
    )
    db.add(db_n)
    db.commit()
    # Deliver (stub: mark as delivered)
    db_n.delivered = True
    db.commit()
    # Emit audit log (stub)
    print(f"AUDIT: deliver {n.channel} to {n.user_id}")
    return db_n

@app.get("/notifications/user/{user_id}", response_model=List[schemas.Notification])
def get_user_notifications(user_id: str, db: Session = Depends(get_db)):
    return db.query(models.Notification).filter_by(user_id=user_id).order_by(models.Notification.timestamp.desc()).all()

@app.post("/notifications/template", response_model=schemas.NotificationTemplate)
def create_or_update_template(t: schemas.NotificationTemplate, db: Session = Depends(get_db)):
    db_t = db.query(models.NotificationTemplate).filter_by(template_id=t.template_id).first()
    if db_t:
        db_t.content = t.content
        db_t.channel = t.channel
        db_t.event_type = t.event_type
    else:
        db_t = models.NotificationTemplate(
            template_id=t.template_id,
            event_type=t.event_type,
            channel=t.channel,
            content=t.content
        )
        db.add(db_t)
    db.commit()
    return db_t

@app.get("/notifications/template/{event_type}", response_model=List[schemas.NotificationTemplate])
def get_template_by_event(event_type: str, db: Session = Depends(get_db)):
    return db.query(models.NotificationTemplate).filter_by(event_type=event_type).all()
