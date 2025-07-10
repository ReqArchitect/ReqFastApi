from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class Node(Base):
    __tablename__ = "node"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core node fields
    name = Column(String, nullable=False)
    description = Column(Text)
    node_type = Column(String, nullable=False, default="vm")  # vm, container, physical, cloud, edge
    environment = Column(String, default="production")  # production, staging, development, testing
    operating_system = Column(String)  # Linux, Windows, macOS, etc.
    hardware_spec = Column(Text)  # JSON string of hardware specifications
    region = Column(String)  # Geographic region or data center
    availability_zone = Column(String)  # Cloud availability zone
    cluster_id = Column(UUID(as_uuid=True), ForeignKey("cluster.id"))  # For container orchestration
    host_capabilities = Column(Text)  # JSON string of host capabilities
    deployed_components = Column(Text)  # JSON string of deployed application components
    availability_target = Column(Float, default=99.9)  # Availability target percentage
    current_availability = Column(Float)  # Current availability percentage
    resource_utilization = Column(Float)  # Current resource utilization percentage
    lifecycle_state = Column(String, default="active")  # active, inactive, maintenance, decommissioned, planned
    
    # Performance and monitoring
    cpu_cores = Column(Integer)  # Number of CPU cores
    cpu_usage_pct = Column(Float)  # Current CPU usage percentage
    memory_gb = Column(Float)  # Memory in GB
    memory_usage_pct = Column(Float)  # Current memory usage percentage
    storage_gb = Column(Float)  # Storage in GB
    storage_usage_pct = Column(Float)  # Current storage usage percentage
    network_bandwidth_mbps = Column(Float)  # Network bandwidth in Mbps
    network_usage_pct = Column(Float)  # Current network usage percentage
    
    # Infrastructure details
    ip_address = Column(String)  # Primary IP address
    mac_address = Column(String)  # MAC address
    hostname = Column(String)  # Hostname
    domain = Column(String)  # Domain name
    subnet = Column(String)  # Subnet information
    gateway = Column(String)  # Gateway address
    dns_servers = Column(Text)  # JSON string of DNS servers
    
    # Cloud-specific fields
    cloud_provider = Column(String)  # AWS, Azure, GCP, etc.
    cloud_instance_id = Column(String)  # Cloud instance identifier
    cloud_instance_type = Column(String)  # Cloud instance type
    cloud_tags = Column(Text)  # JSON string of cloud tags
    
    # Security and compliance
    security_level = Column(String, default="standard")  # basic, standard, high, critical
    compliance_requirements = Column(Text)  # JSON string of compliance requirements
    encryption_enabled = Column(Boolean, default=True)  # Whether encryption is enabled
    backup_enabled = Column(Boolean, default=True)  # Whether backup is enabled
    monitoring_enabled = Column(Boolean, default=True)  # Whether monitoring is enabled
    
    # Operational details
    maintenance_window = Column(String)  # Maintenance window schedule
    last_maintenance = Column(DateTime)  # Last maintenance date
    next_maintenance = Column(DateTime)  # Next scheduled maintenance
    incident_count = Column(Integer, default=0)  # Number of incidents
    last_incident = Column(DateTime)  # Last incident date
    sla_breaches = Column(Integer, default=0)  # Number of SLA breaches
    
    # Cost and resource management
    monthly_cost = Column(Float)  # Monthly operational cost
    cost_center = Column(String)  # Cost center assignment
    resource_pool = Column(String)  # Resource pool assignment
    capacity_planning = Column(Text)  # JSON string of capacity planning data
    
    # Network and connectivity
    network_interfaces = Column(Text)  # JSON string of network interfaces
    firewall_rules = Column(Text)  # JSON string of firewall rules
    load_balancer_config = Column(Text)  # JSON string of load balancer configuration
    vpn_config = Column(Text)  # JSON string of VPN configuration
    
    # Container and virtualization
    container_runtime = Column(String)  # Docker, containerd, etc.
    virtualization_type = Column(String)  # VM, container, bare metal
    hypervisor = Column(String)  # Hypervisor type
    container_orchestrator = Column(String)  # Kubernetes, Docker Swarm, etc.
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("NodeLink", back_populates="node")

class NodeLink(Base):
    __tablename__ = "node_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id = Column(UUID(as_uuid=True), ForeignKey("node.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # application_component, system_software, device, artifact, etc.
    link_type = Column(String, nullable=False)  # hosts, deploys, communicates_with, depends_on, manages
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Deployment context
    deployment_status = Column(String, default="active")  # active, inactive, failed, pending
    deployment_date = Column(DateTime)  # When the deployment occurred
    deployment_version = Column(String)  # Version of the deployed component
    deployment_config = Column(Text)  # JSON string of deployment configuration
    
    # Communication context
    communication_protocol = Column(String)  # HTTP, HTTPS, TCP, UDP, etc.
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
    node = relationship("Node", back_populates="links") 