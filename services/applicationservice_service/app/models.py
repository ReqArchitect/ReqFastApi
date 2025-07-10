from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class ApplicationService(Base):
    __tablename__ = "application_service"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core application service fields
    name = Column(String, nullable=False)
    description = Column(Text)
    service_type = Column(String, nullable=False, default="api")  # ui, api, data, integration, messaging
    exposed_function_id = Column(UUID(as_uuid=True), ForeignKey("application_function.id"))
    exposed_dataobject_id = Column(UUID(as_uuid=True), ForeignKey("data_object.id"))
    status = Column(String, default="active")  # active, inactive, deprecated, planned, maintenance
    latency_target_ms = Column(Integer, default=200)  # Target latency in milliseconds
    availability_target_pct = Column(Float, default=99.9)  # Target availability percentage
    consumer_role_id = Column(UUID(as_uuid=True), ForeignKey("business_role.id"))
    version = Column(String, default="1.0.0")  # Semantic versioning
    delivery_channel = Column(String, default="http")  # http, https, grpc, websocket, message_queue, file_transfer
    
    # Service configuration
    service_endpoint = Column(String)  # URL or endpoint for the service
    authentication_method = Column(String, default="none")  # none, basic, oauth, jwt, api_key
    rate_limiting = Column(Text)  # JSON string of rate limiting configuration
    caching_strategy = Column(Text)  # JSON string of caching configuration
    load_balancing = Column(Text)  # JSON string of load balancing configuration
    
    # Performance and monitoring
    current_latency_ms = Column(Integer)  # Current measured latency
    current_availability_pct = Column(Float)  # Current measured availability
    uptime_percentage = Column(Float)  # Overall uptime percentage
    error_rate = Column(Float)  # Error rate percentage
    throughput_rps = Column(Float)  # Requests per second
    
    # Service dependencies
    dependencies = Column(Text)  # JSON string of service dependencies
    required_services = Column(Text)  # JSON string of required services
    optional_services = Column(Text)  # JSON string of optional services
    
    # Business context
    business_process_id = Column(UUID(as_uuid=True), ForeignKey("business_process.id"))
    capability_id = Column(UUID(as_uuid=True), ForeignKey("capability.id"))
    business_value = Column(String, default="medium")  # low, medium, high, critical
    business_criticality = Column(String, default="medium")  # low, medium, high, critical
    
    # Technical specifications
    technology_stack = Column(Text)  # JSON string of technology stack
    deployment_model = Column(String, default="monolithic")  # monolithic, microservice, serverless, container
    scaling_strategy = Column(String, default="horizontal")  # horizontal, vertical, auto
    backup_strategy = Column(Text)  # JSON string of backup configuration
    
    # Security and compliance
    security_level = Column(String, default="standard")  # basic, standard, high, critical
    compliance_requirements = Column(Text)  # JSON string of compliance requirements
    data_classification = Column(String, default="internal")  # public, internal, confidential, restricted
    encryption_requirements = Column(Text)  # JSON string of encryption requirements
    
    # Documentation and support
    documentation_link = Column(String)  # URL to documentation
    api_documentation = Column(Text)  # JSON string of API documentation
    support_contact = Column(String)  # Support contact information
    maintenance_window = Column(String)  # Maintenance window schedule
    
    # Operational metrics
    last_deployment = Column(DateTime)
    next_deployment = Column(DateTime)
    incident_count = Column(Integer, default=0)
    last_incident = Column(DateTime)
    sla_breaches = Column(Integer, default=0)
    
    # Service quality metrics
    response_time_p95 = Column(Integer)  # 95th percentile response time
    response_time_p99 = Column(Integer)  # 99th percentile response time
    success_rate = Column(Float)  # Success rate percentage
    user_satisfaction = Column(Float)  # User satisfaction score
    
    # Cost and resource metrics
    monthly_cost = Column(Float)  # Monthly operational cost
    resource_utilization = Column(Float)  # Resource utilization percentage
    capacity_planning = Column(Text)  # JSON string of capacity planning data
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("ServiceLink", back_populates="application_service")

class ServiceLink(Base):
    __tablename__ = "service_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_service_id = Column(UUID(as_uuid=True), ForeignKey("application_service.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # business_process, application_function, capability, node, data_object, etc.
    link_type = Column(String, nullable=False)  # realizes, supports, enables, consumes, produces, triggers, requires
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Service interaction context
    interaction_frequency = Column(String, default="regular")  # frequent, regular, occasional, rare
    interaction_type = Column(String, default="synchronous")  # synchronous, asynchronous, batch, real_time
    data_flow_direction = Column(String, default="bidirectional")  # input, output, bidirectional
    performance_impact = Column(String, default="medium")  # low, medium, high, critical
    
    # Service quality impact
    latency_contribution = Column(Float)  # Latency contribution in milliseconds
    availability_impact = Column(Float)  # Availability impact percentage
    throughput_impact = Column(Float)  # Throughput impact percentage
    error_propagation = Column(Float)  # Error propagation percentage
    
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
    application_service = relationship("ApplicationService", back_populates="links") 