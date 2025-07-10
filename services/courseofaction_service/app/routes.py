from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from . import services, schemas, deps

router = APIRouter()

# Course of Action CRUD endpoints
@router.post("/courses-of-action", response_model=schemas.CourseOfAction, status_code=status.HTTP_201_CREATED)
def create_course_of_action(
    course_of_action: schemas.CourseOfActionCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    _: str = Depends(deps.rbac_check("course_of_action:create"))
):
    """Create a new course of action"""
    return services.create_course_of_action(db, course_of_action, tenant_id, user_id)

@router.get("/courses-of-action", response_model=List[schemas.CourseOfAction])
def list_courses_of_action(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    strategy_type: Optional[str] = None,
    risk_level: Optional[str] = None,
    time_horizon: Optional[str] = None,
    implementation_phase: Optional[str] = None,
    impacted_capability_id: Optional[UUID] = None,
    approval_status: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("course_of_action:read"))
):
    """List courses of action with filtering"""
    return services.get_courses_of_action(
        db, tenant_id, skip, limit, strategy_type, risk_level, 
        time_horizon, implementation_phase, impacted_capability_id, approval_status
    )

@router.get("/courses-of-action/{course_of_action_id}", response_model=schemas.CourseOfAction)
def get_course_of_action(
    course_of_action_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("course_of_action:read"))
):
    """Get a course of action by ID"""
    course_of_action = services.get_course_of_action(db, course_of_action_id, tenant_id)
    if not course_of_action:
        raise HTTPException(status_code=404, detail="Course of action not found")
    return course_of_action

@router.put("/courses-of-action/{course_of_action_id}", response_model=schemas.CourseOfAction)
def update_course_of_action(
    course_of_action_id: UUID,
    course_of_action_update: schemas.CourseOfActionUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("course_of_action:update"))
):
    """Update a course of action"""
    course_of_action = services.update_course_of_action(db, course_of_action_id, course_of_action_update, tenant_id)
    if not course_of_action:
        raise HTTPException(status_code=404, detail="Course of action not found")
    return course_of_action

@router.delete("/courses-of-action/{course_of_action_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course_of_action(
    course_of_action_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("course_of_action:delete"))
):
    """Delete a course of action"""
    success = services.delete_course_of_action(db, course_of_action_id, tenant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Course of action not found")

# Action Link CRUD endpoints
@router.post("/courses-of-action/{course_of_action_id}/links", response_model=schemas.ActionLink, status_code=status.HTTP_201_CREATED)
def create_action_link(
    course_of_action_id: UUID,
    action_link: schemas.ActionLinkCreate,
    db: Session = Depends(deps.get_db),
    user_id: UUID = Depends(deps.get_current_user),
    _: str = Depends(deps.rbac_check("action_link:create"))
):
    """Create a new action link"""
    return services.create_action_link(db, course_of_action_id, action_link, user_id)

@router.get("/courses-of-action/{course_of_action_id}/links", response_model=List[schemas.ActionLink])
def list_action_links(
    course_of_action_id: UUID,
    db: Session = Depends(deps.get_db),
    _: str = Depends(deps.rbac_check("action_link:read"))
):
    """List all action links for a course of action"""
    return services.get_action_links(db, course_of_action_id)

@router.get("/courses-of-action/links/{link_id}", response_model=schemas.ActionLink)
def get_action_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    _: str = Depends(deps.rbac_check("action_link:read"))
):
    """Get an action link by ID"""
    action_link = services.get_action_link(db, link_id)
    if not action_link:
        raise HTTPException(status_code=404, detail="Action link not found")
    return action_link

@router.put("/courses-of-action/links/{link_id}", response_model=schemas.ActionLink)
def update_action_link(
    link_id: UUID,
    action_link_update: schemas.ActionLinkUpdate,
    db: Session = Depends(deps.get_db),
    _: str = Depends(deps.rbac_check("action_link:update"))
):
    """Update an action link"""
    action_link = services.update_action_link(db, link_id, action_link_update)
    if not action_link:
        raise HTTPException(status_code=404, detail="Action link not found")
    return action_link

@router.delete("/courses-of-action/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_action_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    _: str = Depends(deps.rbac_check("action_link:delete"))
):
    """Delete an action link"""
    success = services.delete_action_link(db, link_id)
    if not success:
        raise HTTPException(status_code=404, detail="Action link not found")

# Analysis and alignment endpoints
@router.get("/courses-of-action/{course_of_action_id}/alignment-map")
def get_alignment_map(
    course_of_action_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("alignment:read"))
):
    """Get alignment map for a course of action"""
    alignment_map = services.get_alignment_map(db, course_of_action_id, tenant_id)
    if not alignment_map:
        raise HTTPException(status_code=404, detail="Course of action not found")
    return alignment_map

@router.get("/courses-of-action/{course_of_action_id}/risk-profile")
def get_risk_profile(
    course_of_action_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("risk:read"))
):
    """Get risk profile for a course of action"""
    risk_profile = services.get_risk_profile(db, course_of_action_id, tenant_id)
    if not risk_profile:
        raise HTTPException(status_code=404, detail="Course of action not found")
    return risk_profile

@router.get("/courses-of-action/{course_of_action_id}/analysis")
def analyze_course_of_action(
    course_of_action_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("analysis:read"))
):
    """Get comprehensive analysis for a course of action"""
    analysis = services.analyze_course_of_action(db, course_of_action_id, tenant_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Course of action not found")
    return analysis

# Domain-specific query endpoints
@router.get("/courses-of-action/by-type/{strategy_type}", response_model=List[schemas.CourseOfAction])
def get_courses_of_action_by_strategy_type(
    strategy_type: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("course_of_action:read"))
):
    """Get courses of action by strategy type"""
    return services.get_courses_of_action_by_strategy_type(db, tenant_id, strategy_type)

@router.get("/courses-of-action/by-capability/{capability_id}", response_model=List[schemas.CourseOfAction])
def get_courses_of_action_by_capability(
    capability_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("course_of_action:read"))
):
    """Get courses of action by impacted capability"""
    return services.get_courses_of_action_by_capability(db, tenant_id, capability_id)

@router.get("/courses-of-action/by-risk-level/{risk_level}", response_model=List[schemas.CourseOfAction])
def get_courses_of_action_by_risk_level(
    risk_level: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("course_of_action:read"))
):
    """Get courses of action by risk level"""
    return services.get_courses_of_action_by_risk_level(db, tenant_id, risk_level)

@router.get("/courses-of-action/by-time-horizon/{time_horizon}", response_model=List[schemas.CourseOfAction])
def get_courses_of_action_by_time_horizon(
    time_horizon: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("course_of_action:read"))
):
    """Get courses of action by time horizon"""
    return services.get_courses_of_action_by_time_horizon(db, tenant_id, time_horizon)

@router.get("/courses-of-action/by-element/{element_type}/{element_id}", response_model=List[schemas.CourseOfAction])
def get_courses_of_action_by_element(
    element_type: str,
    element_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("course_of_action:read"))
):
    """Get courses of action linked to a specific element"""
    return services.get_courses_of_action_by_element(db, tenant_id, element_type, element_id)

@router.get("/courses-of-action/active", response_model=List[schemas.CourseOfAction])
def get_active_courses_of_action(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("course_of_action:read"))
):
    """Get all active courses of action"""
    return services.get_active_courses_of_action(db, tenant_id)

@router.get("/courses-of-action/critical", response_model=List[schemas.CourseOfAction])
def get_critical_courses_of_action(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("course_of_action:read"))
):
    """Get all critical courses of action"""
    return services.get_critical_courses_of_action(db, tenant_id)

# Enumeration endpoints
@router.get("/courses-of-action/strategy-types")
def get_strategy_types():
    """Get all available strategy types"""
    return services.get_strategy_types()

@router.get("/courses-of-action/time-horizons")
def get_time_horizons():
    """Get all available time horizons"""
    return services.get_time_horizons()

@router.get("/courses-of-action/implementation-phases")
def get_implementation_phases():
    """Get all available implementation phases"""
    return services.get_implementation_phases()

@router.get("/courses-of-action/risk-levels")
def get_risk_levels():
    """Get all available risk levels"""
    return services.get_risk_levels()

@router.get("/courses-of-action/approval-statuses")
def get_approval_statuses():
    """Get all available approval statuses"""
    return services.get_approval_statuses()

@router.get("/courses-of-action/governance-models")
def get_governance_models():
    """Get all available governance models"""
    return services.get_governance_models()

@router.get("/courses-of-action/link-types")
def get_link_types():
    """Get all available link types"""
    return services.get_link_types()

@router.get("/courses-of-action/relationship-strengths")
def get_relationship_strengths():
    """Get all available relationship strengths"""
    return services.get_relationship_strengths()

@router.get("/courses-of-action/dependency-levels")
def get_dependency_levels():
    """Get all available dependency levels"""
    return services.get_dependency_levels()

@router.get("/courses-of-action/strategic-importances")
def get_strategic_importances():
    """Get all available strategic importance levels"""
    return services.get_strategic_importances()

@router.get("/courses-of-action/business-values")
def get_business_values():
    """Get all available business value levels"""
    return services.get_business_values()

@router.get("/courses-of-action/implementation-priorities")
def get_implementation_priorities():
    """Get all available implementation priorities"""
    return services.get_implementation_priorities()

@router.get("/courses-of-action/impact-levels")
def get_impact_levels():
    """Get all available impact levels"""
    return services.get_impact_levels()

@router.get("/courses-of-action/impact-directions")
def get_impact_directions():
    """Get all available impact directions"""
    return services.get_impact_directions()

@router.get("/courses-of-action/constraint-levels")
def get_constraint_levels():
    """Get all available constraint levels"""
    return services.get_constraint_levels() 