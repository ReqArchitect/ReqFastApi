import docker
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
from .models import DockerContainerInfo, ServiceDiscoveryConfig

logger = logging.getLogger(__name__)


class DockerService:
    """Service for safely inspecting Docker containers without modification."""
    
    def __init__(self, config: ServiceDiscoveryConfig):
        self.config = config
        self.client = None
        self._init_docker_client()
    
    def _init_docker_client(self):
        """Initialize Docker client with error handling."""
        try:
            self.client = docker.from_env()
            # Test connection
            self.client.ping()
            logger.info("Docker client initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize Docker client: {e}")
            self.client = None
    
    def get_reqarchitect_containers(self) -> List[DockerContainerInfo]:
        """Get all ReqArchitect service containers without modification."""
        if not self.client:
            logger.warning("Docker client not available")
            return []
        
        try:
            containers = []
            for container in self.client.containers.list(
                filters={
                    "label": self.config.service_label,
                    "status": "running"
                }
            ):
                try:
                    # Get container info without modifying it
                    container_info = container.attrs
                    
                    # Extract port mappings
                    ports = {}
                    if "NetworkSettings" in container_info:
                        network_settings = container_info["NetworkSettings"]
                        if "Ports" in network_settings:
                            for container_port, host_bindings in network_settings["Ports"].items():
                                if host_bindings:
                                    for binding in host_bindings:
                                        ports[container_port] = f"{binding['HostIp']}:{binding['HostPort']}"
                    
                    # Extract labels
                    labels = container_info.get("Config", {}).get("Labels", {})
                    
                    # Parse creation date
                    created_str = container_info.get("Created", "")
                    created = datetime.fromisoformat(created_str.replace("Z", "+00:00")) if created_str else datetime.now()
                    
                    container_info_obj = DockerContainerInfo(
                        container_id=container.id,
                        name=container.name,
                        image=container_info.get("Config", {}).get("Image", ""),
                        status=container.status,
                        ports=ports,
                        labels=labels,
                        created=created,
                        network_settings=container_info.get("NetworkSettings", {})
                    )
                    containers.append(container_info_obj)
                    
                except Exception as e:
                    logger.error(f"Error processing container {container.id}: {e}")
                    continue
            
            logger.info(f"Found {len(containers)} ReqArchitect containers")
            return containers
            
        except Exception as e:
            logger.error(f"Error getting containers: {e}")
            return []
    
    def get_container_by_name(self, container_name: str) -> Optional[DockerContainerInfo]:
        """Get specific container by name."""
        containers = self.get_reqarchitect_containers()
        for container in containers:
            if container.name == container_name or container.name == f"/{container_name}":
                return container
        return None
    
    def get_container_health(self, container_id: str) -> bool:
        """Check if container is healthy without modification."""
        if not self.client:
            return False
        
        try:
            container = self.client.containers.get(container_id)
            # Check container state without restarting or modifying
            state = container.attrs.get("State", {})
            return state.get("Status") == "running" and state.get("Health", {}).get("Status") != "unhealthy"
        except Exception as e:
            logger.error(f"Error checking container health for {container_id}: {e}")
            return False
    
    def get_container_logs(self, container_id: str, tail: int = 10) -> List[str]:
        """Get recent container logs without modification."""
        if not self.client:
            return []
        
        try:
            container = self.client.containers.get(container_id)
            logs = container.logs(tail=tail, timestamps=True).decode("utf-8")
            return logs.split("\n") if logs else []
        except Exception as e:
            logger.error(f"Error getting logs for container {container_id}: {e}")
            return []
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get Docker network information."""
        if not self.client:
            return {}
        
        try:
            networks = self.client.networks.list(names=[self.config.docker_network])
            if networks:
                network = networks[0]
                return {
                    "id": network.id,
                    "name": network.name,
                    "driver": network.attrs.get("Driver", ""),
                    "ipam_config": network.attrs.get("IPAM", {}).get("Config", []),
                    "containers": len(network.attrs.get("Containers", {}))
                }
            return {}
        except Exception as e:
            logger.error(f"Error getting network info: {e}")
            return {} 