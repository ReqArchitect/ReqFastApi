from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from . import schemas, services, deps
from .models import Goal, GoalLink

router = APIRouter(prefix="/goals", tags=["Goals"])

# Goal CRUD endpoints
@router.post("/", response_model=schemas.Goal, status_code=201)
def create_goal(
    goal_in: schemas.GoalCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    rbac=Depends(deps.rbac_check("goal:create"))
):
    """Create a new goal"""
    return services.create_goal(db, goal_in, tenant_id, user_id)

@router.get("/", response_model=List[schemas.Goal])
def list_goals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    goal_type: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    stakeholder_id: Optional[UUID] = Query(None),
    business_actor_id: Optional[UUID] = Query(None),
    origin_driver_id: Optional[UUID] = Query(None),
    parent_goal_id: Optional[UUID] = Query(None),
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """List goals with filtering and pagination"""
    return services.get_goals(
        db, tenant_id, skip, limit, goal_type, priority, status, 
        stakeholder_id, business_actor_id, origin_driver_id, parent_goal_id
    )

@router.get("/{goal_id}", response_model=schemas.Goal)
def get_goal(
    goal_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """Get a goal by ID"""
    return services.get_goal(db, goal_id, tenant_id)

@router.put("/{goal_id}", response_model=schemas.Goal)
def update_goal(
    goal_id: UUID,
    goal_in: schemas.GoalUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:update"))
):
    """Update a goal"""
    goal = services.get_goal(db, goal_id, tenant_id)
    return services.update_goal(db, goal, goal_in)

@router.delete("/{goal_id}", status_code=204)
def delete_goal(
    goal_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:delete"))
):
    """Delete a goal"""
    goal = services.get_goal(db, goal_id, tenant_id)
    services.delete_goal(db, goal)
    return {"ok": True}

# Goal Link endpoints
@router.post("/{goal_id}/links", response_model=schemas.GoalLink, status_code=201)
def create_goal_link(
    goal_id: UUID,
    link_in: schemas.GoalLinkCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    rbac=Depends(deps.rbac_check("goal_link:create"))
):
    """Create a link between goal and another element"""
    # Verify goal exists and belongs to tenant
    services.get_goal(db, goal_id, tenant_id)
    return services.create_goal_link(db, link_in, goal_id, user_id)

@router.get("/{goal_id}/links", response_model=List[schemas.GoalLink])
def list_goal_links(
    goal_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal_link:read"))
):
    """List all links for a goal"""
    # Verify goal exists and belongs to tenant
    services.get_goal(db, goal_id, tenant_id)
    return services.get_goal_links(db, goal_id, tenant_id)

@router.get("/links/{link_id}", response_model=schemas.GoalLink)
def get_goal_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal_link:read"))
):
    """Get a goal link by ID"""
    return services.get_goal_link(db, link_id, tenant_id)

@router.put("/links/{link_id}", response_model=schemas.GoalLink)
def update_goal_link(
    link_id: UUID,
    link_in: schemas.GoalLinkUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal_link:update"))
):
    """Update a goal link"""
    link = services.get_goal_link(db, link_id, tenant_id)
    return services.update_goal_link(db, link, link_in)

@router.delete("/links/{link_id}", status_code=204)
def delete_goal_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal_link:delete"))
):
    """Delete a goal link"""
    link = services.get_goal_link(db, link_id, tenant_id)
    services.delete_goal_link(db, link)
    return {"ok": True}

# Analysis and realization mapping endpoints
@router.get("/{goal_id}/realization-map", response_model=schemas.RealizationMap)
def get_realization_map(
    goal_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("realization:read"))
):
    """Get realization map for a goal"""
    return services.get_realization_map(db, goal_id, tenant_id)

@router.get("/{goal_id}/status-summary", response_model=schemas.GoalStatusSummary)
def get_goal_status_summary(
    goal_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("analysis:read"))
):
    """Get status summary for a goal"""
    return services.get_goal_status_summary(db, goal_id, tenant_id)

@router.get("/{goal_id}/analysis", response_model=schemas.GoalAnalysis)
def analyze_goal(
    goal_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("analysis:read"))
):
    """Analyze a goal for strategic insights"""
    return services.analyze_goal(db, goal_id, tenant_id)

# Domain-specific query endpoints
@router.get("/by-type/{goal_type}", response_model=List[schemas.Goal])
def get_goals_by_type(
    goal_type: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """Get goals filtered by type"""
    return services.get_goals_by_type(db, tenant_id, goal_type)

@router.get("/by-priority/{priority}", response_model=List[schemas.Goal])
def get_goals_by_priority(
    priority: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """Get goals filtered by priority"""
    return services.get_goals_by_priority(db, tenant_id, priority)

@router.get("/by-status/{status}", response_model=List[schemas.Goal])
def get_goals_by_status(
    status: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """Get goals filtered by status"""
    return services.get_goals_by_status(db, tenant_id, status)

@router.get("/by-stakeholder/{stakeholder_id}", response_model=List[schemas.Goal])
def get_goals_by_stakeholder(
    stakeholder_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """Get goals associated with a specific stakeholder"""
    return services.get_goals_by_stakeholder(db, tenant_id, stakeholder_id)

@router.get("/by-business-actor/{business_actor_id}", response_model=List[schemas.Goal])
def get_goals_by_business_actor(
    business_actor_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """Get goals associated with a specific business actor"""
    return services.get_goals_by_business_actor(db, tenant_id, business_actor_id)

@router.get("/by-driver/{driver_id}", response_model=List[schemas.Goal])
def get_goals_by_driver(
    driver_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """Get goals associated with a specific driver"""
    return services.get_goals_by_driver(db, tenant_id, driver_id)

@router.get("/by-element/{element_type}/{element_id}", response_model=List[schemas.Goal])
def get_goals_by_element(
    element_type: str,
    element_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """Get goals that are linked to a specific element"""
    return services.get_goals_by_element(db, tenant_id, element_type, element_id)

@router.get("/active", response_model=List[schemas.Goal])
def get_active_goals(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """Get active goals"""
    return services.get_active_goals(db, tenant_id)

@router.get("/achieved", response_model=List[schemas.Goal])
def get_achieved_goals(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """Get achieved goals"""
    return services.get_achieved_goals(db, tenant_id)

@router.get("/due-soon/{days_ahead}", response_model=List[schemas.Goal])
def get_goals_due_soon(
    days_ahead: int = Query(30, ge=1, le=365),
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """Get goals that are due soon"""
    return services.get_goals_due_soon(db, tenant_id, days_ahead)

@router.get("/high-priority", response_model=List[schemas.Goal])
def get_high_priority_goals(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """Get high priority goals"""
    return services.get_high_priority_goals(db, tenant_id)

@router.get("/by-progress/{min_progress}/{max_progress}", response_model=List[schemas.Goal])
def get_goals_by_progress_range(
    min_progress: int = Query(..., ge=0, le=100),
    max_progress: int = Query(..., ge=0, le=100),
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("goal:read"))
):
    """Get goals within a progress range"""
    return services.get_goals_by_progress_range(db, tenant_id, min_progress, max_progress)

# Utility endpoints
@router.get("/types", response_model=List[str])
def get_goal_types():
    """Get all available goal types"""
    return [e.value for e in schemas.GoalType]

@router.get("/priorities", response_model=List[str])
def get_priorities():
    """Get all available priorities"""
    return [e.value for e in schemas.Priority]

@router.get("/statuses", response_model=List[str])
def get_statuses():
    """Get all available statuses"""
    return [e.value for e in schemas.GoalStatus]

@router.get("/measurement-frequencies", response_model=List[str])
def get_measurement_frequencies():
    """Get all available measurement frequencies"""
    return [e.value for e in schemas.MeasurementFrequency]

@router.get("/review-frequencies", response_model=List[str])
def get_review_frequencies():
    """Get all available review frequencies"""
    return [e.value for e in schemas.ReviewFrequency]

@router.get("/strategic-alignments", response_model=List[str])
def get_strategic_alignments():
    """Get all available strategic alignments"""
    return [e.value for e in schemas.StrategicAlignment]

@router.get("/business-values", response_model=List[str])
def get_business_values():
    """Get all available business values"""
    return [e.value for e in schemas.BusinessValue]

@router.get("/risk-levels", response_model=List[str])
def get_risk_levels():
    """Get all available risk levels"""
    return [e.value for e in schemas.RiskLevel]

@router.get("/assessment-statuses", response_model=List[str])
def get_assessment_statuses():
    """Get all available assessment statuses"""
    return [e.value for e in schemas.AssessmentStatus]

@router.get("/link-types", response_model=List[str])
def get_link_types():
    """Get all available link types"""
    return [e.value for e in schemas.LinkType]

@router.get("/relationship-strengths", response_model=List[str])
def get_relationship_strengths():
    """Get all available relationship strengths"""
    return [e.value for e in schemas.RelationshipStrength]

@router.get("/contribution-levels", response_model=List[str])
def get_contribution_levels():
    """Get all available contribution levels"""
    return [e.value for e in schemas.ContributionLevel] 