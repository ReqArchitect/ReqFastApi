from pydantic import BaseModel, UUID4, EmailStr
from typing import Optional
from datetime import datetime

class AdminBase(BaseModel):
    name: str
    email: EmailStr
    description: Optional[str] = None
    business_case_id: UUID4
    initiative_id: UUID4
    kpi_id: UUID4
    business_model_id: UUID4

class AdminCreate(AdminBase):
    pass

class AdminUpdate(AdminBase):
    pass

class AdminInDBBase(AdminBase):
    id: UUID4
    tenant_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Admin(AdminInDBBase):
    pass
