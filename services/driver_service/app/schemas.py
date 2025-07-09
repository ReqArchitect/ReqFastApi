from pydantic import BaseModel, UUID4, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class DriverType(str, Enum):
    BUSINESS = "business"
    TECHNICAL = "technical"
    REGULATORY = "regulatory"
    ENVIRONMENTAL = "environmental"
    SOCIAL = "social"

class Category(str, Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"

class Urgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ImpactLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TimeHorizon(str, Enum):
    SHORT_TERM = "short-term"
    MEDIUM_TERM = "medium-term"
    LONG_TERM = "long-term"

class GeographicScope(str, Enum):
    LOCAL = "local"
    REGIONAL = "regional"
    NATIONAL = "national"
    GLOBAL = "global"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class LinkType(str, Enum):
    INFLUENCES = "influences"
    DRIVES = "drives"
    CONSTRAINS = "constrains"
    ENABLES = "enables"

class LinkStrength(str, Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"

class InfluenceDirection(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

# Base schemas
class DriverBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    driver_type: DriverType
    category: Category
    urgency: Urgency = Urgency.MEDIUM
    impact_level: ImpactLevel = ImpactLevel.MEDIUM
    source: Optional[str] = None
    stakeholder_id: Optional[UUID4] = None
    business_actor_id: Optional[UUID4] = None
    strategic_priority: int = Field(3, ge=1, le=5)
    time_horizon: Optional[TimeHorizon] = None
    geographic_scope: Optional[GeographicScope] = None
    compliance_required: bool = False
    risk_level: RiskLevel = RiskLevel.MEDIUM

class DriverCreate(DriverBase):
    pass

class DriverUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    driver_type: Optional[DriverType] = None
    category: Optional[Category] = None
    urgency: Optional[Urgency] = None
    impact_level: Optional[ImpactLevel] = None
    source: Optional[str] = None
    stakeholder_id: Optional[UUID4] = None
    business_actor_id: Optional[UUID4] = None
    strategic_priority: Optional[int] = Field(None, ge=1, le=5)
    time_horizon: Optional[TimeHorizon] = None
    geographic_scope: Optional[GeographicScope] = None
    compliance_required: Optional[bool] = None
    risk_level: Optional[RiskLevel] = None

class DriverInDBBase(DriverBase):
    id: UUID4
    tenant_id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Driver(DriverInDBBase):
    pass

# Link schemas
class DriverLinkBase(BaseModel):
    linked_element_id: UUID4
    linked_element_type: str = Field(..., min_length=1, max_length=100)
    link_type: LinkType
    link_strength: LinkStrength = LinkStrength.MEDIUM
    influence_direction: InfluenceDirection = InfluenceDirection.POSITIVE

class DriverLinkCreate(DriverLinkBase):
    pass

class DriverLinkUpdate(BaseModel):
    linked_element_id: Optional[UUID4] = None
    linked_element_type: Optional[str] = Field(None, min_length=1, max_length=100)
    link_type: Optional[LinkType] = None
    link_strength: Optional[LinkStrength] = None
    influence_direction: Optional[InfluenceDirection] = None

class DriverLinkInDBBase(DriverLinkBase):
    id: UUID4
    driver_id: UUID4
    created_by: UUID4
    created_at: datetime

    class Config:
        orm_mode = True

class DriverLink(DriverLinkInDBBase):
    pass

# Response schemas
class DriverWithLinks(Driver):
    links: List[DriverLink] = []

class DriverList(BaseModel):
    drivers: List[Driver]
    total: int
    skip: int
    limit: int

class InfluenceMap(BaseModel):
    driver_id: UUID4
    influenced_elements_count: int
    positive_influences: int
    negative_influences: int
    neutral_influences: int
    affected_layers: List[str]
    strategic_impact_score: float
    last_assessed: datetime

class DriverAnalysis(BaseModel):
    driver_id: UUID4
    urgency_score: float
    impact_score: float
    risk_score: float
    compliance_status: str
    strategic_alignment: str
    time_pressure: str
    last_analyzed: datetime 