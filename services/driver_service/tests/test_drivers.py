import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Driver, DriverLink
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
def test_driver_data():
    """Fixture for test driver data"""
    return {
        "name": "Digital Transformation Initiative",
        "description": "Market pressure to adopt digital technologies",
        "driver_type": "business",
        "category": "external",
        "urgency": "high",
        "impact_level": "high",
        "source": "Market Analysis",
        "strategic_priority": 4,
        "time_horizon": "medium-term",
        "geographic_scope": "global",
        "compliance_required": False,
        "risk_level": "medium"
    }

class TestHealthEndpoint:
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "driver_service"
        assert data["status"] == "healthy"

class TestDriversCRUD:
    def test_create_driver(self, auth_headers, test_driver_data):
        """Test creating a driver"""
        response = client.post("/drivers/", json=test_driver_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == test_driver_data["name"]
        assert data["driver_type"] == test_driver_data["driver_type"]
        assert "id" in data
        assert "tenant_id" in data

    def test_get_drivers(self, auth_headers):
        """Test getting drivers list"""
        response = client.get("/drivers/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_driver_types(self, auth_headers):
        """Test getting driver types"""
        response = client.get("/drivers/types", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "business" in data
        assert "technical" in data
        assert "regulatory" in data
        assert "environmental" in data
        assert "social" in data

    def test_get_categories(self, auth_headers):
        """Test getting categories"""
        response = client.get("/drivers/categories", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "internal" in data
        assert "external" in data
        assert "strategic" in data
        assert "operational" in data

    def test_get_urgencies(self, auth_headers):
        """Test getting urgencies"""
        response = client.get("/drivers/urgencies", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data

    def test_get_impact_levels(self, auth_headers):
        """Test getting impact levels"""
        response = client.get("/drivers/impact-levels", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data

    def test_get_time_horizons(self, auth_headers):
        """Test getting time horizons"""
        response = client.get("/drivers/time-horizons", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "short-term" in data
        assert "medium-term" in data
        assert "long-term" in data

    def test_get_geographic_scopes(self, auth_headers):
        """Test getting geographic scopes"""
        response = client.get("/drivers/geographic-scopes", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "local" in data
        assert "regional" in data
        assert "national" in data
        assert "global" in data

    def test_get_risk_levels(self, auth_headers):
        """Test getting risk levels"""
        response = client.get("/drivers/risk-levels", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data

class TestAuthentication:
    def test_missing_auth_header(self, test_driver_data):
        """Test that endpoints require authentication"""
        response = client.post("/drivers/", json=test_driver_data)
        assert response.status_code == 401

    def test_invalid_token(self, test_driver_data):
        """Test that invalid tokens are rejected"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/drivers/", json=test_driver_data, headers=headers)
        assert response.status_code == 401

class TestValidation:
    def test_invalid_driver_type(self, auth_headers):
        """Test validation of driver type"""
        invalid_data = {
            "name": "Test Driver",
            "driver_type": "invalid_type",
            "category": "external",
            "urgency": "high",
            "impact_level": "high"
        }
        response = client.post("/drivers/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

    def test_missing_required_fields(self, auth_headers):
        """Test validation of required fields"""
        invalid_data = {
            "description": "A test driver"
            # Missing required fields
        }
        response = client.post("/drivers/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

    def test_invalid_strategic_priority(self, auth_headers):
        """Test validation of strategic priority range"""
        invalid_data = {
            "name": "Test Driver",
            "driver_type": "business",
            "category": "external",
            "urgency": "high",
            "impact_level": "high",
            "strategic_priority": 6  # Should be 1-5
        }
        response = client.post("/drivers/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__]) 