from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class BusinessRole(Base):
    __tablename__ = "business_role"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core business role fields
    name = Column(String, nullable=False)
    description = Column(Text)
    organizational_unit = Column(String, nullable=False)  # Department, division, or organizational unit
    role_type = Column(String, nullable=False)  # Architecture Lead, Compliance Officer, Strategy Analyst, Vendor Manager, Data Custodian, etc.
    responsibilities = Column(Text)  # Detailed description of responsibilities
    required_skills = Column(Text)  # JSON string of required skills
    required_capabilities = Column(Text)  # JSON string of required capabilities
    stakeholder_id = Column(UUID(as_uuid=True), ForeignKey("stakeholder.id"))
    
    # Role classification and authority
    role_classification = Column(String, nullable=False, default="operational")  # strategic, tactical, operational, support
    authority_level = Column(String, nullable=False, default="standard")  # executive, senior, standard, junior, trainee
    decision_making_authority = Column(String, default="limited")  # full, partial, limited, none
    approval_authority = Column(String, default="none")  # full, partial, limited, none
    
    # Strategic context
    strategic_importance = Column(String, nullable=False, default="medium")  # low, medium, high, critical
    business_value = Column(String, default="medium")  # low, medium, high, critical
    capability_alignment = Column(Float, default=0.0)  # 0.0 to 1.0
    strategic_alignment = Column(Float, default=0.0)  # 0.0 to 1.0
    
    # Performance and effectiveness
    performance_score = Column(Float, default=0.0)  # 0.0 to 1.0
    effectiveness_score = Column(Float, default=0.0)  # 0.0 to 1.0
    efficiency_score = Column(Float, default=0.0)  # 0.0 to 1.0
    satisfaction_score = Column(Float, default=0.0)  # 0.0 to 1.0
    performance_metrics = Column(Text)  # JSON string of performance metrics
    
    # Operational characteristics
    criticality = Column(String, nullable=False, default="medium")  # low, medium, high, critical
    complexity = Column(String, default="medium")  # simple, medium, complex, very_complex
    workload_level = Column(String, default="standard")  # light, standard, heavy, overloaded
    availability_requirement = Column(String, default="business_hours")  # 24x7, business_hours, on_demand
    
    # Resource and capacity
    headcount_requirement = Column(Integer, default=1)  # Number of people required
    current_headcount = Column(Integer, default=0)  # Current number of people
    skill_gaps = Column(Text)  # JSON string of identified skill gaps
    training_requirements = Column(Text)  # JSON string of training needs
    
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
    
    # Cost and budget
    cost_center = Column(String)  # Cost center identifier
    budget_allocation = Column(Float)  # Budget allocation amount
    salary_range_min = Column(Float)  # Minimum salary for the role
    salary_range_max = Column(Float)  # Maximum salary for the role
    total_compensation = Column(Float)  # Total compensation including benefits
    
    # Relationships and dependencies
    reporting_to_role_id = Column(UUID(as_uuid=True), ForeignKey("business_role.id"))
    supporting_capability_id = Column(UUID(as_uuid=True), ForeignKey("capability.id"))
    business_function_id = Column(UUID(as_uuid=True), ForeignKey("business_function.id"))
    business_process_id = Column(UUID(as_uuid=True), ForeignKey("business_process.id"))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("RoleLink", back_populates="business_role")
    reports_to = relationship("BusinessRole", backref="reports", remote_side=[id])

class RoleLink(Base):
    __tablename__ = "role_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_role_id = Column(UUID(as_uuid=True), ForeignKey("business_role.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # business_function, business_process, application_service, data_object, stakeholder, etc.
    link_type = Column(String, nullable=False)  # performs, owns, manages, supports, collaborates, reports_to, supervises
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Operational context
    interaction_frequency = Column(String, default="regular")  # frequent, regular, occasional, rare
    interaction_type = Column(String, default="synchronous")  # synchronous, asynchronous, batch, real_time
    responsibility_level = Column(String, default="shared")  # primary, secondary, shared, advisory
    
    # Performance and accountability
    accountability_level = Column(String, default="shared")  # full, partial, shared, advisory
    performance_impact = Column(String, default="medium")  # high, medium, low, minimal
    decision_authority = Column(String, default="none")  # full, partial, limited, none
    
    # Traceability
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business_role = relationship("BusinessRole", back_populates="links") 