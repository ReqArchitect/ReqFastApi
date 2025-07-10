from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime
from .database import get_db
from .models import PackageType, PackageStatus, DeliveryRisk, LinkType, RelationshipStrength, DependencyLevel
from .schemas import (
    WorkPackageCreate, WorkPackageUpdate, WorkPackageResponse, WorkPackageList,
    PackageLinkCreate, PackageLinkUpdate, PackageLinkResponse,
    ExecutionStatusResponse, GapClosureMapResponse, EnumResponse, HealthResponse, ErrorResponse
)
from .services import WorkPackageService, PackageLinkService
from .deps import get_current_user, get_current_tenant, require_permission

router = APIRouter(prefix="/work-packages", tags=["Work Packages"])

# Work Package CRUD endpoints
@router.post("/", response_model=WorkPackageResponse, status_code=status.HTTP_201_CREATED)
async def create_work_package(
    work_package_data: WorkPackageCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Create a new work package"""
    require_permission(current_user, "work_package:create")
    
    work_package = WorkPackageService.create_work_package(
        db, work_package_data, current_tenant["id"], current_user["id"]
    )
    return work_package

@router.get("/", response_model=List[WorkPackageList])
async def list_work_packages(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    package_type: Optional[PackageType] = Query(None, description="Filter by package type"),
    status: Optional[PackageStatus] = Query(None, description="Filter by status"),
    delivery_risk: Optional[DeliveryRisk] = Query(None, description="Filter by delivery risk"),
    change_owner_id: Optional[uuid.UUID] = Query(None, description="Filter by change owner"),
    related_goal_id: Optional[uuid.UUID] = Query(None, description="Filter by related goal"),
    target_plateau_id: Optional[uuid.UUID] = Query(None, description="Filter by target plateau"),
    progress_threshold: Optional[float] = Query(None, ge=0.0, le=100.0, description="Filter by minimum progress"),
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """List work packages with filtering and pagination"""
    work_packages = WorkPackageService.list_work_packages(
        db, current_tenant["id"], skip, limit, package_type, status, delivery_risk,
        change_owner_id, related_goal_id, target_plateau_id, progress_threshold
    )
    return work_packages

@router.get("/{work_package_id}", response_model=WorkPackageResponse)
async def get_work_package(
    work_package_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get a work package by ID"""
    work_package = WorkPackageService.get_work_package(db, work_package_id, current_tenant["id"])
    if not work_package:
        raise HTTPException(status_code=404, detail="Work package not found")
    return work_package

@router.put("/{work_package_id}", response_model=WorkPackageResponse)
async def update_work_package(
    work_package_id: uuid.UUID,
    work_package_data: WorkPackageUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Update a work package"""
    require_permission(current_user, "work_package:update")
    
    work_package = WorkPackageService.update_work_package(
        db, work_package_id, work_package_data, current_tenant["id"]
    )
    if not work_package:
        raise HTTPException(status_code=404, detail="Work package not found")
    return work_package

@router.delete("/{work_package_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_package(
    work_package_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Delete a work package"""
    require_permission(current_user, "work_package:delete")
    
    success = WorkPackageService.delete_work_package(db, work_package_id, current_tenant["id"])
    if not success:
        raise HTTPException(status_code=404, detail="Work package not found")

# Package Link endpoints
@router.post("/{work_package_id}/links", response_model=PackageLinkResponse, status_code=status.HTTP_201_CREATED)
async def create_package_link(
    work_package_id: uuid.UUID,
    link_data: PackageLinkCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Create a link between a work package and another element"""
    require_permission(current_user, "work_package:create_link")
    
    package_link = PackageLinkService.create_package_link(
        db, work_package_id, link_data, current_tenant["id"], current_user["id"]
    )
    return package_link

@router.get("/{work_package_id}/links", response_model=List[PackageLinkResponse])
async def list_package_links(
    work_package_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """List all links for a work package"""
    package_links = PackageLinkService.list_package_links(db, work_package_id, current_tenant["id"])
    return package_links

@router.get("/links/{link_id}", response_model=PackageLinkResponse)
async def get_package_link(
    link_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get a package link by ID"""
    package_link = PackageLinkService.get_package_link(db, link_id, current_tenant["id"])
    if not package_link:
        raise HTTPException(status_code=404, detail="Package link not found")
    return package_link

@router.put("/links/{link_id}", response_model=PackageLinkResponse)
async def update_package_link(
    link_id: uuid.UUID,
    link_data: PackageLinkUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Update a package link"""
    require_permission(current_user, "work_package:update_link")
    
    package_link = PackageLinkService.update_package_link(
        db, link_id, link_data, current_tenant["id"]
    )
    if not package_link:
        raise HTTPException(status_code=404, detail="Package link not found")
    return package_link

@router.delete("/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_package_link(
    link_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Delete a package link"""
    require_permission(current_user, "work_package:delete_link")
    
    success = PackageLinkService.delete_package_link(db, link_id, current_tenant["id"])
    if not success:
        raise HTTPException(status_code=404, detail="Package link not found")

# Analysis endpoints
@router.get("/{work_package_id}/execution-status", response_model=ExecutionStatusResponse)
async def get_execution_status(
    work_package_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get execution status analysis for a work package"""
    execution_status = WorkPackageService.get_execution_status(db, work_package_id, current_tenant["id"])
    if not execution_status:
        raise HTTPException(status_code=404, detail="Work package not found")
    return execution_status

@router.get("/{work_package_id}/gap-closure-map", response_model=GapClosureMapResponse)
async def get_gap_closure_map(
    work_package_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get gap closure mapping for a work package"""
    gap_closure_map = WorkPackageService.get_gap_closure_map(db, work_package_id, current_tenant["id"])
    if not gap_closure_map:
        raise HTTPException(status_code=404, detail="Work package not found")
    return gap_closure_map

# Domain-specific query endpoints
@router.get("/by-type/{package_type}", response_model=List[WorkPackageList])
async def get_work_packages_by_type(
    package_type: PackageType,
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get work packages by type"""
    work_packages = WorkPackageService.list_work_packages(
        db, current_tenant["id"], package_type=package_type
    )
    return work_packages

@router.get("/by-status/{status}", response_model=List[WorkPackageList])
async def get_work_packages_by_status(
    status: PackageStatus,
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get work packages by status"""
    work_packages = WorkPackageService.list_work_packages(
        db, current_tenant["id"], status=status
    )
    return work_packages

@router.get("/by-risk/{delivery_risk}", response_model=List[WorkPackageList])
async def get_work_packages_by_risk(
    delivery_risk: DeliveryRisk,
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get work packages by delivery risk"""
    work_packages = WorkPackageService.list_work_packages(
        db, current_tenant["id"], delivery_risk=delivery_risk
    )
    return work_packages

@router.get("/by-goal/{goal_id}", response_model=List[WorkPackageList])
async def get_work_packages_by_goal(
    goal_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get work packages by related goal"""
    work_packages = WorkPackageService.list_work_packages(
        db, current_tenant["id"], related_goal_id=goal_id
    )
    return work_packages

@router.get("/by-plateau/{plateau_id}", response_model=List[WorkPackageList])
async def get_work_packages_by_plateau(
    plateau_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get work packages by target plateau"""
    work_packages = WorkPackageService.list_work_packages(
        db, current_tenant["id"], target_plateau_id=plateau_id
    )
    return work_packages

@router.get("/by-owner/{owner_id}", response_model=List[WorkPackageList])
async def get_work_packages_by_owner(
    owner_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get work packages by change owner"""
    work_packages = WorkPackageService.list_work_packages(
        db, current_tenant["id"], change_owner_id=owner_id
    )
    return work_packages

@router.get("/by-progress/{progress_threshold}", response_model=List[WorkPackageList])
async def get_work_packages_by_progress(
    progress_threshold: float = Query(..., ge=0.0, le=100.0),
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get work packages with progress above threshold"""
    work_packages = WorkPackageService.list_work_packages(
        db, current_tenant["id"], progress_threshold=progress_threshold
    )
    return work_packages

@router.get("/by-element/{element_type}/{element_id}", response_model=List[WorkPackageList])
async def get_work_packages_by_element(
    element_type: str,
    element_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get work packages linked to a specific element"""
    # This would require additional service method to query by linked elements
    # For now, return empty list as placeholder
    return []

@router.get("/active", response_model=List[WorkPackageList])
async def get_active_work_packages(
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get all active work packages"""
    work_packages = WorkPackageService.list_work_packages(
        db, current_tenant["id"], status=PackageStatus.IN_PROGRESS
    )
    return work_packages

@router.get("/critical", response_model=List[WorkPackageList])
async def get_critical_work_packages(
    db: Session = Depends(get_db),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Get all critical work packages (high risk or high priority)"""
    work_packages = WorkPackageService.list_work_packages(
        db, current_tenant["id"], delivery_risk=DeliveryRisk.CRITICAL
    )
    return work_packages

# Enumeration endpoints
@router.get("/package-types", response_model=EnumResponse)
async def get_package_types():
    """Get all available package types"""
    return EnumResponse(values=[pt.value for pt in PackageType])

@router.get("/statuses", response_model=EnumResponse)
async def get_statuses():
    """Get all available statuses"""
    return EnumResponse(values=[s.value for s in PackageStatus])

@router.get("/delivery-risks", response_model=EnumResponse)
async def get_delivery_risks():
    """Get all available delivery risk levels"""
    return EnumResponse(values=[dr.value for dr in DeliveryRisk])

@router.get("/link-types", response_model=EnumResponse)
async def get_link_types():
    """Get all available link types"""
    return EnumResponse(values=[lt.value for lt in LinkType])

@router.get("/relationship-strengths", response_model=EnumResponse)
async def get_relationship_strengths():
    """Get all available relationship strengths"""
    return EnumResponse(values=[rs.value for rs in RelationshipStrength])

@router.get("/dependency-levels", response_model=EnumResponse)
async def get_dependency_levels():
    """Get all available dependency levels"""
    return EnumResponse(values=[dl.value for dl in DependencyLevel])

# Health check endpoint
@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        service="workpackage_service",
        version="1.0.0",
        database="connected",
        redis="connected"
    ) 