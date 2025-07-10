from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from .models import CourseOfAction, ActionLink
from .schemas import CourseOfActionCreate, CourseOfActionUpdate, ActionLinkCreate, ActionLinkUpdate
from .database import SessionLocal
from uuid import UUID
from typing import List, Optional, Dict, Any
import redis
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL)

def emit_event(event_type: str, data: Dict[str, Any]):
    """Emit event to Redis for event-driven architecture"""
    try:
        event = {
            "event_type": event_type,
            "service": "courseofaction_service",
            "data": data,
            "timestamp": str(datetime.utcnow())
        }
        redis_client.publish("courseofaction_events", json.dumps(event))
    except Exception as e:
        print(f"Failed to emit event: {e}")

# Course of Action CRUD operations
def create_course_of_action(db: Session, course_of_action: CourseOfActionCreate, tenant_id: UUID, user_id: UUID) -> CourseOfAction:
    """Create a new course of action"""
    db_course_of_action = CourseOfAction(
        **course_of_action.dict(),
        tenant_id=tenant_id,
        user_id=user_id
    )
    db.add(db_course_of_action)
    db.commit()
    db.refresh(db_course_of_action)
    
    # Emit event
    emit_event("course_of_action_created", {
        "course_of_action_id": str(db_course_of_action.id),
        "tenant_id": str(tenant_id),
        "user_id": str(user_id)
    })
    
    return db_course_of_action

def get_course_of_action(db: Session, course_of_action_id: UUID, tenant_id: UUID) -> Optional[CourseOfAction]:
    """Get a course of action by ID"""
    return db.query(CourseOfAction).filter(
        and_(
            CourseOfAction.id == course_of_action_id,
            CourseOfAction.tenant_id == tenant_id
        )
    ).first()

def get_courses_of_action(
    db: Session, 
    tenant_id: UUID, 
    skip: int = 0, 
    limit: int = 100,
    strategy_type: Optional[str] = None,
    risk_level: Optional[str] = None,
    time_horizon: Optional[str] = None,
    implementation_phase: Optional[str] = None,
    impacted_capability_id: Optional[UUID] = None,
    approval_status: Optional[str] = None
) -> List[CourseOfAction]:
    """Get courses of action with filtering"""
    query = db.query(CourseOfAction).filter(CourseOfAction.tenant_id == tenant_id)
    
    if strategy_type:
        query = query.filter(CourseOfAction.strategy_type == strategy_type)
    if risk_level:
        query = query.filter(CourseOfAction.risk_level == risk_level)
    if time_horizon:
        query = query.filter(CourseOfAction.time_horizon == time_horizon)
    if implementation_phase:
        query = query.filter(CourseOfAction.implementation_phase == implementation_phase)
    if impacted_capability_id:
        query = query.filter(CourseOfAction.impacted_capability_id == impacted_capability_id)
    if approval_status:
        query = query.filter(CourseOfAction.approval_status == approval_status)
    
    return query.offset(skip).limit(limit).all()

def update_course_of_action(
    db: Session, 
    course_of_action_id: UUID, 
    course_of_action_update: CourseOfActionUpdate, 
    tenant_id: UUID
) -> Optional[CourseOfAction]:
    """Update a course of action"""
    db_course_of_action = get_course_of_action(db, course_of_action_id, tenant_id)
    if not db_course_of_action:
        return None
    
    update_data = course_of_action_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course_of_action, field, value)
    
    db.commit()
    db.refresh(db_course_of_action)
    
    # Emit event
    emit_event("course_of_action_updated", {
        "course_of_action_id": str(course_of_action_id),
        "tenant_id": str(tenant_id)
    })
    
    return db_course_of_action

def delete_course_of_action(db: Session, course_of_action_id: UUID, tenant_id: UUID) -> bool:
    """Delete a course of action"""
    db_course_of_action = get_course_of_action(db, course_of_action_id, tenant_id)
    if not db_course_of_action:
        return False
    
    db.delete(db_course_of_action)
    db.commit()
    
    # Emit event
    emit_event("course_of_action_deleted", {
        "course_of_action_id": str(course_of_action_id),
        "tenant_id": str(tenant_id)
    })
    
    return True

# Action Link CRUD operations
def create_action_link(
    db: Session, 
    course_of_action_id: UUID, 
    action_link: ActionLinkCreate, 
    user_id: UUID
) -> ActionLink:
    """Create a new action link"""
    db_action_link = ActionLink(
        **action_link.dict(),
        course_of_action_id=course_of_action_id,
        created_by=user_id
    )
    db.add(db_action_link)
    db.commit()
    db.refresh(db_action_link)
    
    # Emit event
    emit_event("action_link_created", {
        "action_link_id": str(db_action_link.id),
        "course_of_action_id": str(course_of_action_id),
        "user_id": str(user_id)
    })
    
    return db_action_link

def get_action_link(db: Session, action_link_id: UUID) -> Optional[ActionLink]:
    """Get an action link by ID"""
    return db.query(ActionLink).filter(ActionLink.id == action_link_id).first()

def get_action_links(db: Session, course_of_action_id: UUID) -> List[ActionLink]:
    """Get all action links for a course of action"""
    return db.query(ActionLink).filter(ActionLink.course_of_action_id == course_of_action_id).all()

def update_action_link(
    db: Session, 
    action_link_id: UUID, 
    action_link_update: ActionLinkUpdate
) -> Optional[ActionLink]:
    """Update an action link"""
    db_action_link = get_action_link(db, action_link_id)
    if not db_action_link:
        return None
    
    update_data = action_link_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_action_link, field, value)
    
    db.commit()
    db.refresh(db_action_link)
    
    # Emit event
    emit_event("action_link_updated", {
        "action_link_id": str(action_link_id)
    })
    
    return db_action_link

def delete_action_link(db: Session, action_link_id: UUID) -> bool:
    """Delete an action link"""
    db_action_link = get_action_link(db, action_link_id)
    if not db_action_link:
        return False
    
    db.delete(db_action_link)
    db.commit()
    
    # Emit event
    emit_event("action_link_deleted", {
        "action_link_id": str(action_link_id)
    })
    
    return True

# Analysis and alignment functions
def get_alignment_map(db: Session, course_of_action_id: UUID, tenant_id: UUID) -> Dict[str, Any]:
    """Get alignment map for a course of action"""
    course_of_action = get_course_of_action(db, course_of_action_id, tenant_id)
    if not course_of_action:
        return {}
    
    # Calculate alignment scores
    strategic_alignment = {
        "score": course_of_action.strategic_alignment_score,
        "factors": ["goal_alignment", "capability_alignment", "stakeholder_alignment"],
        "status": "high" if course_of_action.strategic_alignment_score > 0.7 else "medium" if course_of_action.strategic_alignment_score > 0.4 else "low"
    }
    
    capability_alignment = {
        "score": course_of_action.capability_impact_score,
        "capability_id": str(course_of_action.impacted_capability_id) if course_of_action.impacted_capability_id else None,
        "status": "high" if course_of_action.capability_impact_score > 0.7 else "medium" if course_of_action.capability_impact_score > 0.4 else "low"
    }
    
    goal_alignment = {
        "score": course_of_action.goal_achievement_score,
        "goal_id": str(course_of_action.origin_goal_id) if course_of_action.origin_goal_id else None,
        "status": "high" if course_of_action.goal_achievement_score > 0.7 else "medium" if course_of_action.goal_achievement_score > 0.4 else "low"
    }
    
    # Calculate overall alignment score
    alignment_scores = [course_of_action.strategic_alignment_score, course_of_action.capability_impact_score, course_of_action.goal_achievement_score]
    overall_alignment_score = sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0.0
    
    # Generate recommendations
    recommendations = []
    if course_of_action.strategic_alignment_score < 0.5:
        recommendations.append("Improve strategic alignment by reviewing goal connections")
    if course_of_action.capability_impact_score < 0.5:
        recommendations.append("Enhance capability impact assessment")
    if course_of_action.goal_achievement_score < 0.5:
        recommendations.append("Strengthen goal achievement tracking")
    
    return {
        "course_of_action_id": course_of_action_id,
        "strategic_alignment": strategic_alignment,
        "capability_alignment": capability_alignment,
        "goal_alignment": goal_alignment,
        "overall_alignment_score": overall_alignment_score,
        "alignment_factors": [
            {"factor": "strategic_alignment", "score": course_of_action.strategic_alignment_score},
            {"factor": "capability_impact", "score": course_of_action.capability_impact_score},
            {"factor": "goal_achievement", "score": course_of_action.goal_achievement_score}
        ],
        "recommendations": recommendations
    }

def get_risk_profile(db: Session, course_of_action_id: UUID, tenant_id: UUID) -> Dict[str, Any]:
    """Get risk profile for a course of action"""
    course_of_action = get_course_of_action(db, course_of_action_id, tenant_id)
    if not course_of_action:
        return {}
    
    # Calculate risk factors
    risk_factors = []
    if course_of_action.risk_level in ["high", "critical"]:
        risk_factors.append({
            "factor": "overall_risk_level",
            "severity": course_of_action.risk_level,
            "description": f"High risk level: {course_of_action.risk_level}"
        })
    
    if course_of_action.success_probability < 0.5:
        risk_factors.append({
            "factor": "low_success_probability",
            "severity": "high" if course_of_action.success_probability < 0.3 else "medium",
            "description": f"Low success probability: {course_of_action.success_probability}"
        })
    
    if course_of_action.current_progress < 25 and course_of_action.implementation_phase == "active":
        risk_factors.append({
            "factor": "slow_progress",
            "severity": "medium",
            "description": f"Slow progress: {course_of_action.current_progress}%"
        })
    
    # Calculate overall risk score
    risk_score_factors = []
    if course_of_action.risk_level == "critical":
        risk_score_factors.append(1.0)
    elif course_of_action.risk_level == "high":
        risk_score_factors.append(0.8)
    elif course_of_action.risk_level == "medium":
        risk_score_factors.append(0.5)
    else:
        risk_score_factors.append(0.2)
    
    risk_score_factors.append(1.0 - course_of_action.success_probability)
    
    overall_risk_score = sum(risk_score_factors) / len(risk_score_factors)
    
    # Generate mitigation strategies
    mitigation_strategies = []
    if course_of_action.risk_level in ["high", "critical"]:
        mitigation_strategies.append({
            "strategy": "enhanced_monitoring",
            "description": "Implement enhanced monitoring and early warning systems"
        })
    
    if course_of_action.success_probability < 0.5:
        mitigation_strategies.append({
            "strategy": "success_improvement",
            "description": "Review and improve success criteria and implementation approach"
        })
    
    # Generate recommendations
    recommendations = []
    if overall_risk_score > 0.7:
        recommendations.append("Implement comprehensive risk mitigation plan")
    if course_of_action.success_probability < 0.5:
        recommendations.append("Review and revise success criteria")
    if course_of_action.current_progress < 25:
        recommendations.append("Accelerate implementation progress")
    
    return {
        "course_of_action_id": course_of_action_id,
        "overall_risk_score": overall_risk_score,
        "risk_breakdown": {
            "risk_level": course_of_action.risk_level,
            "success_probability": course_of_action.success_probability,
            "progress_risk": 1.0 - (course_of_action.current_progress / 100.0)
        },
        "risk_factors": risk_factors,
        "mitigation_strategies": mitigation_strategies,
        "contingency_plans": json.loads(course_of_action.contingency_plans) if course_of_action.contingency_plans else [],
        "risk_monitoring": {
            "monitoring_frequency": "weekly" if overall_risk_score > 0.7 else "monthly",
            "key_metrics": ["progress", "success_probability", "risk_level"],
            "alert_thresholds": {"risk_score": 0.7, "progress_stall": 0}
        },
        "recommendations": recommendations
    }

def analyze_course_of_action(db: Session, course_of_action_id: UUID, tenant_id: UUID) -> Dict[str, Any]:
    """Comprehensive analysis of a course of action"""
    course_of_action = get_course_of_action(db, course_of_action_id, tenant_id)
    if not course_of_action:
        return {}
    
    # Strategic analysis
    strategic_analysis = {
        "strategy_type": course_of_action.strategy_type,
        "time_horizon": course_of_action.time_horizon,
        "strategic_objective": course_of_action.strategic_objective,
        "business_case": course_of_action.business_case,
        "alignment_score": course_of_action.strategic_alignment_score
    }
    
    # Performance analysis
    performance_analysis = {
        "current_progress": course_of_action.current_progress,
        "success_probability": course_of_action.success_probability,
        "implementation_phase": course_of_action.implementation_phase,
        "performance_metrics": json.loads(course_of_action.performance_metrics) if course_of_action.performance_metrics else {}
    }
    
    # Risk analysis
    risk_analysis = {
        "risk_level": course_of_action.risk_level,
        "risk_assessment": json.loads(course_of_action.risk_assessment) if course_of_action.risk_assessment else {},
        "contingency_plans": json.loads(course_of_action.contingency_plans) if course_of_action.contingency_plans else []
    }
    
    # Cost analysis
    cost_analysis = {
        "estimated_cost": course_of_action.estimated_cost,
        "actual_cost": course_of_action.actual_cost,
        "budget_allocation": course_of_action.budget_allocation,
        "cost_benefit_analysis": json.loads(course_of_action.cost_benefit_analysis) if course_of_action.cost_benefit_analysis else {}
    }
    
    # Implementation analysis
    implementation_analysis = {
        "implementation_approach": course_of_action.implementation_approach,
        "milestones": json.loads(course_of_action.milestones) if course_of_action.milestones else [],
        "dependencies": json.loads(course_of_action.dependencies) if course_of_action.dependencies else [],
        "constraints": json.loads(course_of_action.constraints) if course_of_action.constraints else []
    }
    
    # Outcome analysis
    outcome_analysis = {
        "outcomes_achieved": json.loads(course_of_action.outcomes_achieved) if course_of_action.outcomes_achieved else [],
        "lessons_learned": json.loads(course_of_action.lessons_learned) if course_of_action.lessons_learned else [],
        "overall_effectiveness_score": course_of_action.overall_effectiveness_score
    }
    
    # Generate recommendations
    recommendations = []
    if course_of_action.current_progress < 25:
        recommendations.append("Accelerate implementation progress")
    if course_of_action.success_probability < 0.5:
        recommendations.append("Review and improve success criteria")
    if course_of_action.risk_level in ["high", "critical"]:
        recommendations.append("Implement comprehensive risk mitigation")
    if course_of_action.strategic_alignment_score < 0.5:
        recommendations.append("Improve strategic alignment")
    
    return {
        "course_of_action_id": course_of_action_id,
        "strategic_analysis": strategic_analysis,
        "performance_analysis": performance_analysis,
        "risk_analysis": risk_analysis,
        "cost_analysis": cost_analysis,
        "implementation_analysis": implementation_analysis,
        "outcome_analysis": outcome_analysis,
        "recommendations": recommendations
    }

# Domain-specific query functions
def get_courses_of_action_by_strategy_type(db: Session, tenant_id: UUID, strategy_type: str) -> List[CourseOfAction]:
    """Get courses of action by strategy type"""
    return db.query(CourseOfAction).filter(
        and_(
            CourseOfAction.tenant_id == tenant_id,
            CourseOfAction.strategy_type == strategy_type
        )
    ).all()

def get_courses_of_action_by_capability(db: Session, tenant_id: UUID, capability_id: UUID) -> List[CourseOfAction]:
    """Get courses of action by impacted capability"""
    return db.query(CourseOfAction).filter(
        and_(
            CourseOfAction.tenant_id == tenant_id,
            CourseOfAction.impacted_capability_id == capability_id
        )
    ).all()

def get_courses_of_action_by_risk_level(db: Session, tenant_id: UUID, risk_level: str) -> List[CourseOfAction]:
    """Get courses of action by risk level"""
    return db.query(CourseOfAction).filter(
        and_(
            CourseOfAction.tenant_id == tenant_id,
            CourseOfAction.risk_level == risk_level
        )
    ).all()

def get_courses_of_action_by_time_horizon(db: Session, tenant_id: UUID, time_horizon: str) -> List[CourseOfAction]:
    """Get courses of action by time horizon"""
    return db.query(CourseOfAction).filter(
        and_(
            CourseOfAction.tenant_id == tenant_id,
            CourseOfAction.time_horizon == time_horizon
        )
    ).all()

def get_active_courses_of_action(db: Session, tenant_id: UUID) -> List[CourseOfAction]:
    """Get all active courses of action"""
    return db.query(CourseOfAction).filter(
        and_(
            CourseOfAction.tenant_id == tenant_id,
            CourseOfAction.implementation_phase == "active"
        )
    ).all()

def get_critical_courses_of_action(db: Session, tenant_id: UUID) -> List[CourseOfAction]:
    """Get all critical courses of action"""
    return db.query(CourseOfAction).filter(
        and_(
            CourseOfAction.tenant_id == tenant_id,
            or_(
                CourseOfAction.risk_level == "critical",
                CourseOfAction.business_criticality == "critical"
            )
        )
    ).all()

def get_courses_of_action_by_element(db: Session, tenant_id: UUID, element_type: str, element_id: UUID) -> List[CourseOfAction]:
    """Get courses of action linked to a specific element"""
    # This would require joining with ActionLink table
    action_links = db.query(ActionLink).filter(
        and_(
            ActionLink.linked_element_type == element_type,
            ActionLink.linked_element_id == element_id
        )
    ).all()
    
    course_of_action_ids = [link.course_of_action_id for link in action_links]
    return db.query(CourseOfAction).filter(
        and_(
            CourseOfAction.tenant_id == tenant_id,
            CourseOfAction.id.in_(course_of_action_ids)
        )
    ).all()

# Enumeration functions
def get_strategy_types() -> List[str]:
    """Get all available strategy types"""
    return ["transformational", "incremental", "defensive", "innovative"]

def get_time_horizons() -> List[str]:
    """Get all available time horizons"""
    return ["short_term", "medium_term", "long_term"]

def get_implementation_phases() -> List[str]:
    """Get all available implementation phases"""
    return ["planning", "active", "completed", "suspended"]

def get_risk_levels() -> List[str]:
    """Get all available risk levels"""
    return ["low", "medium", "high", "critical"]

def get_approval_statuses() -> List[str]:
    """Get all available approval statuses"""
    return ["draft", "pending", "approved", "rejected", "completed"]

def get_governance_models() -> List[str]:
    """Get all available governance models"""
    return ["basic", "standard", "enhanced", "critical"]

def get_link_types() -> List[str]:
    """Get all available link types"""
    return ["realizes", "supports", "enables", "influences", "constrains", "triggers", "requires"]

def get_relationship_strengths() -> List[str]:
    """Get all available relationship strengths"""
    return ["strong", "medium", "weak"]

def get_dependency_levels() -> List[str]:
    """Get all available dependency levels"""
    return ["high", "medium", "low"]

def get_strategic_importances() -> List[str]:
    """Get all available strategic importance levels"""
    return ["low", "medium", "high", "critical"]

def get_business_values() -> List[str]:
    """Get all available business value levels"""
    return ["low", "medium", "high", "critical"]

def get_implementation_priorities() -> List[str]:
    """Get all available implementation priorities"""
    return ["low", "normal", "high", "critical"]

def get_impact_levels() -> List[str]:
    """Get all available impact levels"""
    return ["low", "medium", "high", "critical"]

def get_impact_directions() -> List[str]:
    """Get all available impact directions"""
    return ["positive", "negative", "neutral"]

def get_constraint_levels() -> List[str]:
    """Get all available constraint levels"""
    return ["low", "medium", "high", "critical"] 