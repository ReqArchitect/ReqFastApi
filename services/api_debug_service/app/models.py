from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class EndpointInfo(BaseModel):
    path: str
    method: str = "GET"
    description: Optional[str] = None
    parameters: Optional[List[str]] = None


class ServiceEndpointMap(BaseModel):
    service_name: str
    docker_container_name: Optional[str] = None
    base_url: str
    status: ServiceStatus
    available_endpoints: List[EndpointInfo] = Field(default_factory=list)
    last_heartbeat: Optional[datetime] = None
    version_tag: Optional[str] = None
    port: Optional[int] = None
    container_id: Optional[str] = None
    image: Optional[str] = None
    labels: Dict[str, str] = Field(default_factory=dict)


class HealthSummary(BaseModel):
    total_services: int
    healthy_services: int
    unhealthy_services: int
    unknown_services: int
    services: List[ServiceEndpointMap]
    last_updated: datetime
    cache_status: str


class EndpointDiscoveryResult(BaseModel):
    service_name: str
    discovery_method: str
    endpoints_found: int
    endpoints: List[EndpointInfo]
    error: Optional[str] = None


class DockerContainerInfo(BaseModel):
    container_id: str
    name: str
    image: str
    status: str
    ports: Dict[str, str]
    labels: Dict[str, str]
    created: datetime
    network_settings: Dict[str, Any] = Field(default_factory=dict)


class ServiceDiscoveryConfig(BaseModel):
    docker_network: str = "reqarchitect-network"
    service_label: str = "reqarchitect-service=true"
    cache_ttl_seconds: int = 300  # 5 minutes
    health_check_timeout: int = 5
    endpoint_discovery_timeout: int = 10
    max_retries: int = 3 