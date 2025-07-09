from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class BusinessFunction(Base):
    __tablename__ = "business_function"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core business function fields
    name = Column(String, nullable=False)
    description = Column(Text)
    competency_area = Column(String, nullable=False)  # Architecture Governance, Compliance Management, Strategy Analysis, Vendor Evaluation, etc.
    organizational_unit = Column(String, nullable=False)  # Department, division, or organizational unit
    owner_role_id = Column(UUID(as_uuid=True), ForeignKey("business_role.id"))
    
    # Input/Output specifications
    input_object_type = Column(String)  # Data objects, services, or other elements that serve as input
    output_object_type = Column(String)  # Data objects, services, or other elements that serve as output
    input_description = Column(Text)  # Detailed description of inputs
    output_description = Column(Text)  # Detailed description of outputs
    
    # Operational characteristics
    frequency = Column(String, nullable=False, default="ongoing")  # ongoing, daily, weekly, monthly, quarterly, annually, ad_hoc
    criticality = Column(String, nullable=False, default="medium")  # low, medium, high, critical
    complexity = Column(String, default="medium")  # simple, medium, complex, very_complex
    maturity_level = Column(String, default="basic")  # basic, developing, mature, advanced
    
    # Performance and alignment
    alignment_score = Column(Float, default=0.0)  # 0.0 to 1.0
    efficiency_score = Column(Float, default=0.0)  # 0.0 to 1.0
    effectiveness_score = Column(Float, default=0.0)  # 0.0 to 1.0
    performance_metrics = Column(Text)  # JSON string of performance metrics
    
    # Resource and capability
    required_skills = Column(Text)  # JSON string of required skills
    required_capabilities = Column(Text)  # JSON string of required capabilities
    resource_requirements = Column(Text)  # JSON string of resource requirements
    technology_dependencies = Column(Text)  # JSON string of technology dependencies
    
    # Governance and compliance
    compliance_requirements = Column(Text)  # JSON string of compliance requirements
    risk_level = Column(String, default="medium")  # low, medium, high, critical
    audit_frequency = Column(String, default="annually")  # monthly, quarterly, annually, ad_hoc
    last_audit_date = Column(DateTime)
    audit_status = Column(String, default="pending")  # pending, in_progress, completed, failed
    
    # Operational status
    status = Column(String, nullable=False, default="active")  # active, inactive, deprecated, planned
    operational_hours = Column(String, default="business_hours")  # 24x7, business_hours, on_demand
    availability_target = Column(Float, default=99.0)  # Percentage availability target
    current_availability = Column(Float, default=100.0)  # Current availability percentage
    
    # Strategic context
    strategic_importance = Column(String, default="medium")  # low, medium, high, critical
    business_value = Column(String, default="medium")  # low, medium, high, critical
    cost_center = Column(String)  # Cost center identifier
    budget_allocation = Column(Float)  # Budget allocation amount
    
    # Relationships and dependencies
    parent_function_id = Column(UUID(as_uuid=True), ForeignKey("business_function.id"))
    supporting_capability_id = Column(UUID(as_uuid=True), ForeignKey("capability.id"))
    business_process_id = Column(UUID(as_uuid=True), ForeignKey("business_process.id"))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("FunctionLink", back_populates="business_function")
    child_functions = relationship("BusinessFunction", backref="parent_function", remote_side=[id])

class FunctionLink(Base):
    __tablename__ = "function_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_function_id = Column(UUID(as_uuid=True), ForeignKey("business_function.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # business_role, business_process, capability, application_service, data_object, etc.
    link_type = Column(String, nullable=False)  # enables, supports, realizes, governs, influences, consumes, produces
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Operational context
    interaction_frequency = Column(String, default="regular")  # frequent, regular, occasional, rare
    interaction_type = Column(String, default="synchronous")  # synchronous, asynchronous, batch, real_time
    data_flow_direction = Column(String, default="bidirectional")  # input, output, bidirectional
    
    # Traceability
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business_function = relationship("BusinessFunction", back_populates="links") 