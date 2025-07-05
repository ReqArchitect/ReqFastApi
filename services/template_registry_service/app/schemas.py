from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class Template(BaseModel):
    template_id: str
    name: str
    input_type: str
    target_layer: str
    content: str
    version: str
    created_by: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    version: Optional[str] = None

class TemplateUsageLog(BaseModel):
    usage_id: str
    template_id: str
    user_id: str
    tenant_id: str
    timestamp: Optional[datetime] = None
    context: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True
