from pydantic import BaseModel, UUID4, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RoleType(str, Enum):
    ARCHITECTURE_LEAD = "Architecture Lead"
    COMPLIANCE_OFFICER = "Compliance Officer"
    STRATEGY_ANALYST = "Strategy Analyst"
    VENDOR_MANAGER = "Vendor Manager"
    DATA_CUSTODIAN = "Data Custodian"
    SECURITY_OFFICER = "Security Officer"
    RISK_MANAGER = "Risk Manager"
    QUALITY_ASSURANCE_LEAD = "Quality Assurance Lead"
    CHANGE_MANAGER = "Change Manager"
    CAPACITY_PLANNER = "Capacity Planner"
    COST_MANAGER = "Cost Manager"
    PERFORMANCE_ANALYST = "Performance Analyst"
    STAKEHOLDER_MANAGER = "Stakeholder Manager"
    TECHNOLOGY_EVALUATOR = "Technology Evaluator"
    PROCESS_OPTIMIZER = "Process Optimizer"

class RoleClassification(str, Enum):
    STRATEGIC = "strategic"
    TACTICAL = "tactical"
    OPERATIONAL = "operational"
    SUPPORT = "support"

class AuthorityLevel(str, Enum):
    EXECUTIVE = "executive"
    SENIOR = "senior"
    STANDARD = "standard"
    JUNIOR = "junior"
    TRAINEE = "trainee"

class DecisionMakingAuthority(str, Enum):
    FULL = "full"
    PARTIAL = "partial"
    LIMITED = "limited"
    NONE = "none"

class ApprovalAuthority(str, Enum):
    FULL = "full"
    PARTIAL = "partial"
    LIMITED = "limited"
    NONE = "none"

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

class WorkloadLevel(str, Enum):
    LIGHT = "light"
    STANDARD = "standard"
    HEAVY = "heavy"
    OVERLOADED = "overloaded"

class AvailabilityRequirement(str, Enum):
    TWENTY_FOUR_SEVEN = "24x7"
    BUSINESS_HOURS = "business_hours"
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

class RoleStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    PLANNED = "planned"

class OperationalHours(str, Enum):
    TWENTY_FOUR_SEVEN = "24x7"
    BUSINESS_HOURS = "business_hours"
    ON_DEMAND = "on_demand"

class LinkType(str, Enum):
    PERFORMS = "performs"
    OWNS = "owns"
    MANAGES = "manages"
    SUPPORTS = "supports"
    COLLABORATES = "collaborates"
    REPORTS_TO = "reports_to"
    SUPERVISES = "supervises"

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

class AccountabilityLevel(str, Enum):
    FULL = "full"
    PARTIAL = "partial"
    SHARED = "shared"
    ADVISORY = "advisory"

class PerformanceImpact(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"

# Base schemas
class BusinessRoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    organizational_unit: str = Field(..., min_length=1, max_length=255)
    role_type: RoleType
    responsibilities: Optional[str] = None
    required_skills: Optional[str] = None
    required_capabilities: Optional[str] = None
    stakeholder_id: Optional[UUID4] = None
    role_classification: RoleClassification = RoleClassification.OPERATIONAL
    authority_level: AuthorityLevel = AuthorityLevel.STANDARD
    decision_making_authority: DecisionMakingAuthority = DecisionMakingAuthority.LIMITED
    approval_authority: ApprovalAuthority = ApprovalAuthority.NONE
    strategic_importance: StrategicImportance = StrategicImportance.MEDIUM
    business_value: BusinessValue = BusinessValue.MEDIUM
    capability_alignment: Optional[float] = Field(None, ge=0.0, le=1.0)
    strategic_alignment: Optional[float] = Field(None, ge=0.0, le=1.0)
    performance_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    effectiveness_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    efficiency_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    satisfaction_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    performance_metrics: Optional[str] = None
    criticality: Criticality = Criticality.MEDIUM
    complexity: Complexity = Complexity.MEDIUM
    workload_level: WorkloadLevel = WorkloadLevel.STANDARD
    availability_requirement: AvailabilityRequirement = AvailabilityRequirement.BUSINESS_HOURS
    headcount_requirement: Optional[int] = Field(None, ge=1)
    current_headcount: Optional[int] = Field(None, ge=0)
    skill_gaps: Optional[str] = None
    training_requirements: Optional[str] = None
    compliance_requirements: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.MEDIUM
    audit_frequency: AuditFrequency = AuditFrequency.ANNUALLY
    last_audit_date: Optional[datetime] = None
    audit_status: AuditStatus = AuditStatus.PENDING
    status: RoleStatus = RoleStatus.ACTIVE
    operational_hours: OperationalHours = OperationalHours.BUSINESS_HOURS
    availability_target: Optional[float] = Field(None, ge=0.0, le=100.0)
    current_availability: Optional[float] = Field(None, ge=0.0, le=100.0)
    cost_center: Optional[str] = None
    budget_allocation: Optional[float] = Field(None, ge=0.0)
    salary_range_min: Optional[float] = Field(None, ge=0.0)
    salary_range_max: Optional[float] = Field(None, ge=0.0)
    total_compensation: Optional[float] = Field(None, ge=0.0)
    reporting_to_role_id: Optional[UUID4] = None
    supporting_capability_id: Optional[UUID4] = None
    business_function_id: Optional[UUID4] = None
    business_process_id: Optional[UUID4] = None

    @validator('capability_alignment', 'strategic_alignment', 'performance_score', 'effectiveness_score', 'efficiency_score', 'satisfaction_score')
    def validate_scores(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Score must be between 0.0 and 1.0')
        return v

    @validator('availability_target', 'current_availability')
    def validate_availability(cls, v):
        if v is not None and (v < 0.0 or v > 100.0):
            raise ValueError('Availability must be between 0.0 and 100.0')
        return v

    @validator('budget_allocation', 'salary_range_min', 'salary_range_max', 'total_compensation')
    def validate_financial(cls, v):
        if v is not None and v < 0.0:
            raise ValueError('Financial values must be non-negative')
        return v

    @validator('headcount_requirement', 'current_headcount')
    def validate_headcount(cls, v):
        if v is not None and v < 0:
            raise ValueError('Headcount must be non-negative')
        return v

class BusinessRoleCreate(BusinessRoleBase):
    pass

class BusinessRoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    organizational_unit: Optional[str] = Field(None, min_length=1, max_length=255)
    role_type: Optional[RoleType] = None
    responsibilities: Optional[str] = None
    required_skills: Optional[str] = None
    required_capabilities: Optional[str] = None
    stakeholder_id: Optional[UUID4] = None
    role_classification: Optional[RoleClassification] = None
    authority_level: Optional[AuthorityLevel] = None
    decision_making_authority: Optional[DecisionMakingAuthority] = None
    approval_authority: Optional[ApprovalAuthority] = None
    strategic_importance: Optional[StrategicImportance] = None
    business_value: Optional[BusinessValue] = None
    capability_alignment: Optional[float] = Field(None, ge=0.0, le=1.0)
    strategic_alignment: Optional[float] = Field(None, ge=0.0, le=1.0)
    performance_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    effectiveness_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    efficiency_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    satisfaction_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    performance_metrics: Optional[str] = None
    criticality: Optional[Criticality] = None
    complexity: Optional[Complexity] = None
    workload_level: Optional[WorkloadLevel] = None
    availability_requirement: Optional[AvailabilityRequirement] = None
    headcount_requirement: Optional[int] = Field(None, ge=1)
    current_headcount: Optional[int] = Field(None, ge=0)
    skill_gaps: Optional[str] = None
    training_requirements: Optional[str] = None
    compliance_requirements: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    audit_frequency: Optional[AuditFrequency] = None
    last_audit_date: Optional[datetime] = None
    audit_status: Optional[AuditStatus] = None
    status: Optional[RoleStatus] = None
    operational_hours: Optional[OperationalHours] = None
    availability_target: Optional[float] = Field(None, ge=0.0, le=100.0)
    current_availability: Optional[float] = Field(None, ge=0.0, le=100.0)
    cost_center: Optional[str] = None
    budget_allocation: Optional[float] = Field(None, ge=0.0)
    salary_range_min: Optional[float] = Field(None, ge=0.0)
    salary_range_max: Optional[float] = Field(None, ge=0.0)
    total_compensation: Optional[float] = Field(None, ge=0.0)
    reporting_to_role_id: Optional[UUID4] = None
    supporting_capability_id: Optional[UUID4] = None
    business_function_id: Optional[UUID4] = None
    business_process_id: Optional[UUID4] = None

class BusinessRoleInDBBase(BusinessRoleBase):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class BusinessRole(BusinessRoleInDBBase):
    pass

# Link schemas
class RoleLinkBase(BaseModel):
    linked_element_id: UUID4
    linked_element_type: str = Field(..., min_length=1, max_length=100)
    link_type: LinkType
    relationship_strength: RelationshipStrength = RelationshipStrength.MEDIUM
    dependency_level: DependencyLevel = DependencyLevel.MEDIUM
    interaction_frequency: InteractionFrequency = InteractionFrequency.REGULAR
    interaction_type: InteractionType = InteractionType.SYNCHRONOUS
    responsibility_level: ResponsibilityLevel = ResponsibilityLevel.SHARED
    accountability_level: AccountabilityLevel = AccountabilityLevel.SHARED
    performance_impact: PerformanceImpact = PerformanceImpact.MEDIUM
    decision_authority: DecisionMakingAuthority = DecisionMakingAuthority.NONE

class RoleLinkCreate(RoleLinkBase):
    pass

class RoleLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID4] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=100)
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    interaction_frequency: Optional[InteractionFrequency] = None
    interaction_type: Optional[InteractionType] = None
    responsibility_level: Optional[ResponsibilityLevel] = None
    accountability_level: Optional[AccountabilityLevel] = None
    performance_impact: Optional[PerformanceImpact] = None
    decision_authority: Optional[DecisionMakingAuthority] = None

class RoleLinkInDBBase(RoleLinkBase):
    id: UUID4
    business_role_id: UUID4
    created_by: UUID4
    created_at: datetime

    class Config:
        orm_mode = True

class RoleLink(RoleLinkInDBBase):
    pass

# Response schemas
class BusinessRoleWithLinks(BusinessRole):
    links: List[RoleLink] = []

class BusinessRoleList(BaseModel):
    business_roles: List[BusinessRole]
    total: int
    skip: int
    limit: int

class ResponsibilityMap(BaseModel):
    business_role_id: UUID4
    linked_elements_count: int
    business_functions_count: int
    business_processes_count: int
    application_services_count: int
    data_objects_count: int
    stakeholders_count: int
    overall_responsibility_score: float
    last_assessed: datetime

class BusinessRoleAlignment(BaseModel):
    business_role_id: UUID4
    capability_alignment: float
    strategic_alignment: float
    performance_score: float
    effectiveness_score: float
    efficiency_score: float
    satisfaction_score: float
    overall_alignment_score: float
    last_analyzed: datetime

class BusinessRoleByOrganizationalUnit(BaseModel):
    business_role_id: UUID4
    name: str
    role_type: str
    organizational_unit: str
    strategic_importance: str
    status: str
    capability_alignment: Optional[float]
    last_updated: datetime

class BusinessRoleByStakeholder(BaseModel):
    business_role_id: UUID4
    name: str
    role_type: str
    organizational_unit: str
    authority_level: str
    criticality: str
    last_updated: datetime

class BusinessRoleByCapability(BaseModel):
    business_role_id: UUID4
    name: str
    role_type: str
    organizational_unit: str
    capability_alignment: float
    strategic_alignment: float
    last_updated: datetime 