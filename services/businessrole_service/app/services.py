from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from .models import BusinessRole, RoleLink
from .schemas import BusinessRoleCreate, BusinessRoleUpdate, RoleLinkCreate, RoleLinkUpdate
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

def emit_event(event_type: str, business_role_id: UUID, tenant_id: UUID, user_id: UUID, details: dict = None):
    """Emit event to Redis for event-driven architecture"""
    event = {
        "event_type": event_type,
        "business_role_id": str(business_role_id),
        "tenant_id": str(tenant_id),
        "user_id": str(user_id),
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {}
    }
    try:
        redis_client.publish("business_role_events", json.dumps(event))
    except Exception as e:
        print(f"Failed to emit event: {e}")

# Business Role CRUD operations
def create_business_role(db: Session, role_in: BusinessRoleCreate, tenant_id: UUID, user_id: UUID) -> BusinessRole:
    """Create a new business role"""
    db_role = BusinessRole(
        **role_in.dict(),
        tenant_id=tenant_id,
        user_id=user_id
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    
    # Emit event
    emit_event("business_role.created", db_role.id, tenant_id, user_id, {
        "name": db_role.name,
        "role_type": db_role.role_type,
        "organizational_unit": db_role.organizational_unit,
        "strategic_importance": db_role.strategic_importance,
        "status": db_role.status
    })
    
    return db_role

def get_business_role(db: Session, role_id: UUID, tenant_id: UUID) -> BusinessRole:
    """Get a business role by ID with tenant scoping"""
    role = db.query(BusinessRole).filter(
        and_(
            BusinessRole.id == role_id,
            BusinessRole.tenant_id == tenant_id
        )
    ).first()
    
    if not role:
        raise HTTPException(status_code=404, detail="Business role not found")
    
    return role

def get_business_roles(
    db: Session, 
    tenant_id: UUID, 
    skip: int = 0, 
    limit: int = 100,
    organizational_unit: Optional[str] = None,
    role_type: Optional[str] = None,
    strategic_importance: Optional[str] = None,
    authority_level: Optional[str] = None,
    status: Optional[str] = None,
    stakeholder_id: Optional[UUID] = None,
    supporting_capability_id: Optional[UUID] = None,
    business_function_id: Optional[UUID] = None,
    business_process_id: Optional[UUID] = None,
    role_classification: Optional[str] = None,
    criticality: Optional[str] = None
) -> List[BusinessRole]:
    """Get business roles with filtering and pagination"""
    query = db.query(BusinessRole).filter(BusinessRole.tenant_id == tenant_id)
    
    if organizational_unit:
        query = query.filter(BusinessRole.organizational_unit == organizational_unit)
    if role_type:
        query = query.filter(BusinessRole.role_type == role_type)
    if strategic_importance:
        query = query.filter(BusinessRole.strategic_importance == strategic_importance)
    if authority_level:
        query = query.filter(BusinessRole.authority_level == authority_level)
    if status:
        query = query.filter(BusinessRole.status == status)
    if stakeholder_id:
        query = query.filter(BusinessRole.stakeholder_id == stakeholder_id)
    if supporting_capability_id:
        query = query.filter(BusinessRole.supporting_capability_id == supporting_capability_id)
    if business_function_id:
        query = query.filter(BusinessRole.business_function_id == business_function_id)
    if business_process_id:
        query = query.filter(BusinessRole.business_process_id == business_process_id)
    if role_classification:
        query = query.filter(BusinessRole.role_classification == role_classification)
    if criticality:
        query = query.filter(BusinessRole.criticality == criticality)
    
    return query.offset(skip).limit(limit).all()

def update_business_role(
    db: Session, 
    role: BusinessRole, 
    role_in: BusinessRoleUpdate
) -> BusinessRole:
    """Update a business role"""
    update_data = role_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(role, field, value)
    
    role.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(role)
    
    # Emit event
    emit_event("business_role.updated", role.id, role.tenant_id, role.user_id, {
        "name": role.name,
        "role_type": role.role_type,
        "organizational_unit": role.organizational_unit,
        "strategic_importance": role.strategic_importance,
        "status": role.status,
        "updated_fields": list(update_data.keys())
    })
    
    return role

def delete_business_role(db: Session, role: BusinessRole):
    """Delete a business role"""
    role_id = role.id
    tenant_id = role.tenant_id
    user_id = role.user_id
    
    db.delete(role)
    db.commit()
    
    # Emit event
    emit_event("business_role.deleted", role_id, tenant_id, user_id, {
        "name": role.name,
        "role_type": role.role_type
    })

# Role Link operations
def create_role_link(
    db: Session, 
    link_in: RoleLinkCreate, 
    role_id: UUID, 
    user_id: UUID
) -> RoleLink:
    """Create a link between business role and another element"""
    db_link = RoleLink(
        **link_in.dict(),
        business_role_id=role_id,
        created_by=user_id
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    # Emit event
    emit_event("role_link.created", role_id, db_link.business_role.tenant_id, user_id, {
        "linked_element_type": db_link.linked_element_type,
        "link_type": db_link.link_type,
        "relationship_strength": db_link.relationship_strength
    })
    
    return db_link

def get_role_link(db: Session, link_id: UUID, tenant_id: UUID) -> RoleLink:
    """Get a role link by ID with tenant scoping"""
    link = db.query(RoleLink).join(BusinessRole).filter(
        and_(
            RoleLink.id == link_id,
            BusinessRole.tenant_id == tenant_id
        )
    ).first()
    
    if not link:
        raise HTTPException(status_code=404, detail="Role link not found")
    
    return link

def get_role_links(db: Session, role_id: UUID, tenant_id: UUID) -> List[RoleLink]:
    """Get all links for a business role"""
    return db.query(RoleLink).join(BusinessRole).filter(
        and_(
            RoleLink.business_role_id == role_id,
            BusinessRole.tenant_id == tenant_id
        )
    ).all()

def update_role_link(
    db: Session, 
    link: RoleLink, 
    link_in: RoleLinkUpdate
) -> RoleLink:
    """Update a role link"""
    update_data = link_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(link, field, value)
    
    db.commit()
    db.refresh(link)
    
    # Emit event
    emit_event("role_link.updated", link.business_role_id, link.business_role.tenant_id, link.created_by, {
        "linked_element_type": link.linked_element_type,
        "link_type": link.link_type,
        "relationship_strength": link.relationship_strength
    })
    
    return link

def delete_role_link(db: Session, link: RoleLink):
    """Delete a role link"""
    link_id = link.id
    role_id = link.business_role_id
    tenant_id = link.business_role.tenant_id
    user_id = link.created_by
    
    db.delete(link)
    db.commit()
    
    # Emit event
    emit_event("role_link.deleted", role_id, tenant_id, user_id, {
        "linked_element_type": link.linked_element_type,
        "link_type": link.link_type
    })

# Analysis and responsibility mapping
def get_responsibility_map(db: Session, role_id: UUID, tenant_id: UUID) -> dict:
    """Get responsibility map for a business role"""
    role = get_business_role(db, role_id, tenant_id)
    links = get_role_links(db, role_id, tenant_id)
    
    # Count linked elements by type
    business_functions_count = len([link for link in links if "business_function" in link.linked_element_type])
    business_processes_count = len([link for link in links if "business_process" in link.linked_element_type])
    application_services_count = len([link for link in links if "application_service" in link.linked_element_type])
    data_objects_count = len([link for link in links if "data_object" in link.linked_element_type])
    stakeholders_count = len([link for link in links if "stakeholder" in link.linked_element_type])
    
    # Calculate overall responsibility score based on accountability levels and performance impact
    total_links = len(links)
    if total_links > 0:
        full_accountability = len([link for link in links if link.accountability_level == "full"])
        high_performance_impact = len([link for link in links if link.performance_impact == "high"])
        primary_responsibility = len([link for link in links if link.responsibility_level == "primary"])
        overall_responsibility_score = (full_accountability + high_performance_impact + primary_responsibility) / (total_links * 3)
    else:
        overall_responsibility_score = 0.0
    
    return {
        "business_role_id": role_id,
        "linked_elements_count": len(links),
        "business_functions_count": business_functions_count,
        "business_processes_count": business_processes_count,
        "application_services_count": application_services_count,
        "data_objects_count": data_objects_count,
        "stakeholders_count": stakeholders_count,
        "overall_responsibility_score": round(overall_responsibility_score, 2),
        "last_assessed": datetime.utcnow()
    }

def analyze_business_role_alignment(db: Session, role_id: UUID, tenant_id: UUID) -> dict:
    """Analyze a business role for alignment insights"""
    role = get_business_role(db, role_id, tenant_id)
    
    # Calculate scores
    capability_alignment = role.capability_alignment or 0.0
    strategic_alignment = role.strategic_alignment or 0.0
    performance_score = role.performance_score or 0.0
    effectiveness_score = role.effectiveness_score or 0.0
    efficiency_score = role.efficiency_score or 0.0
    satisfaction_score = role.satisfaction_score or 0.0
    
    # Calculate overall alignment score
    overall_alignment_score = (capability_alignment + strategic_alignment + performance_score + effectiveness_score + efficiency_score + satisfaction_score) / 6.0
    
    return {
        "business_role_id": role_id,
        "capability_alignment": round(capability_alignment, 2),
        "strategic_alignment": round(strategic_alignment, 2),
        "performance_score": round(performance_score, 2),
        "effectiveness_score": round(effectiveness_score, 2),
        "efficiency_score": round(efficiency_score, 2),
        "satisfaction_score": round(satisfaction_score, 2),
        "overall_alignment_score": round(overall_alignment_score, 2),
        "last_analyzed": datetime.utcnow()
    }

# Domain logic for queries
def get_business_roles_by_organizational_unit(db: Session, tenant_id: UUID, organizational_unit: str) -> List[BusinessRole]:
    """Get business roles filtered by organizational unit"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.organizational_unit == organizational_unit
        )
    ).all()

def get_business_roles_by_role_type(db: Session, tenant_id: UUID, role_type: str) -> List[BusinessRole]:
    """Get business roles filtered by role type"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.role_type == role_type
        )
    ).all()

def get_business_roles_by_strategic_importance(db: Session, tenant_id: UUID, strategic_importance: str) -> List[BusinessRole]:
    """Get business roles filtered by strategic importance"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.strategic_importance == strategic_importance
        )
    ).all()

def get_business_roles_by_authority_level(db: Session, tenant_id: UUID, authority_level: str) -> List[BusinessRole]:
    """Get business roles filtered by authority level"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.authority_level == authority_level
        )
    ).all()

def get_business_roles_by_status(db: Session, tenant_id: UUID, status: str) -> List[BusinessRole]:
    """Get business roles filtered by status"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.status == status
        )
    ).all()

def get_business_roles_by_stakeholder(db: Session, tenant_id: UUID, stakeholder_id: UUID) -> List[BusinessRole]:
    """Get business roles associated with a specific stakeholder"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.stakeholder_id == stakeholder_id
        )
    ).all()

def get_business_roles_by_capability(db: Session, tenant_id: UUID, capability_id: UUID) -> List[BusinessRole]:
    """Get business roles associated with a specific capability"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.supporting_capability_id == capability_id
        )
    ).all()

def get_business_roles_by_function(db: Session, tenant_id: UUID, function_id: UUID) -> List[BusinessRole]:
    """Get business roles associated with a specific business function"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.business_function_id == function_id
        )
    ).all()

def get_business_roles_by_process(db: Session, tenant_id: UUID, process_id: UUID) -> List[BusinessRole]:
    """Get business roles associated with a specific business process"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.business_process_id == process_id
        )
    ).all()

def get_business_roles_by_element(db: Session, tenant_id: UUID, element_type: str, element_id: UUID) -> List[BusinessRole]:
    """Get business roles that are linked to a specific element"""
    return db.query(BusinessRole).join(RoleLink).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            RoleLink.linked_element_id == element_id,
            RoleLink.linked_element_type == element_type
        )
    ).all()

def get_active_business_roles(db: Session, tenant_id: UUID) -> List[BusinessRole]:
    """Get active business roles"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.status == "active"
        )
    ).all()

def get_critical_business_roles(db: Session, tenant_id: UUID) -> List[BusinessRole]:
    """Get critical business roles"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.criticality.in_(["high", "critical"])
        )
    ).all()

def get_business_roles_by_classification(db: Session, tenant_id: UUID, role_classification: str) -> List[BusinessRole]:
    """Get business roles filtered by role classification"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.role_classification == role_classification
        )
    ).all()

def get_business_roles_by_criticality(db: Session, tenant_id: UUID, criticality: str) -> List[BusinessRole]:
    """Get business roles filtered by criticality"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.criticality == criticality
        )
    ).all()

def get_business_roles_by_workload(db: Session, tenant_id: UUID, workload_level: str) -> List[BusinessRole]:
    """Get business roles filtered by workload level"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.workload_level == workload_level
        )
    ).all()

def get_business_roles_by_availability(db: Session, tenant_id: UUID, availability_requirement: str) -> List[BusinessRole]:
    """Get business roles filtered by availability requirement"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.availability_requirement == availability_requirement
        )
    ).all()

def get_business_roles_by_risk_level(db: Session, tenant_id: UUID, risk_level: str) -> List[BusinessRole]:
    """Get business roles filtered by risk level"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.risk_level == risk_level
        )
    ).all()

def get_business_roles_by_business_value(db: Session, tenant_id: UUID, business_value: str) -> List[BusinessRole]:
    """Get business roles filtered by business value"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.business_value == business_value
        )
    ).all()

def get_business_roles_by_decision_authority(db: Session, tenant_id: UUID, decision_making_authority: str) -> List[BusinessRole]:
    """Get business roles filtered by decision making authority"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.decision_making_authority == decision_making_authority
        )
    ).all()

def get_business_roles_by_approval_authority(db: Session, tenant_id: UUID, approval_authority: str) -> List[BusinessRole]:
    """Get business roles filtered by approval authority"""
    return db.query(BusinessRole).filter(
        and_(
            BusinessRole.tenant_id == tenant_id,
            BusinessRole.approval_authority == approval_authority
        )
    ).all() 