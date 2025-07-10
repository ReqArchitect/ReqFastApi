from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class SystemSoftware(Base):
    __tablename__ = "system_software"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core system software fields
    name = Column(String, nullable=False)
    description = Column(Text)
    software_type = Column(String, nullable=False, default="os")  # os, database, middleware, runtime, container_engine
    version = Column(String, nullable=False)  # Version string
    vendor = Column(String)  # Software vendor
    license_type = Column(String, default="proprietary")  # proprietary, open_source, commercial, freeware
    supported_node_id = Column(UUID(as_uuid=True), ForeignKey("node.id"))  # Node that hosts this software
    capabilities_provided = Column(Text)  # JSON string of capabilities provided
    compliance_certifications = Column(Text)  # JSON string of compliance certifications
    lifecycle_state = Column(String, default="active")  # active, inactive, deprecated, end_of_life, planned
    
    # Security and compliance
    vulnerability_score = Column(Float)  # CVSS score (0.0 to 10.0)
    security_patches_available = Column(Boolean, default=False)
    last_security_audit = Column(DateTime)
    compliance_status = Column(String, default="unknown")  # compliant, non_compliant, unknown, pending
    
    # Update and maintenance
    update_channel = Column(String, default="stable")  # stable, beta, alpha, lts
    last_patch_date = Column(DateTime)
    next_patch_date = Column(DateTime)
    auto_update_enabled = Column(Boolean, default=True)
    update_frequency = Column(String, default="monthly")  # daily, weekly, monthly, quarterly, yearly
    
    # Performance and monitoring
    performance_metrics = Column(Text)  # JSON string of performance metrics
    resource_usage = Column(Float)  # Current resource usage percentage
    uptime_percentage = Column(Float)  # Uptime percentage
    response_time_avg = Column(Float)  # Average response time in milliseconds
    
    # Configuration and deployment
    configuration = Column(Text)  # JSON string of configuration
    deployment_environment = Column(String, default="production")  # production, staging, development, testing
    deployment_method = Column(String)  # manual, automated, container, package_manager
    
    # Dependencies and relationships
    dependencies = Column(Text)  # JSON string of software dependencies
    dependent_components = Column(Text)  # JSON string of components that depend on this software
    integration_points = Column(Text)  # JSON string of integration points
    
    # Licensing and cost
    license_expiry = Column(DateTime)
    license_cost = Column(Float)  # Annual license cost
    license_seats = Column(Integer)  # Number of licensed seats/users
    license_usage = Column(Integer)  # Current license usage
    
    # Documentation and support
    documentation_url = Column(String)
    support_contact = Column(String)
    support_level = Column(String, default="standard")  # basic, standard, premium, enterprise
    support_expiry = Column(DateTime)
    
    # Backup and recovery
    backup_enabled = Column(Boolean, default=True)
    backup_frequency = Column(String, default="daily")
    backup_retention_days = Column(Integer, default=30)
    disaster_recovery_plan = Column(Text)  # JSON string of DR plan
    
    # Monitoring and alerting
    monitoring_enabled = Column(Boolean, default=True)
    alerting_enabled = Column(Boolean, default=True)
    monitoring_endpoints = Column(Text)  # JSON string of monitoring endpoints
    alerting_rules = Column(Text)  # JSON string of alerting rules
    
    # Operational details
    installation_date = Column(DateTime)
    last_maintenance = Column(DateTime)
    next_maintenance = Column(DateTime)
    maintenance_window = Column(String)  # Maintenance window schedule
    incident_count = Column(Integer, default=0)  # Number of incidents
    last_incident = Column(DateTime)  # Last incident date
    
    # Compliance and governance
    data_retention_policy = Column(Text)  # JSON string of data retention policy
    access_controls = Column(Text)  # JSON string of access controls
    audit_requirements = Column(Text)  # JSON string of audit requirements
    regulatory_compliance = Column(Text)  # JSON string of regulatory compliance
    
    # Performance characteristics
    cpu_requirements = Column(Float)  # CPU requirements in cores
    memory_requirements = Column(Float)  # Memory requirements in GB
    storage_requirements = Column(Float)  # Storage requirements in GB
    network_requirements = Column(Float)  # Network requirements in Mbps
    
    # Scalability and capacity
    max_concurrent_users = Column(Integer)
    max_data_volume = Column(Float)  # Maximum data volume in GB
    scalability_limits = Column(Text)  # JSON string of scalability limits
    capacity_planning = Column(Text)  # JSON string of capacity planning data
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("SoftwareLink", back_populates="system_software")

class SoftwareLink(Base):
    __tablename__ = "software_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    system_software_id = Column(UUID(as_uuid=True), ForeignKey("system_software.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # node, application_component, device, artifact, etc.
    link_type = Column(String, nullable=False)  # runs_on, depends_on, integrates_with, manages, supports
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Integration context
    integration_status = Column(String, default="active")  # active, inactive, failed, pending, deprecated
    integration_date = Column(DateTime)  # When the integration occurred
    integration_version = Column(String)  # Version of the integration
    integration_config = Column(Text)  # JSON string of integration configuration
    
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
    system_software = relationship("SystemSoftware", back_populates="links") 