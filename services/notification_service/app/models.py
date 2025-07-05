from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Notification(Base):
    __tablename__ = "notification"
    notification_id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    tenant_id = Column(String, index=True)
    channel = Column(String)  # email, toast, slack, webhook
    message = Column(Text)
    event_type = Column(String)
    delivered = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class NotificationTemplate(Base):
    __tablename__ = "notification_template"
    template_id = Column(String, primary_key=True)
    event_type = Column(String, index=True)
    channel = Column(String)
    content = Column(Text)
