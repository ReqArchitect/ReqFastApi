import json
import asyncio
import httpx
import logging
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ServiceStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
    CIRCUIT_OPEN = "circuit_open"

@dataclass
class ServiceConfig:
    service_name: str
    base_path: str
    internal_url: str
    healthcheck_endpoint: str
    timeout_ms: int
    tenant_scope: str
    cacheable: bool
    retry_policy: Dict[str, Any]
    rbac_required: bool
    rate_limit: Dict[str, int]

@dataclass
class ServiceHealth:
    status: ServiceStatus
    last_check: datetime
    response_time_ms: Optional[float] = None
    error_message: Optional[str] = None
    consecutive_failures: int = 0

class ServiceRegistry:
    """Dynamic service registry with health monitoring and circuit breaker logic"""
    
    def __init__(self, catalog_path: str = "service_catalog.json"):
        self.catalog_path = catalog_path
        self.services: Dict[str, ServiceConfig] = {}
        self.health_status: Dict[str, ServiceHealth] = {}
        self.circuit_breaker_threshold = 5
        self.circuit_breaker_timeout = 30  # seconds
        self.health_check_interval = 60  # seconds
        self._load_catalog()
        self._start_health_monitoring()
    
    def _load_catalog(self):
        """Load service catalog from JSON file"""
        try:
            with open(self.catalog_path, 'r') as f:
                catalog = json.load(f)
            
            # Load gateway config
            gateway_config = catalog.get("gateway_config", {})
            self.circuit_breaker_threshold = gateway_config.get("circuit_breaker_threshold", 5)
            self.circuit_breaker_timeout = gateway_config.get("circuit_breaker_timeout_seconds", 30)
            self.health_check_interval = gateway_config.get("health_check_interval_seconds", 60)
            
            # Load services
            for service_key, service_data in catalog.get("services", {}).items():
                config = ServiceConfig(
                    service_name=service_data["service_name"],
                    base_path=service_data["base_path"],
                    internal_url=service_data["internal_url"],
                    healthcheck_endpoint=service_data["healthcheck_endpoint"],
                    timeout_ms=service_data["timeout_ms"],
                    tenant_scope=service_data["tenant_scope"],
                    cacheable=service_data["cacheable"],
                    retry_policy=service_data["retry_policy"],
                    rbac_required=service_data["rbac_required"],
                    rate_limit=service_data["rate_limit"]
                )
                self.services[service_key] = config
                
                # Initialize health status
                self.health_status[service_key] = ServiceHealth(
                    status=ServiceStatus.UNKNOWN,
                    last_check=datetime.utcnow()
                )
            
            logger.info(f"Loaded {len(self.services)} services from catalog")
            
        except Exception as e:
            logger.error(f"Failed to load service catalog: {e}")
            raise
    
    def get_service_config(self, service_key: str) -> Optional[ServiceConfig]:
        """Get service configuration by key"""
        return self.services.get(service_key)
    
    def get_service_by_path(self, path: str) -> Optional[tuple[str, ServiceConfig]]:
        """Get service configuration by request path"""
        for service_key, config in self.services.items():
            if path.startswith(config.base_path):
                return service_key, config
        return None
    
    def is_service_healthy(self, service_key: str) -> bool:
        """Check if service is healthy and circuit breaker is closed"""
        health = self.health_status.get(service_key)
        if not health:
            return False
        
        # Check circuit breaker
        if health.status == ServiceStatus.CIRCUIT_OPEN:
            # Check if circuit breaker timeout has passed
            if datetime.utcnow() - health.last_check > timedelta(seconds=self.circuit_breaker_timeout):
                # Reset circuit breaker
                health.status = ServiceStatus.UNKNOWN
                health.consecutive_failures = 0
                return True
            return False
        
        return health.status == ServiceStatus.HEALTHY
    
    async def check_service_health(self, service_key: str) -> ServiceHealth:
        """Check health of a specific service"""
        config = self.services.get(service_key)
        if not config:
            return ServiceHealth(
                status=ServiceStatus.UNKNOWN,
                last_check=datetime.utcnow(),
                error_message="Service not found in catalog"
            )
        
        health_url = f"{config.internal_url}{config.healthcheck_endpoint}"
        start_time = datetime.utcnow()
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(health_url)
                response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                if response.status_code == 200:
                    health_data = response.json()
                    if health_data.get("status") == "healthy":
                        return ServiceHealth(
                            status=ServiceStatus.HEALTHY,
                            last_check=datetime.utcnow(),
                            response_time_ms=response_time
                        )
                    else:
                        return ServiceHealth(
                            status=ServiceStatus.UNHEALTHY,
                            last_check=datetime.utcnow(),
                            response_time_ms=response_time,
                            error_message=f"Service reported unhealthy status: {health_data.get('status')}"
                        )
                else:
                    return ServiceHealth(
                        status=ServiceStatus.UNHEALTHY,
                        last_check=datetime.utcnow(),
                        response_time_ms=response_time,
                        error_message=f"Health check returned status code: {response.status_code}"
                    )
        
        except Exception as e:
            return ServiceHealth(
                status=ServiceStatus.UNHEALTHY,
                last_check=datetime.utcnow(),
                error_message=f"Health check failed: {str(e)}"
            )
    
    async def update_service_health(self, service_key: str):
        """Update health status for a service"""
        health = await self.check_service_health(service_key)
        current_health = self.health_status.get(service_key)
        
        if current_health:
            if health.status == ServiceStatus.HEALTHY:
                current_health.status = ServiceStatus.HEALTHY
                current_health.consecutive_failures = 0
            else:
                current_health.consecutive_failures += 1
                if current_health.consecutive_failures >= self.circuit_breaker_threshold:
                    current_health.status = ServiceStatus.CIRCUIT_OPEN
                else:
                    current_health.status = ServiceStatus.UNHEALTHY
            
            current_health.last_check = health.last_check
            current_health.response_time_ms = health.response_time_ms
            current_health.error_message = health.error_message
        else:
            self.health_status[service_key] = health
    
    async def check_all_services_health(self):
        """Check health of all services concurrently"""
        tasks = []
        for service_key in self.services.keys():
            tasks.append(self.update_service_health(service_key))
        
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("Completed health check for all services")
    
    def _start_health_monitoring(self):
        """Start background health monitoring"""
        async def health_monitor():
            while True:
                try:
                    await self.check_all_services_health()
                except Exception as e:
                    logger.error(f"Health monitoring error: {e}")
                
                await asyncio.sleep(self.health_check_interval)
        
        # Start health monitoring in background
        asyncio.create_task(health_monitor())
        logger.info("Started health monitoring")
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get health summary for all services"""
        summary = {
            "timestamp": datetime.utcnow().isoformat(),
            "services": {},
            "overall_status": "healthy",
            "healthy_count": 0,
            "unhealthy_count": 0,
            "total_count": len(self.services)
        }
        
        for service_key, health in self.health_status.items():
            service_summary = {
                "status": health.status.value,
                "last_check": health.last_check.isoformat(),
                "response_time_ms": health.response_time_ms,
                "consecutive_failures": health.consecutive_failures,
                "error_message": health.error_message
            }
            
            summary["services"][service_key] = service_summary
            
            if health.status == ServiceStatus.HEALTHY:
                summary["healthy_count"] += 1
            else:
                summary["unhealthy_count"] += 1
        
        # Determine overall status
        if summary["unhealthy_count"] == 0:
            summary["overall_status"] = "healthy"
        elif summary["healthy_count"] >= summary["total_count"] * 0.8:
            summary["overall_status"] = "degraded"
        else:
            summary["overall_status"] = "unhealthy"
        
        return summary
    
    def get_service_metrics(self) -> Dict[str, Any]:
        """Get service metrics for monitoring"""
        metrics = {
            "total_services": len(self.services),
            "healthy_services": 0,
            "unhealthy_services": 0,
            "circuit_open_services": 0,
            "average_response_time_ms": 0.0
        }
        
        total_response_time = 0.0
        response_time_count = 0
        
        for health in self.health_status.values():
            if health.status == ServiceStatus.HEALTHY:
                metrics["healthy_services"] += 1
            elif health.status == ServiceStatus.CIRCUIT_OPEN:
                metrics["circuit_open_services"] += 1
            else:
                metrics["unhealthy_services"] += 1
            
            if health.response_time_ms:
                total_response_time += health.response_time_ms
                response_time_count += 1
        
        if response_time_count > 0:
            metrics["average_response_time_ms"] = total_response_time / response_time_count
        
        return metrics

# Global service registry instance
service_registry = ServiceRegistry() 