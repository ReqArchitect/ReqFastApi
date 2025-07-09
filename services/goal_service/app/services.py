from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from .models import Goal, GoalLink
from .schemas import GoalCreate, GoalUpdate, GoalLinkCreate, GoalLinkUpdate
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

def emit_event(event_type: str, goal_id: UUID, tenant_id: UUID, user_id: UUID, details: dict = None):
    """Emit event to Redis for event-driven architecture"""
    event = {
        "event_type": event_type,
        "goal_id": str(goal_id),
        "tenant_id": str(tenant_id),
        "user_id": str(user_id),
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {}
    }
    try:
        redis_client.publish("goal_events", json.dumps(event))
    except Exception as e:
        print(f"Failed to emit event: {e}")

# Goal CRUD operations
def create_goal(db: Session, goal_in: GoalCreate, tenant_id: UUID, user_id: UUID) -> Goal:
    """Create a new goal"""
    db_goal = Goal(
        **goal_in.dict(),
        tenant_id=tenant_id,
        user_id=user_id
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    
    # Emit event
    emit_event("goal.created", db_goal.id, tenant_id, user_id, {
        "name": db_goal.name,
        "goal_type": db_goal.goal_type,
        "priority": db_goal.priority,
        "status": db_goal.status
    })
    
    return db_goal

def get_goal(db: Session, goal_id: UUID, tenant_id: UUID) -> Goal:
    """Get a goal by ID with tenant scoping"""
    goal = db.query(Goal).filter(
        and_(
            Goal.id == goal_id,
            Goal.tenant_id == tenant_id
        )
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    return goal

def get_goals(
    db: Session, 
    tenant_id: UUID, 
    skip: int = 0, 
    limit: int = 100,
    goal_type: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    stakeholder_id: Optional[UUID] = None,
    business_actor_id: Optional[UUID] = None,
    origin_driver_id: Optional[UUID] = None,
    parent_goal_id: Optional[UUID] = None
) -> List[Goal]:
    """Get goals with filtering and pagination"""
    query = db.query(Goal).filter(Goal.tenant_id == tenant_id)
    
    if goal_type:
        query = query.filter(Goal.goal_type == goal_type)
    if priority:
        query = query.filter(Goal.priority == priority)
    if status:
        query = query.filter(Goal.status == status)
    if stakeholder_id:
        query = query.filter(Goal.stakeholder_id == stakeholder_id)
    if business_actor_id:
        query = query.filter(Goal.business_actor_id == business_actor_id)
    if origin_driver_id:
        query = query.filter(Goal.origin_driver_id == origin_driver_id)
    if parent_goal_id:
        query = query.filter(Goal.parent_goal_id == parent_goal_id)
    
    return query.offset(skip).limit(limit).all()

def update_goal(
    db: Session, 
    goal: Goal, 
    goal_in: GoalUpdate
) -> Goal:
    """Update a goal"""
    update_data = goal_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(goal, field, value)
    
    goal.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(goal)
    
    # Emit event
    emit_event("goal.updated", goal.id, goal.tenant_id, goal.user_id, {
        "name": goal.name,
        "goal_type": goal.goal_type,
        "priority": goal.priority,
        "status": goal.status,
        "updated_fields": list(update_data.keys())
    })
    
    return goal

def delete_goal(db: Session, goal: Goal):
    """Delete a goal"""
    goal_id = goal.id
    tenant_id = goal.tenant_id
    user_id = goal.user_id
    
    db.delete(goal)
    db.commit()
    
    # Emit event
    emit_event("goal.deleted", goal_id, tenant_id, user_id, {
        "name": goal.name,
        "goal_type": goal.goal_type
    })

# Goal Link operations
def create_goal_link(
    db: Session, 
    link_in: GoalLinkCreate, 
    goal_id: UUID, 
    user_id: UUID
) -> GoalLink:
    """Create a link between goal and another element"""
    db_link = GoalLink(
        **link_in.dict(),
        goal_id=goal_id,
        created_by=user_id
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    # Emit event
    emit_event("goal_link.created", goal_id, db_link.goal.tenant_id, user_id, {
        "linked_element_type": db_link.linked_element_type,
        "link_type": db_link.link_type,
        "relationship_strength": db_link.relationship_strength
    })
    
    return db_link

def get_goal_link(db: Session, link_id: UUID, tenant_id: UUID) -> GoalLink:
    """Get a goal link by ID with tenant scoping"""
    link = db.query(GoalLink).join(Goal).filter(
        and_(
            GoalLink.id == link_id,
            Goal.tenant_id == tenant_id
        )
    ).first()
    
    if not link:
        raise HTTPException(status_code=404, detail="Goal link not found")
    
    return link

def get_goal_links(db: Session, goal_id: UUID, tenant_id: UUID) -> List[GoalLink]:
    """Get all links for a goal"""
    return db.query(GoalLink).join(Goal).filter(
        and_(
            GoalLink.goal_id == goal_id,
            Goal.tenant_id == tenant_id
        )
    ).all()

def update_goal_link(
    db: Session, 
    link: GoalLink, 
    link_in: GoalLinkUpdate
) -> GoalLink:
    """Update a goal link"""
    update_data = link_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(link, field, value)
    
    db.commit()
    db.refresh(link)
    
    # Emit event
    emit_event("goal_link.updated", link.goal_id, link.goal.tenant_id, link.created_by, {
        "linked_element_type": link.linked_element_type,
        "link_type": link.link_type,
        "relationship_strength": link.relationship_strength
    })
    
    return link

def delete_goal_link(db: Session, link: GoalLink):
    """Delete a goal link"""
    link_id = link.id
    goal_id = link.goal_id
    tenant_id = link.goal.tenant_id
    user_id = link.created_by
    
    db.delete(link)
    db.commit()
    
    # Emit event
    emit_event("goal_link.deleted", goal_id, tenant_id, user_id, {
        "linked_element_type": link.linked_element_type,
        "link_type": link.link_type
    })

# Analysis and realization mapping
def get_realization_map(db: Session, goal_id: UUID, tenant_id: UUID) -> dict:
    """Get realization map for a goal"""
    goal = get_goal(db, goal_id, tenant_id)
    links = get_goal_links(db, goal_id, tenant_id)
    
    # Count linked elements by type
    requirements_count = len([link for link in links if "requirement" in link.linked_element_type])
    capabilities_count = len([link for link in links if "capability" in link.linked_element_type])
    courses_of_action_count = len([link for link in links if "course_of_action" in link.linked_element_type])
    stakeholders_count = len([link for link in links if "stakeholder" in link.linked_element_type])
    assessments_count = len([link for link in links if "assessment" in link.linked_element_type])
    
    # Calculate overall realization score based on contribution levels
    total_links = len(links)
    if total_links > 0:
        high_contributions = len([link for link in links if link.contribution_level == "high"])
        medium_contributions = len([link for link in links if link.contribution_level == "medium"])
        overall_realization_score = (high_contributions + (medium_contributions * 0.5)) / total_links
    else:
        overall_realization_score = 0.0
    
    return {
        "goal_id": goal_id,
        "linked_elements_count": len(links),
        "requirements_count": requirements_count,
        "capabilities_count": capabilities_count,
        "courses_of_action_count": courses_of_action_count,
        "stakeholders_count": stakeholders_count,
        "assessments_count": assessments_count,
        "overall_realization_score": round(overall_realization_score, 2),
        "last_assessed": datetime.utcnow()
    }

def get_goal_status_summary(db: Session, goal_id: UUID, tenant_id: UUID) -> dict:
    """Get status summary for a goal"""
    goal = get_goal(db, goal_id, tenant_id)
    links = get_goal_links(db, goal_id, tenant_id)
    
    # Calculate days until target
    days_until_target = None
    if goal.target_date:
        days_until_target = (goal.target_date - datetime.utcnow()).days
    
    return {
        "goal_id": goal_id,
        "status": goal.status,
        "progress_percentage": goal.progress_percentage or 0,
        "days_until_target": days_until_target,
        "assessment_score": goal.assessment_score,
        "risk_level": goal.risk_level,
        "strategic_alignment": goal.strategic_alignment,
        "business_value": goal.business_value,
        "linked_elements_count": len(links),
        "last_updated": goal.updated_at
    }

def analyze_goal(db: Session, goal_id: UUID, tenant_id: UUID) -> dict:
    """Analyze a goal for strategic insights"""
    goal = get_goal(db, goal_id, tenant_id)
    links = get_goal_links(db, goal_id, tenant_id)
    
    # Calculate scores
    priority_score = {"low": 1, "medium": 2, "high": 3, "critical": 4}[goal.priority] / 4.0
    progress_score = (goal.progress_percentage or 0) / 100.0
    risk_score = {"low": 1, "medium": 2, "high": 3, "critical": 4}[goal.risk_level] / 4.0
    
    strategic_alignment_score = 0.5
    if goal.strategic_alignment:
        strategic_alignment_score = {"low": 1, "medium": 2, "high": 3}[goal.strategic_alignment] / 3.0
    
    business_value_score = 0.5
    if goal.business_value:
        business_value_score = {"low": 1, "medium": 2, "high": 3}[goal.business_value] / 3.0
    
    # Calculate overall health score
    overall_health_score = (priority_score + progress_score + (1 - risk_score) + strategic_alignment_score + business_value_score) / 5.0
    
    return {
        "goal_id": goal_id,
        "priority_score": round(priority_score, 2),
        "progress_score": round(progress_score, 2),
        "risk_score": round(risk_score, 2),
        "strategic_alignment_score": round(strategic_alignment_score, 2),
        "business_value_score": round(business_value_score, 2),
        "overall_health_score": round(overall_health_score, 2),
        "last_analyzed": datetime.utcnow()
    }

# Domain logic for queries
def get_goals_by_type(db: Session, tenant_id: UUID, goal_type: str) -> List[Goal]:
    """Get goals filtered by type"""
    return db.query(Goal).filter(
        and_(
            Goal.tenant_id == tenant_id,
            Goal.goal_type == goal_type
        )
    ).all()

def get_goals_by_priority(db: Session, tenant_id: UUID, priority: str) -> List[Goal]:
    """Get goals filtered by priority"""
    return db.query(Goal).filter(
        and_(
            Goal.tenant_id == tenant_id,
            Goal.priority == priority
        )
    ).all()

def get_goals_by_status(db: Session, tenant_id: UUID, status: str) -> List[Goal]:
    """Get goals filtered by status"""
    return db.query(Goal).filter(
        and_(
            Goal.tenant_id == tenant_id,
            Goal.status == status
        )
    ).all()

def get_goals_by_stakeholder(db: Session, tenant_id: UUID, stakeholder_id: UUID) -> List[Goal]:
    """Get goals associated with a specific stakeholder"""
    return db.query(Goal).filter(
        and_(
            Goal.tenant_id == tenant_id,
            Goal.stakeholder_id == stakeholder_id
        )
    ).all()

def get_goals_by_business_actor(db: Session, tenant_id: UUID, business_actor_id: UUID) -> List[Goal]:
    """Get goals associated with a specific business actor"""
    return db.query(Goal).filter(
        and_(
            Goal.tenant_id == tenant_id,
            Goal.business_actor_id == business_actor_id
        )
    ).all()

def get_goals_by_driver(db: Session, tenant_id: UUID, driver_id: UUID) -> List[Goal]:
    """Get goals associated with a specific driver"""
    return db.query(Goal).filter(
        and_(
            Goal.tenant_id == tenant_id,
            Goal.origin_driver_id == driver_id
        )
    ).all()

def get_goals_by_element(db: Session, tenant_id: UUID, element_type: str, element_id: UUID) -> List[Goal]:
    """Get goals that are linked to a specific element"""
    return db.query(Goal).join(GoalLink).filter(
        and_(
            Goal.tenant_id == tenant_id,
            GoalLink.linked_element_id == element_id,
            GoalLink.linked_element_type == element_type
        )
    ).all()

def get_active_goals(db: Session, tenant_id: UUID) -> List[Goal]:
    """Get active goals"""
    return db.query(Goal).filter(
        and_(
            Goal.tenant_id == tenant_id,
            Goal.status == "active"
        )
    ).all()

def get_achieved_goals(db: Session, tenant_id: UUID) -> List[Goal]:
    """Get achieved goals"""
    return db.query(Goal).filter(
        and_(
            Goal.tenant_id == tenant_id,
            Goal.status == "achieved"
        )
    ).all()

def get_goals_due_soon(db: Session, tenant_id: UUID, days_ahead: int = 30) -> List[Goal]:
    """Get goals that are due soon"""
    target_date = datetime.utcnow() + timedelta(days=days_ahead)
    
    return db.query(Goal).filter(
        and_(
            Goal.tenant_id == tenant_id,
            Goal.target_date <= target_date,
            Goal.target_date >= datetime.utcnow(),
            Goal.status == "active"
        )
    ).all()

def get_high_priority_goals(db: Session, tenant_id: UUID) -> List[Goal]:
    """Get high priority goals"""
    return db.query(Goal).filter(
        and_(
            Goal.tenant_id == tenant_id,
            Goal.priority.in_(["high", "critical"])
        )
    ).all()

def get_goals_by_progress_range(db: Session, tenant_id: UUID, min_progress: int, max_progress: int) -> List[Goal]:
    """Get goals within a progress range"""
    return db.query(Goal).filter(
        and_(
            Goal.tenant_id == tenant_id,
            Goal.progress_percentage >= min_progress,
            Goal.progress_percentage <= max_progress
        )
    ).all() 