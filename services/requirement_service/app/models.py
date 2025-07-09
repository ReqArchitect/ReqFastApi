from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class Requirement(Base):
    __tablename__ = "requirement"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core requirement fields
    name = Column(String, nullable=False)
    description = Column(Text)
    requirement_type = Column(String, nullable=False)  # functional, non-functional, business, technical
    priority = Column(String, nullable=False, default="medium")  # low, medium, high, critical
    status = Column(String, nullable=False, default="draft")  # draft, active, completed, deprecated
    
    # Traceability fields
    source = Column(String)  # Where the requirement originated
    stakeholder_id = Column(UUID(as_uuid=True), ForeignKey("stakeholder.id"))
    business_case_id = Column(UUID(as_uuid=True), ForeignKey("business_case.id"))
    initiative_id = Column(UUID(as_uuid=True), ForeignKey("initiative.id"))
    
    # Validation and compliance
    acceptance_criteria = Column(Text)
    validation_method = Column(String)  # test, review, demonstration, analysis
    compliance_required = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("RequirementLink", back_populates="requirement")

class RequirementLink(Base):
    __tablename__ = "requirement_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requirement_id = Column(UUID(as_uuid=True), ForeignKey("requirement.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # capability, business_process, application_function, etc.
    link_type = Column(String, nullable=False)  # implements, depends_on, conflicts_with, enhances
    link_strength = Column(String, default="medium")  # weak, medium, strong
    
    # Traceability
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    requirement = relationship("Requirement", back_populates="links") 