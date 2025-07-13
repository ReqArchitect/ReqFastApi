from fastapi import FastAPI, HTTPException, Depends, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import structlog
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio
import os

from .enhanced_models import (
    ServiceEndpointMap, HealthSummary, ServiceStatus, DiscoveryMethod,
    ServiceFilter, PaginationParams, APIResponse, ServiceDetails,
    DiscoveryStats, HealthCheckConfig
)
from .enhanced_docker_service import EnhancedDockerService
from .enhanced_endpoint_discovery import EnhancedEndpointDiscoveryService
from .cache_service import CacheService
from .service_catalog import ServiceCatalog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="Enhanced API Debug Service",
    description="Non-intrusive service for discovering and visualizing API endpoints across ReqArchitect microservices with enhanced discovery methods",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
from .enhanced_models import ServiceDiscoveryConfig
config = ServiceDiscoveryConfig()
docker_service = EnhancedDockerService(config)
endpoint_discovery = EnhancedEndpointDiscoveryService(
    timeout=config.endpoint_discovery_timeout,
    max_retries=config.max_retries
)
# Use event_bus Redis service instead of localhost
cache_service = CacheService(redis_url="redis://event_bus:6379", ttl_seconds=config.cache_ttl_seconds)
service_catalog = ServiceCatalog()

# Configuration for fallback discovery
ENABLE_CATALOG_FALLBACK = os.getenv("ENABLE_CATALOG_FALLBACK", "true").lower() == "true"


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Enhanced API Debug Service starting up")
    logger.info(f"Configuration: {config.dict()}")
    logger.info(f"Catalog fallback enabled: {ENABLE_CATALOG_FALLBACK}")
    
    # Validate service catalog
    catalog_validation = service_catalog.validate_catalog()
    if not catalog_validation["valid"]:
        logger.warning(f"Service catalog validation issues: {catalog_validation['errors']}")
    else:
        logger.info("Service catalog validation passed")
    
    # Pre-load catalog services if fallback is enabled
    if ENABLE_CATALOG_FALLBACK:
        await preload_catalog_services()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Enhanced API Debug Service shutting down")


async def preload_catalog_services():
    """Pre-load catalog services into cache for fallback discovery."""
    try:
        catalog_services = []
        catalog_data = service_catalog.get_all_services()
        
        for catalog_entry in catalog_data:
            service_map = await create_virtual_service_from_catalog(catalog_entry)
            if service_map:
                catalog_services.append(service_map)
        
        if catalog_services:
            cache_service.cache_all_services(catalog_services)
            logger.info(f"Pre-loaded {len(catalog_services)} catalog services for fallback")
        
    except Exception as e:
        logger.error(f"Error pre-loading catalog services: {e}")


async def create_virtual_service_from_catalog(catalog_entry: Dict[str, Any]) -> Optional[ServiceEndpointMap]:
    """Create a virtual ServiceEndpointMap from catalog entry."""
    try:
        service_name = catalog_entry.get("service_name")
        if not service_name:
            return None
        
        # Create virtual service map
        service_map = ServiceEndpointMap(
            service_name=service_name,
            docker_container_name=catalog_entry.get("container_name"),
            base_url=catalog_entry.get("base_url", f"http://{service_name}:{catalog_entry.get('port', 8000)}"),
            status=ServiceStatus.VIRTUAL,
            discovery_method=DiscoveryMethod.CATALOG_FALLBACK,
            available_endpoints=[
                {
                    "path": route,
                    "method": "GET",
                    "description": f"Route for {service_name}"
                }
                for route in catalog_entry.get("routes", [])
            ],
            health_check=None,  # Virtual services don't have real health checks
            last_heartbeat=datetime.now(),
            version_tag=None,
            port=catalog_entry.get("port"),
            container_id=None,
            image=None,
            labels={},
            network_info={},
            catalog_entry=catalog_entry,
            is_virtual=True,
            error_details=None
        )
        
        logger.info(f"Created virtual service map for {service_name}")
        return service_map
        
    except Exception as e:
        logger.error(f"Error creating virtual service from catalog for {catalog_entry.get('service_name', 'unknown')}: {e}")
        return None


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "enhanced_api_debug_service",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "features": [
            "label_based_discovery",
            "catalog_fallback",
            "network_scan",
            "health_checking",
            "caching"
        ],
        "catalog_fallback_enabled": ENABLE_CATALOG_FALLBACK
    }


@app.get("/metrics", tags=["Monitoring"])
async def get_metrics():
    """Get service metrics and statistics."""
    try:
        docker_stats = docker_service.get_discovery_stats()
        cache_stats = cache_service.get_cache_stats()
        catalog_stats = service_catalog.get_catalog_stats()
        
        return {
            "service": "enhanced_api_debug_service",
            "timestamp": datetime.now().isoformat(),
            "docker_stats": docker_stats,
            "cache_stats": cache_stats,
            "catalog_stats": catalog_stats,
            "catalog_fallback_enabled": ENABLE_CATALOG_FALLBACK
        }
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail="Error getting metrics")


@app.get("/api-debug", tags=["API Debug"], response_model=List[ServiceEndpointMap])
async def get_all_service_endpoints(
    use_cache: bool = Query(True, description="Use cached data if available"),
    refresh: bool = Query(False, description="Force refresh cache"),
    filter_status: Optional[ServiceStatus] = Query(None, description="Filter by service status"),
    filter_method: Optional[DiscoveryMethod] = Query(None, description="Filter by discovery method"),
    filter_virtual: Optional[bool] = Query(None, description="Filter virtual containers")
):
    """
    Get endpoint map for all ReqArchitect services with enhanced discovery.
    
    Returns a comprehensive list of all discovered services with their endpoints,
    health status, and metadata using multiple discovery methods.
    """
    try:
        if refresh:
            await refresh_cache_internal()
        
        # Get cached data if available
        if use_cache:
            cached_services = cache_service.get_cached_all_services()
            if cached_services:
                logger.info("Using cached service data")
                services = cached_services
            else:
                services = await discover_all_services_internal()
        else:
            services = await discover_all_services_internal()
        
        # Apply filters
        if filter_status:
            services = [s for s in services if s.status == filter_status]
        
        if filter_method:
            services = [s for s in services if s.discovery_method == filter_method]
        
        if filter_virtual is not None:
            services = [s for s in services if s.is_virtual == filter_virtual]
        
        logger.info(f"Retrieved {len(services)} services")
        return services
        
    except Exception as e:
        logger.error(f"Error getting all service endpoints: {e}")
        raise HTTPException(status_code=500, detail="Error discovering services")


@app.get("/api-debug/health-summary", tags=["API Debug"], response_model=HealthSummary)
async def get_health_summary(
    use_cache: bool = Query(True, description="Use cached data if available"),
    refresh: bool = Query(False, description="Force refresh cache")
):
    """
    Get comprehensive health summary of all services.
    
    Returns a summary of service health including counts of healthy/unhealthy
    services and detailed health information for each service.
    """
    try:
        if refresh:
            await refresh_cache_internal()
        
        # Get all services
        if use_cache:
            cached_services = cache_service.get_cached_all_services()
            if cached_services:
                services = cached_services
            else:
                services = await discover_all_services_internal()
        else:
            services = await discover_all_services_internal()
        
        # Calculate health summary
        total_services = len(services)
        healthy_services = len([s for s in services if s.status == ServiceStatus.HEALTHY])
        unhealthy_services = len([s for s in services if s.status == ServiceStatus.UNHEALTHY])
        unknown_services = len([s for s in services if s.status == ServiceStatus.UNKNOWN])
        virtual_services = len([s for s in services if s.is_virtual])
        
        # Get discovery stats
        discovery_stats = {
            "label_based": len([s for s in services if s.discovery_method == DiscoveryMethod.LABEL_BASED]),
            "catalog_fallback": len([s for s in services if s.discovery_method == DiscoveryMethod.CATALOG_FALLBACK]),
            "network_scan": len([s for s in services if s.discovery_method == DiscoveryMethod.NETWORK_SCAN]),
            "virtual": virtual_services
        }
        
        health_summary = HealthSummary(
            total_services=total_services,
            healthy_services=healthy_services,
            unhealthy_services=unhealthy_services,
            unknown_services=unknown_services,
            virtual_services=virtual_services,
            services=services,
            last_updated=datetime.now(),
            cache_status="hit" if use_cache and cached_services else "miss",
            discovery_stats=discovery_stats
        )
        
        logger.info(f"Health summary: {healthy_services}/{total_services} healthy services")
        return health_summary
        
    except Exception as e:
        logger.error(f"Error getting health summary: {e}")
        raise HTTPException(status_code=500, detail="Error getting health summary")


@app.get("/api-debug/catalog", tags=["API Debug"])
async def get_service_catalog():
    """
    Get the service catalog data.
    
    Returns the complete service catalog used for fallback discovery.
    """
    try:
        catalog_data = service_catalog.get_all_services()
        catalog_stats = service_catalog.get_catalog_stats()
        
        return {
            "catalog_services": catalog_data,
            "catalog_stats": catalog_stats,
            "total_services": len(catalog_data),
            "catalog_fallback_enabled": ENABLE_CATALOG_FALLBACK,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting service catalog: {e}")
        raise HTTPException(status_code=500, detail="Error getting service catalog")


@app.get("/api-debug/stats", tags=["API Debug"])
async def get_discovery_stats():
    """
    Get discovery service statistics.
    
    Returns detailed statistics about the discovery service including
    cache information, network details, and configuration.
    """
    try:
        docker_stats = docker_service.get_discovery_stats()
        cache_stats = cache_service.get_cache_stats()
        catalog_stats = service_catalog.get_catalog_stats()
        
        return {
            "service": "enhanced_api_debug_service",
            "timestamp": datetime.now().isoformat(),
            "configuration": {
                "catalog_fallback_enabled": ENABLE_CATALOG_FALLBACK,
                "cache_ttl_seconds": config.cache_ttl_seconds,
                "endpoint_discovery_timeout": config.endpoint_discovery_timeout,
                "max_retries": config.max_retries
            },
            "docker_stats": docker_stats,
            "cache_stats": cache_stats,
            "catalog_stats": catalog_stats
        }
    except Exception as e:
        logger.error(f"Error getting discovery stats: {e}")
        raise HTTPException(status_code=500, detail="Error getting discovery stats")


@app.get("/api-debug/services/healthy", tags=["API Debug"], response_model=List[ServiceEndpointMap])
async def get_healthy_services():
    """
    Get only healthy services.
    
    Returns a list of all services that are currently healthy.
    """
    try:
        services = await discover_all_services_internal()
        healthy_services = [s for s in services if s.status == ServiceStatus.HEALTHY]
        
        logger.info(f"Retrieved {len(healthy_services)} healthy services")
        return healthy_services
        
    except Exception as e:
        logger.error(f"Error getting healthy services: {e}")
        raise HTTPException(status_code=500, detail="Error getting healthy services")


@app.get("/api-debug/services/unhealthy", tags=["API Debug"], response_model=List[ServiceEndpointMap])
async def get_unhealthy_services():
    """
    Get only unhealthy services.
    
    Returns a list of all services that are currently unhealthy.
    """
    try:
        services = await discover_all_services_internal()
        unhealthy_services = [s for s in services if s.status == ServiceStatus.UNHEALTHY]
        
        logger.info(f"Retrieved {len(unhealthy_services)} unhealthy services")
        return unhealthy_services
        
    except Exception as e:
        logger.error(f"Error getting unhealthy services: {e}")
        raise HTTPException(status_code=500, detail="Error getting unhealthy services")


@app.get("/api-debug/services/virtual", tags=["API Debug"], response_model=List[ServiceEndpointMap])
async def get_virtual_services():
    """
    Get only virtual services (from catalog fallback).
    
    Returns a list of all virtual services created from the service catalog.
    """
    try:
        services = await discover_all_services_internal()
        virtual_services = [s for s in services if s.is_virtual]
        
        logger.info(f"Retrieved {len(virtual_services)} virtual services")
        return virtual_services
        
    except Exception as e:
        logger.error(f"Error getting virtual services: {e}")
        raise HTTPException(status_code=500, detail="Error getting virtual services")


@app.get("/api-debug/{service_name}", tags=["API Debug"], response_model=ServiceEndpointMap)
async def get_service_endpoints(
    service_name: str = Path(..., description="Name of the service to query"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """
    Get detailed endpoint list for a specific service.
    
    Returns comprehensive information about a specific service including
    all discovered endpoints, health status, and container information.
    """
    try:
        service = await discover_service_internal(service_name, use_cache)
        
        if not service:
            raise HTTPException(
                status_code=404, 
                detail=f"Service '{service_name}' not found or not accessible"
            )
        
        logger.info(f"Retrieved endpoints for service: {service_name}")
        return service
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting service endpoints for {service_name}: {e}")
        raise HTTPException(status_code=500, detail="Error getting service endpoints")


@app.get("/api-debug/{service_name}/details", tags=["API Debug"], response_model=ServiceDetails)
async def get_service_details(
    service_name: str = Path(..., description="Name of the service to query"),
    include_logs: bool = Query(True, description="Include container logs"),
    log_lines: int = Query(20, description="Number of log lines to include")
):
    """
    Get detailed information about a specific service.
    
    Returns comprehensive service information including container details,
    logs, network information, and cache statistics.
    """
    try:
        # Get service
        service = await discover_service_internal(service_name, use_cache=True)
        if not service:
            raise HTTPException(
                status_code=404,
                detail=f"Service '{service_name}' not found or not accessible"
            )
        
        # Get container logs if available and not virtual
        container_logs = []
        if include_logs and not service.is_virtual and service.container_id:
            try:
                logs = docker_service.get_container_logs(service.container_id, tail=log_lines)
                container_logs = logs
            except Exception as e:
                logger.warning(f"Could not get logs for {service_name}: {e}")
        
        # Get network info
        network_info = None
        if service.network_info:
            try:
                network_info = docker_service.get_network_info()
            except Exception as e:
                logger.warning(f"Could not get network info: {e}")
        
        # Get cache stats
        cache_stats = cache_service.get_cache_stats()
        
        # Get discovery info
        discovery_info = {
            "discovery_method": service.discovery_method,
            "is_virtual": service.is_virtual,
            "catalog_entry": service.catalog_entry is not None
        }
        
        # Create service details
        service_details = ServiceDetails(
            service=service,
            container_logs=container_logs,
            network_info=network_info,
            cache_stats=cache_stats,
            discovery_info=discovery_info,
            health_history=[]
        )
        
        logger.info(f"Retrieved detailed information for service: {service_name}")
        return service_details
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting service details for {service_name}: {e}")
        raise HTTPException(status_code=500, detail="Error getting service details")


@app.post("/api-debug/refresh", tags=["API Debug"])
async def refresh_cache():
    """
    Force refresh of all cached data.
    
    Invalidates all cached service discovery data and re-discovers
    all services and their endpoints.
    """
    try:
        success = await refresh_cache_internal()
        if success:
            return {"message": "Cache refreshed successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to refresh cache")
    except Exception as e:
        logger.error(f"Error refreshing cache: {e}")
        raise HTTPException(status_code=500, detail="Error refreshing cache")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


# Internal helper functions
async def discover_all_services_internal() -> List[ServiceEndpointMap]:
    """Internal function to discover all services with guaranteed fallback."""
    start_time = asyncio.get_event_loop().time()
    
    try:
        services = []
        
        # Try Docker-based discovery first
        try:
            containers = docker_service.get_reqarchitect_containers()
            
            # Process each container
            for container in containers:
                try:
                    service_map = await create_service_map_from_container(container)
                    if service_map:
                        services.append(service_map)
                except Exception as e:
                    logger.error(f"Error processing container {container.name}: {e}")
                    continue
            
            logger.info(f"Docker discovery found {len(services)} services")
            
        except Exception as e:
            logger.warning(f"Docker discovery failed: {e}")
        
        # Fallback to catalog if Docker failed or returned no services
        if ENABLE_CATALOG_FALLBACK and (not services or len(services) == 0):
            logger.info("Docker discovery returned no services, using catalog fallback")
            catalog_services = await get_catalog_fallback_services()
            services.extend(catalog_services)
            logger.info(f"Catalog fallback added {len(catalog_services)} services")
        
        # Cache the results
        if services:
            cache_service.cache_all_services(services)
        
        duration = asyncio.get_event_loop().time() - start_time
        logger.info(f"Discovered {len(services)} total services in {duration:.2f} seconds")
        return services
        
    except Exception as e:
        logger.error(f"Error discovering all services: {e}")
        # Return catalog services as last resort
        if ENABLE_CATALOG_FALLBACK:
            return await get_catalog_fallback_services()
        return []


async def get_catalog_fallback_services() -> List[ServiceEndpointMap]:
    """Get services from catalog as fallback."""
    try:
        catalog_services = []
        catalog_data = service_catalog.get_all_services()
        
        for catalog_entry in catalog_data:
            service_map = await create_virtual_service_from_catalog(catalog_entry)
            if service_map:
                catalog_services.append(service_map)
        
        logger.info(f"Created {len(catalog_services)} virtual services from catalog")
        return catalog_services
        
    except Exception as e:
        logger.error(f"Error creating catalog fallback services: {e}")
        return []


async def discover_service_internal(service_name: str, use_cache: bool = True) -> Optional[ServiceEndpointMap]:
    """Internal function to discover a specific service with fallback."""
    try:
        # Try cache first
        if use_cache:
            cached_services = cache_service.get_cached_service_endpoints(service_name)
            if cached_services:
                logger.info(f"Using cached data for {service_name}")
                return cached_services[0] if cached_services else None
        
        # Try Docker-based discovery first
        try:
            container = docker_service.get_container_by_service_name(service_name)
            if container:
                service_map = await create_service_map_from_container(container)
                if service_map:
                    cache_service.cache_service_endpoints(service_name, [service_map])
                    return service_map
        except Exception as e:
            logger.warning(f"Docker discovery failed for {service_name}: {e}")
        
        # Fallback to catalog
        if ENABLE_CATALOG_FALLBACK:
            catalog_entry = service_catalog.get_service(service_name)
            if catalog_entry:
                service_map = await create_virtual_service_from_catalog(catalog_entry)
                if service_map:
                    cache_service.cache_service_endpoints(service_name, [service_map])
                    logger.info(f"Found {service_name} in catalog fallback")
                    return service_map
        
        logger.warning(f"Service {service_name} not found in Docker or catalog")
        return None
        
    except Exception as e:
        logger.error(f"Error discovering service {service_name}: {e}")
        return None


async def create_service_map_from_container(container) -> Optional[ServiceEndpointMap]:
    """Create ServiceEndpointMap from Docker container info."""
    try:
        # Extract service name
        service_name = container.service_name
        if not service_name:
            logger.warning(f"No service name for container {container.name}")
            return None
        
        # Determine base URL
        base_url = docker_service._determine_base_url(container)
        if not base_url:
            logger.warning(f"Could not determine base URL for {service_name}")
            return None
        
        # Check health
        health_result = await docker_service.check_service_health(container, timeout=5)
        status = ServiceStatus.HEALTHY if health_result[0] else ServiceStatus.UNHEALTHY
        
        # Discover endpoints
        discovery_result = await endpoint_discovery.discover_endpoints_from_service(
            base_url, service_name, DiscoveryMethod.LABEL_BASED
        )
        
        # Get catalog entry if available
        catalog_entry = service_catalog.get_service(service_name)
        
        # Create service map
        service_map = ServiceEndpointMap(
            service_name=service_name,
            docker_container_name=container.name,
            base_url=base_url,
            status=status,
            discovery_method=discovery_result.discovery_method,
            available_endpoints=discovery_result.endpoints,
            health_check=await endpoint_discovery.check_service_health(base_url, service_name),
            last_heartbeat=datetime.now(),
            version_tag=container.image.split(":")[-1] if ":" in container.image else None,
            port=docker_service._extract_port(container),
            container_id=container.container_id,
            image=container.image,
            labels=container.labels,
            network_info=container.network_settings,
            catalog_entry=catalog_entry,
            is_virtual=container.is_virtual,
            error_details=discovery_result.error
        )
        
        logger.info(f"Created service map for {service_name} with {len(discovery_result.endpoints)} endpoints")
        return service_map
        
    except Exception as e:
        logger.error(f"Error creating service map for container {container.name}: {e}")
        return None


async def refresh_cache_internal() -> bool:
    """Internal function to refresh cache."""
    try:
        # Invalidate cache
        cache_service.invalidate_cache()
        
        # Re-discover services
        await discover_all_services_internal()
        
        logger.info("Cache refreshed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error refreshing cache: {e}")
        return False


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 