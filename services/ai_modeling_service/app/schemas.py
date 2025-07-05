from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class ModelingInput(BaseModel):
    tenant_id: str
    user_id: str
    input_type: str
    input_text: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ModelingOutput(BaseModel):
    id: int
    input_id: int
    layer: str
    elements: List[Dict]
    traceability: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ModelingFeedback(BaseModel):
    output_id: int
    user_id: str
    rating: int
    comments: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
