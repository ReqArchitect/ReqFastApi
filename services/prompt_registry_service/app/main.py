from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from typing import List
from datetime import datetime
import uuid

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
    role = request.headers.get("X-Role")
    if not tenant_id or not user_id or not role:
        raise HTTPException(status_code=401, detail="Missing auth context")
    return {"tenant_id": tenant_id, "user_id": user_id, "role": role}

def require_admin(ctx):
    if ctx["role"] not in ("Owner", "Admin"):
        raise HTTPException(status_code=403, detail="Insufficient role")

@app.get("/prompt_registry/templates", response_model=List[schemas.PromptTemplate])
def list_templates(db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    return db.query(models.PromptTemplate).all()

@app.get("/prompt_registry/template/{input_type}", response_model=schemas.PromptTemplate)
def get_template_by_input_type(input_type: str, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    template = db.query(models.PromptTemplate).filter_by(input_type=input_type).order_by(models.PromptTemplate.version.desc()).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@app.post("/prompt_registry/template", response_model=schemas.PromptTemplate)
def add_template(template: schemas.PromptTemplate, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    db_template = models.PromptTemplate(
        id=template.id or str(uuid.uuid4()),
        name=template.name,
        input_type=template.input_type,
        layer=template.layer,
        template_text=template.template_text,
        version=template.version,
        created_at=datetime.utcnow()
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@app.put("/prompt_registry/template/{id}", response_model=schemas.PromptTemplate)
def update_template(id: str, update: schemas.PromptTemplateUpdate, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    template = db.query(models.PromptTemplate).filter_by(id=id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    if update.name:
        template.name = update.name
    if update.template_text:
        template.template_text = update.template_text
    if update.version:
        template.version = update.version
    db.commit()
    db.refresh(template)
    return template

@app.get("/prompt_registry/history/{id}", response_model=List[schemas.PromptTemplate])
def get_template_history(id: str, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    # For demo, return all versions with same id (in production, use versioning table)
    return db.query(models.PromptTemplate).filter_by(id=id).all()
