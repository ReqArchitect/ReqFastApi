from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from . import schemas, services, deps
from .models import BusinessFunction, FunctionLink

router = APIRouter(prefix="/business-functions", tags=["Business Functions"])

# Business Function CRUD endpoints
@router.post("/", response_model=schemas.BusinessFunction, status_code=201)
def create_business_function(
    function_in: schemas.BusinessFunctionCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    rbac=Depends(deps.rbac_check("business_function:create"))
):
    """Create a new business function"""
    return services.create_business_function(db, function_in, tenant_id, user_id)

@router.get("/", response_model=List[schemas.BusinessFunction])
def list_business_functions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    competency_area: Optional[str] = Query(None),
    organizational_unit: Optional[str] = Query(None),
    criticality: Optional[str] = Query(None),
    frequency: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    owner_role_id: Optional[UUID] = Query(None),
    parent_function_id: Optional[UUID] = Query(None),
    supporting_capability_id: Optional[UUID] = Query(None),
    business_process_id: Optional[UUID] = Query(None),
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """List business functions with filtering and pagination"""
    return services.get_business_functions(
        db, tenant_id, skip, limit, competency_area, organizational_unit, 
        criticality, frequency, status, owner_role_id, parent_function_id, 
        supporting_capability_id, business_process_id
    )

@router.get("/{function_id}", response_model=schemas.BusinessFunction)
def get_business_function(
    function_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get a business function by ID"""
    return services.get_business_function(db, function_id, tenant_id)

@router.put("/{function_id}", response_model=schemas.BusinessFunction)
def update_business_function(
    function_id: UUID,
    function_in: schemas.BusinessFunctionUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:update"))
):
    """Update a business function"""
    function = services.get_business_function(db, function_id, tenant_id)
    return services.update_business_function(db, function, function_in)

@router.delete("/{function_id}", status_code=204)
def delete_business_function(
    function_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:delete"))
):
    """Delete a business function"""
    function = services.get_business_function(db, function_id, tenant_id)
    services.delete_business_function(db, function)
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
    """Create a link between business function and another element"""
    # Verify function exists and belongs to tenant
    services.get_business_function(db, function_id, tenant_id)
    return services.create_function_link(db, link_in, function_id, user_id)

@router.get("/{function_id}/links", response_model=List[schemas.FunctionLink])
def list_function_links(
    function_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("function_link:read"))
):
    """List all links for a business function"""
    # Verify function exists and belongs to tenant
    services.get_business_function(db, function_id, tenant_id)
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
    """Get impact map for a business function"""
    return services.get_impact_map(db, function_id, tenant_id)

@router.get("/{function_id}/analysis", response_model=schemas.BusinessFunctionAnalysis)
def analyze_business_function(
    function_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("analysis:read"))
):
    """Analyze a business function for operational insights"""
    return services.analyze_business_function(db, function_id, tenant_id)

# Domain-specific query endpoints
@router.get("/by-competency-area/{competency_area}", response_model=List[schemas.BusinessFunction])
def get_business_functions_by_competency_area(
    competency_area: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions filtered by competency area"""
    return services.get_business_functions_by_competency_area(db, tenant_id, competency_area)

@router.get("/by-organizational-unit/{organizational_unit}", response_model=List[schemas.BusinessFunction])
def get_business_functions_by_organizational_unit(
    organizational_unit: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions filtered by organizational unit"""
    return services.get_business_functions_by_organizational_unit(db, tenant_id, organizational_unit)

@router.get("/by-criticality/{criticality}", response_model=List[schemas.BusinessFunction])
def get_business_functions_by_criticality(
    criticality: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions filtered by criticality"""
    return services.get_business_functions_by_criticality(db, tenant_id, criticality)

@router.get("/by-frequency/{frequency}", response_model=List[schemas.BusinessFunction])
def get_business_functions_by_frequency(
    frequency: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions filtered by frequency"""
    return services.get_business_functions_by_frequency(db, tenant_id, frequency)

@router.get("/by-status/{status}", response_model=List[schemas.BusinessFunction])
def get_business_functions_by_status(
    status: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions filtered by status"""
    return services.get_business_functions_by_status(db, tenant_id, status)

@router.get("/by-role/{role_id}", response_model=List[schemas.BusinessFunctionByRole])
def get_business_functions_by_role(
    role_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions associated with a specific role"""
    functions = services.get_business_functions_by_role(db, tenant_id, role_id)
    return [
        schemas.BusinessFunctionByRole(
            business_function_id=f.id,
            name=f.name,
            competency_area=f.competency_area,
            organizational_unit=f.organizational_unit,
            criticality=f.criticality,
            status=f.status,
            alignment_score=f.alignment_score,
            last_updated=f.updated_at
        ) for f in functions
    ]

@router.get("/by-process/{process_id}", response_model=List[schemas.BusinessFunctionByProcess])
def get_business_functions_by_process(
    process_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions associated with a specific process"""
    functions = services.get_business_functions_by_process(db, tenant_id, process_id)
    return [
        schemas.BusinessFunctionByProcess(
            business_function_id=f.id,
            name=f.name,
            competency_area=f.competency_area,
            organizational_unit=f.organizational_unit,
            frequency=f.frequency,
            complexity=f.complexity,
            maturity_level=f.maturity_level,
            last_updated=f.updated_at
        ) for f in functions
    ]

@router.get("/by-capability/{capability_id}", response_model=List[schemas.BusinessFunction])
def get_business_functions_by_capability(
    capability_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions associated with a specific capability"""
    return services.get_business_functions_by_capability(db, tenant_id, capability_id)

@router.get("/by-element/{element_type}/{element_id}", response_model=List[schemas.BusinessFunction])
def get_business_functions_by_element(
    element_type: str,
    element_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions that are linked to a specific element"""
    return services.get_business_functions_by_element(db, tenant_id, element_type, element_id)

@router.get("/active", response_model=List[schemas.BusinessFunction])
def get_active_business_functions(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get active business functions"""
    return services.get_active_business_functions(db, tenant_id)

@router.get("/critical", response_model=List[schemas.BusinessFunction])
def get_critical_business_functions(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get critical business functions"""
    return services.get_critical_business_functions(db, tenant_id)

@router.get("/by-complexity/{complexity}", response_model=List[schemas.BusinessFunction])
def get_business_functions_by_complexity(
    complexity: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions filtered by complexity"""
    return services.get_business_functions_by_complexity(db, tenant_id, complexity)

@router.get("/by-maturity/{maturity_level}", response_model=List[schemas.BusinessFunction])
def get_business_functions_by_maturity(
    maturity_level: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions filtered by maturity level"""
    return services.get_business_functions_by_maturity(db, tenant_id, maturity_level)

@router.get("/by-operational-hours/{operational_hours}", response_model=List[schemas.BusinessFunction])
def get_business_functions_by_operational_hours(
    operational_hours: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions filtered by operational hours"""
    return services.get_business_functions_by_operational_hours(db, tenant_id, operational_hours)

@router.get("/by-strategic-importance/{strategic_importance}", response_model=List[schemas.BusinessFunction])
def get_business_functions_by_strategic_importance(
    strategic_importance: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions filtered by strategic importance"""
    return services.get_business_functions_by_strategic_importance(db, tenant_id, strategic_importance)

@router.get("/by-business-value/{business_value}", response_model=List[schemas.BusinessFunction])
def get_business_functions_by_business_value(
    business_value: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions filtered by business value"""
    return services.get_business_functions_by_business_value(db, tenant_id, business_value)

@router.get("/by-risk-level/{risk_level}", response_model=List[schemas.BusinessFunction])
def get_business_functions_by_risk_level(
    risk_level: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    rbac=Depends(deps.rbac_check("business_function:read"))
):
    """Get business functions filtered by risk level"""
    return services.get_business_functions_by_risk_level(db, tenant_id, risk_level)

# Utility endpoints
@router.get("/competency-areas", response_model=List[str])
def get_competency_areas():
    """Get all available competency areas"""
    return [e.value for e in schemas.CompetencyArea]

@router.get("/frequencies", response_model=List[str])
def get_frequencies():
    """Get all available frequencies"""
    return [e.value for e in schemas.Frequency]

@router.get("/criticalities", response_model=List[str])
def get_criticalities():
    """Get all available criticalities"""
    return [e.value for e in schemas.Criticality]

@router.get("/complexities", response_model=List[str])
def get_complexities():
    """Get all available complexities"""
    return [e.value for e in schemas.Complexity]

@router.get("/maturity-levels", response_model=List[str])
def get_maturity_levels():
    """Get all available maturity levels"""
    return [e.value for e in schemas.MaturityLevel]

@router.get("/risk-levels", response_model=List[str])
def get_risk_levels():
    """Get all available risk levels"""
    return [e.value for e in schemas.RiskLevel]

@router.get("/audit-frequencies", response_model=List[str])
def get_audit_frequencies():
    """Get all available audit frequencies"""
    return [e.value for e in schemas.AuditFrequency]

@router.get("/audit-statuses", response_model=List[str])
def get_audit_statuses():
    """Get all available audit statuses"""
    return [e.value for e in schemas.AuditStatus]

@router.get("/function-statuses", response_model=List[str])
def get_function_statuses():
    """Get all available function statuses"""
    return [e.value for e in schemas.FunctionStatus]

@router.get("/operational-hours", response_model=List[str])
def get_operational_hours():
    """Get all available operational hours"""
    return [e.value for e in schemas.OperationalHours]

@router.get("/strategic-importances", response_model=List[str])
def get_strategic_importances():
    """Get all available strategic importances"""
    return [e.value for e in schemas.StrategicImportance]

@router.get("/business-values", response_model=List[str])
def get_business_values():
    """Get all available business values"""
    return [e.value for e in schemas.BusinessValue]

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