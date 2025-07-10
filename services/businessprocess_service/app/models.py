from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class BusinessProcess(Base):
    __tablename__ = "business_process"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core business process fields
    name = Column(String, nullable=False)
    description = Column(Text)
    process_type = Column(String, nullable=False)  # operational, management, support
    input_object_type = Column(String)  # Type of input objects (e.g., "Customer Request", "Order")
    output_object_type = Column(String)  # Type of output objects (e.g., "Processed Order", "Approved Request")
    organizational_unit = Column(String, nullable=False)  # Department or organizational unit
    goal_id = Column(UUID(as_uuid=True), ForeignKey("goal.id"))
    capability_id = Column(UUID(as_uuid=True), ForeignKey("capability.id"))
    actor_id = Column(UUID(as_uuid=True), ForeignKey("actor.id"))
    role_id = Column(UUID(as_uuid=True), ForeignKey("business_role.id"))
    
    # Process classification and characteristics
    process_classification = Column(String, nullable=False, default="operational")  # operational, management, support, strategic
    criticality = Column(String, nullable=False, default="medium")  # low, medium, high, critical
    complexity = Column(String, default="medium")  # simple, medium, complex, very_complex
    automation_level = Column(String, default="manual")  # manual, semi_automated, automated, fully_automated
    
    # Performance and effectiveness
    performance_score = Column(Float, default=0.0)  # 0.0 to 1.0
    effectiveness_score = Column(Float, default=0.0)  # 0.0 to 1.0
    efficiency_score = Column(Float, default=0.0)  # 0.0 to 1.0
    quality_score = Column(Float, default=0.0)  # 0.0 to 1.0
    performance_metrics = Column(Text)  # JSON string of performance metrics
    
    # Operational characteristics
    status = Column(String, nullable=False, default="active")  # active, inactive, deprecated, planned
    priority = Column(String, default="medium")  # low, medium, high, critical
    frequency = Column(String, default="on_demand")  # continuous, daily, weekly, monthly, on_demand
    duration_target = Column(Float)  # Target duration in hours
    duration_average = Column(Float)  # Average actual duration in hours
    volume_target = Column(Integer)  # Target volume per period
    volume_actual = Column(Integer)  # Actual volume per period
    
    # Process flow and sequencing
    process_flow = Column(Text)  # JSON string describing process flow
    decision_points = Column(Text)  # JSON string of decision points
    handoff_points = Column(Text)  # JSON string of handoff points
    dependencies = Column(Text)  # JSON string of process dependencies
    
    # Resource and capacity
    resource_requirements = Column(Text)  # JSON string of resource requirements
    capacity_planning = Column(Text)  # JSON string of capacity planning data
    skill_requirements = Column(Text)  # JSON string of required skills
    training_requirements = Column(Text)  # JSON string of training needs
    
    # Governance and compliance
    compliance_requirements = Column(Text)  # JSON string of compliance requirements
    risk_level = Column(String, default="medium")  # low, medium, high, critical
    audit_frequency = Column(String, default="annually")  # monthly, quarterly, annually, ad_hoc
    last_audit_date = Column(DateTime)
    audit_status = Column(String, default="pending")  # pending, in_progress, completed, failed
    
    # Cost and budget
    cost_center = Column(String)  # Cost center identifier
    budget_allocation = Column(Float)  # Budget allocation amount
    cost_per_transaction = Column(Float)  # Cost per process execution
    roi_metrics = Column(Text)  # JSON string of ROI metrics
    
    # Technology and automation
    technology_stack = Column(Text)  # JSON string of technology stack
    automation_tools = Column(Text)  # JSON string of automation tools
    integration_points = Column(Text)  # JSON string of integration points
    data_requirements = Column(Text)  # JSON string of data requirements
    
    # Quality and standards
    quality_standards = Column(Text)  # JSON string of quality standards
    kpi_metrics = Column(Text)  # JSON string of KPI metrics
    sla_targets = Column(Text)  # JSON string of SLA targets
    quality_gates = Column(Text)  # JSON string of quality gates
    
    # Relationships and dependencies
    parent_process_id = Column(UUID(as_uuid=True), ForeignKey("business_process.id"))
    business_function_id = Column(UUID(as_uuid=True), ForeignKey("business_function.id"))
    application_service_id = Column(UUID(as_uuid=True), ForeignKey("application_service.id"))
    data_object_id = Column(UUID(as_uuid=True), ForeignKey("data_object.id"))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    steps = relationship("ProcessStep", back_populates="business_process")
    links = relationship("ProcessLink", back_populates="business_process")
    parent_process = relationship("BusinessProcess", backref="sub_processes", remote_side=[id])

class ProcessStep(Base):
    __tablename__ = "process_step"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_process_id = Column(UUID(as_uuid=True), ForeignKey("business_process.id"), nullable=False)
    step_order = Column(Integer, nullable=False)  # Order within the process
    name = Column(String, nullable=False)
    description = Column(Text)
    step_type = Column(String, nullable=False)  # task, decision, handoff, approval, review
    
    # Step characteristics
    responsible_role_id = Column(UUID(as_uuid=True), ForeignKey("business_role.id"))
    responsible_actor_id = Column(UUID(as_uuid=True), ForeignKey("actor.id"))
    duration_estimate = Column(Float)  # Estimated duration in hours
    duration_actual = Column(Float)  # Actual duration in hours
    complexity = Column(String, default="medium")  # simple, medium, complex
    
    # Step flow and logic
    input_criteria = Column(Text)  # JSON string of input criteria
    output_criteria = Column(Text)  # JSON string of output criteria
    decision_logic = Column(Text)  # JSON string of decision logic
    handoff_instructions = Column(Text)  # JSON string of handoff instructions
    
    # Step performance
    performance_score = Column(Float, default=0.0)  # 0.0 to 1.0
    quality_score = Column(Float, default=0.0)  # 0.0 to 1.0
    efficiency_score = Column(Float, default=0.0)  # 0.0 to 1.0
    bottleneck_indicator = Column(Boolean, default=False)
    
    # Step automation
    automation_level = Column(String, default="manual")  # manual, semi_automated, automated
    automation_tools = Column(Text)  # JSON string of automation tools
    integration_points = Column(Text)  # JSON string of integration points
    
    # Step governance
    approval_required = Column(Boolean, default=False)
    approval_role_id = Column(UUID(as_uuid=True), ForeignKey("business_role.id"))
    quality_gates = Column(Text)  # JSON string of quality gates
    compliance_checks = Column(Text)  # JSON string of compliance checks
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business_process = relationship("BusinessProcess", back_populates="steps")

class ProcessLink(Base):
    __tablename__ = "process_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_process_id = Column(UUID(as_uuid=True), ForeignKey("business_process.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # business_function, business_role, application_service, data_object, goal, capability, etc.
    link_type = Column(String, nullable=False)  # realizes, supports, uses, produces, consumes, triggers, enables
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Link characteristics
    interaction_frequency = Column(String, default="regular")  # frequent, regular, occasional, rare
    interaction_type = Column(String, default="synchronous")  # synchronous, asynchronous, batch, real_time
    responsibility_level = Column(String, default="shared")  # primary, secondary, shared, advisory
    
    # Performance and impact
    performance_impact = Column(String, default="medium")  # high, medium, low, minimal
    business_value_impact = Column(String, default="medium")  # high, medium, low, minimal
    risk_impact = Column(String, default="medium")  # high, medium, low, minimal
    
    # Flow and sequencing
    flow_direction = Column(String, default="bidirectional")  # input, output, bidirectional
    sequence_order = Column(Integer)  # Order in the process flow
    handoff_type = Column(String, default="standard")  # standard, automated, manual, exception
    
    # Traceability
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business_process = relationship("BusinessProcess", back_populates="links") 