import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Constraint, ConstraintLink
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
def test_constraint_data():
    """Fixture for test constraint data"""
    return {
        "name": "GDPR Data Protection",
        "description": "European data protection regulation compliance",
        "constraint_type": "regulatory",
        "scope": "global",
        "severity": "high",
        "enforcement_level": "mandatory",
        "risk_profile": "high",
        "compliance_required": True,
        "regulatory_framework": "GDPR",
        "mitigation_strategy": "Implement data encryption and access controls",
        "mitigation_status": "in_progress",
        "mitigation_effort": "high",
        "business_impact": "high",
        "technical_impact": "medium",
        "operational_impact": "medium"
    }

class TestHealthEndpoint:
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "constraint_service"
        assert data["status"] == "healthy"

class TestConstraintsCRUD:
    def test_create_constraint(self, auth_headers, test_constraint_data):
        """Test creating a constraint"""
        response = client.post("/constraints/", json=test_constraint_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == test_constraint_data["name"]
        assert data["constraint_type"] == test_constraint_data["constraint_type"]
        assert "id" in data
        assert "tenant_id" in data

    def test_get_constraints(self, auth_headers):
        """Test getting constraints list"""
        response = client.get("/constraints/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_constraint_types(self, auth_headers):
        """Test getting constraint types"""
        response = client.get("/constraints/types", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "technical" in data
        assert "regulatory" in data
        assert "organizational" in data
        assert "environmental" in data
        assert "financial" in data

    def test_get_scopes(self, auth_headers):
        """Test getting scopes"""
        response = client.get("/constraints/scopes", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "global" in data
        assert "domain" in data
        assert "project" in data
        assert "component" in data

    def test_get_severities(self, auth_headers):
        """Test getting severities"""
        response = client.get("/constraints/severities", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data

    def test_get_enforcement_levels(self, auth_headers):
        """Test getting enforcement levels"""
        response = client.get("/constraints/enforcement-levels", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "mandatory" in data
        assert "recommended" in data
        assert "optional" in data

    def test_get_risk_profiles(self, auth_headers):
        """Test getting risk profiles"""
        response = client.get("/constraints/risk-profiles", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data

    def test_get_mitigation_statuses(self, auth_headers):
        """Test getting mitigation statuses"""
        response = client.get("/constraints/mitigation-statuses", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "pending" in data
        assert "in_progress" in data
        assert "implemented" in data
        assert "verified" in data

    def test_get_mitigation_efforts(self, auth_headers):
        """Test getting mitigation efforts"""
        response = client.get("/constraints/mitigation-efforts", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data

    def test_get_impact_levels(self, auth_headers):
        """Test getting impact levels"""
        response = client.get("/constraints/impact-levels", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data

    def test_get_review_frequencies(self, auth_headers):
        """Test getting review frequencies"""
        response = client.get("/constraints/review-frequencies", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "monthly" in data
        assert "quarterly" in data
        assert "annually" in data
        assert "ad_hoc" in data

    def test_get_link_types(self, auth_headers):
        """Test getting link types"""
        response = client.get("/constraints/link-types", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "constrains" in data
        assert "limits" in data
        assert "restricts" in data
        assert "governs" in data
        assert "regulates" in data

    def test_get_compliance_statuses(self, auth_headers):
        """Test getting compliance statuses"""
        response = client.get("/constraints/compliance-statuses", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "compliant" in data
        assert "non_compliant" in data
        assert "partially_compliant" in data
        assert "exempt" in data

class TestAuthentication:
    def test_missing_auth_header(self, test_constraint_data):
        """Test that endpoints require authentication"""
        response = client.post("/constraints/", json=test_constraint_data)
        assert response.status_code == 401

    def test_invalid_token(self, test_constraint_data):
        """Test that invalid tokens are rejected"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/constraints/", json=test_constraint_data, headers=headers)
        assert response.status_code == 401

class TestValidation:
    def test_invalid_constraint_type(self, auth_headers):
        """Test validation of constraint type"""
        invalid_data = {
            "name": "Test Constraint",
            "constraint_type": "invalid_type",
            "scope": "global",
            "severity": "high",
            "enforcement_level": "mandatory"
        }
        response = client.post("/constraints/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

    def test_missing_required_fields(self, auth_headers):
        """Test validation of required fields"""
        invalid_data = {
            "description": "A test constraint"
            # Missing required fields
        }
        response = client.post("/constraints/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

    def test_invalid_scope(self, auth_headers):
        """Test validation of scope"""
        invalid_data = {
            "name": "Test Constraint",
            "constraint_type": "regulatory",
            "scope": "invalid_scope",
            "severity": "high",
            "enforcement_level": "mandatory"
        }
        response = client.post("/constraints/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__]) 