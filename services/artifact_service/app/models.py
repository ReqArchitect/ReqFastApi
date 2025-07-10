from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class Artifact(Base):
    __tablename__ = "artifact"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core artifact fields
    name = Column(String, nullable=False)
    description = Column(Text)
    artifact_type = Column(String, nullable=False, default="source")  # source, build, image, config, script, binary, container
    version = Column(String, nullable=False)  # Version string
    format = Column(String)  # File format (docker, yaml, json, jar, exe, etc.)
    storage_location = Column(String)  # Storage location/path
    checksum = Column(String)  # Hash/checksum for integrity
    build_tool = Column(String)  # Tool used to build (maven, gradle, docker, etc.)
    deployment_target_node_id = Column(UUID(as_uuid=True), ForeignKey("node.id"))  # Node where artifact is deployed
    associated_component_id = Column(UUID(as_uuid=True), ForeignKey("application_component.id"))  # Associated application component
    lifecycle_state = Column(String, default="active")  # active, inactive, deprecated, archived, deleted
    
    # File and size information
    size_mb = Column(Float)  # Size in megabytes
    file_count = Column(Integer)  # Number of files in artifact
    compression_ratio = Column(Float)  # Compression ratio if applicable
    
    # Build and deployment information
    build_date = Column(DateTime)
    deployment_date = Column(DateTime)
    last_modified = Column(DateTime, default=datetime.utcnow)
    last_deployed = Column(DateTime)
    deployment_environment = Column(String, default="production")  # production, staging, development, testing
    
    # Security and integrity
    integrity_verified = Column(Boolean, default=False)
    security_scan_passed = Column(Boolean, default=True)
    vulnerability_count = Column(Integer, default=0)
    security_score = Column(Float)  # 0.0 to 10.0 security score
    
    # Dependencies and relationships
    dependencies = Column(Text)  # JSON string of artifact dependencies
    dependent_artifacts = Column(Text)  # JSON string of artifacts that depend on this
    build_dependencies = Column(Text)  # JSON string of build-time dependencies
    
    # Configuration and metadata
    configuration = Column(Text)  # JSON string of configuration
    metadata = Column(Text)  # JSON string of metadata
    tags = Column(Text)  # JSON string of tags/labels
    
    # Access and permissions
    owner_user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    access_level = Column(String, default="read")  # read, write, admin
    public_access = Column(Boolean, default=False)
    
    # Backup and versioning
    backup_enabled = Column(Boolean, default=True)
    version_control_system = Column(String)  # git, svn, etc.
    repository_url = Column(String)
    branch_name = Column(String)
    commit_hash = Column(String)
    
    # Performance and monitoring
    performance_metrics = Column(Text)  # JSON string of performance metrics
    load_time_avg = Column(Float)  # Average load time in milliseconds
    memory_usage = Column(Float)  # Memory usage in MB
    cpu_usage = Column(Float)  # CPU usage percentage
    
    # Compliance and governance
    compliance_status = Column(String, default="unknown")  # compliant, non_compliant, unknown, pending
    audit_requirements = Column(Text)  # JSON string of audit requirements
    retention_policy = Column(Text)  # JSON string of retention policy
    data_classification = Column(String, default="internal")  # public, internal, confidential, restricted
    
    # Quality and testing
    quality_score = Column(Float)  # 0.0 to 1.0 quality score
    test_coverage = Column(Float)  # Test coverage percentage
    code_quality_metrics = Column(Text)  # JSON string of code quality metrics
    documentation_status = Column(String, default="incomplete")  # complete, incomplete, missing
    
    # Operational details
    operational_hours = Column(String, default="24x7")  # 24x7, business_hours, on_demand
    maintenance_window = Column(String)  # Maintenance window schedule
    incident_count = Column(Integer, default=0)  # Number of incidents
    last_incident = Column(DateTime)  # Last incident date
    
    # Cost and licensing
    license_type = Column(String)  # open_source, proprietary, commercial
    license_cost = Column(Float)  # Annual license cost
    usage_metrics = Column(Text)  # JSON string of usage metrics
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("ArtifactLink", back_populates="artifact")

class ArtifactLink(Base):
    __tablename__ = "artifact_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artifact_id = Column(UUID(as_uuid=True), ForeignKey("artifact.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # application_component, node, device, system_software, etc.
    link_type = Column(String, nullable=False)  # implements, deployed_on, depends_on, contains, configures
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Implementation context
    implementation_status = Column(String, default="active")  # active, inactive, failed, pending, deprecated
    implementation_date = Column(DateTime)  # When the implementation occurred
    implementation_version = Column(String)  # Version of the implementation
    implementation_config = Column(Text)  # JSON string of implementation configuration
    
    # Deployment context
    deployment_status = Column(String, default="deployed")  # deployed, pending, failed, rolled_back
    deployment_date = Column(DateTime)  # When the deployment occurred
    deployment_environment = Column(String, default="production")  # production, staging, development, testing
    deployment_method = Column(String)  # manual, automated, blue_green, canary
    
    # Communication context
    communication_protocol = Column(String)  # HTTP, HTTPS, TCP, UDP, API, etc.
    communication_port = Column(Integer)  # Port number for communication
    communication_frequency = Column(String, default="regular")  # frequent, regular, occasional, rare
    communication_type = Column(String, default="synchronous")  # synchronous, asynchronous, batch, real_time
    
    # Performance impact
    performance_impact = Column(String, default="medium")  # low, medium, high, critical
    latency_contribution = Column(Float)  # Latency contribution in milliseconds
    bandwidth_usage = Column(Float)  # Bandwidth usage in Mbps
    resource_consumption = Column(Float)  # Resource consumption percentage
    
    # Business context
    business_criticality = Column(String, default="medium")  # low, medium, high, critical
    business_value = Column(String, default="medium")  # low, medium, high, critical
    alignment_score = Column(Float)  # 0.0 to 1.0 - how well aligned this link is
    
    # Implementation context
    implementation_priority = Column(String, default="normal")  # low, normal, high, critical
    implementation_phase = Column(String, default="active")  # planning, active, completed, deprecated
    resource_allocation = Column(Float)  # Percentage of resources allocated to this link
    
    # Risk and reliability
    risk_level = Column(String, default="medium")  # low, medium, high, critical
    reliability_score = Column(Float)  # 0.0 to 1.0 reliability score
    failure_impact = Column(String, default="medium")  # low, medium, high, critical
    recovery_time = Column(Integer)  # Recovery time in minutes
    
    # Monitoring and observability
    monitoring_enabled = Column(Boolean, default=True)
    alerting_enabled = Column(Boolean, default=True)
    logging_level = Column(String, default="info")  # debug, info, warning, error
    metrics_collection = Column(Text)  # JSON string of metrics configuration
    
    # Security and compliance
    security_requirements = Column(Text)  # JSON string of security requirements
    compliance_impact = Column(String, default="low")  # low, medium, high, critical
    data_protection = Column(Text)  # JSON string of data protection requirements
    
    # Performance tracking
    performance_contribution = Column(Float)  # Percentage contribution to overall performance
    success_contribution = Column(Float)  # Percentage contribution to success criteria
    quality_metrics = Column(Text)  # JSON string of quality metrics
    
    # Traceability
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    artifact = relationship("Artifact", back_populates="links") 