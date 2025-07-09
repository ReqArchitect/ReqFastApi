import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import patch, MagicMock
from uuid import uuid4
import json
from datetime import datetime

from app.main import app
from app.database import Base, get_db
from app.models import BusinessFunction, FunctionLink
from app.schemas import CompetencyArea, Frequency, Criticality, Complexity, MaturityLevel

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

# Test data
test_tenant_id = str(uuid4())
test_user_id = str(uuid4())
test_role_id = str(uuid4())

# Mock JWT token
mock_jwt_token = {
    "tenant_id": test_tenant_id,
    "user_id": test_user_id,
    "role": "Admin"
}

@pytest.fixture
def mock_auth():
    with patch('app.deps.get_current_tenant') as mock_tenant, \
         patch('app.deps.get_current_user') as mock_user, \
         patch('app.deps.get_current_role') as mock_role:
        mock_tenant.return_value = test_tenant_id
        mock_user.return_value = test_user_id
        mock_role.return_value = "Admin"
        yield

@pytest.fixture
def mock_rbac():
    with patch('app.deps.rbac_check') as mock_rbac_func:
        def rbac_checker(permission):
            def checker(*args, **kwargs):
                return "Admin"
            return checker
        mock_rbac_func.side_effect = rbac_checker
        yield

@pytest.fixture
def sample_business_function_data():
    return {
        "name": "Architecture Governance",
        "description": "Manages enterprise architecture governance",
        "competency_area": CompetencyArea.ARCHITECTURE_GOVERNANCE,
        "organizational_unit": "IT Department",
        "owner_role_id": test_role_id,
        "input_object_type": "Architecture Request",
        "output_object_type": "Architecture Decision",
        "frequency": Frequency.ONGOING,
        "criticality": Criticality.HIGH,
        "complexity": Complexity.COMPLEX,
        "maturity_level": MaturityLevel.MATURE,
        "alignment_score": 0.85,
        "efficiency_score": 0.78,
        "effectiveness_score": 0.92,
        "strategic_importance": "high",
        "business_value": "high",
        "risk_level": "medium",
        "status": "active"
    }

class TestBusinessFunctionCRUD:
    """Test CRUD operations for business functions"""
    
    def test_create_business_function_success(self, mock_auth, mock_rbac, sample_business_function_data):
        """Test successful business function creation"""
        response = client.post(
            "/business-functions/",
            json=sample_business_function_data,
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_business_function_data["name"]
        assert data["competency_area"] == sample_business_function_data["competency_area"]
        assert data["organizational_unit"] == sample_business_function_data["organizational_unit"]
        assert data["tenant_id"] == test_tenant_id
        assert data["user_id"] == test_user_id
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_business_function_validation_error(self, mock_auth, mock_rbac):
        """Test business function creation with validation error"""
        invalid_data = {
            "name": "",  # Invalid: empty name
            "competency_area": "Invalid Area",  # Invalid: not in enum
            "organizational_unit": "IT Department"
        }
        
        response = client.post(
            "/business-functions/",
            json=invalid_data,
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 422

    def test_get_business_function_success(self, mock_auth, mock_rbac, sample_business_function_data):
        """Test successful business function retrieval"""
        # First create a business function
        create_response = client.post(
            "/business-functions/",
            json=sample_business_function_data,
            headers={"Authorization": "Bearer test-token"}
        )
        function_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(
            f"/business-functions/{function_id}",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == function_id
        assert data["name"] == sample_business_function_data["name"]

    def test_get_business_function_not_found(self, mock_auth, mock_rbac):
        """Test business function retrieval with non-existent ID"""
        non_existent_id = str(uuid4())
        
        response = client.get(
            f"/business-functions/{non_existent_id}",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 404

    def test_update_business_function_success(self, mock_auth, mock_rbac, sample_business_function_data):
        """Test successful business function update"""
        # First create a business function
        create_response = client.post(
            "/business-functions/",
            json=sample_business_function_data,
            headers={"Authorization": "Bearer test-token"}
        )
        function_id = create_response.json()["id"]
        
        # Then update it
        update_data = {
            "name": "Updated Architecture Governance",
            "description": "Updated description",
            "criticality": "critical"
        }
        
        response = client.put(
            f"/business-functions/{function_id}",
            json=update_data,
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
        assert data["criticality"] == update_data["criticality"]

    def test_delete_business_function_success(self, mock_auth, mock_rbac, sample_business_function_data):
        """Test successful business function deletion"""
        # First create a business function
        create_response = client.post(
            "/business-functions/",
            json=sample_business_function_data,
            headers={"Authorization": "Bearer test-token"}
        )
        function_id = create_response.json()["id"]
        
        # Then delete it
        response = client.delete(
            f"/business-functions/{function_id}",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 204

class TestBusinessFunctionQueries:
    """Test domain-specific query endpoints"""
    
    def test_list_business_functions_with_filters(self, mock_auth, mock_rbac, sample_business_function_data):
        """Test listing business functions with filters"""
        # Create multiple business functions
        for i in range(3):
            data = sample_business_function_data.copy()
            data["name"] = f"Function {i+1}"
            data["organizational_unit"] = f"Department {i+1}"
            
            client.post(
                "/business-functions/",
                json=data,
                headers={"Authorization": "Bearer test-token"}
            )
        
        # Test filtering by organizational unit
        response = client.get(
            "/business-functions/?organizational_unit=Department 1",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["organizational_unit"] == "Department 1"

    def test_get_business_functions_by_competency_area(self, mock_auth, mock_rbac, sample_business_function_data):
        """Test filtering by competency area"""
        # Create business function
        client.post(
            "/business-functions/",
            json=sample_business_function_data,
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Test filtering
        response = client.get(
            f"/business-functions/by-competency-area/{CompetencyArea.ARCHITECTURE_GOVERNANCE}",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(f["competency_area"] == CompetencyArea.ARCHITECTURE_GOVERNANCE for f in data)

    def test_get_business_functions_by_criticality(self, mock_auth, mock_rbac, sample_business_function_data):
        """Test filtering by criticality"""
        # Create business function
        client.post(
            "/business-functions/",
            json=sample_business_function_data,
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Test filtering
        response = client.get(
            f"/business-functions/by-criticality/{Criticality.HIGH}",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(f["criticality"] == Criticality.HIGH for f in data)

    def test_get_active_business_functions(self, mock_auth, mock_rbac, sample_business_function_data):
        """Test getting active business functions"""
        # Create business function
        client.post(
            "/business-functions/",
            json=sample_business_function_data,
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Test filtering
        response = client.get(
            "/business-functions/active",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(f["status"] == "active" for f in data)

class TestFunctionLinks:
    """Test function link operations"""
    
    def test_create_function_link_success(self, mock_auth, mock_rbac, sample_business_function_data):
        """Test successful function link creation"""
        # First create a business function
        create_response = client.post(
            "/business-functions/",
            json=sample_business_function_data,
            headers={"Authorization": "Bearer test-token"}
        )
        function_id = create_response.json()["id"]
        
        # Create link data
        link_data = {
            "linked_element_id": str(uuid4()),
            "linked_element_type": "business_role",
            "link_type": "enables",
            "relationship_strength": "strong",
            "dependency_level": "high",
            "interaction_frequency": "frequent",
            "interaction_type": "synchronous",
            "data_flow_direction": "bidirectional"
        }
        
        response = client.post(
            f"/business-functions/{function_id}/links",
            json=link_data,
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["business_function_id"] == function_id
        assert data["linked_element_id"] == link_data["linked_element_id"]
        assert data["link_type"] == link_data["link_type"]

    def test_list_function_links(self, mock_auth, mock_rbac, sample_business_function_data):
        """Test listing function links"""
        # First create a business function
        create_response = client.post(
            "/business-functions/",
            json=sample_business_function_data,
            headers={"Authorization": "Bearer test-token"}
        )
        function_id = create_response.json()["id"]
        
        # Create multiple links
        for i in range(3):
            link_data = {
                "linked_element_id": str(uuid4()),
                "linked_element_type": "business_role",
                "link_type": "enables"
            }
            
            client.post(
                f"/business-functions/{function_id}/links",
                json=link_data,
                headers={"Authorization": "Bearer test-token"}
            )
        
        # List links
        response = client.get(
            f"/business-functions/{function_id}/links",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(link["business_function_id"] == function_id for link in data)

class TestAnalysisEndpoints:
    """Test analysis and impact endpoints"""
    
    def test_get_impact_map(self, mock_auth, mock_rbac, sample_business_function_data):
        """Test impact map generation"""
        # First create a business function
        create_response = client.post(
            "/business-functions/",
            json=sample_business_function_data,
            headers={"Authorization": "Bearer test-token"}
        )
        function_id = create_response.json()["id"]
        
        # Create some links
        for i in range(3):
            link_data = {
                "linked_element_id": str(uuid4()),
                "linked_element_type": "business_role",
                "link_type": "enables"
            }
            
            client.post(
                f"/business-functions/{function_id}/links",
                json=link_data,
                headers={"Authorization": "Bearer test-token"}
            )
        
        # Get impact map
        response = client.get(
            f"/business-functions/{function_id}/impact-map",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["business_function_id"] == function_id
        assert data["linked_elements_count"] == 3
        assert "overall_impact_score" in data
        assert "last_assessed" in data

    def test_analyze_business_function(self, mock_auth, mock_rbac, sample_business_function_data):
        """Test business function analysis"""
        # First create a business function
        create_response = client.post(
            "/business-functions/",
            json=sample_business_function_data,
            headers={"Authorization": "Bearer test-token"}
        )
        function_id = create_response.json()["id"]
        
        # Analyze function
        response = client.get(
            f"/business-functions/{function_id}/analysis",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["business_function_id"] == function_id
        assert "alignment_score" in data
        assert "efficiency_score" in data
        assert "effectiveness_score" in data
        assert "risk_score" in data
        assert "strategic_importance_score" in data
        assert "business_value_score" in data
        assert "overall_health_score" in data
        assert "last_analyzed" in data

class TestUtilityEndpoints:
    """Test utility endpoints"""
    
    def test_get_competency_areas(self, mock_auth, mock_rbac):
        """Test getting competency areas"""
        response = client.get(
            "/competency-areas",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "Architecture Governance" in data

    def test_get_frequencies(self, mock_auth, mock_rbac):
        """Test getting frequencies"""
        response = client.get(
            "/frequencies",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "ongoing" in data

    def test_get_criticalities(self, mock_auth, mock_rbac):
        """Test getting criticalities"""
        response = client.get(
            "/criticalities",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "high" in data

class TestHealthAndMetrics:
    """Test health and metrics endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "business_function_service"
        assert data["version"] == "1.0.0"
        assert "status" in data
        assert "uptime" in data
        assert "database_connected" in data

    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        
        assert response.status_code == 200
        assert "business_function_service_requests_total" in response.text

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "business_function_service"
        assert data["version"] == "1.0.0"
        assert "description" in data

class TestAuthenticationAndAuthorization:
    """Test authentication and authorization"""
    
    def test_missing_authorization_header(self):
        """Test missing authorization header"""
        response = client.post("/business-functions/", json={})
        
        assert response.status_code == 401

    def test_invalid_authorization_header(self):
        """Test invalid authorization header"""
        response = client.post(
            "/business-functions/",
            json={},
            headers={"Authorization": "Invalid"}
        )
        
        assert response.status_code == 401

    def test_insufficient_permissions(self, mock_auth):
        """Test insufficient permissions"""
        with patch('app.deps.rbac_check') as mock_rbac_func:
            def rbac_checker(permission):
                def checker(*args, **kwargs):
                    raise HTTPException(status_code=403, detail="Insufficient permissions")
                return checker
            mock_rbac_func.side_effect = rbac_checker
            
            response = client.post(
                "/business-functions/",
                json={"name": "Test"},
                headers={"Authorization": "Bearer test-token"}
            )
            
            assert response.status_code == 403

class TestValidation:
    """Test input validation"""
    
    def test_score_validation(self, mock_auth, mock_rbac):
        """Test score validation"""
        invalid_data = {
            "name": "Test Function",
            "competency_area": CompetencyArea.ARCHITECTURE_GOVERNANCE,
            "organizational_unit": "IT Department",
            "alignment_score": 1.5,  # Invalid: > 1.0
            "efficiency_score": -0.1,  # Invalid: < 0.0
            "effectiveness_score": 0.5  # Valid
        }
        
        response = client.post(
            "/business-functions/",
            json=invalid_data,
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 422

    def test_availability_validation(self, mock_auth, mock_rbac):
        """Test availability validation"""
        invalid_data = {
            "name": "Test Function",
            "competency_area": CompetencyArea.ARCHITECTURE_GOVERNANCE,
            "organizational_unit": "IT Department",
            "availability_target": 150.0,  # Invalid: > 100.0
            "current_availability": -5.0  # Invalid: < 0.0
        }
        
        response = client.post(
            "/business-functions/",
            json=invalid_data,
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 422

    def test_budget_validation(self, mock_auth, mock_rbac):
        """Test budget validation"""
        invalid_data = {
            "name": "Test Function",
            "competency_area": CompetencyArea.ARCHITECTURE_GOVERNANCE,
            "organizational_unit": "IT Department",
            "budget_allocation": -1000.0  # Invalid: negative
        }
        
        response = client.post(
            "/business-functions/",
            json=invalid_data,
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__]) 