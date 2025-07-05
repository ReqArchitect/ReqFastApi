from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TaskPayload(BaseModel):
    task_id: str
    title: str
    description: str
    jira_type: str
    linked_elements: List[str]
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class GenerationRequest(BaseModel):
    task_id: str
    generation_type: str
    model_links: List[str]
    status: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
