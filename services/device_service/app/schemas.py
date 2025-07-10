from pydantic import BaseModel, Field, validator, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums for Device
class DeviceType(str, Enum):
    SERVER = "server"
    MOBILE = "mobile"
    IOT = "iot"
    SENSOR = "sensor"
    ROUTER = "router"
    SWITCH = "switch"
    GATEWAY = "gateway"
    FIREWALL = "firewall"
    LOAD_BALANCER = "load_balancer"
    STORAGE_DEVICE = "storage_device"
    NETWORK_DEVICE = "network_device"
    SECURITY_DEVICE = "security_device"
    EDGE_DEVICE = "edge_device"
    INDUSTRIAL_DEVICE = "industrial_device"
    EMBEDDED_DEVICE = "embedded_device"

class SecurityLevel(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    HIGH = "high"
    CRITICAL = "critical"

class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    UNKNOWN = "unknown"
    PENDING = "pending"

class LifecycleState(str, Enum):
    PLANNING = "planning"
    DEVELOPMENT = "development"
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    DECOMMISSIONED = "decommissioned"

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    FAILED = "failed"
    DECOMMISSIONED = "decommissioned"

class DataClassification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

# Enums for DeviceLink
class LinkType(str, Enum):
    HOSTS = "hosts"
    SUPPORTS = "supports"
    CONNECTS = "connects"
    ENABLES = "enables"
    USES = "uses"
    DEPENDS_ON = "depends_on"
    COMMUNICATES_WITH = "communicates_with"

class RelationshipStrength(str, Enum):
    STRONG = "strong"
    MEDIUM = "medium"
    WEAK = "weak"

class DependencyLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class PerformanceImpact(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BusinessCriticality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ConnectionType(str, Enum):
    WIRED = "wired"
    WIRELESS = "wireless"
    FIBER = "fiber"
    ETHERNET = "ethernet"
    USB = "usb"
    SERIAL = "serial"
    PARALLEL = "parallel"

class ConnectionStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAILED = "failed"
    MAINTENANCE = "maintenance"

class ImplementationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAILED = "failed"
    PENDING = "pending"
    DEPRECATED = "deprecated"

class DeploymentStatus(str, Enum):
    DEPLOYED = "deployed"
    PENDING = "pending"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class LoggingLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

# Base schemas
class DeviceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Device name")
    description: Optional[str] = Field(None, max_length=1000, description="Device description")
    device_type: DeviceType = Field(..., description="Type of device")
    manufacturer: Optional[str] = Field(None, max_length=100, description="Device manufacturer")
    model_number: Optional[str] = Field(None, max_length=50, description="Model number")
    serial_number: Optional[str] = Field(None, max_length=100, description="Serial number")
    asset_tag: Optional[str] = Field(None, max_length=50, description="Asset tag")
    
    # Physical characteristics
    location: Optional[str] = Field(None, max_length=255, description="Physical location")
    rack_position: Optional[str] = Field(None, max_length=50, description="Rack position")
    room_number: Optional[str] = Field(None, max_length=50, description="Room number")
    building: Optional[str] = Field(None, max_length=100, description="Building name/number")
    floor: Optional[str] = Field(None, max_length=20, description="Floor number")
    data_center: Optional[str] = Field(None, max_length=100, description="Data center name")
    region: Optional[str] = Field(None, max_length=100, description="Geographic region")
    country: Optional[str] = Field(None, max_length=100, description="Country")
    timezone: Optional[str] = Field(None, max_length=50, description="Timezone")
    
    # Hardware specifications
    cpu_model: Optional[str] = Field(None, max_length=100, description="CPU model")
    cpu_cores: Optional[int] = Field(None, ge=0, description="Number of CPU cores")
    cpu_speed_ghz: Optional[float] = Field(None, ge=0, description="CPU speed in GHz")
    memory_gb: Optional[float] = Field(None, ge=0, description="Memory in GB")
    storage_gb: Optional[float] = Field(None, ge=0, description="Storage in GB")
    storage_type: Optional[str] = Field(None, max_length=50, description="Storage type")
    network_interfaces: Optional[str] = Field(None, description="JSON string of network interfaces")
    power_consumption_watts: Optional[float] = Field(None, ge=0, description="Power consumption in watts")
    weight_kg: Optional[float] = Field(None, ge=0, description="Weight in kilograms")
    dimensions: Optional[str] = Field(None, description="JSON string of dimensions")
    
    # Operating conditions
    operating_conditions: Optional[str] = Field(None, description="JSON string of operating conditions")
    temperature_range: Optional[str] = Field(None, max_length=100, description="Operating temperature range")
    humidity_range: Optional[str] = Field(None, max_length=100, description="Operating humidity range")
    power_requirements: Optional[str] = Field(None, max_length=200, description="Power requirements")
    cooling_requirements: Optional[str] = Field(None, max_length=200, description="Cooling requirements")
    
    # Software and firmware
    firmware_version: Optional[str] = Field(None, max_length=50, description="Current firmware version")
    firmware_date: Optional[datetime] = Field(None, description="Firmware installation date")
    operating_system: Optional[str] = Field(None, max_length=100, description="Operating system")
    os_version: Optional[str] = Field(None, max_length=50, description="OS version")
    os_install_date: Optional[datetime] = Field(None, description="OS installation date")
    software_inventory: Optional[str] = Field(None, description="JSON string of installed software")
    
    # Network configuration
    ip_addresses: Optional[str] = Field(None, description="JSON string of IP addresses")
    mac_addresses: Optional[str] = Field(None, description="JSON string of MAC addresses")
    hostname: Optional[str] = Field(None, max_length=100, description="Device hostname")
    domain: Optional[str] = Field(None, max_length=100, description="Domain name")
    dns_servers: Optional[str] = Field(None, description="JSON string of DNS servers")
    gateway_address: Optional[str] = Field(None, max_length=50, description="Gateway address")
    subnet_mask: Optional[str] = Field(None, max_length=50, description="Subnet mask")
    
    # Security configuration
    security_level: SecurityLevel = Field(SecurityLevel.STANDARD, description="Security level")
    encryption_enabled: bool = Field(False, description="Encryption enabled")
    encryption_type: Optional[str] = Field(None, max_length=50, description="Type of encryption")
    antivirus_installed: bool = Field(False, description="Antivirus installed")
    antivirus_version: Optional[str] = Field(None, max_length=50, description="Antivirus version")
    firewall_enabled: bool = Field(True, description="Firewall enabled")
    firewall_rules: Optional[str] = Field(None, description="JSON string of firewall rules")
    access_control_list: Optional[str] = Field(None, description="JSON string of ACL")
    
    # Maintenance and lifecycle
    maintenance_schedule: Optional[str] = Field(None, description="JSON string of maintenance schedule")
    last_maintenance: Optional[datetime] = Field(None, description="Last maintenance date")
    next_maintenance: Optional[datetime] = Field(None, description="Next scheduled maintenance")
    last_inspection_date: Optional[datetime] = Field(None, description="Last inspection date")
    next_inspection_date: Optional[datetime] = Field(None, description="Next inspection date")
    warranty_expiry: Optional[datetime] = Field(None, description="Warranty expiry date")
    support_contract: Optional[str] = Field(None, max_length=200, description="Support contract details")
    support_vendor: Optional[str] = Field(None, max_length=100, description="Support vendor")
    
    # Compliance and governance
    compliance_status: ComplianceStatus = Field(ComplianceStatus.UNKNOWN, description="Compliance status")
    compliance_requirements: Optional[str] = Field(None, description="JSON string of compliance requirements")
    audit_requirements: Optional[str] = Field(None, description="JSON string of audit requirements")
    data_classification: DataClassification = Field(DataClassification.INTERNAL, description="Data classification")
    retention_policy: Optional[str] = Field(None, description="JSON string of retention policy")
    
    # Performance monitoring
    performance_metrics: Optional[str] = Field(None, description="JSON string of performance metrics")
    cpu_utilization: Optional[float] = Field(None, ge=0, le=100, description="Current CPU utilization percentage")
    memory_utilization: Optional[float] = Field(None, ge=0, le=100, description="Current memory utilization percentage")
    disk_utilization: Optional[float] = Field(None, ge=0, le=100, description="Current disk utilization percentage")
    network_utilization: Optional[float] = Field(None, ge=0, le=100, description="Current network utilization percentage")
    temperature_celsius: Optional[float] = Field(None, ge=-50, le=100, description="Current temperature in Celsius")
    power_consumption_current: Optional[float] = Field(None, ge=0, description="Current power consumption in watts")
    
    # Availability and reliability
    availability_target_pct: float = Field(99.9, ge=0, le=100, description="Availability target percentage")
    current_availability: Optional[float] = Field(None, ge=0, le=100, description="Current availability percentage")
    uptime_pct: Optional[float] = Field(None, ge=0, le=100, description="Uptime percentage")
    mttf_hours: Optional[float] = Field(None, ge=0, description="Mean Time To Failure in hours")
    mttr_minutes: Optional[int] = Field(None, ge=0, description="Mean Time To Repair in minutes")
    incident_count: int = Field(0, ge=0, description="Number of incidents")
    last_incident: Optional[datetime] = Field(None, description="Last incident date")
    
    # Cost and licensing
    purchase_date: Optional[datetime] = Field(None, description="Purchase date")
    purchase_cost: Optional[float] = Field(None, ge=0, description="Purchase cost")
    current_value: Optional[float] = Field(None, ge=0, description="Current value")
    depreciation_rate: Optional[float] = Field(None, ge=0, le=100, description="Depreciation rate")
    license_cost: Optional[float] = Field(None, ge=0, description="Annual license cost")
    maintenance_cost: Optional[float] = Field(None, ge=0, description="Annual maintenance cost")
    power_cost_per_month: Optional[float] = Field(None, ge=0, description="Monthly power cost")
    
    # Environmental impact
    energy_efficiency_rating: Optional[str] = Field(None, max_length=50, description="Energy efficiency rating")
    carbon_footprint: Optional[float] = Field(None, ge=0, description="Carbon footprint in kg CO2")
    recyclable_materials: bool = Field(False, description="Recyclable materials")
    disposal_method: Optional[str] = Field(None, max_length=100, description="Disposal method")
    
    # Relationships
    supported_node_id: Optional[UUID4] = Field(None, description="Supported node ID")
    system_software_id: Optional[UUID4] = Field(None, description="System software ID")
    communication_path_id: Optional[UUID4] = Field(None, description="Communication path ID")
    artifact_id: Optional[UUID4] = Field(None, description="Associated artifact ID")
    
    # Status and lifecycle
    status: Status = Field(Status.ACTIVE, description="Device status")
    lifecycle_state: LifecycleState = Field(LifecycleState.OPERATIONAL, description="Lifecycle state")

    @validator('serial_number')
    def validate_serial_number(cls, v):
        if v and len(v) < 3:
            raise ValueError('Serial number must be at least 3 characters long')
        return v

    @validator('asset_tag')
    def validate_asset_tag(cls, v):
        if v and len(v) < 2:
            raise ValueError('Asset tag must be at least 2 characters long')
        return v

    @validator('cpu_cores', 'memory_gb', 'storage_gb')
    def validate_positive_values(cls, v):
        if v is not None and v < 0:
            raise ValueError('Value must be non-negative')
        return v

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    device_type: Optional[DeviceType] = None
    manufacturer: Optional[str] = Field(None, max_length=100)
    model_number: Optional[str] = Field(None, max_length=50)
    serial_number: Optional[str] = Field(None, max_length=100)
    asset_tag: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    status: Optional[Status] = None
    lifecycle_state: Optional[LifecycleState] = None
    security_level: Optional[SecurityLevel] = None
    compliance_status: Optional[ComplianceStatus] = None
    availability_target_pct: Optional[float] = Field(None, ge=0, le=100)
    current_availability: Optional[float] = Field(None, ge=0, le=100)

class DeviceResponse(DeviceBase):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DeviceListResponse(BaseModel):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    name: str
    device_type: DeviceType
    manufacturer: Optional[str]
    model_number: Optional[str]
    serial_number: Optional[str]
    asset_tag: Optional[str]
    location: Optional[str]
    status: Status
    lifecycle_state: LifecycleState
    security_level: SecurityLevel
    compliance_status: ComplianceStatus
    availability_target_pct: float
    current_availability: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# DeviceLink schemas
class DeviceLinkBase(BaseModel):
    linked_element_id: UUID4 = Field(..., description="Linked element ID")
    linked_element_type: str = Field(..., min_length=1, max_length=50, description="Linked element type")
    link_type: LinkType = Field(..., description="Type of link")
    relationship_strength: RelationshipStrength = Field(RelationshipStrength.MEDIUM, description="Relationship strength")
    dependency_level: DependencyLevel = Field(DependencyLevel.MEDIUM, description="Dependency level")
    
    # Physical connection context
    connection_type: Optional[ConnectionType] = Field(None, description="Connection type")
    connection_speed: Optional[float] = Field(None, ge=0, description="Connection speed in Mbps")
    connection_protocol: Optional[str] = Field(None, max_length=50, description="Connection protocol")
    connection_port: Optional[str] = Field(None, max_length=20, description="Connection port")
    connection_status: ConnectionStatus = Field(ConnectionStatus.ACTIVE, description="Connection status")
    
    # Performance impact
    performance_impact: PerformanceImpact = Field(PerformanceImpact.MEDIUM, description="Performance impact")
    resource_consumption: Optional[float] = Field(None, ge=0, le=100, description="Resource consumption percentage")
    bandwidth_usage: Optional[float] = Field(None, ge=0, description="Bandwidth usage in Mbps")
    latency_contribution: Optional[float] = Field(None, ge=0, description="Latency contribution in milliseconds")
    
    # Business context
    business_criticality: BusinessCriticality = Field(BusinessCriticality.MEDIUM, description="Business criticality")
    business_value: BusinessCriticality = Field(BusinessCriticality.MEDIUM, description="Business value")
    alignment_score: Optional[float] = Field(None, ge=0, le=1, description="Alignment score (0.0 to 1.0)")
    
    # Implementation context
    implementation_status: ImplementationStatus = Field(ImplementationStatus.ACTIVE, description="Implementation status")
    implementation_date: Optional[datetime] = Field(None, description="Implementation date")
    implementation_version: Optional[str] = Field(None, max_length=50, description="Implementation version")
    implementation_config: Optional[str] = Field(None, description="JSON string of implementation configuration")
    
    # Deployment context
    deployment_status: DeploymentStatus = Field(DeploymentStatus.DEPLOYED, description="Deployment status")
    deployment_date: Optional[datetime] = Field(None, description="Deployment date")
    deployment_environment: str = Field("production", max_length=50, description="Deployment environment")
    deployment_method: Optional[str] = Field(None, max_length=50, description="Deployment method")
    
    # Risk and reliability
    risk_level: RiskLevel = Field(RiskLevel.MEDIUM, description="Risk level")
    reliability_score: Optional[float] = Field(None, ge=0, le=1, description="Reliability score (0.0 to 1.0)")
    failure_impact: PerformanceImpact = Field(PerformanceImpact.MEDIUM, description="Failure impact")
    recovery_time: Optional[int] = Field(None, ge=0, description="Recovery time in minutes")
    
    # Monitoring and observability
    monitoring_enabled: bool = Field(True, description="Monitoring enabled")
    alerting_enabled: bool = Field(True, description="Alerting enabled")
    logging_level: LoggingLevel = Field(LoggingLevel.INFO, description="Logging level")
    metrics_collection: Optional[str] = Field(None, description="JSON string of metrics configuration")
    
    # Security and compliance
    security_requirements: Optional[str] = Field(None, description="JSON string of security requirements")
    compliance_impact: PerformanceImpact = Field(PerformanceImpact.LOW, description="Compliance impact")
    data_protection: Optional[str] = Field(None, description="JSON string of data protection requirements")
    
    # Performance tracking
    performance_contribution: Optional[float] = Field(None, ge=0, le=100, description="Performance contribution percentage")
    success_contribution: Optional[float] = Field(None, ge=0, le=100, description="Success contribution percentage")
    quality_metrics: Optional[str] = Field(None, description="JSON string of quality metrics")

class DeviceLinkCreate(DeviceLinkBase):
    pass

class DeviceLinkUpdate(BaseModel):
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    connection_status: Optional[ConnectionStatus] = None
    performance_impact: Optional[PerformanceImpact] = None
    business_criticality: Optional[BusinessCriticality] = None
    implementation_status: Optional[ImplementationStatus] = None
    deployment_status: Optional[DeploymentStatus] = None
    risk_level: Optional[RiskLevel] = None
    monitoring_enabled: Optional[bool] = None
    alerting_enabled: Optional[bool] = None

class DeviceLinkResponse(DeviceLinkBase):
    id: UUID4
    device_id: UUID4
    created_by: UUID4
    created_at: datetime

    class Config:
        from_attributes = True

# Analysis response schemas
class DeploymentMapResponse(BaseModel):
    device_id: UUID4
    device_name: str
    device_type: DeviceType
    deployment_nodes: List[Dict[str, Any]]
    supported_software: List[Dict[str, Any]]
    communication_paths: List[Dict[str, Any]]
    artifacts: List[Dict[str, Any]]
    deployment_score: float
    recommendations: List[str]

class ComplianceStatusResponse(BaseModel):
    device_id: UUID4
    device_name: str
    compliance_status: ComplianceStatus
    compliance_score: float
    compliance_items: List[Dict[str, Any]]
    non_compliant_items: List[Dict[str, Any]]
    recommendations: List[str]
    last_audit_date: Optional[datetime]
    next_audit_date: Optional[datetime]

# Enumeration response schemas
class EnumerationResponse(BaseModel):
    values: List[str]
    count: int 