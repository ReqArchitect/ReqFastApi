from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from .models import Requirement, RequirementLink
from .schemas import RequirementCreate, RequirementUpdate, RequirementLinkCreate, RequirementLinkUpdate
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

def emit_event(event_type: str, requirement_id: UUID, tenant_id: UUID, user_id: UUID, details: dict = None):
    """Emit event to Redis for event-driven architecture"""
    event = {
        "event_type": event_type,
        "requirement_id": str(requirement_id),
        "tenant_id": str(tenant_id),
        "user_id": str(user_id),
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {}
    }
    try:
        redis_client.publish("requirement_events", json.dumps(event))
    except Exception as e:
        print(f"Failed to emit event: {e}")

# Requirement CRUD operations
def create_requirement(db: Session, requirement_in: RequirementCreate, tenant_id: UUID, user_id: UUID) -> Requirement:
    """Create a new requirement"""
    db_requirement = Requirement(
        **requirement_in.dict(),
        tenant_id=tenant_id,
        user_id=user_id
    )
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    
    # Emit event
    emit_event("requirement.created", db_requirement.id, tenant_id, user_id, {
        "name": db_requirement.name,
        "requirement_type": db_requirement.requirement_type,
        "priority": db_requirement.priority
    })
    
    return db_requirement

def get_requirement(db: Session, requirement_id: UUID, tenant_id: UUID) -> Requirement:
    """Get a requirement by ID with tenant scoping"""
    requirement = db.query(Requirement).filter(
        and_(
            Requirement.id == requirement_id,
            Requirement.tenant_id == tenant_id
        )
    ).first()
    
    if not requirement:
        raise HTTPException(status_code=404, detail="Requirement not found")
    
    return requirement

def get_requirements(
    db: Session, 
    tenant_id: UUID, 
    skip: int = 0, 
    limit: int = 100,
    requirement_type: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None
) -> List[Requirement]:
    """Get requirements with filtering and pagination"""
    query = db.query(Requirement).filter(Requirement.tenant_id == tenant_id)
    
    if requirement_type:
        query = query.filter(Requirement.requirement_type == requirement_type)
    if status:
        query = query.filter(Requirement.status == status)
    if priority:
        query = query.filter(Requirement.priority == priority)
    
    return query.offset(skip).limit(limit).all()

def update_requirement(
    db: Session, 
    requirement: Requirement, 
    requirement_in: RequirementUpdate
) -> Requirement:
    """Update a requirement"""
    update_data = requirement_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(requirement, field, value)
    
    requirement.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(requirement)
    
    # Emit event
    emit_event("requirement.updated", requirement.id, requirement.tenant_id, requirement.user_id, {
        "name": requirement.name,
        "status": requirement.status,
        "updated_fields": list(update_data.keys())
    })
    
    return requirement

def delete_requirement(db: Session, requirement: Requirement):
    """Delete a requirement"""
    requirement_id = requirement.id
    tenant_id = requirement.tenant_id
    user_id = requirement.user_id
    
    db.delete(requirement)
    db.commit()
    
    # Emit event
    emit_event("requirement.deleted", requirement_id, tenant_id, user_id, {
        "name": requirement.name,
        "requirement_type": requirement.requirement_type
    })

# Requirement Link operations
def create_requirement_link(
    db: Session, 
    link_in: RequirementLinkCreate, 
    requirement_id: UUID, 
    user_id: UUID
) -> RequirementLink:
    """Create a link between requirement and another element"""
    db_link = RequirementLink(
        **link_in.dict(),
        requirement_id=requirement_id,
        created_by=user_id
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    # Emit event
    emit_event("requirement_link.created", requirement_id, db_link.requirement.tenant_id, user_id, {
        "linked_element_type": db_link.linked_element_type,
        "link_type": db_link.link_type
    })
    
    return db_link

def get_requirement_link(db: Session, link_id: UUID, tenant_id: UUID) -> RequirementLink:
    """Get a requirement link by ID with tenant scoping"""
    link = db.query(RequirementLink).join(Requirement).filter(
        and_(
            RequirementLink.id == link_id,
            Requirement.tenant_id == tenant_id
        )
    ).first()
    
    if not link:
        raise HTTPException(status_code=404, detail="Requirement link not found")
    
    return link

def get_requirement_links(db: Session, requirement_id: UUID, tenant_id: UUID) -> List[RequirementLink]:
    """Get all links for a requirement"""
    return db.query(RequirementLink).join(Requirement).filter(
        and_(
            RequirementLink.requirement_id == requirement_id,
            Requirement.tenant_id == tenant_id
        )
    ).all()

def update_requirement_link(
    db: Session, 
    link: RequirementLink, 
    link_in: RequirementLinkUpdate
) -> RequirementLink:
    """Update a requirement link"""
    update_data = link_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(link, field, value)
    
    db.commit()
    db.refresh(link)
    
    # Emit event
    emit_event("requirement_link.updated", link.requirement_id, link.requirement.tenant_id, link.created_by, {
        "linked_element_type": link.linked_element_type,
        "link_type": link.link_type
    })
    
    return link

def delete_requirement_link(db: Session, link: RequirementLink):
    """Delete a requirement link"""
    link_id = link.id
    requirement_id = link.requirement_id
    tenant_id = link.requirement.tenant_id
    user_id = link.created_by
    
    db.delete(link)
    db.commit()
    
    # Emit event
    emit_event("requirement_link.deleted", requirement_id, tenant_id, user_id, {
        "linked_element_type": link.linked_element_type,
        "link_type": link.link_type
    })

# Traceability and impact analysis
def check_traceability(db: Session, requirement_id: UUID, tenant_id: UUID) -> dict:
    """Check traceability status for a requirement"""
    requirement = get_requirement(db, requirement_id, tenant_id)
    links = get_requirement_links(db, requirement_id, tenant_id)
    
    # Calculate compliance status
    compliance_status = "compliant" if requirement.compliance_required and requirement.validation_method else "pending"
    
    # Calculate validation status
    validation_status = "validated" if requirement.validation_method else "pending"
    
    return {
        "requirement_id": requirement_id,
        "linked_elements_count": len(links),
        "compliance_status": compliance_status,
        "validation_status": validation_status,
        "last_updated": requirement.updated_at
    }

def get_impact_summary(db: Session, requirement_id: UUID, tenant_id: UUID) -> dict:
    """Get impact summary for a requirement"""
    requirement = get_requirement(db, requirement_id, tenant_id)
    links = get_requirement_links(db, requirement_id, tenant_id)
    
    # Analyze direct impacts
    direct_impact_count = len(links)
    
    # Analyze affected layers (simplified)
    affected_layers = set()
    for link in links:
        if "capability" in link.linked_element_type:
            affected_layers.add("Strategy")
        elif "business" in link.linked_element_type:
            affected_layers.add("Business")
        elif "application" in link.linked_element_type:
            affected_layers.add("Application")
        elif "technology" in link.linked_element_type:
            affected_layers.add("Technology")
    
    # Calculate risk level based on priority and compliance
    risk_level = "low"
    if requirement.priority in ["high", "critical"]:
        risk_level = "high"
    elif requirement.compliance_required:
        risk_level = "medium"
    
    return {
        "requirement_id": requirement_id,
        "direct_impact_count": direct_impact_count,
        "indirect_impact_count": 0,  # Would require deeper analysis
        "affected_layers": list(affected_layers),
        "risk_level": risk_level,
        "last_assessed": datetime.utcnow()
    } 