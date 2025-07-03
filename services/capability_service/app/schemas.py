from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class CapabilityBase(BaseModel):
    name: str
    description: Optional[str] = None
    business_case_id: UUID4
    initiative_id: UUID4
    kpi_id: UUID4
    business_model_id: UUID4

class CapabilityCreate(CapabilityBase):
    pass

class CapabilityUpdate(CapabilityBase):
    pass

class CapabilityInDBBase(CapabilityBase):
    id: UUID4
    tenant_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Capability(CapabilityInDBBase):
    pass
