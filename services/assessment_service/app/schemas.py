from pydantic import BaseModel, Field, validator, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import json

# Enums matching the SQLAlchemy models
class AssessmentType(str, Enum):
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    STRATEGIC = "strategic"
    RISK = "risk"
    MATURITY = "maturity"
    CAPABILITY = "capability"
    GOAL = "goal"
    OUTCOME = "outcome"

class AssessmentStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"
    DRAFT = "draft"
    REVIEW = "review"

class AssessmentMethod(str, Enum):
    QUANTITATIVE = "quantitative"
    QUALITATIVE = "qualitative"
    MIXED = "mixed"
    SURVEY = "survey"
    INTERVIEW = "interview"
    OBSERVATION = "observation"
    DOCUMENT_REVIEW = "document_review"
    METRICS_ANALYSIS = "metrics_analysis"

class ConfidenceLevel(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class LinkType(str, Enum):
    EVALUATES = "evaluates"
    MEASURES = "measures"
    VALIDATES = "validates"
    SUPPORTS = "supports"
    INFLUENCES = "influences"
    CONSTRAINS = "constrains"
    ENABLES = "enables"
    IMPACTS = "impacts"

class RelationshipStrength(str, Enum):
    STRONG = "strong"
    MEDIUM = "medium"
    WEAK = "weak"

class DependencyLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Base schemas
class AssessmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Assessment name")
    description: Optional[str] = Field(None, description="Assessment description")
    assessment_type: AssessmentType = Field(..., description="Type of assessment")
    
    # Evaluation target
    evaluated_goal_id: Optional[UUID4] = Field(None, description="Evaluated goal ID")
    evaluated_capability_id: Optional[UUID4] = Field(None, description="Evaluated capability ID")
    evaluated_business_function_id: Optional[UUID4] = Field(None, description="Evaluated business function ID")
    evaluated_stakeholder_id: Optional[UUID4] = Field(None, description="Evaluated stakeholder ID")
    evaluated_constraint_id: Optional[UUID4] = Field(None, description="Evaluated constraint ID")
    
    # Assessment details
    evaluator_user_id: UUID4 = Field(..., description="Evaluator user ID")
    assessment_method: AssessmentMethod = Field(..., description="Assessment method")
    result_summary: Optional[str] = Field(None, description="Result summary")
    metrics_scored: Optional[str] = Field(None, description="JSON object of scored metrics")
    confidence_level: ConfidenceLevel = Field(ConfidenceLevel.MEDIUM, description="Confidence level")
    confidence_score: float = Field(0.5, ge=0.0, le=1.0, description="Confidence score (0.0 to 1.0)")
    
    # Timeline
    date_conducted: Optional[datetime] = Field(None, description="Date assessment was conducted")
    planned_start_date: Optional[datetime] = Field(None, description="Planned start date")
    planned_end_date: Optional[datetime] = Field(None, description="Planned end date")
    actual_start_date: Optional[datetime] = Field(None, description="Actual start date")
    actual_end_date: Optional[datetime] = Field(None, description="Actual end date")
    
    # Status and progress
    status: AssessmentStatus = Field(AssessmentStatus.PLANNED, description="Assessment status")
    progress_percent: float = Field(0.0, ge=0.0, le=100.0, description="Progress percentage")
    
    # Assessment framework
    assessment_framework: Optional[str] = Field(None, max_length=100, description="Assessment framework")
    assessment_criteria: Optional[str] = Field(None, description="JSON array of assessment criteria")
    assessment_questions: Optional[str] = Field(None, description="JSON array of assessment questions")
    assessment_responses: Optional[str] = Field(None, description="JSON object of responses")
    
    # Results and findings
    key_findings: Optional[str] = Field(None, description="JSON array of key findings")
    recommendations: Optional[str] = Field(None, description="JSON array of recommendations")
    risk_implications: Optional[str] = Field(None, description="JSON object of risk implications")
    improvement_opportunities: Optional[str] = Field(None, description="JSON array of improvement opportunities")
    
    # Quality and validation
    quality_score: float = Field(0.0, ge=0.0, le=1.0, description="Quality score (0.0 to 1.0)")
    validation_status: str = Field("pending", max_length=50, description="Validation status")
    validated_by: Optional[UUID4] = Field(None, description="Validated by user ID")
    validation_date: Optional[datetime] = Field(None, description="Validation date")
    
    # Stakeholders and participants
    stakeholders: Optional[str] = Field(None, description="JSON array of stakeholder IDs")
    participants: Optional[str] = Field(None, description="JSON array of participant IDs")
    reviewers: Optional[str] = Field(None, description="JSON array of reviewer IDs")
    
    # Compliance and standards
    compliance_standards: Optional[str] = Field(None, description="JSON array of compliance standards")
    regulatory_requirements: Optional[str] = Field(None, description="JSON array of regulatory requirements")
    audit_trail: Optional[str] = Field(None, description="JSON array of audit events")
    
    # Reporting and communication
    report_template: Optional[str] = Field(None, max_length=100, description="Report template")
    report_generated: bool = Field(False, description="Report generated flag")
    report_url: Optional[str] = Field(None, max_length=500, description="Report URL")
    communication_plan: Optional[str] = Field(None, description="JSON object of communication plan")
    
    # Metadata
    tags: Optional[str] = Field(None, description="JSON array of tags")
    priority: int = Field(3, ge=1, le=4, description="Priority (1=Critical, 2=High, 3=Medium, 4=Low)")
    complexity: str = Field("medium", description="Complexity level")

    @validator('metrics_scored', 'assessment_criteria', 'assessment_questions', 'assessment_responses',
               'key_findings', 'recommendations', 'risk_implications', 'improvement_opportunities',
               'stakeholders', 'participants', 'reviewers', 'compliance_standards', 
               'regulatory_requirements', 'audit_trail', 'communication_plan', 'tags')
    def validate_json(cls, v):
        if v is not None:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Must be valid JSON")
        return v

    @validator('confidence_score', 'quality_score')
    def validate_score_range(cls, v):
        if v < 0.0 or v > 1.0:
            raise ValueError("Score must be between 0.0 and 1.0")
        return v

    @validator('progress_percent')
    def validate_progress_percent(cls, v):
        if v < 0.0 or v > 100.0:
            raise ValueError("Progress percentage must be between 0.0 and 100.0")
        return v

    @validator('planned_end_date')
    def validate_planned_end_date(cls, v, values):
        if v and 'planned_start_date' in values and values['planned_start_date']:
            if v <= values['planned_start_date']:
                raise ValueError("Planned end date must be after planned start date")
        return v

    @validator('actual_end_date')
    def validate_actual_end_date(cls, v, values):
        if v and 'actual_start_date' in values and values['actual_start_date']:
            if v <= values['actual_start_date']:
                raise ValueError("Actual end date must be after actual start date")
        return v

class AssessmentCreate(AssessmentBase):
    pass

class AssessmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    assessment_type: Optional[AssessmentType] = None
    evaluated_goal_id: Optional[UUID4] = None
    evaluated_capability_id: Optional[UUID4] = None
    evaluated_business_function_id: Optional[UUID4] = None
    evaluated_stakeholder_id: Optional[UUID4] = None
    evaluated_constraint_id: Optional[UUID4] = None
    evaluator_user_id: Optional[UUID4] = None
    assessment_method: Optional[AssessmentMethod] = None
    result_summary: Optional[str] = None
    metrics_scored: Optional[str] = None
    confidence_level: Optional[ConfidenceLevel] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    date_conducted: Optional[datetime] = None
    planned_start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    status: Optional[AssessmentStatus] = None
    progress_percent: Optional[float] = Field(None, ge=0.0, le=100.0)
    assessment_framework: Optional[str] = Field(None, max_length=100)
    assessment_criteria: Optional[str] = None
    assessment_questions: Optional[str] = None
    assessment_responses: Optional[str] = None
    key_findings: Optional[str] = None
    recommendations: Optional[str] = None
    risk_implications: Optional[str] = None
    improvement_opportunities: Optional[str] = None
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    validation_status: Optional[str] = Field(None, max_length=50)
    validated_by: Optional[UUID4] = None
    validation_date: Optional[datetime] = None
    stakeholders: Optional[str] = None
    participants: Optional[str] = None
    reviewers: Optional[str] = None
    compliance_standards: Optional[str] = None
    regulatory_requirements: Optional[str] = None
    audit_trail: Optional[str] = None
    report_template: Optional[str] = Field(None, max_length=100)
    report_generated: Optional[bool] = None
    report_url: Optional[str] = Field(None, max_length=500)
    communication_plan: Optional[str] = None
    tags: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=4)
    complexity: Optional[str] = None

    @validator('metrics_scored', 'assessment_criteria', 'assessment_questions', 'assessment_responses',
               'key_findings', 'recommendations', 'risk_implications', 'improvement_opportunities',
               'stakeholders', 'participants', 'reviewers', 'compliance_standards', 
               'regulatory_requirements', 'audit_trail', 'communication_plan', 'tags')
    def validate_json(cls, v):
        if v is not None:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Must be valid JSON")
        return v

class AssessmentResponse(AssessmentBase):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AssessmentList(BaseModel):
    id: UUID4
    name: str
    assessment_type: AssessmentType
    status: AssessmentStatus
    progress_percent: float
    confidence_level: ConfidenceLevel
    confidence_score: float
    evaluator_user_id: UUID4
    date_conducted: Optional[datetime]
    quality_score: float
    created_at: datetime

    class Config:
        from_attributes = True

# Assessment Link schemas
class AssessmentLinkBase(BaseModel):
    linked_element_id: UUID4 = Field(..., description="Linked element ID")
    linked_element_type: str = Field(..., min_length=1, max_length=100, description="Type of linked element")
    link_type: LinkType = Field(..., description="Type of link")
    relationship_strength: RelationshipStrength = Field(RelationshipStrength.MEDIUM, description="Relationship strength")
    dependency_level: DependencyLevel = Field(DependencyLevel.MEDIUM, description="Dependency level")
    impact_level: str = Field("medium", description="Impact level")
    impact_description: Optional[str] = Field(None, description="Impact description")
    impact_metrics: Optional[str] = Field(None, description="JSON object of impact measurements")
    evidence_provided: Optional[str] = Field(None, description="JSON array of evidence items")
    evidence_quality: float = Field(0.0, ge=0.0, le=1.0, description="Evidence quality score")
    validation_status: str = Field("pending", description="Validation status")
    validated_by: Optional[UUID4] = Field(None, description="Validated by user ID")
    validation_date: Optional[datetime] = Field(None, description="Validation date")
    contribution_score: float = Field(0.0, ge=0.0, le=1.0, description="Contribution score")
    contribution_description: Optional[str] = Field(None, description="Contribution description")
    contribution_metrics: Optional[str] = Field(None, description="JSON object of contribution measurements")

    @validator('impact_metrics', 'evidence_provided', 'contribution_metrics')
    def validate_json(cls, v):
        if v is not None:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Must be valid JSON")
        return v

    @validator('evidence_quality', 'contribution_score')
    def validate_score_range(cls, v):
        if v < 0.0 or v > 1.0:
            raise ValueError("Score must be between 0.0 and 1.0")
        return v

class AssessmentLinkCreate(AssessmentLinkBase):
    pass

class AssessmentLinkUpdate(BaseModel):
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=100)
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    impact_level: Optional[str] = None
    impact_description: Optional[str] = None
    impact_metrics: Optional[str] = None
    evidence_provided: Optional[str] = None
    evidence_quality: Optional[float] = Field(None, ge=0.0, le=1.0)
    validation_status: Optional[str] = None
    validated_by: Optional[UUID4] = None
    validation_date: Optional[datetime] = None
    contribution_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    contribution_description: Optional[str] = None
    contribution_metrics: Optional[str] = None

    @validator('impact_metrics', 'evidence_provided', 'contribution_metrics')
    def validate_json(cls, v):
        if v is not None:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Must be valid JSON")
        return v

class AssessmentLinkResponse(AssessmentLinkBase):
    id: UUID4
    assessment_id: UUID4
    created_by: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Analysis schemas
class EvaluationMetricsResponse(BaseModel):
    assessment_id: UUID4
    overall_score: float
    metrics_breakdown: Dict[str, Any]
    performance_analysis: Dict[str, Any]
    quality_analysis: Dict[str, Any]
    confidence_analysis: Dict[str, Any]
    recommendations: List[str]

class ConfidenceScoreResponse(BaseModel):
    assessment_id: UUID4
    confidence_score: float
    confidence_level: str
    evidence_quality: float
    validation_status: str
    contributing_factors: List[Dict[str, Any]]
    recommendations: List[str]

# Enum response schemas
class EnumResponse(BaseModel):
    values: List[str]

# Health check schema
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    service: str
    version: str
    database: str
    redis: str

# Error response schema
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime 