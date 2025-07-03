from .models import Capability
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from .schemas import CapabilityCreate, CapabilityUpdate
from fastapi import HTTPException

def get_capability(db: Session, capability_id: UUID, tenant_id: UUID) -> Capability:
    obj = db.query(Capability).filter(Capability.id == capability_id, Capability.tenant_id == tenant_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Capability not found")
    return obj

def get_capabilities(db: Session, tenant_id: UUID, skip: int = 0, limit: int = 100) -> List[Capability]:
    return db.query(Capability).filter(Capability.tenant_id == tenant_id).offset(skip).limit(limit).all()

def create_capability(db: Session, obj_in: CapabilityCreate, tenant_id: UUID, user_id: UUID) -> Capability:
    db_obj = Capability(**obj_in.dict(), tenant_id=tenant_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    # Emit event (stub)
    # emit_event("capability.created", db_obj)
    return db_obj

def update_capability(db: Session, db_obj: Capability, obj_in: CapabilityUpdate) -> Capability:
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    # emit_event("capability.updated", db_obj)
    return db_obj

def delete_capability(db: Session, db_obj: Capability):
    db.delete(db_obj)
    db.commit()
    # emit_event("capability.deleted", db_obj)
