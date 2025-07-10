import redis
import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from .models import ServiceEndpointMap, HealthSummary

logger = logging.getLogger(__name__)


class CacheService:
    """Redis cache service for API debug data."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379", ttl_seconds: int = 300):
        self.redis_url = redis_url
        self.ttl_seconds = ttl_seconds
        self.client = None
        self._init_redis_client()
    
    def _init_redis_client(self):
        """Initialize Redis client with error handling."""
        try:
            self.client = redis.from_url(self.redis_url, decode_responses=True)
            # Test connection
            self.client.ping()
            logger.info("Redis client initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize Redis client: {e}")
            self.client = None
    
    def _serialize_datetime(self, obj: Any) -> Any:
        """Serialize datetime objects for JSON storage."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: self._serialize_datetime(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_datetime(item) for item in obj]
        return obj
    
    def _deserialize_datetime(self, obj: Any) -> Any:
        """Deserialize datetime objects from JSON storage."""
        if isinstance(obj, str):
            try:
                return datetime.fromisoformat(obj.replace("Z", "+00:00"))
            except ValueError:
                return obj
        elif isinstance(obj, dict):
            return {k: self._deserialize_datetime(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._deserialize_datetime(item) for item in obj]
        return obj
    
    def cache_service_endpoints(self, service_name: str, endpoints: List[ServiceEndpointMap]) -> bool:
        """Cache service endpoints data."""
        if not self.client:
            return False
        
        try:
            key = f"api_debug:service:{service_name}"
            data = {
                "endpoints": [endpoint.dict() for endpoint in endpoints],
                "cached_at": datetime.now().isoformat(),
                "ttl": self.ttl_seconds
            }
            
            serialized_data = json.dumps(self._serialize_datetime(data))
            self.client.setex(key, self.ttl_seconds, serialized_data)
            logger.debug(f"Cached endpoints for {service_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error caching endpoints for {service_name}: {e}")
            return False
    
    def get_cached_service_endpoints(self, service_name: str) -> Optional[List[ServiceEndpointMap]]:
        """Get cached service endpoints data."""
        if not self.client:
            return None
        
        try:
            key = f"api_debug:service:{service_name}"
            data = self.client.get(key)
            
            if data:
                parsed_data = json.loads(data)
                deserialized_data = self._deserialize_datetime(parsed_data)
                
                endpoints = []
                for endpoint_data in deserialized_data.get("endpoints", []):
                    # Convert datetime strings back to datetime objects
                    if "last_heartbeat" in endpoint_data and endpoint_data["last_heartbeat"]:
                        endpoint_data["last_heartbeat"] = datetime.fromisoformat(
                            endpoint_data["last_heartbeat"].replace("Z", "+00:00")
                        )
                    if "created_at" in endpoint_data and endpoint_data["created_at"]:
                        endpoint_data["created_at"] = datetime.fromisoformat(
                            endpoint_data["created_at"].replace("Z", "+00:00")
                        )
                    if "updated_at" in endpoint_data and endpoint_data["updated_at"]:
                        endpoint_data["updated_at"] = datetime.fromisoformat(
                            endpoint_data["updated_at"].replace("Z", "+00:00")
                        )
                    
                    endpoints.append(ServiceEndpointMap(**endpoint_data))
                
                logger.debug(f"Retrieved cached endpoints for {service_name}")
                return endpoints
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached endpoints for {service_name}: {e}")
            return None
    
    def cache_all_services(self, services: List[ServiceEndpointMap]) -> bool:
        """Cache all services data."""
        if not self.client:
            return False
        
        try:
            key = "api_debug:all_services"
            data = {
                "services": [service.dict() for service in services],
                "cached_at": datetime.now().isoformat(),
                "ttl": self.ttl_seconds
            }
            
            serialized_data = json.dumps(self._serialize_datetime(data))
            self.client.setex(key, self.ttl_seconds, serialized_data)
            logger.debug("Cached all services data")
            return True
            
        except Exception as e:
            logger.error(f"Error caching all services: {e}")
            return False
    
    def get_cached_all_services(self) -> Optional[List[ServiceEndpointMap]]:
        """Get cached all services data."""
        if not self.client:
            return None
        
        try:
            key = "api_debug:all_services"
            data = self.client.get(key)
            
            if data:
                parsed_data = json.loads(data)
                deserialized_data = self._deserialize_datetime(parsed_data)
                
                services = []
                for service_data in deserialized_data.get("services", []):
                    # Convert datetime strings back to datetime objects
                    if "last_heartbeat" in service_data and service_data["last_heartbeat"]:
                        service_data["last_heartbeat"] = datetime.fromisoformat(
                            service_data["last_heartbeat"].replace("Z", "+00:00")
                        )
                    
                    services.append(ServiceEndpointMap(**service_data))
                
                logger.debug("Retrieved cached all services data")
                return services
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached all services: {e}")
            return None
    
    def cache_health_summary(self, summary: HealthSummary) -> bool:
        """Cache health summary data."""
        if not self.client:
            return False
        
        try:
            key = "api_debug:health_summary"
            data = summary.dict()
            serialized_data = json.dumps(self._serialize_datetime(data))
            self.client.setex(key, self.ttl_seconds, serialized_data)
            logger.debug("Cached health summary")
            return True
            
        except Exception as e:
            logger.error(f"Error caching health summary: {e}")
            return False
    
    def get_cached_health_summary(self) -> Optional[HealthSummary]:
        """Get cached health summary data."""
        if not self.client:
            return None
        
        try:
            key = "api_debug:health_summary"
            data = self.client.get(key)
            
            if data:
                parsed_data = json.loads(data)
                deserialized_data = self._deserialize_datetime(parsed_data)
                
                # Convert datetime strings back to datetime objects
                if "last_updated" in deserialized_data and deserialized_data["last_updated"]:
                    deserialized_data["last_updated"] = datetime.fromisoformat(
                        deserialized_data["last_updated"].replace("Z", "+00:00")
                    )
                
                # Convert service datetime objects
                for service in deserialized_data.get("services", []):
                    if "last_heartbeat" in service and service["last_heartbeat"]:
                        service["last_heartbeat"] = datetime.fromisoformat(
                            service["last_heartbeat"].replace("Z", "+00:00")
                        )
                
                summary = HealthSummary(**deserialized_data)
                logger.debug("Retrieved cached health summary")
                return summary
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached health summary: {e}")
            return None
    
    def invalidate_cache(self, pattern: str = "api_debug:*") -> bool:
        """Invalidate cache entries matching pattern."""
        if not self.client:
            return False
        
        try:
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
                logger.info(f"Invalidated {len(keys)} cache entries")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error invalidating cache: {e}")
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if not self.client:
            return {"error": "Redis not available"}
        
        try:
            keys = self.client.keys("api_debug:*")
            stats = {
                "total_keys": len(keys),
                "cache_ttl_seconds": self.ttl_seconds,
                "redis_connected": True
            }
            
            # Get TTL for each key
            key_ttls = {}
            for key in keys:
                ttl = self.client.ttl(key)
                key_ttls[key] = ttl
            
            stats["key_ttls"] = key_ttls
            return stats
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"error": str(e), "redis_connected": False} 