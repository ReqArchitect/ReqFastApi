from pydantic import BaseModel, Field, validator, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums for Gap
class GapType(str, Enum):
    CAPABILITY = "capability"
    PROCESS = "process"
    TECHNOLOGY = "technology"
    COMPLIANCE = "compliance"
    PERFORMANCE = "performance"
    DATA = "data"
    SECURITY = "security"
    INTEGRATION = "integration"
    USER_EXPERIENCE = "user_experience"
    BUSINESS_PROCESS = "business_process"

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ImpactArea(str, Enum):
    BUSINESS = "business"
    APPLICATION = "application"
    TECHNOLOGY = "technology"
    DATA = "data"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    OPERATIONS = "operations"
    CUSTOMER = "customer"

class ResolutionApproach(str, Enum):
    WORKAROUND = "workaround"
    TEMPORARY_FIX = "temporary_fix"
    PERMANENT_SOLUTION = "permanent_solution"
    REDESIGN = "redesign"
    REPLACEMENT = "replacement"
    UPGRADE = "upgrade"

class ResolutionStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class ResolutionPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ImpactLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Status(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class LifecycleState(str, Enum):
    IDENTIFIED = "identified"
    ANALYZED = "analyzed"
    PLANNED = "planned"
    IMPLEMENTING = "implementing"
    RESOLVED = "resolved"

class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class DocumentationStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ReportingFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

# Enums for GapLink
class LinkType(str, Enum):
    IMPACTS = "impacts"
    DEPENDS_ON = "depends_on"
    BLOCKS = "blocks"
    ENABLES = "enables"
    CONSTRAINS = "constrains"
    REALIZES = "realizes"
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

class ImpactType(str, Enum):
    DIRECT = "direct"
    INDIRECT = "indirect"
    CASCADING = "cascading"

class ImpactDuration(str, Enum):
    TEMPORARY = "temporary"
    PERMANENT = "permanent"
    RECURRING = "recurring"

class ImpactScope(str, Enum):
    LOCAL = "local"
    REGIONAL = "regional"
    GLOBAL = "global"

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

class TechnicalComplexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class ImplementationEffort(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class TechnicalRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

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
class GapBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Gap name")
    description: Optional[str] = Field(None, max_length=1000, description="Gap description")
    gap_type: GapType = Field(..., description="Type of gap")
    severity: Severity = Field(..., description="Gap severity")
    impact_area: ImpactArea = Field(..., description="Impact area")
    
    # Plateau relationships
    source_plateau_id: Optional[UUID4] = Field(None, description="Source plateau ID")
    target_plateau_id: Optional[UUID4] = Field(None, description="Target plateau ID")
    
    # Related elements
    related_requirement_id: Optional[UUID4] = Field(None, description="Related requirement ID")
    related_capability_id: Optional[UUID4] = Field(None, description="Related capability ID")
    related_constraint_id: Optional[UUID4] = Field(None, description="Related constraint ID")
    related_workpackage_id: Optional[UUID4] = Field(None, description="Related workpackage ID")
    
    # Resolution and mitigation
    mitigation_strategy: Optional[str] = Field(None, description="JSON string of mitigation strategy")
    resolution_approach: Optional[ResolutionApproach] = Field(None, description="Resolution approach")
    time_to_resolve_estimate: Optional[int] = Field(None, ge=1, description="Estimated time to resolve in days")
    resolution_priority: ResolutionPriority = Field(ResolutionPriority.MEDIUM, description="Resolution priority")
    resolution_status: ResolutionStatus = Field(ResolutionStatus.OPEN, description="Resolution status")
    
    # Impact assessment
    business_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Business impact")
    technical_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Technical impact")
    operational_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Operational impact")
    financial_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Financial impact")
    
    # Risk assessment
    risk_level: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Risk level")
    risk_description: Optional[str] = Field(None, max_length=500, description="Risk description")
    risk_mitigation: Optional[str] = Field(None, description="JSON string of risk mitigation")
    contingency_plan: Optional[str] = Field(None, description="JSON string of contingency plan")
    
    # Cost and effort
    estimated_cost: Optional[float] = Field(None, ge=0, description="Estimated cost to resolve")
    actual_cost: Optional[float] = Field(None, ge=0, description="Actual cost spent")
    effort_estimate: Optional[int] = Field(None, ge=0, description="Effort estimate in person-days")
    actual_effort: Optional[int] = Field(None, ge=0, description="Actual effort spent in person-days")
    
    # Timeline and scheduling
    identified_date: datetime = Field(default_factory=datetime.utcnow, description="When gap was identified")
    planned_resolution_date: Optional[datetime] = Field(None, description="Planned resolution date")
    actual_resolution_date: Optional[datetime] = Field(None, description="Actual resolution date")
    deadline: Optional[datetime] = Field(None, description="Hard deadline for resolution")
    
    # Dependencies and blockers
    dependencies: Optional[str] = Field(None, description="JSON string of dependencies")
    blockers: Optional[str] = Field(None, description="JSON string of blockers")
    prerequisites: Optional[str] = Field(None, description="JSON string of prerequisites")
    related_gaps: Optional[str] = Field(None, description="JSON string of related gap IDs")
    
    # Stakeholders and ownership
    owner_id: Optional[UUID4] = Field(None, description="Gap owner ID")
    assignee_id: Optional[UUID4] = Field(None, description="Person assigned to resolve")
    stakeholder_ids: Optional[str] = Field(None, description="JSON string of stakeholder IDs")
    approver_id: Optional[UUID4] = Field(None, description="Person who approves resolution")
    
    # Analysis and assessment
    root_cause_analysis: Optional[str] = Field(None, description="JSON string of root cause analysis")
    impact_analysis: Optional[str] = Field(None, description="JSON string of impact analysis")
    solution_alternatives: Optional[str] = Field(None, description="JSON string of solution alternatives")
    recommended_solution: Optional[str] = Field(None, description="JSON string of recommended solution")
    
    # Compliance and governance
    compliance_impact: ComplianceImpact = Field(ComplianceImpact.LOW, description="Compliance impact")
    regulatory_requirements: Optional[str] = Field(None, description="JSON string of regulatory requirements")
    audit_trail: Optional[str] = Field(None, description="JSON string of audit trail")
    approval_status: ApprovalStatus = Field(ApprovalStatus.PENDING, description="Approval status")
    
    # Performance metrics
    performance_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Performance impact")
    efficiency_loss: Optional[float] = Field(None, ge=0, le=100, description="Efficiency loss percentage")
    quality_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Quality impact")
    customer_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Customer impact")
    
    # Technology and architecture
    technology_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Technology impact")
    architecture_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Architecture impact")
    integration_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Integration impact")
    data_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Data impact")
    
    # Security and privacy
    security_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Security impact")
    privacy_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Privacy impact")
    security_requirements: Optional[str] = Field(None, description="JSON string of security requirements")
    privacy_requirements: Optional[str] = Field(None, description="JSON string of privacy requirements")
    
    # Communication and reporting
    communication_plan: Optional[str] = Field(None, description="JSON string of communication plan")
    reporting_frequency: ReportingFrequency = Field(ReportingFrequency.WEEKLY, description="Reporting frequency")
    escalation_procedures: Optional[str] = Field(None, description="JSON string of escalation procedures")
    stakeholder_updates: Optional[str] = Field(None, description="JSON string of stakeholder updates")
    
    # Progress tracking
    progress_percentage: float = Field(0.0, ge=0.0, le=100.0, description="Progress percentage (0.0 to 100.0)")
    milestone_achievements: Optional[str] = Field(None, description="JSON string of milestone achievements")
    blockers_encountered: Optional[str] = Field(None, description="JSON string of blockers encountered")
    lessons_learned: Optional[str] = Field(None, description="JSON string of lessons learned")
    
    # Quality and testing
    quality_gates: Optional[str] = Field(None, description="JSON string of quality gates")
    testing_requirements: Optional[str] = Field(None, description="JSON string of testing requirements")
    validation_criteria: Optional[str] = Field(None, description="JSON string of validation criteria")
    acceptance_criteria: Optional[str] = Field(None, description="JSON string of acceptance criteria")
    
    # Documentation and knowledge
    documentation_status: DocumentationStatus = Field(DocumentationStatus.IN_PROGRESS, description="Documentation status")
    knowledge_transfer: Optional[str] = Field(None, description="JSON string of knowledge transfer")
    best_practices: Optional[str] = Field(None, description="JSON string of best practices")
    training_requirements: Optional[str] = Field(None, description="JSON string of training requirements")
    
    # Status and lifecycle
    status: Status = Field(Status.OPEN, description="Gap status")
    lifecycle_state: LifecycleState = Field(LifecycleState.IDENTIFIED, description="Lifecycle state")

    @validator('time_to_resolve_estimate')
    def validate_time_estimate(cls, v):
        if v is not None and v < 1:
            raise ValueError('Time to resolve estimate must be at least 1 day')
        return v

    @validator('efficiency_loss')
    def validate_efficiency_loss(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Efficiency loss must be between 0 and 100')
        return v

    @validator('progress_percentage')
    def validate_progress_percentage(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Progress percentage must be between 0 and 100')
        return v

    @validator('planned_resolution_date', 'actual_resolution_date', 'deadline')
    def validate_dates(cls, v, values):
        if v and 'identified_date' in values and v <= values['identified_date']:
            raise ValueError('Resolution dates must be after identified date')
        return v

class GapCreate(GapBase):
    pass

class GapUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    gap_type: Optional[GapType] = None
    severity: Optional[Severity] = None
    impact_area: Optional[ImpactArea] = None
    resolution_status: Optional[ResolutionStatus] = None
    resolution_priority: Optional[ResolutionPriority] = None
    progress_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    status: Optional[Status] = None
    lifecycle_state: Optional[LifecycleState] = None
    time_to_resolve_estimate: Optional[int] = Field(None, ge=1)
    estimated_cost: Optional[float] = Field(None, ge=0)
    effort_estimate: Optional[int] = Field(None, ge=0)

class GapResponse(GapBase):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class GapListResponse(BaseModel):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    name: str
    gap_type: GapType
    severity: Severity
    impact_area: ImpactArea
    resolution_status: ResolutionStatus
    resolution_priority: ResolutionPriority
    progress_percentage: float
    status: Status
    lifecycle_state: LifecycleState
    identified_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# GapLink schemas
class GapLinkBase(BaseModel):
    linked_element_id: UUID4 = Field(..., description="Linked element ID")
    linked_element_type: str = Field(..., min_length=1, max_length=50, description="Linked element type")
    link_type: LinkType = Field(..., description="Type of link")
    relationship_strength: RelationshipStrength = Field(RelationshipStrength.MEDIUM, description="Relationship strength")
    dependency_level: DependencyLevel = Field(DependencyLevel.MEDIUM, description="Dependency level")
    
    # Impact context
    impact_level: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Impact level")
    impact_type: ImpactType = Field(ImpactType.DIRECT, description="Impact type")
    impact_duration: ImpactDuration = Field(ImpactDuration.TEMPORARY, description="Impact duration")
    impact_scope: ImpactScope = Field(ImpactScope.LOCAL, description="Impact scope")
    
    # Business context
    business_criticality: BusinessCriticality = Field(BusinessCriticality.MEDIUM, description="Business criticality")
    business_value: BusinessCriticality = Field(BusinessCriticality.MEDIUM, description="Business value")
    strategic_importance: StrategicImportance = Field(StrategicImportance.MEDIUM, description="Strategic importance")
    stakeholder_impact: BusinessCriticality = Field(BusinessCriticality.MEDIUM, description="Stakeholder impact")
    
    # Technical context
    technical_complexity: TechnicalComplexity = Field(TechnicalComplexity.MEDIUM, description="Technical complexity")
    implementation_effort: ImplementationEffort = Field(ImplementationEffort.MEDIUM, description="Implementation effort")
    technical_risk: TechnicalRisk = Field(TechnicalRisk.MEDIUM, description="Technical risk")
    integration_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Integration impact")
    
    # Resolution context
    resolution_priority: ResolutionPriority = Field(ResolutionPriority.MEDIUM, description="Resolution priority")
    resolution_approach: Optional[ResolutionApproach] = Field(None, description="Resolution approach")
    resolution_timeline: Optional[str] = Field(None, description="JSON string of resolution timeline")
    resolution_dependencies: Optional[str] = Field(None, description="JSON string of resolution dependencies")
    
    # Resource context
    resource_requirements: Optional[str] = Field(None, description="JSON string of resource requirements")
    skill_requirements: Optional[str] = Field(None, description="JSON string of skill requirements")
    budget_impact: Optional[float] = Field(None, description="Budget impact in currency")
    effort_estimate: Optional[int] = Field(None, ge=0, description="Effort estimate in person-days")
    
    # Performance context
    performance_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Performance impact")
    efficiency_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Efficiency impact")
    quality_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Quality impact")
    reliability_impact: ImpactLevel = Field(ImpactLevel.MEDIUM, description="Reliability impact")
    
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

class GapLinkCreate(GapLinkBase):
    pass

class GapLinkUpdate(BaseModel):
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    impact_level: Optional[ImpactLevel] = None
    impact_type: Optional[ImpactType] = None
    business_criticality: Optional[BusinessCriticality] = None
    technical_complexity: Optional[TechnicalComplexity] = None
    implementation_effort: Optional[ImplementationEffort] = None
    technical_risk: Optional[TechnicalRisk] = None
    resolution_priority: Optional[ResolutionPriority] = None
    resolution_approach: Optional[ResolutionApproach] = None

class GapLinkResponse(GapLinkBase):
    id: UUID4
    gap_id: UUID4
    created_by: UUID4
    created_at: datetime

    class Config:
        from_attributes = True

# Analysis response schemas
class ImpactMapResponse(BaseModel):
    gap_id: UUID4
    gap_name: str
    gap_type: GapType
    severity: Severity
    impact_elements: List[Dict[str, Any]]
    impacted_capabilities: List[Dict[str, Any]]
    impacted_requirements: List[Dict[str, Any]]
    impacted_constraints: List[Dict[str, Any]]
    impact_score: float
    recommendations: List[str]

class ResolutionStatusResponse(BaseModel):
    gap_id: UUID4
    gap_name: str
    resolution_status: ResolutionStatus
    progress_percentage: float
    resolution_timeline: Dict[str, Any]
    blockers: List[Dict[str, Any]]
    dependencies: List[Dict[str, Any]]
    recommendations: List[str]
    estimated_completion: Optional[datetime]

# Enumeration response schemas
class EnumerationResponse(BaseModel):
    values: List[str]
    count: int 