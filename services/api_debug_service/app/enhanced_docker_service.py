import docker
import json
import logging
import os
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
from pathlib import Path
import httpx
import asyncio
from .models import DockerContainerInfo, ServiceDiscoveryConfig

logger = logging.getLogger(__name__)


class EnhancedDockerService:
    """Enhanced Docker service with label-based detection and fallback catalog."""
    
    def __init__(self, config: ServiceDiscoveryConfig):
        self.config = config
        self.client = None
        self.service_catalog = self._load_service_catalog()
        self.enable_catalog_fallback = os.getenv('ENABLE_CATALOG_FALLBACK', 'true').lower() == 'true'
        self._init_docker_client()
    
    def _init_docker_client(self):
        """Initialize Docker client with error handling."""
        try:
            # Use explicit Unix socket connection for Docker
            self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
            # Test connection
            self.client.ping()
            logger.info("Docker client initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize Docker client: {e}")
            self.client = None
    
    def _load_service_catalog(self) -> List[Dict]:
        """Load fallback service catalog from JSON file."""
        try:
            catalog_path = Path(__file__).parent / "service_catalog.json"
            if catalog_path.exists():
                with open(catalog_path, 'r') as f:
                    catalog = json.load(f)
                logger.info(f"Loaded service catalog with {len(catalog)} services")
                return catalog
            else:
                logger.warning("Service catalog not found, will use label-based discovery only")
                return []
        except Exception as e:
            logger.error(f"Error loading service catalog: {e}")
            return []
    
    def get_reqarchitect_containers(self) -> List[DockerContainerInfo]:
        """Get all ReqArchitect service containers using label-based detection."""
        if not self.client:
            logger.warning("Docker client not available")
            return []
        
        try:
            containers = []
            
            # Method 1: Label-based discovery
            labeled_containers = self._discover_labeled_containers()
            containers.extend(labeled_containers)
            
            # Method 2: Catalog-based discovery (if enabled)
            if self.enable_catalog_fallback:
                catalog_containers = self._discover_catalog_containers(labeled_containers)
                containers.extend(catalog_containers)
            
            # Method 3: Network-based discovery
            network_containers = self._discover_network_containers(containers)
            containers.extend(network_containers)
            
            # Remove duplicates based on service_name
            unique_containers = self._deduplicate_containers(containers)
            
            logger.info(f"Discovered {len(unique_containers)} unique ReqArchitect containers")
            return unique_containers
            
        except Exception as e:
            logger.error(f"Error getting containers: {e}")
            return []
    
    def _discover_labeled_containers(self) -> List[DockerContainerInfo]:
        """Discover containers using label-based detection."""
        containers = []
        
        try:
            # Look for containers with reqarchitect-service label
            labeled_containers = self.client.containers.list(
                filters={
                    "label": "reqarchitect-service=true",
                    "status": "running"
                }
            )
            
            for container in labeled_containers:
                try:
                    container_info = self._extract_container_info(container)
                    if container_info:
                        containers.append(container_info)
                        logger.debug(f"Discovered labeled container: {container_info.service_name}")
                except Exception as e:
                    logger.error(f"Error processing labeled container {container.id}: {e}")
                    continue
            
            logger.info(f"Label-based discovery found {len(containers)} containers")
            return containers
            
        except Exception as e:
            logger.error(f"Error in label-based discovery: {e}")
            return []
    
    def _discover_catalog_containers(self, existing_containers: List[DockerContainerInfo]) -> List[DockerContainerInfo]:
        """Discover containers using service catalog fallback."""
        containers = []
        existing_service_names = {c.service_name for c in existing_containers}
        
        try:
            for catalog_entry in self.service_catalog:
                service_name = catalog_entry.get("service_name")
                
                # Skip if already discovered via labels
                if service_name in existing_service_names:
                    continue
                
                # Try to find container by name
                container = self._find_container_by_name(catalog_entry.get("container_name", service_name))
                
                if container:
                    try:
                        container_info = self._extract_container_info(container, catalog_entry)
                        if container_info:
                            containers.append(container_info)
                            logger.debug(f"Discovered catalog container: {container_info.service_name}")
                    except Exception as e:
                        logger.error(f"Error processing catalog container {service_name}: {e}")
                        continue
                else:
                    # Create virtual container info from catalog
                    virtual_container = self._create_virtual_container_info(catalog_entry)
                    if virtual_container:
                        containers.append(virtual_container)
                        logger.debug(f"Created virtual container from catalog: {service_name}")
            
            logger.info(f"Catalog-based discovery found {len(containers)} additional containers")
            return containers
            
        except Exception as e:
            logger.error(f"Error in catalog-based discovery: {e}")
            return []
    
    def _discover_network_containers(self, existing_containers: List[DockerContainerInfo]) -> List[DockerContainerInfo]:
        """Discover containers by scanning Docker network."""
        containers = []
        existing_service_names = {c.service_name for c in existing_containers}
        
        try:
            # Get all running containers
            all_containers = self.client.containers.list(filters={"status": "running"})
            
            for container in all_containers:
                try:
                    # Skip if already discovered
                    container_name = container.name.lstrip("/")
                    if container_name in existing_service_names:
                        continue
                    
                    # Check if container name matches ReqArchitect pattern
                    if self._is_reqarchitect_container(container):
                        container_info = self._extract_container_info(container)
                        if container_info:
                            containers.append(container_info)
                            logger.debug(f"Discovered network container: {container_info.service_name}")
                
                except Exception as e:
                    logger.error(f"Error processing network container {container.id}: {e}")
                    continue
            
            logger.info(f"Network-based discovery found {len(containers)} additional containers")
            return containers
            
        except Exception as e:
            logger.error(f"Error in network-based discovery: {e}")
            return []
    
    def _is_reqarchitect_container(self, container) -> bool:
        """Check if container appears to be a ReqArchitect service."""
        try:
            # Check container name pattern
            container_name = container.name.lstrip("/")
            reqarchitect_patterns = [
                "_service", "service_", "reqarchitect", "reqfastapi"
            ]
            
            if any(pattern in container_name.lower() for pattern in reqarchitect_patterns):
                return True
            
            # Check image name
            image_name = container.image.lower()
            if any(pattern in image_name for pattern in reqarchitect_patterns):
                return True
            
            # Check labels
            labels = container.attrs.get("Config", {}).get("Labels", {})
            if "reqarchitect" in str(labels).lower():
                return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking if container is ReqArchitect: {e}")
            return False
    
    def _find_container_by_name(self, container_name: str):
        """Find container by name."""
        try:
            containers = self.client.containers.list(
                filters={"name": container_name, "status": "running"}
            )
            return containers[0] if containers else None
        except Exception as e:
            logger.debug(f"Error finding container by name {container_name}: {e}")
            return None
    
    def _extract_container_info(self, container, catalog_entry: Optional[Dict] = None) -> Optional[DockerContainerInfo]:
        """Extract container information."""
        try:
            container_info = container.attrs
            
            # Extract service name from labels or catalog
            service_name = self._extract_service_name(container, catalog_entry)
            if not service_name:
                return None
            
            # Extract port mappings
            ports = self._extract_port_mappings(container_info, catalog_entry)
            
            # Extract labels
            labels = container_info.get("Config", {}).get("Labels", {})
            
            # Parse creation date
            created_str = container_info.get("Created", "")
            created = datetime.fromisoformat(created_str.replace("Z", "+00:00")) if created_str else datetime.now()
            
            # Get network settings
            network_settings = container_info.get("NetworkSettings", {})
            
            container_info_obj = DockerContainerInfo(
                container_id=container.id,
                name=container.name,
                image=container_info.get("Config", {}).get("Image", ""),
                status=container.status,
                ports=ports,
                labels=labels,
                created=created,
                network_settings=network_settings,
                service_name=service_name
            )
            
            return container_info_obj
            
        except Exception as e:
            logger.error(f"Error extracting container info for {container.id}: {e}")
            return None
    
    def _extract_service_name(self, container, catalog_entry: Optional[Dict] = None) -> Optional[str]:
        """Extract service name from container labels or catalog."""
        try:
            # Try to get from labels first
            labels = container.attrs.get("Config", {}).get("Labels", {})
            service_name = labels.get("service-name") or labels.get("com.docker.compose.service")
            
            if service_name:
                return service_name
            
            # Try to extract from container name
            container_name = container.name.lstrip("/")
            if "_service" in container_name:
                return container_name
            
            # Use catalog entry if available
            if catalog_entry:
                return catalog_entry.get("service_name")
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting service name: {e}")
            return None
    
    def _extract_port_mappings(self, container_info: Dict, catalog_entry: Optional[Dict] = None) -> Dict[str, str]:
        """Extract port mappings from container info or catalog."""
        ports = {}
        
        try:
            # Try to get from container network settings
            if "NetworkSettings" in container_info:
                network_settings = container_info["NetworkSettings"]
                if "Ports" in network_settings:
                    for container_port, host_bindings in network_settings["Ports"].items():
                        if host_bindings:
                            for binding in host_bindings:
                                ports[container_port] = f"{binding['HostIp']}:{binding['HostPort']}"
            
            # Fallback to catalog if no ports found
            if not ports and catalog_entry:
                port = catalog_entry.get("port")
                if port:
                    ports[f"{port}/tcp"] = f"0.0.0.0:{port}"
            
            return ports
            
        except Exception as e:
            logger.error(f"Error extracting port mappings: {e}")
            return ports
    
    def _create_virtual_container_info(self, catalog_entry: Dict) -> Optional[DockerContainerInfo]:
        """Create virtual container info from catalog entry."""
        try:
            service_name = catalog_entry.get("service_name")
            container_name = catalog_entry.get("container_name", service_name)
            port = catalog_entry.get("port", 8000)
            
            ports = {f"{port}/tcp": f"0.0.0.0:{port}"}
            
            container_info = DockerContainerInfo(
                container_id=f"virtual_{service_name}",
                name=f"/{container_name}",
                image=f"reqarchitect/{service_name}:latest",
                status="virtual",
                ports=ports,
                labels={"reqarchitect-service": "true", "service-name": service_name},
                created=datetime.now(),
                network_settings={},
                service_name=service_name
            )
            
            return container_info
            
        except Exception as e:
            logger.error(f"Error creating virtual container info: {e}")
            return None
    
    def _deduplicate_containers(self, containers: List[DockerContainerInfo]) -> List[DockerContainerInfo]:
        """Remove duplicate containers based on service_name."""
        seen = set()
        unique_containers = []
        
        for container in containers:
            if container.service_name and container.service_name not in seen:
                seen.add(container.service_name)
                unique_containers.append(container)
        
        return unique_containers
    
    async def check_service_health(self, container_info: DockerContainerInfo, timeout: int = 5) -> Tuple[bool, str]:
        """Check service health by pinging health endpoint."""
        try:
            # Determine base URL
            base_url = self._determine_base_url(container_info)
            if not base_url:
                return False, "No base URL available"
            
            # Try health endpoints
            health_endpoints = ["/health", "/healthz", "/ping", "/"]
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                for endpoint in health_endpoints:
                    try:
                        url = f"{base_url}{endpoint}"
                        response = await client.get(url)
                        
                        if response.status_code in [200, 404, 405]:  # 404/405 means endpoint exists
                            logger.debug(f"Health check passed for {container_info.service_name} at {url}")
                            return True, f"Healthy (status: {response.status_code})"
                    
                    except httpx.TimeoutException:
                        logger.debug(f"Health check timeout for {container_info.service_name} at {endpoint}")
                        continue
                    except Exception as e:
                        logger.debug(f"Health check failed for {container_info.service_name} at {endpoint}: {e}")
                        continue
            
            return False, "No health endpoints responded"
            
        except Exception as e:
            logger.error(f"Error checking health for {container_info.service_name}: {e}")
            return False, f"Health check error: {str(e)}"
    
    def _determine_base_url(self, container_info: DockerContainerInfo) -> Optional[str]:
        """Determine base URL from container info."""
        try:
            # Try to get from port mappings
            for container_port, host_binding in container_info.ports.items():
                if host_binding:
                    if ":" in host_binding:
                        host_port = host_binding.split(":")[-1]
                        return f"http://localhost:{host_port}"
            
            # Try to extract port from container port
            for container_port in container_info.ports.keys():
                if container_port.endswith("/tcp"):
                    port = container_port.replace("/tcp", "")
                    return f"http://localhost:{port}"
            
            # Try to get from network settings
            if container_info.network_settings:
                networks = container_info.network_settings.get("Networks", {})
                for network_name, network_info in networks.items():
                    if network_info.get("IPAddress"):
                        ip = network_info["IPAddress"]
                        # Try common ports
                        for port in [8000, 8080, 8013, 8014, 8015, 8016, 8017, 8018, 8019, 8020, 8021, 8022, 8023]:
                            return f"http://{ip}:{port}"
            
            return None
            
        except Exception as e:
            logger.error(f"Error determining base URL: {e}")
            return None
    
    def get_container_by_service_name(self, service_name: str) -> Optional[DockerContainerInfo]:
        """Get container by service name."""
        containers = self.get_reqarchitect_containers()
        for container in containers:
            if container.service_name == service_name:
                return container
        return None
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get Docker network information."""
        if not self.client:
            return {}
        
        try:
            networks = self.client.networks.list()
            network_info = {}
            
            for network in networks:
                if "reqarchitect" in network.name.lower() or "reqfastapi" in network.name.lower():
                    network_info[network.name] = {
                        "id": network.id,
                        "driver": network.attrs.get("Driver", ""),
                        "ipam_config": network.attrs.get("IPAM", {}).get("Config", []),
                        "containers": len(network.attrs.get("Containers", {}))
                    }
            
            return network_info
            
        except Exception as e:
            logger.error(f"Error getting network info: {e}")
            return {}
    
    def get_discovery_stats(self) -> Dict[str, Any]:
        """Get discovery statistics."""
        try:
            containers = self.get_reqarchitect_containers()
            
            stats = {
                "total_containers": len(containers),
                "labeled_containers": len([c for c in containers if c.labels.get("reqarchitect-service") == "true"]),
                "virtual_containers": len([c for c in containers if c.status == "virtual"]),
                "catalog_services": len(self.service_catalog),
                "catalog_fallback_enabled": self.enable_catalog_fallback,
                "docker_client_available": self.client is not None
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting discovery stats: {e}")
            return {"error": str(e)} 