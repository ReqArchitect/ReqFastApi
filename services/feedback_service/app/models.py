from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Feedback(Base):
    __tablename__ = "feedback"
    feedback_id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    tenant_id = Column(String, index=True)
    context_type = Column(String)  # ai_modeling, onboarding, usage_dashboard, template
    context_id = Column(String)
    rating = Column(Integer)
    comment = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class FeedbackSummary(Base):
    __tablename__ = "feedback_summary"
    id = Column(String, primary_key=True)
    context_type = Column(String)
    context_id = Column(String)
    average_rating = Column(Float)
    total_feedback = Column(Integer)
