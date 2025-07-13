from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
    VIRTUAL = "virtual"
    STARTING = "starting"
    STOPPED = "stopped"


class DiscoveryMethod(str, Enum):
    LABEL_BASED = "label_based"
    CATALOG_FALLBACK = "catalog_fallback"
    NETWORK_SCAN = "network_scan"
    VIRTUAL = "virtual"


class EndpointInfo(BaseModel):
    path: str
    method: str = "GET"
    description: Optional[str] = None
    parameters: Optional[List[str]] = None
    response_codes: Optional[List[int]] = None


class HealthCheckResult(BaseModel):
    is_healthy: bool
    status_code: Optional[int] = None
    response_time: Optional[float] = None
    error_message: Optional[str] = None
    last_check: datetime
    endpoint_tested: str


class ServiceEndpointMap(BaseModel):
    service_name: str
    docker_container_name: Optional[str] = None
    base_url: str
    status: ServiceStatus
    discovery_method: DiscoveryMethod
    available_endpoints: List[EndpointInfo] = Field(default_factory=list)
    health_check: Optional[HealthCheckResult] = None
    last_heartbeat: Optional[datetime] = None
    version_tag: Optional[str] = None
    port: Optional[int] = None
    container_id: Optional[str] = None
    image: Optional[str] = None
    labels: Dict[str, str] = Field(default_factory=dict)
    network_info: Optional[Dict[str, Any]] = None
    catalog_entry: Optional[Dict[str, Any]] = None
    is_virtual: bool = False
    error_details: Optional[str] = None


class DockerContainerInfo(BaseModel):
    container_id: str
    name: str
    image: str
    status: str
    ports: Dict[str, str]
    labels: Dict[str, str]
    created: datetime
    network_settings: Dict[str, Any] = Field(default_factory=dict)
    service_name: Optional[str] = None
    is_virtual: bool = False


class ServiceCatalogEntry(BaseModel):
    service_name: str
    base_url: str
    container_name: str
    routes: List[str]
    healthcheck: str
    port: int
    description: str


class HealthSummary(BaseModel):
    total_services: int
    healthy_services: int
    unhealthy_services: int
    unknown_services: int
    virtual_services: int
    services: List[ServiceEndpointMap]
    last_updated: datetime
    cache_status: str
    discovery_stats: Dict[str, Any] = Field(default_factory=dict)


class DiscoveryResult(BaseModel):
    service_name: str
    discovery_method: DiscoveryMethod
    endpoints_found: int
    endpoints: List[EndpointInfo]
    health_status: ServiceStatus
    health_check_result: Optional[HealthCheckResult] = None
    error: Optional[str] = None
    catalog_used: bool = False


class ServiceDiscoveryConfig(BaseModel):
    docker_network: str = "reqarchitect-network"
    service_label: str = "reqarchitect-service=true"
    service_name_label: str = "service-name"
    cache_ttl_seconds: int = 300  # 5 minutes
    health_check_timeout: int = 5
    endpoint_discovery_timeout: int = 10
    max_retries: int = 3
    enable_catalog_fallback: bool = True
    enable_network_scan: bool = True
    enable_virtual_containers: bool = True
    health_check_endpoints: List[str] = Field(default_factory=lambda: ["/health", "/healthz", "/ping", "/"])
    catalog_file_path: str = "app/service_catalog.json"


class NetworkInfo(BaseModel):
    network_id: str
    network_name: str
    driver: str
    ipam_config: List[Dict[str, Any]] = Field(default_factory=list)
    container_count: int
    containers: List[str] = Field(default_factory=list)


class DiscoveryStats(BaseModel):
    total_containers_discovered: int
    labeled_containers: int
    catalog_containers: int
    network_containers: int
    virtual_containers: int
    healthy_containers: int
    unhealthy_containers: int
    unknown_containers: int
    discovery_methods_used: List[DiscoveryMethod] = Field(default_factory=list)
    catalog_services_available: int
    catalog_fallback_enabled: bool
    docker_client_available: bool
    last_discovery_time: datetime
    discovery_duration_seconds: float
    errors_encountered: List[str] = Field(default_factory=list)


class ServiceDetails(BaseModel):
    service: ServiceEndpointMap
    container_logs: List[str] = Field(default_factory=list)
    network_info: Optional[NetworkInfo] = None
    cache_stats: Dict[str, Any] = Field(default_factory=dict)
    discovery_info: Dict[str, Any] = Field(default_factory=dict)
    health_history: List[HealthCheckResult] = Field(default_factory=list)


class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    service: str = "api_debug_service"
    version: str = "1.0.0"


class ServiceFilter(BaseModel):
    status: Optional[ServiceStatus] = None
    discovery_method: Optional[DiscoveryMethod] = None
    is_virtual: Optional[bool] = None
    has_health_check: Optional[bool] = None
    service_name_contains: Optional[str] = None


class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 100
    sort_by: str = "service_name"
    sort_order: str = "asc"


class ServiceSearchParams(BaseModel):
    query: str
    search_fields: List[str] = Field(default_factory=lambda: ["service_name", "description", "image"])
    case_sensitive: bool = False
    use_regex: bool = False


class HealthCheckConfig(BaseModel):
    timeout_seconds: int = 5
    retry_count: int = 2
    retry_delay_seconds: float = 1.0
    success_status_codes: List[int] = Field(default_factory=lambda: [200, 404, 405])
    health_endpoints: List[str] = Field(default_factory=lambda: ["/health", "/healthz", "/ping", "/"])
    enable_ssl_verification: bool = False
    user_agent: str = "ReqArchitect-API-Debug/1.0"


class CacheConfig(BaseModel):
    ttl_seconds: int = 300
    max_size: int = 1000
    enable_compression: bool = True
    cache_health_results: bool = True
    cache_discovery_results: bool = True
    cache_service_details: bool = True


class LoggingConfig(BaseModel):
    level: str = "INFO"
    format: str = "json"
    include_timestamps: bool = True
    include_service_name: bool = True
    include_request_id: bool = True
    log_discovery_events: bool = True
    log_health_checks: bool = False
    log_cache_operations: bool = False 