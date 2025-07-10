from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class CommunicationPath(Base):
    __tablename__ = "communication_path"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core communication path fields
    name = Column(String, nullable=False)
    description = Column(Text)
    path_type = Column(String, nullable=False, default="LAN")  # LAN, WAN, VPN, API Gateway, Message Queue, Serial Link, Interconnect
    protocol = Column(String, nullable=False)  # HTTP, HTTPS, AMQP, TCP, GRPC, MQTT, etc.
    bandwidth_mbps = Column(Float)  # Bandwidth in Mbps
    latency_ms = Column(Float)  # Latency in milliseconds
    source_node_id = Column(UUID(as_uuid=True), ForeignKey("node.id"))  # Source node
    target_node_id = Column(UUID(as_uuid=True), ForeignKey("node.id"))  # Target node
    topology = Column(String, default="point_to_point")  # point_to_point, broadcast, mesh, star, ring
    
    # Security and encryption
    encryption_status = Column(String, default="none")  # none, basic, strong, end_to_end
    encryption_algorithm = Column(String)  # AES, RSA, TLS, etc.
    encryption_key_size = Column(Integer)  # Key size in bits
    ssl_tls_enabled = Column(Boolean, default=False)
    certificate_required = Column(Boolean, default=False)
    
    # Quality of Service
    qos_policy = Column(String)  # QoS policy name
    priority_level = Column(String, default="normal")  # low, normal, high, critical
    bandwidth_guarantee = Column(Float)  # Guaranteed bandwidth in Mbps
    latency_guarantee = Column(Float)  # Guaranteed latency in ms
    
    # Performance and monitoring
    availability_target_pct = Column(Float, default=99.9)  # Availability target percentage
    current_availability = Column(Float)  # Current availability percentage
    uptime_pct = Column(Float)  # Uptime percentage
    last_tested = Column(DateTime)  # Last health check
    last_maintenance = Column(DateTime)  # Last maintenance
    next_maintenance = Column(DateTime)  # Next scheduled maintenance
    
    # Network configuration
    ip_addresses = Column(Text)  # JSON string of IP addresses
    port_numbers = Column(Text)  # JSON string of port numbers
    subnet_mask = Column(String)  # Subnet mask
    gateway_address = Column(String)  # Gateway address
    dns_servers = Column(Text)  # JSON string of DNS servers
    
    # Routing and switching
    routing_protocol = Column(String)  # OSPF, BGP, RIP, etc.
    routing_table = Column(Text)  # JSON string of routing table
    switch_configuration = Column(Text)  # JSON string of switch configuration
    vlan_id = Column(Integer)  # VLAN identifier
    
    # Load balancing and redundancy
    load_balancer_enabled = Column(Boolean, default=False)
    load_balancer_type = Column(String)  # round_robin, least_connections, etc.
    redundancy_enabled = Column(Boolean, default=False)
    failover_time = Column(Integer)  # Failover time in seconds
    backup_path_id = Column(UUID(as_uuid=True), ForeignKey("communication_path.id"))  # Backup path
    
    # Monitoring and alerting
    monitoring_enabled = Column(Boolean, default=True)
    alerting_enabled = Column(Boolean, default=True)
    monitoring_endpoints = Column(Text)  # JSON string of monitoring endpoints
    alert_thresholds = Column(Text)  # JSON string of alert thresholds
    
    # Performance metrics
    packet_loss_pct = Column(Float)  # Packet loss percentage
    jitter_ms = Column(Float)  # Jitter in milliseconds
    throughput_mbps = Column(Float)  # Current throughput in Mbps
    connection_count = Column(Integer)  # Number of active connections
    error_rate_pct = Column(Float)  # Error rate percentage
    
    # Security monitoring
    security_scan_enabled = Column(Boolean, default=True)
    intrusion_detection_enabled = Column(Boolean, default=True)
    firewall_rules = Column(Text)  # JSON string of firewall rules
    access_control_list = Column(Text)  # JSON string of ACL
    
    # Compliance and governance
    compliance_status = Column(String, default="unknown")  # compliant, non_compliant, unknown, pending
    audit_requirements = Column(Text)  # JSON string of audit requirements
    data_classification = Column(String, default="internal")  # public, internal, confidential, restricted
    retention_policy = Column(Text)  # JSON string of retention policy
    
    # Cost and licensing
    cost_per_month = Column(Float)  # Monthly cost
    license_type = Column(String)  # open_source, proprietary, commercial
    license_cost = Column(Float)  # Annual license cost
    usage_metrics = Column(Text)  # JSON string of usage metrics
    
    # Operational details
    operational_hours = Column(String, default="24x7")  # 24x7, business_hours, on_demand
    maintenance_window = Column(String)  # Maintenance window schedule
    incident_count = Column(Integer, default=0)  # Number of incidents
    last_incident = Column(DateTime)  # Last incident date
    mttr_minutes = Column(Integer)  # Mean Time To Repair in minutes
    mtta_minutes = Column(Integer)  # Mean Time To Acknowledge in minutes
    
    # Configuration management
    configuration_version = Column(String)  # Configuration version
    configuration_backup = Column(Text)  # JSON string of configuration backup
    change_history = Column(Text)  # JSON string of change history
    rollback_enabled = Column(Boolean, default=True)
    
    # Documentation
    documentation_url = Column(String)  # URL to documentation
    runbook_url = Column(String)  # URL to runbook
    troubleshooting_guide = Column(Text)  # Troubleshooting guide
    contact_information = Column(Text)  # JSON string of contact information
    
    # Status and lifecycle
    status = Column(String, default="active")  # active, inactive, maintenance, failed, deprecated
    lifecycle_state = Column(String, default="operational")  # planning, development, operational, maintenance, decommissioned
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("PathLink", back_populates="communication_path")
    backup_path = relationship("CommunicationPath", remote_side=[id])

class PathLink(Base):
    __tablename__ = "path_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    communication_path_id = Column(UUID(as_uuid=True), ForeignKey("communication_path.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # artifact, interface, application_service, device, etc.
    link_type = Column(String, nullable=False)  # uses, connects, enables, supports, transports
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Communication context
    communication_protocol = Column(String)  # Protocol used for communication
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
    implementation_status = Column(String, default="active")  # active, inactive, failed, pending, deprecated
    implementation_date = Column(DateTime)  # When the implementation occurred
    implementation_version = Column(String)  # Version of the implementation
    implementation_config = Column(Text)  # JSON string of implementation configuration
    
    # Deployment context
    deployment_status = Column(String, default="deployed")  # deployed, pending, failed, rolled_back
    deployment_date = Column(DateTime)  # When the deployment occurred
    deployment_environment = Column(String, default="production")  # production, staging, development, testing
    deployment_method = Column(String)  # manual, automated, blue_green, canary
    
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
    communication_path = relationship("CommunicationPath", back_populates="links") 