import json
import logging
from typing import List, Dict, Optional, Any
from pathlib import Path
from .enhanced_models import ServiceCatalogEntry

logger = logging.getLogger(__name__)


class ServiceCatalog:
    """Service catalog manager for fallback service discovery."""
    
    def __init__(self, catalog_file_path: str = "app/service_catalog.json"):
        self.catalog_file_path = Path(catalog_file_path)
        self.catalog_data = []
        self._load_catalog()
    
    def _load_catalog(self):
        """Load service catalog from JSON file."""
        try:
            if self.catalog_file_path.exists():
                with open(self.catalog_file_path, 'r') as f:
                    self.catalog_data = json.load(f)
                logger.info(f"Loaded service catalog with {len(self.catalog_data)} services")
            else:
                logger.warning(f"Service catalog not found at {self.catalog_file_path}")
                self.catalog_data = []
        except Exception as e:
            logger.error(f"Error loading service catalog: {e}")
            self.catalog_data = []
    
    def get_all_services(self) -> List[Dict[str, Any]]:
        """Get all services from catalog."""
        return self.catalog_data.copy()
    
    def get_service(self, service_name: str) -> Optional[Dict[str, Any]]:
        """Get specific service by name."""
        for service in self.catalog_data:
            if service.get("service_name") == service_name:
                return service
        return None
    
    def get_service_by_container_name(self, container_name: str) -> Optional[Dict[str, Any]]:
        """Get service by container name."""
        for service in self.catalog_data:
            if service.get("container_name") == container_name:
                return service
        return None
    
    def get_services_by_port(self, port: int) -> List[Dict[str, Any]]:
        """Get services by port number."""
        return [service for service in self.catalog_data if service.get("port") == port]
    
    def get_service_names(self) -> List[str]:
        """Get list of all service names."""
        return [service.get("service_name") for service in self.catalog_data if service.get("service_name")]
    
    def get_container_names(self) -> List[str]:
        """Get list of all container names."""
        return [service.get("container_name") for service in self.catalog_data if service.get("container_name")]
    
    def get_ports(self) -> List[int]:
        """Get list of all ports."""
        return [service.get("port") for service in self.catalog_data if service.get("port")]
    
    def search_services(self, query: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """Search services by name, description, or container name."""
        results = []
        query_lower = query if case_sensitive else query.lower()
        
        for service in self.catalog_data:
            service_name = service.get("service_name", "")
            description = service.get("description", "")
            container_name = service.get("container_name", "")
            
            if not case_sensitive:
                service_name = service_name.lower()
                description = description.lower()
                container_name = container_name.lower()
            
            if (query_lower in service_name or 
                query_lower in description or 
                query_lower in container_name):
                results.append(service)
        
        return results
    
    def get_service_routes(self, service_name: str) -> List[str]:
        """Get routes for a specific service."""
        service = self.get_service(service_name)
        if service:
            return service.get("routes", [])
        return []
    
    def get_health_check_endpoint(self, service_name: str) -> Optional[str]:
        """Get health check endpoint for a specific service."""
        service = self.get_service(service_name)
        if service:
            return service.get("healthcheck")
        return None
    
    def get_service_base_url(self, service_name: str) -> Optional[str]:
        """Get base URL for a specific service."""
        service = self.get_service(service_name)
        if service:
            return service.get("base_url")
        return None
    
    def get_service_port(self, service_name: str) -> Optional[int]:
        """Get port for a specific service."""
        service = self.get_service(service_name)
        if service:
            return service.get("port")
        return None
    
    def is_service_in_catalog(self, service_name: str) -> bool:
        """Check if service exists in catalog."""
        return self.get_service(service_name) is not None
    
    def get_catalog_stats(self) -> Dict[str, Any]:
        """Get catalog statistics."""
        return {
            "total_services": len(self.catalog_data),
            "service_names": self.get_service_names(),
            "container_names": self.get_container_names(),
            "ports": self.get_ports(),
            "catalog_file_path": str(self.catalog_file_path),
            "catalog_file_exists": self.catalog_file_path.exists()
        }
    
    def reload_catalog(self) -> bool:
        """Reload catalog from file."""
        try:
            self._load_catalog()
            return True
        except Exception as e:
            logger.error(f"Error reloading catalog: {e}")
            return False
    
    def validate_catalog(self) -> Dict[str, Any]:
        """Validate catalog data structure."""
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "validated_services": 0
        }
        
        for i, service in enumerate(self.catalog_data):
            try:
                # Check required fields
                if not service.get("service_name"):
                    validation_results["errors"].append(f"Service {i}: Missing service_name")
                    validation_results["valid"] = False
                
                if not service.get("base_url"):
                    validation_results["warnings"].append(f"Service {service.get('service_name', f'index_{i}')}: Missing base_url")
                
                if not service.get("routes"):
                    validation_results["warnings"].append(f"Service {service.get('service_name', f'index_{i}')}: No routes defined")
                
                if not service.get("healthcheck"):
                    validation_results["warnings"].append(f"Service {service.get('service_name', f'index_{i}')}: No healthcheck endpoint")
                
                validation_results["validated_services"] += 1
                
            except Exception as e:
                validation_results["errors"].append(f"Service {i}: Validation error - {e}")
                validation_results["valid"] = False
        
        return validation_results
    
    def export_catalog(self, format: str = "json") -> str:
        """Export catalog in specified format."""
        if format.lower() == "json":
            return json.dumps(self.catalog_data, indent=2)
        elif format.lower() == "yaml":
            import yaml
            return yaml.dump(self.catalog_data, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_service_summary(self) -> List[Dict[str, Any]]:
        """Get summary of all services."""
        summary = []
        for service in self.catalog_data:
            summary.append({
                "service_name": service.get("service_name"),
                "container_name": service.get("container_name"),
                "port": service.get("port"),
                "base_url": service.get("base_url"),
                "route_count": len(service.get("routes", [])),
                "has_healthcheck": bool(service.get("healthcheck")),
                "description": service.get("description", "")
            })
        return summary
    
    def filter_services(self, **filters) -> List[Dict[str, Any]]:
        """Filter services by various criteria."""
        filtered_services = []
        
        for service in self.catalog_data:
            match = True
            
            for key, value in filters.items():
                if key in service:
                    if isinstance(value, (list, tuple)):
                        if service[key] not in value:
                            match = False
                            break
                    else:
                        if service[key] != value:
                            match = False
                            break
                else:
                    match = False
                    break
            
            if match:
                filtered_services.append(service)
        
        return filtered_services
    
    def get_services_by_pattern(self, pattern: str, field: str = "service_name") -> List[Dict[str, Any]]:
        """Get services matching a pattern in a specific field."""
        import re
        matching_services = []
        
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            for service in self.catalog_data:
                if field in service and regex.search(str(service[field])):
                    matching_services.append(service)
        except re.error as e:
            logger.error(f"Invalid regex pattern '{pattern}': {e}")
        
        return matching_services 