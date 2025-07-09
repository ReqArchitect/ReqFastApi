from pydantic import BaseModel, UUID4, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CompetencyArea(str, Enum):
    ARCHITECTURE_GOVERNANCE = "Architecture Governance"
    COMPLIANCE_MANAGEMENT = "Compliance Management"
    STRATEGY_ANALYSIS = "Strategy Analysis"
    VENDOR_EVALUATION = "Vendor Evaluation"
    RISK_MANAGEMENT = "Risk Management"
    PERFORMANCE_MONITORING = "Performance Monitoring"
    QUALITY_ASSURANCE = "Quality Assurance"
    CHANGE_MANAGEMENT = "Change Management"
    CAPACITY_PLANNING = "Capacity Planning"
    COST_MANAGEMENT = "Cost Management"
    SECURITY_MANAGEMENT = "Security Management"
    DATA_MANAGEMENT = "Data Management"
    TECHNOLOGY_EVALUATION = "Technology Evaluation"
    PROCESS_OPTIMIZATION = "Process Optimization"
    STAKEHOLDER_MANAGEMENT = "Stakeholder Management"

class Frequency(str, Enum):
    ONGOING = "ongoing"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"
    AD_HOC = "ad_hoc"

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

class MaturityLevel(str, Enum):
    BASIC = "basic"
    DEVELOPING = "developing"
    MATURE = "mature"
    ADVANCED = "advanced"

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

class FunctionStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    PLANNED = "planned"

class OperationalHours(str, Enum):
    TWENTY_FOUR_SEVEN = "24x7"
    BUSINESS_HOURS = "business_hours"
    ON_DEMAND = "on_demand"

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

class LinkType(str, Enum):
    ENABLES = "enables"
    SUPPORTS = "supports"
    REALIZES = "realizes"
    GOVERNS = "governs"
    INFLUENCES = "influences"
    CONSUMES = "consumes"
    PRODUCES = "produces"

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

class DataFlowDirection(str, Enum):
    INPUT = "input"
    OUTPUT = "output"
    BIDIRECTIONAL = "bidirectional"

# Base schemas
class BusinessFunctionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    competency_area: CompetencyArea
    organizational_unit: str = Field(..., min_length=1, max_length=255)
    owner_role_id: Optional[UUID4] = None
    input_object_type: Optional[str] = None
    output_object_type: Optional[str] = None
    input_description: Optional[str] = None
    output_description: Optional[str] = None
    frequency: Frequency = Frequency.ONGOING
    criticality: Criticality = Criticality.MEDIUM
    complexity: Complexity = Complexity.MEDIUM
    maturity_level: MaturityLevel = MaturityLevel.BASIC
    alignment_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    efficiency_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    effectiveness_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    performance_metrics: Optional[str] = None
    required_skills: Optional[str] = None
    required_capabilities: Optional[str] = None
    resource_requirements: Optional[str] = None
    technology_dependencies: Optional[str] = None
    compliance_requirements: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.MEDIUM
    audit_frequency: AuditFrequency = AuditFrequency.ANNUALLY
    last_audit_date: Optional[datetime] = None
    audit_status: AuditStatus = AuditStatus.PENDING
    status: FunctionStatus = FunctionStatus.ACTIVE
    operational_hours: OperationalHours = OperationalHours.BUSINESS_HOURS
    availability_target: Optional[float] = Field(None, ge=0.0, le=100.0)
    current_availability: Optional[float] = Field(None, ge=0.0, le=100.0)
    strategic_importance: StrategicImportance = StrategicImportance.MEDIUM
    business_value: BusinessValue = BusinessValue.MEDIUM
    cost_center: Optional[str] = None
    budget_allocation: Optional[float] = Field(None, ge=0.0)
    parent_function_id: Optional[UUID4] = None
    supporting_capability_id: Optional[UUID4] = None
    business_process_id: Optional[UUID4] = None

    @validator('alignment_score', 'efficiency_score', 'effectiveness_score')
    def validate_scores(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Score must be between 0.0 and 1.0')
        return v

    @validator('availability_target', 'current_availability')
    def validate_availability(cls, v):
        if v is not None and (v < 0.0 or v > 100.0):
            raise ValueError('Availability must be between 0.0 and 100.0')
        return v

    @validator('budget_allocation')
    def validate_budget(cls, v):
        if v is not None and v < 0.0:
            raise ValueError('Budget allocation must be non-negative')
        return v

class BusinessFunctionCreate(BusinessFunctionBase):
    pass

class BusinessFunctionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    competency_area: Optional[CompetencyArea] = None
    organizational_unit: Optional[str] = Field(None, min_length=1, max_length=255)
    owner_role_id: Optional[UUID4] = None
    input_object_type: Optional[str] = None
    output_object_type: Optional[str] = None
    input_description: Optional[str] = None
    output_description: Optional[str] = None
    frequency: Optional[Frequency] = None
    criticality: Optional[Criticality] = None
    complexity: Optional[Complexity] = None
    maturity_level: Optional[MaturityLevel] = None
    alignment_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    efficiency_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    effectiveness_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    performance_metrics: Optional[str] = None
    required_skills: Optional[str] = None
    required_capabilities: Optional[str] = None
    resource_requirements: Optional[str] = None
    technology_dependencies: Optional[str] = None
    compliance_requirements: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    audit_frequency: Optional[AuditFrequency] = None
    last_audit_date: Optional[datetime] = None
    audit_status: Optional[AuditStatus] = None
    status: Optional[FunctionStatus] = None
    operational_hours: Optional[OperationalHours] = None
    availability_target: Optional[float] = Field(None, ge=0.0, le=100.0)
    current_availability: Optional[float] = Field(None, ge=0.0, le=100.0)
    strategic_importance: Optional[StrategicImportance] = None
    business_value: Optional[BusinessValue] = None
    cost_center: Optional[str] = None
    budget_allocation: Optional[float] = Field(None, ge=0.0)
    parent_function_id: Optional[UUID4] = None
    supporting_capability_id: Optional[UUID4] = None
    business_process_id: Optional[UUID4] = None

class BusinessFunctionInDBBase(BusinessFunctionBase):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class BusinessFunction(BusinessFunctionInDBBase):
    pass

# Link schemas
class FunctionLinkBase(BaseModel):
    linked_element_id: UUID4
    linked_element_type: str = Field(..., min_length=1, max_length=100)
    link_type: LinkType
    relationship_strength: RelationshipStrength = RelationshipStrength.MEDIUM
    dependency_level: DependencyLevel = DependencyLevel.MEDIUM
    interaction_frequency: InteractionFrequency = InteractionFrequency.REGULAR
    interaction_type: InteractionType = InteractionType.SYNCHRONOUS
    data_flow_direction: DataFlowDirection = DataFlowDirection.BIDIRECTIONAL

class FunctionLinkCreate(FunctionLinkBase):
    pass

class FunctionLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID4] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=100)
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    interaction_frequency: Optional[InteractionFrequency] = None
    interaction_type: Optional[InteractionType] = None
    data_flow_direction: Optional[DataFlowDirection] = None

class FunctionLinkInDBBase(FunctionLinkBase):
    id: UUID4
    business_function_id: UUID4
    created_by: UUID4
    created_at: datetime

    class Config:
        orm_mode = True

class FunctionLink(FunctionLinkInDBBase):
    pass

# Response schemas
class BusinessFunctionWithLinks(BusinessFunction):
    links: List[FunctionLink] = []

class BusinessFunctionList(BaseModel):
    business_functions: List[BusinessFunction]
    total: int
    skip: int
    limit: int

class ImpactMap(BaseModel):
    business_function_id: UUID4
    linked_elements_count: int
    business_roles_count: int
    business_processes_count: int
    capabilities_count: int
    application_services_count: int
    data_objects_count: int
    overall_impact_score: float
    last_assessed: datetime

class BusinessFunctionAnalysis(BaseModel):
    business_function_id: UUID4
    alignment_score: float
    efficiency_score: float
    effectiveness_score: float
    risk_score: float
    strategic_importance_score: float
    business_value_score: float
    overall_health_score: float
    last_analyzed: datetime

class BusinessFunctionByRole(BaseModel):
    business_function_id: UUID4
    name: str
    competency_area: str
    organizational_unit: str
    criticality: str
    status: str
    alignment_score: Optional[float]
    last_updated: datetime

class BusinessFunctionByProcess(BaseModel):
    business_function_id: UUID4
    name: str
    competency_area: str
    organizational_unit: str
    frequency: str
    complexity: str
    maturity_level: str
    last_updated: datetime 