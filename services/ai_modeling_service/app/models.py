from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ModelingInput(Base):
    __tablename__ = "modeling_input"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String, index=True)
    user_id = Column(String, index=True)
    input_type = Column(String)  # goal, initiative, kpi, canvas, architecture_text
    input_text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class ModelingOutput(Base):
    __tablename__ = "modeling_output"
    id = Column(Integer, primary_key=True, autoincrement=True)
    input_id = Column(Integer)
    layer = Column(String)
    elements = Column(JSON)  # List[Dict]
    traceability = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class ModelingFeedback(Base):
    __tablename__ = "modeling_feedback"
    id = Column(Integer, primary_key=True, autoincrement=True)
    output_id = Column(Integer)
    user_id = Column(String)
    rating = Column(Integer)
    comments = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
