from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from .models import Constraint, ConstraintLink
from .schemas import ConstraintCreate, ConstraintUpdate, ConstraintLinkCreate, ConstraintLinkUpdate
from fastapi import HTTPException
from uuid import UUID
from typing import List, Optional
from datetime import datetime
import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Redis setup for event emission
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL)

def emit_event(event_type: str, constraint_id: UUID, tenant_id: UUID, user_id: UUID, details: dict = None):
    """Emit event to Redis for event-driven architecture"""
    event = {
        "event_type": event_type,
        "constraint_id": str(constraint_id),
        "tenant_id": str(tenant_id),
        "user_id": str(user_id),
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {}
    }
    try:
        redis_client.publish("constraint_events", json.dumps(event))
    except Exception as e:
        print(f"Failed to emit event: {e}")

# Constraint CRUD operations
def create_constraint(db: Session, constraint_in: ConstraintCreate, tenant_id: UUID, user_id: UUID) -> Constraint:
    """Create a new constraint"""
    db_constraint = Constraint(
        **constraint_in.dict(),
        tenant_id=tenant_id,
        user_id=user_id
    )
    db.add(db_constraint)
    db.commit()
    db.refresh(db_constraint)
    
    # Emit event
    emit_event("constraint.created", db_constraint.id, tenant_id, user_id, {
        "name": db_constraint.name,
        "constraint_type": db_constraint.constraint_type,
        "severity": db_constraint.severity,
        "enforcement_level": db_constraint.enforcement_level
    })
    
    return db_constraint

def get_constraint(db: Session, constraint_id: UUID, tenant_id: UUID) -> Constraint:
    """Get a constraint by ID with tenant scoping"""
    constraint = db.query(Constraint).filter(
        and_(
            Constraint.id == constraint_id,
            Constraint.tenant_id == tenant_id
        )
    ).first()
    
    if not constraint:
        raise HTTPException(status_code=404, detail="Constraint not found")
    
    return constraint

def get_constraints(
    db: Session, 
    tenant_id: UUID, 
    skip: int = 0, 
    limit: int = 100,
    constraint_type: Optional[str] = None,
    scope: Optional[str] = None,
    severity: Optional[str] = None,
    enforcement_level: Optional[str] = None,
    stakeholder_id: Optional[UUID] = None,
    business_actor_id: Optional[UUID] = None,
    compliance_required: Optional[bool] = None
) -> List[Constraint]:
    """Get constraints with filtering and pagination"""
    query = db.query(Constraint).filter(Constraint.tenant_id == tenant_id)
    
    if constraint_type:
        query = query.filter(Constraint.constraint_type == constraint_type)
    if scope:
        query = query.filter(Constraint.scope == scope)
    if severity:
        query = query.filter(Constraint.severity == severity)
    if enforcement_level:
        query = query.filter(Constraint.enforcement_level == enforcement_level)
    if stakeholder_id:
        query = query.filter(Constraint.stakeholder_id == stakeholder_id)
    if business_actor_id:
        query = query.filter(Constraint.business_actor_id == business_actor_id)
    if compliance_required is not None:
        query = query.filter(Constraint.compliance_required == compliance_required)
    
    return query.offset(skip).limit(limit).all()

def update_constraint(
    db: Session, 
    constraint: Constraint, 
    constraint_in: ConstraintUpdate
) -> Constraint:
    """Update a constraint"""
    update_data = constraint_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(constraint, field, value)
    
    constraint.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(constraint)
    
    # Emit event
    emit_event("constraint.updated", constraint.id, constraint.tenant_id, constraint.user_id, {
        "name": constraint.name,
        "constraint_type": constraint.constraint_type,
        "severity": constraint.severity,
        "updated_fields": list(update_data.keys())
    })
    
    return constraint

def delete_constraint(db: Session, constraint: Constraint):
    """Delete a constraint"""
    constraint_id = constraint.id
    tenant_id = constraint.tenant_id
    user_id = constraint.user_id
    
    db.delete(constraint)
    db.commit()
    
    # Emit event
    emit_event("constraint.deleted", constraint_id, tenant_id, user_id, {
        "name": constraint.name,
        "constraint_type": constraint.constraint_type
    })

# Constraint Link operations
def create_constraint_link(
    db: Session, 
    link_in: ConstraintLinkCreate, 
    constraint_id: UUID, 
    user_id: UUID
) -> ConstraintLink:
    """Create a link between constraint and another element"""
    db_link = ConstraintLink(
        **link_in.dict(),
        constraint_id=constraint_id,
        created_by=user_id
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    # Emit event
    emit_event("constraint_link.created", constraint_id, db_link.constraint.tenant_id, user_id, {
        "linked_element_type": db_link.linked_element_type,
        "link_type": db_link.link_type,
        "compliance_status": db_link.compliance_status
    })
    
    return db_link

def get_constraint_link(db: Session, link_id: UUID, tenant_id: UUID) -> ConstraintLink:
    """Get a constraint link by ID with tenant scoping"""
    link = db.query(ConstraintLink).join(Constraint).filter(
        and_(
            ConstraintLink.id == link_id,
            Constraint.tenant_id == tenant_id
        )
    ).first()
    
    if not link:
        raise HTTPException(status_code=404, detail="Constraint link not found")
    
    return link

def get_constraint_links(db: Session, constraint_id: UUID, tenant_id: UUID) -> List[ConstraintLink]:
    """Get all links for a constraint"""
    return db.query(ConstraintLink).join(Constraint).filter(
        and_(
            ConstraintLink.constraint_id == constraint_id,
            Constraint.tenant_id == tenant_id
        )
    ).all()

def update_constraint_link(
    db: Session, 
    link: ConstraintLink, 
    link_in: ConstraintLinkUpdate
) -> ConstraintLink:
    """Update a constraint link"""
    update_data = link_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(link, field, value)
    
    db.commit()
    db.refresh(link)
    
    # Emit event
    emit_event("constraint_link.updated", link.constraint_id, link.constraint.tenant_id, link.created_by, {
        "linked_element_type": link.linked_element_type,
        "link_type": link.link_type,
        "compliance_status": link.compliance_status
    })
    
    return link

def delete_constraint_link(db: Session, link: ConstraintLink):
    """Delete a constraint link"""
    link_id = link.id
    constraint_id = link.constraint_id
    tenant_id = link.constraint.tenant_id
    user_id = link.created_by
    
    db.delete(link)
    db.commit()
    
    # Emit event
    emit_event("constraint_link.deleted", constraint_id, tenant_id, user_id, {
        "linked_element_type": link.linked_element_type,
        "link_type": link.link_type
    })

# Analysis and impact mapping
def get_impact_map(db: Session, constraint_id: UUID, tenant_id: UUID) -> dict:
    """Get impact map for a constraint"""
    constraint = get_constraint(db, constraint_id, tenant_id)
    links = get_constraint_links(db, constraint_id, tenant_id)
    
    # Calculate compliance statistics
    compliant_elements = len([link for link in links if link.compliance_status == "compliant"])
    non_compliant_elements = len([link for link in links if link.compliance_status == "non_compliant"])
    partially_compliant_elements = len([link for link in links if link.compliance_status == "partially_compliant"])
    exempt_elements = len([link for link in links if link.compliance_status == "exempt"])
    
    # Analyze affected layers
    affected_layers = set()
    for link in links:
        if "goal" in link.linked_element_type:
            affected_layers.add("Motivation")
        elif "requirement" in link.linked_element_type:
            affected_layers.add("Motivation")
        elif "capability" in link.linked_element_type:
            affected_layers.add("Strategy")
        elif "business" in link.linked_element_type:
            affected_layers.add("Business")
        elif "application" in link.linked_element_type:
            affected_layers.add("Application")
        elif "technology" in link.linked_element_type:
            affected_layers.add("Technology")
    
    # Calculate overall compliance score
    total_elements = len(links)
    if total_elements > 0:
        overall_compliance_score = (compliant_elements + (partially_compliant_elements * 0.5)) / total_elements
    else:
        overall_compliance_score = 1.0
    
    return {
        "constraint_id": constraint_id,
        "impacted_elements_count": len(links),
        "compliant_elements": compliant_elements,
        "non_compliant_elements": non_compliant_elements,
        "partially_compliant_elements": partially_compliant_elements,
        "exempt_elements": exempt_elements,
        "affected_layers": list(affected_layers),
        "overall_compliance_score": round(overall_compliance_score, 2),
        "last_assessed": datetime.utcnow()
    }

def analyze_constraint(db: Session, constraint_id: UUID, tenant_id: UUID) -> dict:
    """Analyze a constraint for strategic insights"""
    constraint = get_constraint(db, constraint_id, tenant_id)
    links = get_constraint_links(db, constraint_id, tenant_id)
    
    # Calculate scores
    severity_score = {"low": 1, "medium": 2, "high": 3, "critical": 4}[constraint.severity] / 4.0
    risk_score = {"low": 1, "medium": 2, "high": 3, "critical": 4}[constraint.risk_profile] / 4.0
    compliance_score = 1.0 if constraint.compliance_required else 0.5
    
    business_impact_score = {"low": 1, "medium": 2, "high": 3, "critical": 4}[constraint.business_impact] / 4.0
    technical_impact_score = {"low": 1, "medium": 2, "high": 3, "critical": 4}[constraint.technical_impact] / 4.0
    operational_impact_score = {"low": 1, "medium": 2, "high": 3, "critical": 4}[constraint.operational_impact] / 4.0
    mitigation_effort_score = {"low": 1, "medium": 2, "high": 3, "critical": 4}[constraint.mitigation_effort] / 4.0
    
    # Calculate overall impact score
    overall_impact_score = (business_impact_score + technical_impact_score + operational_impact_score) / 3.0
    
    return {
        "constraint_id": constraint_id,
        "severity_score": round(severity_score, 2),
        "risk_score": round(risk_score, 2),
        "compliance_score": round(compliance_score, 2),
        "business_impact_score": round(business_impact_score, 2),
        "technical_impact_score": round(technical_impact_score, 2),
        "operational_impact_score": round(operational_impact_score, 2),
        "mitigation_effort_score": round(mitigation_effort_score, 2),
        "overall_impact_score": round(overall_impact_score, 2),
        "last_analyzed": datetime.utcnow()
    }

# Domain logic for queries
def get_constraints_by_type(db: Session, tenant_id: UUID, constraint_type: str) -> List[Constraint]:
    """Get constraints filtered by type"""
    return db.query(Constraint).filter(
        and_(
            Constraint.tenant_id == tenant_id,
            Constraint.constraint_type == constraint_type
        )
    ).all()

def get_constraints_by_scope(db: Session, tenant_id: UUID, scope: str) -> List[Constraint]:
    """Get constraints filtered by scope"""
    return db.query(Constraint).filter(
        and_(
            Constraint.tenant_id == tenant_id,
            Constraint.scope == scope
        )
    ).all()

def get_constraints_by_severity(db: Session, tenant_id: UUID, severity: str) -> List[Constraint]:
    """Get constraints filtered by severity"""
    return db.query(Constraint).filter(
        and_(
            Constraint.tenant_id == tenant_id,
            Constraint.severity == severity
        )
    ).all()

def get_constraints_by_stakeholder(db: Session, tenant_id: UUID, stakeholder_id: UUID) -> List[Constraint]:
    """Get constraints associated with a specific stakeholder"""
    return db.query(Constraint).filter(
        and_(
            Constraint.tenant_id == tenant_id,
            Constraint.stakeholder_id == stakeholder_id
        )
    ).all()

def get_constraints_by_business_actor(db: Session, tenant_id: UUID, business_actor_id: UUID) -> List[Constraint]:
    """Get constraints associated with a specific business actor"""
    return db.query(Constraint).filter(
        and_(
            Constraint.tenant_id == tenant_id,
            Constraint.business_actor_id == business_actor_id
        )
    ).all()

def get_constraints_by_element(db: Session, tenant_id: UUID, element_type: str, element_id: UUID) -> List[Constraint]:
    """Get constraints that affect a specific element"""
    return db.query(Constraint).join(ConstraintLink).filter(
        and_(
            Constraint.tenant_id == tenant_id,
            ConstraintLink.linked_element_id == element_id,
            ConstraintLink.linked_element_type == element_type
        )
    ).all()

def get_compliance_constraints(db: Session, tenant_id: UUID) -> List[Constraint]:
    """Get constraints that require compliance"""
    return db.query(Constraint).filter(
        and_(
            Constraint.tenant_id == tenant_id,
            Constraint.compliance_required == True
        )
    ).all()

def get_expiring_constraints(db: Session, tenant_id: UUID, days_ahead: int = 30) -> List[Constraint]:
    """Get constraints that are expiring soon"""
    from datetime import timedelta
    expiry_date = datetime.utcnow() + timedelta(days=days_ahead)
    
    return db.query(Constraint).filter(
        and_(
            Constraint.tenant_id == tenant_id,
            Constraint.expiry_date <= expiry_date,
            Constraint.expiry_date >= datetime.utcnow()
        )
    ).all() 