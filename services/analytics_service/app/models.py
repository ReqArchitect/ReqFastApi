from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class TenantUsageSnapshot(Base):
    __tablename__ = "tenant_usage_snapshot"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    active_users = Column(Integer, default=0)
    model_count = Column(Integer, default=0)
    api_requests = Column(Integer, default=0)
    data_footprint_mb = Column(Float, default=0.0)

class BillingAlert(Base):
    __tablename__ = "billing_alert"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String, index=True)
    alert_type = Column(String)  # "api_limit", "storage_limit", "trial_expiry"
    triggered_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved = Column(Boolean, default=False)
