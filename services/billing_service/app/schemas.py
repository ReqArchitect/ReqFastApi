from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class SubscriptionPlan(BaseModel):
    plan_id: str
    name: str
    limits: Dict[str, Any]
    price_per_month: float

    class Config:
        orm_mode = True

class TenantBillingProfile(BaseModel):
    tenant_id: str
    plan_id: str
    billing_email: str
    payment_method: str
    trial_expiry: datetime
    active: bool

    class Config:
        orm_mode = True

class BillingEvent(BaseModel):
    event_id: str
    tenant_id: str
    event_type: str
    timestamp: datetime
    metadata: Dict[str, Any]

    class Config:
        orm_mode = True
