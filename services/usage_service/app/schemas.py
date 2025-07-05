from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UsageMetrics(BaseModel):
    tenant_id: str
    active_users: int
    model_count: int
    api_requests: int
    data_footprint: float

    class Config:
        orm_mode = True

class AuditEvent(BaseModel):
    id: int
    tenant_id: str
    user_id: str
    event_type: str
    event_time: datetime
    details: Optional[str]

    class Config:
        orm_mode = True

class SystemStats(BaseModel):
    uptime_percent: float
    error_rate_percent: float
    p95_latency_ms: float
    collected_at: datetime

    class Config:
        orm_mode = True
