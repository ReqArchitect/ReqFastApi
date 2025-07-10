from sqlalchemy import Column, String, DateTime, Integer, Float, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid
from datetime import datetime

class ValidationCycle(Base):
    """Model for validation cycles"""
    __tablename__ = "validation_cycles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, nullable=False, index=True)
    start_time = Column(DateTime, default=func.now(), nullable=False)
    end_time = Column(DateTime, nullable=True)
    triggered_by = Column(String, nullable=False)  # user_id or "system"
    rule_set_id = Column(String, nullable=True)
    total_issues_found = Column(Integer, default=0)
    execution_status = Column(String, default="running")  # running, completed, failed
    maturity_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    issues = relationship("ValidationIssue", back_populates="validation_cycle")

class ValidationIssue(Base):
    """Model for validation issues"""
    __tablename__ = "validation_issues"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, nullable=False, index=True)
    validation_cycle_id = Column(String, ForeignKey("validation_cycles.id"), nullable=True)
    entity_type = Column(String, nullable=False)  # goal, capability, process, etc.
    entity_id = Column(String, nullable=False)
    issue_type = Column(String, nullable=False)  # missing_link, orphaned, stale, invalid_enum, broken_traceability
    severity = Column(String, nullable=False)  # low, medium, high, critical
    description = Column(Text, nullable=False)
    recommended_fix = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)  # Additional context
    timestamp = Column(DateTime, default=func.now())
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(String, nullable=True)
    
    # Relationships
    validation_cycle = relationship("ValidationCycle", back_populates="issues")

class ValidationRule(Base):
    """Model for validation rules"""
    __tablename__ = "validation_rules"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    rule_type = Column(String, nullable=False)  # traceability, completeness, alignment
    scope = Column(String, nullable=False)  # Motivation, Business, Application, Technology, Implementation
    rule_logic = Column(Text, nullable=False)  # JSON or code representation
    is_active = Column(Boolean, default=True)
    severity = Column(String, default="medium")  # low, medium, high, critical
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ValidationException(Base):
    """Model for whitelisted intentional modeling gaps"""
    __tablename__ = "validation_exceptions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, nullable=False, index=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    rule_id = Column(String, ForeignKey("validation_rules.id"), nullable=True)
    reason = Column(Text, nullable=False)
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=True)  # Optional expiration
    is_active = Column(Boolean, default=True)
    
    # Relationships
    rule = relationship("ValidationRule")

class ValidationScorecard(Base):
    """Model for validation scorecards"""
    __tablename__ = "validation_scorecards"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, nullable=False, index=True)
    validation_cycle_id = Column(String, ForeignKey("validation_cycles.id"), nullable=False)
    layer = Column(String, nullable=False)  # Motivation, Business, Application, Technology, Implementation
    completeness_score = Column(Float, nullable=False)
    traceability_score = Column(Float, nullable=False)
    alignment_score = Column(Float, nullable=False)
    overall_score = Column(Float, nullable=False)
    issues_count = Column(Integer, default=0)
    critical_issues = Column(Integer, default=0)
    high_issues = Column(Integer, default=0)
    medium_issues = Column(Integer, default=0)
    low_issues = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    validation_cycle = relationship("ValidationCycle")

class TraceabilityMatrix(Base):
    """Model for storing traceability matrix data"""
    __tablename__ = "traceability_matrix"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, nullable=False, index=True)
    source_layer = Column(String, nullable=False)
    target_layer = Column(String, nullable=False)
    source_entity_type = Column(String, nullable=False)
    target_entity_type = Column(String, nullable=False)
    relationship_type = Column(String, nullable=False)
    connection_count = Column(Integer, default=0)
    missing_connections = Column(Integer, default=0)
    strength_score = Column(Float, nullable=True)
    last_updated = Column(DateTime, default=func.now()) 