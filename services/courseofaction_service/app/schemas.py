from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum

class StrategyType(str, Enum):
    TRANSFORMATIONAL = "transformational"
    INCREMENTAL = "incremental"
    DEFENSIVE = "defensive"
    INNOVATIVE = "innovative"

class TimeHorizon(str, Enum):
    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"

class ImplementationPhase(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ApprovalStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"

class GovernanceModel(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    ENHANCED = "enhanced"
    CRITICAL = "critical"

class LinkType(str, Enum):
    REALIZES = "realizes"
    SUPPORTS = "supports"
    ENABLES = "enables"
    INFLUENCES = "influences"
    CONSTRAINS = "constrains"
    TRIGGERS = "triggers"
    REQUIRES = "requires"

class RelationshipStrength(str, Enum):
    STRONG = "strong"
    MEDIUM = "medium"
    WEAK = "weak"

class DependencyLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class StrategicImportance(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BusinessValue(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ImplementationPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

class ImpactLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ImpactDirection(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class ConstraintLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Base schemas
class CourseOfActionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    strategy_type: StrategyType = StrategyType.TRANSFORMATIONAL
    origin_goal_id: Optional[UUID] = None
    influenced_by_driver_id: Optional[UUID] = None
    impacted_capability_id: Optional[UUID] = None
    strategic_objective: Optional[str] = None
    business_case: Optional[str] = None
    success_criteria: Optional[str] = None
    key_performance_indicators: Optional[str] = None
    time_horizon: TimeHorizon = TimeHorizon.MEDIUM_TERM
    start_date: Optional[datetime] = None
    target_completion_date: Optional[datetime] = None
    actual_completion_date: Optional[datetime] = None
    implementation_phase: ImplementationPhase = ImplementationPhase.PLANNING
    success_probability: float = Field(0.5, ge=0.0, le=1.0)
    risk_level: RiskLevel = RiskLevel.MEDIUM
    risk_assessment: Optional[str] = None
    contingency_plans: Optional[str] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    budget_allocation: Optional[float] = None
    resource_requirements: Optional[str] = None
    cost_benefit_analysis: Optional[str] = None
    stakeholders: Optional[str] = None
    governance_model: GovernanceModel = GovernanceModel.STANDARD
    approval_status: ApprovalStatus = ApprovalStatus.DRAFT
    approval_date: Optional[datetime] = None
    approved_by: Optional[UUID] = None
    implementation_approach: Optional[str] = None
    milestones: Optional[str] = None
    dependencies: Optional[str] = None
    constraints: Optional[str] = None
    current_progress: float = Field(0.0, ge=0.0, le=100.0)
    performance_metrics: Optional[str] = None
    outcomes_achieved: Optional[str] = None
    lessons_learned: Optional[str] = None
    strategic_alignment_score: float = Field(0.0, ge=0.0, le=1.0)
    capability_impact_score: float = Field(0.0, ge=0.0, le=1.0)
    goal_achievement_score: float = Field(0.0, ge=0.0, le=1.0)
    overall_effectiveness_score: float = Field(0.0, ge=0.0, le=1.0)
    compliance_requirements: Optional[str] = None
    audit_trail: Optional[str] = None
    regulatory_impact: Optional[str] = None
    technology_requirements: Optional[str] = None
    system_impact: Optional[str] = None
    integration_requirements: Optional[str] = None
    change_management_plan: Optional[str] = None
    communication_plan: Optional[str] = None
    training_requirements: Optional[str] = None

    @validator('success_probability')
    def validate_success_probability(cls, v):
        if v < 0 or v > 1:
            raise ValueError('Success probability must be between 0 and 1')
        return v

    @validator('current_progress')
    def validate_current_progress(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Current progress must be between 0 and 100')
        return v

    @validator('strategic_alignment_score', 'capability_impact_score', 'goal_achievement_score', 'overall_effectiveness_score')
    def validate_scores(cls, v):
        if v < 0 or v > 1:
            raise ValueError('Scores must be between 0 and 1')
        return v

class CourseOfActionCreate(CourseOfActionBase):
    pass

class CourseOfActionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    strategy_type: Optional[StrategyType] = None
    origin_goal_id: Optional[UUID] = None
    influenced_by_driver_id: Optional[UUID] = None
    impacted_capability_id: Optional[UUID] = None
    strategic_objective: Optional[str] = None
    business_case: Optional[str] = None
    success_criteria: Optional[str] = None
    key_performance_indicators: Optional[str] = None
    time_horizon: Optional[TimeHorizon] = None
    start_date: Optional[datetime] = None
    target_completion_date: Optional[datetime] = None
    actual_completion_date: Optional[datetime] = None
    implementation_phase: Optional[ImplementationPhase] = None
    success_probability: Optional[float] = Field(None, ge=0.0, le=1.0)
    risk_level: Optional[RiskLevel] = None
    risk_assessment: Optional[str] = None
    contingency_plans: Optional[str] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    budget_allocation: Optional[float] = None
    resource_requirements: Optional[str] = None
    cost_benefit_analysis: Optional[str] = None
    stakeholders: Optional[str] = None
    governance_model: Optional[GovernanceModel] = None
    approval_status: Optional[ApprovalStatus] = None
    approval_date: Optional[datetime] = None
    approved_by: Optional[UUID] = None
    implementation_approach: Optional[str] = None
    milestones: Optional[str] = None
    dependencies: Optional[str] = None
    constraints: Optional[str] = None
    current_progress: Optional[float] = Field(None, ge=0.0, le=100.0)
    performance_metrics: Optional[str] = None
    outcomes_achieved: Optional[str] = None
    lessons_learned: Optional[str] = None
    strategic_alignment_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    capability_impact_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    goal_achievement_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    overall_effectiveness_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    compliance_requirements: Optional[str] = None
    audit_trail: Optional[str] = None
    regulatory_impact: Optional[str] = None
    technology_requirements: Optional[str] = None
    system_impact: Optional[str] = None
    integration_requirements: Optional[str] = None
    change_management_plan: Optional[str] = None
    communication_plan: Optional[str] = None
    training_requirements: Optional[str] = None

class CourseOfAction(CourseOfActionBase):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Action Link schemas
class ActionLinkBase(BaseModel):
    linked_element_id: UUID
    linked_element_type: str = Field(..., min_length=1, max_length=100)
    link_type: LinkType
    relationship_strength: RelationshipStrength = RelationshipStrength.MEDIUM
    dependency_level: DependencyLevel = DependencyLevel.MEDIUM
    strategic_importance: StrategicImportance = StrategicImportance.MEDIUM
    business_value: BusinessValue = BusinessValue.MEDIUM
    alignment_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    implementation_priority: ImplementationPriority = ImplementationPriority.NORMAL
    implementation_phase: ImplementationPhase = ImplementationPhase.PLANNING
    resource_allocation: Optional[float] = Field(None, ge=0.0, le=100.0)
    impact_level: ImpactLevel = ImpactLevel.MEDIUM
    impact_direction: ImpactDirection = ImpactDirection.POSITIVE
    impact_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    risk_level: RiskLevel = RiskLevel.MEDIUM
    constraint_level: ConstraintLevel = ConstraintLevel.MEDIUM
    risk_mitigation: Optional[str] = None
    performance_contribution: Optional[float] = Field(None, ge=0.0, le=100.0)
    success_contribution: Optional[float] = Field(None, ge=0.0, le=100.0)
    outcome_measurement: Optional[str] = None

    @validator('alignment_score', 'impact_confidence')
    def validate_scores(cls, v):
        if v is not None and (v < 0 or v > 1):
            raise ValueError('Scores must be between 0 and 1')
        return v

    @validator('resource_allocation', 'performance_contribution', 'success_contribution')
    def validate_percentages(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Percentages must be between 0 and 100')
        return v

class ActionLinkCreate(ActionLinkBase):
    pass

class ActionLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=100)
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    strategic_importance: Optional[StrategicImportance] = None
    business_value: Optional[BusinessValue] = None
    alignment_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    implementation_priority: Optional[ImplementationPriority] = None
    implementation_phase: Optional[ImplementationPhase] = None
    resource_allocation: Optional[float] = Field(None, ge=0.0, le=100.0)
    impact_level: Optional[ImpactLevel] = None
    impact_direction: Optional[ImpactDirection] = None
    impact_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    risk_level: Optional[RiskLevel] = None
    constraint_level: Optional[ConstraintLevel] = None
    risk_mitigation: Optional[str] = None
    performance_contribution: Optional[float] = Field(None, ge=0.0, le=100.0)
    success_contribution: Optional[float] = Field(None, ge=0.0, le=100.0)
    outcome_measurement: Optional[str] = None

class ActionLink(ActionLinkBase):
    id: UUID
    course_of_action_id: UUID
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Analysis and alignment schemas
class AlignmentMap(BaseModel):
    course_of_action_id: UUID
    strategic_alignment: Dict[str, Any]
    capability_alignment: Dict[str, Any]
    goal_alignment: Dict[str, Any]
    stakeholder_alignment: Dict[str, Any]
    overall_alignment_score: float
    alignment_factors: List[Dict[str, Any]]
    recommendations: List[str]

class RiskProfile(BaseModel):
    course_of_action_id: UUID
    overall_risk_score: float
    risk_breakdown: Dict[str, Any]
    risk_factors: List[Dict[str, Any]]
    mitigation_strategies: List[Dict[str, Any]]
    contingency_plans: List[Dict[str, Any]]
    risk_monitoring: Dict[str, Any]
    recommendations: List[str]

class CourseOfActionAnalysis(BaseModel):
    course_of_action_id: UUID
    strategic_analysis: Dict[str, Any]
    performance_analysis: Dict[str, Any]
    risk_analysis: Dict[str, Any]
    cost_analysis: Dict[str, Any]
    implementation_analysis: Dict[str, Any]
    outcome_analysis: Dict[str, Any]
    recommendations: List[str]

# Domain-specific schemas
class CourseOfActionByStrategyType(BaseModel):
    strategy_type: StrategyType
    count: int
    courses_of_action: List[CourseOfAction]

class CourseOfActionByCapability(BaseModel):
    capability_id: UUID
    capability_name: str
    count: int
    courses_of_action: List[CourseOfAction]

class CourseOfActionByRiskLevel(BaseModel):
    risk_level: RiskLevel
    count: int
    courses_of_action: List[CourseOfAction]

class CourseOfActionByTimeHorizon(BaseModel):
    time_horizon: TimeHorizon
    count: int
    courses_of_action: List[CourseOfAction]

# Response schemas for specific queries
class CourseOfActionByElement(BaseModel):
    element_type: str
    element_id: UUID
    element_name: str
    courses_of_action: List[CourseOfAction]

class CourseOfActionSummary(BaseModel):
    total_courses_of_action: int
    active_courses_of_action: int
    high_risk_courses_of_action: int
    courses_of_action_by_strategy: Dict[str, int]
    courses_of_action_by_phase: Dict[str, int]
    average_success_probability: float
    total_estimated_cost: float
    average_progress: float 