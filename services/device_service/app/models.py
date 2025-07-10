from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class Device(Base):
    __tablename__ = "device"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core device fields
    name = Column(String, nullable=False)
    description = Column(Text)
    device_type = Column(String, nullable=False)  # server, mobile, iot, sensor, router, switch, gateway, etc.
    manufacturer = Column(String)
    model_number = Column(String)
    serial_number = Column(String, unique=True)
    asset_tag = Column(String, unique=True)
    
    # Physical characteristics
    location = Column(String)  # Physical location
    rack_position = Column(String)  # Rack position if applicable
    room_number = Column(String)  # Room number
    building = Column(String)  # Building name/number
    floor = Column(String)  # Floor number
    data_center = Column(String)  # Data center name
    region = Column(String)  # Geographic region
    country = Column(String)  # Country
    timezone = Column(String)  # Timezone
    
    # Hardware specifications
    cpu_model = Column(String)  # CPU model
    cpu_cores = Column(Integer)  # Number of CPU cores
    cpu_speed_ghz = Column(Float)  # CPU speed in GHz
    memory_gb = Column(Float)  # Memory in GB
    storage_gb = Column(Float)  # Storage in GB
    storage_type = Column(String)  # SSD, HDD, NVMe, etc.
    network_interfaces = Column(Text)  # JSON string of network interfaces
    power_consumption_watts = Column(Float)  # Power consumption in watts
    weight_kg = Column(Float)  # Weight in kilograms
    dimensions = Column(Text)  # JSON string of dimensions
    
    # Operating conditions
    operating_conditions = Column(Text)  # JSON string of operating conditions
    temperature_range = Column(String)  # Operating temperature range
    humidity_range = Column(String)  # Operating humidity range
    power_requirements = Column(String)  # Power requirements
    cooling_requirements = Column(String)  # Cooling requirements
    
    # Software and firmware
    firmware_version = Column(String)  # Current firmware version
    firmware_date = Column(DateTime)  # Firmware installation date
    operating_system = Column(String)  # Operating system
    os_version = Column(String)  # OS version
    os_install_date = Column(DateTime)  # OS installation date
    software_inventory = Column(Text)  # JSON string of installed software
    
    # Network configuration
    ip_addresses = Column(Text)  # JSON string of IP addresses
    mac_addresses = Column(Text)  # JSON string of MAC addresses
    hostname = Column(String)  # Device hostname
    domain = Column(String)  # Domain name
    dns_servers = Column(Text)  # JSON string of DNS servers
    gateway_address = Column(String)  # Gateway address
    subnet_mask = Column(String)  # Subnet mask
    
    # Security configuration
    security_level = Column(String, default="standard")  # basic, standard, high, critical
    encryption_enabled = Column(Boolean, default=False)
    encryption_type = Column(String)  # Type of encryption
    antivirus_installed = Column(Boolean, default=False)
    antivirus_version = Column(String)  # Antivirus version
    firewall_enabled = Column(Boolean, default=True)
    firewall_rules = Column(Text)  # JSON string of firewall rules
    access_control_list = Column(Text)  # JSON string of ACL
    
    # Maintenance and lifecycle
    maintenance_schedule = Column(Text)  # JSON string of maintenance schedule
    last_maintenance = Column(DateTime)  # Last maintenance date
    next_maintenance = Column(DateTime)  # Next scheduled maintenance
    last_inspection_date = Column(DateTime)  # Last inspection date
    next_inspection_date = Column(DateTime)  # Next inspection date
    warranty_expiry = Column(DateTime)  # Warranty expiry date
    support_contract = Column(String)  # Support contract details
    support_vendor = Column(String)  # Support vendor
    
    # Compliance and governance
    compliance_status = Column(String, default="unknown")  # compliant, non_compliant, unknown, pending
    compliance_requirements = Column(Text)  # JSON string of compliance requirements
    audit_requirements = Column(Text)  # JSON string of audit requirements
    data_classification = Column(String, default="internal")  # public, internal, confidential, restricted
    retention_policy = Column(Text)  # JSON string of retention policy
    
    # Performance monitoring
    performance_metrics = Column(Text)  # JSON string of performance metrics
    cpu_utilization = Column(Float)  # Current CPU utilization percentage
    memory_utilization = Column(Float)  # Current memory utilization percentage
    disk_utilization = Column(Float)  # Current disk utilization percentage
    network_utilization = Column(Float)  # Current network utilization percentage
    temperature_celsius = Column(Float)  # Current temperature in Celsius
    power_consumption_current = Column(Float)  # Current power consumption in watts
    
    # Availability and reliability
    availability_target_pct = Column(Float, default=99.9)  # Availability target percentage
    current_availability = Column(Float)  # Current availability percentage
    uptime_pct = Column(Float)  # Uptime percentage
    mttf_hours = Column(Float)  # Mean Time To Failure in hours
    mttr_minutes = Column(Integer)  # Mean Time To Repair in minutes
    incident_count = Column(Integer, default=0)  # Number of incidents
    last_incident = Column(DateTime)  # Last incident date
    
    # Cost and licensing
    purchase_date = Column(DateTime)  # Purchase date
    purchase_cost = Column(Float)  # Purchase cost
    current_value = Column(Float)  # Current value
    depreciation_rate = Column(Float)  # Depreciation rate
    license_cost = Column(Float)  # Annual license cost
    maintenance_cost = Column(Float)  # Annual maintenance cost
    power_cost_per_month = Column(Float)  # Monthly power cost
    
    # Environmental impact
    energy_efficiency_rating = Column(String)  # Energy efficiency rating
    carbon_footprint = Column(Float)  # Carbon footprint in kg CO2
    recyclable_materials = Column(Boolean, default=False)
    disposal_method = Column(String)  # Disposal method
    
    # Relationships
    supported_node_id = Column(UUID(as_uuid=True), ForeignKey("node.id"))  # Supported node
    system_software_id = Column(UUID(as_uuid=True), ForeignKey("system_software.id"))  # System software
    communication_path_id = Column(UUID(as_uuid=True), ForeignKey("communication_path.id"))  # Communication path
    artifact_id = Column(UUID(as_uuid=True), ForeignKey("artifact.id"))  # Associated artifact
    
    # Status and lifecycle
    status = Column(String, default="active")  # active, inactive, maintenance, failed, decommissioned
    lifecycle_state = Column(String, default="operational")  # planning, development, operational, maintenance, decommissioned
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("DeviceLink", back_populates="device")

class DeviceLink(Base):
    __tablename__ = "device_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("device.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # node, system_software, artifact, communication_path, etc.
    link_type = Column(String, nullable=False)  # hosts, supports, connects, enables, uses
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Physical connection context
    connection_type = Column(String)  # wired, wireless, fiber, ethernet, etc.
    connection_speed = Column(Float)  # Connection speed in Mbps
    connection_protocol = Column(String)  # Connection protocol
    connection_port = Column(String)  # Connection port
    connection_status = Column(String, default="active")  # active, inactive, failed, maintenance
    
    # Performance impact
    performance_impact = Column(String, default="medium")  # low, medium, high, critical
    resource_consumption = Column(Float)  # Resource consumption percentage
    bandwidth_usage = Column(Float)  # Bandwidth usage in Mbps
    latency_contribution = Column(Float)  # Latency contribution in milliseconds
    
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
    device = relationship("Device", back_populates="links") 