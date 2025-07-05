from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PromptTemplate(Base):
    __tablename__ = "prompt_template"
    id = Column(String, primary_key=True)
    name = Column(String)
    input_type = Column(String)  # goal, kpi, initiative, canvas, architecture_text
    layer = Column(String)  # strategy, business, application, etc.
    template_text = Column(Text)
    version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
