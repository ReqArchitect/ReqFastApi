import logging
from typing import Optional, Tuple
from app.service_registry import service_registry

logger = logging.getLogger(__name__)

def resolve_service(path: str) -> Optional[str]:
    """
    Resolve service URL using service registry with health checks.
    
    Args:
        path: Request path (e.g., "/assessment/assessments")
        
    Returns:
        Service URL if healthy service found, None otherwise
    """
    # Find service by path
    service_info = service_registry.get_service_by_path(path)
    if not service_info:
        logger.warning(f"No service found for path: {path}")
        return None
    
    service_key, config = service_info
    
    # Check if service is healthy
    if not service_registry.is_service_healthy(service_key):
        logger.warning(f"Service {service_key} is unhealthy, circuit breaker may be open")
        return None
    
    # Return internal URL
    return config.internal_url

def get_service_config(path: str) -> Optional[Tuple[str, any]]:
    """
    Get service configuration by path.
    
    Args:
        path: Request path
        
    Returns:
        Tuple of (service_key, config) if found, None otherwise
    """
    return service_registry.get_service_by_path(path)

def is_service_healthy(service_key: str) -> bool:
    """
    Check if service is healthy.
    
    Args:
        service_key: Service identifier
        
    Returns:
        True if service is healthy, False otherwise
    """
    return service_registry.is_service_healthy(service_key)

def get_service_health_summary() -> dict:
    """
    Get health summary for all services.
    
    Returns:
        Dictionary with health status for all services
    """
    return service_registry.get_health_summary()

def get_service_metrics() -> dict:
    """
    Get service metrics for monitoring.
    
    Returns:
        Dictionary with service metrics
    """
    return service_registry.get_service_metrics()
