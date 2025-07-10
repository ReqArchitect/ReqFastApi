from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from .database import get_db_session
from .deps import get_current_user, get_redis_client, check_permissions
from .services import NodeService, NodeLinkService
from .schemas import (
    NodeCreate, NodeUpdate, NodeResponse, NodeListResponse,
    NodeLinkCreate, NodeLinkUpdate, NodeLinkResponse, NodeLinkListResponse,
    DeploymentMapResponse, CapacityAnalysisResponse, NodeAnalysisResponse,
    EnumerationResponse
)

router = APIRouter(prefix="/nodes", tags=["nodes"])

# Node Management Endpoints

@router.post("/", response_model=NodeResponse, status_code=status.HTTP_201_CREATED)
async def create_node(
    node_data: NodeCreate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Create a new node."""
    await check_permissions(current_user, "node:create")
    
    node_service = NodeService(db, redis_client)
    node = node_service.create_node(
        node_data=node_data,
        tenant_id=current_user["tenant_id"],
        user_id=current_user["user_id"]
    )
    return node

@router.get("/", response_model=List[NodeResponse])
async def list_nodes(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    node_type: Optional[str] = Query(None, description="Filter by node type"),
    environment: Optional[str] = Query(None, description="Filter by environment"),
    lifecycle_state: Optional[str] = Query(None, description="Filter by lifecycle state"),
    region: Optional[str] = Query(None, description="Filter by region"),
    security_level: Optional[str] = Query(None, description="Filter by security level"),
    cluster_id: Optional[UUID] = Query(None, description="Filter by cluster ID"),
    performance_threshold: Optional[float] = Query(None, ge=0.0, le=100.0, description="Filter by minimum availability"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """List all nodes with filtering and pagination."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    nodes, total = node_service.list_nodes(
        tenant_id=current_user["tenant_id"],
        skip=skip,
        limit=limit,
        node_type=node_type,
        environment=environment,
        lifecycle_state=lifecycle_state,
        region=region,
        security_level=security_level,
        cluster_id=cluster_id,
        performance_threshold=performance_threshold
    )
    return nodes

@router.get("/{node_id}", response_model=NodeResponse)
async def get_node(
    node_id: UUID = Path(..., description="Node ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get a node by ID."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    node = node_service.get_node(node_id, current_user["tenant_id"])
    
    if not node:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    
    return node

@router.put("/{node_id}", response_model=NodeResponse)
async def update_node(
    node_data: NodeUpdate,
    node_id: UUID = Path(..., description="Node ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Update a node."""
    await check_permissions(current_user, "node:update")
    
    node_service = NodeService(db, redis_client)
    node = node_service.update_node(node_id, node_data, current_user["tenant_id"])
    
    if not node:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    
    return node

@router.delete("/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_node(
    node_id: UUID = Path(..., description="Node ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Delete a node."""
    await check_permissions(current_user, "node:delete")
    
    node_service = NodeService(db, redis_client)
    success = node_service.delete_node(node_id, current_user["tenant_id"])
    
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")

# Node Link Management Endpoints

@router.post("/{node_id}/links", response_model=NodeLinkResponse, status_code=status.HTTP_201_CREATED)
async def create_node_link(
    link_data: NodeLinkCreate,
    node_id: UUID = Path(..., description="Node ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Create a link between a node and another element."""
    await check_permissions(current_user, "node_link:create")
    
    link_service = NodeLinkService(db, redis_client)
    link = link_service.create_node_link(
        node_id=node_id,
        link_data=link_data,
        tenant_id=current_user["tenant_id"],
        user_id=current_user["user_id"]
    )
    return link

@router.get("/{node_id}/links", response_model=List[NodeLinkResponse])
async def list_node_links(
    node_id: UUID = Path(..., description="Node ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """List all links for a node."""
    await check_permissions(current_user, "node_link:read")
    
    link_service = NodeLinkService(db, redis_client)
    links = link_service.list_node_links(node_id, current_user["tenant_id"])
    return links

@router.get("/links/{link_id}", response_model=NodeLinkResponse)
async def get_node_link(
    link_id: UUID = Path(..., description="Link ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get a node link by ID."""
    await check_permissions(current_user, "node_link:read")
    
    link_service = NodeLinkService(db, redis_client)
    link = link_service.get_node_link(link_id, current_user["tenant_id"])
    
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node link not found")
    
    return link

@router.put("/links/{link_id}", response_model=NodeLinkResponse)
async def update_node_link(
    link_data: NodeLinkUpdate,
    link_id: UUID = Path(..., description="Link ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Update a node link."""
    await check_permissions(current_user, "node_link:update")
    
    link_service = NodeLinkService(db, redis_client)
    link = link_service.update_node_link(link_id, link_data, current_user["tenant_id"])
    
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node link not found")
    
    return link

@router.delete("/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_node_link(
    link_id: UUID = Path(..., description="Link ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Delete a node link."""
    await check_permissions(current_user, "node_link:delete")
    
    link_service = NodeLinkService(db, redis_client)
    success = link_service.delete_node_link(link_id, current_user["tenant_id"])
    
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node link not found")

# Analysis & Impact Endpoints

@router.get("/{node_id}/deployment-map", response_model=DeploymentMapResponse)
async def get_deployment_map(
    node_id: UUID = Path(..., description="Node ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get deployment map for a node."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    deployment_map = node_service.get_deployment_map(node_id, current_user["tenant_id"])
    
    if not deployment_map:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    
    return deployment_map

@router.get("/{node_id}/capacity-analysis", response_model=CapacityAnalysisResponse)
async def get_capacity_analysis(
    node_id: UUID = Path(..., description="Node ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get capacity analysis for a node."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    capacity_analysis = node_service.get_capacity_analysis(node_id, current_user["tenant_id"])
    
    if not capacity_analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    
    return capacity_analysis

@router.get("/{node_id}/analysis", response_model=NodeAnalysisResponse)
async def analyze_node(
    node_id: UUID = Path(..., description="Node ID"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get comprehensive analysis for a node."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    analysis = node_service.analyze_node(node_id, current_user["tenant_id"])
    
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    
    return analysis

# Domain-Specific Query Endpoints

@router.get("/by-type/{node_type}", response_model=List[NodeResponse])
async def get_nodes_by_type(
    node_type: str = Path(..., description="Node type"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get nodes filtered by type."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    nodes = node_service.get_nodes_by_type(node_type, current_user["tenant_id"])
    return nodes

@router.get("/by-environment/{environment}", response_model=List[NodeResponse])
async def get_nodes_by_environment(
    environment: str = Path(..., description="Environment"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get nodes filtered by environment."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    nodes = node_service.get_nodes_by_environment(environment, current_user["tenant_id"])
    return nodes

@router.get("/by-region/{region}", response_model=List[NodeResponse])
async def get_nodes_by_region(
    region: str = Path(..., description="Region"),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get nodes filtered by region."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    nodes = node_service.get_nodes_by_region(region, current_user["tenant_id"])
    return nodes

@router.get("/active", response_model=List[NodeResponse])
async def get_active_nodes(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get all active nodes."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    nodes = node_service.get_active_nodes(current_user["tenant_id"])
    return nodes

@router.get("/critical", response_model=List[NodeResponse])
async def get_critical_nodes(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get all critical nodes."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    nodes = node_service.get_critical_nodes(current_user["tenant_id"])
    return nodes

# Enumeration Endpoints

@router.get("/node-types", response_model=EnumerationResponse)
async def get_node_types(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get all available node types."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    node_types = node_service.get_node_types()
    return EnumerationResponse(values=node_types)

@router.get("/environments", response_model=EnumerationResponse)
async def get_environments(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get all available environments."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    environments = node_service.get_environments()
    return EnumerationResponse(values=environments)

@router.get("/lifecycle-states", response_model=EnumerationResponse)
async def get_lifecycle_states(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get all available lifecycle states."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    lifecycle_states = node_service.get_lifecycle_states()
    return EnumerationResponse(values=lifecycle_states)

@router.get("/security-levels", response_model=EnumerationResponse)
async def get_security_levels(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get all available security levels."""
    await check_permissions(current_user, "node:read")
    
    node_service = NodeService(db, redis_client)
    security_levels = node_service.get_security_levels()
    return EnumerationResponse(values=security_levels)

@router.get("/link-types", response_model=EnumerationResponse)
async def get_link_types(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
    redis_client = Depends(get_redis_client)
):
    """Get all available link types."""
    await check_permissions(current_user, "node_link:read")
    
    node_service = NodeService(db, redis_client)
    link_types = node_service.get_link_types()
    return EnumerationResponse(values=link_types) 