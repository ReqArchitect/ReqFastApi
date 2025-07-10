import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import Mock, patch
import uuid
from datetime import datetime

from app.main import app
from app.database import Base, get_db
from app.models import BusinessProcess, ProcessStep, ProcessLink
from app.schemas import ProcessType, Criticality, Complexity, AutomationLevel, ProcessStatus

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
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

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_tenant_id():
    return str(uuid.uuid4())

@pytest.fixture
def test_user_id():
    return str(uuid.uuid4())

@pytest.fixture
def mock_jwt_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0LXVzZXIiLCJ0ZW5hbnRfaWQiOiJ0ZXN0LXRlbmFudCIsInJvbGUiOiJlZGl0b3IifQ.test"

@pytest.fixture
def mock_auth_header(mock_jwt_token):
    return {"Authorization": f"Bearer {mock_jwt_token}"}

@pytest.fixture
def sample_business_process_data():
    return {
        "name": "Test Business Process",
        "description": "A test business process",
        "process_type": "operational",
        "input_object_type": "Test Input",
        "output_object_type": "Test Output",
        "organizational_unit": "Test Department",
        "process_classification": "operational",
        "criticality": "medium",
        "complexity": "medium",
        "automation_level": "manual",
        "performance_score": 0.8,
        "effectiveness_score": 0.85,
        "efficiency_score": 0.75,
        "quality_score": 0.9,
        "status": "active",
        "priority": "medium",
        "frequency": "daily",
        "duration_target": 4.0,
        "duration_average": 3.8,
        "volume_target": 100,
        "volume_actual": 95
    }

@pytest.fixture
def sample_process_step_data():
    return {
        "step_order": 1,
        "name": "Test Step",
        "description": "A test process step",
        "step_type": "task",
        "complexity": "medium",
        "duration_estimate": 0.5,
        "duration_actual": 0.4,
        "performance_score": 0.9,
        "quality_score": 0.95,
        "efficiency_score": 0.85,
        "bottleneck_indicator": False,
        "automation_level": "automated",
        "approval_required": False
    }

@pytest.fixture
def sample_process_link_data():
    return {
        "linked_element_id": str(uuid.uuid4()),
        "linked_element_type": "business_function",
        "link_type": "realizes",
        "relationship_strength": "strong",
        "dependency_level": "high",
        "interaction_frequency": "frequent",
        "interaction_type": "synchronous",
        "responsibility_level": "primary",
        "performance_impact": "high",
        "business_value_impact": "high",
        "risk_impact": "medium",
        "flow_direction": "bidirectional",
        "sequence_order": 1,
        "handoff_type": "automated"
    }

class TestBusinessProcessCRUD:
    """Test business process CRUD operations"""
    
    @patch('app.deps.get_current_user')
    def test_create_business_process(self, mock_get_current_user, client, sample_business_process_data, mock_auth_header):
        """Test creating a business process"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "editor"
        }
        
        response = client.post(
            "/api/v1/business-processes/",
            json=sample_business_process_data,
            headers=mock_auth_header
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_business_process_data["name"]
        assert data["process_type"] == sample_business_process_data["process_type"]
        assert "id" in data
        assert "tenant_id" in data
        assert "user_id" in data
    
    @patch('app.deps.get_current_user')
    def test_get_business_processes(self, mock_get_current_user, client, mock_auth_header):
        """Test getting business processes list"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "viewer"
        }
        
        response = client.get(
            "/api/v1/business-processes/",
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "business_processes" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data
    
    @patch('app.deps.get_current_user')
    def test_get_business_process(self, mock_get_current_user, client, mock_auth_header):
        """Test getting a specific business process"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "viewer"
        }
        
        # First create a business process
        sample_data = {
            "name": "Test Process",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        create_response = client.post(
            "/api/v1/business-processes/",
            json=sample_data,
            headers=mock_auth_header
        )
        
        process_id = create_response.json()["id"]
        
        # Then get it
        response = client.get(
            f"/api/v1/business-processes/{process_id}",
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == process_id
        assert data["name"] == sample_data["name"]
    
    @patch('app.deps.get_current_user')
    def test_update_business_process(self, mock_get_current_user, client, mock_auth_header):
        """Test updating a business process"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "editor"
        }
        
        # First create a business process
        sample_data = {
            "name": "Original Name",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        create_response = client.post(
            "/api/v1/business-processes/",
            json=sample_data,
            headers=mock_auth_header
        )
        
        process_id = create_response.json()["id"]
        
        # Then update it
        update_data = {
            "name": "Updated Name",
            "performance_score": 0.95
        }
        
        response = client.put(
            f"/api/v1/business-processes/{process_id}",
            json=update_data,
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["performance_score"] == update_data["performance_score"]
    
    @patch('app.deps.get_current_user')
    def test_delete_business_process(self, mock_get_current_user, client, mock_auth_header):
        """Test deleting a business process"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "admin"
        }
        
        # First create a business process
        sample_data = {
            "name": "To Delete",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        create_response = client.post(
            "/api/v1/business-processes/",
            json=sample_data,
            headers=mock_auth_header
        )
        
        process_id = create_response.json()["id"]
        
        # Then delete it
        response = client.delete(
            f"/api/v1/business-processes/{process_id}",
            headers=mock_auth_header
        )
        
        assert response.status_code == 204

class TestBusinessProcessAnalysis:
    """Test business process analysis endpoints"""
    
    @patch('app.deps.get_current_user')
    def test_get_process_flow_map(self, mock_get_current_user, client, mock_auth_header):
        """Test getting process flow map"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "viewer"
        }
        
        # Create a business process first
        sample_data = {
            "name": "Test Process",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        create_response = client.post(
            "/api/v1/business-processes/",
            json=sample_data,
            headers=mock_auth_header
        )
        
        process_id = create_response.json()["id"]
        
        # Get flow map
        response = client.get(
            f"/api/v1/business-processes/{process_id}/flow-map",
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["business_process_id"] == process_id
        assert "total_steps" in data
        assert "flow_complexity_score" in data
        assert "last_analyzed" in data
    
    @patch('app.deps.get_current_user')
    def test_get_process_realization_health(self, mock_get_current_user, client, mock_auth_header):
        """Test getting process realization health"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "viewer"
        }
        
        # Create a business process first
        sample_data = {
            "name": "Test Process",
            "process_type": "operational",
            "organizational_unit": "Test Dept",
            "performance_score": 0.8,
            "effectiveness_score": 0.85,
            "efficiency_score": 0.75,
            "quality_score": 0.9
        }
        
        create_response = client.post(
            "/api/v1/business-processes/",
            json=sample_data,
            headers=mock_auth_header
        )
        
        process_id = create_response.json()["id"]
        
        # Get realization health
        response = client.get(
            f"/api/v1/business-processes/{process_id}/realization-health",
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["business_process_id"] == process_id
        assert "performance_score" in data
        assert "effectiveness_score" in data
        assert "efficiency_score" in data
        assert "quality_score" in data
        assert "overall_health_score" in data
        assert "last_assessed" in data

class TestDomainQueries:
    """Test domain query endpoints"""
    
    @patch('app.deps.get_current_user')
    def test_get_business_processes_by_role(self, mock_get_current_user, client, mock_auth_header):
        """Test getting business processes by role"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "viewer"
        }
        
        role_id = str(uuid.uuid4())
        
        response = client.get(
            f"/api/v1/business-processes/by-role/{role_id}",
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @patch('app.deps.get_current_user')
    def test_get_business_processes_by_function(self, mock_get_current_user, client, mock_auth_header):
        """Test getting business processes by function"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "viewer"
        }
        
        function_id = str(uuid.uuid4())
        
        response = client.get(
            f"/api/v1/business-processes/by-function/{function_id}",
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @patch('app.deps.get_current_user')
    def test_get_business_processes_by_goal(self, mock_get_current_user, client, mock_auth_header):
        """Test getting business processes by goal"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "viewer"
        }
        
        goal_id = str(uuid.uuid4())
        
        response = client.get(
            f"/api/v1/business-processes/by-goal/{goal_id}",
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @patch('app.deps.get_current_user')
    def test_get_business_processes_by_status(self, mock_get_current_user, client, mock_auth_header):
        """Test getting business processes by status"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "viewer"
        }
        
        response = client.get(
            "/api/v1/business-processes/by-status/active",
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @patch('app.deps.get_current_user')
    def test_get_business_processes_by_criticality(self, mock_get_current_user, client, mock_auth_header):
        """Test getting business processes by criticality"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "viewer"
        }
        
        response = client.get(
            "/api/v1/business-processes/by-criticality/medium",
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

class TestProcessSteps:
    """Test process steps CRUD operations"""
    
    @patch('app.deps.get_current_user')
    def test_create_process_step(self, mock_get_current_user, client, sample_process_step_data, mock_auth_header):
        """Test creating a process step"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "editor"
        }
        
        # First create a business process
        process_data = {
            "name": "Test Process",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        process_response = client.post(
            "/api/v1/business-processes/",
            json=process_data,
            headers=mock_auth_header
        )
        
        process_id = process_response.json()["id"]
        
        # Then create a step
        response = client.post(
            f"/api/v1/business-processes/{process_id}/steps/",
            json=sample_process_step_data,
            headers=mock_auth_header
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_process_step_data["name"]
        assert data["business_process_id"] == process_id
        assert "id" in data
    
    @patch('app.deps.get_current_user')
    def test_get_process_steps(self, mock_get_current_user, client, mock_auth_header):
        """Test getting process steps"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "viewer"
        }
        
        # First create a business process
        process_data = {
            "name": "Test Process",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        process_response = client.post(
            "/api/v1/business-processes/",
            json=process_data,
            headers=mock_auth_header
        )
        
        process_id = process_response.json()["id"]
        
        # Then get steps
        response = client.get(
            f"/api/v1/business-processes/{process_id}/steps/",
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @patch('app.deps.get_current_user')
    def test_update_process_step(self, mock_get_current_user, client, mock_auth_header):
        """Test updating a process step"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "editor"
        }
        
        # First create a business process and step
        process_data = {
            "name": "Test Process",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        process_response = client.post(
            "/api/v1/business-processes/",
            json=process_data,
            headers=mock_auth_header
        )
        
        process_id = process_response.json()["id"]
        
        step_data = {
            "step_order": 1,
            "name": "Original Step",
            "step_type": "task"
        }
        
        step_response = client.post(
            f"/api/v1/business-processes/{process_id}/steps/",
            json=step_data,
            headers=mock_auth_header
        )
        
        step_id = step_response.json()["id"]
        
        # Then update the step
        update_data = {
            "name": "Updated Step",
            "performance_score": 0.95
        }
        
        response = client.put(
            f"/api/v1/steps/{step_id}",
            json=update_data,
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["performance_score"] == update_data["performance_score"]
    
    @patch('app.deps.get_current_user')
    def test_delete_process_step(self, mock_get_current_user, client, mock_auth_header):
        """Test deleting a process step"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "editor"
        }
        
        # First create a business process and step
        process_data = {
            "name": "Test Process",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        process_response = client.post(
            "/api/v1/business-processes/",
            json=process_data,
            headers=mock_auth_header
        )
        
        process_id = process_response.json()["id"]
        
        step_data = {
            "step_order": 1,
            "name": "To Delete",
            "step_type": "task"
        }
        
        step_response = client.post(
            f"/api/v1/business-processes/{process_id}/steps/",
            json=step_data,
            headers=mock_auth_header
        )
        
        step_id = step_response.json()["id"]
        
        # Then delete the step
        response = client.delete(
            f"/api/v1/steps/{step_id}",
            headers=mock_auth_header
        )
        
        assert response.status_code == 204

class TestProcessLinks:
    """Test process links CRUD operations"""
    
    @patch('app.deps.get_current_user')
    def test_create_process_link(self, mock_get_current_user, client, sample_process_link_data, mock_auth_header):
        """Test creating a process link"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "editor"
        }
        
        # First create a business process
        process_data = {
            "name": "Test Process",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        process_response = client.post(
            "/api/v1/business-processes/",
            json=process_data,
            headers=mock_auth_header
        )
        
        process_id = process_response.json()["id"]
        
        # Then create a link
        response = client.post(
            f"/api/v1/business-processes/{process_id}/links/",
            json=sample_process_link_data,
            headers=mock_auth_header
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["business_process_id"] == process_id
        assert data["linked_element_type"] == sample_process_link_data["linked_element_type"]
        assert data["link_type"] == sample_process_link_data["link_type"]
        assert "id" in data
    
    @patch('app.deps.get_current_user')
    def test_get_process_links(self, mock_get_current_user, client, mock_auth_header):
        """Test getting process links"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "viewer"
        }
        
        # First create a business process
        process_data = {
            "name": "Test Process",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        process_response = client.post(
            "/api/v1/business-processes/",
            json=process_data,
            headers=mock_auth_header
        )
        
        process_id = process_response.json()["id"]
        
        # Then get links
        response = client.get(
            f"/api/v1/business-processes/{process_id}/links/",
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @patch('app.deps.get_current_user')
    def test_update_process_link(self, mock_get_current_user, client, mock_auth_header):
        """Test updating a process link"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "editor"
        }
        
        # First create a business process and link
        process_data = {
            "name": "Test Process",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        process_response = client.post(
            "/api/v1/business-processes/",
            json=process_data,
            headers=mock_auth_header
        )
        
        process_id = process_response.json()["id"]
        
        link_data = {
            "linked_element_id": str(uuid.uuid4()),
            "linked_element_type": "business_function",
            "link_type": "realizes"
        }
        
        link_response = client.post(
            f"/api/v1/business-processes/{process_id}/links/",
            json=link_data,
            headers=mock_auth_header
        )
        
        link_id = link_response.json()["id"]
        
        # Then update the link
        update_data = {
            "relationship_strength": "medium",
            "performance_impact": "medium"
        }
        
        response = client.put(
            f"/api/v1/links/{link_id}",
            json=update_data,
            headers=mock_auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["relationship_strength"] == update_data["relationship_strength"]
        assert data["performance_impact"] == update_data["performance_impact"]
    
    @patch('app.deps.get_current_user')
    def test_delete_process_link(self, mock_get_current_user, client, mock_auth_header):
        """Test deleting a process link"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "editor"
        }
        
        # First create a business process and link
        process_data = {
            "name": "Test Process",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        process_response = client.post(
            "/api/v1/business-processes/",
            json=process_data,
            headers=mock_auth_header
        )
        
        process_id = process_response.json()["id"]
        
        link_data = {
            "linked_element_id": str(uuid.uuid4()),
            "linked_element_type": "business_function",
            "link_type": "realizes"
        }
        
        link_response = client.post(
            f"/api/v1/business-processes/{process_id}/links/",
            json=link_data,
            headers=mock_auth_header
        )
        
        link_id = link_response.json()["id"]
        
        # Then delete the link
        response = client.delete(
            f"/api/v1/links/{link_id}",
            headers=mock_auth_header
        )
        
        assert response.status_code == 204

class TestAuthentication:
    """Test authentication and authorization"""
    
    def test_unauthorized_access(self, client):
        """Test accessing endpoints without authentication"""
        response = client.get("/api/v1/business-processes/")
        assert response.status_code == 401
    
    def test_invalid_token(self, client):
        """Test accessing endpoints with invalid token"""
        response = client.get(
            "/api/v1/business-processes/",
            headers={"Authorization": "Bearer invalid-token"}
        )
        assert response.status_code == 401
    
    @patch('app.deps.get_current_user')
    def test_insufficient_permissions(self, mock_get_current_user, client, mock_auth_header):
        """Test accessing endpoints with insufficient permissions"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "viewer"
        }
        
        # Try to create with viewer role
        sample_data = {
            "name": "Test Process",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        response = client.post(
            "/api/v1/business-processes/",
            json=sample_data,
            headers=mock_auth_header
        )
        
        # Should fail due to insufficient permissions
        assert response.status_code == 403

class TestValidation:
    """Test input validation"""
    
    @patch('app.deps.get_current_user')
    def test_invalid_business_process_data(self, mock_get_current_user, client, mock_auth_header):
        """Test creating business process with invalid data"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "editor"
        }
        
        # Missing required fields
        invalid_data = {
            "name": "",  # Empty name
            "process_type": "invalid_type",  # Invalid enum
            "performance_score": 1.5  # Invalid score range
        }
        
        response = client.post(
            "/api/v1/business-processes/",
            json=invalid_data,
            headers=mock_auth_header
        )
        
        assert response.status_code == 422
    
    @patch('app.deps.get_current_user')
    def test_invalid_process_step_data(self, mock_get_current_user, client, mock_auth_header):
        """Test creating process step with invalid data"""
        mock_get_current_user.return_value = {
            "user_id": "test-user",
            "tenant_id": "test-tenant",
            "role": "editor"
        }
        
        # First create a business process
        process_data = {
            "name": "Test Process",
            "process_type": "operational",
            "organizational_unit": "Test Dept"
        }
        
        process_response = client.post(
            "/api/v1/business-processes/",
            json=process_data,
            headers=mock_auth_header
        )
        
        process_id = process_response.json()["id"]
        
        # Invalid step data
        invalid_step_data = {
            "step_order": 0,  # Invalid order
            "name": "",  # Empty name
            "step_type": "invalid_type",  # Invalid enum
            "performance_score": 1.5  # Invalid score range
        }
        
        response = client.post(
            f"/api/v1/business-processes/{process_id}/steps/",
            json=invalid_step_data,
            headers=mock_auth_header
        )
        
        assert response.status_code == 422

class TestHealthAndMetrics:
    """Test health and metrics endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "businessprocess_service"
        assert "version" in data
        assert "timestamp" in data
    
    def test_metrics(self, client):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        # Should return Prometheus metrics format
        assert "businessprocess_service_requests_total" in response.text

if __name__ == "__main__":
    pytest.main([__file__]) 