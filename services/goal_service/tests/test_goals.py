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
from app.models import Goal, GoalLink
from app.schemas import GoalType, Priority, GoalStatus

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
TEST_GOAL_ID = str(uuid4())

def create_test_token(role="Admin"):
    """Create a test JWT token"""
    payload = {
        "user_id": TEST_USER_ID,
        "tenant_id": TEST_TENANT_ID,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, "test-secret", algorithm="HS256")

@pytest.fixture
def auth_headers():
    """Fixture for authentication headers"""
    token = create_test_token()
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_goal_data():
    """Fixture for test goal data"""
    return {
        "name": "Test Goal",
        "description": "Test goal description",
        "goal_type": "strategic",
        "priority": "high",
        "status": "active",
        "success_criteria": "Test success criteria",
        "key_performance_indicators": "[\"KPI1\", \"KPI2\"]",
        "measurement_frequency": "monthly",
        "target_date": (datetime.utcnow() + timedelta(days=30)).isoformat(),
        "start_date": datetime.utcnow().isoformat(),
        "review_frequency": "quarterly",
        "progress_percentage": 25,
        "progress_notes": "Test progress notes",
        "strategic_alignment": "high",
        "business_value": "high",
        "risk_level": "medium",
        "assessment_status": "in_progress",
        "assessment_score": 75,
        "assessment_notes": "Test assessment notes"
    }

@pytest.fixture
def test_goal_link_data():
    """Fixture for test goal link data"""
    return {
        "linked_element_id": str(uuid4()),
        "linked_element_type": "requirement",
        "link_type": "realizes",
        "relationship_strength": "strong",
        "contribution_level": "high"
    }

class TestAuthentication:
    """Test authentication and authorization"""
    
    def test_missing_auth_header(self):
        """Test that missing auth header returns 401"""
        response = client.get("/goals/")
        assert response.status_code == 401
        assert "Missing or invalid authorization header" in response.json()["detail"]
    
    def test_invalid_auth_header(self):
        """Test that invalid auth header returns 401"""
        response = client.get("/goals/", headers={"Authorization": "Invalid"})
        assert response.status_code == 401
        assert "Missing or invalid authorization header" in response.json()["detail"]
    
    def test_invalid_token(self):
        """Test that invalid token returns 401"""
        response = client.get("/goals/", headers={"Authorization": "Bearer invalid"})
        assert response.status_code == 401
        assert "Invalid token" in response.json()["detail"]
    
    def test_valid_token(self, auth_headers):
        """Test that valid token allows access"""
        response = client.get("/goals/", headers=auth_headers)
        assert response.status_code == 200

class TestGoalCRUD:
    """Test goal CRUD operations"""
    
    def test_create_goal(self, auth_headers, test_goal_data):
        """Test creating a goal"""
        response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == test_goal_data["name"]
        assert data["goal_type"] == test_goal_data["goal_type"]
        assert data["priority"] == test_goal_data["priority"]
        assert data["status"] == test_goal_data["status"]
        assert "id" in data
        assert "tenant_id" in data
        assert "user_id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_goal_validation(self, auth_headers):
        """Test goal creation validation"""
        # Test missing required fields
        response = client.post("/goals/", json={}, headers=auth_headers)
        assert response.status_code == 422
        
        # Test invalid goal type
        invalid_data = {"name": "Test", "goal_type": "invalid"}
        response = client.post("/goals/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422
        
        # Test invalid priority
        invalid_data = {"name": "Test", "goal_type": "strategic", "priority": "invalid"}
        response = client.post("/goals/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422
    
    def test_get_goals(self, auth_headers, test_goal_data):
        """Test getting goals list"""
        # Create a goal first
        client.post("/goals/", json=test_goal_data, headers=auth_headers)
        
        response = client.get("/goals/", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_goal(self, auth_headers, test_goal_data):
        """Test getting a specific goal"""
        # Create a goal first
        create_response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
        goal_id = create_response.json()["id"]
        
        response = client.get(f"/goals/{goal_id}", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == goal_id
        assert data["name"] == test_goal_data["name"]
    
    def test_get_goal_not_found(self, auth_headers):
        """Test getting a non-existent goal"""
        response = client.get(f"/goals/{uuid4()}", headers=auth_headers)
        assert response.status_code == 404
        assert "Goal not found" in response.json()["detail"]
    
    def test_update_goal(self, auth_headers, test_goal_data):
        """Test updating a goal"""
        # Create a goal first
        create_response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
        goal_id = create_response.json()["id"]
        
        # Update the goal
        update_data = {"name": "Updated Goal", "progress_percentage": 50}
        response = client.put(f"/goals/{goal_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Updated Goal"
        assert data["progress_percentage"] == 50
    
    def test_delete_goal(self, auth_headers, test_goal_data):
        """Test deleting a goal"""
        # Create a goal first
        create_response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
        goal_id = create_response.json()["id"]
        
        # Delete the goal
        response = client.delete(f"/goals/{goal_id}", headers=auth_headers)
        assert response.status_code == 204
        
        # Verify goal is deleted
        get_response = client.get(f"/goals/{goal_id}", headers=auth_headers)
        assert get_response.status_code == 404

class TestGoalLinks:
    """Test goal link operations"""
    
    def test_create_goal_link(self, auth_headers, test_goal_data, test_goal_link_data):
        """Test creating a goal link"""
        # Create a goal first
        create_response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
        goal_id = create_response.json()["id"]
        
        # Create a link
        response = client.post(f"/goals/{goal_id}/links", json=test_goal_link_data, headers=auth_headers)
        assert response.status_code == 201
        
        data = response.json()
        assert data["goal_id"] == goal_id
        assert data["linked_element_id"] == test_goal_link_data["linked_element_id"]
        assert data["linked_element_type"] == test_goal_link_data["linked_element_type"]
        assert data["link_type"] == test_goal_link_data["link_type"]
    
    def test_get_goal_links(self, auth_headers, test_goal_data, test_goal_link_data):
        """Test getting goal links"""
        # Create a goal first
        create_response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
        goal_id = create_response.json()["id"]
        
        # Create a link
        client.post(f"/goals/{goal_id}/links", json=test_goal_link_data, headers=auth_headers)
        
        # Get links
        response = client.get(f"/goals/{goal_id}/links", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_update_goal_link(self, auth_headers, test_goal_data, test_goal_link_data):
        """Test updating a goal link"""
        # Create a goal first
        create_response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
        goal_id = create_response.json()["id"]
        
        # Create a link
        link_response = client.post(f"/goals/{goal_id}/links", json=test_goal_link_data, headers=auth_headers)
        link_id = link_response.json()["id"]
        
        # Update the link
        update_data = {"link_type": "supports", "contribution_level": "medium"}
        response = client.put(f"/links/{link_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["link_type"] == "supports"
        assert data["contribution_level"] == "medium"
    
    def test_delete_goal_link(self, auth_headers, test_goal_data, test_goal_link_data):
        """Test deleting a goal link"""
        # Create a goal first
        create_response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
        goal_id = create_response.json()["id"]
        
        # Create a link
        link_response = client.post(f"/goals/{goal_id}/links", json=test_goal_link_data, headers=auth_headers)
        link_id = link_response.json()["id"]
        
        # Delete the link
        response = client.delete(f"/links/{link_id}", headers=auth_headers)
        assert response.status_code == 204

class TestAnalysisEndpoints:
    """Test analysis and realization mapping endpoints"""
    
    def test_get_realization_map(self, auth_headers, test_goal_data, test_goal_link_data):
        """Test getting realization map"""
        # Create a goal first
        create_response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
        goal_id = create_response.json()["id"]
        
        # Create a link
        client.post(f"/goals/{goal_id}/links", json=test_goal_link_data, headers=auth_headers)
        
        # Get realization map
        response = client.get(f"/goals/{goal_id}/realization-map", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["goal_id"] == goal_id
        assert "linked_elements_count" in data
        assert "overall_realization_score" in data
        assert "last_assessed" in data
    
    def test_get_status_summary(self, auth_headers, test_goal_data):
        """Test getting status summary"""
        # Create a goal first
        create_response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
        goal_id = create_response.json()["id"]
        
        # Get status summary
        response = client.get(f"/goals/{goal_id}/status-summary", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["goal_id"] == goal_id
        assert "status" in data
        assert "progress_percentage" in data
        assert "risk_level" in data
        assert "linked_elements_count" in data
    
    def test_analyze_goal(self, auth_headers, test_goal_data):
        """Test goal analysis"""
        # Create a goal first
        create_response = client.post("/goals/", json=test_goal_data, headers=auth_headers)
        goal_id = create_response.json()["id"]
        
        # Analyze goal
        response = client.get(f"/goals/{goal_id}/analysis", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["goal_id"] == goal_id
        assert "priority_score" in data
        assert "progress_score" in data
        assert "risk_score" in data
        assert "strategic_alignment_score" in data
        assert "business_value_score" in data
        assert "overall_health_score" in data

class TestDomainQueries:
    """Test domain-specific query endpoints"""
    
    def test_get_goals_by_type(self, auth_headers, test_goal_data):
        """Test getting goals by type"""
        # Create a goal first
        client.post("/goals/", json=test_goal_data, headers=auth_headers)
        
        response = client.get("/goals/by-type/strategic", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert all(goal["goal_type"] == "strategic" for goal in data)
    
    def test_get_goals_by_priority(self, auth_headers, test_goal_data):
        """Test getting goals by priority"""
        # Create a goal first
        client.post("/goals/", json=test_goal_data, headers=auth_headers)
        
        response = client.get("/goals/by-priority/high", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert all(goal["priority"] == "high" for goal in data)
    
    def test_get_goals_by_status(self, auth_headers, test_goal_data):
        """Test getting goals by status"""
        # Create a goal first
        client.post("/goals/", json=test_goal_data, headers=auth_headers)
        
        response = client.get("/goals/by-status/active", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert all(goal["status"] == "active" for goal in data)
    
    def test_get_active_goals(self, auth_headers, test_goal_data):
        """Test getting active goals"""
        # Create a goal first
        client.post("/goals/", json=test_goal_data, headers=auth_headers)
        
        response = client.get("/goals/active", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert all(goal["status"] == "active" for goal in data)
    
    def test_get_high_priority_goals(self, auth_headers, test_goal_data):
        """Test getting high priority goals"""
        # Create a goal first
        client.post("/goals/", json=test_goal_data, headers=auth_headers)
        
        response = client.get("/goals/high-priority", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert all(goal["priority"] in ["high", "critical"] for goal in data)

class TestUtilityEndpoints:
    """Test utility endpoints"""
    
    def test_get_goal_types(self, auth_headers):
        """Test getting goal types"""
        response = client.get("/goals/types", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert "strategic" in data
        assert "operational" in data
        assert "technical" in data
        assert "tactical" in data
    
    def test_get_priorities(self, auth_headers):
        """Test getting priorities"""
        response = client.get("/goals/priorities", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data
    
    def test_get_statuses(self, auth_headers):
        """Test getting statuses"""
        response = client.get("/goals/statuses", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert "active" in data
        assert "achieved" in data
        assert "abandoned" in data
        assert "on_hold" in data
    
    def test_get_link_types(self, auth_headers):
        """Test getting link types"""
        response = client.get("/goals/link-types", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert "realizes" in data
        assert "supports" in data
        assert "enables" in data
        assert "governs" in data
        assert "influences" in data

class TestSystemEndpoints:
    """Test system endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["service"] == "goal_service"
        assert data["version"] == "1.0.0"
        assert "status" in data
        assert "uptime" in data
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; version=0.0.4; charset=utf-8"
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["service"] == "goal_service"
        assert data["version"] == "1.0.0"
        assert "description" in data
        assert "documentation" in data 