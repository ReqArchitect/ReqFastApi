from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from datetime import datetime
from typing import List
import uuid
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

# --- Security helpers ---
def require_admin(request: Request):
    role = request.headers.get("X-Role")
    if role not in ("Owner", "Admin"):
        raise HTTPException(status_code=403, detail="Insufficient role")

# --- Template rendering ---
def render_template(content: str, context: dict) -> str:
    def replacer(match):
        key = match.group(1)
        return str(context.get(key, f"{{{{{key}}}}}"))
    return re.sub(r"{{\s*(\w+)\s*}}", replacer, content)

# --- Endpoints ---
@app.get("/templates", response_model=List[schemas.Template])
def list_templates(db: Session = Depends(get_db)):
    return db.query(models.Template).all()

@app.get("/templates/{input_type}", response_model=List[schemas.Template])
def get_templates_by_input_type(input_type: str, db: Session = Depends(get_db)):
    return db.query(models.Template).filter_by(input_type=input_type).all()

@app.post("/templates", response_model=schemas.Template)
def create_template(t: schemas.Template, db: Session = Depends(get_db), request: Request = None):
    require_admin(request)
    db_t = models.Template(
        template_id=t.template_id or str(uuid.uuid4()),
        name=t.name,
        input_type=t.input_type,
        target_layer=t.target_layer,
        content=t.content,
        version=t.version,
        created_by=t.created_by,
        created_at=datetime.utcnow()
    )
    db.add(db_t)
    db.commit()
    return db_t

@app.put("/templates/{template_id}", response_model=schemas.Template)
def update_template(template_id: str, update: schemas.TemplateUpdate, db: Session = Depends(get_db), request: Request = None):
    require_admin(request)
    db_t = db.query(models.Template).filter_by(template_id=template_id).first()
    if not db_t:
        raise HTTPException(status_code=404, detail="Template not found")
    if update.name:
        db_t.name = update.name
    if update.content:
        db_t.content = update.content
    if update.version:
        db_t.version = update.version
    db.commit()
    return db_t

@app.get("/templates/history/{template_id}", response_model=List[schemas.Template])
def get_template_history(template_id: str, db: Session = Depends(get_db)):
    # For demo, return all with same template_id (in prod, use versioning table)
    return db.query(models.Template).filter_by(template_id=template_id).all()

@app.post("/templates/log_usage")
def log_usage(log: schemas.TemplateUsageLog, db: Session = Depends(get_db)):
    # Rate-limit stub: in prod, use Redis or similar
    db_log = models.TemplateUsageLog(
        usage_id=log.usage_id or str(uuid.uuid4()),
        template_id=log.template_id,
        user_id=log.user_id,
        tenant_id=log.tenant_id,
        timestamp=datetime.utcnow(),
        context=log.context or {}
    )
    db.add(db_log)
    db.commit()
    return {"status": "logged"}
