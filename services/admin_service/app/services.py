from .models import Admin
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from .schemas import AdminCreate, AdminUpdate
from fastapi import HTTPException

def get_admin(db: Session, admin_id: UUID, tenant_id: UUID) -> Admin:
    obj = db.query(Admin).filter(Admin.id == admin_id, Admin.tenant_id == tenant_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Admin not found")
    return obj

def get_admins(db: Session, tenant_id: UUID, skip: int = 0, limit: int = 100) -> List[Admin]:
    return db.query(Admin).filter(Admin.tenant_id == tenant_id).offset(skip).limit(limit).all()

def create_admin(db: Session, obj_in: AdminCreate, tenant_id: UUID, user_id: UUID) -> Admin:
    db_obj = Admin(**obj_in.dict(), tenant_id=tenant_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    # Emit event (stub)
    # emit_event("admin.created", db_obj)
    return db_obj

def update_admin(db: Session, db_obj: Admin, obj_in: AdminUpdate) -> Admin:
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    # emit_event("admin.updated", db_obj)
    return db_obj

def delete_admin(db: Session, db_obj: Admin):
    db.delete(db_obj)
    db.commit()
    # emit_event("admin.deleted", db_obj)
