import httpx
import asyncio
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path
import json
import re
from .enhanced_models import EndpointInfo, DiscoveryResult, DiscoveryMethod, ServiceStatus, HealthCheckResult
from .service_catalog import ServiceCatalog
from datetime import datetime

logger = logging.getLogger(__name__)


class EnhancedEndpointDiscoveryService:
    """Enhanced service for discovering API endpoints from ReqArchitect services."""
    
    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.service_catalog = ServiceCatalog()
        self.known_endpoints = self._load_known_endpoints()
    
    def _load_known_endpoints(self) -> Dict[str, List[EndpointInfo]]:
        """Load known endpoints from service catalog and patterns."""
        known_endpoints = {}
        
        # Load from service catalog
        catalog_entries = self.service_catalog.get_all_services()
        for entry in catalog_entries:
            service_name = entry.get("service_name")
            routes = entry.get("routes", [])
            
            endpoints = []
            for route in routes:
                # Parse route to extract method and path
                method = "GET"
                path = route
                
                # Handle different route patterns
                if route.startswith("POST:"):
                    method = "POST"
                    path = route[5:]
                elif route.startswith("PUT:"):
                    method = "PUT"
                    path = route[4:]
                elif route.startswith("DELETE:"):
                    method = "DELETE"
                    path = route[7:]
                elif route.startswith("PATCH:"):
                    method = "PATCH"
                    path = route[6:]
                
                endpoints.append(EndpointInfo(
                    path=path,
                    method=method,
                    description=f"Route from service catalog"
                ))
            
            if endpoints:
                known_endpoints[service_name] = endpoints
        
        # Add common ReqArchitect service endpoints
        common_patterns = {
            "goal_service": [
                EndpointInfo(path="/goals", method="GET", description="List all goals"),
                EndpointInfo(path="/goals", method="POST", description="Create new goal"),
                EndpointInfo(path="/goals/{id}", method="GET", description="Get goal by ID"),
                EndpointInfo(path="/goals/{id}", method="PUT", description="Update goal"),
                EndpointInfo(path="/goals/{id}", method="DELETE", description="Delete goal"),
                EndpointInfo(path="/goals/{id}/assessment", method="GET", description="Get goal assessment"),
                EndpointInfo(path="/goals/by-status/{status}", method="GET", description="Get goals by status"),
                EndpointInfo(path="/goals/critical", method="GET", description="Get critical goals"),
                EndpointInfo(path="/goals/active", method="GET", description="Get active goals"),
                EndpointInfo(path="/health", method="GET", description="Health check endpoint")
            ],
            "workpackage_service": [
                EndpointInfo(path="/work-packages", method="GET", description="List all work packages"),
                EndpointInfo(path="/work-packages", method="POST", description="Create new work package"),
                EndpointInfo(path="/work-packages/{id}", method="GET", description="Get work package by ID"),
                EndpointInfo(path="/work-packages/{id}", method="PUT", description="Update work package"),
                EndpointInfo(path="/work-packages/{id}", method="DELETE", description="Delete work package"),
                EndpointInfo(path="/work-packages/active", method="GET", description="Get active work packages"),
                EndpointInfo(path="/work-packages/by-status/{status}", method="GET", description="Get work packages by status"),
                EndpointInfo(path="/health", method="GET", description="Health check endpoint")
            ],
            "auth_service": [
                EndpointInfo(path="/auth/login", method="POST", description="User login"),
                EndpointInfo(path="/auth/signup", method="POST", description="User signup"),
                EndpointInfo(path="/auth/profile", method="GET", description="Get user profile"),
                EndpointInfo(path="/auth/logout", method="POST", description="User logout"),
                EndpointInfo(path="/auth/invite", method="POST", description="Invite user"),
                EndpointInfo(path="/auth/accept-invite", method="POST", description="Accept invitation"),
                EndpointInfo(path="/auth/rbac-summary", method="GET", description="RBAC summary"),
                EndpointInfo(path="/auth/validate", method="POST", description="Validate token"),
                EndpointInfo(path="/auth/refresh", method="POST", description="Refresh token"),
                EndpointInfo(path="/health", method="GET", description="Health check endpoint")
            ],
            "gateway_service": [
                EndpointInfo(path="/gateway/route", method="POST", description="Route request"),
                EndpointInfo(path="/gateway/health", method="GET", description="Gateway health"),
                EndpointInfo(path="/gateway/metrics", method="GET", description="Gateway metrics"),
                EndpointInfo(path="/gateway/services", method="GET", description="Service registry"),
                EndpointInfo(path="/health", method="GET", description="Health check endpoint")
            ],
            "applicationfunction_service": [
                EndpointInfo(path="/application-functions", method="GET", description="List all application functions"),
                EndpointInfo(path="/application-functions", method="POST", description="Create new application function"),
                EndpointInfo(path="/application-functions/{id}", method="GET", description="Get application function by ID"),
                EndpointInfo(path="/application-functions/{id}", method="PUT", description="Update application function"),
                EndpointInfo(path="/application-functions/{id}", method="DELETE", description="Delete application function"),
                EndpointInfo(path="/application-functions/active", method="GET", description="Get active application functions"),
                EndpointInfo(path="/application-functions/critical", method="GET", description="Get critical application functions"),
                EndpointInfo(path="/application-functions/{id}/impact-map", method="GET", description="Get impact map"),
                EndpointInfo(path="/application-functions/{id}/performance-score", method="GET", description="Get performance score"),
                EndpointInfo(path="/application-functions/{id}/analysis", method="GET", description="Get analysis"),
                EndpointInfo(path="/health", method="GET", description="Health check endpoint")
            ]
        }
        
        # Merge with catalog entries
        for service_name, endpoints in common_patterns.items():
            if service_name in known_endpoints:
                # Merge and deduplicate
                existing_paths = {ep.path for ep in known_endpoints[service_name]}
                for endpoint in endpoints:
                    if endpoint.path not in existing_paths:
                        known_endpoints[service_name].append(endpoint)
            else:
                known_endpoints[service_name] = endpoints
        
        return known_endpoints
    
    async def discover_endpoints_from_service(self, base_url: str, service_name: str, 
                                            discovery_method: DiscoveryMethod = DiscoveryMethod.LABEL_BASED) -> DiscoveryResult:
        """Discover endpoints from a service using multiple methods."""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Method 1: Swagger/OpenAPI discovery
            swagger_result = await self._discover_from_swagger(base_url, service_name)
            if swagger_result.endpoints:
                return self._create_discovery_result(
                    service_name, discovery_method, swagger_result.endpoints, 
                    ServiceStatus.HEALTHY, start_time
                )
            
            # Method 2: API Reference documentation
            api_ref_result = await self._discover_from_api_reference(base_url, service_name)
            if api_ref_result.endpoints:
                return self._create_discovery_result(
                    service_name, discovery_method, api_ref_result.endpoints,
                    ServiceStatus.HEALTHY, start_time
                )
            
            # Method 3: Known patterns with verification
            pattern_result = await self._discover_from_known_patterns(base_url, service_name)
            if pattern_result.endpoints:
                return self._create_discovery_result(
                    service_name, discovery_method, pattern_result.endpoints,
                    ServiceStatus.HEALTHY, start_time
                )
            
            # Method 4: Health endpoint discovery
            health_result = await self._discover_from_health_endpoint(base_url, service_name)
            if health_result.endpoints:
                return self._create_discovery_result(
                    service_name, discovery_method, health_result.endpoints,
                    ServiceStatus.HEALTHY, start_time
                )
            
            # Method 5: Catalog fallback
            catalog_result = await self._discover_from_catalog(base_url, service_name)
            if catalog_result.endpoints:
                return self._create_discovery_result(
                    service_name, discovery_method, catalog_result.endpoints,
                    ServiceStatus.UNKNOWN, start_time, catalog_used=True
                )
            
            # No endpoints found
            return self._create_discovery_result(
                service_name, discovery_method, [],
                ServiceStatus.UNKNOWN, start_time,
                error="No endpoints discovered"
            )
            
        except Exception as e:
            logger.error(f"Error discovering endpoints for {service_name}: {e}")
            return self._create_discovery_result(
                service_name, discovery_method, [],
                ServiceStatus.UNKNOWN, start_time,
                error=str(e)
            )
    
    def _create_discovery_result(self, service_name: str, discovery_method: DiscoveryMethod,
                               endpoints: List[EndpointInfo], status: ServiceStatus,
                               start_time: float, catalog_used: bool = False,
                               error: Optional[str] = None) -> DiscoveryResult:
        """Create a discovery result."""
        duration = asyncio.get_event_loop().time() - start_time
        
        return DiscoveryResult(
            service_name=service_name,
            discovery_method=discovery_method,
            endpoints_found=len(endpoints),
            endpoints=endpoints,
            health_status=status,
            catalog_used=catalog_used,
            error=error
        )
    
    async def _discover_from_swagger(self, base_url: str, service_name: str) -> DiscoveryResult:
        """Discover endpoints from Swagger/OpenAPI documentation."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Try common OpenAPI endpoints
                openapi_urls = [
                    f"{base_url}/openapi.json",
                    f"{base_url}/swagger.json",
                    f"{base_url}/docs/openapi.json",
                    f"{base_url}/api/openapi.json"
                ]
                
                for url in openapi_urls:
                    try:
                        response = await client.get(url)
                        if response.status_code == 200:
                            data = response.json()
                            endpoints = self._parse_openapi_spec(data)
                            return DiscoveryResult(
                                service_name=service_name,
                                discovery_method=DiscoveryMethod.LABEL_BASED,
                                endpoints_found=len(endpoints),
                                endpoints=endpoints,
                                health_status=ServiceStatus.HEALTHY
                            )
                    except Exception as e:
                        logger.debug(f"Failed to get OpenAPI spec from {url}: {e}")
                        continue
                
                return DiscoveryResult(
                    service_name=service_name,
                    discovery_method=DiscoveryMethod.LABEL_BASED,
                    endpoints_found=0,
                    endpoints=[],
                    health_status=ServiceStatus.UNKNOWN,
                    error="No OpenAPI spec found"
                )
                
            except Exception as e:
                return DiscoveryResult(
                    service_name=service_name,
                    discovery_method=DiscoveryMethod.LABEL_BASED,
                    endpoints_found=0,
                    endpoints=[],
                    health_status=ServiceStatus.UNKNOWN,
                    error=str(e)
                )
    
    def _parse_openapi_spec(self, spec: Dict[str, Any]) -> List[EndpointInfo]:
        """Parse OpenAPI specification to extract endpoints."""
        endpoints = []
        
        if "paths" not in spec:
            return endpoints
        
        for path, methods in spec["paths"].items():
            for method, details in methods.items():
                if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                    description = details.get("summary", details.get("description", ""))
                    
                    # Extract response codes
                    response_codes = []
                    if "responses" in details:
                        response_codes = list(details["responses"].keys())
                    
                    # Extract parameters
                    parameters = []
                    if "parameters" in details:
                        for param in details["parameters"]:
                            param_name = param.get("name", "")
                            if param_name:
                                parameters.append(param_name)
                    
                    endpoints.append(EndpointInfo(
                        path=path,
                        method=method.upper(),
                        description=description,
                        parameters=parameters if parameters else None,
                        response_codes=response_codes if response_codes else None
                    ))
        
        return endpoints
    
    async def _discover_from_api_reference(self, base_url: str, service_name: str) -> DiscoveryResult:
        """Discover endpoints from API reference documentation."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Try to get API reference markdown
                api_ref_urls = [
                    f"{base_url}/API_REFERENCE.md",
                    f"{base_url}/api-reference.md",
                    f"{base_url}/docs/API_REFERENCE.md"
                ]
                
                for url in api_ref_urls:
                    try:
                        response = await client.get(url)
                        if response.status_code == 200:
                            content = response.text
                            endpoints = self._parse_api_reference_md(content)
                            return DiscoveryResult(
                                service_name=service_name,
                                discovery_method=DiscoveryMethod.LABEL_BASED,
                                endpoints_found=len(endpoints),
                                endpoints=endpoints,
                                health_status=ServiceStatus.HEALTHY
                            )
                    except Exception as e:
                        logger.debug(f"Failed to get API reference from {url}: {e}")
                        continue
                
                return DiscoveryResult(
                    service_name=service_name,
                    discovery_method=DiscoveryMethod.LABEL_BASED,
                    endpoints_found=0,
                    endpoints=[],
                    health_status=ServiceStatus.UNKNOWN,
                    error="API reference not found"
                )
                
            except Exception as e:
                return DiscoveryResult(
                    service_name=service_name,
                    discovery_method=DiscoveryMethod.LABEL_BASED,
                    endpoints_found=0,
                    endpoints=[],
                    health_status=ServiceStatus.UNKNOWN,
                    error=str(e)
                )
    
    def _parse_api_reference_md(self, content: str) -> List[EndpointInfo]:
        """Parse API reference markdown to extract endpoints."""
        endpoints = []
        
        # Look for HTTP method patterns in markdown
        patterns = [
            r'\*\*(GET|POST|PUT|DELETE|PATCH)\*\*\s*`([^`]+)`',
            r'`([^`]+)`\s*\(([A-Z]+)\)',
            r'([A-Z]+)\s+`([^`]+)`',
            r'###\s+(GET|POST|PUT|DELETE|PATCH)\s+`([^`]+)`',
            r'##\s+(GET|POST|PUT|DELETE|PATCH)\s+`([^`]+)`'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    method, path = match
                    endpoints.append(EndpointInfo(
                        path=path.strip(),
                        method=method.upper(),
                        description=f"Discovered from API reference"
                    ))
        
        return endpoints
    
    async def _discover_from_known_patterns(self, base_url: str, service_name: str) -> DiscoveryResult:
        """Discover endpoints using known patterns for the service."""
        known_endpoints = self.known_endpoints.get(service_name, [])
        
        if not known_endpoints:
            return DiscoveryResult(
                service_name=service_name,
                discovery_method=DiscoveryMethod.LABEL_BASED,
                endpoints_found=0,
                endpoints=[],
                health_status=ServiceStatus.UNKNOWN,
                error="No known patterns for service"
            )
        
        # Verify endpoints exist by making HEAD requests
        verified_endpoints = []
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for endpoint in known_endpoints:
                try:
                    response = await client.head(f"{base_url}{endpoint.path}")
                    if response.status_code in [200, 404, 405]:  # 404/405 means endpoint exists but method not allowed
                        verified_endpoints.append(endpoint)
                except Exception:
                    # If we can't verify, include it anyway
                    verified_endpoints.append(endpoint)
        
        return DiscoveryResult(
            service_name=service_name,
            discovery_method=DiscoveryMethod.LABEL_BASED,
            endpoints_found=len(verified_endpoints),
            endpoints=verified_endpoints,
            health_status=ServiceStatus.HEALTHY
        )
    
    async def _discover_from_health_endpoint(self, base_url: str, service_name: str) -> DiscoveryResult:
        """Discover basic endpoints from health check."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Try common health endpoints
                health_endpoints = ["/health", "/healthz", "/ping", "/"]
                
                discovered_endpoints = []
                for endpoint in health_endpoints:
                    try:
                        url = f"{base_url}{endpoint}"
                        response = await client.get(url)
                        
                        if response.status_code in [200, 404, 405]:
                            discovered_endpoints.append(EndpointInfo(
                                path=endpoint,
                                method="GET",
                                description="Health check endpoint"
                            ))
                    except Exception:
                        continue
                
                return DiscoveryResult(
                    service_name=service_name,
                    discovery_method=DiscoveryMethod.LABEL_BASED,
                    endpoints_found=len(discovered_endpoints),
                    endpoints=discovered_endpoints,
                    health_status=ServiceStatus.HEALTHY
                )
                
            except Exception as e:
                return DiscoveryResult(
                    service_name=service_name,
                    discovery_method=DiscoveryMethod.LABEL_BASED,
                    endpoints_found=0,
                    endpoints=[],
                    health_status=ServiceStatus.UNKNOWN,
                    error=str(e)
                )
    
    async def _discover_from_catalog(self, base_url: str, service_name: str) -> DiscoveryResult:
        """Discover endpoints from service catalog."""
        try:
            catalog_entry = self.service_catalog.get_service(service_name)
            if not catalog_entry:
                return DiscoveryResult(
                    service_name=service_name,
                    discovery_method=DiscoveryMethod.CATALOG_FALLBACK,
                    endpoints_found=0,
                    endpoints=[],
                    health_status=ServiceStatus.UNKNOWN,
                    error="Service not found in catalog"
                )
            
            routes = catalog_entry.get("routes", [])
            endpoints = []
            
            for route in routes:
                # Parse route to extract method and path
                method = "GET"
                path = route
                
                # Handle different route patterns
                if route.startswith("POST:"):
                    method = "POST"
                    path = route[5:]
                elif route.startswith("PUT:"):
                    method = "PUT"
                    path = route[4:]
                elif route.startswith("DELETE:"):
                    method = "DELETE"
                    path = route[7:]
                elif route.startswith("PATCH:"):
                    method = "PATCH"
                    path = route[6:]
                
                endpoints.append(EndpointInfo(
                    path=path,
                    method=method,
                    description=f"Route from service catalog"
                ))
            
            return DiscoveryResult(
                service_name=service_name,
                discovery_method=DiscoveryMethod.CATALOG_FALLBACK,
                endpoints_found=len(endpoints),
                endpoints=endpoints,
                health_status=ServiceStatus.UNKNOWN,
                catalog_used=True
            )
            
        except Exception as e:
            return DiscoveryResult(
                service_name=service_name,
                discovery_method=DiscoveryMethod.CATALOG_FALLBACK,
                endpoints_found=0,
                endpoints=[],
                health_status=ServiceStatus.UNKNOWN,
                error=str(e)
            )
    
    async def check_service_health(self, base_url: str, service_name: str, 
                                 timeout: int = 5) -> HealthCheckResult:
        """Check service health by pinging health endpoints."""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Get health endpoints from catalog or use defaults
            catalog_entry = self.service_catalog.get_service(service_name)
            health_endpoints = [catalog_entry.get("healthcheck", "/health")] if catalog_entry else ["/health", "/healthz", "/ping", "/"]
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                for endpoint in health_endpoints:
                    try:
                        url = f"{base_url}{endpoint}"
                        response = await client.get(url)
                        
                        if response.status_code in [200, 404, 405]:  # 404/405 means endpoint exists
                            response_time = asyncio.get_event_loop().time() - start_time
                            return HealthCheckResult(
                                is_healthy=True,
                                status_code=response.status_code,
                                response_time=response_time,
                                last_check=datetime.now(),
                                endpoint_tested=endpoint
                            )
                    
                    except httpx.TimeoutException:
                        logger.debug(f"Health check timeout for {service_name} at {endpoint}")
                        continue
                    except Exception as e:
                        logger.debug(f"Health check failed for {service_name} at {endpoint}: {e}")
                        continue
            
            # No health endpoints responded
            response_time = asyncio.get_event_loop().time() - start_time
            return HealthCheckResult(
                is_healthy=False,
                response_time=response_time,
                error_message="No health endpoints responded",
                last_check=datetime.now(),
                endpoint_tested="multiple"
            )
            
        except Exception as e:
            response_time = asyncio.get_event_loop().time() - start_time
            return HealthCheckResult(
                is_healthy=False,
                response_time=response_time,
                error_message=str(e),
                last_check=datetime.now(),
                endpoint_tested="error"
            ) 