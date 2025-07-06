from pydantic import BaseModel
from typing import Dict, Any

class AuditLogCreate(BaseModel):
    service: str
    event_type: str
    payload: Dict[str, Any]
