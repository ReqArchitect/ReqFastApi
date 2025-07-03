from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from . import schemas, services, deps
from .models import Capability
from typing import List

router = APIRouter()

@router.post("/capabilities", response_model=schemas.Capability)
def create_capability(
    capability_in: schemas.CapabilityCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    rbac=Depends(deps.rbac_check("capability:create")),
):
    return services.create_capability(db, capability_in, tenant_id, user_id)

@router.get("/capabilities", response_model=List[schemas.Capability])
def list_capabilities(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("capability:read")),
    skip: int = 0, limit: int = 100
):
    return services.get_capabilities(db, tenant_id, skip, limit)

@router.get("/capabilities/{id}", response_model=schemas.Capability)
def get_capability(
    id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("capability:read")),
):
    return services.get_capability(db, id, tenant_id)

@router.put("/capabilities/{id}", response_model=schemas.Capability)
def update_capability(
    id: UUID,
    capability_in: schemas.CapabilityUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("capability:update")),
):
    db_obj = services.get_capability(db, id, tenant_id)
    return services.update_capability(db, db_obj, capability_in)

@router.delete("/capabilities/{id}")
def delete_capability(
    id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("capability:delete")),
):
    db_obj = services.get_capability(db, id, tenant_id)
    services.delete_capability(db, db_obj)
    return {"ok": True}

@router.get("/capabilities/{id}/traceability-check")
def traceability_check(
    id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("capability:read")),
):
    # Implement traceability logic (stub)
    return {"traceability": "ok"}

@router.get("/capabilities/{id}/impact-summary")
def impact_summary(
    id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("capability:read")),
):
    # Implement impact summary logic (stub)
    return {"impact": "none"}
