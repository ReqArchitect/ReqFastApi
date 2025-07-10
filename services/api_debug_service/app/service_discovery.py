import asyncio
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import (
    ServiceEndpointMap, HealthSummary, ServiceStatus, 
    ServiceDiscoveryConfig, EndpointDiscoveryResult
)
from .docker_service import DockerService
from .endpoint_discovery import EndpointDiscoveryService
from .cache_service import CacheService

logger = logging.getLogger(__name__)


class ServiceDiscoveryOrchestrator:
    """Main orchestrator for service discovery and endpoint mapping."""
    
    def __init__(self, config: ServiceDiscoveryConfig):
        self.config = config
        self.docker_service = DockerService(config)
        self.endpoint_discovery = EndpointDiscoveryService(
            timeout=config.endpoint_discovery_timeout,
            max_retries=config.max_retries
        )
        self.cache_service = CacheService(ttl_seconds=config.cache_ttl_seconds)
    
    async def discover_all_services(self, use_cache: bool = True) -> List[ServiceEndpointMap]:
        """Discover all ReqArchitect services and their endpoints."""
        # Try cache first
        if use_cache:
            cached_services = self.cache_service.get_cached_all_services()
            if cached_services:
                logger.info("Using cached service data")
                return cached_services
        
        # Discover from Docker
        containers = self.docker_service.get_reqarchitect_containers()
        services = []
        
        for container in containers:
            try:
                service_map = await self._create_service_map_from_container(container)
                if service_map:
                    services.append(service_map)
            except Exception as e:
                logger.error(f"Error processing container {container.name}: {e}")
                continue
        
        # Cache the results
        if services:
            self.cache_service.cache_all_services(services)
        
        logger.info(f"Discovered {len(services)} services")
        return services
    
    async def discover_service(self, service_name: str, use_cache: bool = True) -> Optional[ServiceEndpointMap]:
        """Discover a specific service by name."""
        # Try cache first
        if use_cache:
            cached_services = self.cache_service.get_cached_service_endpoints(service_name)
            if cached_services:
                logger.info(f"Using cached data for {service_name}")
                return cached_services[0] if cached_services else None
        
        # Find container for service
        container = self.docker_service.get_container_by_name(service_name)
        if not container:
            logger.warning(f"Container not found for service: {service_name}")
            return None
        
        # Create service map
        service_map = await self._create_service_map_from_container(container)
        if service_map:
            # Cache the result
            self.cache_service.cache_service_endpoints(service_name, [service_map])
        
        return service_map
    
    async def _create_service_map_from_container(self, container) -> Optional[ServiceEndpointMap]:
        """Create ServiceEndpointMap from Docker container info."""
        try:
            # Extract service name from container name
            service_name = container.name.lstrip("/").replace("-", "_")
            
            # Determine base URL from port mappings
            base_url = self._determine_base_url(container)
            if not base_url:
                logger.warning(f"Could not determine base URL for {service_name}")
                return None
            
            # Check container health
            is_healthy = self.docker_service.get_container_health(container.container_id)
            status = ServiceStatus.HEALTHY if is_healthy else ServiceStatus.UNHEALTHY
            
            # Discover endpoints
            discovery_result = await self.endpoint_discovery.discover_endpoints_from_service(
                base_url, service_name
            )
            
            # Create service map
            service_map = ServiceEndpointMap(
                service_name=service_name,
                docker_container_name=container.name,
                base_url=base_url,
                status=status,
                available_endpoints=discovery_result.endpoints,
                last_heartbeat=datetime.now(),
                version_tag=container.image.split(":")[-1] if ":" in container.image else None,
                port=self._extract_port(container),
                container_id=container.container_id,
                image=container.image,
                labels=container.labels
            )
            
            logger.info(f"Created service map for {service_name} with {len(discovery_result.endpoints)} endpoints")
            return service_map
            
        except Exception as e:
            logger.error(f"Error creating service map for container {container.name}: {e}")
            return None
    
    def _determine_base_url(self, container) -> Optional[str]:
        """Determine base URL from container port mappings."""
        try:
            # Look for exposed ports
            for container_port, host_binding in container.ports.items():
                if host_binding:
                    # Extract port from binding (e.g., "0.0.0.0:8080" -> "8080")
                    if ":" in host_binding:
                        host_port = host_binding.split(":")[-1]
                        return f"http://localhost:{host_port}"
            
            # Fallback: try to extract port from container port
            for container_port in container.ports.keys():
                if container_port.endswith("/tcp"):
                    port = container_port.replace("/tcp", "")
                    return f"http://localhost:{port}"
            
            return None
            
        except Exception as e:
            logger.error(f"Error determining base URL: {e}")
            return None
    
    def _extract_port(self, container) -> Optional[int]:
        """Extract port number from container."""
        try:
            for container_port in container.ports.keys():
                if container_port.endswith("/tcp"):
                    return int(container_port.replace("/tcp", ""))
            return None
        except Exception:
            return None
    
    async def get_health_summary(self, use_cache: bool = True) -> HealthSummary:
        """Get comprehensive health summary of all services."""
        # Try cache first
        if use_cache:
            cached_summary = self.cache_service.get_cached_health_summary()
            if cached_summary:
                logger.info("Using cached health summary")
                return cached_summary
        
        # Get all services
        services = await self.discover_all_services(use_cache=False)
        
        # Calculate health metrics
        total_services = len(services)
        healthy_services = len([s for s in services if s.status == ServiceStatus.HEALTHY])
        unhealthy_services = len([s for s in services if s.status == ServiceStatus.UNHEALTHY])
        unknown_services = len([s for s in services if s.status == ServiceStatus.UNKNOWN])
        
        # Create summary
        summary = HealthSummary(
            total_services=total_services,
            healthy_services=healthy_services,
            unhealthy_services=unhealthy_services,
            unknown_services=unknown_services,
            services=services,
            last_updated=datetime.now(),
            cache_status="fresh"
        )
        
        # Cache the summary
        self.cache_service.cache_health_summary(summary)
        
        logger.info(f"Health summary: {healthy_services}/{total_services} healthy services")
        return summary
    
    async def get_service_details(self, service_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific service."""
        service_map = await self.discover_service(service_name)
        if not service_map:
            return None
        
        # Get container logs
        logs = self.docker_service.get_container_logs(service_map.container_id, tail=20)
        
        # Get network info
        network_info = self.docker_service.get_network_info()
        
        return {
            "service": service_map.dict(),
            "logs": logs,
            "network_info": network_info,
            "cache_stats": self.cache_service.get_cache_stats()
        }
    
    async def refresh_cache(self) -> bool:
        """Force refresh of all cached data."""
        try:
            # Invalidate cache
            self.cache_service.invalidate_cache()
            
            # Re-discover services
            await self.discover_all_services(use_cache=False)
            await self.get_health_summary(use_cache=False)
            
            logger.info("Cache refreshed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error refreshing cache: {e}")
            return False
    
    def get_discovery_stats(self) -> Dict[str, Any]:
        """Get discovery service statistics."""
        cache_stats = self.cache_service.get_cache_stats()
        network_info = self.docker_service.get_network_info()
        
        return {
            "cache": cache_stats,
            "network": network_info,
            "config": self.config.dict(),
            "discovery_methods": [
                "swagger_openapi",
                "api_reference_md", 
                "known_patterns",
                "health_endpoint"
            ]
        } 