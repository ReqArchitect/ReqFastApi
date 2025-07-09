from pydantic import BaseModel, UUID4, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RequirementType(str, Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non-functional"
    BUSINESS = "business"
    TECHNICAL = "technical"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Status(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    DEPRECATED = "deprecated"

class LinkType(str, Enum):
    IMPLEMENTS = "implements"
    DEPENDS_ON = "depends_on"
    CONFLICTS_WITH = "conflicts_with"
    ENHANCES = "enhances"

class LinkStrength(str, Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"

# Base schemas
class RequirementBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    requirement_type: RequirementType
    priority: Priority = Priority.MEDIUM
    status: Status = Status.DRAFT
    source: Optional[str] = None
    stakeholder_id: Optional[UUID4] = None
    business_case_id: Optional[UUID4] = None
    initiative_id: Optional[UUID4] = None
    acceptance_criteria: Optional[str] = None
    validation_method: Optional[str] = None
    compliance_required: bool = False

class RequirementCreate(RequirementBase):
    pass

class RequirementUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    requirement_type: Optional[RequirementType] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    source: Optional[str] = None
    stakeholder_id: Optional[UUID4] = None
    business_case_id: Optional[UUID4] = None
    initiative_id: Optional[UUID4] = None
    acceptance_criteria: Optional[str] = None
    validation_method: Optional[str] = None
    compliance_required: Optional[bool] = None

class RequirementInDBBase(RequirementBase):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Requirement(RequirementInDBBase):
    pass

# Link schemas
class RequirementLinkBase(BaseModel):
    linked_element_id: UUID4
    linked_element_type: str = Field(..., min_length=1, max_length=100)
    link_type: LinkType
    link_strength: LinkStrength = LinkStrength.MEDIUM

class RequirementLinkCreate(RequirementLinkBase):
    pass

class RequirementLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID4] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=100)
    link_type: Optional[LinkType] = None
    link_strength: Optional[LinkStrength] = None

class RequirementLinkInDBBase(RequirementLinkBase):
    id: UUID4
    requirement_id: UUID4
    created_by: UUID4
    created_at: datetime

    class Config:
        orm_mode = True

class RequirementLink(RequirementLinkInDBBase):
    pass

# Response schemas
class RequirementWithLinks(Requirement):
    links: List[RequirementLink] = []

class RequirementList(BaseModel):
    requirements: List[Requirement]
    total: int
    skip: int
    limit: int

class TraceabilityCheck(BaseModel):
    requirement_id: UUID4
    linked_elements_count: int
    compliance_status: str
    validation_status: str
    last_updated: datetime

class ImpactSummary(BaseModel):
    requirement_id: UUID4
    direct_impact_count: int
    indirect_impact_count: int
    affected_layers: List[str]
    risk_level: str
    last_assessed: datetime 