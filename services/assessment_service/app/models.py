from sqlalchemy import Column, String, DateTime, Float, Integer, Text, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime
from .database import Base
import enum

class AssessmentType(str, enum.Enum):
    """Assessment types in ArchiMate 3.2"""
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    STRATEGIC = "strategic"
    RISK = "risk"
    MATURITY = "maturity"
    CAPABILITY = "capability"
    GOAL = "goal"
    OUTCOME = "outcome"

class AssessmentStatus(str, enum.Enum):
    """Assessment status values"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"
    DRAFT = "draft"
    REVIEW = "review"

class AssessmentMethod(str, enum.Enum):
    """Assessment methods"""
    QUANTITATIVE = "quantitative"
    QUALITATIVE = "qualitative"
    MIXED = "mixed"
    SURVEY = "survey"
    INTERVIEW = "interview"
    OBSERVATION = "observation"
    DOCUMENT_REVIEW = "document_review"
    METRICS_ANALYSIS = "metrics_analysis"

class ConfidenceLevel(str, enum.Enum):
    """Confidence levels for assessment results"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class LinkType(str, enum.Enum):
    """Assessment link types to other ArchiMate elements"""
    EVALUATES = "evaluates"
    MEASURES = "measures"
    VALIDATES = "validates"
    SUPPORTS = "supports"
    INFLUENCES = "influences"
    CONSTRAINS = "constrains"
    ENABLES = "enables"
    IMPACTS = "impacts"

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

class Assessment(Base):
    """ArchiMate 3.2 Assessment element - evaluations of goals, outcomes, and performance measures"""
    __tablename__ = "assessments"

    # Primary key and tenant isolation
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)

    # Core Assessment attributes
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    assessment_type = Column(Enum(AssessmentType), nullable=False, index=True)
    
    # Evaluation target
    evaluated_goal_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    evaluated_capability_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    evaluated_business_function_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    evaluated_stakeholder_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    evaluated_constraint_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    # Assessment details
    evaluator_user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    assessment_method = Column(Enum(AssessmentMethod), nullable=False, index=True)
    result_summary = Column(Text)
    metrics_scored = Column(Text)  # JSON object of scored metrics
    confidence_level = Column(Enum(ConfidenceLevel), nullable=False, default=ConfidenceLevel.MEDIUM, index=True)
    confidence_score = Column(Float, default=0.5, ge=0.0, le=1.0)  # 0.0 to 1.0
    
    # Timeline
    date_conducted = Column(DateTime, nullable=True, index=True)
    planned_start_date = Column(DateTime, nullable=True, index=True)
    planned_end_date = Column(DateTime, nullable=True, index=True)
    actual_start_date = Column(DateTime, nullable=True)
    actual_end_date = Column(DateTime, nullable=True)
    
    # Status and progress
    status = Column(Enum(AssessmentStatus), nullable=False, default=AssessmentStatus.PLANNED, index=True)
    progress_percent = Column(Float, default=0.0, ge=0.0, le=100.0)
    
    # Assessment framework
    assessment_framework = Column(String(100))  # e.g., "TOGAF", "COBIT", "ISO27001"
    assessment_criteria = Column(Text)  # JSON array of assessment criteria
    assessment_questions = Column(Text)  # JSON array of assessment questions
    assessment_responses = Column(Text)  # JSON object of responses
    
    # Results and findings
    key_findings = Column(Text)  # JSON array of key findings
    recommendations = Column(Text)  # JSON array of recommendations
    risk_implications = Column(Text)  # JSON object of risk implications
    improvement_opportunities = Column(Text)  # JSON array of improvement opportunities
    
    # Quality and validation
    quality_score = Column(Float, default=0.0, ge=0.0, le=1.0)
    validation_status = Column(String(50), default="pending")
    validated_by = Column(UUID(as_uuid=True), nullable=True)
    validation_date = Column(DateTime, nullable=True)
    
    # Stakeholders and participants
    stakeholders = Column(Text)  # JSON array of stakeholder IDs
    participants = Column(Text)  # JSON array of participant IDs
    reviewers = Column(Text)  # JSON array of reviewer IDs
    
    # Compliance and standards
    compliance_standards = Column(Text)  # JSON array of compliance standards
    regulatory_requirements = Column(Text)  # JSON array of regulatory requirements
    audit_trail = Column(Text)  # JSON array of audit events
    
    # Reporting and communication
    report_template = Column(String(100))
    report_generated = Column(Boolean, default=False)
    report_url = Column(String(500))
    communication_plan = Column(Text)  # JSON object of communication plan
    
    # Metadata
    tags = Column(Text)  # JSON array of tags
    priority = Column(Integer, default=3)  # 1=Critical, 2=High, 3=Medium, 4=Low
    complexity = Column(String(20), default="medium")  # simple, medium, complex
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    assessment_links = relationship("AssessmentLink", back_populates="assessment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Assessment(id={self.id}, name='{self.name}', type='{self.assessment_type}', status='{self.status}')>"

class AssessmentLink(Base):
    """Links between Assessments and other ArchiMate elements"""
    __tablename__ = "assessment_links"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=False, index=True)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Link metadata
    linked_element_type = Column(String(100), nullable=False, index=True)  # goal, capability, constraint, etc.
    link_type = Column(Enum(LinkType), nullable=False, index=True)
    relationship_strength = Column(Enum(RelationshipStrength), default=RelationshipStrength.MEDIUM)
    dependency_level = Column(Enum(DependencyLevel), default=DependencyLevel.MEDIUM)
    
    # Assessment impact
    impact_level = Column(String(20), default="medium")  # low, medium, high, critical
    impact_description = Column(Text)
    impact_metrics = Column(Text)  # JSON object of impact measurements
    
    # Evidence and validation
    evidence_provided = Column(Text)  # JSON array of evidence items
    evidence_quality = Column(Float, default=0.0, ge=0.0, le=1.0)  # 0.0 to 1.0
    validation_status = Column(String(50), default="pending")
    validated_by = Column(UUID(as_uuid=True), nullable=True)
    validation_date = Column(DateTime, nullable=True)
    
    # Assessment contribution
    contribution_score = Column(Float, default=0.0, ge=0.0, le=1.0)  # 0.0 to 1.0
    contribution_description = Column(Text)
    contribution_metrics = Column(Text)  # JSON object of contribution measurements
    
    # Metadata
    created_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    assessment = relationship("Assessment", back_populates="assessment_links")

    def __repr__(self):
        return f"<AssessmentLink(id={self.id}, assessment_id={self.assessment_id}, linked_element_type='{self.linked_element_type}', link_type='{self.link_type}')>" 