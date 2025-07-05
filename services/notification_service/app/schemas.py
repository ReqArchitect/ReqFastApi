from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Notification(BaseModel):
    notification_id: str
    user_id: str
    tenant_id: str
    channel: str
    message: str
    event_type: str
    delivered: bool
    timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True

class NotificationTemplate(BaseModel):
    template_id: str
    event_type: str
    channel: str
    content: str

    class Config:
        orm_mode = True
