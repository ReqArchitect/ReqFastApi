from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Event(Base):
    __tablename__ = "event"
    event_id = Column(String, primary_key=True)
    event_type = Column(String)
    payload = Column(JSON)
    source_service = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Subscription(Base):
    __tablename__ = "subscription"
    id = Column(String, primary_key=True)
    event_type = Column(String)
    subscriber_service = Column(String)
    callback_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
