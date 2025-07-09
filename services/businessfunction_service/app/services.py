from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from .models import BusinessFunction, FunctionLink
from .schemas import BusinessFunctionCreate, BusinessFunctionUpdate, FunctionLinkCreate, FunctionLinkUpdate
from fastapi import HTTPException
from uuid import UUID
from typing import List, Optional
from datetime import datetime, timedelta
import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Redis setup for event emission
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL)

def emit_event(event_type: str, business_function_id: UUID, tenant_id: UUID, user_id: UUID, details: dict = None):
    """Emit event to Redis for event-driven architecture"""
    event = {
        "event_type": event_type,
        "business_function_id": str(business_function_id),
        "tenant_id": str(tenant_id),
        "user_id": str(user_id),
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {}
    }
    try:
        redis_client.publish("business_function_events", json.dumps(event))
    except Exception as e:
        print(f"Failed to emit event: {e}")

# Business Function CRUD operations
def create_business_function(db: Session, function_in: BusinessFunctionCreate, tenant_id: UUID, user_id: UUID) -> BusinessFunction:
    """Create a new business function"""
    db_function = BusinessFunction(
        **function_in.dict(),
        tenant_id=tenant_id,
        user_id=user_id
    )
    db.add(db_function)
    db.commit()
    db.refresh(db_function)
    
    # Emit event
    emit_event("business_function.created", db_function.id, tenant_id, user_id, {
        "name": db_function.name,
        "competency_area": db_function.competency_area,
        "organizational_unit": db_function.organizational_unit,
        "criticality": db_function.criticality,
        "status": db_function.status
    })
    
    return db_function

def get_business_function(db: Session, function_id: UUID, tenant_id: UUID) -> BusinessFunction:
    """Get a business function by ID with tenant scoping"""
    function = db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.id == function_id,
            BusinessFunction.tenant_id == tenant_id
        )
    ).first()
    
    if not function:
        raise HTTPException(status_code=404, detail="Business function not found")
    
    return function

def get_business_functions(
    db: Session, 
    tenant_id: UUID, 
    skip: int = 0, 
    limit: int = 100,
    competency_area: Optional[str] = None,
    organizational_unit: Optional[str] = None,
    criticality: Optional[str] = None,
    frequency: Optional[str] = None,
    status: Optional[str] = None,
    owner_role_id: Optional[UUID] = None,
    parent_function_id: Optional[UUID] = None,
    supporting_capability_id: Optional[UUID] = None,
    business_process_id: Optional[UUID] = None
) -> List[BusinessFunction]:
    """Get business functions with filtering and pagination"""
    query = db.query(BusinessFunction).filter(BusinessFunction.tenant_id == tenant_id)
    
    if competency_area:
        query = query.filter(BusinessFunction.competency_area == competency_area)
    if organizational_unit:
        query = query.filter(BusinessFunction.organizational_unit == organizational_unit)
    if criticality:
        query = query.filter(BusinessFunction.criticality == criticality)
    if frequency:
        query = query.filter(BusinessFunction.frequency == frequency)
    if status:
        query = query.filter(BusinessFunction.status == status)
    if owner_role_id:
        query = query.filter(BusinessFunction.owner_role_id == owner_role_id)
    if parent_function_id:
        query = query.filter(BusinessFunction.parent_function_id == parent_function_id)
    if supporting_capability_id:
        query = query.filter(BusinessFunction.supporting_capability_id == supporting_capability_id)
    if business_process_id:
        query = query.filter(BusinessFunction.business_process_id == business_process_id)
    
    return query.offset(skip).limit(limit).all()

def update_business_function(
    db: Session, 
    function: BusinessFunction, 
    function_in: BusinessFunctionUpdate
) -> BusinessFunction:
    """Update a business function"""
    update_data = function_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(function, field, value)
    
    function.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(function)
    
    # Emit event
    emit_event("business_function.updated", function.id, function.tenant_id, function.user_id, {
        "name": function.name,
        "competency_area": function.competency_area,
        "organizational_unit": function.organizational_unit,
        "criticality": function.criticality,
        "status": function.status,
        "updated_fields": list(update_data.keys())
    })
    
    return function

def delete_business_function(db: Session, function: BusinessFunction):
    """Delete a business function"""
    function_id = function.id
    tenant_id = function.tenant_id
    user_id = function.user_id
    
    db.delete(function)
    db.commit()
    
    # Emit event
    emit_event("business_function.deleted", function_id, tenant_id, user_id, {
        "name": function.name,
        "competency_area": function.competency_area
    })

# Function Link operations
def create_function_link(
    db: Session, 
    link_in: FunctionLinkCreate, 
    function_id: UUID, 
    user_id: UUID
) -> FunctionLink:
    """Create a link between business function and another element"""
    db_link = FunctionLink(
        **link_in.dict(),
        business_function_id=function_id,
        created_by=user_id
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    # Emit event
    emit_event("function_link.created", function_id, db_link.business_function.tenant_id, user_id, {
        "linked_element_type": db_link.linked_element_type,
        "link_type": db_link.link_type,
        "relationship_strength": db_link.relationship_strength
    })
    
    return db_link

def get_function_link(db: Session, link_id: UUID, tenant_id: UUID) -> FunctionLink:
    """Get a function link by ID with tenant scoping"""
    link = db.query(FunctionLink).join(BusinessFunction).filter(
        and_(
            FunctionLink.id == link_id,
            BusinessFunction.tenant_id == tenant_id
        )
    ).first()
    
    if not link:
        raise HTTPException(status_code=404, detail="Function link not found")
    
    return link

def get_function_links(db: Session, function_id: UUID, tenant_id: UUID) -> List[FunctionLink]:
    """Get all links for a business function"""
    return db.query(FunctionLink).join(BusinessFunction).filter(
        and_(
            FunctionLink.business_function_id == function_id,
            BusinessFunction.tenant_id == tenant_id
        )
    ).all()

def update_function_link(
    db: Session, 
    link: FunctionLink, 
    link_in: FunctionLinkUpdate
) -> FunctionLink:
    """Update a function link"""
    update_data = link_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(link, field, value)
    
    db.commit()
    db.refresh(link)
    
    # Emit event
    emit_event("function_link.updated", link.business_function_id, link.business_function.tenant_id, link.created_by, {
        "linked_element_type": link.linked_element_type,
        "link_type": link.link_type,
        "relationship_strength": link.relationship_strength
    })
    
    return link

def delete_function_link(db: Session, link: FunctionLink):
    """Delete a function link"""
    link_id = link.id
    function_id = link.business_function_id
    tenant_id = link.business_function.tenant_id
    user_id = link.created_by
    
    db.delete(link)
    db.commit()
    
    # Emit event
    emit_event("function_link.deleted", function_id, tenant_id, user_id, {
        "linked_element_type": link.linked_element_type,
        "link_type": link.link_type
    })

# Analysis and impact mapping
def get_impact_map(db: Session, function_id: UUID, tenant_id: UUID) -> dict:
    """Get impact map for a business function"""
    function = get_business_function(db, function_id, tenant_id)
    links = get_function_links(db, function_id, tenant_id)
    
    # Count linked elements by type
    business_roles_count = len([link for link in links if "business_role" in link.linked_element_type])
    business_processes_count = len([link for link in links if "business_process" in link.linked_element_type])
    capabilities_count = len([link for link in links if "capability" in link.linked_element_type])
    application_services_count = len([link for link in links if "application_service" in link.linked_element_type])
    data_objects_count = len([link for link in links if "data_object" in link.linked_element_type])
    
    # Calculate overall impact score based on dependency levels and relationship strengths
    total_links = len(links)
    if total_links > 0:
        high_dependencies = len([link for link in links if link.dependency_level == "high"])
        strong_relationships = len([link for link in links if link.relationship_strength == "strong"])
        overall_impact_score = (high_dependencies + strong_relationships) / (total_links * 2)
    else:
        overall_impact_score = 0.0
    
    return {
        "business_function_id": function_id,
        "linked_elements_count": len(links),
        "business_roles_count": business_roles_count,
        "business_processes_count": business_processes_count,
        "capabilities_count": capabilities_count,
        "application_services_count": application_services_count,
        "data_objects_count": data_objects_count,
        "overall_impact_score": round(overall_impact_score, 2),
        "last_assessed": datetime.utcnow()
    }

def analyze_business_function(db: Session, function_id: UUID, tenant_id: UUID) -> dict:
    """Analyze a business function for operational insights"""
    function = get_business_function(db, function_id, tenant_id)
    
    # Calculate scores
    alignment_score = function.alignment_score or 0.0
    efficiency_score = function.efficiency_score or 0.0
    effectiveness_score = function.effectiveness_score or 0.0
    
    # Risk score based on risk level
    risk_score = {"low": 0.25, "medium": 0.5, "high": 0.75, "critical": 1.0}[function.risk_level]
    
    # Strategic importance score
    strategic_importance_score = {"low": 0.25, "medium": 0.5, "high": 0.75, "critical": 1.0}[function.strategic_importance]
    
    # Business value score
    business_value_score = {"low": 0.25, "medium": 0.5, "high": 0.75, "critical": 1.0}[function.business_value]
    
    # Calculate overall health score
    overall_health_score = (alignment_score + efficiency_score + effectiveness_score + (1 - risk_score) + strategic_importance_score + business_value_score) / 6.0
    
    return {
        "business_function_id": function_id,
        "alignment_score": round(alignment_score, 2),
        "efficiency_score": round(efficiency_score, 2),
        "effectiveness_score": round(effectiveness_score, 2),
        "risk_score": round(risk_score, 2),
        "strategic_importance_score": round(strategic_importance_score, 2),
        "business_value_score": round(business_value_score, 2),
        "overall_health_score": round(overall_health_score, 2),
        "last_analyzed": datetime.utcnow()
    }

# Domain logic for queries
def get_business_functions_by_competency_area(db: Session, tenant_id: UUID, competency_area: str) -> List[BusinessFunction]:
    """Get business functions filtered by competency area"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.competency_area == competency_area
        )
    ).all()

def get_business_functions_by_organizational_unit(db: Session, tenant_id: UUID, organizational_unit: str) -> List[BusinessFunction]:
    """Get business functions filtered by organizational unit"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.organizational_unit == organizational_unit
        )
    ).all()

def get_business_functions_by_criticality(db: Session, tenant_id: UUID, criticality: str) -> List[BusinessFunction]:
    """Get business functions filtered by criticality"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.criticality == criticality
        )
    ).all()

def get_business_functions_by_frequency(db: Session, tenant_id: UUID, frequency: str) -> List[BusinessFunction]:
    """Get business functions filtered by frequency"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.frequency == frequency
        )
    ).all()

def get_business_functions_by_status(db: Session, tenant_id: UUID, status: str) -> List[BusinessFunction]:
    """Get business functions filtered by status"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.status == status
        )
    ).all()

def get_business_functions_by_role(db: Session, tenant_id: UUID, role_id: UUID) -> List[BusinessFunction]:
    """Get business functions associated with a specific role"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.owner_role_id == role_id
        )
    ).all()

def get_business_functions_by_process(db: Session, tenant_id: UUID, process_id: UUID) -> List[BusinessFunction]:
    """Get business functions associated with a specific process"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.business_process_id == process_id
        )
    ).all()

def get_business_functions_by_capability(db: Session, tenant_id: UUID, capability_id: UUID) -> List[BusinessFunction]:
    """Get business functions associated with a specific capability"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.supporting_capability_id == capability_id
        )
    ).all()

def get_business_functions_by_element(db: Session, tenant_id: UUID, element_type: str, element_id: UUID) -> List[BusinessFunction]:
    """Get business functions that are linked to a specific element"""
    return db.query(BusinessFunction).join(FunctionLink).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            FunctionLink.linked_element_id == element_id,
            FunctionLink.linked_element_type == element_type
        )
    ).all()

def get_active_business_functions(db: Session, tenant_id: UUID) -> List[BusinessFunction]:
    """Get active business functions"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.status == "active"
        )
    ).all()

def get_critical_business_functions(db: Session, tenant_id: UUID) -> List[BusinessFunction]:
    """Get critical business functions"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.criticality.in_(["high", "critical"])
        )
    ).all()

def get_business_functions_by_complexity(db: Session, tenant_id: UUID, complexity: str) -> List[BusinessFunction]:
    """Get business functions filtered by complexity"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.complexity == complexity
        )
    ).all()

def get_business_functions_by_maturity(db: Session, tenant_id: UUID, maturity_level: str) -> List[BusinessFunction]:
    """Get business functions filtered by maturity level"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.maturity_level == maturity_level
        )
    ).all()

def get_business_functions_by_operational_hours(db: Session, tenant_id: UUID, operational_hours: str) -> List[BusinessFunction]:
    """Get business functions filtered by operational hours"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.operational_hours == operational_hours
        )
    ).all()

def get_business_functions_by_strategic_importance(db: Session, tenant_id: UUID, strategic_importance: str) -> List[BusinessFunction]:
    """Get business functions filtered by strategic importance"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.strategic_importance == strategic_importance
        )
    ).all()

def get_business_functions_by_business_value(db: Session, tenant_id: UUID, business_value: str) -> List[BusinessFunction]:
    """Get business functions filtered by business value"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.business_value == business_value
        )
    ).all()

def get_business_functions_by_risk_level(db: Session, tenant_id: UUID, risk_level: str) -> List[BusinessFunction]:
    """Get business functions filtered by risk level"""
    return db.query(BusinessFunction).filter(
        and_(
            BusinessFunction.tenant_id == tenant_id,
            BusinessFunction.risk_level == risk_level
        )
    ).all() 