from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import logging

from .database import get_db_session
from .services import SystemSoftwareService, SoftwareLinkService
from .schemas import (
    SystemSoftwareCreate, SystemSoftwareUpdate, SystemSoftwareResponse,
    SoftwareLinkCreate, SoftwareLinkUpdate, SoftwareLinkResponse,
    SystemSoftwareListResponse, SoftwareLinkListResponse,
    DependencyMapResponse, ComplianceCheckResponse, SystemSoftwareAnalysisResponse,
    EnumerationResponse
)
from .deps import get_current_user, get_redis_client, check_permission
from .config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/system-software", tags=["System Software"])

# System Software Management Endpoints

@router.post("/", response_model=SystemSoftwareResponse, status_code=status.HTTP_201_CREATED)
async def create_system_software(
    system_software_data: SystemSoftwareCreate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Create a new SystemSoftware."""
    await check_permission(current_user, "system_software:create")
    
    service = SystemSoftwareService(db, redis_client)
    system_software = service.create_system_software(
        tenant_id=current_user["tenant_id"],
        user_id=current_user["user_id"],
        system_software_data=system_software_data
    )
    
    return system_software

@router.get("/", response_model=List[SystemSoftwareResponse])
async def list_system_software(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    software_type: Optional[str] = Query(None, description="Filter by software type"),
    vendor: Optional[str] = Query(None, description="Filter by vendor"),
    lifecycle_state: Optional[str] = Query(None, description="Filter by lifecycle state"),
    vulnerability_threshold: Optional[float] = Query(None, ge=0.0, le=10.0, description="Filter by maximum vulnerability score"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """List SystemSoftware with filtering and pagination."""
    await check_permission(current_user, "system_software:read")
    
    service = SystemSoftwareService(db, redis_client)
    system_software_list = service.list_system_software(
        tenant_id=current_user["tenant_id"],
        skip=skip,
        limit=limit,
        software_type=software_type,
        vendor=vendor,
        lifecycle_state=lifecycle_state,
        vulnerability_threshold=vulnerability_threshold
    )
    
    return system_software_list

@router.get("/{system_software_id}", response_model=SystemSoftwareResponse)
async def get_system_software(
    system_software_id: uuid.UUID,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get SystemSoftware by ID."""
    await check_permission(current_user, "system_software:read")
    
    service = SystemSoftwareService(db, redis_client)
    system_software = service.get_system_software(system_software_id, current_user["tenant_id"])
    
    if not system_software:
        raise HTTPException(status_code=404, detail="System software not found")
    
    return system_software

@router.put("/{system_software_id}", response_model=SystemSoftwareResponse)
async def update_system_software(
    system_software_id: uuid.UUID,
    system_software_data: SystemSoftwareUpdate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Update SystemSoftware."""
    await check_permission(current_user, "system_software:update")
    
    service = SystemSoftwareService(db, redis_client)
    system_software = service.update_system_software(
        system_software_id=system_software_id,
        tenant_id=current_user["tenant_id"],
        system_software_data=system_software_data
    )
    
    if not system_software:
        raise HTTPException(status_code=404, detail="System software not found")
    
    return system_software

@router.delete("/{system_software_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system_software(
    system_software_id: uuid.UUID,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Delete SystemSoftware."""
    await check_permission(current_user, "system_software:delete")
    
    service = SystemSoftwareService(db, redis_client)
    success = service.delete_system_software(system_software_id, current_user["tenant_id"])
    
    if not success:
        raise HTTPException(status_code=404, detail="System software not found")

# Analysis Endpoints

@router.get("/{system_software_id}/dependency-map", response_model=DependencyMapResponse)
async def get_dependency_map(
    system_software_id: uuid.UUID,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get dependency map for SystemSoftware."""
    await check_permission(current_user, "system_software:read")
    
    service = SystemSoftwareService(db, redis_client)
    dependency_map = service.get_dependency_map(system_software_id, current_user["tenant_id"])
    
    if not dependency_map:
        raise HTTPException(status_code=404, detail="System software not found")
    
    return dependency_map

@router.get("/{system_software_id}/compliance-check", response_model=ComplianceCheckResponse)
async def get_compliance_check(
    system_software_id: uuid.UUID,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get compliance check for SystemSoftware."""
    await check_permission(current_user, "system_software:read")
    
    service = SystemSoftwareService(db, redis_client)
    compliance_check = service.get_compliance_check(system_software_id, current_user["tenant_id"])
    
    if not compliance_check:
        raise HTTPException(status_code=404, detail="System software not found")
    
    return compliance_check

@router.get("/{system_software_id}/analysis", response_model=SystemSoftwareAnalysisResponse)
async def analyze_system_software(
    system_software_id: uuid.UUID,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get comprehensive analysis for SystemSoftware."""
    await check_permission(current_user, "system_software:read")
    
    service = SystemSoftwareService(db, redis_client)
    analysis = service.analyze_system_software(system_software_id, current_user["tenant_id"])
    
    if not analysis:
        raise HTTPException(status_code=404, detail="System software not found")
    
    return analysis

# Domain-Specific Query Endpoints

@router.get("/by-type/{software_type}", response_model=List[SystemSoftwareResponse])
async def get_by_software_type(
    software_type: str,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get SystemSoftware by type."""
    await check_permission(current_user, "system_software:read")
    
    service = SystemSoftwareService(db, redis_client)
    return service.get_by_software_type(current_user["tenant_id"], software_type)

@router.get("/by-vendor/{vendor}", response_model=List[SystemSoftwareResponse])
async def get_by_vendor(
    vendor: str,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get SystemSoftware by vendor."""
    await check_permission(current_user, "system_software:read")
    
    service = SystemSoftwareService(db, redis_client)
    return service.get_by_vendor(current_user["tenant_id"], vendor)

@router.get("/by-vulnerability/{max_score}", response_model=List[SystemSoftwareResponse])
async def get_by_vulnerability_score(
    max_score: float,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get SystemSoftware with vulnerability score below threshold."""
    await check_permission(current_user, "system_software:read")
    
    service = SystemSoftwareService(db, redis_client)
    return service.get_by_vulnerability_score(current_user["tenant_id"], max_score)

@router.get("/by-lifecycle/{lifecycle_state}", response_model=List[SystemSoftwareResponse])
async def get_by_lifecycle_state(
    lifecycle_state: str,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get SystemSoftware by lifecycle state."""
    await check_permission(current_user, "system_software:read")
    
    service = SystemSoftwareService(db, redis_client)
    return service.get_by_lifecycle_state(current_user["tenant_id"], lifecycle_state)

@router.get("/active", response_model=List[SystemSoftwareResponse])
async def get_active_system_software(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get all active SystemSoftware."""
    await check_permission(current_user, "system_software:read")
    
    service = SystemSoftwareService(db, redis_client)
    return service.get_active_system_software(current_user["tenant_id"])

@router.get("/critical", response_model=List[SystemSoftwareResponse])
async def get_critical_system_software(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get critical SystemSoftware."""
    await check_permission(current_user, "system_software:read")
    
    service = SystemSoftwareService(db, redis_client)
    return service.get_critical_system_software(current_user["tenant_id"])

# Enumeration Endpoints

@router.get("/software-types", response_model=EnumerationResponse)
async def get_software_types():
    """Get all available software types."""
    return EnumerationResponse(values=[
        "os", "database", "middleware", "runtime", "container_engine"
    ])

@router.get("/license-types", response_model=EnumerationResponse)
async def get_license_types():
    """Get all available license types."""
    return EnumerationResponse(values=[
        "proprietary", "open_source", "commercial", "freeware"
    ])

@router.get("/lifecycle-states", response_model=EnumerationResponse)
async def get_lifecycle_states():
    """Get all available lifecycle states."""
    return EnumerationResponse(values=[
        "active", "inactive", "deprecated", "end_of_life", "planned"
    ])

@router.get("/compliance-statuses", response_model=EnumerationResponse)
async def get_compliance_statuses():
    """Get all available compliance statuses."""
    return EnumerationResponse(values=[
        "compliant", "non_compliant", "unknown", "pending"
    ])

@router.get("/update-channels", response_model=EnumerationResponse)
async def get_update_channels():
    """Get all available update channels."""
    return EnumerationResponse(values=[
        "stable", "beta", "alpha", "lts"
    ])

@router.get("/update-frequencies", response_model=EnumerationResponse)
async def get_update_frequencies():
    """Get all available update frequencies."""
    return EnumerationResponse(values=[
        "daily", "weekly", "monthly", "quarterly", "yearly"
    ])

@router.get("/deployment-environments", response_model=EnumerationResponse)
async def get_deployment_environments():
    """Get all available deployment environments."""
    return EnumerationResponse(values=[
        "production", "staging", "development", "testing"
    ])

@router.get("/support-levels", response_model=EnumerationResponse)
async def get_support_levels():
    """Get all available support levels."""
    return EnumerationResponse(values=[
        "basic", "standard", "premium", "enterprise"
    ])

# Software Link Management Endpoints

@router.post("/{system_software_id}/links", response_model=SoftwareLinkResponse, status_code=status.HTTP_201_CREATED)
async def create_software_link(
    system_software_id: uuid.UUID,
    link_data: SoftwareLinkCreate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Create a new SoftwareLink."""
    await check_permission(current_user, "system_software:create")
    
    service = SoftwareLinkService(db, redis_client)
    software_link = service.create_software_link(
        system_software_id=system_software_id,
        tenant_id=current_user["tenant_id"],
        user_id=current_user["user_id"],
        link_data=link_data
    )
    
    if not software_link:
        raise HTTPException(status_code=404, detail="System software not found")
    
    return software_link

@router.get("/{system_software_id}/links", response_model=List[SoftwareLinkResponse])
async def list_software_links(
    system_software_id: uuid.UUID,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """List SoftwareLinks for a SystemSoftware."""
    await check_permission(current_user, "system_software:read")
    
    service = SoftwareLinkService(db, redis_client)
    return service.list_software_links(system_software_id, current_user["tenant_id"])

@router.get("/links/{link_id}", response_model=SoftwareLinkResponse)
async def get_software_link(
    link_id: uuid.UUID,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get SoftwareLink by ID."""
    await check_permission(current_user, "system_software:read")
    
    service = SoftwareLinkService(db, redis_client)
    software_link = service.get_software_link(link_id, current_user["tenant_id"])
    
    if not software_link:
        raise HTTPException(status_code=404, detail="Software link not found")
    
    return software_link

@router.put("/links/{link_id}", response_model=SoftwareLinkResponse)
async def update_software_link(
    link_id: uuid.UUID,
    link_data: SoftwareLinkUpdate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Update SoftwareLink."""
    await check_permission(current_user, "system_software:update")
    
    service = SoftwareLinkService(db, redis_client)
    software_link = service.update_software_link(
        link_id=link_id,
        tenant_id=current_user["tenant_id"],
        link_data=link_data
    )
    
    if not software_link:
        raise HTTPException(status_code=404, detail="Software link not found")
    
    return software_link

@router.delete("/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_software_link(
    link_id: uuid.UUID,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Delete SoftwareLink."""
    await check_permission(current_user, "system_software:delete")
    
    service = SoftwareLinkService(db, redis_client)
    success = service.delete_software_link(link_id, current_user["tenant_id"])
    
    if not success:
        raise HTTPException(status_code=404, detail="Software link not found")

# Link-specific Enumeration Endpoints

@router.get("/link-types", response_model=EnumerationResponse)
async def get_link_types():
    """Get all available link types."""
    return EnumerationResponse(values=[
        "runs_on", "depends_on", "integrates_with", "manages", "supports"
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

@router.get("/integration-statuses", response_model=EnumerationResponse)
async def get_integration_statuses():
    """Get all available integration statuses."""
    return EnumerationResponse(values=[
        "active", "inactive", "failed", "pending", "deprecated"
    ])

@router.get("/communication-frequencies", response_model=EnumerationResponse)
async def get_communication_frequencies():
    """Get all available communication frequencies."""
    return EnumerationResponse(values=[
        "frequent", "regular", "occasional", "rare"
    ])

@router.get("/communication-types", response_model=EnumerationResponse)
async def get_communication_types():
    """Get all available communication types."""
    return EnumerationResponse(values=[
        "synchronous", "asynchronous", "batch", "real_time"
    ])

@router.get("/performance-impacts", response_model=EnumerationResponse)
async def get_performance_impacts():
    """Get all available performance impact levels."""
    return EnumerationResponse(values=[
        "low", "medium", "high", "critical"
    ])

@router.get("/business-values", response_model=EnumerationResponse)
async def get_business_values():
    """Get all available business value levels."""
    return EnumerationResponse(values=[
        "low", "medium", "high", "critical"
    ])

@router.get("/business-criticalities", response_model=EnumerationResponse)
async def get_business_criticalities():
    """Get all available business criticality levels."""
    return EnumerationResponse(values=[
        "low", "medium", "high", "critical"
    ]) 