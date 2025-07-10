import httpx
import asyncio
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path
import json
import re
from .models import EndpointInfo, EndpointDiscoveryResult

logger = logging.getLogger(__name__)


class EndpointDiscoveryService:
    """Service for discovering API endpoints from ReqArchitect services."""
    
    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.known_endpoints = self._load_known_endpoints()
    
    def _load_known_endpoints(self) -> Dict[str, List[EndpointInfo]]:
        """Load known endpoints from API reference files."""
        known_endpoints = {}
        
        # Common ReqArchitect service endpoints
        service_patterns = {
            "goal_service": [
                EndpointInfo(path="/goals", method="GET"),
                EndpointInfo(path="/goals", method="POST"),
                EndpointInfo(path="/goals/{id}", method="GET"),
                EndpointInfo(path="/goals/{id}", method="PUT"),
                EndpointInfo(path="/goals/{id}", method="DELETE"),
                EndpointInfo(path="/goals/{id}/assessment", method="GET"),
                EndpointInfo(path="/goals/by-status/{status}", method="GET"),
                EndpointInfo(path="/goals/critical", method="GET"),
                EndpointInfo(path="/goals/active", method="GET")
            ],
            "workpackage_service": [
                EndpointInfo(path="/work-packages", method="GET"),
                EndpointInfo(path="/work-packages", method="POST"),
                EndpointInfo(path="/work-packages/{id}", method="GET"),
                EndpointInfo(path="/work-packages/{id}", method="PUT"),
                EndpointInfo(path="/work-packages/{id}", method="DELETE"),
                EndpointInfo(path="/work-packages/active", method="GET"),
                EndpointInfo(path="/work-packages/by-status/{status}", method="GET")
            ],
            "businessfunction_service": [
                EndpointInfo(path="/business-functions", method="GET"),
                EndpointInfo(path="/business-functions", method="POST"),
                EndpointInfo(path="/business-functions/{id}", method="GET"),
                EndpointInfo(path="/business-functions/{id}", method="PUT"),
                EndpointInfo(path="/business-functions/{id}", method="DELETE"),
                EndpointInfo(path="/business-functions/active", method="GET")
            ],
            "businessprocess_service": [
                EndpointInfo(path="/business-processes", method="GET"),
                EndpointInfo(path="/business-processes", method="POST"),
                EndpointInfo(path="/business-processes/{id}", method="GET"),
                EndpointInfo(path="/business-processes/{id}", method="PUT"),
                EndpointInfo(path="/business-processes/{id}", method="DELETE"),
                EndpointInfo(path="/business-processes/active", method="GET")
            ],
            "businessrole_service": [
                EndpointInfo(path="/business-roles", method="GET"),
                EndpointInfo(path="/business-roles", method="POST"),
                EndpointInfo(path="/business-roles/{id}", method="GET"),
                EndpointInfo(path="/business-roles/{id}", method="PUT"),
                EndpointInfo(path="/business-roles/{id}", method="DELETE"),
                EndpointInfo(path="/business-roles/active", method="GET")
            ],
            "capability_service": [
                EndpointInfo(path="/capabilities", method="GET"),
                EndpointInfo(path="/capabilities", method="POST"),
                EndpointInfo(path="/capabilities/{id}", method="GET"),
                EndpointInfo(path="/capabilities/{id}", method="PUT"),
                EndpointInfo(path="/capabilities/{id}", method="DELETE"),
                EndpointInfo(path="/capabilities/active", method="GET")
            ],
            "constraint_service": [
                EndpointInfo(path="/constraints", method="GET"),
                EndpointInfo(path="/constraints", method="POST"),
                EndpointInfo(path="/constraints/{id}", method="GET"),
                EndpointInfo(path="/constraints/{id}", method="PUT"),
                EndpointInfo(path="/constraints/{id}", method="DELETE"),
                EndpointInfo(path="/constraints/active", method="GET")
            ],
            "driver_service": [
                EndpointInfo(path="/drivers", method="GET"),
                EndpointInfo(path="/drivers", method="POST"),
                EndpointInfo(path="/drivers/{id}", method="GET"),
                EndpointInfo(path="/drivers/{id}", method="PUT"),
                EndpointInfo(path="/drivers/{id}", method="DELETE"),
                EndpointInfo(path="/drivers/active", method="GET")
            ],
            "requirement_service": [
                EndpointInfo(path="/requirements", method="GET"),
                EndpointInfo(path="/requirements", method="POST"),
                EndpointInfo(path="/requirements/{id}", method="GET"),
                EndpointInfo(path="/requirements/{id}", method="PUT"),
                EndpointInfo(path="/requirements/{id}", method="DELETE"),
                EndpointInfo(path="/requirements/active", method="GET")
            ],
            "applicationfunction_service": [
                EndpointInfo(path="/application-functions", method="GET"),
                EndpointInfo(path="/application-functions", method="POST"),
                EndpointInfo(path="/application-functions/{id}", method="GET"),
                EndpointInfo(path="/application-functions/{id}", method="PUT"),
                EndpointInfo(path="/application-functions/{id}", method="DELETE"),
                EndpointInfo(path="/application-functions/active", method="GET"),
                EndpointInfo(path="/application-functions/critical", method="GET"),
                EndpointInfo(path="/application-functions/{id}/impact-map", method="GET"),
                EndpointInfo(path="/application-functions/{id}/performance-score", method="GET"),
                EndpointInfo(path="/application-functions/{id}/analysis", method="GET")
            ],
            "auth_service": [
                EndpointInfo(path="/auth/login", method="POST"),
                EndpointInfo(path="/auth/signup", method="POST"),
                EndpointInfo(path="/auth/profile", method="GET"),
                EndpointInfo(path="/auth/logout", method="POST"),
                EndpointInfo(path="/auth/invite", method="POST"),
                EndpointInfo(path="/auth/accept-invite", method="POST"),
                EndpointInfo(path="/auth/rbac-summary", method="GET"),
                EndpointInfo(path="/auth/validate", method="POST"),
                EndpointInfo(path="/auth/refresh", method="POST")
            ],
            "gateway_service": [
                EndpointInfo(path="/gateway/route", method="POST"),
                EndpointInfo(path="/gateway/health", method="GET"),
                EndpointInfo(path="/gateway/metrics", method="GET"),
                EndpointInfo(path="/gateway/services", method="GET")
            ],
            "architecture_validation_service": [
                EndpointInfo(path="/validation/validate", method="POST"),
                EndpointInfo(path="/validation/score", method="POST"),
                EndpointInfo(path="/validation/reports", method="GET"),
                EndpointInfo(path="/validation/health", method="GET")
            ]
        }
        
        return service_patterns
    
    async def discover_endpoints_from_service(self, base_url: str, service_name: str) -> EndpointDiscoveryResult:
        """Discover endpoints from a service using multiple methods."""
        methods = [
            self._discover_from_swagger,
            self._discover_from_api_reference,
            self._discover_from_known_patterns,
            self._discover_from_health_endpoint
        ]
        
        for method in methods:
            try:
                result = await method(base_url, service_name)
                if result.endpoints:
                    logger.info(f"Discovered {len(result.endpoints)} endpoints for {service_name} using {result.discovery_method}")
                    return result
            except Exception as e:
                logger.debug(f"Method {method.__name__} failed for {service_name}: {e}")
                continue
        
        # Fallback to known patterns
        known_endpoints = self.known_endpoints.get(service_name, [])
        return EndpointDiscoveryResult(
            service_name=service_name,
            discovery_method="known_patterns_fallback",
            endpoints_found=len(known_endpoints),
            endpoints=known_endpoints
        )
    
    async def _discover_from_swagger(self, base_url: str, service_name: str) -> EndpointDiscoveryResult:
        """Discover endpoints from Swagger/OpenAPI documentation."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Try common OpenAPI endpoints
                openapi_urls = [
                    f"{base_url}/openapi.json",
                    f"{base_url}/swagger.json",
                    f"{base_url}/docs/openapi.json"
                ]
                
                for url in openapi_urls:
                    response = await client.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        endpoints = self._parse_openapi_spec(data)
                        return EndpointDiscoveryResult(
                            service_name=service_name,
                            discovery_method="swagger_openapi",
                            endpoints_found=len(endpoints),
                            endpoints=endpoints
                        )
                
                return EndpointDiscoveryResult(
                    service_name=service_name,
                    discovery_method="swagger_openapi",
                    endpoints_found=0,
                    endpoints=[],
                    error="No OpenAPI spec found"
                )
                
            except Exception as e:
                return EndpointDiscoveryResult(
                    service_name=service_name,
                    discovery_method="swagger_openapi",
                    endpoints_found=0,
                    endpoints=[],
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
                    endpoints.append(EndpointInfo(
                        path=path,
                        method=method.upper(),
                        description=description
                    ))
        
        return endpoints
    
    async def _discover_from_api_reference(self, base_url: str, service_name: str) -> EndpointDiscoveryResult:
        """Discover endpoints from API reference documentation."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Try to get API reference markdown
                response = await client.get(f"{base_url}/API_REFERENCE.md")
                if response.status_code == 200:
                    content = response.text
                    endpoints = self._parse_api_reference_md(content)
                    return EndpointDiscoveryResult(
                        service_name=service_name,
                        discovery_method="api_reference_md",
                        endpoints_found=len(endpoints),
                        endpoints=endpoints
                    )
                
                return EndpointDiscoveryResult(
                    service_name=service_name,
                    discovery_method="api_reference_md",
                    endpoints_found=0,
                    endpoints=[],
                    error="API reference not found"
                )
                
            except Exception as e:
                return EndpointDiscoveryResult(
                    service_name=service_name,
                    discovery_method="api_reference_md",
                    endpoints_found=0,
                    endpoints=[],
                    error=str(e)
                )
    
    def _parse_api_reference_md(self, content: str) -> List[EndpointInfo]:
        """Parse API reference markdown to extract endpoints."""
        endpoints = []
        
        # Look for HTTP method patterns in markdown
        patterns = [
            r'\*\*(GET|POST|PUT|DELETE|PATCH)\*\*\s*`([^`]+)`',
            r'`([^`]+)`\s*\(([A-Z]+)\)',
            r'([A-Z]+)\s+`([^`]+)`'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    method, path = match
                    endpoints.append(EndpointInfo(
                        path=path.strip(),
                        method=method.upper()
                    ))
        
        return endpoints
    
    async def _discover_from_known_patterns(self, base_url: str, service_name: str) -> EndpointDiscoveryResult:
        """Discover endpoints using known patterns for the service."""
        known_endpoints = self.known_endpoints.get(service_name, [])
        
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
        
        return EndpointDiscoveryResult(
            service_name=service_name,
            discovery_method="known_patterns",
            endpoints_found=len(verified_endpoints),
            endpoints=verified_endpoints
        )
    
    async def _discover_from_health_endpoint(self, base_url: str, service_name: str) -> EndpointDiscoveryResult:
        """Discover basic endpoints from health check."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Try common health endpoints
                health_urls = [
                    f"{base_url}/health",
                    f"{base_url}/healthz",
                    f"{base_url}/ping"
                ]
                
                endpoints = []
                for url in health_urls:
                    try:
                        response = await client.get(url)
                        if response.status_code == 200:
                            endpoints.append(EndpointInfo(
                                path=url.replace(base_url, ""),
                                method="GET",
                                description="Health check endpoint"
                            ))
                    except Exception:
                        continue
                
                return EndpointDiscoveryResult(
                    service_name=service_name,
                    discovery_method="health_endpoint",
                    endpoints_found=len(endpoints),
                    endpoints=endpoints
                )
                
            except Exception as e:
                return EndpointDiscoveryResult(
                    service_name=service_name,
                    discovery_method="health_endpoint",
                    endpoints_found=0,
                    endpoints=[],
                    error=str(e)
                ) 