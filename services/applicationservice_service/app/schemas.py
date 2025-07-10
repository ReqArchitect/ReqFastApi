from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum

class ServiceType(str, Enum):
    UI = "ui"
    API = "api"
    DATA = "data"
    INTEGRATION = "integration"
    MESSAGING = "messaging"

class ServiceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    PLANNED = "planned"
    MAINTENANCE = "maintenance"

class DeliveryChannel(str, Enum):
    HTTP = "http"
    HTTPS = "https"
    GRPC = "grpc"
    WEBSOCKET = "websocket"
    MESSAGE_QUEUE = "message_queue"
    FILE_TRANSFER = "file_transfer"

class AuthenticationMethod(str, Enum):
    NONE = "none"
    BASIC = "basic"
    OAUTH = "oauth"
    JWT = "jwt"
    API_KEY = "api_key"

class DeploymentModel(str, Enum):
    MONOLITHIC = "monolithic"
    MICROSERVICE = "microservice"
    SERVERLESS = "serverless"
    CONTAINER = "container"

class ScalingStrategy(str, Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    AUTO = "auto"

class SecurityLevel(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    HIGH = "high"
    CRITICAL = "critical"

class DataClassification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class BusinessValue(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BusinessCriticality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class LinkType(str, Enum):
    REALIZES = "realizes"
    SUPPORTS = "supports"
    ENABLES = "enables"
    CONSUMES = "consumes"
    PRODUCES = "produces"
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
class ApplicationServiceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the application service")
    description: Optional[str] = Field(None, max_length=2000, description="Description of the application service")
    service_type: ServiceType = Field(ServiceType.API, description="Type of application service")
    exposed_function_id: Optional[UUID] = Field(None, description="ID of the exposed application function")
    exposed_dataobject_id: Optional[UUID] = Field(None, description="ID of the exposed data object")
    status: ServiceStatus = Field(ServiceStatus.ACTIVE, description="Current status of the service")
    latency_target_ms: int = Field(200, ge=1, le=30000, description="Target latency in milliseconds")
    availability_target_pct: float = Field(99.9, ge=0.0, le=100.0, description="Target availability percentage")
    consumer_role_id: Optional[UUID] = Field(None, description="ID of the consumer business role")
    version: str = Field(default="1.0.0", pattern=r"^\d+\.\d+\.\d+$", description="Semantic version")
    delivery_channel: DeliveryChannel = Field(DeliveryChannel.HTTP, description="Delivery channel for the service")
    
    # Service configuration
    service_endpoint: Optional[str] = Field(None, max_length=500, description="URL or endpoint for the service")
    authentication_method: AuthenticationMethod = Field(AuthenticationMethod.NONE, description="Authentication method")
    rate_limiting: Optional[str] = Field(None, description="JSON string of rate limiting configuration")
    caching_strategy: Optional[str] = Field(None, description="JSON string of caching configuration")
    load_balancing: Optional[str] = Field(None, description="JSON string of load balancing configuration")
    
    # Business context
    business_process_id: Optional[UUID] = Field(None, description="ID of the associated business process")
    capability_id: Optional[UUID] = Field(None, description="ID of the associated capability")
    business_value: BusinessValue = Field(BusinessValue.MEDIUM, description="Business value level")
    business_criticality: BusinessCriticality = Field(BusinessCriticality.MEDIUM, description="Business criticality level")
    
    # Technical specifications
    technology_stack: Optional[str] = Field(None, description="JSON string of technology stack")
    deployment_model: DeploymentModel = Field(DeploymentModel.MONOLITHIC, description="Deployment model")
    scaling_strategy: ScalingStrategy = Field(ScalingStrategy.HORIZONTAL, description="Scaling strategy")
    backup_strategy: Optional[str] = Field(None, description="JSON string of backup configuration")
    
    # Security and compliance
    security_level: SecurityLevel = Field(SecurityLevel.STANDARD, description="Security level")
    compliance_requirements: Optional[str] = Field(None, description="JSON string of compliance requirements")
    data_classification: DataClassification = Field(DataClassification.INTERNAL, description="Data classification level")
    encryption_requirements: Optional[str] = Field(None, description="JSON string of encryption requirements")
    
    # Documentation and support
    documentation_link: Optional[str] = Field(None, max_length=500, description="URL to documentation")
    api_documentation: Optional[str] = Field(None, description="JSON string of API documentation")
    support_contact: Optional[str] = Field(None, max_length=255, description="Support contact information")
    maintenance_window: Optional[str] = Field(None, max_length=255, description="Maintenance window schedule")

class ApplicationServiceCreate(ApplicationServiceBase):
    pass

class ApplicationServiceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    service_type: Optional[ServiceType] = None
    exposed_function_id: Optional[UUID] = None
    exposed_dataobject_id: Optional[UUID] = None
    status: Optional[ServiceStatus] = None
    latency_target_ms: Optional[int] = Field(None, ge=1, le=30000)
    availability_target_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    consumer_role_id: Optional[UUID] = None
    version: Optional[str] = Field(None, pattern=r"^\d+\.\d+\.\d+$")
    delivery_channel: Optional[DeliveryChannel] = None
    service_endpoint: Optional[str] = Field(None, max_length=500)
    authentication_method: Optional[AuthenticationMethod] = None
    rate_limiting: Optional[str] = None
    caching_strategy: Optional[str] = None
    load_balancing: Optional[str] = None
    business_process_id: Optional[UUID] = None
    capability_id: Optional[UUID] = None
    business_value: Optional[BusinessValue] = None
    business_criticality: Optional[BusinessCriticality] = None
    technology_stack: Optional[str] = None
    deployment_model: Optional[DeploymentModel] = None
    scaling_strategy: Optional[ScalingStrategy] = None
    backup_strategy: Optional[str] = None
    security_level: Optional[SecurityLevel] = None
    compliance_requirements: Optional[str] = None
    data_classification: Optional[DataClassification] = None
    encryption_requirements: Optional[str] = None
    documentation_link: Optional[str] = Field(None, max_length=500)
    api_documentation: Optional[str] = None
    support_contact: Optional[str] = Field(None, max_length=255)
    maintenance_window: Optional[str] = Field(None, max_length=255)

class ApplicationServiceResponse(ApplicationServiceBase):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    current_latency_ms: Optional[int] = None
    current_availability_pct: Optional[float] = None
    uptime_percentage: Optional[float] = None
    error_rate: Optional[float] = None
    throughput_rps: Optional[float] = None
    dependencies: Optional[str] = None
    required_services: Optional[str] = None
    optional_services: Optional[str] = None
    last_deployment: Optional[datetime] = None
    next_deployment: Optional[datetime] = None
    incident_count: int = 0
    last_incident: Optional[datetime] = None
    sla_breaches: int = 0
    response_time_p95: Optional[int] = None
    response_time_p99: Optional[int] = None
    success_rate: Optional[float] = None
    user_satisfaction: Optional[float] = None
    monthly_cost: Optional[float] = None
    resource_utilization: Optional[float] = None
    capacity_planning: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ServiceLinkBase(BaseModel):
    linked_element_id: UUID = Field(..., description="ID of the linked element")
    linked_element_type: str = Field(..., min_length=1, max_length=50, description="Type of the linked element")
    link_type: LinkType = Field(..., description="Type of relationship")
    relationship_strength: RelationshipStrength = Field(RelationshipStrength.MEDIUM, description="Strength of the relationship")
    dependency_level: DependencyLevel = Field(DependencyLevel.MEDIUM, description="Level of dependency")
    interaction_frequency: InteractionFrequency = Field(InteractionFrequency.REGULAR, description="Frequency of interaction")
    interaction_type: InteractionType = Field(InteractionType.SYNCHRONOUS, description="Type of interaction")
    data_flow_direction: DataFlowDirection = Field(DataFlowDirection.BIDIRECTIONAL, description="Direction of data flow")
    performance_impact: PerformanceImpact = Field(PerformanceImpact.MEDIUM, description="Impact on performance")
    latency_contribution: Optional[float] = Field(None, ge=0.0, description="Latency contribution in milliseconds")
    availability_impact: Optional[float] = Field(None, ge=0.0, le=100.0, description="Availability impact percentage")
    throughput_impact: Optional[float] = Field(None, ge=0.0, description="Throughput impact percentage")
    error_propagation: Optional[float] = Field(None, ge=0.0, le=100.0, description="Error propagation percentage")
    business_criticality: BusinessCriticality = Field(BusinessCriticality.MEDIUM, description="Business criticality level")
    business_value: BusinessValue = Field(BusinessValue.MEDIUM, description="Business value level")
    alignment_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Alignment score (0.0 to 1.0)")
    implementation_priority: str = Field("normal", description="Implementation priority")
    implementation_phase: str = Field("active", description="Implementation phase")
    resource_allocation: Optional[float] = Field(None, ge=0.0, le=100.0, description="Percentage of resources allocated")
    risk_level: str = Field("medium", description="Risk level")
    reliability_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Reliability score (0.0 to 1.0)")
    failure_impact: str = Field("medium", description="Impact of failure")
    recovery_time: Optional[int] = Field(None, ge=0, description="Recovery time in minutes")
    monitoring_enabled: bool = Field(True, description="Whether monitoring is enabled")
    alerting_enabled: bool = Field(True, description="Whether alerting is enabled")
    logging_level: str = Field("info", description="Logging level")
    metrics_collection: Optional[str] = Field(None, description="JSON string of metrics configuration")
    security_requirements: Optional[str] = Field(None, description="JSON string of security requirements")
    compliance_impact: str = Field("low", description="Compliance impact level")
    data_protection: Optional[str] = Field(None, description="JSON string of data protection requirements")
    performance_contribution: Optional[float] = Field(None, ge=0.0, le=100.0, description="Percentage contribution to overall performance")
    success_contribution: Optional[float] = Field(None, ge=0.0, le=100.0, description="Percentage contribution to success criteria")
    quality_metrics: Optional[str] = Field(None, description="JSON string of quality metrics")

class ServiceLinkCreate(ServiceLinkBase):
    pass

class ServiceLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=50)
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    interaction_frequency: Optional[InteractionFrequency] = None
    interaction_type: Optional[InteractionType] = None
    data_flow_direction: Optional[DataFlowDirection] = None
    performance_impact: Optional[PerformanceImpact] = None
    latency_contribution: Optional[float] = Field(None, ge=0.0)
    availability_impact: Optional[float] = Field(None, ge=0.0, le=100.0)
    throughput_impact: Optional[float] = Field(None, ge=0.0)
    error_propagation: Optional[float] = Field(None, ge=0.0, le=100.0)
    business_criticality: Optional[BusinessCriticality] = None
    business_value: Optional[BusinessValue] = None
    alignment_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    implementation_priority: Optional[str] = None
    implementation_phase: Optional[str] = None
    resource_allocation: Optional[float] = Field(None, ge=0.0, le=100.0)
    risk_level: Optional[str] = None
    reliability_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    failure_impact: Optional[str] = None
    recovery_time: Optional[int] = Field(None, ge=0)
    monitoring_enabled: Optional[bool] = None
    alerting_enabled: Optional[bool] = None
    logging_level: Optional[str] = None
    metrics_collection: Optional[str] = None
    security_requirements: Optional[str] = None
    compliance_impact: Optional[str] = None
    data_protection: Optional[str] = None
    performance_contribution: Optional[float] = Field(None, ge=0.0, le=100.0)
    success_contribution: Optional[float] = Field(None, ge=0.0, le=100.0)
    quality_metrics: Optional[str] = None

class ServiceLinkResponse(ServiceLinkBase):
    id: UUID
    application_service_id: UUID
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Analysis and impact schemas
class ImpactMapResponse(BaseModel):
    service_id: UUID
    direct_impacts: List[Dict[str, Any]]
    indirect_impacts: List[Dict[str, Any]]
    risk_assessment: Dict[str, Any]
    dependency_chain: List[Dict[str, Any]]
    total_impact_score: float

class PerformanceScoreResponse(BaseModel):
    service_id: UUID
    latency_score: float
    availability_score: float
    throughput_score: float
    overall_score: float
    recommendations: List[str]
    performance_metrics: Dict[str, Any]

class ServiceAnalysisResponse(BaseModel):
    service_id: UUID
    operational_health: Dict[str, Any]
    business_alignment: Dict[str, Any]
    technical_debt: Dict[str, Any]
    risk_factors: List[Dict[str, Any]]
    improvement_opportunities: List[str]
    compliance_status: Dict[str, Any]

# Enumeration schemas
class EnumerationResponse(BaseModel):
    values: List[str]

# Pagination and filtering
class ApplicationServiceListResponse(BaseModel):
    services: List[ApplicationServiceResponse]
    total: int
    skip: int
    limit: int

class ServiceLinkListResponse(BaseModel):
    links: List[ServiceLinkResponse]
    total: int
    skip: int
    limit: int 