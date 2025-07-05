from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Enum as SqlEnum
from datetime import datetime
from typing import List
import enum

Base = declarative_base()

class JiraTypeEnum(str, enum.Enum):
    Epic = "Epic"
    Story = "Story"
    Subtask = "Subtask"

class TaskPayload(Base):
    __tablename__ = "task_payload"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(String)
    jira_type = Column(SqlEnum(JiraTypeEnum))
    linked_elements = Column(JSON)  # List[str]
    created_at = Column(DateTime, default=datetime.utcnow)

class GenerationRequest(Base):
    __tablename__ = "generation_request"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, index=True)
    generation_type = Column(String)  # backend, frontend, openapi, docs
    model_links = Column(JSON)  # List[str]
    status = Column(String, default="pending")  # pending, completed, error
    created_at = Column(DateTime, default=datetime.utcnow)
