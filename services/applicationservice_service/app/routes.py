from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from uuid import UUID
import logging

from .deps import get_current_user, get_db, get_redis_client, check_permissions
from .services import ApplicationServiceService, ServiceLinkService
from .schemas import (
    ApplicationServiceCreate, ApplicationServiceUpdate, ApplicationServiceResponse,
    ServiceLinkCreate, ServiceLinkUpdate, ServiceLinkResponse,
    ImpactMapResponse, PerformanceScoreResponse, ServiceAnalysisResponse,
    ApplicationServiceListResponse, ServiceLinkListResponse, EnumerationResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/application-services", tags=["Application Services"])

# Application Service Management Endpoints

@router.post("/", response_model=ApplicationServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_application_service(
    service_data: ApplicationServiceCreate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Create a new application service."""
    await check_permissions(current_user, "application_service:create")
    
    service_service = ApplicationServiceService(db, redis_client)
    return service_service.create_application_service(
        service_data, current_user["tenant_id"], current_user["user_id"]
    )

@router.get("/", response_model=List[ApplicationServiceResponse])
async def list_application_services(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    business_criticality: Optional[str] = Query(None),
    business_value: Optional[str] = Query(None),
    capability_id: Optional[UUID] = Query(None),
    technology_stack: Optional[str] = Query(None),
    performance_threshold: Optional[float] = Query(None),
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """List application services with filtering and pagination."""
    await check_permissions(current_user, "application_service:read")
    
    service_service = ApplicationServiceService(db, redis_client)
    return service_service.list_application_services(
        tenant_id=current_user["tenant_id"],
        skip=skip,
        limit=limit,
        service_type=service_type,
        status=status,
        business_criticality=business_criticality,
        business_value=business_value,
        capability_id=capability_id,
        technology_stack=technology_stack,
        performance_threshold=performance_threshold
    )

@router.get("/{service_id}", response_model=ApplicationServiceResponse)
async def get_application_service(
    service_id: UUID,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Get application service by ID."""
    await check_permissions(current_user, "application_service:read")
    
    service_service = ApplicationServiceService(db, redis_client)
    service = service_service.get_application_service(service_id, current_user["tenant_id"])
    
    if not service:
        raise HTTPException(status_code=404, detail="Application service not found")
    
    return service

@router.put("/{service_id}", response_model=ApplicationServiceResponse)
async def update_application_service(
    service_id: UUID,
    service_data: ApplicationServiceUpdate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Update application service."""
    await check_permissions(current_user, "application_service:update")
    
    service_service = ApplicationServiceService(db, redis_client)
    service = service_service.update_application_service(
        service_id, service_data, current_user["tenant_id"]
    )
    
    if not service:
        raise HTTPException(status_code=404, detail="Application service not found")
    
    return service

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application_service(
    service_id: UUID,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Delete application service."""
    await check_permissions(current_user, "application_service:delete")
    
    service_service = ApplicationServiceService(db, redis_client)
    success = service_service.delete_application_service(service_id, current_user["tenant_id"])
    
    if not success:
        raise HTTPException(status_code=404, detail="Application service not found")

# Service Link Management Endpoints

@router.post("/{service_id}/links", response_model=ServiceLinkResponse, status_code=status.HTTP_201_CREATED)
async def create_service_link(
    service_id: UUID,
    link_data: ServiceLinkCreate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Create a link between an application service and another element."""
    await check_permissions(current_user, "application_service:create")
    
    link_service = ServiceLinkService(db, redis_client)
    return link_service.create_service_link(
        service_id, link_data, current_user["tenant_id"], current_user["user_id"]
    )

@router.get("/{service_id}/links", response_model=List[ServiceLinkResponse])
async def list_service_links(
    service_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """List all links for an application service."""
    await check_permissions(current_user, "application_service:read")
    
    link_service = ServiceLinkService(db, redis_client)
    return link_service.list_service_links(
        service_id, current_user["tenant_id"], skip, limit
    )

@router.get("/links/{link_id}", response_model=ServiceLinkResponse)
async def get_service_link(
    link_id: UUID,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Get service link by ID."""
    await check_permissions(current_user, "application_service:read")
    
    link_service = ServiceLinkService(db, redis_client)
    link = link_service.get_service_link(link_id, current_user["tenant_id"])
    
    if not link:
        raise HTTPException(status_code=404, detail="Service link not found")
    
    return link

@router.put("/links/{link_id}", response_model=ServiceLinkResponse)
async def update_service_link(
    link_id: UUID,
    link_data: ServiceLinkUpdate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Update service link."""
    await check_permissions(current_user, "application_service:update")
    
    link_service = ServiceLinkService(db, redis_client)
    link = link_service.update_service_link(link_id, link_data, current_user["tenant_id"])
    
    if not link:
        raise HTTPException(status_code=404, detail="Service link not found")
    
    return link

@router.delete("/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service_link(
    link_id: UUID,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Delete service link."""
    await check_permissions(current_user, "application_service:delete")
    
    link_service = ServiceLinkService(db, redis_client)
    success = link_service.delete_service_link(link_id, current_user["tenant_id"])
    
    if not success:
        raise HTTPException(status_code=404, detail="Service link not found")

# Analysis & Impact Endpoints

@router.get("/{service_id}/impact-map", response_model=ImpactMapResponse)
async def get_impact_map(
    service_id: UUID,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Get impact mapping for application service."""
    await check_permissions(current_user, "application_service:read")
    
    service_service = ApplicationServiceService(db, redis_client)
    impact_map = service_service.get_impact_map(service_id, current_user["tenant_id"])
    
    if not impact_map:
        raise HTTPException(status_code=404, detail="Application service not found")
    
    return impact_map

@router.get("/{service_id}/performance-score", response_model=PerformanceScoreResponse)
async def get_performance_score(
    service_id: UUID,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Get performance score for application service."""
    await check_permissions(current_user, "application_service:read")
    
    service_service = ApplicationServiceService(db, redis_client)
    performance_score = service_service.get_performance_score(service_id, current_user["tenant_id"])
    
    if not performance_score:
        raise HTTPException(status_code=404, detail="Application service not found")
    
    return performance_score

@router.get("/{service_id}/analysis", response_model=ServiceAnalysisResponse)
async def analyze_service(
    service_id: UUID,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Analyze application service comprehensively."""
    await check_permissions(current_user, "application_service:read")
    
    service_service = ApplicationServiceService(db, redis_client)
    analysis = service_service.analyze_service(service_id, current_user["tenant_id"])
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Application service not found")
    
    return analysis

# Domain-Specific Query Endpoints

@router.get("/by-type/{service_type}", response_model=List[ApplicationServiceResponse])
async def get_by_service_type(
    service_type: str,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Get application services by type."""
    await check_permissions(current_user, "application_service:read")
    
    service_service = ApplicationServiceService(db, redis_client)
    return service_service.list_application_services(
        tenant_id=current_user["tenant_id"],
        service_type=service_type
    )

@router.get("/by-status/{status}", response_model=List[ApplicationServiceResponse])
async def get_by_status(
    status: str,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Get application services by status."""
    await check_permissions(current_user, "application_service:read")
    
    service_service = ApplicationServiceService(db, redis_client)
    return service_service.list_application_services(
        tenant_id=current_user["tenant_id"],
        status=status
    )

@router.get("/by-capability/{capability_id}", response_model=List[ApplicationServiceResponse])
async def get_by_capability(
    capability_id: UUID,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Get application services by capability."""
    await check_permissions(current_user, "application_service:read")
    
    service_service = ApplicationServiceService(db, redis_client)
    return service_service.list_application_services(
        tenant_id=current_user["tenant_id"],
        capability_id=capability_id
    )

@router.get("/by-performance/{performance_threshold}", response_model=List[ApplicationServiceResponse])
async def get_by_performance(
    performance_threshold: float,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Get application services with availability above threshold."""
    await check_permissions(current_user, "application_service:read")
    
    service_service = ApplicationServiceService(db, redis_client)
    return service_service.list_application_services(
        tenant_id=current_user["tenant_id"],
        performance_threshold=performance_threshold
    )

@router.get("/by-element/{element_type}/{element_id}", response_model=List[ApplicationServiceResponse])
async def get_by_element(
    element_type: str,
    element_id: UUID,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Get application services linked to a specific element."""
    await check_permissions(current_user, "application_service:read")
    
    # This would require a more complex query to find services linked to specific elements
    # For now, return empty list - could be implemented with additional service method
    return []

@router.get("/active", response_model=List[ApplicationServiceResponse])
async def get_active_services(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Get all active application services."""
    await check_permissions(current_user, "application_service:read")
    
    service_service = ApplicationServiceService(db, redis_client)
    return service_service.list_application_services(
        tenant_id=current_user["tenant_id"],
        status="active"
    )

@router.get("/critical", response_model=List[ApplicationServiceResponse])
async def get_critical_services(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),
    redis_client = Depends(get_redis_client)
):
    """Get all critical application services."""
    await check_permissions(current_user, "application_service:read")
    
    service_service = ApplicationServiceService(db, redis_client)
    return service_service.list_application_services(
        tenant_id=current_user["tenant_id"],
        business_criticality="critical"
    )

# Enumeration Endpoints

@router.get("/service-types", response_model=EnumerationResponse)
async def get_service_types():
    """Get all available service types."""
    return EnumerationResponse(values=[
        "ui", "api", "data", "integration", "messaging"
    ])

@router.get("/statuses", response_model=EnumerationResponse)
async def get_statuses():
    """Get all available statuses."""
    return EnumerationResponse(values=[
        "active", "inactive", "deprecated", "planned", "maintenance"
    ])

@router.get("/business-criticalities", response_model=EnumerationResponse)
async def get_business_criticalities():
    """Get all available business criticality levels."""
    return EnumerationResponse(values=[
        "low", "medium", "high", "critical"
    ])

@router.get("/business-values", response_model=EnumerationResponse)
async def get_business_values():
    """Get all available business value levels."""
    return EnumerationResponse(values=[
        "low", "medium", "high", "critical"
    ])

@router.get("/delivery-channels", response_model=EnumerationResponse)
async def get_delivery_channels():
    """Get all available delivery channels."""
    return EnumerationResponse(values=[
        "http", "https", "grpc", "websocket", "message_queue", "file_transfer"
    ])

@router.get("/authentication-methods", response_model=EnumerationResponse)
async def get_authentication_methods():
    """Get all available authentication methods."""
    return EnumerationResponse(values=[
        "none", "basic", "oauth", "jwt", "api_key"
    ])

@router.get("/deployment-models", response_model=EnumerationResponse)
async def get_deployment_models():
    """Get all available deployment models."""
    return EnumerationResponse(values=[
        "monolithic", "microservice", "serverless", "container"
    ])

@router.get("/scaling-strategies", response_model=EnumerationResponse)
async def get_scaling_strategies():
    """Get all available scaling strategies."""
    return EnumerationResponse(values=[
        "horizontal", "vertical", "auto"
    ])

@router.get("/security-levels", response_model=EnumerationResponse)
async def get_security_levels():
    """Get all available security levels."""
    return EnumerationResponse(values=[
        "basic", "standard", "high", "critical"
    ])

@router.get("/data-classifications", response_model=EnumerationResponse)
async def get_data_classifications():
    """Get all available data classification levels."""
    return EnumerationResponse(values=[
        "public", "internal", "confidential", "restricted"
    ])

@router.get("/link-types", response_model=EnumerationResponse)
async def get_link_types():
    """Get all available link types."""
    return EnumerationResponse(values=[
        "realizes", "supports", "enables", "consumes", "produces", "triggers", "requires"
    ])

@router.get("/relationship-strengths", response_model=EnumerationResponse)
async def get_relationship_strengths():
    """Get all available relationship strengths."""
    return EnumerationResponse(values=[
        "strong", "medium", "weak"
    ])

@router.get("/dependency-levels", response_model=EnumerationResponse)
async def get_dependency_levels():
    """Get all available dependency levels."""
    return EnumerationResponse(values=[
        "high", "medium", "low"
    ])

@router.get("/interaction-frequencies", response_model=EnumerationResponse)
async def get_interaction_frequencies():
    """Get all available interaction frequencies."""
    return EnumerationResponse(values=[
        "frequent", "regular", "occasional", "rare"
    ])

@router.get("/interaction-types", response_model=EnumerationResponse)
async def get_interaction_types():
    """Get all available interaction types."""
    return EnumerationResponse(values=[
        "synchronous", "asynchronous", "batch", "real_time", "event_driven"
    ])

@router.get("/data-flow-directions", response_model=EnumerationResponse)
async def get_data_flow_directions():
    """Get all available data flow directions."""
    return EnumerationResponse(values=[
        "input", "output", "bidirectional"
    ])

@router.get("/performance-impacts", response_model=EnumerationResponse)
async def get_performance_impacts():
    """Get all available performance impact levels."""
    return EnumerationResponse(values=[
        "low", "medium", "high", "critical"
    ]) 