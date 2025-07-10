from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class Plateau(Base):
    __tablename__ = "plateau"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core plateau fields
    name = Column(String, nullable=False)
    description = Column(Text)
    time_window_start = Column(DateTime, nullable=False)
    time_window_end = Column(DateTime, nullable=False)
    maturity_level = Column(String, nullable=False)  # initial, developing, mature, optimized
    business_value_score = Column(Float, default=0.0)  # 0.0 to 1.0
    transformation_phase = Column(String, nullable=False)  # planning, implementation, validation, deployment, maintenance
    status = Column(String, default="planned")  # planned, current, historical, cancelled
    
    # Stakeholder and ownership
    stakeholder_id = Column(UUID(as_uuid=True), ForeignKey("stakeholder.id"))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    sponsor_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    
    # Associated capabilities and components
    associated_capability_ids = Column(Text)  # JSON string of capability IDs
    associated_goal_ids = Column(Text)  # JSON string of goal IDs
    associated_workpackage_ids = Column(Text)  # JSON string of workpackage IDs
    associated_component_ids = Column(Text)  # JSON string of component IDs
    associated_gap_ids = Column(Text)  # JSON string of gap IDs
    
    # Architecture snapshot
    snapshot_hash = Column(String, unique=True)  # Hash of architecture snapshot
    snapshot_data = Column(Text)  # JSON string of architecture snapshot
    baseline_architecture_id = Column(UUID(as_uuid=True), ForeignKey("architecture.id"))
    target_architecture_id = Column(UUID(as_uuid=True), ForeignKey("architecture.id"))
    
    # Progress and metrics
    completion_percentage = Column(Float, default=0.0)  # 0.0 to 100.0
    on_track_score = Column(Float, default=0.0)  # 0.0 to 1.0
    risk_score = Column(Float, default=0.0)  # 0.0 to 1.0
    quality_score = Column(Float, default=0.0)  # 0.0 to 1.0
    
    # Financial metrics
    budget_allocated = Column(Float)  # Budget allocated in currency
    budget_spent = Column(Float)  # Budget spent in currency
    cost_savings = Column(Float)  # Cost savings achieved
    roi_percentage = Column(Float)  # Return on investment percentage
    business_impact_score = Column(Float)  # 0.0 to 1.0
    
    # Timeline and milestones
    planned_start_date = Column(DateTime)
    planned_end_date = Column(DateTime)
    actual_start_date = Column(DateTime)
    actual_end_date = Column(DateTime)
    critical_path_duration = Column(Integer)  # Duration in days
    slack_days = Column(Integer)  # Available slack in days
    
    # Dependencies and constraints
    dependencies = Column(Text)  # JSON string of dependencies
    constraints = Column(Text)  # JSON string of constraints
    assumptions = Column(Text)  # JSON string of assumptions
    risks = Column(Text)  # JSON string of risks
    
    # Change management
    change_requests = Column(Text)  # JSON string of change requests
    approved_changes = Column(Text)  # JSON string of approved changes
    rejected_changes = Column(Text)  # JSON string of rejected changes
    change_impact_assessment = Column(Text)  # JSON string of impact assessment
    
    # Quality and compliance
    quality_gates = Column(Text)  # JSON string of quality gates
    compliance_requirements = Column(Text)  # JSON string of compliance requirements
    audit_trail = Column(Text)  # JSON string of audit trail
    approval_status = Column(String, default="pending")  # pending, approved, rejected
    
    # Communication and reporting
    communication_plan = Column(Text)  # JSON string of communication plan
    stakeholder_updates = Column(Text)  # JSON string of stakeholder updates
    reporting_frequency = Column(String, default="weekly")  # daily, weekly, monthly
    escalation_procedures = Column(Text)  # JSON string of escalation procedures
    
    # Performance metrics
    kpi_targets = Column(Text)  # JSON string of KPI targets
    kpi_actuals = Column(Text)  # JSON string of KPI actuals
    performance_metrics = Column(Text)  # JSON string of performance metrics
    success_criteria = Column(Text)  # JSON string of success criteria
    
    # Resource allocation
    resource_requirements = Column(Text)  # JSON string of resource requirements
    resource_allocation = Column(Text)  # JSON string of resource allocation
    skill_requirements = Column(Text)  # JSON string of skill requirements
    training_requirements = Column(Text)  # JSON string of training requirements
    
    # Technology and infrastructure
    technology_stack = Column(Text)  # JSON string of technology stack
    infrastructure_requirements = Column(Text)  # JSON string of infrastructure requirements
    integration_requirements = Column(Text)  # JSON string of integration requirements
    migration_strategy = Column(Text)  # JSON string of migration strategy
    
    # Business alignment
    business_objectives = Column(Text)  # JSON string of business objectives
    strategic_alignment = Column(Float)  # 0.0 to 1.0
    stakeholder_satisfaction = Column(Float)  # 0.0 to 1.0
    business_readiness = Column(Float)  # 0.0 to 1.0
    
    # Lessons learned and knowledge management
    lessons_learned = Column(Text)  # JSON string of lessons learned
    best_practices = Column(Text)  # JSON string of best practices
    documentation_status = Column(String, default="in_progress")  # not_started, in_progress, completed
    knowledge_transfer = Column(Text)  # JSON string of knowledge transfer
    
    # Governance and oversight
    governance_structure = Column(Text)  # JSON string of governance structure
    decision_making_process = Column(Text)  # JSON string of decision making process
    escalation_matrix = Column(Text)  # JSON string of escalation matrix
    approval_workflow = Column(Text)  # JSON string of approval workflow
    
    # Risk management
    risk_register = Column(Text)  # JSON string of risk register
    mitigation_strategies = Column(Text)  # JSON string of mitigation strategies
    contingency_plans = Column(Text)  # JSON string of contingency plans
    risk_monitoring = Column(Text)  # JSON string of risk monitoring
    
    # Status and lifecycle
    lifecycle_state = Column(String, default="planning")  # planning, active, completed, cancelled
    priority_level = Column(String, default="medium")  # low, medium, high, critical
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("PlateauLink", back_populates="plateau")

class PlateauLink(Base):
    __tablename__ = "plateau_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plateau_id = Column(UUID(as_uuid=True), ForeignKey("plateau.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # goal, workpackage, capability, component, gap, etc.
    link_type = Column(String, nullable=False)  # realizes, supports, enables, depends_on, impacts
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Transformation context
    transformation_impact = Column(String, default="medium")  # low, medium, high, critical
    change_scope = Column(String, default="moderate")  # minor, moderate, major, transformational
    implementation_complexity = Column(String, default="medium")  # low, medium, high, very_high
    risk_level = Column(String, default="medium")  # low, medium, high, critical
    
    # Business context
    business_criticality = Column(String, default="medium")  # low, medium, high, critical
    business_value = Column(String, default="medium")  # low, medium, high, critical
    strategic_importance = Column(String, default="medium")  # low, medium, high, critical
    stakeholder_impact = Column(String, default="medium")  # low, medium, high, critical
    
    # Implementation context
    implementation_status = Column(String, default="planned")  # planned, in_progress, completed, failed
    implementation_priority = Column(String, default="medium")  # low, medium, high, critical
    implementation_phase = Column(String, default="planning")  # planning, implementation, validation, deployment
    implementation_timeline = Column(Text)  # JSON string of implementation timeline
    
    # Resource context
    resource_requirements = Column(Text)  # JSON string of resource requirements
    skill_requirements = Column(Text)  # JSON string of skill requirements
    budget_impact = Column(Float)  # Budget impact in currency
    effort_estimate = Column(Integer)  # Effort estimate in person-days
    
    # Performance context
    performance_impact = Column(String, default="medium")  # low, medium, high, critical
    quality_impact = Column(String, default="medium")  # low, medium, high, critical
    efficiency_gain = Column(Float)  # Efficiency gain percentage
    effectiveness_improvement = Column(Float)  # Effectiveness improvement percentage
    
    # Risk and compliance
    risk_assessment = Column(Text)  # JSON string of risk assessment
    compliance_impact = Column(String, default="low")  # low, medium, high, critical
    security_impact = Column(String, default="medium")  # low, medium, high, critical
    regulatory_impact = Column(String, default="low")  # low, medium, high, critical
    
    # Success metrics
    success_criteria = Column(Text)  # JSON string of success criteria
    kpi_targets = Column(Text)  # JSON string of KPI targets
    measurement_framework = Column(Text)  # JSON string of measurement framework
    validation_approach = Column(Text)  # JSON string of validation approach
    
    # Dependencies and constraints
    dependencies = Column(Text)  # JSON string of dependencies
    constraints = Column(Text)  # JSON string of constraints
    prerequisites = Column(Text)  # JSON string of prerequisites
    blockers = Column(Text)  # JSON string of blockers
    
    # Communication and change management
    communication_plan = Column(Text)  # JSON string of communication plan
    change_management_approach = Column(Text)  # JSON string of change management approach
    stakeholder_engagement = Column(Text)  # JSON string of stakeholder engagement
    training_requirements = Column(Text)  # JSON string of training requirements
    
    # Monitoring and governance
    monitoring_framework = Column(Text)  # JSON string of monitoring framework
    governance_structure = Column(Text)  # JSON string of governance structure
    escalation_procedures = Column(Text)  # JSON string of escalation procedures
    approval_workflow = Column(Text)  # JSON string of approval workflow
    
    # Traceability
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    plateau = relationship("Plateau", back_populates="links") 