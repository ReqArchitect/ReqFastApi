from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class Driver(Base):
    __tablename__ = "driver"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core driver fields
    name = Column(String, nullable=False)
    description = Column(Text)
    driver_type = Column(String, nullable=False)  # business, technical, regulatory, environmental, social
    category = Column(String, nullable=False)  # internal, external, strategic, operational
    urgency = Column(String, nullable=False, default="medium")  # low, medium, high, critical
    impact_level = Column(String, nullable=False, default="medium")  # low, medium, high, critical
    
    # Source and stakeholder information
    source = Column(String)  # Where the driver originated
    stakeholder_id = Column(UUID(as_uuid=True), ForeignKey("stakeholder.id"))
    business_actor_id = Column(UUID(as_uuid=True), ForeignKey("business_actor.id"))
    
    # Strategic context
    strategic_priority = Column(Integer, default=3)  # 1-5 scale
    time_horizon = Column(String)  # short-term, medium-term, long-term
    geographic_scope = Column(String)  # local, regional, national, global
    
    # Compliance and risk
    compliance_required = Column(Boolean, default=False)
    risk_level = Column(String, default="medium")  # low, medium, high, critical
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("DriverLink", back_populates="driver")

class DriverLink(Base):
    __tablename__ = "driver_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    driver_id = Column(UUID(as_uuid=True), ForeignKey("driver.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # goal, requirement, capability, business_actor, etc.
    link_type = Column(String, nullable=False)  # influences, drives, constrains, enables
    link_strength = Column(String, default="medium")  # weak, medium, strong
    influence_direction = Column(String, default="positive")  # positive, negative, neutral
    
    # Traceability
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    driver = relationship("Driver", back_populates="links") 