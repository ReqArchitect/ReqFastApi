from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum

class FunctionType(str, Enum):
    DATA_PROCESSING = "data_processing"
    ORCHESTRATION = "orchestration"
    USER_INTERACTION = "user_interaction"
    RULE_ENGINE = "rule_engine"
    ETL_PROCESSOR = "etl_processor"
    USER_SESSION_MANAGER = "user_session_manager"
    EVENT_HANDLER = "event_handler"
    UI_CONTROLLER = "ui_controller"

class BusinessCriticality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BusinessValue(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class FunctionStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    PLANNED = "planned"
    MAINTENANCE = "maintenance"

class OperationalHours(str, Enum):
    TWENTY_FOUR_SEVEN = "24x7"
    BUSINESS_HOURS = "business_hours"
    ON_DEMAND = "on_demand"

class SecurityLevel(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    HIGH = "high"
    CRITICAL = "critical"

class LinkType(str, Enum):
    REALIZES = "realizes"
    SUPPORTS = "supports"
    ENABLES = "enables"
    GOVERNS = "governs"
    INFLUENCES = "influences"
    CONSUMES = "consumes"
    PRODUCES = "produces"
    TRIGGERS = "triggers"

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
    EVENT_DRIVEN = "event_driven"

class DataFlowDirection(str, Enum):
    INPUT = "input"
    OUTPUT = "output"
    BIDIRECTIONAL = "bidirectional"

class PerformanceImpact(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Base schemas
class ApplicationFunctionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    purpose: Optional[str] = None
    technology_stack: Optional[str] = None
    module_location: Optional[str] = None
    function_type: FunctionType = FunctionType.DATA_PROCESSING
    performance_characteristics: Optional[str] = None
    response_time_target: Optional[float] = None
    throughput_target: Optional[float] = None
    availability_target: float = 99.9
    business_criticality: BusinessCriticality = BusinessCriticality.MEDIUM
    business_value: BusinessValue = BusinessValue.MEDIUM
    status: FunctionStatus = FunctionStatus.ACTIVE
    operational_hours: OperationalHours = OperationalHours.TWENTY_FOUR_SEVEN
    maintenance_window: Optional[str] = None
    api_endpoints: Optional[str] = None
    data_sources: Optional[str] = None
    data_sinks: Optional[str] = None
    error_handling: Optional[str] = None
    logging_config: Optional[str] = None
    security_level: SecurityLevel = SecurityLevel.STANDARD
    compliance_requirements: Optional[str] = None
    access_controls: Optional[str] = None
    audit_requirements: Optional[str] = None
    monitoring_config: Optional[str] = None
    alerting_rules: Optional[str] = None
    health_check_endpoint: Optional[str] = None
    metrics_endpoint: Optional[str] = None
    parent_function_id: Optional[UUID] = None
    application_service_id: Optional[UUID] = None
    data_object_id: Optional[UUID] = None
    node_id: Optional[UUID] = None
    supported_business_function_id: Optional[UUID] = None

class ApplicationFunctionCreate(ApplicationFunctionBase):
    pass

class ApplicationFunctionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    purpose: Optional[str] = None
    technology_stack: Optional[str] = None
    module_location: Optional[str] = None
    function_type: Optional[FunctionType] = None
    performance_characteristics: Optional[str] = None
    response_time_target: Optional[float] = None
    throughput_target: Optional[float] = None
    availability_target: Optional[float] = None
    business_criticality: Optional[BusinessCriticality] = None
    business_value: Optional[BusinessValue] = None
    status: Optional[FunctionStatus] = None
    operational_hours: Optional[OperationalHours] = None
    maintenance_window: Optional[str] = None
    api_endpoints: Optional[str] = None
    data_sources: Optional[str] = None
    data_sinks: Optional[str] = None
    error_handling: Optional[str] = None
    logging_config: Optional[str] = None
    security_level: Optional[SecurityLevel] = None
    compliance_requirements: Optional[str] = None
    access_controls: Optional[str] = None
    audit_requirements: Optional[str] = None
    monitoring_config: Optional[str] = None
    alerting_rules: Optional[str] = None
    health_check_endpoint: Optional[str] = None
    metrics_endpoint: Optional[str] = None
    parent_function_id: Optional[UUID] = None
    application_service_id: Optional[UUID] = None
    data_object_id: Optional[UUID] = None
    node_id: Optional[UUID] = None
    supported_business_function_id: Optional[UUID] = None

class ApplicationFunction(ApplicationFunctionBase):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    current_availability: float = 100.0
    last_maintenance: Optional[datetime] = None
    next_maintenance: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Function Link schemas
class FunctionLinkBase(BaseModel):
    linked_element_id: UUID
    linked_element_type: str = Field(..., min_length=1, max_length=100)
    link_type: LinkType
    relationship_strength: RelationshipStrength = RelationshipStrength.MEDIUM
    dependency_level: DependencyLevel = DependencyLevel.MEDIUM
    interaction_frequency: InteractionFrequency = InteractionFrequency.REGULAR
    interaction_type: InteractionType = InteractionType.SYNCHRONOUS
    data_flow_direction: DataFlowDirection = DataFlowDirection.BIDIRECTIONAL
    performance_impact: PerformanceImpact = PerformanceImpact.LOW
    latency_contribution: Optional[float] = None
    throughput_impact: Optional[float] = None

class FunctionLinkCreate(FunctionLinkBase):
    pass

class FunctionLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=100)
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    interaction_frequency: Optional[InteractionFrequency] = None
    interaction_type: Optional[InteractionType] = None
    data_flow_direction: Optional[DataFlowDirection] = None
    performance_impact: Optional[PerformanceImpact] = None
    latency_contribution: Optional[float] = None
    throughput_impact: Optional[float] = None

class FunctionLink(FunctionLinkBase):
    id: UUID
    application_function_id: UUID
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Analysis and impact schemas
class ImpactMap(BaseModel):
    function_id: UUID
    direct_impacts: List[Dict[str, Any]]
    indirect_impacts: List[Dict[str, Any]]
    risk_assessment: Dict[str, Any]
    dependency_chain: List[Dict[str, Any]]
    total_impact_score: float

class PerformanceScore(BaseModel):
    function_id: UUID
    response_time_score: float
    throughput_score: float
    availability_score: float
    overall_score: float
    recommendations: List[str]
    performance_metrics: Dict[str, Any]

class ApplicationFunctionAnalysis(BaseModel):
    function_id: UUID
    operational_health: Dict[str, Any]
    business_alignment: Dict[str, Any]
    technical_debt: Dict[str, Any]
    risk_factors: List[Dict[str, Any]]
    improvement_opportunities: List[str]
    compliance_status: Dict[str, Any]

# Domain-specific schemas
class ApplicationFunctionByType(BaseModel):
    function_type: FunctionType
    count: int
    functions: List[ApplicationFunction]

class ApplicationFunctionByStatus(BaseModel):
    status: FunctionStatus
    count: int
    functions: List[ApplicationFunction]

class ApplicationFunctionByBusinessFunction(BaseModel):
    business_function_id: UUID
    business_function_name: str
    count: int
    functions: List[ApplicationFunction]

class ApplicationFunctionByPerformance(BaseModel):
    performance_category: str
    count: int
    functions: List[ApplicationFunction]

# Response schemas for specific queries
class ApplicationFunctionByElement(BaseModel):
    element_type: str
    element_id: UUID
    element_name: str
    functions: List[ApplicationFunction]

class ApplicationFunctionSummary(BaseModel):
    total_functions: int
    active_functions: int
    critical_functions: int
    functions_by_type: Dict[str, int]
    functions_by_status: Dict[str, int]
    average_performance_score: float
    compliance_rate: float 