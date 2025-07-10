from pydantic import BaseModel, UUID4, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ProcessType(str, Enum):
    OPERATIONAL = "operational"
    MANAGEMENT = "management"
    SUPPORT = "support"
    STRATEGIC = "strategic"

class ProcessClassification(str, Enum):
    OPERATIONAL = "operational"
    MANAGEMENT = "management"
    SUPPORT = "support"
    STRATEGIC = "strategic"

class Criticality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Complexity(str, Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"

class AutomationLevel(str, Enum):
    MANUAL = "manual"
    SEMI_AUTOMATED = "semi_automated"
    AUTOMATED = "automated"
    FULLY_AUTOMATED = "fully_automated"

class ProcessStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    PLANNED = "planned"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Frequency(str, Enum):
    CONTINUOUS = "continuous"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ON_DEMAND = "on_demand"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AuditFrequency(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"
    AD_HOC = "ad_hoc"

class AuditStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class StepType(str, Enum):
    TASK = "task"
    DECISION = "decision"
    HANDOFF = "handoff"
    APPROVAL = "approval"
    REVIEW = "review"

class LinkType(str, Enum):
    REALIZES = "realizes"
    SUPPORTS = "supports"
    USES = "uses"
    PRODUCES = "produces"
    CONSUMES = "consumes"
    TRIGGERS = "triggers"
    ENABLES = "enables"

class RelationshipStrength(str, Enum):
    STRONG = "strong"
    MEDIUM = "medium"
    WEAK = "weak"

class DependencyLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class InteractionFrequency(str, Enum):
    FREQUENT = "frequent"
    REGULAR = "regular"
    OCCASIONAL = "occasional"
    RARE = "rare"

class InteractionType(str, Enum):
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    BATCH = "batch"
    REAL_TIME = "real_time"

class ResponsibilityLevel(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SHARED = "shared"
    ADVISORY = "advisory"

class PerformanceImpact(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"

class FlowDirection(str, Enum):
    INPUT = "input"
    OUTPUT = "output"
    BIDIRECTIONAL = "bidirectional"

class HandoffType(str, Enum):
    STANDARD = "standard"
    AUTOMATED = "automated"
    MANUAL = "manual"
    EXCEPTION = "exception"

# Base schemas
class BusinessProcessBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    process_type: ProcessType
    input_object_type: Optional[str] = None
    output_object_type: Optional[str] = None
    organizational_unit: str = Field(..., min_length=1, max_length=255)
    goal_id: Optional[UUID4] = None
    capability_id: Optional[UUID4] = None
    actor_id: Optional[UUID4] = None
    role_id: Optional[UUID4] = None
    process_classification: ProcessClassification = ProcessClassification.OPERATIONAL
    criticality: Criticality = Criticality.MEDIUM
    complexity: Complexity = Complexity.MEDIUM
    automation_level: AutomationLevel = AutomationLevel.MANUAL
    performance_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    effectiveness_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    efficiency_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    performance_metrics: Optional[str] = None
    status: ProcessStatus = ProcessStatus.ACTIVE
    priority: Priority = Priority.MEDIUM
    frequency: Frequency = Frequency.ON_DEMAND
    duration_target: Optional[float] = Field(None, ge=0.0)
    duration_average: Optional[float] = Field(None, ge=0.0)
    volume_target: Optional[int] = Field(None, ge=0)
    volume_actual: Optional[int] = Field(None, ge=0)
    process_flow: Optional[str] = None
    decision_points: Optional[str] = None
    handoff_points: Optional[str] = None
    dependencies: Optional[str] = None
    resource_requirements: Optional[str] = None
    capacity_planning: Optional[str] = None
    skill_requirements: Optional[str] = None
    training_requirements: Optional[str] = None
    compliance_requirements: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.MEDIUM
    audit_frequency: AuditFrequency = AuditFrequency.ANNUALLY
    last_audit_date: Optional[datetime] = None
    audit_status: AuditStatus = AuditStatus.PENDING
    cost_center: Optional[str] = None
    budget_allocation: Optional[float] = Field(None, ge=0.0)
    cost_per_transaction: Optional[float] = Field(None, ge=0.0)
    roi_metrics: Optional[str] = None
    technology_stack: Optional[str] = None
    automation_tools: Optional[str] = None
    integration_points: Optional[str] = None
    data_requirements: Optional[str] = None
    quality_standards: Optional[str] = None
    kpi_metrics: Optional[str] = None
    sla_targets: Optional[str] = None
    quality_gates: Optional[str] = None
    parent_process_id: Optional[UUID4] = None
    business_function_id: Optional[UUID4] = None
    application_service_id: Optional[UUID4] = None
    data_object_id: Optional[UUID4] = None

    @validator('performance_score', 'effectiveness_score', 'efficiency_score', 'quality_score')
    def validate_scores(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Score must be between 0.0 and 1.0')
        return v

    @validator('duration_target', 'duration_average', 'budget_allocation', 'cost_per_transaction')
    def validate_positive_floats(cls, v):
        if v is not None and v < 0.0:
            raise ValueError('Value must be non-negative')
        return v

    @validator('volume_target', 'volume_actual')
    def validate_positive_ints(cls, v):
        if v is not None and v < 0:
            raise ValueError('Value must be non-negative')
        return v

class BusinessProcessCreate(BusinessProcessBase):
    pass

class BusinessProcessUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    process_type: Optional[ProcessType] = None
    input_object_type: Optional[str] = None
    output_object_type: Optional[str] = None
    organizational_unit: Optional[str] = Field(None, min_length=1, max_length=255)
    goal_id: Optional[UUID4] = None
    capability_id: Optional[UUID4] = None
    actor_id: Optional[UUID4] = None
    role_id: Optional[UUID4] = None
    process_classification: Optional[ProcessClassification] = None
    criticality: Optional[Criticality] = None
    complexity: Optional[Complexity] = None
    automation_level: Optional[AutomationLevel] = None
    performance_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    effectiveness_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    efficiency_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    performance_metrics: Optional[str] = None
    status: Optional[ProcessStatus] = None
    priority: Optional[Priority] = None
    frequency: Optional[Frequency] = None
    duration_target: Optional[float] = Field(None, ge=0.0)
    duration_average: Optional[float] = Field(None, ge=0.0)
    volume_target: Optional[int] = Field(None, ge=0)
    volume_actual: Optional[int] = Field(None, ge=0)
    process_flow: Optional[str] = None
    decision_points: Optional[str] = None
    handoff_points: Optional[str] = None
    dependencies: Optional[str] = None
    resource_requirements: Optional[str] = None
    capacity_planning: Optional[str] = None
    skill_requirements: Optional[str] = None
    training_requirements: Optional[str] = None
    compliance_requirements: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    audit_frequency: Optional[AuditFrequency] = None
    last_audit_date: Optional[datetime] = None
    audit_status: Optional[AuditStatus] = None
    cost_center: Optional[str] = None
    budget_allocation: Optional[float] = Field(None, ge=0.0)
    cost_per_transaction: Optional[float] = Field(None, ge=0.0)
    roi_metrics: Optional[str] = None
    technology_stack: Optional[str] = None
    automation_tools: Optional[str] = None
    integration_points: Optional[str] = None
    data_requirements: Optional[str] = None
    quality_standards: Optional[str] = None
    kpi_metrics: Optional[str] = None
    sla_targets: Optional[str] = None
    quality_gates: Optional[str] = None
    parent_process_id: Optional[UUID4] = None
    business_function_id: Optional[UUID4] = None
    application_service_id: Optional[UUID4] = None
    data_object_id: Optional[UUID4] = None

class BusinessProcessInDBBase(BusinessProcessBase):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class BusinessProcess(BusinessProcessInDBBase):
    pass

# Process Step schemas
class ProcessStepBase(BaseModel):
    step_order: int = Field(..., ge=1)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    step_type: StepType
    responsible_role_id: Optional[UUID4] = None
    responsible_actor_id: Optional[UUID4] = None
    duration_estimate: Optional[float] = Field(None, ge=0.0)
    duration_actual: Optional[float] = Field(None, ge=0.0)
    complexity: Complexity = Complexity.MEDIUM
    input_criteria: Optional[str] = None
    output_criteria: Optional[str] = None
    decision_logic: Optional[str] = None
    handoff_instructions: Optional[str] = None
    performance_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    efficiency_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    bottleneck_indicator: bool = False
    automation_level: AutomationLevel = AutomationLevel.MANUAL
    automation_tools: Optional[str] = None
    integration_points: Optional[str] = None
    approval_required: bool = False
    approval_role_id: Optional[UUID4] = None
    quality_gates: Optional[str] = None
    compliance_checks: Optional[str] = None

    @validator('performance_score', 'quality_score', 'efficiency_score')
    def validate_scores(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Score must be between 0.0 and 1.0')
        return v

    @validator('duration_estimate', 'duration_actual')
    def validate_duration(cls, v):
        if v is not None and v < 0.0:
            raise ValueError('Duration must be non-negative')
        return v

class ProcessStepCreate(ProcessStepBase):
    pass

class ProcessStepUpdate(BaseModel):
    step_order: Optional[int] = Field(None, ge=1)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    step_type: Optional[StepType] = None
    responsible_role_id: Optional[UUID4] = None
    responsible_actor_id: Optional[UUID4] = None
    duration_estimate: Optional[float] = Field(None, ge=0.0)
    duration_actual: Optional[float] = Field(None, ge=0.0)
    complexity: Optional[Complexity] = None
    input_criteria: Optional[str] = None
    output_criteria: Optional[str] = None
    decision_logic: Optional[str] = None
    handoff_instructions: Optional[str] = None
    performance_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    efficiency_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    bottleneck_indicator: Optional[bool] = None
    automation_level: Optional[AutomationLevel] = None
    automation_tools: Optional[str] = None
    integration_points: Optional[str] = None
    approval_required: Optional[bool] = None
    approval_role_id: Optional[UUID4] = None
    quality_gates: Optional[str] = None
    compliance_checks: Optional[str] = None

class ProcessStepInDBBase(ProcessStepBase):
    id: UUID4
    business_process_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProcessStep(ProcessStepInDBBase):
    pass

# Process Link schemas
class ProcessLinkBase(BaseModel):
    linked_element_id: UUID4
    linked_element_type: str = Field(..., min_length=1, max_length=100)
    link_type: LinkType
    relationship_strength: RelationshipStrength = RelationshipStrength.MEDIUM
    dependency_level: DependencyLevel = DependencyLevel.MEDIUM
    interaction_frequency: InteractionFrequency = InteractionFrequency.REGULAR
    interaction_type: InteractionType = InteractionType.SYNCHRONOUS
    responsibility_level: ResponsibilityLevel = ResponsibilityLevel.SHARED
    performance_impact: PerformanceImpact = PerformanceImpact.MEDIUM
    business_value_impact: PerformanceImpact = PerformanceImpact.MEDIUM
    risk_impact: PerformanceImpact = PerformanceImpact.MEDIUM
    flow_direction: FlowDirection = FlowDirection.BIDIRECTIONAL
    sequence_order: Optional[int] = Field(None, ge=1)
    handoff_type: HandoffType = HandoffType.STANDARD

class ProcessLinkCreate(ProcessLinkBase):
    pass

class ProcessLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID4] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=100)
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    interaction_frequency: Optional[InteractionFrequency] = None
    interaction_type: Optional[InteractionType] = None
    responsibility_level: Optional[ResponsibilityLevel] = None
    performance_impact: Optional[PerformanceImpact] = None
    business_value_impact: Optional[PerformanceImpact] = None
    risk_impact: Optional[PerformanceImpact] = None
    flow_direction: Optional[FlowDirection] = None
    sequence_order: Optional[int] = Field(None, ge=1)
    handoff_type: Optional[HandoffType] = None

class ProcessLinkInDBBase(ProcessLinkBase):
    id: UUID4
    business_process_id: UUID4
    created_by: UUID4
    created_at: datetime

    class Config:
        orm_mode = True

class ProcessLink(ProcessLinkInDBBase):
    pass

# Response schemas
class BusinessProcessWithSteps(BusinessProcess):
    steps: List[ProcessStep] = []

class BusinessProcessWithLinks(BusinessProcess):
    links: List[ProcessLink] = []

class BusinessProcessList(BaseModel):
    business_processes: List[BusinessProcess]
    total: int
    skip: int
    limit: int

class ProcessFlowMap(BaseModel):
    business_process_id: UUID4
    total_steps: int
    automated_steps: int
    manual_steps: int
    decision_points: int
    handoff_points: int
    bottleneck_steps: int
    average_step_duration: float
    total_process_duration: float
    flow_complexity_score: float
    last_analyzed: datetime

class ProcessRealizationHealth(BaseModel):
    business_process_id: UUID4
    performance_score: float
    effectiveness_score: float
    efficiency_score: float
    quality_score: float
    automation_score: float
    compliance_score: float
    overall_health_score: float
    last_assessed: datetime

class BusinessProcessByRole(BaseModel):
    business_process_id: UUID4
    name: str
    process_type: str
    organizational_unit: str
    criticality: str
    status: str
    performance_score: Optional[float]
    last_updated: datetime

class BusinessProcessByFunction(BaseModel):
    business_process_id: UUID4
    name: str
    process_type: str
    organizational_unit: str
    criticality: str
    status: str
    performance_score: Optional[float]
    last_updated: datetime

class BusinessProcessByGoal(BaseModel):
    business_process_id: UUID4
    name: str
    process_type: str
    organizational_unit: str
    criticality: str
    status: str
    performance_score: Optional[float]
    last_updated: datetime

class BusinessProcessByStatus(BaseModel):
    business_process_id: UUID4
    name: str
    process_type: str
    organizational_unit: str
    criticality: str
    status: str
    performance_score: Optional[float]
    last_updated: datetime

class BusinessProcessByCriticality(BaseModel):
    business_process_id: UUID4
    name: str
    process_type: str
    organizational_unit: str
    criticality: str
    status: str
    performance_score: Optional[float]
    last_updated: datetime 