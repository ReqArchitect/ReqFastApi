from pydantic import BaseModel, Field, validator, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums for validation
class ArtifactType(str, Enum):
    SOURCE = "source"
    BUILD = "build"
    IMAGE = "image"
    CONFIG = "config"
    SCRIPT = "script"
    BINARY = "binary"
    CONTAINER = "container"
    PACKAGE = "package"
    LIBRARY = "library"
    FRAMEWORK = "framework"

class LifecycleState(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    DELETED = "deleted"
    PLANNED = "planned"
    DEVELOPMENT = "development"
    TESTING = "testing"

class DeploymentEnvironment(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
    TESTING = "testing"
    SANDBOX = "sandbox"

class AccessLevel(str, Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    UNKNOWN = "unknown"
    PENDING = "pending"

class DataClassification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class DocumentationStatus(str, Enum):
    COMPLETE = "complete"
    INCOMPLETE = "incomplete"
    MISSING = "missing"

class OperationalHours(str, Enum):
    TWENTY_FOUR_SEVEN = "24x7"
    BUSINESS_HOURS = "business_hours"
    ON_DEMAND = "on_demand"

class LinkType(str, Enum):
    IMPLEMENTS = "implements"
    DEPLOYED_ON = "deployed_on"
    DEPENDS_ON = "depends_on"
    CONTAINS = "contains"
    CONFIGURES = "configures"
    SUPPORTS = "supports"
    ENABLES = "enables"
    GOVERNED_BY = "governed_by"

class RelationshipStrength(str, Enum):
    STRONG = "strong"
    MEDIUM = "medium"
    WEAK = "weak"

class DependencyLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

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

class BusinessCriticality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

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
class ArtifactBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Artifact name")
    description: Optional[str] = Field(None, max_length=1000, description="Artifact description")
    artifact_type: ArtifactType = Field(..., description="Type of artifact")
    version: str = Field(..., min_length=1, max_length=50, description="Version string")
    format: Optional[str] = Field(None, max_length=50, description="File format")
    storage_location: Optional[str] = Field(None, max_length=500, description="Storage location/path")
    checksum: Optional[str] = Field(None, max_length=128, description="Hash/checksum for integrity")
    build_tool: Optional[str] = Field(None, max_length=100, description="Tool used to build")
    deployment_target_node_id: Optional[UUID4] = Field(None, description="Node where artifact is deployed")
    associated_component_id: Optional[UUID4] = Field(None, description="Associated application component")
    lifecycle_state: LifecycleState = Field(LifecycleState.ACTIVE, description="Lifecycle state")
    size_mb: Optional[float] = Field(None, ge=0, le=1000000, description="Size in megabytes")
    file_count: Optional[int] = Field(None, ge=0, description="Number of files in artifact")
    compression_ratio: Optional[float] = Field(None, ge=0, le=1, description="Compression ratio")
    deployment_environment: DeploymentEnvironment = Field(DeploymentEnvironment.PRODUCTION, description="Deployment environment")
    integrity_verified: bool = Field(False, description="Whether integrity is verified")
    security_scan_passed: bool = Field(True, description="Whether security scan passed")
    vulnerability_count: int = Field(0, ge=0, description="Number of vulnerabilities")
    security_score: Optional[float] = Field(None, ge=0, le=10, description="Security score (0-10)")
    dependencies: Optional[str] = Field(None, description="JSON string of artifact dependencies")
    dependent_artifacts: Optional[str] = Field(None, description="JSON string of dependent artifacts")
    build_dependencies: Optional[str] = Field(None, description="JSON string of build-time dependencies")
    configuration: Optional[str] = Field(None, description="JSON string of configuration")
    metadata: Optional[str] = Field(None, description="JSON string of metadata")
    tags: Optional[str] = Field(None, description="JSON string of tags/labels")
    access_level: AccessLevel = Field(AccessLevel.READ, description="Access level")
    public_access: bool = Field(False, description="Whether artifact is publicly accessible")
    backup_enabled: bool = Field(True, description="Whether backup is enabled")
    version_control_system: Optional[str] = Field(None, max_length=50, description="Version control system")
    repository_url: Optional[str] = Field(None, max_length=500, description="Repository URL")
    branch_name: Optional[str] = Field(None, max_length=100, description="Branch name")
    commit_hash: Optional[str] = Field(None, max_length=64, description="Commit hash")
    performance_metrics: Optional[str] = Field(None, description="JSON string of performance metrics")
    load_time_avg: Optional[float] = Field(None, ge=0, description="Average load time in milliseconds")
    memory_usage: Optional[float] = Field(None, ge=0, description="Memory usage in MB")
    cpu_usage: Optional[float] = Field(None, ge=0, le=100, description="CPU usage percentage")
    compliance_status: ComplianceStatus = Field(ComplianceStatus.UNKNOWN, description="Compliance status")
    audit_requirements: Optional[str] = Field(None, description="JSON string of audit requirements")
    retention_policy: Optional[str] = Field(None, description="JSON string of retention policy")
    data_classification: DataClassification = Field(DataClassification.INTERNAL, description="Data classification")
    quality_score: Optional[float] = Field(None, ge=0, le=1, description="Quality score (0-1)")
    test_coverage: Optional[float] = Field(None, ge=0, le=100, description="Test coverage percentage")
    code_quality_metrics: Optional[str] = Field(None, description="JSON string of code quality metrics")
    documentation_status: DocumentationStatus = Field(DocumentationStatus.INCOMPLETE, description="Documentation status")
    operational_hours: OperationalHours = Field(OperationalHours.TWENTY_FOUR_SEVEN, description="Operational hours")
    maintenance_window: Optional[str] = Field(None, max_length=200, description="Maintenance window schedule")
    incident_count: int = Field(0, ge=0, description="Number of incidents")
    license_type: Optional[str] = Field(None, max_length=50, description="License type")
    license_cost: Optional[float] = Field(None, ge=0, description="Annual license cost")
    usage_metrics: Optional[str] = Field(None, description="JSON string of usage metrics")

    @validator('checksum')
    def validate_checksum(cls, v):
        if v and not (v.startswith('sha256:') or v.startswith('md5:') or len(v) in [32, 40, 64]):
            raise ValueError('Invalid checksum format')
        return v

    @validator('size_mb')
    def validate_size(cls, v):
        if v is not None and v > 1000000:  # 1TB limit
            raise ValueError('Artifact size cannot exceed 1TB')
        return v

    @validator('security_score')
    def validate_security_score(cls, v):
        if v is not None and (v < 0 or v > 10):
            raise ValueError('Security score must be between 0 and 10')
        return v

    @validator('quality_score')
    def validate_quality_score(cls, v):
        if v is not None and (v < 0 or v > 1):
            raise ValueError('Quality score must be between 0 and 1')
        return v

    @validator('test_coverage')
    def validate_test_coverage(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Test coverage must be between 0 and 100')
        return v

class ArtifactCreate(ArtifactBase):
    pass

class ArtifactUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    artifact_type: Optional[ArtifactType] = None
    version: Optional[str] = Field(None, min_length=1, max_length=50)
    format: Optional[str] = Field(None, max_length=50)
    storage_location: Optional[str] = Field(None, max_length=500)
    checksum: Optional[str] = Field(None, max_length=128)
    build_tool: Optional[str] = Field(None, max_length=100)
    deployment_target_node_id: Optional[UUID4] = None
    associated_component_id: Optional[UUID4] = None
    lifecycle_state: Optional[LifecycleState] = None
    size_mb: Optional[float] = Field(None, ge=0, le=1000000)
    file_count: Optional[int] = Field(None, ge=0)
    compression_ratio: Optional[float] = Field(None, ge=0, le=1)
    deployment_environment: Optional[DeploymentEnvironment] = None
    integrity_verified: Optional[bool] = None
    security_scan_passed: Optional[bool] = None
    vulnerability_count: Optional[int] = Field(None, ge=0)
    security_score: Optional[float] = Field(None, ge=0, le=10)
    dependencies: Optional[str] = None
    dependent_artifacts: Optional[str] = None
    build_dependencies: Optional[str] = None
    configuration: Optional[str] = None
    metadata: Optional[str] = None
    tags: Optional[str] = None
    access_level: Optional[AccessLevel] = None
    public_access: Optional[bool] = None
    backup_enabled: Optional[bool] = None
    version_control_system: Optional[str] = Field(None, max_length=50)
    repository_url: Optional[str] = Field(None, max_length=500)
    branch_name: Optional[str] = Field(None, max_length=100)
    commit_hash: Optional[str] = Field(None, max_length=64)
    performance_metrics: Optional[str] = None
    load_time_avg: Optional[float] = Field(None, ge=0)
    memory_usage: Optional[float] = Field(None, ge=0)
    cpu_usage: Optional[float] = Field(None, ge=0, le=100)
    compliance_status: Optional[ComplianceStatus] = None
    audit_requirements: Optional[str] = None
    retention_policy: Optional[str] = None
    data_classification: Optional[DataClassification] = None
    quality_score: Optional[float] = Field(None, ge=0, le=1)
    test_coverage: Optional[float] = Field(None, ge=0, le=100)
    code_quality_metrics: Optional[str] = None
    documentation_status: Optional[DocumentationStatus] = None
    operational_hours: Optional[OperationalHours] = None
    maintenance_window: Optional[str] = Field(None, max_length=200)
    incident_count: Optional[int] = Field(None, ge=0)
    license_type: Optional[str] = Field(None, max_length=50)
    license_cost: Optional[float] = Field(None, ge=0)
    usage_metrics: Optional[str] = None

class ArtifactResponse(ArtifactBase):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    owner_user_id: Optional[UUID4] = None
    build_date: Optional[datetime] = None
    deployment_date: Optional[datetime] = None
    last_modified: datetime
    last_deployed: Optional[datetime] = None
    last_incident: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ArtifactLinkBase(BaseModel):
    linked_element_id: UUID4 = Field(..., description="ID of the linked element")
    linked_element_type: str = Field(..., min_length=1, max_length=100, description="Type of linked element")
    link_type: LinkType = Field(..., description="Type of link")
    relationship_strength: RelationshipStrength = Field(RelationshipStrength.MEDIUM, description="Strength of relationship")
    dependency_level: DependencyLevel = Field(DependencyLevel.MEDIUM, description="Level of dependency")
    implementation_status: ImplementationStatus = Field(ImplementationStatus.ACTIVE, description="Implementation status")
    implementation_date: Optional[datetime] = Field(None, description="Implementation date")
    implementation_version: Optional[str] = Field(None, max_length=50, description="Implementation version")
    implementation_config: Optional[str] = Field(None, description="JSON string of implementation configuration")
    deployment_status: DeploymentStatus = Field(DeploymentStatus.DEPLOYED, description="Deployment status")
    deployment_date: Optional[datetime] = Field(None, description="Deployment date")
    deployment_environment: DeploymentEnvironment = Field(DeploymentEnvironment.PRODUCTION, description="Deployment environment")
    deployment_method: Optional[str] = Field(None, max_length=50, description="Deployment method")
    communication_protocol: Optional[str] = Field(None, max_length=20, description="Communication protocol")
    communication_port: Optional[int] = Field(None, ge=1, le=65535, description="Communication port")
    communication_frequency: CommunicationFrequency = Field(CommunicationFrequency.REGULAR, description="Communication frequency")
    communication_type: CommunicationType = Field(CommunicationType.SYNCHRONOUS, description="Communication type")
    performance_impact: PerformanceImpact = Field(PerformanceImpact.MEDIUM, description="Performance impact")
    latency_contribution: Optional[float] = Field(None, ge=0, description="Latency contribution in milliseconds")
    bandwidth_usage: Optional[float] = Field(None, ge=0, description="Bandwidth usage in Mbps")
    resource_consumption: Optional[float] = Field(None, ge=0, le=100, description="Resource consumption percentage")
    business_criticality: BusinessCriticality = Field(BusinessCriticality.MEDIUM, description="Business criticality")
    business_value: BusinessCriticality = Field(BusinessCriticality.MEDIUM, description="Business value")
    alignment_score: Optional[float] = Field(None, ge=0, le=1, description="Alignment score (0-1)")
    implementation_priority: str = Field("normal", max_length=20, description="Implementation priority")
    implementation_phase: str = Field("active", max_length=20, description="Implementation phase")
    resource_allocation: Optional[float] = Field(None, ge=0, le=100, description="Resource allocation percentage")
    risk_level: RiskLevel = Field(RiskLevel.MEDIUM, description="Risk level")
    reliability_score: Optional[float] = Field(None, ge=0, le=1, description="Reliability score (0-1)")
    failure_impact: PerformanceImpact = Field(PerformanceImpact.MEDIUM, description="Failure impact")
    recovery_time: Optional[int] = Field(None, ge=0, description="Recovery time in minutes")
    monitoring_enabled: bool = Field(True, description="Whether monitoring is enabled")
    alerting_enabled: bool = Field(True, description="Whether alerting is enabled")
    logging_level: LoggingLevel = Field(LoggingLevel.INFO, description="Logging level")
    metrics_collection: Optional[str] = Field(None, description="JSON string of metrics configuration")
    security_requirements: Optional[str] = Field(None, description="JSON string of security requirements")
    compliance_impact: PerformanceImpact = Field(PerformanceImpact.LOW, description="Compliance impact")
    data_protection: Optional[str] = Field(None, description="JSON string of data protection requirements")
    performance_contribution: Optional[float] = Field(None, ge=0, le=100, description="Performance contribution percentage")
    success_contribution: Optional[float] = Field(None, ge=0, le=100, description="Success contribution percentage")
    quality_metrics: Optional[str] = Field(None, description="JSON string of quality metrics")

    @validator('communication_port')
    def validate_port(cls, v):
        if v is not None and (v < 1 or v > 65535):
            raise ValueError('Port must be between 1 and 65535')
        return v

    @validator('resource_consumption')
    def validate_resource_consumption(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Resource consumption must be between 0 and 100')
        return v

    @validator('alignment_score')
    def validate_alignment_score(cls, v):
        if v is not None and (v < 0 or v > 1):
            raise ValueError('Alignment score must be between 0 and 1')
        return v

    @validator('reliability_score')
    def validate_reliability_score(cls, v):
        if v is not None and (v < 0 or v > 1):
            raise ValueError('Reliability score must be between 0 and 1')
        return v

    @validator('performance_contribution')
    def validate_performance_contribution(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Performance contribution must be between 0 and 100')
        return v

    @validator('success_contribution')
    def validate_success_contribution(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Success contribution must be between 0 and 100')
        return v

class ArtifactLinkCreate(ArtifactLinkBase):
    pass

class ArtifactLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID4] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=100)
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    implementation_status: Optional[ImplementationStatus] = None
    implementation_date: Optional[datetime] = None
    implementation_version: Optional[str] = Field(None, max_length=50)
    implementation_config: Optional[str] = None
    deployment_status: Optional[DeploymentStatus] = None
    deployment_date: Optional[datetime] = None
    deployment_environment: Optional[DeploymentEnvironment] = None
    deployment_method: Optional[str] = Field(None, max_length=50)
    communication_protocol: Optional[str] = Field(None, max_length=20)
    communication_port: Optional[int] = Field(None, ge=1, le=65535)
    communication_frequency: Optional[CommunicationFrequency] = None
    communication_type: Optional[CommunicationType] = None
    performance_impact: Optional[PerformanceImpact] = None
    latency_contribution: Optional[float] = Field(None, ge=0)
    bandwidth_usage: Optional[float] = Field(None, ge=0)
    resource_consumption: Optional[float] = Field(None, ge=0, le=100)
    business_criticality: Optional[BusinessCriticality] = None
    business_value: Optional[BusinessCriticality] = None
    alignment_score: Optional[float] = Field(None, ge=0, le=1)
    implementation_priority: Optional[str] = Field(None, max_length=20)
    implementation_phase: Optional[str] = Field(None, max_length=20)
    resource_allocation: Optional[float] = Field(None, ge=0, le=100)
    risk_level: Optional[RiskLevel] = None
    reliability_score: Optional[float] = Field(None, ge=0, le=1)
    failure_impact: Optional[PerformanceImpact] = None
    recovery_time: Optional[int] = Field(None, ge=0)
    monitoring_enabled: Optional[bool] = None
    alerting_enabled: Optional[bool] = None
    logging_level: Optional[LoggingLevel] = None
    metrics_collection: Optional[str] = None
    security_requirements: Optional[str] = None
    compliance_impact: Optional[PerformanceImpact] = None
    data_protection: Optional[str] = None
    performance_contribution: Optional[float] = Field(None, ge=0, le=100)
    success_contribution: Optional[float] = Field(None, ge=0, le=100)
    quality_metrics: Optional[str] = None

class ArtifactLinkResponse(ArtifactLinkBase):
    id: UUID4
    artifact_id: UUID4
    created_by: UUID4
    created_at: datetime

    class Config:
        from_attributes = True

# Analysis response schemas
class DependencyMapResponse(BaseModel):
    artifact_id: UUID4
    direct_dependencies: List[Dict[str, Any]]
    indirect_dependencies: List[Dict[str, Any]]
    dependency_tree: Dict[str, Any]
    circular_dependencies: List[Dict[str, Any]]
    total_dependencies: int
    max_depth: int

class IntegrityCheckResponse(BaseModel):
    artifact_id: UUID4
    checksum_valid: bool
    security_scan_passed: bool
    vulnerability_count: int
    security_score: float
    integrity_score: float
    compliance_status: str
    recommendations: List[str]
    issues: List[Dict[str, Any]]

# Enumeration response schemas
class EnumerationResponse(BaseModel):
    values: List[str]

# Health check response
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    database: str
    redis: str
    uptime: float 