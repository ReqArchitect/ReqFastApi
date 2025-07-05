from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import httpx
import os
import logging
from prometheus_client import make_asgi_app
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal
from typing import List
from datetime import datetime
import json

app = FastAPI()
FastAPIInstrumentor().instrument_app(app)
HTTPXClientInstrumentor().instrument()

# Observability endpoints
app.mount("/metrics", make_asgi_app())

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/model/tree")
async def get_model_tree(request: Request):
    # Fan-out to all element services (stub)
    # Merge results, preserve correlation_id
    return {"tree": []}

@app.get("/model/{element}/{id}/full-details")
async def get_full_details(element: str, id: str, request: Request):
    # Fan-out to element service, aggregate traceability, KPI, etc. (stub)
    return {"element": element, "id": id, "details": {}}

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

def emit_audit_event(tenant_id, user_id, event_type, details=None):
    logging.info(f"AUDIT: {tenant_id=} {user_id=} {event_type=} {details=}")
    # Integrate with audit_log_service

def nlp_map_task_to_elements(title, description):
    elements = []
    if "initiative" in title.lower() or "initiative" in description.lower():
        elements.append("Initiative:AutoMapped")
    if "capability" in title.lower() or "capability" in description.lower():
        elements.append("Capability:AutoMapped")
    return elements or ["Capability:Default"]

def trigger_generation_flow(task, gen_type, db):
    # Stub: In production, call internal services
    trace = f"@source:Jira#{task.task_id} @trace:{','.join(task.linked_elements)}"
    req = models.GenerationRequest(
        task_id=task.task_id,
        generation_type=gen_type,
        model_links=task.linked_elements,
        status="completed",
        created_at=datetime.utcnow()
    )
    db.add(req)
    db.commit()
    emit_audit_event(task.task_id, "system", f"trigger_{gen_type}", trace)
    return req

@app.post("/orchestrator/ingest_task", response_model=schemas.TaskPayload)
def ingest_task(payload: schemas.TaskPayload, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    elements = nlp_map_task_to_elements(payload.title, payload.description)
    task = models.TaskPayload(
        task_id=payload.task_id,
        title=payload.title,
        description=payload.description,
        jira_type=payload.jira_type,
        linked_elements=elements,
        created_at=datetime.utcnow()
    )
    db.add(task)
    db.commit()
    emit_audit_event(ctx["tenant_id"], ctx["user_id"], "ingest_task", json.dumps(elements))
    return schemas.TaskPayload.from_orm(task)

@app.post("/orchestrator/trigger_generation", response_model=schemas.GenerationRequest)
def trigger_generation(req: schemas.GenerationRequest, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    task = db.query(models.TaskPayload).filter_by(task_id=req.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    gen_req = trigger_generation_flow(task, req.generation_type, db)
    return schemas.GenerationRequest.from_orm(gen_req)

@app.get("/orchestrator/status/{task_id}", response_model=List[schemas.GenerationRequest])
def get_generation_status(task_id: str, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    return db.query(models.GenerationRequest).filter_by(task_id=task_id).all()

@app.get("/orchestrator/logs/{task_id}")
def get_audit_logs(task_id: str, db: Session = Depends(get_db), ctx: dict = Depends(get_auth_context)):
    require_admin(ctx)
    return {"logs": [f"@source:Jira#{task_id} @trace:..."]}
