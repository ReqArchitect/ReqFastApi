from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from .models import Driver, DriverLink
from .schemas import DriverCreate, DriverUpdate, DriverLinkCreate, DriverLinkUpdate
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

def emit_event(event_type: str, driver_id: UUID, tenant_id: UUID, user_id: UUID, details: dict = None):
    """Emit event to Redis for event-driven architecture"""
    event = {
        "event_type": event_type,
        "driver_id": str(driver_id),
        "tenant_id": str(tenant_id),
        "user_id": str(user_id),
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {}
    }
    try:
        redis_client.publish("driver_events", json.dumps(event))
    except Exception as e:
        print(f"Failed to emit event: {e}")

# Driver CRUD operations
def create_driver(db: Session, driver_in: DriverCreate, tenant_id: UUID, user_id: UUID) -> Driver:
    """Create a new driver"""
    db_driver = Driver(
        **driver_in.dict(),
        tenant_id=tenant_id,
        user_id=user_id
    )
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    
    # Emit event
    emit_event("driver.created", db_driver.id, tenant_id, user_id, {
        "name": db_driver.name,
        "driver_type": db_driver.driver_type,
        "urgency": db_driver.urgency,
        "impact_level": db_driver.impact_level
    })
    
    return db_driver

def get_driver(db: Session, driver_id: UUID, tenant_id: UUID) -> Driver:
    """Get a driver by ID with tenant scoping"""
    driver = db.query(Driver).filter(
        and_(
            Driver.id == driver_id,
            Driver.tenant_id == tenant_id
        )
    ).first()
    
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    return driver

def get_drivers(
    db: Session, 
    tenant_id: UUID, 
    skip: int = 0, 
    limit: int = 100,
    driver_type: Optional[str] = None,
    category: Optional[str] = None,
    urgency: Optional[str] = None,
    impact_level: Optional[str] = None,
    stakeholder_id: Optional[UUID] = None,
    business_actor_id: Optional[UUID] = None
) -> List[Driver]:
    """Get drivers with filtering and pagination"""
    query = db.query(Driver).filter(Driver.tenant_id == tenant_id)
    
    if driver_type:
        query = query.filter(Driver.driver_type == driver_type)
    if category:
        query = query.filter(Driver.category == category)
    if urgency:
        query = query.filter(Driver.urgency == urgency)
    if impact_level:
        query = query.filter(Driver.impact_level == impact_level)
    if stakeholder_id:
        query = query.filter(Driver.stakeholder_id == stakeholder_id)
    if business_actor_id:
        query = query.filter(Driver.business_actor_id == business_actor_id)
    
    return query.offset(skip).limit(limit).all()

def update_driver(
    db: Session, 
    driver: Driver, 
    driver_in: DriverUpdate
) -> Driver:
    """Update a driver"""
    update_data = driver_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(driver, field, value)
    
    driver.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(driver)
    
    # Emit event
    emit_event("driver.updated", driver.id, driver.tenant_id, driver.user_id, {
        "name": driver.name,
        "driver_type": driver.driver_type,
        "urgency": driver.urgency,
        "updated_fields": list(update_data.keys())
    })
    
    return driver

def delete_driver(db: Session, driver: Driver):
    """Delete a driver"""
    driver_id = driver.id
    tenant_id = driver.tenant_id
    user_id = driver.user_id
    
    db.delete(driver)
    db.commit()
    
    # Emit event
    emit_event("driver.deleted", driver_id, tenant_id, user_id, {
        "name": driver.name,
        "driver_type": driver.driver_type
    })

# Driver Link operations
def create_driver_link(
    db: Session, 
    link_in: DriverLinkCreate, 
    driver_id: UUID, 
    user_id: UUID
) -> DriverLink:
    """Create a link between driver and another element"""
    db_link = DriverLink(
        **link_in.dict(),
        driver_id=driver_id,
        created_by=user_id
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    # Emit event
    emit_event("driver_link.created", driver_id, db_link.driver.tenant_id, user_id, {
        "linked_element_type": db_link.linked_element_type,
        "link_type": db_link.link_type,
        "influence_direction": db_link.influence_direction
    })
    
    return db_link

def get_driver_link(db: Session, link_id: UUID, tenant_id: UUID) -> DriverLink:
    """Get a driver link by ID with tenant scoping"""
    link = db.query(DriverLink).join(Driver).filter(
        and_(
            DriverLink.id == link_id,
            Driver.tenant_id == tenant_id
        )
    ).first()
    
    if not link:
        raise HTTPException(status_code=404, detail="Driver link not found")
    
    return link

def get_driver_links(db: Session, driver_id: UUID, tenant_id: UUID) -> List[DriverLink]:
    """Get all links for a driver"""
    return db.query(DriverLink).join(Driver).filter(
        and_(
            DriverLink.driver_id == driver_id,
            Driver.tenant_id == tenant_id
        )
    ).all()

def update_driver_link(
    db: Session, 
    link: DriverLink, 
    link_in: DriverLinkUpdate
) -> DriverLink:
    """Update a driver link"""
    update_data = link_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(link, field, value)
    
    db.commit()
    db.refresh(link)
    
    # Emit event
    emit_event("driver_link.updated", link.driver_id, link.driver.tenant_id, link.created_by, {
        "linked_element_type": link.linked_element_type,
        "link_type": link.link_type,
        "influence_direction": link.influence_direction
    })
    
    return link

def delete_driver_link(db: Session, link: DriverLink):
    """Delete a driver link"""
    link_id = link.id
    driver_id = link.driver_id
    tenant_id = link.driver.tenant_id
    user_id = link.created_by
    
    db.delete(link)
    db.commit()
    
    # Emit event
    emit_event("driver_link.deleted", driver_id, tenant_id, user_id, {
        "linked_element_type": link.linked_element_type,
        "link_type": link.link_type
    })

# Analysis and influence mapping
def get_influence_map(db: Session, driver_id: UUID, tenant_id: UUID) -> dict:
    """Get influence map for a driver"""
    driver = get_driver(db, driver_id, tenant_id)
    links = get_driver_links(db, driver_id, tenant_id)
    
    # Calculate influence statistics
    positive_influences = len([link for link in links if link.influence_direction == "positive"])
    negative_influences = len([link for link in links if link.influence_direction == "negative"])
    neutral_influences = len([link for link in links if link.influence_direction == "neutral"])
    
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
    
    # Calculate strategic impact score
    strategic_impact_score = (driver.strategic_priority * 0.3 + 
                            ({"low": 1, "medium": 2, "high": 3, "critical": 4}[driver.impact_level] * 0.4) +
                            ({"low": 1, "medium": 2, "high": 3, "critical": 4}[driver.urgency] * 0.3))
    
    return {
        "driver_id": driver_id,
        "influenced_elements_count": len(links),
        "positive_influences": positive_influences,
        "negative_influences": negative_influences,
        "neutral_influences": neutral_influences,
        "affected_layers": list(affected_layers),
        "strategic_impact_score": round(strategic_impact_score, 2),
        "last_assessed": datetime.utcnow()
    }

def analyze_driver(db: Session, driver_id: UUID, tenant_id: UUID) -> dict:
    """Analyze a driver for strategic insights"""
    driver = get_driver(db, driver_id, tenant_id)
    links = get_driver_links(db, driver_id, tenant_id)
    
    # Calculate scores
    urgency_score = {"low": 1, "medium": 2, "high": 3, "critical": 4}[driver.urgency] / 4.0
    impact_score = {"low": 1, "medium": 2, "high": 3, "critical": 4}[driver.impact_level] / 4.0
    risk_score = {"low": 1, "medium": 2, "high": 3, "critical": 4}[driver.risk_level] / 4.0
    
    # Determine compliance status
    compliance_status = "compliant" if driver.compliance_required and driver.driver_type == "regulatory" else "non-applicable"
    
    # Determine strategic alignment
    strategic_alignment = "high" if driver.strategic_priority >= 4 else "medium" if driver.strategic_priority >= 3 else "low"
    
    # Determine time pressure
    time_pressure = "high" if driver.urgency in ["high", "critical"] else "medium" if driver.urgency == "medium" else "low"
    
    return {
        "driver_id": driver_id,
        "urgency_score": round(urgency_score, 2),
        "impact_score": round(impact_score, 2),
        "risk_score": round(risk_score, 2),
        "compliance_status": compliance_status,
        "strategic_alignment": strategic_alignment,
        "time_pressure": time_pressure,
        "last_analyzed": datetime.utcnow()
    }

# Domain logic for queries
def get_drivers_by_urgency(db: Session, tenant_id: UUID, urgency: str) -> List[Driver]:
    """Get drivers filtered by urgency"""
    return db.query(Driver).filter(
        and_(
            Driver.tenant_id == tenant_id,
            Driver.urgency == urgency
        )
    ).all()

def get_drivers_by_category(db: Session, tenant_id: UUID, category: str) -> List[Driver]:
    """Get drivers filtered by category"""
    return db.query(Driver).filter(
        and_(
            Driver.tenant_id == tenant_id,
            Driver.category == category
        )
    ).all()

def get_drivers_by_stakeholder(db: Session, tenant_id: UUID, stakeholder_id: UUID) -> List[Driver]:
    """Get drivers associated with a specific stakeholder"""
    return db.query(Driver).filter(
        and_(
            Driver.tenant_id == tenant_id,
            Driver.stakeholder_id == stakeholder_id
        )
    ).all()

def get_drivers_by_business_actor(db: Session, tenant_id: UUID, business_actor_id: UUID) -> List[Driver]:
    """Get drivers associated with a specific business actor"""
    return db.query(Driver).filter(
        and_(
            Driver.tenant_id == tenant_id,
            Driver.business_actor_id == business_actor_id
        )
    ).all()

def get_drivers_by_associated_goals(db: Session, tenant_id: UUID, goal_id: UUID) -> List[Driver]:
    """Get drivers that influence a specific goal"""
    return db.query(Driver).join(DriverLink).filter(
        and_(
            Driver.tenant_id == tenant_id,
            DriverLink.linked_element_id == goal_id,
            DriverLink.linked_element_type == "goal"
        )
    ).all()

def get_drivers_by_associated_requirements(db: Session, tenant_id: UUID, requirement_id: UUID) -> List[Driver]:
    """Get drivers that influence a specific requirement"""
    return db.query(Driver).join(DriverLink).filter(
        and_(
            Driver.tenant_id == tenant_id,
            DriverLink.linked_element_id == requirement_id,
            DriverLink.linked_element_type == "requirement"
        )
    ).all() 