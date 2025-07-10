from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from . import schemas, services, deps
from .models import ApplicationFunction, FunctionLink

router = APIRouter(prefix="/application-functions", tags=["Application Functions"])

# Application Function CRUD endpoints
@router.post("/", response_model=schemas.ApplicationFunction, status_code=201)
def create_application_function(
    function_in: schemas.ApplicationFunctionCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    rbac=Depends(deps.rbac_check("application_function:create"))
):
    """Create a new application function"""
    return services.create_application_function(db, function_in, tenant_id, user_id)

@router.get("/", response_model=List[schemas.ApplicationFunction])
def list_application_functions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    function_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    business_criticality: Optional[str] = Query(None),
    business_value: Optional[str] = Query(None),
    supported_business_function_id: Optional[UUID] = Query(None),
    technology_stack: Optional[str] = Query(None),
    performance_threshold: Optional[float] = Query(None),
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("application_function:read"))
):
    """List application functions with filtering and pagination"""
    return services.get_application_functions(
        db, tenant_id, skip, limit, function_type, status, 
        business_criticality, business_value, supported_business_function_id,
        technology_stack, performance_threshold
    )

@router.get("/{function_id}", response_model=schemas.ApplicationFunction)
def get_application_function(
    function_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("application_function:read"))
):
    """Get an application function by ID"""
    return services.get_application_function(db, function_id, tenant_id)

@router.put("/{function_id}", response_model=schemas.ApplicationFunction)
def update_application_function(
    function_id: UUID,
    function_in: schemas.ApplicationFunctionUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("application_function:update"))
):
    """Update an application function"""
    function = services.get_application_function(db, function_id, tenant_id)
    return services.update_application_function(db, function, function_in)

@router.delete("/{function_id}", status_code=204)
def delete_application_function(
    function_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("application_function:delete"))
):
    """Delete an application function"""
    function = services.get_application_function(db, function_id, tenant_id)
    services.delete_application_function(db, function)
    return {"ok": True}

# Function Link endpoints
@router.post("/{function_id}/links", response_model=schemas.FunctionLink, status_code=201)
def create_function_link(
    function_id: UUID,
    link_in: schemas.FunctionLinkCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    rbac=Depends(deps.rbac_check("function_link:create"))
):
    """Create a link between application function and another element"""
    # Verify function exists and belongs to tenant
    services.get_application_function(db, function_id, tenant_id)
    return services.create_function_link(db, link_in, function_id, user_id)

@router.get("/{function_id}/links", response_model=List[schemas.FunctionLink])
def list_function_links(
    function_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("function_link:read"))
):
    """List all links for an application function"""
    # Verify function exists and belongs to tenant
    services.get_application_function(db, function_id, tenant_id)
    return services.get_function_links(db, function_id, tenant_id)

@router.get("/links/{link_id}", response_model=schemas.FunctionLink)
def get_function_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("function_link:read"))
):
    """Get a function link by ID"""
    return services.get_function_link(db, link_id, tenant_id)

@router.put("/links/{link_id}", response_model=schemas.FunctionLink)
def update_function_link(
    link_id: UUID,
    link_in: schemas.FunctionLinkUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("function_link:update"))
):
    """Update a function link"""
    link = services.get_function_link(db, link_id, tenant_id)
    return services.update_function_link(db, link, link_in)

@router.delete("/links/{link_id}", status_code=204)
def delete_function_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("function_link:delete"))
):
    """Delete a function link"""
    link = services.get_function_link(db, link_id, tenant_id)
    services.delete_function_link(db, link)
    return {"ok": True}

# Analysis and impact mapping endpoints
@router.get("/{function_id}/impact-map", response_model=schemas.ImpactMap)
def get_impact_map(
    function_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("impact:read"))
):
    """Get impact map for an application function"""
    return services.get_impact_map(db, function_id, tenant_id)

@router.get("/{function_id}/performance-score", response_model=schemas.PerformanceScore)
def get_performance_score(
    function_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("performance:read"))
):
    """Get performance score for an application function"""
    return services.get_performance_score(db, function_id, tenant_id)

@router.get("/{function_id}/analysis", response_model=schemas.ApplicationFunctionAnalysis)
def analyze_application_function(
    function_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("analysis:read"))
):
    """Analyze an application function for operational insights"""
    return services.analyze_application_function(db, function_id, tenant_id)

# Domain-specific query endpoints
@router.get("/by-type/{function_type}", response_model=List[schemas.ApplicationFunction])
def get_application_functions_by_type(
    function_type: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("application_function:read"))
):
    """Get application functions filtered by type"""
    return services.get_application_functions_by_type(db, tenant_id, function_type)

@router.get("/by-status/{status}", response_model=List[schemas.ApplicationFunction])
def get_application_functions_by_status(
    status: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("application_function:read"))
):
    """Get application functions filtered by status"""
    return services.get_application_functions_by_status(db, tenant_id, status)

@router.get("/by-business-function/{business_function_id}", response_model=List[schemas.ApplicationFunction])
def get_application_functions_by_business_function(
    business_function_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("application_function:read"))
):
    """Get application functions filtered by business function"""
    return services.get_application_functions_by_business_function(db, tenant_id, business_function_id)

@router.get("/by-performance/{performance_threshold}", response_model=List[schemas.ApplicationFunction])
def get_application_functions_by_performance(
    performance_threshold: float,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("application_function:read"))
):
    """Get application functions filtered by performance threshold"""
    return services.get_application_functions_by_performance(db, tenant_id, performance_threshold)

@router.get("/by-element/{element_type}/{element_id}", response_model=List[schemas.ApplicationFunction])
def get_application_functions_by_element(
    element_type: str,
    element_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("application_function:read"))
):
    """Get application functions filtered by linked element"""
    return services.get_application_functions_by_element(db, tenant_id, element_type, element_id)

@router.get("/active", response_model=List[schemas.ApplicationFunction])
def get_active_application_functions(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("application_function:read"))
):
    """Get active application functions"""
    return services.get_active_application_functions(db, tenant_id)

@router.get("/critical", response_model=List[schemas.ApplicationFunction])
def get_critical_application_functions(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("application_function:read"))
):
    """Get critical application functions"""
    return services.get_critical_application_functions(db, tenant_id)

# Enumeration endpoints for frontend dropdowns
@router.get("/function-types", response_model=List[str])
def get_function_types():
    """Get all available function types"""
    return [e.value for e in schemas.FunctionType]

@router.get("/statuses", response_model=List[str])
def get_statuses():
    """Get all available statuses"""
    return [e.value for e in schemas.FunctionStatus]

@router.get("/business-criticalities", response_model=List[str])
def get_business_criticalities():
    """Get all available business criticalities"""
    return [e.value for e in schemas.BusinessCriticality]

@router.get("/business-values", response_model=List[str])
def get_business_values():
    """Get all available business values"""
    return [e.value for e in schemas.BusinessValue]

@router.get("/operational-hours", response_model=List[str])
def get_operational_hours():
    """Get all available operational hours"""
    return [e.value for e in schemas.OperationalHours]

@router.get("/security-levels", response_model=List[str])
def get_security_levels():
    """Get all available security levels"""
    return [e.value for e in schemas.SecurityLevel]

@router.get("/link-types", response_model=List[str])
def get_link_types():
    """Get all available link types"""
    return [e.value for e in schemas.LinkType]

@router.get("/relationship-strengths", response_model=List[str])
def get_relationship_strengths():
    """Get all available relationship strengths"""
    return [e.value for e in schemas.RelationshipStrength]

@router.get("/dependency-levels", response_model=List[str])
def get_dependency_levels():
    """Get all available dependency levels"""
    return [e.value for e in schemas.DependencyLevel]

@router.get("/interaction-frequencies", response_model=List[str])
def get_interaction_frequencies():
    """Get all available interaction frequencies"""
    return [e.value for e in schemas.InteractionFrequency]

@router.get("/interaction-types", response_model=List[str])
def get_interaction_types():
    """Get all available interaction types"""
    return [e.value for e in schemas.InteractionType]

@router.get("/data-flow-directions", response_model=List[str])
def get_data_flow_directions():
    """Get all available data flow directions"""
    return [e.value for e in schemas.DataFlowDirection]

@router.get("/performance-impacts", response_model=List[str])
def get_performance_impacts():
    """Get all available performance impacts"""
    return [e.value for e in schemas.PerformanceImpact] 