from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class CourseOfAction(Base):
    __tablename__ = "course_of_action"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core course of action fields
    name = Column(String, nullable=False)
    description = Column(Text)
    strategy_type = Column(String, nullable=False, default="transformational")  # transformational, incremental, defensive, innovative
    origin_goal_id = Column(UUID(as_uuid=True), ForeignKey("goal.id"))
    influenced_by_driver_id = Column(UUID(as_uuid=True), ForeignKey("driver.id"))
    impacted_capability_id = Column(UUID(as_uuid=True), ForeignKey("capability.id"))
    
    # Strategic context
    strategic_objective = Column(Text)  # Clear statement of what the course of action aims to achieve
    business_case = Column(Text)  # Justification and business value
    success_criteria = Column(Text)  # JSON string of measurable success criteria
    key_performance_indicators = Column(Text)  # JSON string of KPIs
    
    # Time and planning
    time_horizon = Column(String, default="medium_term")  # short_term, medium_term, long_term
    start_date = Column(DateTime)
    target_completion_date = Column(DateTime)
    actual_completion_date = Column(DateTime)
    implementation_phase = Column(String, default="planning")  # planning, active, completed, suspended
    
    # Risk and probability
    success_probability = Column(Float, default=0.5)  # 0.0 to 1.0
    risk_level = Column(String, default="medium")  # low, medium, high, critical
    risk_assessment = Column(Text)  # JSON string of risk factors and mitigation strategies
    contingency_plans = Column(Text)  # JSON string of backup plans
    
    # Resource and cost
    estimated_cost = Column(Float)
    actual_cost = Column(Float)
    budget_allocation = Column(Float)
    resource_requirements = Column(Text)  # JSON string of required resources
    cost_benefit_analysis = Column(Text)  # JSON string of cost-benefit analysis
    
    # Stakeholders and governance
    stakeholders = Column(Text)  # JSON string of key stakeholders
    governance_model = Column(String, default="standard")  # basic, standard, enhanced, critical
    approval_status = Column(String, default="draft")  # draft, pending, approved, rejected, completed
    approval_date = Column(DateTime)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    
    # Implementation details
    implementation_approach = Column(Text)  # Detailed implementation strategy
    milestones = Column(Text)  # JSON string of key milestones
    dependencies = Column(Text)  # JSON string of dependencies on other initiatives
    constraints = Column(Text)  # JSON string of constraints and limitations
    
    # Performance and outcomes
    current_progress = Column(Float, default=0.0)  # 0.0 to 100.0
    performance_metrics = Column(Text)  # JSON string of performance metrics
    outcomes_achieved = Column(Text)  # JSON string of achieved outcomes
    lessons_learned = Column(Text)  # JSON string of lessons learned
    
    # Strategic alignment
    strategic_alignment_score = Column(Float, default=0.0)  # 0.0 to 1.0
    capability_impact_score = Column(Float, default=0.0)  # 0.0 to 1.0
    goal_achievement_score = Column(Float, default=0.0)  # 0.0 to 1.0
    overall_effectiveness_score = Column(Float, default=0.0)  # 0.0 to 1.0
    
    # Compliance and audit
    compliance_requirements = Column(Text)  # JSON string of compliance requirements
    audit_trail = Column(Text)  # JSON string of audit events
    regulatory_impact = Column(Text)  # JSON string of regulatory considerations
    
    # Technology and systems
    technology_requirements = Column(Text)  # JSON string of technology needs
    system_impact = Column(Text)  # JSON string of system changes required
    integration_requirements = Column(Text)  # JSON string of integration needs
    
    # Change management
    change_management_plan = Column(Text)  # JSON string of change management approach
    communication_plan = Column(Text)  # JSON string of communication strategy
    training_requirements = Column(Text)  # JSON string of training needs
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("ActionLink", back_populates="course_of_action")

class ActionLink(Base):
    __tablename__ = "action_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_of_action_id = Column(UUID(as_uuid=True), ForeignKey("course_of_action.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # goal, requirement, capability, business_process, assessment, driver, constraint, etc.
    link_type = Column(String, nullable=False)  # realizes, supports, enables, influences, constrains, triggers, requires
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Strategic context
    strategic_importance = Column(String, default="medium")  # low, medium, high, critical
    business_value = Column(String, default="medium")  # low, medium, high, critical
    alignment_score = Column(Float)  # 0.0 to 1.0 - how well aligned this link is
    
    # Implementation context
    implementation_priority = Column(String, default="normal")  # low, normal, high, critical
    implementation_phase = Column(String, default="planning")  # planning, active, completed
    resource_allocation = Column(Float)  # Percentage of resources allocated to this link
    
    # Impact assessment
    impact_level = Column(String, default="medium")  # low, medium, high, critical
    impact_direction = Column(String, default="positive")  # positive, negative, neutral
    impact_confidence = Column(Float)  # 0.0 to 1.0 - confidence in impact assessment
    
    # Risk and constraints
    risk_level = Column(String, default="medium")  # low, medium, high, critical
    constraint_level = Column(String, default="medium")  # low, medium, high, critical
    risk_mitigation = Column(Text)  # JSON string of risk mitigation strategies
    
    # Performance tracking
    performance_contribution = Column(Float)  # Percentage contribution to overall performance
    success_contribution = Column(Float)  # Percentage contribution to success criteria
    outcome_measurement = Column(Text)  # JSON string of outcome measurement approach
    
    # Traceability
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    course_of_action = relationship("CourseOfAction", back_populates="links") 