from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PromptTemplate(BaseModel):
    id: str
    name: str
    input_type: str
    layer: str
    template_text: str
    version: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class PromptTemplateUpdate(BaseModel):
    name: Optional[str] = None
    template_text: Optional[str] = None
    version: Optional[str] = None
