from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from . import schemas, services, deps
from .models import Driver, DriverLink

router = APIRouter(prefix="/drivers", tags=["Drivers"])

# Driver CRUD endpoints
@router.post("/", response_model=schemas.Driver, status_code=201)
def create_driver(
    driver_in: schemas.DriverCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    rbac=Depends(deps.rbac_check("driver:create"))
):
    """Create a new driver"""
    return services.create_driver(db, driver_in, tenant_id, user_id)

@router.get("/", response_model=List[schemas.Driver])
def list_drivers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    driver_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    urgency: Optional[str] = Query(None),
    impact_level: Optional[str] = Query(None),
    stakeholder_id: Optional[UUID] = Query(None),
    business_actor_id: Optional[UUID] = Query(None),
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver:read"))
):
    """List drivers with filtering and pagination"""
    return services.get_drivers(
        db, tenant_id, skip, limit, driver_type, category, urgency, 
        impact_level, stakeholder_id, business_actor_id
    )

@router.get("/{driver_id}", response_model=schemas.Driver)
def get_driver(
    driver_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver:read"))
):
    """Get a driver by ID"""
    return services.get_driver(db, driver_id, tenant_id)

@router.put("/{driver_id}", response_model=schemas.Driver)
def update_driver(
    driver_id: UUID,
    driver_in: schemas.DriverUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver:update"))
):
    """Update a driver"""
    driver = services.get_driver(db, driver_id, tenant_id)
    return services.update_driver(db, driver, driver_in)

@router.delete("/{driver_id}", status_code=204)
def delete_driver(
    driver_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver:delete"))
):
    """Delete a driver"""
    driver = services.get_driver(db, driver_id, tenant_id)
    services.delete_driver(db, driver)
    return {"ok": True}

# Driver Link endpoints
@router.post("/{driver_id}/links", response_model=schemas.DriverLink, status_code=201)
def create_driver_link(
    driver_id: UUID,
    link_in: schemas.DriverLinkCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    rbac=Depends(deps.rbac_check("driver_link:create"))
):
    """Create a link between driver and another element"""
    # Verify driver exists and belongs to tenant
    services.get_driver(db, driver_id, tenant_id)
    return services.create_driver_link(db, link_in, driver_id, user_id)

@router.get("/{driver_id}/links", response_model=List[schemas.DriverLink])
def list_driver_links(
    driver_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver_link:read"))
):
    """List all links for a driver"""
    # Verify driver exists and belongs to tenant
    services.get_driver(db, driver_id, tenant_id)
    return services.get_driver_links(db, driver_id, tenant_id)

@router.get("/links/{link_id}", response_model=schemas.DriverLink)
def get_driver_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver_link:read"))
):
    """Get a driver link by ID"""
    return services.get_driver_link(db, link_id, tenant_id)

@router.put("/links/{link_id}", response_model=schemas.DriverLink)
def update_driver_link(
    link_id: UUID,
    link_in: schemas.DriverLinkUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver_link:update"))
):
    """Update a driver link"""
    link = services.get_driver_link(db, link_id, tenant_id)
    return services.update_driver_link(db, link, link_in)

@router.delete("/links/{link_id}", status_code=204)
def delete_driver_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver_link:delete"))
):
    """Delete a driver link"""
    link = services.get_driver_link(db, link_id, tenant_id)
    services.delete_driver_link(db, link)
    return {"ok": True}

# Analysis and influence mapping endpoints
@router.get("/{driver_id}/influence-map", response_model=schemas.InfluenceMap)
def get_influence_map(
    driver_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("influence:read"))
):
    """Get influence map for a driver"""
    return services.get_influence_map(db, driver_id, tenant_id)

@router.get("/{driver_id}/analysis", response_model=schemas.DriverAnalysis)
def analyze_driver(
    driver_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("analysis:read"))
):
    """Analyze a driver for strategic insights"""
    return services.analyze_driver(db, driver_id, tenant_id)

# Domain-specific query endpoints
@router.get("/by-urgency/{urgency}", response_model=List[schemas.Driver])
def get_drivers_by_urgency(
    urgency: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver:read"))
):
    """Get drivers filtered by urgency"""
    return services.get_drivers_by_urgency(db, tenant_id, urgency)

@router.get("/by-category/{category}", response_model=List[schemas.Driver])
def get_drivers_by_category(
    category: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver:read"))
):
    """Get drivers filtered by category"""
    return services.get_drivers_by_category(db, tenant_id, category)

@router.get("/by-stakeholder/{stakeholder_id}", response_model=List[schemas.Driver])
def get_drivers_by_stakeholder(
    stakeholder_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver:read"))
):
    """Get drivers associated with a specific stakeholder"""
    return services.get_drivers_by_stakeholder(db, tenant_id, stakeholder_id)

@router.get("/by-business-actor/{business_actor_id}", response_model=List[schemas.Driver])
def get_drivers_by_business_actor(
    business_actor_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver:read"))
):
    """Get drivers associated with a specific business actor"""
    return services.get_drivers_by_business_actor(db, tenant_id, business_actor_id)

@router.get("/by-goal/{goal_id}", response_model=List[schemas.Driver])
def get_drivers_by_associated_goal(
    goal_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver:read"))
):
    """Get drivers that influence a specific goal"""
    return services.get_drivers_by_associated_goals(db, tenant_id, goal_id)

@router.get("/by-requirement/{requirement_id}", response_model=List[schemas.Driver])
def get_drivers_by_associated_requirement(
    requirement_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("driver:read"))
):
    """Get drivers that influence a specific requirement"""
    return services.get_drivers_by_associated_requirements(db, tenant_id, requirement_id)

# Utility endpoints
@router.get("/types", response_model=List[str])
def get_driver_types():
    """Get all available driver types"""
    return [e.value for e in schemas.DriverType]

@router.get("/categories", response_model=List[str])
def get_categories():
    """Get all available categories"""
    return [e.value for e in schemas.Category]

@router.get("/urgencies", response_model=List[str])
def get_urgencies():
    """Get all available urgencies"""
    return [e.value for e in schemas.Urgency]

@router.get("/impact-levels", response_model=List[str])
def get_impact_levels():
    """Get all available impact levels"""
    return [e.value for e in schemas.ImpactLevel]

@router.get("/time-horizons", response_model=List[str])
def get_time_horizons():
    """Get all available time horizons"""
    return [e.value for e in schemas.TimeHorizon]

@router.get("/geographic-scopes", response_model=List[str])
def get_geographic_scopes():
    """Get all available geographic scopes"""
    return [e.value for e in schemas.GeographicScope]

@router.get("/risk-levels", response_model=List[str])
def get_risk_levels():
    """Get all available risk levels"""
    return [e.value for e in schemas.RiskLevel]

@router.get("/link-types", response_model=List[str])
def get_link_types():
    """Get all available link types"""
    return [e.value for e in schemas.LinkType]

@router.get("/link-strengths", response_model=List[str])
def get_link_strengths():
    """Get all available link strengths"""
    return [e.value for e in schemas.LinkStrength]

@router.get("/influence-directions", response_model=List[str])
def get_influence_directions():
    """Get all available influence directions"""
    return [e.value for e in schemas.InfluenceDirection] 