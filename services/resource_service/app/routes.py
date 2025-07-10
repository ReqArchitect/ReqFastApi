from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from . import models, schemas, services, deps

router = APIRouter()

# Resource CRUD endpoints
@router.post("/resources", response_model=schemas.Resource, status_code=status.HTTP_201_CREATED)
def create_resource(
    resource_in: schemas.ResourceCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    role: str = Depends(deps.rbac_check("resource:create"))
):
    """Create a new resource"""
    return services.create_resource(db, resource_in, tenant_id, user_id)

@router.get("/resources", response_model=List[schemas.Resource])
def list_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    resource_type: Optional[str] = None,
    deployment_status: Optional[str] = None,
    criticality: Optional[str] = None,
    strategic_importance: Optional[str] = None,
    associated_capability_id: Optional[UUID] = None,
    availability_threshold: Optional[float] = None,
    utilization_threshold: Optional[float] = None,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource:read"))
):
    """List resources with filtering"""
    return services.get_resources(
        db, tenant_id, skip, limit, resource_type, deployment_status,
        criticality, strategic_importance, associated_capability_id,
        availability_threshold, utilization_threshold
    )

@router.get("/resources/{resource_id}", response_model=schemas.Resource)
def get_resource(
    resource_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource:read"))
):
    """Get resource by ID"""
    return services.get_resource(db, resource_id, tenant_id)

@router.put("/resources/{resource_id}", response_model=schemas.Resource)
def update_resource(
    resource_id: UUID,
    resource_in: schemas.ResourceUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource:update"))
):
    """Update resource"""
    resource = services.get_resource(db, resource_id, tenant_id)
    return services.update_resource(db, resource, resource_in)

@router.delete("/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource:delete"))
):
    """Delete resource"""
    resource = services.get_resource(db, resource_id, tenant_id)
    services.delete_resource(db, resource)

# Resource Link endpoints
@router.post("/resources/{resource_id}/links", response_model=schemas.ResourceLink, status_code=status.HTTP_201_CREATED)
def create_resource_link(
    resource_id: UUID,
    link_in: schemas.ResourceLinkCreate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    user_id: UUID = Depends(deps.get_current_user),
    role: str = Depends(deps.rbac_check("resource_link:create"))
):
    """Create a resource link"""
    # Verify resource exists and belongs to tenant
    services.get_resource(db, resource_id, tenant_id)
    return services.create_resource_link(db, link_in, resource_id, user_id)

@router.get("/resources/{resource_id}/links", response_model=List[schemas.ResourceLink])
def list_resource_links(
    resource_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource_link:read"))
):
    """List resource links"""
    # Verify resource exists and belongs to tenant
    services.get_resource(db, resource_id, tenant_id)
    return services.get_resource_links(db, resource_id, tenant_id)

@router.get("/resources/links/{link_id}", response_model=schemas.ResourceLink)
def get_resource_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource_link:read"))
):
    """Get resource link by ID"""
    return services.get_resource_link(db, link_id, tenant_id)

@router.put("/resources/links/{link_id}", response_model=schemas.ResourceLink)
def update_resource_link(
    link_id: UUID,
    link_in: schemas.ResourceLinkUpdate,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource_link:update"))
):
    """Update resource link"""
    link = services.get_resource_link(db, link_id, tenant_id)
    return services.update_resource_link(db, link, link_in)

@router.delete("/resources/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource_link(
    link_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource_link:delete"))
):
    """Delete resource link"""
    link = services.get_resource_link(db, link_id, tenant_id)
    services.delete_resource_link(db, link)

# Analysis and impact endpoints
@router.get("/resources/{resource_id}/impact-score", response_model=schemas.ImpactScore)
def get_impact_score(
    resource_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("impact:read"))
):
    """Get impact score for resource"""
    return services.get_impact_score(db, resource_id, tenant_id)

@router.get("/resources/{resource_id}/allocation-map", response_model=schemas.AllocationMap)
def get_allocation_map(
    resource_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("allocation:read"))
):
    """Get allocation map for resource"""
    return services.get_allocation_map(db, resource_id, tenant_id)

@router.get("/resources/{resource_id}/analysis", response_model=schemas.ResourceAnalysis)
def analyze_resource(
    resource_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("analysis:read"))
):
    """Analyze resource for operational insights"""
    return services.analyze_resource(db, resource_id, tenant_id)

# Domain-specific query endpoints
@router.get("/resources/by-type/{resource_type}", response_model=List[schemas.Resource])
def get_resources_by_type(
    resource_type: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource:read"))
):
    """Get resources by type"""
    return services.get_resources_by_type(db, tenant_id, resource_type)

@router.get("/resources/by-status/{deployment_status}", response_model=List[schemas.Resource])
def get_resources_by_status(
    deployment_status: str,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource:read"))
):
    """Get resources by status"""
    return services.get_resources_by_status(db, tenant_id, deployment_status)

@router.get("/resources/by-capability/{capability_id}", response_model=List[schemas.Resource])
def get_resources_by_capability(
    capability_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource:read"))
):
    """Get resources by capability"""
    return services.get_resources_by_capability(db, tenant_id, capability_id)

@router.get("/resources/by-performance/{performance_threshold}", response_model=List[schemas.Resource])
def get_resources_by_performance(
    performance_threshold: float,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource:read"))
):
    """Get resources by performance threshold"""
    return services.get_resources_by_performance(db, tenant_id, performance_threshold)

@router.get("/resources/by-element/{element_type}/{element_id}", response_model=List[schemas.Resource])
def get_resources_by_element(
    element_type: str,
    element_id: UUID,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource:read"))
):
    """Get resources by linked element"""
    return services.get_resources_by_element(db, tenant_id, element_type, element_id)

@router.get("/resources/active", response_model=List[schemas.Resource])
def get_active_resources(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource:read"))
):
    """Get active resources"""
    return services.get_active_resources(db, tenant_id)

@router.get("/resources/critical", response_model=List[schemas.Resource])
def get_critical_resources(
    db: Session = Depends(deps.get_db),
    tenant_id: UUID = Depends(deps.get_current_tenant),
    role: str = Depends(deps.rbac_check("resource:read"))
):
    """Get critical resources"""
    return services.get_critical_resources(db, tenant_id)

# Enumeration endpoints
@router.get("/resources/resource-types", response_model=List[str])
def get_resource_types():
    """Get all resource types"""
    return [e.value for e in schemas.ResourceType]

@router.get("/resources/deployment-statuses", response_model=List[str])
def get_deployment_statuses():
    """Get all deployment statuses"""
    return [e.value for e in schemas.DeploymentStatus]

@router.get("/resources/criticalities", response_model=List[str])
def get_criticalities():
    """Get all criticality levels"""
    return [e.value for e in schemas.Criticality]

@router.get("/resources/strategic-importances", response_model=List[str])
def get_strategic_importances():
    """Get all strategic importance levels"""
    return [e.value for e in schemas.StrategicImportance]

@router.get("/resources/business-values", response_model=List[str])
def get_business_values():
    """Get all business value levels"""
    return [e.value for e in schemas.BusinessValue]

@router.get("/resources/operational-hours", response_model=List[str])
def get_operational_hours():
    """Get all operational hour types"""
    return [e.value for e in schemas.OperationalHours]

@router.get("/resources/expertise-levels", response_model=List[str])
def get_expertise_levels():
    """Get all expertise levels"""
    return [e.value for e in schemas.ExpertiseLevel]

@router.get("/resources/governance-models", response_model=List[str])
def get_governance_models():
    """Get all governance models"""
    return [e.value for e in schemas.GovernanceModel]

@router.get("/resources/link-types", response_model=List[str])
def get_link_types():
    """Get all link types"""
    return [e.value for e in schemas.LinkType]

@router.get("/resources/relationship-strengths", response_model=List[str])
def get_relationship_strengths():
    """Get all relationship strengths"""
    return [e.value for e in schemas.RelationshipStrength]

@router.get("/resources/dependency-levels", response_model=List[str])
def get_dependency_levels():
    """Get all dependency levels"""
    return [e.value for e in schemas.DependencyLevel]

@router.get("/resources/interaction-frequencies", response_model=List[str])
def get_interaction_frequencies():
    """Get all interaction frequencies"""
    return [e.value for e in schemas.InteractionFrequency]

@router.get("/resources/interaction-types", response_model=List[str])
def get_interaction_types():
    """Get all interaction types"""
    return [e.value for e in schemas.InteractionType]

@router.get("/resources/data-flow-directions", response_model=List[str])
def get_data_flow_directions():
    """Get all data flow directions"""
    return [e.value for e in schemas.DataFlowDirection]

@router.get("/resources/performance-impacts", response_model=List[str])
def get_performance_impacts():
    """Get all performance impact levels"""
    return [e.value for e in schemas.PerformanceImpact]

@router.get("/resources/allocation-priorities", response_model=List[str])
def get_allocation_priorities():
    """Get all allocation priorities"""
    return [e.value for e in schemas.AllocationPriority] 