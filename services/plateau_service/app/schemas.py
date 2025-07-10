from pydantic import BaseModel, Field, validator, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums for Plateau
class MaturityLevel(str, Enum):
    INITIAL = "initial"
    DEVELOPING = "developing"
    MATURE = "mature"
    OPTIMIZED = "optimized"

class TransformationPhase(str, Enum):
    PLANNING = "planning"
    IMPLEMENTATION = "implementation"
    VALIDATION = "validation"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"

class Status(str, Enum):
    PLANNED = "planned"
    CURRENT = "current"
    HISTORICAL = "historical"
    CANCELLED = "cancelled"

class LifecycleState(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class ReportingFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class DocumentationStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# Enums for PlateauLink
class LinkType(str, Enum):
    REALIZES = "realizes"
    SUPPORTS = "supports"
    ENABLES = "enables"
    DEPENDS_ON = "depends_on"
    IMPACTS = "impacts"
    INFLUENCES = "influences"
    GOVERNES = "governes"

class RelationshipStrength(str, Enum):
    STRONG = "strong"
    MEDIUM = "medium"
    WEAK = "weak"

class DependencyLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TransformationImpact(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ChangeScope(str, Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    TRANSFORMATIONAL = "transformational"

class ImplementationComplexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BusinessCriticality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class StrategicImportance(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ImplementationStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ImplementationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ImplementationPhase(str, Enum):
    PLANNING = "planning"
    IMPLEMENTATION = "implementation"
    VALIDATION = "validation"
    DEPLOYMENT = "deployment"

class ComplianceImpact(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SecurityImpact(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RegulatoryImpact(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Base schemas
class PlateauBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Plateau name")
    description: Optional[str] = Field(None, max_length=1000, description="Plateau description")
    time_window_start: datetime = Field(..., description="Start of time window")
    time_window_end: datetime = Field(..., description="End of time window")
    maturity_level: MaturityLevel = Field(..., description="Maturity level")
    business_value_score: float = Field(0.0, ge=0.0, le=1.0, description="Business value score (0.0 to 1.0)")
    transformation_phase: TransformationPhase = Field(..., description="Transformation phase")
    status: Status = Field(Status.PLANNED, description="Plateau status")
    
    # Stakeholder and ownership
    stakeholder_id: Optional[UUID4] = Field(None, description="Stakeholder ID")
    owner_id: Optional[UUID4] = Field(None, description="Owner ID")
    sponsor_id: Optional[UUID4] = Field(None, description="Sponsor ID")
    
    # Associated capabilities and components
    associated_capability_ids: Optional[str] = Field(None, description="JSON string of capability IDs")
    associated_goal_ids: Optional[str] = Field(None, description="JSON string of goal IDs")
    associated_workpackage_ids: Optional[str] = Field(None, description="JSON string of workpackage IDs")
    associated_component_ids: Optional[str] = Field(None, description="JSON string of component IDs")
    associated_gap_ids: Optional[str] = Field(None, description="JSON string of gap IDs")
    
    # Architecture snapshot
    snapshot_hash: Optional[str] = Field(None, max_length=64, description="Hash of architecture snapshot")
    snapshot_data: Optional[str] = Field(None, description="JSON string of architecture snapshot")
    baseline_architecture_id: Optional[UUID4] = Field(None, description="Baseline architecture ID")
    target_architecture_id: Optional[UUID4] = Field(None, description="Target architecture ID")
    
    # Progress and metrics
    completion_percentage: float = Field(0.0, ge=0.0, le=100.0, description="Completion percentage")
    on_track_score: float = Field(0.0, ge=0.0, le=1.0, description="On track score (0.0 to 1.0)")
    risk_score: float = Field(0.0, ge=0.0, le=1.0, description="Risk score (0.0 to 1.0)")
    quality_score: float = Field(0.0, ge=0.0, le=1.0, description="Quality score (0.0 to 1.0)")
    
    # Financial metrics
    budget_allocated: Optional[float] = Field(None, ge=0, description="Budget allocated in currency")
    budget_spent: Optional[float] = Field(None, ge=0, description="Budget spent in currency")
    cost_savings: Optional[float] = Field(None, description="Cost savings achieved")
    roi_percentage: Optional[float] = Field(None, description="Return on investment percentage")
    business_impact_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Business impact score (0.0 to 1.0)")
    
    # Timeline and milestones
    planned_start_date: Optional[datetime] = Field(None, description="Planned start date")
    planned_end_date: Optional[datetime] = Field(None, description="Planned end date")
    actual_start_date: Optional[datetime] = Field(None, description="Actual start date")
    actual_end_date: Optional[datetime] = Field(None, description="Actual end date")
    critical_path_duration: Optional[int] = Field(None, ge=0, description="Critical path duration in days")
    slack_days: Optional[int] = Field(None, ge=0, description="Available slack in days")
    
    # Dependencies and constraints
    dependencies: Optional[str] = Field(None, description="JSON string of dependencies")
    constraints: Optional[str] = Field(None, description="JSON string of constraints")
    assumptions: Optional[str] = Field(None, description="JSON string of assumptions")
    risks: Optional[str] = Field(None, description="JSON string of risks")
    
    # Change management
    change_requests: Optional[str] = Field(None, description="JSON string of change requests")
    approved_changes: Optional[str] = Field(None, description="JSON string of approved changes")
    rejected_changes: Optional[str] = Field(None, description="JSON string of rejected changes")
    change_impact_assessment: Optional[str] = Field(None, description="JSON string of impact assessment")
    
    # Quality and compliance
    quality_gates: Optional[str] = Field(None, description="JSON string of quality gates")
    compliance_requirements: Optional[str] = Field(None, description="JSON string of compliance requirements")
    audit_trail: Optional[str] = Field(None, description="JSON string of audit trail")
    approval_status: ApprovalStatus = Field(ApprovalStatus.PENDING, description="Approval status")
    
    # Communication and reporting
    communication_plan: Optional[str] = Field(None, description="JSON string of communication plan")
    stakeholder_updates: Optional[str] = Field(None, description="JSON string of stakeholder updates")
    reporting_frequency: ReportingFrequency = Field(ReportingFrequency.WEEKLY, description="Reporting frequency")
    escalation_procedures: Optional[str] = Field(None, description="JSON string of escalation procedures")
    
    # Performance metrics
    kpi_targets: Optional[str] = Field(None, description="JSON string of KPI targets")
    kpi_actuals: Optional[str] = Field(None, description="JSON string of KPI actuals")
    performance_metrics: Optional[str] = Field(None, description="JSON string of performance metrics")
    success_criteria: Optional[str] = Field(None, description="JSON string of success criteria")
    
    # Resource allocation
    resource_requirements: Optional[str] = Field(None, description="JSON string of resource requirements")
    resource_allocation: Optional[str] = Field(None, description="JSON string of resource allocation")
    skill_requirements: Optional[str] = Field(None, description="JSON string of skill requirements")
    training_requirements: Optional[str] = Field(None, description="JSON string of training requirements")
    
    # Technology and infrastructure
    technology_stack: Optional[str] = Field(None, description="JSON string of technology stack")
    infrastructure_requirements: Optional[str] = Field(None, description="JSON string of infrastructure requirements")
    integration_requirements: Optional[str] = Field(None, description="JSON string of integration requirements")
    migration_strategy: Optional[str] = Field(None, description="JSON string of migration strategy")
    
    # Business alignment
    business_objectives: Optional[str] = Field(None, description="JSON string of business objectives")
    strategic_alignment: Optional[float] = Field(None, ge=0.0, le=1.0, description="Strategic alignment (0.0 to 1.0)")
    stakeholder_satisfaction: Optional[float] = Field(None, ge=0.0, le=1.0, description="Stakeholder satisfaction (0.0 to 1.0)")
    business_readiness: Optional[float] = Field(None, ge=0.0, le=1.0, description="Business readiness (0.0 to 1.0)")
    
    # Lessons learned and knowledge management
    lessons_learned: Optional[str] = Field(None, description="JSON string of lessons learned")
    best_practices: Optional[str] = Field(None, description="JSON string of best practices")
    documentation_status: DocumentationStatus = Field(DocumentationStatus.IN_PROGRESS, description="Documentation status")
    knowledge_transfer: Optional[str] = Field(None, description="JSON string of knowledge transfer")
    
    # Governance and oversight
    governance_structure: Optional[str] = Field(None, description="JSON string of governance structure")
    decision_making_process: Optional[str] = Field(None, description="JSON string of decision making process")
    escalation_matrix: Optional[str] = Field(None, description="JSON string of escalation matrix")
    approval_workflow: Optional[str] = Field(None, description="JSON string of approval workflow")
    
    # Risk management
    risk_register: Optional[str] = Field(None, description="JSON string of risk register")
    mitigation_strategies: Optional[str] = Field(None, description="JSON string of mitigation strategies")
    contingency_plans: Optional[str] = Field(None, description="JSON string of contingency plans")
    risk_monitoring: Optional[str] = Field(None, description="JSON string of risk monitoring")
    
    # Status and lifecycle
    lifecycle_state: LifecycleState = Field(LifecycleState.PLANNING, description="Lifecycle state")
    priority_level: PriorityLevel = Field(PriorityLevel.MEDIUM, description="Priority level")

    @validator('time_window_end')
    def validate_time_window(cls, v, values):
        if 'time_window_start' in values and v <= values['time_window_start']:
            raise ValueError('Time window end must be after start')
        return v

    @validator('snapshot_hash')
    def validate_snapshot_hash(cls, v):
        if v and len(v) < 8:
            raise ValueError('Snapshot hash must be at least 8 characters long')
        return v

    @validator('completion_percentage', 'on_track_score', 'risk_score', 'quality_score')
    def validate_percentage_values(cls, v):
        if v is not None and (v < 0 or v > 1):
            raise ValueError('Score must be between 0.0 and 1.0')
        return v

class PlateauCreate(PlateauBase):
    pass

class PlateauUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    time_window_start: Optional[datetime] = None
    time_window_end: Optional[datetime] = None
    maturity_level: Optional[MaturityLevel] = None
    business_value_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    transformation_phase: Optional[TransformationPhase] = None
    status: Optional[Status] = None
    completion_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    on_track_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    risk_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    lifecycle_state: Optional[LifecycleState] = None
    priority_level: Optional[PriorityLevel] = None

class PlateauResponse(PlateauBase):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PlateauListResponse(BaseModel):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    name: str
    time_window_start: datetime
    time_window_end: datetime
    maturity_level: MaturityLevel
    business_value_score: float
    transformation_phase: TransformationPhase
    status: Status
    completion_percentage: float
    on_track_score: float
    risk_score: float
    quality_score: float
    lifecycle_state: LifecycleState
    priority_level: PriorityLevel
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# PlateauLink schemas
class PlateauLinkBase(BaseModel):
    linked_element_id: UUID4 = Field(..., description="Linked element ID")
    linked_element_type: str = Field(..., min_length=1, max_length=50, description="Linked element type")
    link_type: LinkType = Field(..., description="Type of link")
    relationship_strength: RelationshipStrength = Field(RelationshipStrength.MEDIUM, description="Relationship strength")
    dependency_level: DependencyLevel = Field(DependencyLevel.MEDIUM, description="Dependency level")
    
    # Transformation context
    transformation_impact: TransformationImpact = Field(TransformationImpact.MEDIUM, description="Transformation impact")
    change_scope: ChangeScope = Field(ChangeScope.MODERATE, description="Change scope")
    implementation_complexity: ImplementationComplexity = Field(ImplementationComplexity.MEDIUM, description="Implementation complexity")
    risk_level: RiskLevel = Field(RiskLevel.MEDIUM, description="Risk level")
    
    # Business context
    business_criticality: BusinessCriticality = Field(BusinessCriticality.MEDIUM, description="Business criticality")
    business_value: BusinessCriticality = Field(BusinessCriticality.MEDIUM, description="Business value")
    strategic_importance: StrategicImportance = Field(StrategicImportance.MEDIUM, description="Strategic importance")
    stakeholder_impact: BusinessCriticality = Field(BusinessCriticality.MEDIUM, description="Stakeholder impact")
    
    # Implementation context
    implementation_status: ImplementationStatus = Field(ImplementationStatus.PLANNED, description="Implementation status")
    implementation_priority: ImplementationPriority = Field(ImplementationPriority.MEDIUM, description="Implementation priority")
    implementation_phase: ImplementationPhase = Field(ImplementationPhase.PLANNING, description="Implementation phase")
    implementation_timeline: Optional[str] = Field(None, description="JSON string of implementation timeline")
    
    # Resource context
    resource_requirements: Optional[str] = Field(None, description="JSON string of resource requirements")
    skill_requirements: Optional[str] = Field(None, description="JSON string of skill requirements")
    budget_impact: Optional[float] = Field(None, description="Budget impact in currency")
    effort_estimate: Optional[int] = Field(None, ge=0, description="Effort estimate in person-days")
    
    # Performance context
    performance_impact: TransformationImpact = Field(TransformationImpact.MEDIUM, description="Performance impact")
    quality_impact: TransformationImpact = Field(TransformationImpact.MEDIUM, description="Quality impact")
    efficiency_gain: Optional[float] = Field(None, description="Efficiency gain percentage")
    effectiveness_improvement: Optional[float] = Field(None, description="Effectiveness improvement percentage")
    
    # Risk and compliance
    risk_assessment: Optional[str] = Field(None, description="JSON string of risk assessment")
    compliance_impact: ComplianceImpact = Field(ComplianceImpact.LOW, description="Compliance impact")
    security_impact: SecurityImpact = Field(SecurityImpact.MEDIUM, description="Security impact")
    regulatory_impact: RegulatoryImpact = Field(RegulatoryImpact.LOW, description="Regulatory impact")
    
    # Success metrics
    success_criteria: Optional[str] = Field(None, description="JSON string of success criteria")
    kpi_targets: Optional[str] = Field(None, description="JSON string of KPI targets")
    measurement_framework: Optional[str] = Field(None, description="JSON string of measurement framework")
    validation_approach: Optional[str] = Field(None, description="JSON string of validation approach")
    
    # Dependencies and constraints
    dependencies: Optional[str] = Field(None, description="JSON string of dependencies")
    constraints: Optional[str] = Field(None, description="JSON string of constraints")
    prerequisites: Optional[str] = Field(None, description="JSON string of prerequisites")
    blockers: Optional[str] = Field(None, description="JSON string of blockers")
    
    # Communication and change management
    communication_plan: Optional[str] = Field(None, description="JSON string of communication plan")
    change_management_approach: Optional[str] = Field(None, description="JSON string of change management approach")
    stakeholder_engagement: Optional[str] = Field(None, description="JSON string of stakeholder engagement")
    training_requirements: Optional[str] = Field(None, description="JSON string of training requirements")
    
    # Monitoring and governance
    monitoring_framework: Optional[str] = Field(None, description="JSON string of monitoring framework")
    governance_structure: Optional[str] = Field(None, description="JSON string of governance structure")
    escalation_procedures: Optional[str] = Field(None, description="JSON string of escalation procedures")
    approval_workflow: Optional[str] = Field(None, description="JSON string of approval workflow")

class PlateauLinkCreate(PlateauLinkBase):
    pass

class PlateauLinkUpdate(BaseModel):
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    transformation_impact: Optional[TransformationImpact] = None
    change_scope: Optional[ChangeScope] = None
    implementation_complexity: Optional[ImplementationComplexity] = None
    risk_level: Optional[RiskLevel] = None
    business_criticality: Optional[BusinessCriticality] = None
    implementation_status: Optional[ImplementationStatus] = None
    implementation_priority: Optional[ImplementationPriority] = None
    implementation_phase: Optional[ImplementationPhase] = None

class PlateauLinkResponse(PlateauLinkBase):
    id: UUID4
    plateau_id: UUID4
    created_by: UUID4
    created_at: datetime

    class Config:
        from_attributes = True

# Analysis response schemas
class ChangeMapResponse(BaseModel):
    plateau_id: UUID4
    plateau_name: str
    transformation_phase: TransformationPhase
    change_elements: List[Dict[str, Any]]
    impacted_capabilities: List[Dict[str, Any]]
    impacted_goals: List[Dict[str, Any]]
    impacted_workpackages: List[Dict[str, Any]]
    change_score: float
    recommendations: List[str]

class ValueMetricsResponse(BaseModel):
    plateau_id: UUID4
    plateau_name: str
    business_value_score: float
    roi_percentage: Optional[float]
    cost_savings: Optional[float]
    efficiency_gain: Optional[float]
    effectiveness_improvement: Optional[float]
    stakeholder_satisfaction: Optional[float]
    strategic_alignment: Optional[float]
    business_impact_score: Optional[float]
    value_metrics: List[Dict[str, Any]]
    recommendations: List[str]

# Enumeration response schemas
class EnumerationResponse(BaseModel):
    values: List[str]
    count: int 