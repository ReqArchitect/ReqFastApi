from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum

class NodeType(str, Enum):
    VM = "vm"
    CONTAINER = "container"
    PHYSICAL = "physical"
    CLOUD = "cloud"
    EDGE = "edge"

class Environment(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
    TESTING = "testing"

class LifecycleState(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    DECOMMISSIONED = "decommissioned"
    PLANNED = "planned"

class SecurityLevel(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    HIGH = "high"
    CRITICAL = "critical"

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
    HOSTS = "hosts"
    DEPLOYS = "deploys"
    COMMUNICATES_WITH = "communicates_with"
    DEPENDS_ON = "depends_on"
    MANAGES = "manages"

class RelationshipStrength(str, Enum):
    STRONG = "strong"
    MEDIUM = "medium"
    WEAK = "weak"

class DependencyLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class DeploymentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAILED = "failed"
    PENDING = "pending"

class CommunicationFrequency(str, Enum):
    FREQUENT = "frequent"
    REGULAR = "regular"
    OCCASIONAL = "occasional"
    RARE = "rare"

class CommunicationType(str, Enum):
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    BATCH = "batch"
    REAL_TIME = "real_time"

class PerformanceImpact(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Base schemas
class NodeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the node")
    description: Optional[str] = Field(None, max_length=2000, description="Description of the node")
    node_type: NodeType = Field(NodeType.VM, description="Type of node")
    environment: Environment = Field(Environment.PRODUCTION, description="Environment where the node is deployed")
    operating_system: Optional[str] = Field(None, max_length=100, description="Operating system")
    hardware_spec: Optional[str] = Field(None, description="JSON string of hardware specifications")
    region: Optional[str] = Field(None, max_length=100, description="Geographic region or data center")
    availability_zone: Optional[str] = Field(None, max_length=100, description="Cloud availability zone")
    cluster_id: Optional[UUID] = Field(None, description="ID of the cluster for container orchestration")
    host_capabilities: Optional[str] = Field(None, description="JSON string of host capabilities")
    deployed_components: Optional[str] = Field(None, description="JSON string of deployed application components")
    availability_target: float = Field(99.9, ge=0.0, le=100.0, description="Availability target percentage")
    lifecycle_state: LifecycleState = Field(LifecycleState.ACTIVE, description="Current lifecycle state")
    
    # Performance and monitoring
    cpu_cores: Optional[int] = Field(None, ge=1, description="Number of CPU cores")
    memory_gb: Optional[float] = Field(None, ge=0.1, description="Memory in GB")
    storage_gb: Optional[float] = Field(None, ge=0.1, description="Storage in GB")
    network_bandwidth_mbps: Optional[float] = Field(None, ge=0.1, description="Network bandwidth in Mbps")
    
    # Infrastructure details
    ip_address: Optional[str] = Field(None, max_length=45, description="Primary IP address")
    mac_address: Optional[str] = Field(None, max_length=17, description="MAC address")
    hostname: Optional[str] = Field(None, max_length=255, description="Hostname")
    domain: Optional[str] = Field(None, max_length=255, description="Domain name")
    subnet: Optional[str] = Field(None, max_length=100, description="Subnet information")
    gateway: Optional[str] = Field(None, max_length=45, description="Gateway address")
    dns_servers: Optional[str] = Field(None, description="JSON string of DNS servers")
    
    # Cloud-specific fields
    cloud_provider: Optional[str] = Field(None, max_length=50, description="Cloud provider")
    cloud_instance_id: Optional[str] = Field(None, max_length=255, description="Cloud instance identifier")
    cloud_instance_type: Optional[str] = Field(None, max_length=100, description="Cloud instance type")
    cloud_tags: Optional[str] = Field(None, description="JSON string of cloud tags")
    
    # Security and compliance
    security_level: SecurityLevel = Field(SecurityLevel.STANDARD, description="Security level")
    compliance_requirements: Optional[str] = Field(None, description="JSON string of compliance requirements")
    encryption_enabled: bool = Field(True, description="Whether encryption is enabled")
    backup_enabled: bool = Field(True, description="Whether backup is enabled")
    monitoring_enabled: bool = Field(True, description="Whether monitoring is enabled")
    
    # Operational details
    maintenance_window: Optional[str] = Field(None, max_length=255, description="Maintenance window schedule")
    
    # Cost and resource management
    monthly_cost: Optional[float] = Field(None, ge=0.0, description="Monthly operational cost")
    cost_center: Optional[str] = Field(None, max_length=100, description="Cost center assignment")
    resource_pool: Optional[str] = Field(None, max_length=100, description="Resource pool assignment")
    capacity_planning: Optional[str] = Field(None, description="JSON string of capacity planning data")
    
    # Network and connectivity
    network_interfaces: Optional[str] = Field(None, description="JSON string of network interfaces")
    firewall_rules: Optional[str] = Field(None, description="JSON string of firewall rules")
    load_balancer_config: Optional[str] = Field(None, description="JSON string of load balancer configuration")
    vpn_config: Optional[str] = Field(None, description="JSON string of VPN configuration")
    
    # Container and virtualization
    container_runtime: Optional[str] = Field(None, max_length=50, description="Container runtime")
    virtualization_type: Optional[str] = Field(None, max_length=50, description="Virtualization type")
    hypervisor: Optional[str] = Field(None, max_length=50, description="Hypervisor type")
    container_orchestrator: Optional[str] = Field(None, max_length=50, description="Container orchestrator")

class NodeCreate(NodeBase):
    pass

class NodeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    node_type: Optional[NodeType] = None
    environment: Optional[Environment] = None
    operating_system: Optional[str] = Field(None, max_length=100)
    hardware_spec: Optional[str] = None
    region: Optional[str] = Field(None, max_length=100)
    availability_zone: Optional[str] = Field(None, max_length=100)
    cluster_id: Optional[UUID] = None
    host_capabilities: Optional[str] = None
    deployed_components: Optional[str] = None
    availability_target: Optional[float] = Field(None, ge=0.0, le=100.0)
    lifecycle_state: Optional[LifecycleState] = None
    cpu_cores: Optional[int] = Field(None, ge=1)
    memory_gb: Optional[float] = Field(None, ge=0.1)
    storage_gb: Optional[float] = Field(None, ge=0.1)
    network_bandwidth_mbps: Optional[float] = Field(None, ge=0.1)
    ip_address: Optional[str] = Field(None, max_length=45)
    mac_address: Optional[str] = Field(None, max_length=17)
    hostname: Optional[str] = Field(None, max_length=255)
    domain: Optional[str] = Field(None, max_length=255)
    subnet: Optional[str] = Field(None, max_length=100)
    gateway: Optional[str] = Field(None, max_length=45)
    dns_servers: Optional[str] = None
    cloud_provider: Optional[str] = Field(None, max_length=50)
    cloud_instance_id: Optional[str] = Field(None, max_length=255)
    cloud_instance_type: Optional[str] = Field(None, max_length=100)
    cloud_tags: Optional[str] = None
    security_level: Optional[SecurityLevel] = None
    compliance_requirements: Optional[str] = None
    encryption_enabled: Optional[bool] = None
    backup_enabled: Optional[bool] = None
    monitoring_enabled: Optional[bool] = None
    maintenance_window: Optional[str] = Field(None, max_length=255)
    monthly_cost: Optional[float] = Field(None, ge=0.0)
    cost_center: Optional[str] = Field(None, max_length=100)
    resource_pool: Optional[str] = Field(None, max_length=100)
    capacity_planning: Optional[str] = None
    network_interfaces: Optional[str] = None
    firewall_rules: Optional[str] = None
    load_balancer_config: Optional[str] = None
    vpn_config: Optional[str] = None
    container_runtime: Optional[str] = Field(None, max_length=50)
    virtualization_type: Optional[str] = Field(None, max_length=50)
    hypervisor: Optional[str] = Field(None, max_length=50)
    container_orchestrator: Optional[str] = Field(None, max_length=50)

class NodeResponse(NodeBase):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    current_availability: Optional[float] = None
    resource_utilization: Optional[float] = None
    cpu_usage_pct: Optional[float] = None
    memory_usage_pct: Optional[float] = None
    storage_usage_pct: Optional[float] = None
    network_usage_pct: Optional[float] = None
    last_maintenance: Optional[datetime] = None
    next_maintenance: Optional[datetime] = None
    incident_count: int = 0
    last_incident: Optional[datetime] = None
    sla_breaches: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NodeLinkBase(BaseModel):
    linked_element_id: UUID = Field(..., description="ID of the linked element")
    linked_element_type: str = Field(..., min_length=1, max_length=50, description="Type of the linked element")
    link_type: LinkType = Field(..., description="Type of relationship")
    relationship_strength: RelationshipStrength = Field(RelationshipStrength.MEDIUM, description="Strength of the relationship")
    dependency_level: DependencyLevel = Field(DependencyLevel.MEDIUM, description="Level of dependency")
    deployment_status: DeploymentStatus = Field(DeploymentStatus.ACTIVE, description="Deployment status")
    deployment_version: Optional[str] = Field(None, max_length=50, description="Version of the deployed component")
    deployment_config: Optional[str] = Field(None, description="JSON string of deployment configuration")
    communication_protocol: Optional[str] = Field(None, max_length=20, description="Communication protocol")
    communication_port: Optional[int] = Field(None, ge=1, le=65535, description="Port number for communication")
    communication_frequency: CommunicationFrequency = Field(CommunicationFrequency.REGULAR, description="Frequency of communication")
    communication_type: CommunicationType = Field(CommunicationType.SYNCHRONOUS, description="Type of communication")
    performance_impact: PerformanceImpact = Field(PerformanceImpact.MEDIUM, description="Impact on performance")
    latency_contribution: Optional[float] = Field(None, ge=0.0, description="Latency contribution in milliseconds")
    bandwidth_usage: Optional[float] = Field(None, ge=0.0, description="Bandwidth usage in Mbps")
    resource_consumption: Optional[float] = Field(None, ge=0.0, le=100.0, description="Resource consumption percentage")
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

class NodeLinkCreate(NodeLinkBase):
    pass

class NodeLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=50)
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    deployment_status: Optional[DeploymentStatus] = None
    deployment_version: Optional[str] = Field(None, max_length=50)
    deployment_config: Optional[str] = None
    communication_protocol: Optional[str] = Field(None, max_length=20)
    communication_port: Optional[int] = Field(None, ge=1, le=65535)
    communication_frequency: Optional[CommunicationFrequency] = None
    communication_type: Optional[CommunicationType] = None
    performance_impact: Optional[PerformanceImpact] = None
    latency_contribution: Optional[float] = Field(None, ge=0.0)
    bandwidth_usage: Optional[float] = Field(None, ge=0.0)
    resource_consumption: Optional[float] = Field(None, ge=0.0, le=100.0)
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

class NodeLinkResponse(NodeLinkBase):
    id: UUID
    node_id: UUID
    deployment_date: Optional[datetime] = None
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Analysis and impact schemas
class DeploymentMapResponse(BaseModel):
    node_id: UUID
    deployed_components: List[Dict[str, Any]]
    deployment_status: Dict[str, Any]
    resource_allocation: Dict[str, Any]
    capacity_utilization: Dict[str, Any]
    deployment_health: Dict[str, Any]

class CapacityAnalysisResponse(BaseModel):
    node_id: UUID
    current_capacity: Dict[str, Any]
    projected_capacity: Dict[str, Any]
    capacity_recommendations: List[str]
    scaling_opportunities: List[str]
    resource_optimization: Dict[str, Any]

class NodeAnalysisResponse(BaseModel):
    node_id: UUID
    operational_health: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    resource_efficiency: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    improvement_opportunities: List[str]
    compliance_status: Dict[str, Any]

# Enumeration schemas
class EnumerationResponse(BaseModel):
    values: List[str]

# Pagination and filtering
class NodeListResponse(BaseModel):
    nodes: List[NodeResponse]
    total: int
    skip: int
    limit: int

class NodeLinkListResponse(BaseModel):
    links: List[NodeLinkResponse]
    total: int
    skip: int
    limit: int 