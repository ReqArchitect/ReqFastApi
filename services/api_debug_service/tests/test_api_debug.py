import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app
from app.models import ServiceEndpointMap, HealthSummary, ServiceStatus, EndpointInfo
from app.service_discovery import ServiceDiscoveryOrchestrator
from app.docker_service import DockerService
from app.endpoint_discovery import EndpointDiscoveryService
from app.cache_service import CacheService


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


@pytest.fixture
def mock_service_map():
    """Mock service endpoint map."""
    return ServiceEndpointMap(
        service_name="test_service",
        docker_container_name="/test-service",
        base_url="http://localhost:8080",
        status=ServiceStatus.HEALTHY,
        available_endpoints=[
            EndpointInfo(path="/test", method="GET", description="Test endpoint"),
            EndpointInfo(path="/test/{id}", method="GET", description="Test by ID"),
            EndpointInfo(path="/test", method="POST", description="Create test"),
        ],
        last_heartbeat=datetime.now(),
        version_tag="latest",
        port=8080,
        container_id="test123",
        image="test/service:latest",
        labels={"reqarchitect-service": "true"}
    )


@pytest.fixture
def mock_health_summary(mock_service_map):
    """Mock health summary."""
    return HealthSummary(
        total_services=1,
        healthy_services=1,
        unhealthy_services=0,
        unknown_services=0,
        services=[mock_service_map],
        last_updated=datetime.now(),
        cache_status="fresh"
    )


class TestHealthEndpoints:
    """Test health and utility endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "api_debug_service"
        assert "timestamp" in data
        assert "version" in data
    
    def test_metrics(self, client):
        """Test metrics endpoint."""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "api_debug_service"
        assert "timestamp" in data
        assert "stats" in data


class TestServiceDiscovery:
    """Test service discovery functionality."""
    
    @pytest.mark.asyncio
    async def test_discover_all_services(self, mock_service_map):
        """Test discovering all services."""
        with patch.object(ServiceDiscoveryOrchestrator, 'discover_all_services') as mock_discover:
            mock_discover.return_value = [mock_service_map]
            
            orchestrator = ServiceDiscoveryOrchestrator(Mock())
            services = await orchestrator.discover_all_services()
            
            assert len(services) == 1
            assert services[0].service_name == "test_service"
            assert services[0].status == ServiceStatus.HEALTHY
    
    @pytest.mark.asyncio
    async def test_discover_specific_service(self, mock_service_map):
        """Test discovering a specific service."""
        with patch.object(ServiceDiscoveryOrchestrator, 'discover_service') as mock_discover:
            mock_discover.return_value = mock_service_map
            
            orchestrator = ServiceDiscoveryOrchestrator(Mock())
            service = await orchestrator.discover_service("test_service")
            
            assert service.service_name == "test_service"
            assert service.status == ServiceStatus.HEALTHY
    
    @pytest.mark.asyncio
    async def test_get_health_summary(self, mock_health_summary):
        """Test getting health summary."""
        with patch.object(ServiceDiscoveryOrchestrator, 'get_health_summary') as mock_summary:
            mock_summary.return_value = mock_health_summary
            
            orchestrator = ServiceDiscoveryOrchestrator(Mock())
            summary = await orchestrator.get_health_summary()
            
            assert summary.total_services == 1
            assert summary.healthy_services == 1
            assert summary.unhealthy_services == 0


class TestAPIEndpoints:
    """Test main API endpoints."""
    
    def test_get_all_service_endpoints(self, client, mock_service_map):
        """Test getting all service endpoints."""
        with patch.object(ServiceDiscoveryOrchestrator, 'discover_all_services') as mock_discover:
            mock_discover.return_value = [mock_service_map]
            
            response = client.get("/api-debug")
            assert response.status_code == 200
            
            data = response.json()
            assert len(data) == 1
            assert data[0]["service_name"] == "test_service"
            assert data[0]["status"] == "healthy"
            assert len(data[0]["available_endpoints"]) == 3
    
    def test_get_service_endpoints(self, client, mock_service_map):
        """Test getting specific service endpoints."""
        with patch.object(ServiceDiscoveryOrchestrator, 'discover_service') as mock_discover:
            mock_discover.return_value = mock_service_map
            
            response = client.get("/api-debug/test_service")
            assert response.status_code == 200
            
            data = response.json()
            assert data["service_name"] == "test_service"
            assert data["status"] == "healthy"
            assert len(data["available_endpoints"]) == 3
    
    def test_get_service_endpoints_not_found(self, client):
        """Test getting service endpoints for non-existent service."""
        with patch.object(ServiceDiscoveryOrchestrator, 'discover_service') as mock_discover:
            mock_discover.return_value = None
            
            response = client.get("/api-debug/unknown_service")
            assert response.status_code == 404
            assert "not found" in response.json()["detail"].lower()
    
    def test_get_health_summary(self, client, mock_health_summary):
        """Test getting health summary."""
        with patch.object(ServiceDiscoveryOrchestrator, 'get_health_summary') as mock_summary:
            mock_summary.return_value = mock_health_summary
            
            response = client.get("/api-debug/health-summary")
            assert response.status_code == 200
            
            data = response.json()
            assert data["total_services"] == 1
            assert data["healthy_services"] == 1
            assert data["unhealthy_services"] == 0
            assert data["unknown_services"] == 0
    
    def test_get_service_details(self, client, mock_service_map):
        """Test getting service details."""
        mock_details = {
            "service": mock_service_map.dict(),
            "logs": ["2024-01-15T10:30:00Z INFO: Service started"],
            "network_info": {"name": "test-network"},
            "cache_stats": {"total_keys": 1}
        }
        
        with patch.object(ServiceDiscoveryOrchestrator, 'get_service_details') as mock_details_func:
            mock_details_func.return_value = mock_details
            
            response = client.get("/api-debug/test_service/details")
            assert response.status_code == 200
            
            data = response.json()
            assert "service" in data
            assert "logs" in data
            assert "network_info" in data
            assert "cache_stats" in data
    
    def test_get_service_details_not_found(self, client):
        """Test getting service details for non-existent service."""
        with patch.object(ServiceDiscoveryOrchestrator, 'get_service_details') as mock_details:
            mock_details.return_value = None
            
            response = client.get("/api-debug/unknown_service/details")
            assert response.status_code == 404
            assert "not found" in response.json()["detail"].lower()
    
    def test_refresh_cache(self, client):
        """Test cache refresh endpoint."""
        with patch.object(ServiceDiscoveryOrchestrator, 'refresh_cache') as mock_refresh:
            mock_refresh.return_value = True
            
            response = client.post("/api-debug/refresh")
            assert response.status_code == 200
            
            data = response.json()
            assert data["message"] == "Cache refreshed successfully"
            assert data["status"] == "success"
    
    def test_get_discovery_stats(self, client):
        """Test getting discovery statistics."""
        mock_stats = {
            "cache": {"total_keys": 5},
            "network": {"name": "test-network"},
            "config": {"docker_network": "test"},
            "discovery_methods": ["swagger", "api_ref"]
        }
        
        with patch.object(ServiceDiscoveryOrchestrator, 'get_discovery_stats') as mock_stats_func:
            mock_stats_func.return_value = mock_stats
            
            response = client.get("/api-debug/stats")
            assert response.status_code == 200
            
            data = response.json()
            assert "cache" in data
            assert "network" in data
            assert "config" in data
            assert "discovery_methods" in data


class TestFilteredEndpoints:
    """Test filtered endpoint endpoints."""
    
    def test_get_healthy_services(self, client, mock_service_map):
        """Test getting only healthy services."""
        with patch.object(ServiceDiscoveryOrchestrator, 'discover_all_services') as mock_discover:
            mock_discover.return_value = [mock_service_map]
            
            response = client.get("/api-debug/services/healthy")
            assert response.status_code == 200
            
            data = response.json()
            assert len(data) == 1
            assert data[0]["status"] == "healthy"
    
    def test_get_unhealthy_services(self, client):
        """Test getting only unhealthy services."""
        unhealthy_service = ServiceEndpointMap(
            service_name="unhealthy_service",
            docker_container_name="/unhealthy-service",
            base_url="http://localhost:8089",
            status=ServiceStatus.UNHEALTHY,
            available_endpoints=[],
            last_heartbeat=datetime.now(),
            version_tag="latest",
            port=8089,
            container_id="unhealthy123",
            image="test/unhealthy:latest",
            labels={"reqarchitect-service": "true"}
        )
        
        with patch.object(ServiceDiscoveryOrchestrator, 'discover_all_services') as mock_discover:
            mock_discover.return_value = [unhealthy_service]
            
            response = client.get("/api-debug/services/unhealthy")
            assert response.status_code == 200
            
            data = response.json()
            assert len(data) == 1
            assert data[0]["status"] == "unhealthy"


class TestDockerService:
    """Test Docker service functionality."""
    
    def test_get_reqarchitect_containers(self):
        """Test getting ReqArchitect containers."""
        with patch('docker.from_env') as mock_docker:
            mock_client = Mock()
            mock_container = Mock()
            mock_container.id = "test123"
            mock_container.name = "/test-service"
            mock_container.status = "running"
            mock_container.attrs = {
                "Config": {
                    "Image": "test/service:latest",
                    "Labels": {"reqarchitect-service": "true"}
                },
                "NetworkSettings": {
                    "Ports": {
                        "8080/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8080"}]
                    }
                },
                "Created": "2024-01-15T10:30:00Z"
            }
            mock_client.containers.list.return_value = [mock_container]
            mock_docker.return_value = mock_client
            
            docker_service = DockerService(Mock())
            containers = docker_service.get_reqarchitect_containers()
            
            assert len(containers) == 1
            assert containers[0].name == "/test-service"
            assert containers[0].image == "test/service:latest"
    
    def test_get_container_health(self):
        """Test checking container health."""
        with patch('docker.from_env') as mock_docker:
            mock_client = Mock()
            mock_container = Mock()
            mock_container.attrs = {
                "State": {
                    "Status": "running",
                    "Health": {"Status": "healthy"}
                }
            }
            mock_client.containers.get.return_value = mock_container
            mock_docker.return_value = mock_client
            
            docker_service = DockerService(Mock())
            is_healthy = docker_service.get_container_health("test123")
            
            assert is_healthy is True


class TestEndpointDiscovery:
    """Test endpoint discovery functionality."""
    
    @pytest.mark.asyncio
    async def test_discover_from_swagger(self):
        """Test discovering endpoints from Swagger."""
        mock_openapi_spec = {
            "paths": {
                "/test": {
                    "get": {"summary": "Get test"},
                    "post": {"summary": "Create test"}
                },
                "/test/{id}": {
                    "get": {"summary": "Get test by ID"}
                }
            }
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_openapi_spec
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            discovery = EndpointDiscoveryService()
            result = await discovery._discover_from_swagger("http://localhost:8080", "test_service")
            
            assert result.discovery_method == "swagger_openapi"
            assert result.endpoints_found == 3
            assert len(result.endpoints) == 3
    
    @pytest.mark.asyncio
    async def test_discover_from_known_patterns(self):
        """Test discovering endpoints from known patterns."""
        discovery = EndpointDiscoveryService()
        result = await discovery._discover_from_known_patterns("http://localhost:8080", "goal_service")
        
        assert result.discovery_method == "known_patterns"
        assert result.endpoints_found > 0
        assert len(result.endpoints) > 0


class TestCacheService:
    """Test cache service functionality."""
    
    def test_cache_service_endpoints(self):
        """Test caching service endpoints."""
        with patch('redis.from_url') as mock_redis:
            mock_client = Mock()
            mock_redis.return_value = mock_client
            
            cache_service = CacheService()
            success = cache_service.cache_service_endpoints("test_service", [Mock()])
            
            assert success is True
            mock_client.setex.assert_called_once()
    
    def test_get_cached_service_endpoints(self):
        """Test getting cached service endpoints."""
        mock_service_data = {
            "endpoints": [{"service_name": "test_service"}],
            "cached_at": "2024-01-15T10:30:00Z",
            "ttl": 300
        }
        
        with patch('redis.from_url') as mock_redis:
            mock_client = Mock()
            mock_client.get.return_value = '{"endpoints": [{"service_name": "test_service"}], "cached_at": "2024-01-15T10:30:00Z", "ttl": 300}'
            mock_redis.return_value = mock_client
            
            cache_service = CacheService()
            result = cache_service.get_cached_service_endpoints("test_service")
            
            assert result is not None
            assert len(result) == 1
            assert result[0].service_name == "test_service"


class TestErrorHandling:
    """Test error handling."""
    
    def test_global_exception_handler(self, client):
        """Test global exception handler."""
        with patch.object(ServiceDiscoveryOrchestrator, 'discover_all_services') as mock_discover:
            mock_discover.side_effect = Exception("Test error")
            
            response = client.get("/api-debug")
            assert response.status_code == 500
            assert "Internal server error" in response.json()["detail"]
    
    def test_docker_service_error(self):
        """Test Docker service error handling."""
        with patch('docker.from_env') as mock_docker:
            mock_docker.side_effect = Exception("Docker error")
            
            docker_service = DockerService(Mock())
            containers = docker_service.get_reqarchitect_containers()
            
            assert containers == []
    
    def test_cache_service_error(self):
        """Test cache service error handling."""
        with patch('redis.from_url') as mock_redis:
            mock_redis.side_effect = Exception("Redis error")
            
            cache_service = CacheService()
            result = cache_service.get_cached_service_endpoints("test_service")
            
            assert result is None


if __name__ == "__main__":
    pytest.main([__file__]) 