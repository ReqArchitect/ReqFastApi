from pydantic import BaseModel
from typing import List
from datetime import datetime

class TenantUsageSnapshot(BaseModel):
    id: int
    tenant_id: str
    date: datetime
    active_users: int
    model_count: int
    api_requests: int
    data_footprint_mb: float

    class Config:
        orm_mode = True

class BillingAlert(BaseModel):
    id: int
    tenant_id: str
    alert_type: str
    triggered_at: datetime
    resolved: bool

    class Config:
        orm_mode = True
