from sqlalchemy import Column, String, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plan"
    plan_id = Column(String, primary_key=True)
    name = Column(String)
    limits = Column(JSON)
    price_per_month = Column(Float)

class TenantBillingProfile(Base):
    __tablename__ = "tenant_billing_profile"
    tenant_id = Column(String, primary_key=True)
    plan_id = Column(String)
    billing_email = Column(String)
    payment_method = Column(String)
    trial_expiry = Column(DateTime)
    active = Column(Boolean, default=True)

class BillingEvent(Base):
    __tablename__ = "billing_event"
    event_id = Column(String, primary_key=True)
    tenant_id = Column(String)
    event_type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)
