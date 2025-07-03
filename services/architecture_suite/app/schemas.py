from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class ArchitecturePackageBase(BaseModel):
    tenant_id: UUID
    user_id: UUID
    business_case_id: UUID
    initiative_id: UUID
    kpi_id: UUID
    business_model_id: UUID
    name: str
    description: Optional[str] = None

class ArchitecturePackageCreate(ArchitecturePackageBase):
    pass

class ArchitecturePackageUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    business_case_id: Optional[UUID] = None
    initiative_id: Optional[UUID] = None
    kpi_id: Optional[UUID] = None
    business_model_id: Optional[UUID] = None

class ArchitecturePackageInDB(ArchitecturePackageBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ArchitecturePackageOut(ArchitecturePackageInDB):
    pass
