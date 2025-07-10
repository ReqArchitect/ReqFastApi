from pydantic import BaseModel, Field, validator, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import json

# Enums matching the SQLAlchemy models
class PackageType(str, Enum):
    PROJECT = "project"
    EPIC = "epic"
    TASK = "task"
    RELEASE = "release"
    PHASE = "phase"
    SPRINT = "sprint"
    INITIATIVE = "initiative"
    MILESTONE = "milestone"

class PackageStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DELAYED = "delayed"
    BLOCKED = "blocked"

class DeliveryRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class LinkType(str, Enum):
    REALIZES = "realizes"
    CLOSES = "closes"
    DELIVERS = "delivers"
    SUPPORTS = "supports"
    ENABLES = "enables"
    IMPACTS = "impacts"
    DEPENDS_ON = "depends_on"
    CONTRIBUTES_TO = "contributes_to"

class RelationshipStrength(str, Enum):
    STRONG = "strong"
    MEDIUM = "medium"
    WEAK = "weak"

class DependencyLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Base schemas
class WorkPackageBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Work package name")
    description: Optional[str] = Field(None, description="Work package description")
    package_type: PackageType = Field(..., description="Type of work package")
    
    # Strategic alignment
    strategic_driver_id: Optional[UUID4] = Field(None, description="Related strategic driver ID")
    related_goal_id: Optional[UUID4] = Field(None, description="Related goal ID")
    target_plateau_id: Optional[UUID4] = Field(None, description="Target plateau ID")
    
    # Scope and impact
    impacted_capabilities: Optional[str] = Field(None, description="JSON array of impacted capability IDs")
    impacted_application_components: Optional[str] = Field(None, description="JSON array of impacted application component IDs")
    impacted_technology_nodes: Optional[str] = Field(None, description="JSON array of impacted technology node IDs")
    
    # Scheduling and timeline
    scheduled_start: Optional[datetime] = Field(None, description="Scheduled start date")
    scheduled_end: Optional[datetime] = Field(None, description="Scheduled end date")
    actual_start: Optional[datetime] = Field(None, description="Actual start date")
    actual_end: Optional[datetime] = Field(None, description="Actual end date")
    
    # Status and progress
    current_status: PackageStatus = Field(PackageStatus.PLANNED, description="Current status")
    progress_percent: float = Field(0.0, ge=0.0, le=100.0, description="Progress percentage")
    
    # Risk and quality
    delivery_risk: DeliveryRisk = Field(DeliveryRisk.MEDIUM, description="Delivery risk level")
    quality_gates: Optional[str] = Field(None, description="JSON array of quality gate definitions")
    risk_mitigation_plan: Optional[str] = Field(None, description="Risk mitigation plan")
    
    # Resource allocation
    estimated_effort_hours: Optional[float] = Field(None, ge=0.0, description="Estimated effort in hours")
    actual_effort_hours: float = Field(0.0, ge=0.0, description="Actual effort in hours")
    budget_allocation: Optional[float] = Field(None, ge=0.0, description="Budget allocation")
    actual_cost: float = Field(0.0, ge=0.0, description="Actual cost")
    
    # Team and ownership
    change_owner_id: Optional[UUID4] = Field(None, description="Change owner ID")
    team_members: Optional[str] = Field(None, description="JSON array of team member IDs")
    stakeholders: Optional[str] = Field(None, description="JSON array of stakeholder IDs")
    
    # Dependencies and relationships
    dependencies: Optional[str] = Field(None, description="JSON array of dependent work package IDs")
    blockers: Optional[str] = Field(None, description="JSON array of blocking work package IDs")
    
    # Quality and compliance
    quality_metrics: Optional[str] = Field(None, description="JSON object of quality metrics")
    compliance_requirements: Optional[str] = Field(None, description="JSON array of compliance requirements")
    audit_trail: Optional[str] = Field(None, description="JSON array of audit events")
    
    # Monitoring and reporting
    kpis: Optional[str] = Field(None, description="JSON object of key performance indicators")
    reporting_frequency: str = Field("weekly", description="Reporting frequency")
    escalation_path: Optional[str] = Field(None, description="JSON object of escalation contacts")
    
    # Metadata
    tags: Optional[str] = Field(None, description="JSON array of tags")
    priority: int = Field(3, ge=1, le=4, description="Priority (1=Critical, 2=High, 3=Medium, 4=Low)")
    complexity: str = Field("medium", description="Complexity level")

    @validator('impacted_capabilities', 'impacted_application_components', 'impacted_technology_nodes', 
               'team_members', 'stakeholders', 'dependencies', 'blockers', 'compliance_requirements', 
               'audit_trail', 'tags')
    def validate_json_array(cls, v):
        if v is not None:
            try:
                data = json.loads(v)
                if not isinstance(data, list):
                    raise ValueError("Must be a valid JSON array")
            except json.JSONDecodeError:
                raise ValueError("Must be valid JSON")
        return v

    @validator('quality_gates', 'quality_metrics', 'kpis', 'escalation_path')
    def validate_json_object(cls, v):
        if v is not None:
            try:
                data = json.loads(v)
                if not isinstance(data, dict):
                    raise ValueError("Must be a valid JSON object")
            except json.JSONDecodeError:
                raise ValueError("Must be valid JSON")
        return v

    @validator('scheduled_end')
    def validate_scheduled_end(cls, v, values):
        if v and 'scheduled_start' in values and values['scheduled_start']:
            if v <= values['scheduled_start']:
                raise ValueError("Scheduled end must be after scheduled start")
        return v

    @validator('actual_end')
    def validate_actual_end(cls, v, values):
        if v and 'actual_start' in values and values['actual_start']:
            if v <= values['actual_start']:
                raise ValueError("Actual end must be after actual start")
        return v

    @validator('progress_percent')
    def validate_progress_percent(cls, v):
        if v < 0 or v > 100:
            raise ValueError("Progress percentage must be between 0 and 100")
        return v

class WorkPackageCreate(WorkPackageBase):
    pass

class WorkPackageUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    package_type: Optional[PackageType] = None
    strategic_driver_id: Optional[UUID4] = None
    related_goal_id: Optional[UUID4] = None
    target_plateau_id: Optional[UUID4] = None
    impacted_capabilities: Optional[str] = None
    impacted_application_components: Optional[str] = None
    impacted_technology_nodes: Optional[str] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    current_status: Optional[PackageStatus] = None
    progress_percent: Optional[float] = Field(None, ge=0.0, le=100.0)
    delivery_risk: Optional[DeliveryRisk] = None
    quality_gates: Optional[str] = None
    risk_mitigation_plan: Optional[str] = None
    estimated_effort_hours: Optional[float] = Field(None, ge=0.0)
    actual_effort_hours: Optional[float] = Field(None, ge=0.0)
    budget_allocation: Optional[float] = Field(None, ge=0.0)
    actual_cost: Optional[float] = Field(None, ge=0.0)
    change_owner_id: Optional[UUID4] = None
    team_members: Optional[str] = None
    stakeholders: Optional[str] = None
    dependencies: Optional[str] = None
    blockers: Optional[str] = None
    quality_metrics: Optional[str] = None
    compliance_requirements: Optional[str] = None
    audit_trail: Optional[str] = None
    kpis: Optional[str] = None
    reporting_frequency: Optional[str] = None
    escalation_path: Optional[str] = None
    tags: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=4)
    complexity: Optional[str] = None

    @validator('impacted_capabilities', 'impacted_application_components', 'impacted_technology_nodes', 
               'team_members', 'stakeholders', 'dependencies', 'blockers', 'compliance_requirements', 
               'audit_trail', 'tags')
    def validate_json_array(cls, v):
        if v is not None:
            try:
                data = json.loads(v)
                if not isinstance(data, list):
                    raise ValueError("Must be a valid JSON array")
            except json.JSONDecodeError:
                raise ValueError("Must be valid JSON")
        return v

    @validator('quality_gates', 'quality_metrics', 'kpis', 'escalation_path')
    def validate_json_object(cls, v):
        if v is not None:
            try:
                data = json.loads(v)
                if not isinstance(data, dict):
                    raise ValueError("Must be a valid JSON object")
            except json.JSONDecodeError:
                raise ValueError("Must be valid JSON")
        return v

class WorkPackageResponse(WorkPackageBase):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WorkPackageList(BaseModel):
    id: UUID4
    name: str
    package_type: PackageType
    current_status: PackageStatus
    progress_percent: float
    delivery_risk: DeliveryRisk
    scheduled_start: Optional[datetime]
    scheduled_end: Optional[datetime]
    estimated_effort_hours: Optional[float]
    budget_allocation: Optional[float]
    priority: int
    created_at: datetime

    class Config:
        from_attributes = True

# Package Link schemas
class PackageLinkBase(BaseModel):
    linked_element_id: UUID4 = Field(..., description="Linked element ID")
    linked_element_type: str = Field(..., min_length=1, max_length=100, description="Type of linked element")
    link_type: LinkType = Field(..., description="Type of link")
    relationship_strength: RelationshipStrength = Field(RelationshipStrength.MEDIUM, description="Relationship strength")
    dependency_level: DependencyLevel = Field(DependencyLevel.MEDIUM, description="Dependency level")
    impact_level: str = Field("medium", description="Impact level")
    impact_description: Optional[str] = Field(None, description="Impact description")
    impact_metrics: Optional[str] = Field(None, description="JSON object of impact measurements")
    traceability_score: float = Field(0.0, ge=0.0, le=1.0, description="Traceability score")
    traceability_evidence: Optional[str] = Field(None, description="JSON array of evidence items")
    is_validated: bool = Field(False, description="Validation status")
    validation_date: Optional[datetime] = Field(None, description="Validation date")
    validated_by: Optional[UUID4] = Field(None, description="Validated by user ID")

    @validator('impact_metrics', 'traceability_evidence')
    def validate_json(cls, v):
        if v is not None:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Must be valid JSON")
        return v

    @validator('traceability_score')
    def validate_traceability_score(cls, v):
        if v < 0 or v > 1:
            raise ValueError("Traceability score must be between 0 and 1")
        return v

class PackageLinkCreate(PackageLinkBase):
    pass

class PackageLinkUpdate(BaseModel):
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=100)
    link_type: Optional[LinkType] = None
    relationship_strength: Optional[RelationshipStrength] = None
    dependency_level: Optional[DependencyLevel] = None
    impact_level: Optional[str] = None
    impact_description: Optional[str] = None
    impact_metrics: Optional[str] = None
    traceability_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    traceability_evidence: Optional[str] = None
    is_validated: Optional[bool] = None
    validation_date: Optional[datetime] = None
    validated_by: Optional[UUID4] = None

    @validator('impact_metrics', 'traceability_evidence')
    def validate_json(cls, v):
        if v is not None:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Must be valid JSON")
        return v

class PackageLinkResponse(PackageLinkBase):
    id: UUID4
    work_package_id: UUID4
    created_by: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Analysis schemas
class ExecutionStatusResponse(BaseModel):
    work_package_id: UUID4
    overall_status: str
    progress_analysis: Dict[str, Any]
    timeline_analysis: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    quality_gates_status: Dict[str, Any]
    resource_utilization: Dict[str, Any]
    recommendations: List[str]

class GapClosureMapResponse(BaseModel):
    work_package_id: UUID4
    gaps_addressed: List[Dict[str, Any]]
    closure_progress: Dict[str, Any]
    impact_assessment: Dict[str, Any]
    traceability_matrix: Dict[str, Any]
    validation_status: Dict[str, Any]

# Enum response schemas
class EnumResponse(BaseModel):
    values: List[str]

# Health check schema
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    service: str
    version: str
    database: str
    redis: str

# Error response schema
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime 