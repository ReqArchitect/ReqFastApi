from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class Gap(Base):
    __tablename__ = "gap"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core gap fields
    name = Column(String, nullable=False)
    description = Column(Text)
    gap_type = Column(String, nullable=False)  # capability, process, technology, compliance, performance, data, security
    severity = Column(String, nullable=False)  # low, medium, high, critical
    impact_area = Column(String, nullable=False)  # business, application, technology, data, security, compliance
    
    # Plateau relationships
    source_plateau_id = Column(UUID(as_uuid=True), ForeignKey("plateau.id"))  # Source plateau
    target_plateau_id = Column(UUID(as_uuid=True), ForeignKey("plateau.id"))  # Target plateau
    
    # Related elements
    related_requirement_id = Column(UUID(as_uuid=True), ForeignKey("requirement.id"))
    related_capability_id = Column(UUID(as_uuid=True), ForeignKey("capability.id"))
    related_constraint_id = Column(UUID(as_uuid=True), ForeignKey("constraint.id"))
    related_workpackage_id = Column(UUID(as_uuid=True), ForeignKey("workpackage.id"))
    
    # Resolution and mitigation
    mitigation_strategy = Column(Text)  # JSON string of mitigation strategy
    resolution_approach = Column(String)  # workaround, temporary_fix, permanent_solution, redesign
    time_to_resolve_estimate = Column(Integer)  # Estimated time to resolve in days
    resolution_priority = Column(String, default="medium")  # low, medium, high, critical
    resolution_status = Column(String, default="open")  # open, in_progress, resolved, closed, cancelled
    
    # Impact assessment
    business_impact = Column(String, default="medium")  # low, medium, high, critical
    technical_impact = Column(String, default="medium")  # low, medium, high, critical
    operational_impact = Column(String, default="medium")  # low, medium, high, critical
    financial_impact = Column(String, default="medium")  # low, medium, high, critical
    
    # Risk assessment
    risk_level = Column(String, default="medium")  # low, medium, high, critical
    risk_description = Column(Text)  # Risk description
    risk_mitigation = Column(Text)  # JSON string of risk mitigation
    contingency_plan = Column(Text)  # JSON string of contingency plan
    
    # Cost and effort
    estimated_cost = Column(Float)  # Estimated cost to resolve
    actual_cost = Column(Float)  # Actual cost spent
    effort_estimate = Column(Integer)  # Effort estimate in person-days
    actual_effort = Column(Integer)  # Actual effort spent in person-days
    
    # Timeline and scheduling
    identified_date = Column(DateTime, default=datetime.utcnow)  # When gap was identified
    planned_resolution_date = Column(DateTime)  # Planned resolution date
    actual_resolution_date = Column(DateTime)  # Actual resolution date
    deadline = Column(DateTime)  # Hard deadline for resolution
    
    # Dependencies and blockers
    dependencies = Column(Text)  # JSON string of dependencies
    blockers = Column(Text)  # JSON string of blockers
    prerequisites = Column(Text)  # JSON string of prerequisites
    related_gaps = Column(Text)  # JSON string of related gap IDs
    
    # Stakeholders and ownership
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))  # Gap owner
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))  # Person assigned to resolve
    stakeholder_ids = Column(Text)  # JSON string of stakeholder IDs
    approver_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))  # Person who approves resolution
    
    # Analysis and assessment
    root_cause_analysis = Column(Text)  # JSON string of root cause analysis
    impact_analysis = Column(Text)  # JSON string of impact analysis
    solution_alternatives = Column(Text)  # JSON string of solution alternatives
    recommended_solution = Column(Text)  # JSON string of recommended solution
    
    # Compliance and governance
    compliance_impact = Column(String, default="low")  # low, medium, high, critical
    regulatory_requirements = Column(Text)  # JSON string of regulatory requirements
    audit_trail = Column(Text)  # JSON string of audit trail
    approval_status = Column(String, default="pending")  # pending, approved, rejected
    
    # Performance metrics
    performance_impact = Column(String, default="medium")  # low, medium, high, critical
    efficiency_loss = Column(Float)  # Efficiency loss percentage
    quality_impact = Column(String, default="medium")  # low, medium, high, critical
    customer_impact = Column(String, default="medium")  # low, medium, high, critical
    
    # Technology and architecture
    technology_impact = Column(String, default="medium")  # low, medium, high, critical
    architecture_impact = Column(String, default="medium")  # low, medium, high, critical
    integration_impact = Column(String, default="medium")  # low, medium, high, critical
    data_impact = Column(String, default="medium")  # low, medium, high, critical
    
    # Security and privacy
    security_impact = Column(String, default="medium")  # low, medium, high, critical
    privacy_impact = Column(String, default="medium")  # low, medium, high, critical
    security_requirements = Column(Text)  # JSON string of security requirements
    privacy_requirements = Column(Text)  # JSON string of privacy requirements
    
    # Communication and reporting
    communication_plan = Column(Text)  # JSON string of communication plan
    reporting_frequency = Column(String, default="weekly")  # daily, weekly, monthly
    escalation_procedures = Column(Text)  # JSON string of escalation procedures
    stakeholder_updates = Column(Text)  # JSON string of stakeholder updates
    
    # Progress tracking
    progress_percentage = Column(Float, default=0.0)  # Progress percentage (0.0 to 100.0)
    milestone_achievements = Column(Text)  # JSON string of milestone achievements
    blockers_encountered = Column(Text)  # JSON string of blockers encountered
    lessons_learned = Column(Text)  # JSON string of lessons learned
    
    # Quality and testing
    quality_gates = Column(Text)  # JSON string of quality gates
    testing_requirements = Column(Text)  # JSON string of testing requirements
    validation_criteria = Column(Text)  # JSON string of validation criteria
    acceptance_criteria = Column(Text)  # JSON string of acceptance criteria
    
    # Documentation and knowledge
    documentation_status = Column(String, default="in_progress")  # not_started, in_progress, completed
    knowledge_transfer = Column(Text)  # JSON string of knowledge transfer
    best_practices = Column(Text)  # JSON string of best practices
    training_requirements = Column(Text)  # JSON string of training requirements
    
    # Status and lifecycle
    status = Column(String, default="open")  # open, in_progress, resolved, closed, cancelled
    lifecycle_state = Column(String, default="identified")  # identified, analyzed, planned, implementing, resolved
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("GapLink", back_populates="gap")

class GapLink(Base):
    __tablename__ = "gap_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gap_id = Column(UUID(as_uuid=True), ForeignKey("gap.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # capability, requirement, constraint, workpackage, component, node, etc.
    link_type = Column(String, nullable=False)  # impacts, depends_on, blocks, enables, constrains, realizes
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Impact context
    impact_level = Column(String, default="medium")  # low, medium, high, critical
    impact_type = Column(String, default="direct")  # direct, indirect, cascading
    impact_duration = Column(String, default="temporary")  # temporary, permanent, recurring
    impact_scope = Column(String, default="local")  # local, regional, global
    
    # Business context
    business_criticality = Column(String, default="medium")  # low, medium, high, critical
    business_value = Column(String, default="medium")  # low, medium, high, critical
    strategic_importance = Column(String, default="medium")  # low, medium, high, critical
    stakeholder_impact = Column(String, default="medium")  # low, medium, high, critical
    
    # Technical context
    technical_complexity = Column(String, default="medium")  # low, medium, high, very_high
    implementation_effort = Column(String, default="medium")  # low, medium, high, very_high
    technical_risk = Column(String, default="medium")  # low, medium, high, critical
    integration_impact = Column(String, default="medium")  # low, medium, high, critical
    
    # Resolution context
    resolution_priority = Column(String, default="medium")  # low, medium, high, critical
    resolution_approach = Column(String, default="standard")  # standard, workaround, redesign, replacement
    resolution_timeline = Column(Text)  # JSON string of resolution timeline
    resolution_dependencies = Column(Text)  # JSON string of resolution dependencies
    
    # Resource context
    resource_requirements = Column(Text)  # JSON string of resource requirements
    skill_requirements = Column(Text)  # JSON string of skill requirements
    budget_impact = Column(Float)  # Budget impact in currency
    effort_estimate = Column(Integer)  # Effort estimate in person-days
    
    # Performance context
    performance_impact = Column(String, default="medium")  # low, medium, high, critical
    efficiency_impact = Column(String, default="medium")  # low, medium, high, critical
    quality_impact = Column(String, default="medium")  # low, medium, high, critical
    reliability_impact = Column(String, default="medium")  # low, medium, high, critical
    
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
    gap = relationship("Gap", back_populates="links") 