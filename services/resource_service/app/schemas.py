from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum

class ResourceType(str, Enum):
    HUMAN = "human"
    SYSTEM = "system"
    FINANCIAL = "financial"
    KNOWLEDGE = "knowledge"

class Criticality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

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

class DeploymentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PLANNED = "planned"
    RETIRED = "retired"

class OperationalHours(str, Enum):
    TWENTY_FOUR_SEVEN = "24x7"
    BUSINESS_HOURS = "business_hours"
    ON_DEMAND = "on_demand"

class ExpertiseLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"
    SPECIALIST = "specialist"

class GovernanceModel(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    ENHANCED = "enhanced"
    CRITICAL = "critical"

class LinkType(str, Enum):
    ENABLES = "enables"
    SUPPORTS = "supports"
    REALIZES = "realizes"
    GOVERNS = "governs"
    INFLUENCES = "influences"
    CONSUMES = "consumes"
    PRODUCES = "produces"
    REQUIRES = "requires"

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

class PerformanceImpact(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AllocationPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

# Base schemas
class ResourceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    resource_type: ResourceType = ResourceType.HUMAN
    quantity: float = Field(1.0, gt=0)
    unit_of_measure: str = "unit"
    availability: float = Field(100.0, ge=0, le=100)
    location: Optional[str] = None
    deployment_status: DeploymentStatus = DeploymentStatus.ACTIVE
    criticality: Criticality = Criticality.MEDIUM
    strategic_importance: StrategicImportance = StrategicImportance.MEDIUM
    business_value: BusinessValue = BusinessValue.MEDIUM
    cost_per_unit: Optional[float] = None
    total_cost: Optional[float] = None
    budget_allocation: Optional[float] = None
    cost_center: Optional[str] = None
    skills_required: Optional[str] = None
    capabilities_provided: Optional[str] = None
    expertise_level: ExpertiseLevel = ExpertiseLevel.INTERMEDIATE
    performance_metrics: Optional[str] = None
    utilization_rate: float = Field(0.0, ge=0, le=100)
    efficiency_score: float = Field(0.0, ge=0, le=1)
    effectiveness_score: float = Field(0.0, ge=0, le=1)
    operational_hours: OperationalHours = OperationalHours.BUSINESS_HOURS
    maintenance_schedule: Optional[str] = None
    technology_stack: Optional[str] = None
    system_requirements: Optional[str] = None
    integration_points: Optional[str] = None
    dependencies: Optional[str] = None
    governance_model: GovernanceModel = GovernanceModel.STANDARD
    compliance_requirements: Optional[str] = None
    audit_requirements: Optional[str] = None
    risk_assessment: Optional[str] = None
    parent_resource_id: Optional[UUID] = None
    associated_capability_id: Optional[UUID] = None
    business_function_id: Optional[UUID] = None
    application_component_id: Optional[UUID] = None
    node_id: Optional[UUID] = None

    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than 0')
        return v

    @validator('availability')
    def validate_availability(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Availability must be between 0 and 100')
        return v

    @validator('utilization_rate')
    def validate_utilization_rate(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Utilization rate must be between 0 and 100')
        return v

    @validator('efficiency_score', 'effectiveness_score')
    def validate_scores(cls, v):
        if v < 0 or v > 1:
            raise ValueError('Scores must be between 0 and 1')
        return v

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    resource_type: Optional[ResourceType] = None
    quantity: Optional[float] = Field(None, gt=0)
    unit_of_measure: Optional[str] = None
    availability: Optional[float] = Field(None, ge=0, le=100)
    location: Optional[str] = None
    deployment_status: Optional[DeploymentStatus] = None
    criticality: Optional[Criticality] = None
    strategic_importance: Optional[StrategicImportance] = None
    business_value: Optional[BusinessValue] = None
    cost_per_unit: Optional[float] = None
    total_cost: Optional[float] = None
    budget_allocation: Optional[float] = None
    cost_center: Optional[str] = None
    skills_required: Optional[str] = None
    capabilities_provided: Optional[str] = None
    expertise_level: Optional[ExpertiseLevel] = None
    performance_metrics: Optional[str] = None
    utilization_rate: Optional[float] = Field(None, ge=0, le=100)
    efficiency_score: Optional[float] = Field(None, ge=0, le=1)
    effectiveness_score: Optional[float] = Field(None, ge=0, le=1)
    operational_hours: Optional[OperationalHours] = None
    maintenance_schedule: Optional[str] = None
    technology_stack: Optional[str] = None
    system_requirements: Optional[str] = None
    integration_points: Optional[str] = None
    dependencies: Optional[str] = None
    governance_model: Optional[GovernanceModel] = None
    compliance_requirements: Optional[str] = None
    audit_requirements: Optional[str] = None
    risk_assessment: Optional[str] = None
    parent_resource_id: Optional[UUID] = None
    associated_capability_id: Optional[UUID] = None
    business_function_id: Optional[UUID] = None
    application_component_id: Optional[UUID] = None
    node_id: Optional[UUID] = None

class Resource(ResourceBase):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    allocated_quantity: float = 0.0
    available_quantity: float = 1.0
    last_maintenance: Optional[datetime] = None
    next_maintenance: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Resource Link schemas
class ResourceLinkBase(BaseModel):
    linked_element_id: UUID
    linked_element_type: str = Field(..., min_length=1, max_length=100)
    link_type: LinkType
    relationship_strength: RelationshipStrength = RelationshipStrength.MEDIUM
    dependency_level: DependencyLevel = DependencyLevel.MEDIUM
    allocation_percentage: float = Field(0.0, ge=0, le=100)
    allocation_start_date: Optional[datetime] = None
    allocation_end_date: Optional[datetime] = None
    allocation_priority: AllocationPriority = AllocationPriority.NORMAL
    interaction_frequency: InteractionFrequency = InteractionFrequency.REGULAR
    interaction_type: InteractionType = InteractionType.SYNCHRONOUS
    data_flow_direction: DataFlowDirection = DataFlowDirection.BIDIRECTIONAL
    performance_impact: PerformanceImpact = PerformanceImpact.LOW
    efficiency_contribution: Optional[float] = None
    effectiveness_contribution: Optional[float] = None

    @validator('allocation_percentage')
    def validate_allocation_percentage(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Allocation percentage must be between 0 and 100')
        return v

    @validator('efficiency_contribution', 'effectiveness_contribution')
    def validate_contributions(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Contributions must be between 0 and 100')
        return v

class ResourceLinkCreate(ResourceLinkBase):
    pass

class ResourceLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=100)
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    allocation_percentage: Optional[float] = Field(None, ge=0, le=100)
    allocation_start_date: Optional[datetime] = None
    allocation_end_date: Optional[datetime] = None
    allocation_priority: Optional[AllocationPriority] = None
    interaction_frequency: Optional[InteractionFrequency] = None
    interaction_type: Optional[InteractionType] = None
    data_flow_direction: Optional[DataFlowDirection] = None
    performance_impact: Optional[PerformanceImpact] = None
    efficiency_contribution: Optional[float] = None
    effectiveness_contribution: Optional[float] = None

class ResourceLink(ResourceLinkBase):
    id: UUID
    resource_id: UUID
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Analysis and impact schemas
class ImpactScore(BaseModel):
    resource_id: UUID
    strategic_impact_score: float
    operational_impact_score: float
    financial_impact_score: float
    risk_impact_score: float
    overall_impact_score: float
    impact_factors: List[Dict[str, Any]]
    recommendations: List[str]

class AllocationMap(BaseModel):
    resource_id: UUID
    total_allocated: float
    allocation_breakdown: List[Dict[str, Any]]
    utilization_analysis: Dict[str, Any]
    capacity_planning: Dict[str, Any]
    optimization_opportunities: List[str]
    allocation_metrics: Dict[str, Any]

class ResourceAnalysis(BaseModel):
    resource_id: UUID
    performance_analysis: Dict[str, Any]
    cost_analysis: Dict[str, Any]
    utilization_analysis: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    optimization_recommendations: List[str]
    strategic_alignment: Dict[str, Any]

# Domain-specific schemas
class ResourceByType(BaseModel):
    resource_type: ResourceType
    count: int
    resources: List[Resource]

class ResourceByStatus(BaseModel):
    deployment_status: DeploymentStatus
    count: int
    resources: List[Resource]

class ResourceByCapability(BaseModel):
    capability_id: UUID
    capability_name: str
    count: int
    resources: List[Resource]

class ResourceByPerformance(BaseModel):
    performance_category: str
    count: int
    resources: List[Resource]

# Response schemas for specific queries
class ResourceByElement(BaseModel):
    element_type: str
    element_id: UUID
    element_name: str
    resources: List[Resource]

class ResourceSummary(BaseModel):
    total_resources: int
    active_resources: int
    critical_resources: int
    resources_by_type: Dict[str, int]
    resources_by_status: Dict[str, int]
    average_utilization: float
    total_cost: float
    allocation_rate: float 