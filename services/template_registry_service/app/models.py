from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Template(Base):
    __tablename__ = "template"
    template_id = Column(String, primary_key=True)
    name = Column(String)
    input_type = Column(String)  # goal, kpi, initiative, canvas, architecture_text
    target_layer = Column(String)  # strategy, business, application, technology
    content = Column(Text)
    version = Column(String)
    created_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class TemplateUsageLog(Base):
    __tablename__ = "template_usage_log"
    usage_id = Column(String, primary_key=True)
    template_id = Column(String)
    user_id = Column(String)
    tenant_id = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    context = Column(JSON)
