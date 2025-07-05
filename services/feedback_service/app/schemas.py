from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Feedback(BaseModel):
    feedback_id: str
    user_id: str
    tenant_id: str
    context_type: str
    context_id: str
    rating: int
    comment: Optional[str] = None
    timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True

class FeedbackSummary(BaseModel):
    context_type: str
    context_id: str
    average_rating: float
    total_feedback: int

    class Config:
        orm_mode = True
