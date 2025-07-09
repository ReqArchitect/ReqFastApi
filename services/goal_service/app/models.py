from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class Goal(Base):
    __tablename__ = "goal"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core goal fields
    name = Column(String, nullable=False)
    description = Column(Text)
    goal_type = Column(String, nullable=False)  # strategic, operational, technical, tactical
    priority = Column(String, nullable=False, default="medium")  # low, medium, high, critical
    status = Column(String, nullable=False, default="active")  # active, achieved, abandoned, on_hold
    
    # Strategic context
    origin_driver_id = Column(UUID(as_uuid=True), ForeignKey("driver.id"))
    stakeholder_id = Column(UUID(as_uuid=True), ForeignKey("stakeholder.id"))
    business_actor_id = Column(UUID(as_uuid=True), ForeignKey("business_actor.id"))
    
    # Success criteria and measurement
    success_criteria = Column(Text)
    key_performance_indicators = Column(Text)  # JSON string of KPIs
    measurement_frequency = Column(String)  # daily, weekly, monthly, quarterly, annually
    
    # Timeline and milestones
    target_date = Column(DateTime)
    start_date = Column(DateTime)
    completion_date = Column(DateTime)
    review_frequency = Column(String)  # monthly, quarterly, annually, ad_hoc
    
    # Progress tracking
    progress_percentage = Column(Integer, default=0)  # 0-100
    progress_notes = Column(Text)
    last_progress_update = Column(DateTime)
    
    # Alignment and dependencies
    parent_goal_id = Column(UUID(as_uuid=True), ForeignKey("goal.id"))
    strategic_alignment = Column(String)  # high, medium, low
    business_value = Column(String)  # high, medium, low
    risk_level = Column(String, default="medium")  # low, medium, high, critical
    
    # Assessment and evaluation
    assessment_status = Column(String, default="pending")  # pending, in_progress, completed, failed
    assessment_score = Column(Integer)  # 0-100
    assessment_notes = Column(Text)
    last_assessment_date = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("GoalLink", back_populates="goal")
    child_goals = relationship("Goal", backref="parent_goal", remote_side=[id])

class GoalLink(Base):
    __tablename__ = "goal_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    goal_id = Column(UUID(as_uuid=True), ForeignKey("goal.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # requirement, capability, course_of_action, stakeholder, assessment, etc.
    link_type = Column(String, nullable=False)  # realizes, supports, enables, governs, influences
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    contribution_level = Column(String, default="medium")  # high, medium, low
    
    # Traceability
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    goal = relationship("Goal", back_populates="links") 