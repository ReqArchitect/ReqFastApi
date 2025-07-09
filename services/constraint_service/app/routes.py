from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from . import schemas, services, deps
from .models import Constraint, ConstraintLink

router = APIRouter(prefix="/constraints", tags=["Constraints"])

# Constraint CRUD endpoints
@router.post("/", response_model=schemas.Constraint, status_code=201)
def create_constraint(
    constraint_in: schemas.ConstraintCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    rbac=Depends(deps.rbac_check("constraint:create"))
):
    """Create a new constraint"""
    return services.create_constraint(db, constraint_in, tenant_id, user_id)

@router.get("/", response_model=List[schemas.Constraint])
def list_constraints(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    constraint_type: Optional[str] = Query(None),
    scope: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    enforcement_level: Optional[str] = Query(None),
    stakeholder_id: Optional[UUID] = Query(None),
    business_actor_id: Optional[UUID] = Query(None),
    compliance_required: Optional[bool] = Query(None),
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint:read"))
):
    """List constraints with filtering and pagination"""
    return services.get_constraints(
        db, tenant_id, skip, limit, constraint_type, scope, severity, 
        enforcement_level, stakeholder_id, business_actor_id, compliance_required
    )

@router.get("/{constraint_id}", response_model=schemas.Constraint)
def get_constraint(
    constraint_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint:read"))
):
    """Get a constraint by ID"""
    return services.get_constraint(db, constraint_id, tenant_id)

@router.put("/{constraint_id}", response_model=schemas.Constraint)
def update_constraint(
    constraint_id: UUID,
    constraint_in: schemas.ConstraintUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint:update"))
):
    """Update a constraint"""
    constraint = services.get_constraint(db, constraint_id, tenant_id)
    return services.update_constraint(db, constraint, constraint_in)

@router.delete("/{constraint_id}", status_code=204)
def delete_constraint(
    constraint_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint:delete"))
):
    """Delete a constraint"""
    constraint = services.get_constraint(db, constraint_id, tenant_id)
    services.delete_constraint(db, constraint)
    return {"ok": True}

# Constraint Link endpoints
@router.post("/{constraint_id}/links", response_model=schemas.ConstraintLink, status_code=201)
def create_constraint_link(
    constraint_id: UUID,
    link_in: schemas.ConstraintLinkCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    rbac=Depends(deps.rbac_check("constraint_link:create"))
):
    """Create a link between constraint and another element"""
    # Verify constraint exists and belongs to tenant
    services.get_constraint(db, constraint_id, tenant_id)
    return services.create_constraint_link(db, link_in, constraint_id, user_id)

@router.get("/{constraint_id}/links", response_model=List[schemas.ConstraintLink])
def list_constraint_links(
    constraint_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint_link:read"))
):
    """List all links for a constraint"""
    # Verify constraint exists and belongs to tenant
    services.get_constraint(db, constraint_id, tenant_id)
    return services.get_constraint_links(db, constraint_id, tenant_id)

@router.get("/links/{link_id}", response_model=schemas.ConstraintLink)
def get_constraint_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint_link:read"))
):
    """Get a constraint link by ID"""
    return services.get_constraint_link(db, link_id, tenant_id)

@router.put("/links/{link_id}", response_model=schemas.ConstraintLink)
def update_constraint_link(
    link_id: UUID,
    link_in: schemas.ConstraintLinkUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint_link:update"))
):
    """Update a constraint link"""
    link = services.get_constraint_link(db, link_id, tenant_id)
    return services.update_constraint_link(db, link, link_in)

@router.delete("/links/{link_id}", status_code=204)
def delete_constraint_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint_link:delete"))
):
    """Delete a constraint link"""
    link = services.get_constraint_link(db, link_id, tenant_id)
    services.delete_constraint_link(db, link)
    return {"ok": True}

# Analysis and impact mapping endpoints
@router.get("/{constraint_id}/impact-map", response_model=schemas.ImpactMap)
def get_impact_map(
    constraint_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("impact:read"))
):
    """Get impact map for a constraint"""
    return services.get_impact_map(db, constraint_id, tenant_id)

@router.get("/{constraint_id}/analysis", response_model=schemas.ConstraintAnalysis)
def analyze_constraint(
    constraint_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("analysis:read"))
):
    """Analyze a constraint for strategic insights"""
    return services.analyze_constraint(db, constraint_id, tenant_id)

# Domain-specific query endpoints
@router.get("/by-type/{constraint_type}", response_model=List[schemas.Constraint])
def get_constraints_by_type(
    constraint_type: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint:read"))
):
    """Get constraints filtered by type"""
    return services.get_constraints_by_type(db, tenant_id, constraint_type)

@router.get("/by-scope/{scope}", response_model=List[schemas.Constraint])
def get_constraints_by_scope(
    scope: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint:read"))
):
    """Get constraints filtered by scope"""
    return services.get_constraints_by_scope(db, tenant_id, scope)

@router.get("/by-severity/{severity}", response_model=List[schemas.Constraint])
def get_constraints_by_severity(
    severity: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint:read"))
):
    """Get constraints filtered by severity"""
    return services.get_constraints_by_severity(db, tenant_id, severity)

@router.get("/by-stakeholder/{stakeholder_id}", response_model=List[schemas.Constraint])
def get_constraints_by_stakeholder(
    stakeholder_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint:read"))
):
    """Get constraints associated with a specific stakeholder"""
    return services.get_constraints_by_stakeholder(db, tenant_id, stakeholder_id)

@router.get("/by-business-actor/{business_actor_id}", response_model=List[schemas.Constraint])
def get_constraints_by_business_actor(
    business_actor_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint:read"))
):
    """Get constraints associated with a specific business actor"""
    return services.get_constraints_by_business_actor(db, tenant_id, business_actor_id)

@router.get("/by-element/{element_type}/{element_id}", response_model=List[schemas.Constraint])
def get_constraints_by_element(
    element_type: str,
    element_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint:read"))
):
    """Get constraints that affect a specific element"""
    return services.get_constraints_by_element(db, tenant_id, element_type, element_id)

@router.get("/compliance/required", response_model=List[schemas.Constraint])
def get_compliance_constraints(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint:read"))
):
    """Get constraints that require compliance"""
    return services.get_compliance_constraints(db, tenant_id)

@router.get("/expiring/{days_ahead}", response_model=List[schemas.Constraint])
def get_expiring_constraints(
    days_ahead: int = Query(30, ge=1, le=365),
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("constraint:read"))
):
    """Get constraints that are expiring soon"""
    return services.get_expiring_constraints(db, tenant_id, days_ahead)

# Utility endpoints
@router.get("/types", response_model=List[str])
def get_constraint_types():
    """Get all available constraint types"""
    return [e.value for e in schemas.ConstraintType]

@router.get("/scopes", response_model=List[str])
def get_scopes():
    """Get all available scopes"""
    return [e.value for e in schemas.Scope]

@router.get("/severities", response_model=List[str])
def get_severities():
    """Get all available severities"""
    return [e.value for e in schemas.Severity]

@router.get("/enforcement-levels", response_model=List[str])
def get_enforcement_levels():
    """Get all available enforcement levels"""
    return [e.value for e in schemas.EnforcementLevel]

@router.get("/risk-profiles", response_model=List[str])
def get_risk_profiles():
    """Get all available risk profiles"""
    return [e.value for e in schemas.RiskProfile]

@router.get("/mitigation-statuses", response_model=List[str])
def get_mitigation_statuses():
    """Get all available mitigation statuses"""
    return [e.value for e in schemas.MitigationStatus]

@router.get("/mitigation-efforts", response_model=List[str])
def get_mitigation_efforts():
    """Get all available mitigation efforts"""
    return [e.value for e in schemas.MitigationEffort]

@router.get("/impact-levels", response_model=List[str])
def get_impact_levels():
    """Get all available impact levels"""
    return [e.value for e in schemas.ImpactLevel]

@router.get("/review-frequencies", response_model=List[str])
def get_review_frequencies():
    """Get all available review frequencies"""
    return [e.value for e in schemas.ReviewFrequency]

@router.get("/link-types", response_model=List[str])
def get_link_types():
    """Get all available link types"""
    return [e.value for e in schemas.LinkType]

@router.get("/compliance-statuses", response_model=List[str])
def get_compliance_statuses():
    """Get all available compliance statuses"""
    return [e.value for e in schemas.ComplianceStatus] 