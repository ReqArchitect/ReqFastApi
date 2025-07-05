from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class Event(BaseModel):
    event_id: str
    event_type: str
    payload: Dict[str, Any]
    source_service: str
    timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True

class Subscription(BaseModel):
    id: str
    event_type: str
    subscriber_service: str
    callback_url: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
