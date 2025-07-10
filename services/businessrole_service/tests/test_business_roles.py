import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import jwt
import uuid
from datetime import datetime

from app.main import app
from app.database import Base, get_db
from app.models import BusinessRole, RoleLink
from app.schemas import RoleType, RoleClassification, AuthorityLevel, StrategicImportance

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
TEST_TENANT_ID = str(uuid.uuid4())
TEST_USER_ID = str(uuid.uuid4())
TEST_SECRET_KEY = "test-secret-key"

def create_test_token(role="Admin"):
    """Create a test JWT token"""
    payload = {
        "tenant_id": TEST_TENANT_ID,
        "user_id": TEST_USER_ID,
        "role": role,
        "exp": datetime.utcnow().timestamp() + 3600
    }
    return jwt.encode(payload, TEST_SECRET_KEY, algorithm="HS256")

def get_auth_headers(role="Admin"):
    """Get authentication headers"""
    token = create_test_token(role)
    return {"Authorization": f"Bearer {token}"}

class TestBusinessRoleCRUD:
    """Test business role CRUD operations"""
    
    def test_create_business_role(self):
        """Test creating a business role"""
        headers = get_auth_headers()
        data = {
            "name": "Test Enterprise Architect",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "responsibilities": "Test responsibilities",
            "required_skills": "[\"TOGAF\", \"ArchiMate\"]",
            "required_capabilities": "[\"Strategic Planning\"]",
            "role_classification": "strategic",
            "authority_level": "senior",
            "decision_making_authority": "full",
            "approval_authority": "partial",
            "strategic_importance": "high",
            "business_value": "high",
            "capability_alignment": 0.85,
            "strategic_alignment": 0.90,
            "performance_score": 0.88,
            "effectiveness_score": 0.92,
            "efficiency_score": 0.85,
            "satisfaction_score": 0.90,
            "criticality": "high",
            "complexity": "complex",
            "workload_level": "standard",
            "availability_requirement": "business_hours",
            "headcount_requirement": 2,
            "current_headcount": 1,
            "skill_gaps": "[\"Cloud Architecture\"]",
            "training_requirements": "[\"AWS Solutions Architect\"]",
            "compliance_requirements": "[\"SOX\", \"GDPR\"]",
            "risk_level": "medium",
            "audit_frequency": "quarterly",
            "status": "active",
            "operational_hours": "business_hours",
            "availability_target": 99.5,
            "current_availability": 100.0,
            "cost_center": "IT-ARCH-001",
            "budget_allocation": 250000.00,
            "salary_range_min": 120000.00,
            "salary_range_max": 180000.00,
            "total_compensation": 200000.00
        }
        
        response = client.post("/api/v1/business-roles", json=data, headers=headers)
        assert response.status_code == 201
        
        result = response.json()
        assert result["name"] == "Test Enterprise Architect"
        assert result["role_type"] == "Architecture Lead"
        assert result["organizational_unit"] == "IT Department"
        assert result["strategic_importance"] == "high"
        assert result["status"] == "active"
        assert "id" in result
        assert "tenant_id" in result
        assert "user_id" in result
        assert "created_at" in result
        assert "updated_at" in result
    
    def test_get_business_role(self):
        """Test getting a business role by ID"""
        # First create a business role
        headers = get_auth_headers()
        create_data = {
            "name": "Test Role for Get",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "high",
            "status": "active"
        }
        
        create_response = client.post("/api/v1/business-roles", json=create_data, headers=headers)
        assert create_response.status_code == 201
        role_id = create_response.json()["id"]
        
        # Now get the business role
        response = client.get(f"/api/v1/business-roles/{role_id}", headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert result["id"] == role_id
        assert result["name"] == "Test Role for Get"
        assert result["role_type"] == "Architecture Lead"
    
    def test_get_business_roles_list(self):
        """Test getting a list of business roles"""
        headers = get_auth_headers()
        
        response = client.get("/api/v1/business-roles", headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert "business_roles" in result
        assert "total" in result
        assert "skip" in result
        assert "limit" in result
        assert isinstance(result["business_roles"], list)
    
    def test_update_business_role(self):
        """Test updating a business role"""
        # First create a business role
        headers = get_auth_headers()
        create_data = {
            "name": "Test Role for Update",
            "description": "Original description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active"
        }
        
        create_response = client.post("/api/v1/business-roles", json=create_data, headers=headers)
        assert create_response.status_code == 201
        role_id = create_response.json()["id"]
        
        # Now update the business role
        update_data = {
            "name": "Updated Test Role",
            "description": "Updated description",
            "strategic_importance": "high",
            "capability_alignment": 0.95
        }
        
        response = client.put(f"/api/v1/business-roles/{role_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert result["name"] == "Updated Test Role"
        assert result["description"] == "Updated description"
        assert result["strategic_importance"] == "high"
        assert result["capability_alignment"] == 0.95
    
    def test_delete_business_role(self):
        """Test deleting a business role"""
        # First create a business role
        headers = get_auth_headers()
        create_data = {
            "name": "Test Role for Delete",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active"
        }
        
        create_response = client.post("/api/v1/business-roles", json=create_data, headers=headers)
        assert create_response.status_code == 201
        role_id = create_response.json()["id"]
        
        # Now delete the business role
        response = client.delete(f"/api/v1/business-roles/{role_id}", headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert result["message"] == "Business role deleted successfully"
        
        # Verify the role is deleted
        get_response = client.get(f"/api/v1/business-roles/{role_id}", headers=headers)
        assert get_response.status_code == 404

class TestRoleLinkCRUD:
    """Test role link CRUD operations"""
    
    def test_create_role_link(self):
        """Test creating a role link"""
        # First create a business role
        headers = get_auth_headers()
        create_role_data = {
            "name": "Test Role for Link",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active"
        }
        
        create_role_response = client.post("/api/v1/business-roles", json=create_role_data, headers=headers)
        assert create_role_response.status_code == 201
        role_id = create_role_response.json()["id"]
        
        # Now create a role link
        link_data = {
            "linked_element_id": str(uuid.uuid4()),
            "linked_element_type": "business_function",
            "link_type": "performs",
            "relationship_strength": "strong",
            "dependency_level": "high",
            "interaction_frequency": "frequent",
            "interaction_type": "synchronous",
            "responsibility_level": "primary",
            "accountability_level": "full",
            "performance_impact": "high",
            "decision_authority": "full"
        }
        
        response = client.post(f"/api/v1/business-roles/{role_id}/links", json=link_data, headers=headers)
        assert response.status_code == 201
        
        result = response.json()
        assert result["business_role_id"] == role_id
        assert result["linked_element_type"] == "business_function"
        assert result["link_type"] == "performs"
        assert result["relationship_strength"] == "strong"
        assert "id" in result
        assert "created_by" in result
        assert "created_at" in result
    
    def test_get_role_links(self):
        """Test getting role links for a business role"""
        # First create a business role
        headers = get_auth_headers()
        create_role_data = {
            "name": "Test Role for Links",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active"
        }
        
        create_role_response = client.post("/api/v1/business-roles", json=create_role_data, headers=headers)
        assert create_role_response.status_code == 201
        role_id = create_role_response.json()["id"]
        
        # Create a role link
        link_data = {
            "linked_element_id": str(uuid.uuid4()),
            "linked_element_type": "business_function",
            "link_type": "performs",
            "relationship_strength": "strong",
            "dependency_level": "high"
        }
        
        create_link_response = client.post(f"/api/v1/business-roles/{role_id}/links", json=link_data, headers=headers)
        assert create_link_response.status_code == 201
        
        # Now get the role links
        response = client.get(f"/api/v1/business-roles/{role_id}/links", headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["business_role_id"] == role_id
        assert result[0]["linked_element_type"] == "business_function"
    
    def test_update_role_link(self):
        """Test updating a role link"""
        # First create a business role and link
        headers = get_auth_headers()
        create_role_data = {
            "name": "Test Role for Link Update",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active"
        }
        
        create_role_response = client.post("/api/v1/business-roles", json=create_role_data, headers=headers)
        assert create_role_response.status_code == 201
        role_id = create_role_response.json()["id"]
        
        link_data = {
            "linked_element_id": str(uuid.uuid4()),
            "linked_element_type": "business_function",
            "link_type": "performs",
            "relationship_strength": "medium",
            "dependency_level": "medium"
        }
        
        create_link_response = client.post(f"/api/v1/business-roles/{role_id}/links", json=link_data, headers=headers)
        assert create_link_response.status_code == 201
        link_id = create_link_response.json()["id"]
        
        # Now update the role link
        update_data = {
            "relationship_strength": "strong",
            "dependency_level": "high",
            "performance_impact": "high"
        }
        
        response = client.put(f"/api/v1/role-links/{link_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert result["relationship_strength"] == "strong"
        assert result["dependency_level"] == "high"
        assert result["performance_impact"] == "high"
    
    def test_delete_role_link(self):
        """Test deleting a role link"""
        # First create a business role and link
        headers = get_auth_headers()
        create_role_data = {
            "name": "Test Role for Link Delete",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active"
        }
        
        create_role_response = client.post("/api/v1/business-roles", json=create_role_data, headers=headers)
        assert create_role_response.status_code == 201
        role_id = create_role_response.json()["id"]
        
        link_data = {
            "linked_element_id": str(uuid.uuid4()),
            "linked_element_type": "business_function",
            "link_type": "performs",
            "relationship_strength": "medium",
            "dependency_level": "medium"
        }
        
        create_link_response = client.post(f"/api/v1/business-roles/{role_id}/links", json=link_data, headers=headers)
        assert create_link_response.status_code == 201
        link_id = create_link_response.json()["id"]
        
        # Now delete the role link
        response = client.delete(f"/api/v1/role-links/{link_id}", headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert result["message"] == "Role link deleted successfully"

class TestAnalysisEndpoints:
    """Test analysis endpoints"""
    
    def test_get_responsibility_map(self):
        """Test getting responsibility map for a business role"""
        # First create a business role
        headers = get_auth_headers()
        create_role_data = {
            "name": "Test Role for Analysis",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active"
        }
        
        create_role_response = client.post("/api/v1/business-roles", json=create_role_data, headers=headers)
        assert create_role_response.status_code == 201
        role_id = create_role_response.json()["id"]
        
        # Create some role links
        link_data = {
            "linked_element_id": str(uuid.uuid4()),
            "linked_element_type": "business_function",
            "link_type": "performs",
            "relationship_strength": "strong",
            "dependency_level": "high",
            "responsibility_level": "primary",
            "accountability_level": "full",
            "performance_impact": "high"
        }
        
        client.post(f"/api/v1/business-roles/{role_id}/links", json=link_data, headers=headers)
        
        # Now get the responsibility map
        response = client.get(f"/api/v1/business-roles/{role_id}/responsibility-map", headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert result["business_role_id"] == role_id
        assert "linked_elements_count" in result
        assert "business_functions_count" in result
        assert "business_processes_count" in result
        assert "application_services_count" in result
        assert "data_objects_count" in result
        assert "stakeholders_count" in result
        assert "overall_responsibility_score" in result
        assert "last_assessed" in result
    
    def test_get_alignment_score(self):
        """Test getting alignment score for a business role"""
        # First create a business role
        headers = get_auth_headers()
        create_role_data = {
            "name": "Test Role for Alignment",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active",
            "capability_alignment": 0.85,
            "strategic_alignment": 0.90,
            "performance_score": 0.88,
            "effectiveness_score": 0.92,
            "efficiency_score": 0.85,
            "satisfaction_score": 0.90
        }
        
        create_role_response = client.post("/api/v1/business-roles", json=create_role_data, headers=headers)
        assert create_role_response.status_code == 201
        role_id = create_role_response.json()["id"]
        
        # Now get the alignment score
        response = client.get(f"/api/v1/business-roles/{role_id}/alignment-score", headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert result["business_role_id"] == role_id
        assert result["capability_alignment"] == 0.85
        assert result["strategic_alignment"] == 0.90
        assert result["performance_score"] == 0.88
        assert result["effectiveness_score"] == 0.92
        assert result["efficiency_score"] == 0.85
        assert result["satisfaction_score"] == 0.90
        assert "overall_alignment_score" in result
        assert "last_analyzed" in result

class TestDomainQueryEndpoints:
    """Test domain query endpoints"""
    
    def test_get_business_roles_by_organizational_unit(self):
        """Test getting business roles by organizational unit"""
        headers = get_auth_headers()
        
        # Create a business role with specific organizational unit
        create_data = {
            "name": "Test Role for Org Unit",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active"
        }
        
        client.post("/api/v1/business-roles", json=create_data, headers=headers)
        
        # Now query by organizational unit
        response = client.get("/api/v1/business-roles/organizational-unit/IT%20Department", headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert isinstance(result, list)
        assert len(result) >= 1
        assert result[0]["organizational_unit"] == "IT Department"
    
    def test_get_business_roles_by_role_type(self):
        """Test getting business roles by role type"""
        headers = get_auth_headers()
        
        # Create a business role with specific role type
        create_data = {
            "name": "Test Role for Role Type",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active"
        }
        
        client.post("/api/v1/business-roles", json=create_data, headers=headers)
        
        # Now query by role type
        response = client.get("/api/v1/business-roles/role-type/Architecture%20Lead", headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert isinstance(result, list)
        assert len(result) >= 1
        assert result[0]["role_type"] == "Architecture Lead"
    
    def test_get_business_roles_by_strategic_importance(self):
        """Test getting business roles by strategic importance"""
        headers = get_auth_headers()
        
        # Create a business role with specific strategic importance
        create_data = {
            "name": "Test Role for Strategic Importance",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "high",
            "status": "active"
        }
        
        client.post("/api/v1/business-roles", json=create_data, headers=headers)
        
        # Now query by strategic importance
        response = client.get("/api/v1/business-roles/strategic-importance/high", headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert isinstance(result, list)
        assert len(result) >= 1
        assert result[0]["strategic_importance"] == "high"
    
    def test_get_active_business_roles(self):
        """Test getting active business roles"""
        headers = get_auth_headers()
        
        # Create an active business role
        create_data = {
            "name": "Test Active Role",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active"
        }
        
        client.post("/api/v1/business-roles", json=create_data, headers=headers)
        
        # Now query active roles
        response = client.get("/api/v1/business-roles/active", headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert isinstance(result, list)
        assert len(result) >= 1
        assert result[0]["status"] == "active"
    
    def test_get_critical_business_roles(self):
        """Test getting critical business roles"""
        headers = get_auth_headers()
        
        # Create a critical business role
        create_data = {
            "name": "Test Critical Role",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active",
            "criticality": "critical"
        }
        
        client.post("/api/v1/business-roles", json=create_data, headers=headers)
        
        # Now query critical roles
        response = client.get("/api/v1/business-roles/critical", headers=headers)
        assert response.status_code == 200
        
        result = response.json()
        assert isinstance(result, list)
        assert len(result) >= 1
        assert result[0]["criticality"] in ["high", "critical"]

class TestAuthenticationAndAuthorization:
    """Test authentication and authorization"""
    
    def test_missing_authentication(self):
        """Test that endpoints require authentication"""
        response = client.get("/api/v1/business-roles")
        assert response.status_code == 401
    
    def test_invalid_token(self):
        """Test that invalid tokens are rejected"""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.get("/api/v1/business-roles", headers=headers)
        assert response.status_code == 401
    
    def test_insufficient_permissions(self):
        """Test that insufficient permissions are rejected"""
        # Create a token with Viewer role (limited permissions)
        headers = get_auth_headers("Viewer")
        
        # Try to create a business role (should fail for Viewer)
        data = {
            "name": "Test Role",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active"
        }
        
        response = client.post("/api/v1/business-roles", json=data, headers=headers)
        assert response.status_code == 403
    
    def test_sufficient_permissions(self):
        """Test that sufficient permissions are allowed"""
        # Create a token with Admin role (sufficient permissions)
        headers = get_auth_headers("Admin")
        
        # Try to create a business role (should succeed for Admin)
        data = {
            "name": "Test Role with Permissions",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active"
        }
        
        response = client.post("/api/v1/business-roles", json=data, headers=headers)
        assert response.status_code == 201

class TestValidation:
    """Test input validation"""
    
    def test_invalid_role_type(self):
        """Test that invalid role type is rejected"""
        headers = get_auth_headers()
        data = {
            "name": "Test Role",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Invalid Role Type",
            "strategic_importance": "medium",
            "status": "active"
        }
        
        response = client.post("/api/v1/business-roles", json=data, headers=headers)
        assert response.status_code == 422
    
    def test_invalid_score_range(self):
        """Test that invalid score ranges are rejected"""
        headers = get_auth_headers()
        data = {
            "name": "Test Role",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active",
            "capability_alignment": 1.5  # Invalid: should be 0.0 to 1.0
        }
        
        response = client.post("/api/v1/business-roles", json=data, headers=headers)
        assert response.status_code == 422
    
    def test_missing_required_fields(self):
        """Test that missing required fields are rejected"""
        headers = get_auth_headers()
        data = {
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active"
            # Missing "name" field
        }
        
        response = client.post("/api/v1/business-roles", json=data, headers=headers)
        assert response.status_code == 422
    
    def test_valid_data(self):
        """Test that valid data is accepted"""
        headers = get_auth_headers()
        data = {
            "name": "Test Valid Role",
            "description": "Test description",
            "organizational_unit": "IT Department",
            "role_type": "Architecture Lead",
            "strategic_importance": "medium",
            "status": "active",
            "capability_alignment": 0.85,
            "strategic_alignment": 0.90,
            "performance_score": 0.88,
            "effectiveness_score": 0.92,
            "efficiency_score": 0.85,
            "satisfaction_score": 0.90
        }
        
        response = client.post("/api/v1/business-roles", json=data, headers=headers)
        assert response.status_code == 201

class TestHealthAndMetrics:
    """Test health and metrics endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        result = response.json()
        assert result["status"] == "healthy"
        assert result["service"] == "business_role_service"
        assert "version" in result
        assert "timestamp" in result
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "business_role_service_requests_total" in response.text
        assert "business_role_service_request_duration_seconds" in response.text
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        
        result = response.json()
        assert result["service"] == "Business Role Service"
        assert "version" in result
        assert "description" in result
        assert "docs" in result
        assert "health" in result
        assert "metrics" in result 