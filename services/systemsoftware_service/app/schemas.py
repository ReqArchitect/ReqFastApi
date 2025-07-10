from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum

class SoftwareType(str, Enum):
    OS = "os"
    DATABASE = "database"
    MIDDLEWARE = "middleware"
    RUNTIME = "runtime"
    CONTAINER_ENGINE = "container_engine"

class LicenseType(str, Enum):
    PROPRIETARY = "proprietary"
    OPEN_SOURCE = "open_source"
    COMMERCIAL = "commercial"
    FREEWARE = "freeware"

class LifecycleState(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    END_OF_LIFE = "end_of_life"
    PLANNED = "planned"

class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    UNKNOWN = "unknown"
    PENDING = "pending"

class UpdateChannel(str, Enum):
    STABLE = "stable"
    BETA = "beta"
    ALPHA = "alpha"
    LTS = "lts"

class UpdateFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class DeploymentEnvironment(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
    TESTING = "testing"

class SupportLevel(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class LinkType(str, Enum):
    RUNS_ON = "runs_on"
    DEPENDS_ON = "depends_on"
    INTEGRATES_WITH = "integrates_with"
    MANAGES = "manages"
    SUPPORTS = "supports"

class RelationshipStrength(str, Enum):
    STRONG = "strong"
    MEDIUM = "medium"
    WEAK = "weak"

class DependencyLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class IntegrationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAILED = "failed"
    PENDING = "pending"
    DEPRECATED = "deprecated"

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

# Base schemas
class SystemSoftwareBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the system software")
    description: Optional[str] = Field(None, max_length=2000, description="Description of the system software")
    software_type: SoftwareType = Field(SoftwareType.OS, description="Type of system software")
    version: str = Field(..., min_length=1, max_length=50, description="Version of the software")
    vendor: Optional[str] = Field(None, max_length=100, description="Software vendor")
    license_type: LicenseType = Field(LicenseType.PROPRIETARY, description="Type of license")
    supported_node_id: Optional[UUID] = Field(None, description="ID of the node that hosts this software")
    capabilities_provided: Optional[str] = Field(None, description="JSON string of capabilities provided")
    compliance_certifications: Optional[str] = Field(None, description="JSON string of compliance certifications")
    lifecycle_state: LifecycleState = Field(LifecycleState.ACTIVE, description="Current lifecycle state")
    
    # Security and compliance
    vulnerability_score: Optional[float] = Field(None, ge=0.0, le=10.0, description="CVSS vulnerability score")
    security_patches_available: bool = Field(False, description="Whether security patches are available")
    compliance_status: ComplianceStatus = Field(ComplianceStatus.UNKNOWN, description="Compliance status")
    
    # Update and maintenance
    update_channel: UpdateChannel = Field(UpdateChannel.STABLE, description="Update channel")
    auto_update_enabled: bool = Field(True, description="Whether auto-update is enabled")
    update_frequency: UpdateFrequency = Field(UpdateFrequency.MONTHLY, description="Update frequency")
    
    # Performance and monitoring
    resource_usage: Optional[float] = Field(None, ge=0.0, le=100.0, description="Current resource usage percentage")
    uptime_percentage: Optional[float] = Field(None, ge=0.0, le=100.0, description="Uptime percentage")
    response_time_avg: Optional[float] = Field(None, ge=0.0, description="Average response time in milliseconds")
    
    # Configuration and deployment
    configuration: Optional[str] = Field(None, description="JSON string of configuration")
    deployment_environment: DeploymentEnvironment = Field(DeploymentEnvironment.PRODUCTION, description="Deployment environment")
    deployment_method: Optional[str] = Field(None, max_length=50, description="Deployment method")
    
    # Dependencies and relationships
    dependencies: Optional[str] = Field(None, description="JSON string of software dependencies")
    dependent_components: Optional[str] = Field(None, description="JSON string of components that depend on this software")
    integration_points: Optional[str] = Field(None, description="JSON string of integration points")
    
    # Licensing and cost
    license_cost: Optional[float] = Field(None, ge=0.0, description="Annual license cost")
    license_seats: Optional[int] = Field(None, ge=0, description="Number of licensed seats/users")
    license_usage: Optional[int] = Field(None, ge=0, description="Current license usage")
    
    # Documentation and support
    documentation_url: Optional[str] = Field(None, max_length=500, description="Documentation URL")
    support_contact: Optional[str] = Field(None, max_length=200, description="Support contact")
    support_level: SupportLevel = Field(SupportLevel.STANDARD, description="Support level")
    
    # Backup and recovery
    backup_enabled: bool = Field(True, description="Whether backup is enabled")
    backup_frequency: str = Field("daily", description="Backup frequency")
    backup_retention_days: int = Field(30, ge=1, description="Backup retention in days")
    disaster_recovery_plan: Optional[str] = Field(None, description="JSON string of DR plan")
    
    # Monitoring and alerting
    monitoring_enabled: bool = Field(True, description="Whether monitoring is enabled")
    alerting_enabled: bool = Field(True, description="Whether alerting is enabled")
    monitoring_endpoints: Optional[str] = Field(None, description="JSON string of monitoring endpoints")
    alerting_rules: Optional[str] = Field(None, description="JSON string of alerting rules")
    
    # Operational details
    maintenance_window: Optional[str] = Field(None, max_length=255, description="Maintenance window schedule")
    
    # Performance characteristics
    cpu_requirements: Optional[float] = Field(None, ge=0.1, description="CPU requirements in cores")
    memory_requirements: Optional[float] = Field(None, ge=0.1, description="Memory requirements in GB")
    storage_requirements: Optional[float] = Field(None, ge=0.1, description="Storage requirements in GB")
    network_requirements: Optional[float] = Field(None, ge=0.1, description="Network requirements in Mbps")
    
    # Scalability and capacity
    max_concurrent_users: Optional[int] = Field(None, ge=1, description="Maximum concurrent users")
    max_data_volume: Optional[float] = Field(None, ge=0.1, description="Maximum data volume in GB")
    scalability_limits: Optional[str] = Field(None, description="JSON string of scalability limits")
    capacity_planning: Optional[str] = Field(None, description="JSON string of capacity planning data")

class SystemSoftwareCreate(SystemSoftwareBase):
    pass

class SystemSoftwareUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    software_type: Optional[SoftwareType] = None
    version: Optional[str] = Field(None, min_length=1, max_length=50)
    vendor: Optional[str] = Field(None, max_length=100)
    license_type: Optional[LicenseType] = None
    supported_node_id: Optional[UUID] = None
    capabilities_provided: Optional[str] = None
    compliance_certifications: Optional[str] = None
    lifecycle_state: Optional[LifecycleState] = None
    vulnerability_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    security_patches_available: Optional[bool] = None
    compliance_status: Optional[ComplianceStatus] = None
    update_channel: Optional[UpdateChannel] = None
    auto_update_enabled: Optional[bool] = None
    update_frequency: Optional[UpdateFrequency] = None
    resource_usage: Optional[float] = Field(None, ge=0.0, le=100.0)
    uptime_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    response_time_avg: Optional[float] = Field(None, ge=0.0)
    configuration: Optional[str] = None
    deployment_environment: Optional[DeploymentEnvironment] = None
    deployment_method: Optional[str] = Field(None, max_length=50)
    dependencies: Optional[str] = None
    dependent_components: Optional[str] = None
    integration_points: Optional[str] = None
    license_cost: Optional[float] = Field(None, ge=0.0)
    license_seats: Optional[int] = Field(None, ge=0)
    license_usage: Optional[int] = Field(None, ge=0)
    documentation_url: Optional[str] = Field(None, max_length=500)
    support_contact: Optional[str] = Field(None, max_length=200)
    support_level: Optional[SupportLevel] = None
    backup_enabled: Optional[bool] = None
    backup_frequency: Optional[str] = None
    backup_retention_days: Optional[int] = Field(None, ge=1)
    disaster_recovery_plan: Optional[str] = None
    monitoring_enabled: Optional[bool] = None
    alerting_enabled: Optional[bool] = None
    monitoring_endpoints: Optional[str] = None
    alerting_rules: Optional[str] = None
    maintenance_window: Optional[str] = Field(None, max_length=255)
    cpu_requirements: Optional[float] = Field(None, ge=0.1)
    memory_requirements: Optional[float] = Field(None, ge=0.1)
    storage_requirements: Optional[float] = Field(None, ge=0.1)
    network_requirements: Optional[float] = Field(None, ge=0.1)
    max_concurrent_users: Optional[int] = Field(None, ge=1)
    max_data_volume: Optional[float] = Field(None, ge=0.1)
    scalability_limits: Optional[str] = None
    capacity_planning: Optional[str] = None

class SystemSoftwareResponse(SystemSoftwareBase):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    last_security_audit: Optional[datetime] = None
    last_patch_date: Optional[datetime] = None
    next_patch_date: Optional[datetime] = None
    performance_metrics: Optional[str] = None
    installation_date: Optional[datetime] = None
    last_maintenance: Optional[datetime] = None
    next_maintenance: Optional[datetime] = None
    incident_count: int = 0
    last_incident: Optional[datetime] = None
    data_retention_policy: Optional[str] = None
    access_controls: Optional[str] = None
    audit_requirements: Optional[str] = None
    regulatory_compliance: Optional[str] = None
    license_expiry: Optional[datetime] = None
    support_expiry: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SoftwareLinkBase(BaseModel):
    linked_element_id: UUID = Field(..., description="ID of the linked element")
    linked_element_type: str = Field(..., min_length=1, max_length=50, description="Type of the linked element")
    link_type: LinkType = Field(..., description="Type of relationship")
    relationship_strength: RelationshipStrength = Field(RelationshipStrength.MEDIUM, description="Strength of the relationship")
    dependency_level: DependencyLevel = Field(DependencyLevel.MEDIUM, description="Level of dependency")
    integration_status: IntegrationStatus = Field(IntegrationStatus.ACTIVE, description="Integration status")
    integration_version: Optional[str] = Field(None, max_length=50, description="Version of the integration")
    integration_config: Optional[str] = Field(None, description="JSON string of integration configuration")
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

class SoftwareLinkCreate(SoftwareLinkBase):
    pass

class SoftwareLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=50)
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    integration_status: Optional[IntegrationStatus] = None
    integration_version: Optional[str] = Field(None, max_length=50)
    integration_config: Optional[str] = None
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

class SoftwareLinkResponse(SoftwareLinkBase):
    id: UUID
    system_software_id: UUID
    integration_date: Optional[datetime] = None
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Analysis and impact schemas
class DependencyMapResponse(BaseModel):
    system_software_id: UUID
    dependencies: List[Dict[str, Any]]
    dependent_components: List[Dict[str, Any]]
    integration_points: List[Dict[str, Any]]
    dependency_health: Dict[str, Any]

class ComplianceCheckResponse(BaseModel):
    system_software_id: UUID
    compliance_status: Dict[str, Any]
    vulnerability_assessment: Dict[str, Any]
    certification_status: Dict[str, Any]
    compliance_recommendations: List[str]

class SystemSoftwareAnalysisResponse(BaseModel):
    system_software_id: UUID
    operational_health: Dict[str, Any]
    security_status: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    improvement_opportunities: List[str]
    compliance_status: Dict[str, Any]

# Enumeration schemas
class EnumerationResponse(BaseModel):
    values: List[str]

# Pagination and filtering
class SystemSoftwareListResponse(BaseModel):
    system_software: List[SystemSoftwareResponse]
    total: int
    skip: int
    limit: int

class SoftwareLinkListResponse(BaseModel):
    links: List[SoftwareLinkResponse]
    total: int
    skip: int
    limit: int 