from pydantic import BaseModel, UUID4, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class GoalType(str, Enum):
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    TECHNICAL = "technical"
    TACTICAL = "tactical"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class GoalStatus(str, Enum):
    ACTIVE = "active"
    ACHIEVED = "achieved"
    ABANDONED = "abandoned"
    ON_HOLD = "on_hold"

class MeasurementFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"

class ReviewFrequency(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"
    AD_HOC = "ad_hoc"

class StrategicAlignment(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class BusinessValue(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AssessmentStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class LinkType(str, Enum):
    REALIZES = "realizes"
    SUPPORTS = "supports"
    ENABLES = "enables"
    GOVERNS = "governs"
    INFLUENCES = "influences"

class RelationshipStrength(str, Enum):
    STRONG = "strong"
    MEDIUM = "medium"
    WEAK = "weak"

class ContributionLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Base schemas
class GoalBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    goal_type: GoalType
    priority: Priority = Priority.MEDIUM
    status: GoalStatus = GoalStatus.ACTIVE
    origin_driver_id: Optional[UUID4] = None
    stakeholder_id: Optional[UUID4] = None
    business_actor_id: Optional[UUID4] = None
    success_criteria: Optional[str] = None
    key_performance_indicators: Optional[str] = None
    measurement_frequency: Optional[MeasurementFrequency] = None
    target_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    review_frequency: Optional[ReviewFrequency] = None
    progress_percentage: Optional[int] = Field(None, ge=0, le=100)
    progress_notes: Optional[str] = None
    parent_goal_id: Optional[UUID4] = None
    strategic_alignment: Optional[StrategicAlignment] = None
    business_value: Optional[BusinessValue] = None
    risk_level: RiskLevel = RiskLevel.MEDIUM
    assessment_status: AssessmentStatus = AssessmentStatus.PENDING
    assessment_score: Optional[int] = Field(None, ge=0, le=100)
    assessment_notes: Optional[str] = None

    @validator('target_date', 'start_date', 'completion_date')
    def validate_dates(cls, v):
        if v and v < datetime.utcnow():
            raise ValueError('Dates must be in the future')
        return v

    @validator('progress_percentage', 'assessment_score')
    def validate_percentage(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Percentage must be between 0 and 100')
        return v

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    goal_type: Optional[GoalType] = None
    priority: Optional[Priority] = None
    status: Optional[GoalStatus] = None
    origin_driver_id: Optional[UUID4] = None
    stakeholder_id: Optional[UUID4] = None
    business_actor_id: Optional[UUID4] = None
    success_criteria: Optional[str] = None
    key_performance_indicators: Optional[str] = None
    measurement_frequency: Optional[MeasurementFrequency] = None
    target_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    review_frequency: Optional[ReviewFrequency] = None
    progress_percentage: Optional[int] = Field(None, ge=0, le=100)
    progress_notes: Optional[str] = None
    parent_goal_id: Optional[UUID4] = None
    strategic_alignment: Optional[StrategicAlignment] = None
    business_value: Optional[BusinessValue] = None
    risk_level: Optional[RiskLevel] = None
    assessment_status: Optional[AssessmentStatus] = None
    assessment_score: Optional[int] = Field(None, ge=0, le=100)
    assessment_notes: Optional[str] = None

class GoalInDBBase(GoalBase):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    last_progress_update: Optional[datetime] = None
    last_assessment_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Goal(GoalInDBBase):
    pass

# Link schemas
class GoalLinkBase(BaseModel):
    linked_element_id: UUID4
    linked_element_type: str = Field(..., min_length=1, max_length=100)
    link_type: LinkType
    relationship_strength: RelationshipStrength = RelationshipStrength.MEDIUM
    contribution_level: ContributionLevel = ContributionLevel.MEDIUM

class GoalLinkCreate(GoalLinkBase):
    pass

class GoalLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID4] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=100)
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    contribution_level: Optional[ContributionLevel] = None

class GoalLinkInDBBase(GoalLinkBase):
    id: UUID4
    goal_id: UUID4
    created_by: UUID4
    created_at: datetime

    class Config:
        orm_mode = True

class GoalLink(GoalLinkInDBBase):
    pass

# Response schemas
class GoalWithLinks(Goal):
    links: List[GoalLink] = []

class GoalList(BaseModel):
    goals: List[Goal]
    total: int
    skip: int
    limit: int

class RealizationMap(BaseModel):
    goal_id: UUID4
    linked_elements_count: int
    requirements_count: int
    capabilities_count: int
    courses_of_action_count: int
    stakeholders_count: int
    assessments_count: int
    overall_realization_score: float
    last_assessed: datetime

class GoalStatusSummary(BaseModel):
    goal_id: UUID4
    status: GoalStatus
    progress_percentage: int
    days_until_target: Optional[int]
    assessment_score: Optional[int]
    risk_level: RiskLevel
    strategic_alignment: Optional[StrategicAlignment]
    business_value: Optional[BusinessValue]
    linked_elements_count: int
    last_updated: datetime

class GoalAnalysis(BaseModel):
    goal_id: UUID4
    priority_score: float
    progress_score: float
    risk_score: float
    strategic_alignment_score: float
    business_value_score: float
    overall_health_score: float
    last_analyzed: datetime 