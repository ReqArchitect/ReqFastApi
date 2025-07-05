from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class UsageMetrics(Base):
    __tablename__ = "usage_metrics"
    tenant_id = Column(String, primary_key=True)
    active_users = Column(Integer, default=0)
    model_count = Column(Integer, default=0)
    api_requests = Column(Integer, default=0)
    data_footprint = Column(Float, default=0.0)  # MB

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String, index=True)
    user_id = Column(String)
    event_type = Column(String)
    event_time = Column(DateTime, default=datetime.datetime.utcnow)
    details = Column(String)

class SystemStats(Base):
    __tablename__ = "system_stats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uptime_percent = Column(Float)
    error_rate_percent = Column(Float)
    p95_latency_ms = Column(Float)
    collected_at = Column(DateTime, default=datetime.datetime.utcnow)
