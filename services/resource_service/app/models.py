from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class Resource(Base):
    __tablename__ = "resource"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    # Core resource fields
    name = Column(String, nullable=False)
    description = Column(Text)
    resource_type = Column(String, nullable=False, default="human")  # human, system, financial, knowledge
    quantity = Column(Float, default=1.0)  # Quantity of the resource
    unit_of_measure = Column(String, default="unit")  # Unit of measurement (FTE, hours, dollars, etc.)
    
    # Availability and allocation
    availability = Column(Float, default=100.0)  # Percentage availability
    allocated_quantity = Column(Float, default=0.0)  # Currently allocated quantity
    available_quantity = Column(Float, default=1.0)  # Available quantity (quantity - allocated)
    
    # Location and deployment
    location = Column(String)  # Physical or logical location
    deployment_status = Column(String, default="active")  # active, inactive, planned, retired
    
    # Criticality and importance
    criticality = Column(String, default="medium")  # low, medium, high, critical
    strategic_importance = Column(String, default="medium")  # low, medium, high, critical
    business_value = Column(String, default="medium")  # low, medium, high, critical
    
    # Cost and financial aspects
    cost_per_unit = Column(Float)  # Cost per unit of the resource
    total_cost = Column(Float)  # Total cost of the resource
    budget_allocation = Column(Float)  # Budget allocated to this resource
    cost_center = Column(String)  # Cost center identifier
    
    # Skills and capabilities
    skills_required = Column(Text)  # JSON string of required skills
    capabilities_provided = Column(Text)  # JSON string of capabilities provided
    expertise_level = Column(String, default="intermediate")  # beginner, intermediate, expert, specialist
    
    # Performance and metrics
    performance_metrics = Column(Text)  # JSON string of performance metrics
    utilization_rate = Column(Float, default=0.0)  # Current utilization percentage
    efficiency_score = Column(Float, default=0.0)  # Efficiency score (0.0 to 1.0)
    effectiveness_score = Column(Float, default=0.0)  # Effectiveness score (0.0 to 1.0)
    
    # Operational characteristics
    operational_hours = Column(String, default="business_hours")  # 24x7, business_hours, on_demand
    maintenance_schedule = Column(String)  # Maintenance schedule
    last_maintenance = Column(DateTime)
    next_maintenance = Column(DateTime)
    
    # Technology and system aspects
    technology_stack = Column(Text)  # JSON string of technology stack
    system_requirements = Column(Text)  # JSON string of system requirements
    integration_points = Column(Text)  # JSON string of integration points
    dependencies = Column(Text)  # JSON string of dependencies
    
    # Governance and compliance
    governance_model = Column(String, default="standard")  # basic, standard, enhanced, critical
    compliance_requirements = Column(Text)  # JSON string of compliance requirements
    audit_requirements = Column(Text)  # JSON string of audit requirements
    risk_assessment = Column(Text)  # JSON string of risk assessment
    
    # Relationships and associations
    associated_capability_id = Column(UUID(as_uuid=True), ForeignKey("capability.id"))
    parent_resource_id = Column(UUID(as_uuid=True), ForeignKey("resource.id"))
    business_function_id = Column(UUID(as_uuid=True), ForeignKey("business_function.id"))
    application_component_id = Column(UUID(as_uuid=True), ForeignKey("application_component.id"))
    node_id = Column(UUID(as_uuid=True), ForeignKey("node.id"))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = relationship("ResourceLink", back_populates="resource")
    child_resources = relationship("Resource", backref="parent_resource", remote_side=[id])

class ResourceLink(Base):
    __tablename__ = "resource_link"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_id = Column(UUID(as_uuid=True), ForeignKey("resource.id"), nullable=False)
    linked_element_id = Column(UUID(as_uuid=True), nullable=False)
    linked_element_type = Column(String, nullable=False)  # goal, constraint, business_function, application_component, node, capability, etc.
    link_type = Column(String, nullable=False)  # enables, supports, realizes, governs, influences, consumes, produces, requires
    relationship_strength = Column(String, default="medium")  # strong, medium, weak
    dependency_level = Column(String, default="medium")  # high, medium, low
    
    # Allocation context
    allocation_percentage = Column(Float, default=0.0)  # Percentage of resource allocated
    allocation_start_date = Column(DateTime)  # Start date of allocation
    allocation_end_date = Column(DateTime)  # End date of allocation
    allocation_priority = Column(String, default="normal")  # low, normal, high, critical
    
    # Operational context
    interaction_frequency = Column(String, default="regular")  # frequent, regular, occasional, rare
    interaction_type = Column(String, default="synchronous")  # synchronous, asynchronous, batch, real_time
    data_flow_direction = Column(String, default="bidirectional")  # input, output, bidirectional
    
    # Performance impact
    performance_impact = Column(String, default="low")  # low, medium, high, critical
    efficiency_contribution = Column(Float)  # Efficiency contribution percentage
    effectiveness_contribution = Column(Float)  # Effectiveness contribution percentage
    
    # Traceability
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resource = relationship("Resource", back_populates="links") 