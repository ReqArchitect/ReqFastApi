import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from uuid import UUID, uuid4
from datetime import datetime
import jwt
import os

from app.main import app
from app.database import Base, get_db
from app.models import ApplicationFunction, FunctionLink
from app.schemas import FunctionType, BusinessCriticality, BusinessValue, FunctionStatus

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Test data
TEST_TENANT_ID = uuid4()
TEST_USER_ID = uuid4()
TEST_SECRET_KEY = "test-secret-key"

def create_test_token(tenant_id=TEST_TENANT_ID, user_id=TEST_USER_ID, role="Admin"):
    payload = {
        "tenant_id": str(tenant_id),
        "user_id": str(user_id),
        "role": role,
        "exp": datetime.utcnow().timestamp() + 3600
    }
    return jwt.encode(payload, TEST_SECRET_KEY, algorithm="HS256")

@pytest.fixture
def auth_headers():
    token = create_test_token()
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers():
    token = create_test_token(role="Admin")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def editor_headers():
    token = create_test_token(role="Editor")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def viewer_headers():
    token = create_test_token(role="Viewer")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_application_function():
    return {
        "name": "Test Application Function",
        "description": "A test application function",
        "purpose": "Testing purposes",
        "function_type": FunctionType.DATA_PROCESSING,
        "business_criticality": BusinessCriticality.MEDIUM,
        "business_value": BusinessValue.MEDIUM,
        "status": FunctionStatus.ACTIVE,
        "availability_target": 99.9
    }

@pytest.fixture
def sample_function_link():
    return {
        "linked_element_id": str(uuid4()),
        "linked_element_type": "business_function",
        "link_type": "supports",
        "relationship_strength": "medium",
        "dependency_level": "medium",
        "interaction_frequency": "regular",
        "interaction_type": "synchronous",
        "data_flow_direction": "bidirectional",
        "performance_impact": "low"
    }

class TestApplicationFunctionCRUD:
    """Test CRUD operations for ApplicationFunction"""

    def test_create_application_function(self, auth_headers, sample_application_function):
        """Test creating a new application function"""
        response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_application_function["name"]
        assert data["function_type"] == sample_application_function["function_type"]
        assert "id" in data
        assert "tenant_id" in data
        assert "user_id" in data

    def test_create_application_function_unauthorized(self, sample_application_function):
        """Test creating application function without authentication"""
        response = client.post(
            "/application-functions/",
            json=sample_application_function
        )
        assert response.status_code == 401

    def test_create_application_function_insufficient_permissions(self, viewer_headers, sample_application_function):
        """Test creating application function with insufficient permissions"""
        response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=viewer_headers
        )
        assert response.status_code == 403

    def test_get_application_function(self, auth_headers, sample_application_function):
        """Test getting an application function by ID"""
        # Create function first
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )
        function_id = create_response.json()["id"]

        # Get function
        response = client.get(f"/application-functions/{function_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == function_id
        assert data["name"] == sample_application_function["name"]

    def test_get_application_function_not_found(self, auth_headers):
        """Test getting non-existent application function"""
        response = client.get(f"/application-functions/{uuid4()}", headers=auth_headers)
        assert response.status_code == 404

    def test_list_application_functions(self, auth_headers, sample_application_function):
        """Test listing application functions"""
        # Create multiple functions
        for i in range(3):
            sample_application_function["name"] = f"Test Function {i}"
            client.post(
                "/application-functions/",
                json=sample_application_function,
                headers=auth_headers
            )

        response = client.get("/application-functions/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

    def test_list_application_functions_with_filtering(self, auth_headers, sample_application_function):
        """Test listing application functions with filters"""
        # Create function with specific type
        sample_application_function["function_type"] = FunctionType.USER_INTERACTION
        client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )

        # Filter by function type
        response = client.get(
            "/application-functions/?function_type=user_interaction",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert all(func["function_type"] == "user_interaction" for func in data)

    def test_update_application_function(self, auth_headers, sample_application_function):
        """Test updating an application function"""
        # Create function first
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )
        function_id = create_response.json()["id"]

        # Update function
        update_data = {"name": "Updated Function Name", "description": "Updated description"}
        response = client.put(
            f"/application-functions/{function_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Function Name"
        assert data["description"] == "Updated description"

    def test_delete_application_function(self, auth_headers, sample_application_function):
        """Test deleting an application function"""
        # Create function first
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )
        function_id = create_response.json()["id"]

        # Delete function
        response = client.delete(f"/application-functions/{function_id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify function is deleted
        get_response = client.get(f"/application-functions/{function_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_application_function_insufficient_permissions(self, editor_headers, sample_application_function):
        """Test deleting application function with insufficient permissions"""
        # Create function first
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=editor_headers
        )
        function_id = create_response.json()["id"]

        # Try to delete function
        response = client.delete(f"/application-functions/{function_id}", headers=editor_headers)
        assert response.status_code == 403

class TestFunctionLinkCRUD:
    """Test CRUD operations for FunctionLink"""

    def test_create_function_link(self, auth_headers, sample_application_function, sample_function_link):
        """Test creating a function link"""
        # Create application function first
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )
        function_id = create_response.json()["id"]

        # Create function link
        response = client.post(
            f"/application-functions/{function_id}/links",
            json=sample_function_link,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["application_function_id"] == function_id
        assert data["linked_element_id"] == sample_function_link["linked_element_id"]

    def test_list_function_links(self, auth_headers, sample_application_function, sample_function_link):
        """Test listing function links"""
        # Create application function first
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )
        function_id = create_response.json()["id"]

        # Create function link
        client.post(
            f"/application-functions/{function_id}/links",
            json=sample_function_link,
            headers=auth_headers
        )

        # List function links
        response = client.get(f"/application-functions/{function_id}/links", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_get_function_link(self, auth_headers, sample_application_function, sample_function_link):
        """Test getting a function link by ID"""
        # Create application function first
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )
        function_id = create_response.json()["id"]

        # Create function link
        link_response = client.post(
            f"/application-functions/{function_id}/links",
            json=sample_function_link,
            headers=auth_headers
        )
        link_id = link_response.json()["id"]

        # Get function link
        response = client.get(f"/application-functions/links/{link_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == link_id

    def test_update_function_link(self, auth_headers, sample_application_function, sample_function_link):
        """Test updating a function link"""
        # Create application function first
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )
        function_id = create_response.json()["id"]

        # Create function link
        link_response = client.post(
            f"/application-functions/{function_id}/links",
            json=sample_function_link,
            headers=auth_headers
        )
        link_id = link_response.json()["id"]

        # Update function link
        update_data = {"relationship_strength": "strong", "dependency_level": "high"}
        response = client.put(
            f"/application-functions/links/{link_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["relationship_strength"] == "strong"
        assert data["dependency_level"] == "high"

    def test_delete_function_link(self, auth_headers, sample_application_function, sample_function_link):
        """Test deleting a function link"""
        # Create application function first
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )
        function_id = create_response.json()["id"]

        # Create function link
        link_response = client.post(
            f"/application-functions/{function_id}/links",
            json=sample_function_link,
            headers=auth_headers
        )
        link_id = link_response.json()["id"]

        # Delete function link
        response = client.delete(f"/application-functions/links/{link_id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify link is deleted
        get_response = client.get(f"/application-functions/links/{link_id}", headers=auth_headers)
        assert get_response.status_code == 404

class TestAnalysisEndpoints:
    """Test analysis and impact endpoints"""

    def test_get_impact_map(self, auth_headers, sample_application_function, sample_function_link):
        """Test getting impact map for application function"""
        # Create application function first
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )
        function_id = create_response.json()["id"]

        # Create function link
        client.post(
            f"/application-functions/{function_id}/links",
            json=sample_function_link,
            headers=auth_headers
        )

        # Get impact map
        response = client.get(f"/application-functions/{function_id}/impact-map", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["function_id"] == function_id
        assert "direct_impacts" in data
        assert "indirect_impacts" in data
        assert "risk_assessment" in data
        assert "dependency_chain" in data
        assert "total_impact_score" in data

    def test_get_performance_score(self, auth_headers, sample_application_function):
        """Test getting performance score for application function"""
        # Create application function first
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )
        function_id = create_response.json()["id"]

        # Get performance score
        response = client.get(f"/application-functions/{function_id}/performance-score", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["function_id"] == function_id
        assert "response_time_score" in data
        assert "throughput_score" in data
        assert "availability_score" in data
        assert "overall_score" in data
        assert "recommendations" in data
        assert "performance_metrics" in data

    def test_analyze_application_function(self, auth_headers, sample_application_function):
        """Test analyzing application function"""
        # Create application function first
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )
        function_id = create_response.json()["id"]

        # Analyze application function
        response = client.get(f"/application-functions/{function_id}/analysis", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["function_id"] == function_id
        assert "operational_health" in data
        assert "business_alignment" in data
        assert "technical_debt" in data
        assert "risk_factors" in data
        assert "improvement_opportunities" in data
        assert "compliance_status" in data

class TestDomainSpecificQueries:
    """Test domain-specific query endpoints"""

    def test_get_by_function_type(self, auth_headers, sample_application_function):
        """Test getting application functions by type"""
        # Create function with specific type
        sample_application_function["function_type"] = FunctionType.USER_INTERACTION
        client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )

        # Get by function type
        response = client.get("/application-functions/by-type/user_interaction", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(func["function_type"] == "user_interaction" for func in data)

    def test_get_by_status(self, auth_headers, sample_application_function):
        """Test getting application functions by status"""
        # Create function with specific status
        sample_application_function["status"] = FunctionStatus.ACTIVE
        client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )

        # Get by status
        response = client.get("/application-functions/by-status/active", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(func["status"] == "active" for func in data)

    def test_get_active_functions(self, auth_headers, sample_application_function):
        """Test getting active application functions"""
        # Create active function
        sample_application_function["status"] = FunctionStatus.ACTIVE
        client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )

        # Get active functions
        response = client.get("/application-functions/active", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(func["status"] == "active" for func in data)

    def test_get_critical_functions(self, auth_headers, sample_application_function):
        """Test getting critical application functions"""
        # Create critical function
        sample_application_function["business_criticality"] = BusinessCriticality.CRITICAL
        client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )

        # Get critical functions
        response = client.get("/application-functions/critical", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(func["business_criticality"] == "critical" for func in data)

class TestEnumerationEndpoints:
    """Test enumeration endpoints"""

    def test_get_function_types(self, auth_headers):
        """Test getting function types"""
        response = client.get("/application-functions/function-types", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "data_processing" in data
        assert "user_interaction" in data
        assert "orchestration" in data

    def test_get_statuses(self, auth_headers):
        """Test getting statuses"""
        response = client.get("/application-functions/statuses", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "active" in data
        assert "inactive" in data
        assert "deprecated" in data

    def test_get_business_criticalities(self, auth_headers):
        """Test getting business criticalities"""
        response = client.get("/application-functions/business-criticalities", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data

    def test_get_business_values(self, auth_headers):
        """Test getting business values"""
        response = client.get("/application-functions/business-values", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data

    def test_get_operational_hours(self, auth_headers):
        """Test getting operational hours"""
        response = client.get("/application-functions/operational-hours", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "24x7" in data
        assert "business_hours" in data
        assert "on_demand" in data

    def test_get_security_levels(self, auth_headers):
        """Test getting security levels"""
        response = client.get("/application-functions/security-levels", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "basic" in data
        assert "standard" in data
        assert "high" in data
        assert "critical" in data

    def test_get_link_types(self, auth_headers):
        """Test getting link types"""
        response = client.get("/application-functions/link-types", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "realizes" in data
        assert "supports" in data
        assert "enables" in data
        assert "governs" in data

    def test_get_relationship_strengths(self, auth_headers):
        """Test getting relationship strengths"""
        response = client.get("/application-functions/relationship-strengths", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "strong" in data
        assert "medium" in data
        assert "weak" in data

    def test_get_dependency_levels(self, auth_headers):
        """Test getting dependency levels"""
        response = client.get("/application-functions/dependency-levels", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "high" in data
        assert "medium" in data
        assert "low" in data

    def test_get_interaction_frequencies(self, auth_headers):
        """Test getting interaction frequencies"""
        response = client.get("/application-functions/interaction-frequencies", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "frequent" in data
        assert "regular" in data
        assert "occasional" in data
        assert "rare" in data

    def test_get_interaction_types(self, auth_headers):
        """Test getting interaction types"""
        response = client.get("/application-functions/interaction-types", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "synchronous" in data
        assert "asynchronous" in data
        assert "batch" in data
        assert "real_time" in data
        assert "event_driven" in data

    def test_get_data_flow_directions(self, auth_headers):
        """Test getting data flow directions"""
        response = client.get("/application-functions/data-flow-directions", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "input" in data
        assert "output" in data
        assert "bidirectional" in data

    def test_get_performance_impacts(self, auth_headers):
        """Test getting performance impacts"""
        response = client.get("/application-functions/performance-impacts", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data

class TestValidation:
    """Test input validation"""

    def test_create_application_function_invalid_data(self, auth_headers):
        """Test creating application function with invalid data"""
        invalid_data = {
            "name": "",  # Empty name should fail
            "function_type": "invalid_type",  # Invalid function type
            "availability_target": 150.0  # Invalid availability (should be <= 100)
        }
        response = client.post(
            "/application-functions/",
            json=invalid_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_create_function_link_invalid_data(self, auth_headers, sample_application_function):
        """Test creating function link with invalid data"""
        # Create application function first
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=auth_headers
        )
        function_id = create_response.json()["id"]

        invalid_link_data = {
            "linked_element_id": "invalid-uuid",  # Invalid UUID
            "linked_element_type": "",  # Empty type
            "link_type": "invalid_link_type"  # Invalid link type
        }
        response = client.post(
            f"/application-functions/{function_id}/links",
            json=invalid_link_data,
            headers=auth_headers
        )
        assert response.status_code == 422

class TestHealthAndMonitoring:
    """Test health and monitoring endpoints"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "application_function_service"
        assert data["status"] == "healthy"
        assert "uptime" in data
        assert "total_requests" in data
        assert "error_rate" in data

    def test_metrics(self):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "application_function_service_requests_total" in response.text

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "application_function_service"
        assert data["version"] == "1.0.0"
        assert "documentation" in data
        assert "health" in data
        assert "metrics" in data

class TestMultiTenancy:
    """Test multi-tenancy functionality"""

    def test_tenant_isolation(self, sample_application_function):
        """Test that tenants cannot access each other's data"""
        # Create token for tenant 1
        tenant1_token = create_test_token(tenant_id=uuid4())
        tenant1_headers = {"Authorization": f"Bearer {tenant1_token}"}

        # Create token for tenant 2
        tenant2_token = create_test_token(tenant_id=uuid4())
        tenant2_headers = {"Authorization": f"Bearer {tenant2_token}"}

        # Create function for tenant 1
        create_response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=tenant1_headers
        )
        function_id = create_response.json()["id"]

        # Try to access function from tenant 2
        response = client.get(f"/application-functions/{function_id}", headers=tenant2_headers)
        assert response.status_code == 404

class TestErrorHandling:
    """Test error handling"""

    def test_invalid_jwt_token(self, sample_application_function):
        """Test with invalid JWT token"""
        invalid_headers = {"Authorization": "Bearer invalid-token"}
        response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=invalid_headers
        )
        assert response.status_code == 401

    def test_missing_authorization_header(self, sample_application_function):
        """Test without authorization header"""
        response = client.post(
            "/application-functions/",
            json=sample_application_function
        )
        assert response.status_code == 401

    def test_expired_token(self, sample_application_function):
        """Test with expired JWT token"""
        # Create expired token
        payload = {
            "tenant_id": str(TEST_TENANT_ID),
            "user_id": str(TEST_USER_ID),
            "role": "Admin",
            "exp": datetime.utcnow().timestamp() - 3600  # Expired 1 hour ago
        }
        expired_token = jwt.encode(payload, TEST_SECRET_KEY, algorithm="HS256")
        expired_headers = {"Authorization": f"Bearer {expired_token}"}

        response = client.post(
            "/application-functions/",
            json=sample_application_function,
            headers=expired_headers
        )
        assert response.status_code == 401 