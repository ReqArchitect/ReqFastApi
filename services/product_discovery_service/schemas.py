from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class BusinessCase(BaseModel):
    uuid: UUID
    tenant_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    title: str
    description: str

class Initiative(BaseModel):
    uuid: UUID
    tenant_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    business_case_id: UUID
    name: str
    description: str

class KPI(BaseModel):
    uuid: UUID
    tenant_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    initiative_id: UUID  # Ensure this is always a valid UUID string in test payloads
    metric: str
    target_value: float

class BusinessModelCanvas(BaseModel):
    uuid: UUID
    tenant_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    canvas_data: dict

    model_config = {
        "extra": "forbid"
    }
