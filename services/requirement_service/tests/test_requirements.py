import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Requirement, RequirementLink
from uuid import uuid4
import jwt
import os

# Test database setup
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

# Create test tables
Base.metadata.create_all(bind=engine)

# Test client
client = TestClient(app)

# Test data
TEST_TENANT_ID = str(uuid4())
TEST_USER_ID = str(uuid4())
TEST_JWT_SECRET = "test_secret_key"

def create_test_token(tenant_id=TEST_TENANT_ID, user_id=TEST_USER_ID, role="Admin"):
    """Create a test JWT token"""
    payload = {
        "user_id": user_id,
        "tenant_id": tenant_id,
        "role": role,
        "iat": 1516239022,
        "exp": 1516239922
    }
    return jwt.encode(payload, TEST_JWT_SECRET, algorithm="HS256")

@pytest.fixture
def auth_headers():
    """Fixture for authentication headers"""
    token = create_test_token()
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_requirement_data():
    """Fixture for test requirement data"""
    return {
        "name": "Test Requirement",
        "description": "A test requirement for testing",
        "requirement_type": "functional",
        "priority": "high",
        "status": "draft",
        "source": "Test Source",
        "acceptance_criteria": "Must pass all tests",
        "validation_method": "test",
        "compliance_required": True
    }

class TestHealthEndpoint:
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "requirement_service"
        assert data["status"] == "healthy"

class TestRequirementsCRUD:
    def test_create_requirement(self, auth_headers, test_requirement_data):
        """Test creating a requirement"""
        response = client.post("/requirements/", json=test_requirement_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == test_requirement_data["name"]
        assert data["requirement_type"] == test_requirement_data["requirement_type"]
        assert "id" in data
        assert "tenant_id" in data

    def test_get_requirements(self, auth_headers):
        """Test getting requirements list"""
        response = client.get("/requirements/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_requirement_types(self, auth_headers):
        """Test getting requirement types"""
        response = client.get("/requirements/types", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "functional" in data
        assert "non-functional" in data
        assert "business" in data
        assert "technical" in data

    def test_get_priorities(self, auth_headers):
        """Test getting priorities"""
        response = client.get("/requirements/priorities", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data

    def test_get_statuses(self, auth_headers):
        """Test getting statuses"""
        response = client.get("/requirements/statuses", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "draft" in data
        assert "active" in data
        assert "completed" in data
        assert "deprecated" in data

class TestAuthentication:
    def test_missing_auth_header(self, test_requirement_data):
        """Test that endpoints require authentication"""
        response = client.post("/requirements/", json=test_requirement_data)
        assert response.status_code == 401

    def test_invalid_token(self, test_requirement_data):
        """Test that invalid tokens are rejected"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/requirements/", json=test_requirement_data, headers=headers)
        assert response.status_code == 401

class TestValidation:
    def test_invalid_requirement_type(self, auth_headers):
        """Test validation of requirement type"""
        invalid_data = {
            "name": "Test Requirement",
            "requirement_type": "invalid_type",
            "priority": "high",
            "status": "draft"
        }
        response = client.post("/requirements/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

    def test_missing_required_fields(self, auth_headers):
        """Test validation of required fields"""
        invalid_data = {
            "description": "A test requirement"
            # Missing required fields
        }
        response = client.post("/requirements/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__]) 