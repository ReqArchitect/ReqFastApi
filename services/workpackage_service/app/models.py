from sqlalchemy import Column, String, DateTime, Float, Integer, Text, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime
from .database import Base
import enum

class PackageType(str, enum.Enum):
    """Work package types in ArchiMate 3.2"""
    PROJECT = "project"
    EPIC = "epic"
    TASK = "task"
    RELEASE = "release"
    PHASE = "phase"
    SPRINT = "sprint"
    INITIATIVE = "initiative"
    MILESTONE = "milestone"

class PackageStatus(str, enum.Enum):
    """Work package status values"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DELAYED = "delayed"
    BLOCKED = "blocked"

class DeliveryRisk(str, enum.Enum):
    """Delivery risk levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class LinkType(str, enum.Enum):
    """Package link types to other ArchiMate elements"""
    REALIZES = "realizes"
    CLOSES = "closes"
    DELIVERS = "delivers"
    SUPPORTS = "supports"
    ENABLES = "enables"
    IMPACTS = "impacts"
    DEPENDS_ON = "depends_on"
    CONTRIBUTES_TO = "contributes_to"

class RelationshipStrength(str, enum.Enum):
    """Relationship strength levels"""
    STRONG = "strong"
    MEDIUM = "medium"
    WEAK = "weak"

class DependencyLevel(str, enum.Enum):
    """Dependency level classifications"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class WorkPackage(Base):
    """ArchiMate 3.2 Work Package element - units of work that realize transformation efforts"""
    __tablename__ = "work_packages"

    # Primary key and tenant isolation
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)

    # Core Work Package attributes
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    package_type = Column(Enum(PackageType), nullable=False, index=True)
    
    # Strategic alignment
    strategic_driver_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    related_goal_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    target_plateau_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    # Scope and impact
    impacted_capabilities = Column(Text)  # JSON array of capability IDs
    impacted_application_components = Column(Text)  # JSON array of component IDs
    impacted_technology_nodes = Column(Text)  # JSON array of node IDs
    
    # Scheduling and timeline
    scheduled_start = Column(DateTime, nullable=True, index=True)
    scheduled_end = Column(DateTime, nullable=True, index=True)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)
    
    # Status and progress
    current_status = Column(Enum(PackageStatus), nullable=False, default=PackageStatus.PLANNED, index=True)
    progress_percent = Column(Float, default=0.0)
    
    # Risk and quality
    delivery_risk = Column(Enum(DeliveryRisk), nullable=False, default=DeliveryRisk.MEDIUM, index=True)
    quality_gates = Column(Text)  # JSON array of quality gate definitions
    risk_mitigation_plan = Column(Text)
    
    # Resource allocation
    estimated_effort_hours = Column(Float, nullable=True)
    actual_effort_hours = Column(Float, default=0.0)
    budget_allocation = Column(Float, nullable=True)
    actual_cost = Column(Float, default=0.0)
    
    # Team and ownership
    change_owner_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    team_members = Column(Text)  # JSON array of team member IDs
    stakeholders = Column(Text)  # JSON array of stakeholder IDs
    
    # Dependencies and relationships
    dependencies = Column(Text)  # JSON array of dependent work package IDs
    blockers = Column(Text)  # JSON array of blocking work package IDs
    
    # Quality and compliance
    quality_metrics = Column(Text)  # JSON object of quality metrics
    compliance_requirements = Column(Text)  # JSON array of compliance requirements
    audit_trail = Column(Text)  # JSON array of audit events
    
    # Monitoring and reporting
    kpis = Column(Text)  # JSON object of key performance indicators
    reporting_frequency = Column(String(50), default="weekly")
    escalation_path = Column(Text)  # JSON object of escalation contacts
    
    # Metadata
    tags = Column(Text)  # JSON array of tags
    priority = Column(Integer, default=3)  # 1=Critical, 2=High, 3=Medium, 4=Low
    complexity = Column(String(20), default="medium")  # simple, medium, complex
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    package_links = relationship("PackageLink", back_populates="work_package", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<WorkPackage(id={self.id}, name='{self.name}', type='{self.package_type}', status='{self.current_status}')>"

class PackageLink(Base):
    """Links between Work Packages and other ArchiMate elements"""
    __tablename__ = "package_links"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    work_package_id = Column(UUID(as_uuid=True), ForeignKey("work_packages.id"), nullable=False, index=True)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Link metadata
    linked_element_type = Column(String(100), nullable=False, index=True)  # requirement, goal, gap, capability, etc.
    link_type = Column(Enum(LinkType), nullable=False, index=True)
    relationship_strength = Column(Enum(RelationshipStrength), default=RelationshipStrength.MEDIUM)
    dependency_level = Column(Enum(DependencyLevel), default=DependencyLevel.MEDIUM)
    
    # Impact assessment
    impact_level = Column(String(20), default="medium")  # low, medium, high, critical
    impact_description = Column(Text)
    impact_metrics = Column(Text)  # JSON object of impact measurements
    
    # Traceability
    traceability_score = Column(Float, default=0.0)  # 0.0 to 1.0
    traceability_evidence = Column(Text)  # JSON array of evidence items
    
    # Validation
    is_validated = Column(Boolean, default=False)
    validation_date = Column(DateTime, nullable=True)
    validated_by = Column(UUID(as_uuid=True), nullable=True)
    
    # Metadata
    created_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    work_package = relationship("WorkPackage", back_populates="package_links")

    def __repr__(self):
        return f"<PackageLink(id={self.id}, work_package_id={self.work_package_id}, linked_element_type='{self.linked_element_type}', link_type='{self.link_type}')>" 