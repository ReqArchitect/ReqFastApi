from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from . import schemas, services, deps
from .models import Requirement, RequirementLink

router = APIRouter(prefix="/requirements", tags=["Requirements"])

# Requirement CRUD endpoints
@router.post("/", response_model=schemas.Requirement, status_code=201)
def create_requirement(
    requirement_in: schemas.RequirementCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    rbac=Depends(deps.rbac_check("requirement:create"))
):
    """Create a new requirement"""
    return services.create_requirement(db, requirement_in, tenant_id, user_id)

@router.get("/", response_model=List[schemas.Requirement])
def list_requirements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    requirement_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("requirement:read"))
):
    """List requirements with filtering and pagination"""
    return services.get_requirements(
        db, tenant_id, skip, limit, requirement_type, status, priority
    )

@router.get("/{requirement_id}", response_model=schemas.Requirement)
def get_requirement(
    requirement_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("requirement:read"))
):
    """Get a requirement by ID"""
    return services.get_requirement(db, requirement_id, tenant_id)

@router.put("/{requirement_id}", response_model=schemas.Requirement)
def update_requirement(
    requirement_id: UUID,
    requirement_in: schemas.RequirementUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("requirement:update"))
):
    """Update a requirement"""
    requirement = services.get_requirement(db, requirement_id, tenant_id)
    return services.update_requirement(db, requirement, requirement_in)

@router.delete("/{requirement_id}", status_code=204)
def delete_requirement(
    requirement_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("requirement:delete"))
):
    """Delete a requirement"""
    requirement = services.get_requirement(db, requirement_id, tenant_id)
    services.delete_requirement(db, requirement)
    return {"ok": True}

# Requirement Link endpoints
@router.post("/{requirement_id}/links", response_model=schemas.RequirementLink, status_code=201)
def create_requirement_link(
    requirement_id: UUID,
    link_in: schemas.RequirementLinkCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    rbac=Depends(deps.rbac_check("requirement_link:create"))
):
    """Create a link between requirement and another element"""
    # Verify requirement exists and belongs to tenant
    services.get_requirement(db, requirement_id, tenant_id)
    return services.create_requirement_link(db, link_in, requirement_id, user_id)

@router.get("/{requirement_id}/links", response_model=List[schemas.RequirementLink])
def list_requirement_links(
    requirement_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("requirement_link:read"))
):
    """List all links for a requirement"""
    # Verify requirement exists and belongs to tenant
    services.get_requirement(db, requirement_id, tenant_id)
    return services.get_requirement_links(db, requirement_id, tenant_id)

@router.get("/links/{link_id}", response_model=schemas.RequirementLink)
def get_requirement_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("requirement_link:read"))
):
    """Get a requirement link by ID"""
    return services.get_requirement_link(db, link_id, tenant_id)

@router.put("/links/{link_id}", response_model=schemas.RequirementLink)
def update_requirement_link(
    link_id: UUID,
    link_in: schemas.RequirementLinkUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("requirement_link:update"))
):
    """Update a requirement link"""
    link = services.get_requirement_link(db, link_id, tenant_id)
    return services.update_requirement_link(db, link, link_in)

@router.delete("/links/{link_id}", status_code=204)
def delete_requirement_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("requirement_link:delete"))
):
    """Delete a requirement link"""
    link = services.get_requirement_link(db, link_id, tenant_id)
    services.delete_requirement_link(db, link)
    return {"ok": True}

# Traceability and impact analysis endpoints
@router.get("/{requirement_id}/traceability-check", response_model=schemas.TraceabilityCheck)
def check_traceability(
    requirement_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("traceability:read"))
):
    """Check traceability status for a requirement"""
    return services.check_traceability(db, requirement_id, tenant_id)

@router.get("/{requirement_id}/impact-summary", response_model=schemas.ImpactSummary)
def get_impact_summary(
    requirement_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("impact:read"))
):
    """Get impact summary for a requirement"""
    return services.get_impact_summary(db, requirement_id, tenant_id)

# Additional utility endpoints
@router.get("/types", response_model=List[str])
def get_requirement_types():
    """Get all available requirement types"""
    return [e.value for e in schemas.RequirementType]

@router.get("/priorities", response_model=List[str])
def get_priorities():
    """Get all available priorities"""
    return [e.value for e in schemas.Priority]

@router.get("/statuses", response_model=List[str])
def get_statuses():
    """Get all available statuses"""
    return [e.value for e in schemas.Status]

@router.get("/link-types", response_model=List[str])
def get_link_types():
    """Get all available link types"""
    return [e.value for e in schemas.LinkType]

@router.get("/link-strengths", response_model=List[str])
def get_link_strengths():
    """Get all available link strengths"""
    return [e.value for e in schemas.LinkStrength] 