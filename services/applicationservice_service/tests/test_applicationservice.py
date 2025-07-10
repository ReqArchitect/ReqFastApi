import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import redis
from unittest.mock import Mock, patch
from uuid import uuid4
import json

from app.main import app
from app.database import get_db_session
from app.models import Base, ApplicationService, ServiceLink
from app.schemas import ApplicationServiceCreate, ServiceLinkCreate
from app.config import settings

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Mock Redis client
mock_redis = Mock()

def override_get_redis_client():
    """Override Redis dependency for testing."""
    return mock_redis

# Mock JWT token
mock_jwt_token = {
    "tenant_id": str(uuid4()),
    "user_id": str(uuid4()),
    "role": "admin",
    "email": "test@example.com",
    "permissions": ["application_service:create", "application_service:read", "application_service:update", "application_service:delete"]
}

def override_get_current_user():
    """Override authentication dependency for testing."""
    return mock_jwt_token

# Override dependencies
app.dependency_overrides[get_db_session] = override_get_db
app.dependency_overrides[mock_redis] = override_get_redis_client
app.dependency_overrides[mock_jwt_token] = override_get_current_user

# Test client
client = TestClient(app)

class TestApplicationService:
    """Test cases for ApplicationService functionality."""
    
    def setup_method(self):
        """Setup test data."""
        self.tenant_id = uuid4()
        self.user_id = uuid4()
        self.service_data = {
            "name": "Test Application Service",
            "description": "A test application service",
            "service_type": "api",
            "status": "active",
            "latency_target_ms": 200,
            "availability_target_pct": 99.9,
            "version": "1.0.0",
            "delivery_channel": "http",
            "authentication_method": "jwt",
            "business_value": "high",
            "business_criticality": "high",
            "technology_stack": '{"framework": "FastAPI", "database": "PostgreSQL"}',
            "deployment_model": "microservice",
            "scaling_strategy": "horizontal",
            "security_level": "high",
            "data_classification": "internal",
            "service_endpoint": "https://api.example.com/v1",
            "documentation_link": "https://docs.example.com",
            "support_contact": "support@example.com"
        }
        
        self.link_data = {
            "linked_element_id": str(uuid4()),
            "linked_element_type": "business_process",
            "link_type": "supports",
            "relationship_strength": "strong",
            "dependency_level": "high",
            "interaction_frequency": "frequent",
            "interaction_type": "synchronous",
            "data_flow_direction": "bidirectional",
            "performance_impact": "medium",
            "latency_contribution": 50.0,
            "availability_impact": 5.0,
            "throughput_impact": 10.0,
            "error_propagation": 2.0,
            "business_criticality": "high",
            "business_value": "high",
            "alignment_score": 0.8,
            "implementation_priority": "high",
            "implementation_phase": "active",
            "resource_allocation": 25.0,
            "risk_level": "medium",
            "reliability_score": 0.9,
            "failure_impact": "high",
            "recovery_time": 30,
            "monitoring_enabled": True,
            "alerting_enabled": True,
            "logging_level": "info",
            "metrics_collection": '{"prometheus": true, "grafana": true}',
            "security_requirements": '{"encryption": "required", "authentication": "jwt"}',
            "compliance_impact": "medium",
            "data_protection": '{"gdpr": true, "sox": false}',
            "performance_contribution": 15.0,
            "success_contribution": 20.0,
            "quality_metrics": '{"response_time": "p95", "availability": "99.9%"}'
        }

    def test_create_application_service(self):
        """Test creating an application service."""
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            response = client.post(
                "/application-services/",
                json=self.service_data,
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            
            assert response.status_code == 201
            data = response.json()
            assert data["name"] == self.service_data["name"]
            assert data["service_type"] == self.service_data["service_type"]
            assert data["status"] == self.service_data["status"]
            assert "id" in data
            assert "tenant_id" in data
            assert "user_id" in data

    def test_get_application_service(self):
        """Test getting an application service by ID."""
        # First create a service
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            create_response = client.post(
                "/application-services/",
                json=self.service_data,
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            service_id = create_response.json()["id"]
            
            # Then get the service
            response = client.get(
                f"/application-services/{service_id}",
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == service_id
            assert data["name"] == self.service_data["name"]

    def test_list_application_services(self):
        """Test listing application services."""
        # Create multiple services
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            for i in range(3):
                service_data = self.service_data.copy()
                service_data["name"] = f"Test Service {i+1}"
                client.post(
                    "/application-services/",
                    json=service_data,
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
            
            # List services
            response = client.get(
                "/application-services/",
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) >= 3

    def test_update_application_service(self):
        """Test updating an application service."""
        # First create a service
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            create_response = client.post(
                "/application-services/",
                json=self.service_data,
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            service_id = create_response.json()["id"]
            
            # Update the service
            update_data = {
                "name": "Updated Application Service",
                "description": "Updated description",
                "availability_target_pct": 99.99
            }
            
            response = client.put(
                f"/application-services/{service_id}",
                json=update_data,
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == update_data["name"]
            assert data["description"] == update_data["description"]
            assert data["availability_target_pct"] == update_data["availability_target_pct"]

    def test_delete_application_service(self):
        """Test deleting an application service."""
        # First create a service
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            create_response = client.post(
                "/application-services/",
                json=self.service_data,
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            service_id = create_response.json()["id"]
            
            # Delete the service
            response = client.delete(
                f"/application-services/{service_id}",
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            
            assert response.status_code == 204
            
            # Verify service is deleted
            get_response = client.get(
                f"/application-services/{service_id}",
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            assert get_response.status_code == 404

    def test_create_service_link(self):
        """Test creating a service link."""
        # First create a service
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            create_service_response = client.post(
                "/application-services/",
                json=self.service_data,
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            service_id = create_service_response.json()["id"]
            
            # Create a link
            with patch('app.services.ServiceLinkService._emit_link_event'):
                response = client.post(
                    f"/application-services/{service_id}/links",
                    json=self.link_data,
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
                
                assert response.status_code == 201
                data = response.json()
                assert data["application_service_id"] == service_id
                assert data["linked_element_id"] == self.link_data["linked_element_id"]
                assert data["link_type"] == self.link_data["link_type"]

    def test_get_service_link(self):
        """Test getting a service link by ID."""
        # First create a service and link
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            create_service_response = client.post(
                "/application-services/",
                json=self.service_data,
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            service_id = create_service_response.json()["id"]
            
            with patch('app.services.ServiceLinkService._emit_link_event'):
                create_link_response = client.post(
                    f"/application-services/{service_id}/links",
                    json=self.link_data,
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
                link_id = create_link_response.json()["id"]
                
                # Get the link
                response = client.get(
                    f"/application-services/links/{link_id}",
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["id"] == link_id
                assert data["application_service_id"] == service_id

    def test_list_service_links(self):
        """Test listing service links."""
        # First create a service and multiple links
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            create_service_response = client.post(
                "/application-services/",
                json=self.service_data,
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            service_id = create_service_response.json()["id"]
            
            with patch('app.services.ServiceLinkService._emit_link_event'):
                for i in range(3):
                    link_data = self.link_data.copy()
                    link_data["linked_element_id"] = str(uuid4())
                    client.post(
                        f"/application-services/{service_id}/links",
                        json=link_data,
                        headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                    )
                
                # List links
                response = client.get(
                    f"/application-services/{service_id}/links",
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert len(data) >= 3

    def test_update_service_link(self):
        """Test updating a service link."""
        # First create a service and link
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            create_service_response = client.post(
                "/application-services/",
                json=self.service_data,
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            service_id = create_service_response.json()["id"]
            
            with patch('app.services.ServiceLinkService._emit_link_event'):
                create_link_response = client.post(
                    f"/application-services/{service_id}/links",
                    json=self.link_data,
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
                link_id = create_link_response.json()["id"]
                
                # Update the link
                update_data = {
                    "relationship_strength": "medium",
                    "dependency_level": "medium",
                    "performance_impact": "low"
                }
                
                response = client.put(
                    f"/application-services/links/{link_id}",
                    json=update_data,
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["relationship_strength"] == update_data["relationship_strength"]
                assert data["dependency_level"] == update_data["dependency_level"]
                assert data["performance_impact"] == update_data["performance_impact"]

    def test_delete_service_link(self):
        """Test deleting a service link."""
        # First create a service and link
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            create_service_response = client.post(
                "/application-services/",
                json=self.service_data,
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            service_id = create_service_response.json()["id"]
            
            with patch('app.services.ServiceLinkService._emit_link_event'):
                create_link_response = client.post(
                    f"/application-services/{service_id}/links",
                    json=self.link_data,
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
                link_id = create_link_response.json()["id"]
                
                # Delete the link
                response = client.delete(
                    f"/application-services/links/{link_id}",
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
                
                assert response.status_code == 204
                
                # Verify link is deleted
                get_response = client.get(
                    f"/application-services/links/{link_id}",
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
                assert get_response.status_code == 404

    def test_get_impact_map(self):
        """Test getting impact map for a service."""
        # First create a service
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            create_response = client.post(
                "/application-services/",
                json=self.service_data,
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            service_id = create_response.json()["id"]
            
            # Get impact map
            response = client.get(
                f"/application-services/{service_id}/impact-map",
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["service_id"] == service_id
            assert "direct_impacts" in data
            assert "risk_assessment" in data
            assert "total_impact_score" in data

    def test_get_performance_score(self):
        """Test getting performance score for a service."""
        # First create a service
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            create_response = client.post(
                "/application-services/",
                json=self.service_data,
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            service_id = create_response.json()["id"]
            
            # Get performance score
            response = client.get(
                f"/application-services/{service_id}/performance-score",
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["service_id"] == service_id
            assert "latency_score" in data
            assert "availability_score" in data
            assert "overall_score" in data
            assert "recommendations" in data

    def test_analyze_service(self):
        """Test analyzing a service."""
        # First create a service
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            create_response = client.post(
                "/application-services/",
                json=self.service_data,
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            service_id = create_response.json()["id"]
            
            # Analyze service
            response = client.get(
                f"/application-services/{service_id}/analysis",
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["service_id"] == service_id
            assert "operational_health" in data
            assert "business_alignment" in data
            assert "technical_debt" in data
            assert "risk_factors" in data
            assert "improvement_opportunities" in data
            assert "compliance_status" in data

    def test_get_by_service_type(self):
        """Test getting services by type."""
        # Create services with different types
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            for service_type in ["api", "ui", "data"]:
                service_data = self.service_data.copy()
                service_data["service_type"] = service_type
                client.post(
                    "/application-services/",
                    json=service_data,
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
            
            # Get API services
            response = client.get(
                "/application-services/by-type/api",
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert all(service["service_type"] == "api" for service in data)

    def test_get_by_status(self):
        """Test getting services by status."""
        # Create services with different statuses
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            for status in ["active", "inactive", "planned"]:
                service_data = self.service_data.copy()
                service_data["status"] = status
                client.post(
                    "/application-services/",
                    json=service_data,
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
            
            # Get active services
            response = client.get(
                "/application-services/by-status/active",
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert all(service["status"] == "active" for service in data)

    def test_get_active_services(self):
        """Test getting active services."""
        # Create services with different statuses
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            for status in ["active", "inactive", "planned"]:
                service_data = self.service_data.copy()
                service_data["status"] = status
                client.post(
                    "/application-services/",
                    json=service_data,
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
            
            # Get active services
            response = client.get(
                "/application-services/active",
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert all(service["status"] == "active" for service in data)

    def test_get_critical_services(self):
        """Test getting critical services."""
        # Create services with different criticality levels
        with patch('app.services.ApplicationServiceService._emit_service_event'):
            for criticality in ["low", "medium", "high", "critical"]:
                service_data = self.service_data.copy()
                service_data["business_criticality"] = criticality
                client.post(
                    "/application-services/",
                    json=service_data,
                    headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
                )
            
            # Get critical services
            response = client.get(
                "/application-services/critical",
                headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert all(service["business_criticality"] == "critical" for service in data)

    def test_enumeration_endpoints(self):
        """Test enumeration endpoints."""
        endpoints = [
            "/application-services/service-types",
            "/application-services/statuses",
            "/application-services/business-criticalities",
            "/application-services/business-values",
            "/application-services/delivery-channels",
            "/application-services/authentication-methods",
            "/application-services/deployment-models",
            "/application-services/scaling-strategies",
            "/application-services/security-levels",
            "/application-services/data-classifications",
            "/application-services/link-types",
            "/application-services/relationship-strengths",
            "/application-services/dependency-levels",
            "/application-services/interaction-frequencies",
            "/application-services/interaction-types",
            "/application-services/data-flow-directions",
            "/application-services/performance-impacts"
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            data = response.json()
            assert "values" in data
            assert isinstance(data["values"], list)
            assert len(data["values"]) > 0

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data

    def test_metrics_endpoint(self):
        """Test metrics endpoint."""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "status" in data

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "description" in data

    def test_service_info(self):
        """Test service info endpoint."""
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "description" in data
        assert "features" in data
        assert "archimate_layer" in data
        assert "archimate_element" in data

    def test_service_capabilities(self):
        """Test service capabilities endpoint."""
        response = client.get("/capabilities")
        assert response.status_code == 200
        data = response.json()
        assert "core_features" in data
        assert "archimate_integration" in data
        assert "observability" in data
        assert "security" in data
        assert "event_integration" in data

    def test_unauthorized_access(self):
        """Test unauthorized access."""
        response = client.post("/application-services/", json=self.service_data)
        assert response.status_code == 401

    def test_invalid_service_data(self):
        """Test invalid service data validation."""
        invalid_data = self.service_data.copy()
        invalid_data["name"] = ""  # Invalid: empty name
        
        response = client.post(
            "/application-services/",
            json=invalid_data,
            headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
        )
        assert response.status_code == 422

    def test_service_not_found(self):
        """Test getting non-existent service."""
        fake_id = str(uuid4())
        response = client.get(
            f"/application-services/{fake_id}",
            headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
        )
        assert response.status_code == 404

    def test_link_not_found(self):
        """Test getting non-existent link."""
        fake_id = str(uuid4())
        response = client.get(
            f"/application-services/links/{fake_id}",
            headers={"Authorization": f"Bearer {json.dumps(mock_jwt_token)}"}
        )
        assert response.status_code == 404 