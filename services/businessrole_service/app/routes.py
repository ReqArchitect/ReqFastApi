from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from . import services, deps, schemas
from .database import get_db

router = APIRouter()

# Business Role CRUD endpoints
@router.post("/business-roles", response_model=schemas.BusinessRole)
def create_business_role(
    role_in: schemas.BusinessRoleCreate,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    _: str = Depends(deps.rbac_check("business_role:create"))
):
    """Create a new business role"""
    return services.create_business_role(db, role_in, tenant_id, user_id)

@router.get("/business-roles/{role_id}", response_model=schemas.BusinessRole)
def get_business_role(
    role_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get a business role by ID"""
    return services.get_business_role(db, role_id, tenant_id)

@router.get("/business-roles", response_model=schemas.BusinessRoleList)
def get_business_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    organizational_unit: Optional[str] = Query(None),
    role_type: Optional[str] = Query(None),
    strategic_importance: Optional[str] = Query(None),
    authority_level: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    stakeholder_id: Optional[UUID] = Query(None),
    supporting_capability_id: Optional[UUID] = Query(None),
    business_function_id: Optional[UUID] = Query(None),
    business_process_id: Optional[UUID] = Query(None),
    role_classification: Optional[str] = Query(None),
    criticality: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles with filtering and pagination"""
    roles = services.get_business_roles(
        db, tenant_id, skip, limit,
        organizational_unit=organizational_unit,
        role_type=role_type,
        strategic_importance=strategic_importance,
        authority_level=authority_level,
        status=status,
        stakeholder_id=stakeholder_id,
        supporting_capability_id=supporting_capability_id,
        business_function_id=business_function_id,
        business_process_id=business_process_id,
        role_classification=role_classification,
        criticality=criticality
    )
    
    total = len(roles)  # In a real implementation, you'd get total count separately
    
    return schemas.BusinessRoleList(
        business_roles=roles,
        total=total,
        skip=skip,
        limit=limit
    )

@router.put("/business-roles/{role_id}", response_model=schemas.BusinessRole)
def update_business_role(
    role_id: UUID,
    role_in: schemas.BusinessRoleUpdate,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:update"))
):
    """Update a business role"""
    role = services.get_business_role(db, role_id, tenant_id)
    return services.update_business_role(db, role, role_in)

@router.delete("/business-roles/{role_id}")
def delete_business_role(
    role_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:delete"))
):
    """Delete a business role"""
    role = services.get_business_role(db, role_id, tenant_id)
    services.delete_business_role(db, role)
    return {"message": "Business role deleted successfully"}

# Role Link endpoints
@router.post("/business-roles/{role_id}/links", response_model=schemas.RoleLink)
def create_role_link(
    role_id: UUID,
    link_in: schemas.RoleLinkCreate,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    _: str = Depends(deps.rbac_check("role_link:create"))
):
    """Create a link between business role and another element"""
    # Verify the business role exists and belongs to tenant
    services.get_business_role(db, role_id, tenant_id)
    return services.create_role_link(db, link_in, role_id, user_id)

@router.get("/business-roles/{role_id}/links", response_model=List[schemas.RoleLink])
def get_role_links(
    role_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("role_link:read"))
):
    """Get all links for a business role"""
    # Verify the business role exists and belongs to tenant
    services.get_business_role(db, role_id, tenant_id)
    return services.get_role_links(db, role_id, tenant_id)

@router.get("/role-links/{link_id}", response_model=schemas.RoleLink)
def get_role_link(
    link_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("role_link:read"))
):
    """Get a role link by ID"""
    return services.get_role_link(db, link_id, tenant_id)

@router.put("/role-links/{link_id}", response_model=schemas.RoleLink)
def update_role_link(
    link_id: UUID,
    link_in: schemas.RoleLinkUpdate,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("role_link:update"))
):
    """Update a role link"""
    link = services.get_role_link(db, link_id, tenant_id)
    return services.update_role_link(db, link, link_in)

@router.delete("/role-links/{link_id}")
def delete_role_link(
    link_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("role_link:delete"))
):
    """Delete a role link"""
    link = services.get_role_link(db, link_id, tenant_id)
    services.delete_role_link(db, link)
    return {"message": "Role link deleted successfully"}

# Analysis endpoints
@router.get("/business-roles/{role_id}/responsibility-map", response_model=schemas.ResponsibilityMap)
def get_responsibility_map(
    role_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("responsibility:read"))
):
    """Get responsibility map for a business role"""
    return services.get_responsibility_map(db, role_id, tenant_id)

@router.get("/business-roles/{role_id}/alignment-score", response_model=schemas.BusinessRoleAlignment)
def get_alignment_score(
    role_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("alignment:read"))
):
    """Get alignment analysis for a business role"""
    return services.analyze_business_role_alignment(db, role_id, tenant_id)

# Domain query endpoints
@router.get("/business-roles/organizational-unit/{organizational_unit}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_organizational_unit(
    organizational_unit: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by organizational unit"""
    return services.get_business_roles_by_organizational_unit(db, tenant_id, organizational_unit)

@router.get("/business-roles/role-type/{role_type}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_role_type(
    role_type: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by role type"""
    return services.get_business_roles_by_role_type(db, tenant_id, role_type)

@router.get("/business-roles/strategic-importance/{strategic_importance}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_strategic_importance(
    strategic_importance: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by strategic importance"""
    return services.get_business_roles_by_strategic_importance(db, tenant_id, strategic_importance)

@router.get("/business-roles/authority-level/{authority_level}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_authority_level(
    authority_level: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by authority level"""
    return services.get_business_roles_by_authority_level(db, tenant_id, authority_level)

@router.get("/business-roles/status/{status}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_status(
    status: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by status"""
    return services.get_business_roles_by_status(db, tenant_id, status)

@router.get("/business-roles/stakeholder/{stakeholder_id}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_stakeholder(
    stakeholder_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by stakeholder"""
    return services.get_business_roles_by_stakeholder(db, tenant_id, stakeholder_id)

@router.get("/business-roles/capability/{capability_id}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_capability(
    capability_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by capability"""
    return services.get_business_roles_by_capability(db, tenant_id, capability_id)

@router.get("/business-roles/function/{function_id}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_function(
    function_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by business function"""
    return services.get_business_roles_by_function(db, tenant_id, function_id)

@router.get("/business-roles/process/{process_id}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_process(
    process_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by business process"""
    return services.get_business_roles_by_process(db, tenant_id, process_id)

@router.get("/business-roles/element/{element_type}/{element_id}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_element(
    element_type: str,
    element_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles linked to a specific element"""
    return services.get_business_roles_by_element(db, tenant_id, element_type, element_id)

@router.get("/business-roles/active", response_model=List[schemas.BusinessRole])
def get_active_business_roles(
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get active business roles"""
    return services.get_active_business_roles(db, tenant_id)

@router.get("/business-roles/critical", response_model=List[schemas.BusinessRole])
def get_critical_business_roles(
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get critical business roles"""
    return services.get_critical_business_roles(db, tenant_id)

@router.get("/business-roles/classification/{role_classification}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_classification(
    role_classification: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by role classification"""
    return services.get_business_roles_by_classification(db, tenant_id, role_classification)

@router.get("/business-roles/criticality/{criticality}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_criticality(
    criticality: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by criticality"""
    return services.get_business_roles_by_criticality(db, tenant_id, criticality)

@router.get("/business-roles/workload/{workload_level}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_workload(
    workload_level: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by workload level"""
    return services.get_business_roles_by_workload(db, tenant_id, workload_level)

@router.get("/business-roles/availability/{availability_requirement}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_availability(
    availability_requirement: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by availability requirement"""
    return services.get_business_roles_by_availability(db, tenant_id, availability_requirement)

@router.get("/business-roles/risk-level/{risk_level}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_risk_level(
    risk_level: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by risk level"""
    return services.get_business_roles_by_risk_level(db, tenant_id, risk_level)

@router.get("/business-roles/business-value/{business_value}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_business_value(
    business_value: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by business value"""
    return services.get_business_roles_by_business_value(db, tenant_id, business_value)

@router.get("/business-roles/decision-authority/{decision_making_authority}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_decision_authority(
    decision_making_authority: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by decision making authority"""
    return services.get_business_roles_by_decision_authority(db, tenant_id, decision_making_authority)

@router.get("/business-roles/approval-authority/{approval_authority}", response_model=List[schemas.BusinessRole])
def get_business_roles_by_approval_authority(
    approval_authority: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    _: str = Depends(deps.rbac_check("business_role:read"))
):
    """Get business roles by approval authority"""
    return services.get_business_roles_by_approval_authority(db, tenant_id, approval_authority) 