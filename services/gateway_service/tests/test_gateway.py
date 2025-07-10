import pytest
import jwt
import time
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.service_registry import ServiceRegistry, ServiceConfig, ServiceHealth, ServiceStatus
from app.rbac import RBACValidator, RBACContext, Role, Permission
from app.observability import ObservabilityManager, RequestContext

# Test client
client = TestClient(app)

class TestServiceRegistry:
    """Test service registry functionality"""
    
    def test_load_service_catalog(self):
        """Test loading service catalog from JSON"""
        registry = ServiceRegistry("service_catalog.json")
        assert len(registry.services) > 0
        assert "assessment" in registry.services
        assert "usage" in registry.services
    
    def test_get_service_by_path(self):
        """Test service resolution by path"""
        registry = ServiceRegistry("service_catalog.json")
        service_info = registry.get_service_by_path("/assessment/assessments")
        assert service_info is not None
        service_key, config = service_info
        assert service_key == "assessment"
        assert config.base_path == "/assessment"
    
    def test_service_health_check(self):
        """Test service health checking"""
        registry = ServiceRegistry("service_catalog.json")
        health = registry.health_status.get("assessment")
        assert health is not None
        assert isinstance(health, ServiceHealth)
    
    def test_circuit_breaker_logic(self):
        """Test circuit breaker pattern"""
        registry = ServiceRegistry("service_catalog.json")
        
        # Initially should be unknown
        assert registry.is_service_healthy("assessment") is False
        
        # Simulate healthy service
        health = registry.health_status["assessment"]
        health.status = ServiceStatus.HEALTHY
        assert registry.is_service_healthy("assessment") is True
        
        # Simulate circuit breaker open
        health.status = ServiceStatus.CIRCUIT_OPEN
        assert registry.is_service_healthy("assessment") is False

class TestRBACValidator:
    """Test RBAC validation logic"""
    
    def setup_method(self):
        self.validator = RBACValidator()
    
    def test_create_context(self):
        """Test RBAC context creation"""
        context = self.validator.create_context("user123", "tenant456", "Admin")
        assert context.user_id == "user123"
        assert context.tenant_id == "tenant456"
        assert context.role == Role.ADMIN
        assert len(context.permissions) > 0
    
    def test_permission_validation(self):
        """Test permission validation"""
        context = self.validator.create_context("user123", "tenant456", "Admin")
        
        # Admin should have all permissions
        assert self.validator.has_permission(context, Permission.ASSESSMENT_CREATE)
        assert self.validator.has_permission(context, Permission.ASSESSMENT_READ)
        assert self.validator.has_permission(context, Permission.ASSESSMENT_UPDATE)
        assert self.validator.has_permission(context, Permission.ASSESSMENT_DELETE)
    
    def test_viewer_permissions(self):
        """Test viewer role permissions"""
        context = self.validator.create_context("user123", "tenant456", "Viewer")
        
        # Viewer should only have read permissions
        assert self.validator.has_permission(context, Permission.ASSESSMENT_READ)
        assert not self.validator.has_permission(context, Permission.ASSESSMENT_CREATE)
        assert not self.validator.has_permission(context, Permission.ASSESSMENT_UPDATE)
        assert not self.validator.has_permission(context, Permission.ASSESSMENT_DELETE)
    
    def test_request_permission_validation(self):
        """Test request permission validation"""
        context = self.validator.create_context("user123", "tenant456", "Editor")
        
        # Editor should have create, read, update but not delete
        assert self.validator.validate_request_permission(context, "assessment", "POST")
        assert self.validator.validate_request_permission(context, "assessment", "GET")
        assert self.validator.validate_request_permission(context, "assessment", "PUT")
        assert not self.validator.validate_request_permission(context, "assessment", "DELETE")

class TestObservabilityManager:
    """Test observability functionality"""
    
    def setup_method(self):
        self.manager = ObservabilityManager()
    
    def test_create_request_context(self):
        """Test request context creation"""
        context = self.manager.create_request_context(
            method="POST",
            path="/assessment/assessments",
            user_id="user123",
            tenant_id="tenant456",
            service_target="assessment"
        )
        assert context.method == "POST"
        assert context.path == "/assessment/assessments"
        assert context.user_id == "user123"
        assert context.tenant_id == "tenant456"
        assert context.service_target == "assessment"
        assert context.request_id is not None
        assert context.correlation_id is not None
    
    def test_log_request_start(self):
        """Test request start logging"""
        context = self.manager.create_request_context("GET", "/test")
        # Should not raise exception
        self.manager.log_request_start(context)
    
    def test_log_request_end(self):
        """Test request end logging"""
        context = self.manager.create_request_context("GET", "/test")
        # Should not raise exception
        self.manager.log_request_end(context, 200)
        assert context.status_code == 200
        assert context.latency_ms is not None
    
    def test_log_rbac_decision(self):
        """Test RBAC decision logging"""
        context = self.manager.create_request_context("GET", "/test")
        # Should not raise exception
        self.manager.log_rbac_decision(context, "assessment", "GET", True, "Admin")

class TestGatewayEndpoints:
    """Test gateway API endpoints"""
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "gateway_service"
        assert "status" in data
        assert "uptime" in data
    
    def test_gateway_health_endpoint(self):
        """Test detailed gateway health endpoint"""
        response = client.get("/gateway-health")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "gateway_service"
        assert "service_health" in data
        assert "service_metrics" in data
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "gateway_uptime_seconds" in data
        assert "gateway_requests_total" in data
        assert "gateway_errors_total" in data
    
    def test_services_endpoint(self):
        """Test services listing endpoint"""
        response = client.get("/services")
        assert response.status_code == 200
        data = response.json()
        assert "services" in data
        assert "total_services" in data
        assert "overall_status" in data

class TestAuthentication:
    """Test authentication middleware"""
    
    def test_missing_token(self):
        """Test request without JWT token"""
        response = client.get("/assessment/assessments")
        assert response.status_code == 401
        assert "Missing or invalid authorization header" in response.json()["detail"]
    
    def test_invalid_token(self):
        """Test request with invalid JWT token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/assessment/assessments", headers=headers)
        assert response.status_code == 401
        assert "Invalid token" in response.json()["detail"]
    
    def test_expired_token(self):
        """Test request with expired JWT token"""
        # Create expired token
        payload = {
            "user_id": "user123",
            "tenant_id": "tenant456",
            "role": "Admin",
            "exp": time.time() - 3600  # Expired 1 hour ago
        }
        token = jwt.encode(payload, "REPLACE_WITH_REAL_SECRET", algorithm="HS256")
        
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/assessment/assessments", headers=headers)
        assert response.status_code == 401
        assert "Token has expired" in response.json()["detail"]
    
    def test_valid_token(self):
        """Test request with valid JWT token"""
        # Create valid token
        payload = {
            "user_id": "user123",
            "tenant_id": "tenant456",
            "role": "Admin",
            "exp": time.time() + 3600  # Valid for 1 hour
        }
        token = jwt.encode(payload, "REPLACE_WITH_REAL_SECRET", algorithm="HS256")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Mock the service proxy to avoid actual HTTP calls
        with patch('app.main.proxy_request_with_retry') as mock_proxy:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = b'{"test": "data"}'
            mock_response.headers = {}
            mock_proxy.return_value = mock_response
            
            response = client.get("/assessment/assessments", headers=headers)
            # Should pass authentication but fail at routing (service not found)
            assert response.status_code in [404, 503]

class TestRBACEnforcement:
    """Test RBAC enforcement"""
    
    def test_viewer_delete_denied(self):
        """Test that viewer cannot delete"""
        # Create token with viewer role
        payload = {
            "user_id": "user123",
            "tenant_id": "tenant456",
            "role": "Viewer",
            "exp": time.time() + 3600
        }
        token = jwt.encode(payload, "REPLACE_WITH_REAL_SECRET", algorithm="HS256")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Mock service resolution to avoid actual routing
        with patch('app.routing.get_service_config') as mock_get_service:
            mock_get_service.return_value = ("assessment", Mock(rbac_required=True))
            
            response = client.delete("/assessment/assessments/123", headers=headers)
            assert response.status_code == 403
            assert "Insufficient permissions" in response.json()["detail"]
    
    def test_admin_delete_allowed(self):
        """Test that admin can delete"""
        # Create token with admin role
        payload = {
            "user_id": "user123",
            "tenant_id": "tenant456",
            "role": "Admin",
            "exp": time.time() + 3600
        }
        token = jwt.encode(payload, "REPLACE_WITH_REAL_SECRET", algorithm="HS256")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Mock service resolution and proxy
        with patch('app.routing.get_service_config') as mock_get_service, \
             patch('app.main.proxy_request_with_retry') as mock_proxy:
            
            mock_get_service.return_value = ("assessment", Mock(rbac_required=True))
            mock_response = Mock()
            mock_response.status_code = 204
            mock_response.content = b''
            mock_response.headers = {}
            mock_proxy.return_value = mock_response
            
            response = client.delete("/assessment/assessments/123", headers=headers)
            # Should pass RBAC but may fail at routing
            assert response.status_code in [204, 404, 503]

class TestFaultTolerance:
    """Test fault tolerance mechanisms"""
    
    def test_service_not_found(self):
        """Test handling of unknown service"""
        payload = {
            "user_id": "user123",
            "tenant_id": "tenant456",
            "role": "Admin",
            "exp": time.time() + 3600
        }
        token = jwt.encode(payload, "REPLACE_WITH_REAL_SECRET", algorithm="HS256")
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/unknown-service/endpoint", headers=headers)
        assert response.status_code == 404
        assert "No service found for path" in response.json()["detail"]
    
    def test_unhealthy_service(self):
        """Test handling of unhealthy service"""
        payload = {
            "user_id": "user123",
            "tenant_id": "tenant456",
            "role": "Admin",
            "exp": time.time() + 3600
        }
        token = jwt.encode(payload, "REPLACE_WITH_REAL_SECRET", algorithm="HS256")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Mock service as unhealthy
        with patch('app.service_registry.ServiceRegistry.is_service_healthy') as mock_health:
            mock_health.return_value = False
            
            response = client.get("/assessment/assessments", headers=headers)
            assert response.status_code == 503
            assert "currently unavailable" in response.json()["detail"]

class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_rate_limit_exceeded(self):
        """Test rate limit enforcement"""
        payload = {
            "user_id": "user123",
            "tenant_id": "tenant456",
            "role": "Admin",
            "exp": time.time() + 3600
        }
        token = jwt.encode(payload, "REPLACE_WITH_REAL_SECRET", algorithm="HS256")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Mock rate limit store to simulate exceeded limit
        with patch('app.middleware.rate_limit_store') as mock_store:
            mock_store.__getitem__.return_value = [time.time()] * 150  # Exceed limit
            
            response = client.get("/assessment/assessments", headers=headers)
            assert response.status_code == 429
            assert "Rate limit exceeded" in response.json()["detail"]

if __name__ == "__main__":
    pytest.main([__file__]) 