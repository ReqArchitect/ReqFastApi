from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from .database import get_db_session
from .services import ArtifactService, ArtifactLinkService
from .schemas import (
    ArtifactCreate, ArtifactUpdate, ArtifactResponse,
    ArtifactLinkCreate, ArtifactLinkUpdate, ArtifactLinkResponse,
    DependencyMapResponse, IntegrityCheckResponse, EnumerationResponse
)
from .deps import get_current_user, get_redis_client, check_permission
from .config import settings

router = APIRouter(prefix="/artifacts", tags=["artifacts"])

# Artifact Management Endpoints

@router.post("/", response_model=ArtifactResponse, status_code=status.HTTP_201_CREATED)
async def create_artifact(
    artifact_data: ArtifactCreate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Create a new artifact."""
    check_permission(current_user, "artifact:create")
    
    service = ArtifactService(db, redis_client)
    artifact = service.create_artifact(
        artifact_data, 
        current_user["tenant_id"], 
        current_user["user_id"]
    )
    return artifact

@router.get("/", response_model=List[ArtifactResponse])
async def list_artifacts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    artifact_type: Optional[str] = Query(None, description="Filter by artifact type"),
    lifecycle_state: Optional[str] = Query(None, description="Filter by lifecycle state"),
    deployment_environment: Optional[str] = Query(None, description="Filter by deployment environment"),
    format_filter: Optional[str] = Query(None, description="Filter by format (contains)"),
    deployment_target_node_id: Optional[uuid.UUID] = Query(None, description="Filter by deployment target node"),
    associated_component_id: Optional[uuid.UUID] = Query(None, description="Filter by associated component"),
    integrity_verified: Optional[bool] = Query(None, description="Filter by integrity verification status"),
    security_scan_passed: Optional[bool] = Query(None, description="Filter by security scan status"),
    compliance_status: Optional[str] = Query(None, description="Filter by compliance status"),
    data_classification: Optional[str] = Query(None, description="Filter by data classification"),
    size_threshold: Optional[float] = Query(None, ge=0, description="Filter by maximum size in MB"),
    vulnerability_threshold: Optional[int] = Query(None, ge=0, description="Filter by maximum vulnerability count"),
    quality_threshold: Optional[float] = Query(None, ge=0, le=1, description="Filter by minimum quality score"),
    search_term: Optional[str] = Query(None, description="Search in name, description, and storage location"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """List artifacts with filtering and pagination."""
    check_permission(current_user, "artifact:read")
    
    service = ArtifactService(db, redis_client)
    artifacts = service.list_artifacts(
        tenant_id=current_user["tenant_id"],
        skip=skip,
        limit=limit,
        artifact_type=artifact_type,
        lifecycle_state=lifecycle_state,
        deployment_environment=deployment_environment,
        format_filter=format_filter,
        deployment_target_node_id=deployment_target_node_id,
        associated_component_id=associated_component_id,
        integrity_verified=integrity_verified,
        security_scan_passed=security_scan_passed,
        compliance_status=compliance_status,
        data_classification=data_classification,
        size_threshold=size_threshold,
        vulnerability_threshold=vulnerability_threshold,
        quality_threshold=quality_threshold,
        search_term=search_term
    )
    return artifacts

@router.get("/{artifact_id}", response_model=ArtifactResponse)
async def get_artifact(
    artifact_id: uuid.UUID = Path(..., description="Artifact ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get an artifact by ID."""
    check_permission(current_user, "artifact:read")
    
    service = ArtifactService(db, redis_client)
    artifact = service.get_artifact(artifact_id, current_user["tenant_id"])
    
    if not artifact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact not found")
    
    return artifact

@router.put("/{artifact_id}", response_model=ArtifactResponse)
async def update_artifact(
    artifact_data: ArtifactUpdate,
    artifact_id: uuid.UUID = Path(..., description="Artifact ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Update an artifact."""
    check_permission(current_user, "artifact:update")
    
    service = ArtifactService(db, redis_client)
    artifact = service.update_artifact(artifact_id, artifact_data, current_user["tenant_id"])
    
    if not artifact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact not found")
    
    return artifact

@router.delete("/{artifact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artifact(
    artifact_id: uuid.UUID = Path(..., description="Artifact ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Delete an artifact."""
    check_permission(current_user, "artifact:delete")
    
    service = ArtifactService(db, redis_client)
    success = service.delete_artifact(artifact_id, current_user["tenant_id"])
    
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact not found")

# Artifact Link Management Endpoints

@router.post("/{artifact_id}/links", response_model=ArtifactLinkResponse, status_code=status.HTTP_201_CREATED)
async def create_artifact_link(
    link_data: ArtifactLinkCreate,
    artifact_id: uuid.UUID = Path(..., description="Artifact ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Create a link between an artifact and another element."""
    check_permission(current_user, "artifact_link:create")
    
    service = ArtifactLinkService(db, redis_client)
    link = service.create_artifact_link(
        artifact_id, 
        link_data, 
        current_user["tenant_id"], 
        current_user["user_id"]
    )
    return link

@router.get("/{artifact_id}/links", response_model=List[ArtifactLinkResponse])
async def list_artifact_links(
    artifact_id: uuid.UUID = Path(..., description="Artifact ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """List all links for an artifact."""
    check_permission(current_user, "artifact_link:read")
    
    service = ArtifactLinkService(db, redis_client)
    links = service.get_artifact_links(artifact_id, current_user["tenant_id"])
    return links

@router.get("/links/{link_id}", response_model=ArtifactLinkResponse)
async def get_artifact_link(
    link_id: uuid.UUID = Path(..., description="Link ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get an artifact link by ID."""
    check_permission(current_user, "artifact_link:read")
    
    service = ArtifactLinkService(db, redis_client)
    link = service.get_artifact_link(link_id, current_user["tenant_id"])
    
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact link not found")
    
    return link

@router.put("/links/{link_id}", response_model=ArtifactLinkResponse)
async def update_artifact_link(
    link_data: ArtifactLinkUpdate,
    link_id: uuid.UUID = Path(..., description="Link ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Update an artifact link."""
    check_permission(current_user, "artifact_link:update")
    
    service = ArtifactLinkService(db, redis_client)
    link = service.update_artifact_link(link_id, link_data, current_user["tenant_id"])
    
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact link not found")
    
    return link

@router.delete("/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artifact_link(
    link_id: uuid.UUID = Path(..., description="Link ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Delete an artifact link."""
    check_permission(current_user, "artifact_link:delete")
    
    service = ArtifactLinkService(db, redis_client)
    success = service.delete_artifact_link(link_id, current_user["tenant_id"])
    
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact link not found")

# Analysis Endpoints

@router.get("/{artifact_id}/dependency-map", response_model=DependencyMapResponse)
async def get_artifact_dependency_map(
    artifact_id: uuid.UUID = Path(..., description="Artifact ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get dependency map for an artifact."""
    check_permission(current_user, "artifact:read")
    
    service = ArtifactService(db, redis_client)
    dependency_map = service.get_artifact_dependency_map(artifact_id, current_user["tenant_id"])
    
    if not dependency_map:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact not found")
    
    return dependency_map

@router.get("/{artifact_id}/integrity-check", response_model=IntegrityCheckResponse)
async def check_artifact_integrity(
    artifact_id: uuid.UUID = Path(..., description="Artifact ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Check artifact integrity and security."""
    check_permission(current_user, "artifact:read")
    
    service = ArtifactService(db, redis_client)
    integrity_check = service.check_artifact_integrity(artifact_id, current_user["tenant_id"])
    
    if not integrity_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact not found")
    
    return integrity_check

# Domain-Specific Query Endpoints

@router.get("/by-type/{artifact_type}", response_model=List[ArtifactResponse])
async def get_artifacts_by_type(
    artifact_type: str = Path(..., description="Artifact type"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get artifacts by type."""
    check_permission(current_user, "artifact:read")
    
    service = ArtifactService(db, redis_client)
    artifacts = service.get_artifacts_by_type(artifact_type, current_user["tenant_id"])
    return artifacts

@router.get("/by-format/{format_filter}", response_model=List[ArtifactResponse])
async def get_artifacts_by_format(
    format_filter: str = Path(..., description="Format filter"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get artifacts by format."""
    check_permission(current_user, "artifact:read")
    
    service = ArtifactService(db, redis_client)
    artifacts = service.get_artifacts_by_format(format_filter, current_user["tenant_id"])
    return artifacts

@router.get("/by-deployment-target/{node_id}", response_model=List[ArtifactResponse])
async def get_artifacts_by_deployment_target(
    node_id: uuid.UUID = Path(..., description="Deployment target node ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get artifacts by deployment target node."""
    check_permission(current_user, "artifact:read")
    
    service = ArtifactService(db, redis_client)
    artifacts = service.get_artifacts_by_deployment_target(node_id, current_user["tenant_id"])
    return artifacts

@router.get("/by-component/{component_id}", response_model=List[ArtifactResponse])
async def get_artifacts_by_component(
    component_id: uuid.UUID = Path(..., description="Associated component ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get artifacts by associated component."""
    check_permission(current_user, "artifact:read")
    
    service = ArtifactService(db, redis_client)
    artifacts = service.get_artifacts_by_component(component_id, current_user["tenant_id"])
    return artifacts

@router.get("/by-modification-date/{start_date}/{end_date}", response_model=List[ArtifactResponse])
async def get_artifacts_by_modification_date(
    start_date: datetime = Path(..., description="Start date"),
    end_date: datetime = Path(..., description="End date"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get artifacts modified between dates."""
    check_permission(current_user, "artifact:read")
    
    service = ArtifactService(db, redis_client)
    artifacts = service.get_artifacts_by_modification_date(start_date, end_date, current_user["tenant_id"])
    return artifacts

@router.get("/active", response_model=List[ArtifactResponse])
async def get_active_artifacts(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get all active artifacts."""
    check_permission(current_user, "artifact:read")
    
    service = ArtifactService(db, redis_client)
    artifacts = service.get_active_artifacts(current_user["tenant_id"])
    return artifacts

@router.get("/critical", response_model=List[ArtifactResponse])
async def get_critical_artifacts(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get critical artifacts."""
    check_permission(current_user, "artifact:read")
    
    service = ArtifactService(db, redis_client)
    artifacts = service.get_critical_artifacts(current_user["tenant_id"])
    return artifacts

@router.get("/statistics")
async def get_artifact_statistics(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get artifact statistics for tenant."""
    check_permission(current_user, "artifact:read")
    
    service = ArtifactService(db, redis_client)
    statistics = service.get_artifact_statistics(current_user["tenant_id"])
    return statistics

# Link Query Endpoints

@router.get("/links/by-element/{element_type}/{element_id}", response_model=List[ArtifactLinkResponse])
async def get_links_by_element(
    element_type: str = Path(..., description="Element type"),
    element_id: uuid.UUID = Path(..., description="Element ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get artifact links by linked element."""
    check_permission(current_user, "artifact_link:read")
    
    service = ArtifactLinkService(db, redis_client)
    links = service.get_links_by_element(element_id, element_type, current_user["tenant_id"])
    return links

@router.get("/links/by-type/{link_type}", response_model=List[ArtifactLinkResponse])
async def get_links_by_type(
    link_type: str = Path(..., description="Link type"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get artifact links by link type."""
    check_permission(current_user, "artifact_link:read")
    
    service = ArtifactLinkService(db, redis_client)
    links = service.get_links_by_type(link_type, current_user["tenant_id"])
    return links

# Enumeration Endpoints

@router.get("/artifact-types", response_model=EnumerationResponse)
async def get_artifact_types():
    """Get all available artifact types."""
    from .schemas import ArtifactType
    return EnumerationResponse(values=[e.value for e in ArtifactType])

@router.get("/lifecycle-states", response_model=EnumerationResponse)
async def get_lifecycle_states():
    """Get all available lifecycle states."""
    from .schemas import LifecycleState
    return EnumerationResponse(values=[e.value for e in LifecycleState])

@router.get("/deployment-environments", response_model=EnumerationResponse)
async def get_deployment_environments():
    """Get all available deployment environments."""
    from .schemas import DeploymentEnvironment
    return EnumerationResponse(values=[e.value for e in DeploymentEnvironment])

@router.get("/access-levels", response_model=EnumerationResponse)
async def get_access_levels():
    """Get all available access levels."""
    from .schemas import AccessLevel
    return EnumerationResponse(values=[e.value for e in AccessLevel])

@router.get("/compliance-statuses", response_model=EnumerationResponse)
async def get_compliance_statuses():
    """Get all available compliance statuses."""
    from .schemas import ComplianceStatus
    return EnumerationResponse(values=[e.value for e in ComplianceStatus])

@router.get("/data-classifications", response_model=EnumerationResponse)
async def get_data_classifications():
    """Get all available data classifications."""
    from .schemas import DataClassification
    return EnumerationResponse(values=[e.value for e in DataClassification])

@router.get("/documentation-statuses", response_model=EnumerationResponse)
async def get_documentation_statuses():
    """Get all available documentation statuses."""
    from .schemas import DocumentationStatus
    return EnumerationResponse(values=[e.value for e in DocumentationStatus])

@router.get("/operational-hours", response_model=EnumerationResponse)
async def get_operational_hours():
    """Get all available operational hour types."""
    from .schemas import OperationalHours
    return EnumerationResponse(values=[e.value for e in OperationalHours])

@router.get("/link-types", response_model=EnumerationResponse)
async def get_link_types():
    """Get all available link types."""
    from .schemas import LinkType
    return EnumerationResponse(values=[e.value for e in LinkType])

@router.get("/relationship-strengths", response_model=EnumerationResponse)
async def get_relationship_strengths():
    """Get all available relationship strengths."""
    from .schemas import RelationshipStrength
    return EnumerationResponse(values=[e.value for e in RelationshipStrength])

@router.get("/dependency-levels", response_model=EnumerationResponse)
async def get_dependency_levels():
    """Get all available dependency levels."""
    from .schemas import DependencyLevel
    return EnumerationResponse(values=[e.value for e in DependencyLevel])

@router.get("/implementation-statuses", response_model=EnumerationResponse)
async def get_implementation_statuses():
    """Get all available implementation statuses."""
    from .schemas import ImplementationStatus
    return EnumerationResponse(values=[e.value for e in ImplementationStatus])

@router.get("/deployment-statuses", response_model=EnumerationResponse)
async def get_deployment_statuses():
    """Get all available deployment statuses."""
    from .schemas import DeploymentStatus
    return EnumerationResponse(values=[e.value for e in DeploymentStatus])

@router.get("/communication-frequencies", response_model=EnumerationResponse)
async def get_communication_frequencies():
    """Get all available communication frequencies."""
    from .schemas import CommunicationFrequency
    return EnumerationResponse(values=[e.value for e in CommunicationFrequency])

@router.get("/communication-types", response_model=EnumerationResponse)
async def get_communication_types():
    """Get all available communication types."""
    from .schemas import CommunicationType
    return EnumerationResponse(values=[e.value for e in CommunicationType])

@router.get("/performance-impacts", response_model=EnumerationResponse)
async def get_performance_impacts():
    """Get all available performance impact levels."""
    from .schemas import PerformanceImpact
    return EnumerationResponse(values=[e.value for e in PerformanceImpact])

@router.get("/business-criticalities", response_model=EnumerationResponse)
async def get_business_criticalities():
    """Get all available business criticality levels."""
    from .schemas import BusinessCriticality
    return EnumerationResponse(values=[e.value for e in BusinessCriticality])

@router.get("/risk-levels", response_model=EnumerationResponse)
async def get_risk_levels():
    """Get all available risk levels."""
    from .schemas import RiskLevel
    return EnumerationResponse(values=[e.value for e in RiskLevel])

@router.get("/logging-levels", response_model=EnumerationResponse)
async def get_logging_levels():
    """Get all available logging levels."""
    from .schemas import LoggingLevel
    return EnumerationResponse(values=[e.value for e in LoggingLevel]) 