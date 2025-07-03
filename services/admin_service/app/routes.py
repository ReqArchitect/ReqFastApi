from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from . import schemas, services, deps
from .models import Admin
from typing import List

router = APIRouter()

@router.post("/admins", response_model=schemas.Admin)
def create_admin(
    admin_in: schemas.AdminCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    rbac=Depends(deps.rbac_check("admin:create")),
):
    return services.create_admin(db, admin_in, tenant_id, user_id)

@router.get("/admins", response_model=List[schemas.Admin])
def list_admins(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("admin:read")),
    skip: int = 0, limit: int = 100
):
    return services.get_admins(db, tenant_id, skip, limit)

@router.get("/admins/{id}", response_model=schemas.Admin)
def get_admin(
    id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("admin:read")),
):
    return services.get_admin(db, id, tenant_id)

@router.put("/admins/{id}", response_model=schemas.Admin)
def update_admin(
    id: UUID,
    admin_in: schemas.AdminUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("admin:update")),
):
    db_obj = services.get_admin(db, id, tenant_id)
    return services.update_admin(db, db_obj, admin_in)

@router.delete("/admins/{id}")
def delete_admin(
    id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("admin:delete")),
):
    db_obj = services.get_admin(db, id, tenant_id)
    services.delete_admin(db, db_obj)
    return {"ok": True}
