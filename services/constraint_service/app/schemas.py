from pydantic import BaseModel, UUID4, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ConstraintType(str, Enum):
    TECHNICAL = "technical"
    REGULATORY = "regulatory"
    ORGANIZATIONAL = "organizational"
    ENVIRONMENTAL = "environmental"
    FINANCIAL = "financial"

class Scope(str, Enum):
    GLOBAL = "global"
    DOMAIN = "domain"
    PROJECT = "project"
    COMPONENT = "component"

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class EnforcementLevel(str, Enum):
    MANDATORY = "mandatory"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"

class RiskProfile(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class MitigationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"

class MitigationEffort(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ImpactLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ReviewFrequency(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"
    AD_HOC = "ad_hoc"

class LinkType(str, Enum):
    CONSTRAINS = "constrains"
    LIMITS = "limits"
    RESTRICTS = "restricts"
    GOVERNS = "governs"
    REGULATES = "regulates"

class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    EXEMPT = "exempt"

# Base schemas
class ConstraintBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    constraint_type: ConstraintType
    scope: Scope
    severity: Severity = Severity.MEDIUM
    enforcement_level: EnforcementLevel = EnforcementLevel.MANDATORY
    stakeholder_id: Optional[UUID4] = None
    business_actor_id: Optional[UUID4] = None
    risk_profile: RiskProfile = RiskProfile.MEDIUM
    compliance_required: bool = False
    regulatory_framework: Optional[str] = None
    mitigation_strategy: Optional[str] = None
    mitigation_status: MitigationStatus = MitigationStatus.PENDING
    mitigation_effort: MitigationEffort = MitigationEffort.MEDIUM
    business_impact: ImpactLevel = ImpactLevel.MEDIUM
    technical_impact: ImpactLevel = ImpactLevel.MEDIUM
    operational_impact: ImpactLevel = ImpactLevel.MEDIUM
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    review_frequency: Optional[ReviewFrequency] = None

class ConstraintCreate(ConstraintBase):
    pass

class ConstraintUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    constraint_type: Optional[ConstraintType] = None
    scope: Optional[Scope] = None
    severity: Optional[Severity] = None
    enforcement_level: Optional[EnforcementLevel] = None
    stakeholder_id: Optional[UUID4] = None
    business_actor_id: Optional[UUID4] = None
    risk_profile: Optional[RiskProfile] = None
    compliance_required: Optional[bool] = None
    regulatory_framework: Optional[str] = None
    mitigation_strategy: Optional[str] = None
    mitigation_status: Optional[MitigationStatus] = None
    mitigation_effort: Optional[MitigationEffort] = None
    business_impact: Optional[ImpactLevel] = None
    technical_impact: Optional[ImpactLevel] = None
    operational_impact: Optional[ImpactLevel] = None
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    review_frequency: Optional[ReviewFrequency] = None

class ConstraintInDBBase(ConstraintBase):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Constraint(ConstraintInDBBase):
    pass

# Link schemas
class ConstraintLinkBase(BaseModel):
    linked_element_id: UUID4
    linked_element_type: str = Field(..., min_length=1, max_length=100)
    link_type: LinkType
    impact_level: ImpactLevel = ImpactLevel.MEDIUM
    compliance_status: ComplianceStatus = ComplianceStatus.COMPLIANT

class ConstraintLinkCreate(ConstraintLinkBase):
    pass

class ConstraintLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID4] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=100)
    link_type: Optional[LinkType] = None
    impact_level: Optional[ImpactLevel] = None
    compliance_status: Optional[ComplianceStatus] = None

class ConstraintLinkInDBBase(ConstraintLinkBase):
    id: UUID4
    constraint_id: UUID4
    created_by: UUID4
    created_at: datetime

    class Config:
        orm_mode = True

class ConstraintLink(ConstraintLinkInDBBase):
    pass

# Response schemas
class ConstraintWithLinks(Constraint):
    links: List[ConstraintLink] = []

class ConstraintList(BaseModel):
    constraints: List[Constraint]
    total: int
    skip: int
    limit: int

class ImpactMap(BaseModel):
    constraint_id: UUID4
    impacted_elements_count: int
    compliant_elements: int
    non_compliant_elements: int
    partially_compliant_elements: int
    exempt_elements: int
    affected_layers: List[str]
    overall_compliance_score: float
    last_assessed: datetime

class ConstraintAnalysis(BaseModel):
    constraint_id: UUID4
    severity_score: float
    risk_score: float
    compliance_score: float
    business_impact_score: float
    technical_impact_score: float
    operational_impact_score: float
    mitigation_effort_score: float
    overall_impact_score: float
    last_analyzed: datetime 