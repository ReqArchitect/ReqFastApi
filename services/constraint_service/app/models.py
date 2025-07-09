from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class Constraint(Base):
    __tablename__ = "constraint"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core constraint fields
    name = Column(String, nullable=False)
    description = Column(Text)
    constraint_type = Column(String, nullable=False)  # technical, regulatory, organizational, environmental, financial
    scope = Column(String, nullable=False)  # global, domain, project, component
    severity = Column(String, nullable=False, default="medium")  # low, medium, high, critical
    enforcement_level = Column(String, nullable=False, default="mandatory")  # mandatory, recommended, optional
    
    # Stakeholder and ownership
    stakeholder_id = Column(UUID(as_uuid=True), ForeignKey("stakeholder.id"))
    business_actor_id = Column(UUID(as_uuid=True), ForeignKey("business_actor.id"))
    
    # Risk and compliance
    risk_profile = Column(String, default="medium")  # low, medium, high, critical
    compliance_required = Column(Boolean, default=False)
    regulatory_framework = Column(String)  # GDPR, SOX, ISO, etc.
    
    # Mitigation and management
    mitigation_strategy = Column(Text)
    mitigation_status = Column(String, default="pending")  # pending, in_progress, implemented, verified
    mitigation_effort = Column(String, default="medium")  # low, medium, high, critical
    
    # Impact assessment
    business_impact = Column(String, default="medium")  # low, medium, high, critical
    technical_impact = Column(String, default="medium")  # low, medium, high, critical
    operational_impact = Column(String, default="medium")  # low, medium, high, critical
    
    # Time and lifecycle
    effective_date = Column(DateTime)
    expiry_date = Column(DateTime)
    review_frequency = Column(String)  # monthly, quarterly, annually, ad_hoc
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("ConstraintLink", back_populates="constraint")

class ConstraintLink(Base):
    __tablename__ = "constraint_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    constraint_id = Column(UUID(as_uuid=True), ForeignKey("constraint.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # goal, requirement, capability, application_component, business_process, etc.
    link_type = Column(String, nullable=False)  # constrains, limits, restricts, governs, regulates
    impact_level = Column(String, default="medium")  # low, medium, high, critical
    compliance_status = Column(String, default="compliant")  # compliant, non_compliant, partially_compliant, exempt
    
    # Traceability
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    constraint = relationship("Constraint", back_populates="links") 