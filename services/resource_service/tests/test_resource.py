import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from uuid import uuid4
import jwt
import os
from datetime import datetime, timedelta

from app.main import app
from app.database import Base, get_db
from app.models import Resource, ResourceLink
from app.schemas import ResourceType, Criticality, StrategicImportance, BusinessValue

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
TEST_TENANT_ID = str(uuid4())
TEST_USER_ID = str(uuid4())
TEST_SECRET_KEY = "test-secret-key"

def create_test_token(role="Admin"):
    """Create a test JWT token"""
    payload = {
        "tenant_id": TEST_TENANT_ID,
        "user_id": TEST_USER_ID,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, TEST_SECRET_KEY, algorithm="HS256")

def get_auth_headers(role="Admin"):
    """Get authentication headers"""
    token = create_test_token(role)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def db_session():
    """Database session fixture"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def sample_resource_data():
    """Sample resource data for testing"""
    return {
        "name": "Test Enterprise Architect",
        "description": "Test enterprise architect resource",
        "resource_type": "human",
        "quantity": 1.0,
        "unit_of_measure": "FTE",
        "availability": 95.0,
        "location": "Test Location",
        "deployment_status": "active",
        "criticality": "high",
        "strategic_importance": "high",
        "business_value": "high",
        "cost_per_unit": 100000.0,
        "total_cost": 100000.0,
        "budget_allocation": 100000.0,
        "cost_center": "TEST-ARCH",
        "skills_required": '{"enterprise_architecture": "expert"}',
        "capabilities_provided": '{"strategic_planning": true}',
        "expertise_level": "expert",
        "performance_metrics": '{"projects_delivered": 5}',
        "utilization_rate": 80.0,
        "efficiency_score": 0.85,
        "effectiveness_score": 0.8,
        "operational_hours": "business_hours",
        "maintenance_schedule": "Monthly reviews",
        "technology_stack": '{"tools": ["Sparx EA"]}',
        "system_requirements": '{"hardware": "Workstation"}',
        "integration_points": '{"portfolio": "PPM"}',
        "dependencies": '{"business": "Stakeholders"}',
        "governance_model": "enhanced",
        "compliance_requirements": '{"sox": true}',
        "audit_requirements": '{"quarterly": true}',
        "risk_assessment": '{"key_person": "medium"}'
    }

@pytest.fixture
def sample_resource_link_data():
    """Sample resource link data for testing"""
    return {
        "linked_element_id": str(uuid4()),
        "linked_element_type": "business_function",
        "link_type": "enables",
        "relationship_strength": "strong",
        "dependency_level": "high",
        "allocation_percentage": 75.0,
        "allocation_start_date": "2024-01-01T00:00:00Z",
        "allocation_end_date": "2024-12-31T23:59:59Z",
        "allocation_priority": "high",
        "interaction_frequency": "frequent",
        "interaction_type": "synchronous",
        "data_flow_direction": "bidirectional",
        "performance_impact": "medium",
        "efficiency_contribution": 85.0,
        "effectiveness_contribution": 80.0
    }

class TestResourceCRUD:
    """Test Resource CRUD operations"""

    def test_create_resource(self, sample_resource_data):
        """Test creating a resource"""
        headers = get_auth_headers()
        response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_resource_data["name"]
        assert data["resource_type"] == sample_resource_data["resource_type"]
        assert data["tenant_id"] == TEST_TENANT_ID
        assert data["user_id"] == TEST_USER_ID

    def test_create_resource_validation_error(self):
        """Test resource creation with validation error"""
        headers = get_auth_headers()
        invalid_data = {"name": "", "resource_type": "invalid_type"}
        response = client.post("/api/v1/resources", json=invalid_data, headers=headers)
        
        assert response.status_code == 422

    def test_get_resource(self, db_session, sample_resource_data):
        """Test getting a resource by ID"""
        # Create resource first
        headers = get_auth_headers()
        create_response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        resource_id = create_response.json()["id"]
        
        # Get resource
        response = client.get(f"/api/v1/resources/{resource_id}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == resource_id
        assert data["name"] == sample_resource_data["name"]

    def test_get_resource_not_found(self):
        """Test getting a non-existent resource"""
        headers = get_auth_headers()
        response = client.get(f"/api/v1/resources/{uuid4()}", headers=headers)
        
        assert response.status_code == 404

    def test_list_resources(self, sample_resource_data):
        """Test listing resources"""
        headers = get_auth_headers()
        
        # Create multiple resources
        for i in range(3):
            resource_data = sample_resource_data.copy()
            resource_data["name"] = f"Test Resource {i}"
            client.post("/api/v1/resources", json=resource_data, headers=headers)
        
        # List resources
        response = client.get("/api/v1/resources", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

    def test_list_resources_with_filters(self, sample_resource_data):
        """Test listing resources with filters"""
        headers = get_auth_headers()
        
        # Create resource
        client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        
        # List with filter
        response = client.get("/api/v1/resources?resource_type=human", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert all(r["resource_type"] == "human" for r in data)

    def test_update_resource(self, sample_resource_data):
        """Test updating a resource"""
        headers = get_auth_headers()
        
        # Create resource
        create_response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        resource_id = create_response.json()["id"]
        
        # Update resource
        update_data = {"name": "Updated Resource Name", "utilization_rate": 90.0}
        response = client.put(f"/api/v1/resources/{resource_id}", json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Resource Name"
        assert data["utilization_rate"] == 90.0

    def test_delete_resource(self, sample_resource_data):
        """Test deleting a resource"""
        headers = get_auth_headers()
        
        # Create resource
        create_response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        resource_id = create_response.json()["id"]
        
        # Delete resource
        response = client.delete(f"/api/v1/resources/{resource_id}", headers=headers)
        
        assert response.status_code == 204
        
        # Verify resource is deleted
        get_response = client.get(f"/api/v1/resources/{resource_id}", headers=headers)
        assert get_response.status_code == 404

class TestResourceLinkCRUD:
    """Test ResourceLink CRUD operations"""

    def test_create_resource_link(self, sample_resource_data, sample_resource_link_data):
        """Test creating a resource link"""
        headers = get_auth_headers()
        
        # Create resource first
        create_response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        resource_id = create_response.json()["id"]
        
        # Create resource link
        response = client.post(f"/api/v1/resources/{resource_id}/links", 
                             json=sample_resource_link_data, headers=headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["resource_id"] == resource_id
        assert data["linked_element_id"] == sample_resource_link_data["linked_element_id"]

    def test_list_resource_links(self, sample_resource_data, sample_resource_link_data):
        """Test listing resource links"""
        headers = get_auth_headers()
        
        # Create resource and link
        create_response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        resource_id = create_response.json()["id"]
        
        client.post(f"/api/v1/resources/{resource_id}/links", 
                   json=sample_resource_link_data, headers=headers)
        
        # List links
        response = client.get(f"/api/v1/resources/{resource_id}/links", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["resource_id"] == resource_id

    def test_update_resource_link(self, sample_resource_data, sample_resource_link_data):
        """Test updating a resource link"""
        headers = get_auth_headers()
        
        # Create resource and link
        create_response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        resource_id = create_response.json()["id"]
        
        link_response = client.post(f"/api/v1/resources/{resource_id}/links", 
                                  json=sample_resource_link_data, headers=headers)
        link_id = link_response.json()["id"]
        
        # Update link
        update_data = {"relationship_strength": "medium", "allocation_percentage": 60.0}
        response = client.put(f"/api/v1/resources/links/{link_id}", json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["relationship_strength"] == "medium"
        assert data["allocation_percentage"] == 60.0

    def test_delete_resource_link(self, sample_resource_data, sample_resource_link_data):
        """Test deleting a resource link"""
        headers = get_auth_headers()
        
        # Create resource and link
        create_response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        resource_id = create_response.json()["id"]
        
        link_response = client.post(f"/api/v1/resources/{resource_id}/links", 
                                  json=sample_resource_link_data, headers=headers)
        link_id = link_response.json()["id"]
        
        # Delete link
        response = client.delete(f"/api/v1/resources/links/{link_id}", headers=headers)
        
        assert response.status_code == 204

class TestAnalysisEndpoints:
    """Test analysis and impact endpoints"""

    def test_get_impact_score(self, sample_resource_data):
        """Test getting impact score"""
        headers = get_auth_headers()
        
        # Create resource
        create_response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        resource_id = create_response.json()["id"]
        
        # Get impact score
        response = client.get(f"/api/v1/resources/{resource_id}/impact-score", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["resource_id"] == resource_id
        assert "strategic_impact_score" in data
        assert "operational_impact_score" in data
        assert "financial_impact_score" in data
        assert "risk_impact_score" in data
        assert "overall_impact_score" in data

    def test_get_allocation_map(self, sample_resource_data, sample_resource_link_data):
        """Test getting allocation map"""
        headers = get_auth_headers()
        
        # Create resource and link
        create_response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        resource_id = create_response.json()["id"]
        
        client.post(f"/api/v1/resources/{resource_id}/links", 
                   json=sample_resource_link_data, headers=headers)
        
        # Get allocation map
        response = client.get(f"/api/v1/resources/{resource_id}/allocation-map", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["resource_id"] == resource_id
        assert "total_allocated" in data
        assert "allocation_breakdown" in data
        assert "utilization_analysis" in data

    def test_analyze_resource(self, sample_resource_data):
        """Test resource analysis"""
        headers = get_auth_headers()
        
        # Create resource
        create_response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        resource_id = create_response.json()["id"]
        
        # Analyze resource
        response = client.get(f"/api/v1/resources/{resource_id}/analysis", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["resource_id"] == resource_id
        assert "performance_analysis" in data
        assert "cost_analysis" in data
        assert "utilization_analysis" in data
        assert "risk_assessment" in data

class TestDomainSpecificQueries:
    """Test domain-specific query endpoints"""

    def test_get_resources_by_type(self, sample_resource_data):
        """Test getting resources by type"""
        headers = get_auth_headers()
        
        # Create resource
        client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        
        # Get by type
        response = client.get("/api/v1/resources/by-type/human", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert all(r["resource_type"] == "human" for r in data)

    def test_get_resources_by_status(self, sample_resource_data):
        """Test getting resources by status"""
        headers = get_auth_headers()
        
        # Create resource
        client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        
        # Get by status
        response = client.get("/api/v1/resources/by-status/active", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert all(r["deployment_status"] == "active" for r in data)

    def test_get_active_resources(self, sample_resource_data):
        """Test getting active resources"""
        headers = get_auth_headers()
        
        # Create resource
        client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        
        # Get active resources
        response = client.get("/api/v1/resources/active", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert all(r["deployment_status"] == "active" for r in data)

    def test_get_critical_resources(self, sample_resource_data):
        """Test getting critical resources"""
        headers = get_auth_headers()
        
        # Create resource
        client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        
        # Get critical resources
        response = client.get("/api/v1/resources/critical", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert all(r["criticality"] == "critical" for r in data)

class TestEnumerationEndpoints:
    """Test enumeration endpoints"""

    def test_get_resource_types(self):
        """Test getting resource types"""
        headers = get_auth_headers()
        response = client.get("/api/v1/resources/resource-types", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "human" in data
        assert "system" in data
        assert "financial" in data
        assert "knowledge" in data

    def test_get_deployment_statuses(self):
        """Test getting deployment statuses"""
        headers = get_auth_headers()
        response = client.get("/api/v1/resources/deployment-statuses", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "active" in data
        assert "inactive" in data
        assert "planned" in data
        assert "retired" in data

    def test_get_criticalities(self):
        """Test getting criticalities"""
        headers = get_auth_headers()
        response = client.get("/api/v1/resources/criticalities", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data

class TestRBAC:
    """Test Role-Based Access Control"""

    def test_owner_permissions(self, sample_resource_data):
        """Test Owner role permissions"""
        headers = get_auth_headers("Owner")
        
        # Create resource
        response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        assert response.status_code == 201
        
        resource_id = response.json()["id"]
        
        # Read resource
        response = client.get(f"/api/v1/resources/{resource_id}", headers=headers)
        assert response.status_code == 200
        
        # Update resource
        response = client.put(f"/api/v1/resources/{resource_id}", 
                            json={"name": "Updated"}, headers=headers)
        assert response.status_code == 200
        
        # Delete resource
        response = client.delete(f"/api/v1/resources/{resource_id}", headers=headers)
        assert response.status_code == 204

    def test_admin_permissions(self, sample_resource_data):
        """Test Admin role permissions"""
        headers = get_auth_headers("Admin")
        
        # Create resource
        response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        assert response.status_code == 201
        
        resource_id = response.json()["id"]
        
        # Read resource
        response = client.get(f"/api/v1/resources/{resource_id}", headers=headers)
        assert response.status_code == 200
        
        # Update resource
        response = client.put(f"/api/v1/resources/{resource_id}", 
                            json={"name": "Updated"}, headers=headers)
        assert response.status_code == 200
        
        # Delete resource
        response = client.delete(f"/api/v1/resources/{resource_id}", headers=headers)
        assert response.status_code == 204

    def test_editor_permissions(self, sample_resource_data):
        """Test Editor role permissions"""
        headers = get_auth_headers("Editor")
        
        # Create resource
        response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        assert response.status_code == 201
        
        resource_id = response.json()["id"]
        
        # Read resource
        response = client.get(f"/api/v1/resources/{resource_id}", headers=headers)
        assert response.status_code == 200
        
        # Update resource
        response = client.put(f"/api/v1/resources/{resource_id}", 
                            json={"name": "Updated"}, headers=headers)
        assert response.status_code == 200
        
        # Delete resource (should fail)
        response = client.delete(f"/api/v1/resources/{resource_id}", headers=headers)
        assert response.status_code == 403

    def test_viewer_permissions(self, sample_resource_data):
        """Test Viewer role permissions"""
        headers = get_auth_headers("Viewer")
        
        # Create resource (should fail)
        response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        assert response.status_code == 403
        
        # Create resource with Admin role first
        admin_headers = get_auth_headers("Admin")
        create_response = client.post("/api/v1/resources", json=sample_resource_data, headers=admin_headers)
        resource_id = create_response.json()["id"]
        
        # Read resource (should succeed)
        response = client.get(f"/api/v1/resources/{resource_id}", headers=headers)
        assert response.status_code == 200
        
        # Update resource (should fail)
        response = client.put(f"/api/v1/resources/{resource_id}", 
                            json={"name": "Updated"}, headers=headers)
        assert response.status_code == 403
        
        # Delete resource (should fail)
        response = client.delete(f"/api/v1/resources/{resource_id}", headers=headers)
        assert response.status_code == 403

class TestAuthentication:
    """Test authentication and authorization"""

    def test_missing_token(self, sample_resource_data):
        """Test missing authentication token"""
        response = client.post("/api/v1/resources", json=sample_resource_data)
        assert response.status_code == 401

    def test_invalid_token(self, sample_resource_data):
        """Test invalid authentication token"""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        assert response.status_code == 401

    def test_expired_token(self, sample_resource_data):
        """Test expired authentication token"""
        # Create expired token
        payload = {
            "tenant_id": TEST_TENANT_ID,
            "user_id": TEST_USER_ID,
            "role": "Admin",
            "exp": datetime.utcnow() - timedelta(hours=1)  # Expired
        }
        expired_token = jwt.encode(payload, TEST_SECRET_KEY, algorithm="HS256")
        headers = {"Authorization": f"Bearer {expired_token}"}
        
        response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        assert response.status_code == 401

class TestValidation:
    """Test input validation"""

    def test_resource_validation(self):
        """Test resource field validation"""
        headers = get_auth_headers()
        
        # Test invalid resource type
        invalid_data = {
            "name": "Test Resource",
            "resource_type": "invalid_type",
            "quantity": -1,  # Invalid quantity
            "availability": 150  # Invalid availability
        }
        response = client.post("/api/v1/resources", json=invalid_data, headers=headers)
        assert response.status_code == 422

    def test_resource_link_validation(self, sample_resource_data):
        """Test resource link field validation"""
        headers = get_auth_headers()
        
        # Create resource first
        create_response = client.post("/api/v1/resources", json=sample_resource_data, headers=headers)
        resource_id = create_response.json()["id"]
        
        # Test invalid link data
        invalid_link_data = {
            "linked_element_id": str(uuid4()),
            "linked_element_type": "business_function",
            "link_type": "invalid_type",
            "allocation_percentage": 150  # Invalid percentage
        }
        response = client.post(f"/api/v1/resources/{resource_id}/links", 
                             json=invalid_link_data, headers=headers)
        assert response.status_code == 422

class TestHealthAndMetrics:
    """Test health and metrics endpoints"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "resource_service"

    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        # Should return Prometheus metrics
        assert "resource_service_requests_total" in response.text

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Resource Service"
        assert data["version"] == "1.0.0" 