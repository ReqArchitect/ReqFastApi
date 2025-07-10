from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class ApplicationFunction(Base):
    __tablename__ = "application_function"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core application function fields
    name = Column(String, nullable=False)
    description = Column(Text)
    purpose = Column(Text)  # Purpose and responsibility of the function
    
    # Technology and implementation
    technology_stack = Column(Text)  # JSON string of technology stack
    module_location = Column(String)  # Physical or logical location of the function
    function_type = Column(String, nullable=False, default="data_processing")  # data_processing, orchestration, user_interaction, rule_engine, etl_processor, user_session_manager, event_handler, ui_controller
    
    # Performance characteristics
    performance_characteristics = Column(Text)  # JSON string of performance metrics
    response_time_target = Column(Float)  # Target response time in milliseconds
    throughput_target = Column(Float)  # Target throughput (requests per second)
    availability_target = Column(Float, default=99.9)  # Availability target percentage
    current_availability = Column(Float, default=100.0)  # Current availability percentage
    
    # Business alignment
    supported_business_function_id = Column(UUID(as_uuid=True), ForeignKey("business_function.id"))
    business_criticality = Column(String, default="medium")  # low, medium, high, critical
    business_value = Column(String, default="medium")  # low, medium, high, critical
    
    # Operational characteristics
    status = Column(String, nullable=False, default="active")  # active, inactive, deprecated, planned, maintenance
    operational_hours = Column(String, default="24x7")  # 24x7, business_hours, on_demand
    maintenance_window = Column(String)  # Maintenance window schedule
    last_maintenance = Column(DateTime)
    next_maintenance = Column(DateTime)
    
    # Technical specifications
    api_endpoints = Column(Text)  # JSON string of API endpoints
    data_sources = Column(Text)  # JSON string of data sources
    data_sinks = Column(Text)  # JSON string of data sinks
    error_handling = Column(Text)  # JSON string of error handling strategies
    logging_config = Column(Text)  # JSON string of logging configuration
    
    # Security and compliance
    security_level = Column(String, default="standard")  # basic, standard, high, critical
    compliance_requirements = Column(Text)  # JSON string of compliance requirements
    access_controls = Column(Text)  # JSON string of access controls
    audit_requirements = Column(Text)  # JSON string of audit requirements
    
    # Monitoring and observability
    monitoring_config = Column(Text)  # JSON string of monitoring configuration
    alerting_rules = Column(Text)  # JSON string of alerting rules
    health_check_endpoint = Column(String)  # Health check endpoint URL
    metrics_endpoint = Column(String)  # Metrics endpoint URL
    
    # Dependencies and relationships
    parent_function_id = Column(UUID(as_uuid=True), ForeignKey("application_function.id"))
    application_service_id = Column(UUID(as_uuid=True), ForeignKey("application_service.id"))
    data_object_id = Column(UUID(as_uuid=True), ForeignKey("data_object.id"))
    node_id = Column(UUID(as_uuid=True), ForeignKey("node.id"))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("FunctionLink", back_populates="application_function")
    child_functions = relationship("ApplicationFunction", backref="parent_function", remote_side=[id])

class FunctionLink(Base):
    __tablename__ = "function_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_function_id = Column(UUID(as_uuid=True), ForeignKey("application_function.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # business_function, business_process, capability, application_service, data_object, node, etc.
    link_type = Column(String, nullable=False)  # realizes, supports, enables, governs, influences, consumes, produces, triggers
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Operational context
    interaction_frequency = Column(String, default="regular")  # frequent, regular, occasional, rare
    interaction_type = Column(String, default="synchronous")  # synchronous, asynchronous, batch, real_time, event_driven
    data_flow_direction = Column(String, default="bidirectional")  # input, output, bidirectional
    
    # Performance impact
    performance_impact = Column(String, default="low")  # low, medium, high, critical
    latency_contribution = Column(Float)  # Latency contribution in milliseconds
    throughput_impact = Column(Float)  # Throughput impact percentage
    
    # Traceability
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    application_function = relationship("ApplicationFunction", back_populates="links") 