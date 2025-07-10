from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class IssueType(str, Enum):
    MISSING_LINK = "missing_link"
    ORPHANED = "orphaned"
    STALE = "stale"
    INVALID_ENUM = "invalid_enum"
    BROKEN_TRACEABILITY = "broken_traceability"

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RuleType(str, Enum):
    TRACEABILITY = "traceability"
    COMPLETENESS = "completeness"
    ALIGNMENT = "alignment"

class Scope(str, Enum):
    MOTIVATION = "Motivation"
    BUSINESS = "Business"
    APPLICATION = "Application"
    TECHNOLOGY = "Technology"
    IMPLEMENTATION = "Implementation"

class ExecutionStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

# Request/Response Schemas

class ValidationCycleBase(BaseModel):
    tenant_id: str
    triggered_by: str
    rule_set_id: Optional[str] = None

class ValidationCycleCreate(ValidationCycleBase):
    pass

class ValidationCycleResponse(ValidationCycleBase):
    id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_issues_found: int
    execution_status: ExecutionStatus
    maturity_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime

class ValidationIssueBase(BaseModel):
    tenant_id: str
    entity_type: str
    entity_id: str
    issue_type: IssueType
    severity: Severity
    description: str
    recommended_fix: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ValidationIssueCreate(ValidationIssueBase):
    validation_cycle_id: Optional[str] = None

class ValidationIssueResponse(ValidationIssueBase):
    id: str
    validation_cycle_id: Optional[str] = None
    timestamp: datetime
    is_resolved: bool
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None

class ValidationRuleBase(BaseModel):
    name: str
    description: str
    rule_type: RuleType
    scope: Scope
    rule_logic: str
    severity: Severity = Severity.MEDIUM

class ValidationRuleCreate(ValidationRuleBase):
    pass

class ValidationRuleUpdate(BaseModel):
    description: Optional[str] = None
    rule_logic: Optional[str] = None
    is_active: Optional[bool] = None
    severity: Optional[Severity] = None

class ValidationRuleResponse(ValidationRuleBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

class ValidationExceptionBase(BaseModel):
    tenant_id: str
    entity_type: str
    entity_id: str
    rule_id: Optional[str] = None
    reason: str
    expires_at: Optional[datetime] = None

class ValidationExceptionCreate(ValidationExceptionBase):
    pass

class ValidationExceptionResponse(ValidationExceptionBase):
    id: str
    created_by: str
    created_at: datetime
    is_active: bool

class ValidationScorecardResponse(BaseModel):
    id: str
    tenant_id: str
    validation_cycle_id: str
    layer: str
    completeness_score: float
    traceability_score: float
    alignment_score: float
    overall_score: float
    issues_count: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    created_at: datetime

class TraceabilityMatrixResponse(BaseModel):
    id: str
    tenant_id: str
    source_layer: str
    target_layer: str
    source_entity_type: str
    target_entity_type: str
    relationship_type: str
    connection_count: int
    missing_connections: int
    strength_score: Optional[float] = None
    last_updated: datetime

class ValidationRunRequest(BaseModel):
    rule_set_id: Optional[str] = None
    force_full_scan: bool = False

class ValidationRunResponse(BaseModel):
    validation_cycle_id: str
    status: ExecutionStatus
    message: str

class IssuesListResponse(BaseModel):
    issues: List[ValidationIssueResponse]
    total_count: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int

class ScorecardResponse(BaseModel):
    tenant_id: str
    validation_cycle_id: str
    overall_maturity_score: float
    layer_scores: List[ValidationScorecardResponse]
    summary: Dict[str, Any]

class TraceabilityMatrixRequest(BaseModel):
    source_layer: Optional[str] = None
    target_layer: Optional[str] = None
    entity_type: Optional[str] = None

class ValidationHistoryResponse(BaseModel):
    cycles: List[ValidationCycleResponse]
    total_cycles: int
    average_maturity_score: float
    last_validation_date: Optional[datetime] = None

class ExceptionCreateRequest(BaseModel):
    entity_type: str
    entity_id: str
    rule_id: Optional[str] = None
    reason: str
    expires_at: Optional[datetime] = None

class RuleToggleRequest(BaseModel):
    is_active: bool

# Validation Engine Schemas

class TracePath(BaseModel):
    """Represents a traceability path between elements"""
    source_entity: str
    target_entity: str
    relationship_type: str
    strength: float = 1.0
    metadata: Optional[Dict[str, Any]] = None

class ValidationContext(BaseModel):
    """Context for validation operations"""
    tenant_id: str
    user_id: str
    validation_cycle_id: str
    rule_set_id: Optional[str] = None
    exceptions: List[ValidationExceptionResponse] = []

class ValidationResult(BaseModel):
    """Result of a validation operation"""
    rule_id: str
    rule_name: str
    passed: bool
    issues_found: List[ValidationIssueCreate]
    execution_time_ms: float
    metadata: Optional[Dict[str, Any]] = None

class ArchitectureElement(BaseModel):
    """Represents an architecture element for validation"""
    id: str
    type: str
    name: str
    layer: str
    properties: Dict[str, Any]
    relationships: List[Dict[str, Any]]
    last_modified: Optional[datetime] = None
    created_at: Optional[datetime] = None

class ValidationMetrics(BaseModel):
    """Metrics for validation performance"""
    total_elements_checked: int
    total_issues_found: int
    validation_duration_ms: float
    memory_usage_mb: float
    cache_hit_rate: float 