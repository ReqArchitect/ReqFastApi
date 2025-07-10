import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
from app.schemas import (
    ValidationRunRequest, ValidationRunResponse, IssuesListResponse,
    ScorecardResponse, ValidationHistoryResponse
)
import jwt
import json

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def valid_jwt_token():
    """Create a valid JWT token for testing"""
    payload = {
        "user_id": "test-user-id",
        "tenant_id": "test-tenant-id",
        "role": "Admin",
        "exp": 9999999999  # Far future expiration
    }
    return jwt.encode(payload, "REPLACE_WITH_REAL_SECRET", algorithm="HS256")

@pytest.fixture
def viewer_jwt_token():
    """Create a JWT token for Viewer role"""
    payload = {
        "user_id": "test-user-id",
        "tenant_id": "test-tenant-id",
        "role": "Viewer",
        "exp": 9999999999
    }
    return jwt.encode(payload, "REPLACE_WITH_REAL_SECRET", algorithm="HS256")

@pytest.fixture
def mock_validation_service():
    with patch('app.routes.get_validation_service') as mock_service:
        mock_service.return_value = Mock()
        yield mock_service.return_value

class TestValidationRoutes:
    
    def test_run_validation_cycle_success(self, client, valid_jwt_token, mock_validation_service):
        """Test successful validation cycle creation"""
        # Mock service response
        mock_validation_service.run_validation_cycle = AsyncMock()
        mock_validation_service.run_validation_cycle.return_value = Mock(
            id="cycle-1",
            tenant_id="test-tenant-id",
            start_time="2024-01-15T10:00:00Z",
            end_time=None,
            triggered_by="test-user-id",
            rule_set_id=None,
            total_issues_found=0,
            execution_status="running",
            maturity_score=None,
            created_at="2024-01-15T10:00:00Z",
            updated_at="2024-01-15T10:00:00Z"
        )
        
        response = client.post(
            "/validation/run",
            headers={"Authorization": f"Bearer {valid_jwt_token}"},
            json={
                "rule_set_id": None,
                "force_full_scan": False
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["validation_cycle_id"] == "cycle-1"
        assert data["status"] == "running"
        assert "started successfully" in data["message"]
    
    def test_run_validation_cycle_insufficient_permissions(self, client, viewer_jwt_token):
        """Test validation cycle creation with insufficient permissions"""
        response = client.post(
            "/validation/run",
            headers={"Authorization": f"Bearer {viewer_jwt_token}"},
            json={
                "rule_set_id": None,
                "force_full_scan": False
            }
        )
        
        assert response.status_code == 403
        data = response.json()
        assert "Insufficient permissions" in data["detail"]
    
    def test_run_validation_cycle_no_auth(self, client):
        """Test validation cycle creation without authentication"""
        response = client.post(
            "/validation/run",
            json={
                "rule_set_id": None,
                "force_full_scan": False
            }
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "Not authenticated" in data["detail"]
    
    def test_run_validation_cycle_service_error(self, client, valid_jwt_token, mock_validation_service):
        """Test validation cycle creation with service error"""
        mock_validation_service.run_validation_cycle = AsyncMock()
        mock_validation_service.run_validation_cycle.side_effect = Exception("Service error")
        
        response = client.post(
            "/validation/run",
            headers={"Authorization": f"Bearer {valid_jwt_token}"},
            json={
                "rule_set_id": None,
                "force_full_scan": False
            }
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to start validation cycle" in data["detail"]
    
    def test_get_validation_issues_success(self, client, valid_jwt_token, mock_validation_service):
        """Test getting validation issues"""
        # Mock service response
        mock_validation_service.get_validation_issues.return_value = Mock(
            issues=[],
            total_count=0,
            critical_count=0,
            high_count=0,
            medium_count=0,
            low_count=0
        )
        
        response = client.get(
            "/validation/issues?skip=0&limit=100",
            headers={"Authorization": f"Bearer {valid_jwt_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "issues" in data
        assert "total_count" in data
        assert data["total_count"] == 0
    
    def test_get_validation_issues_with_pagination(self, client, valid_jwt_token, mock_validation_service):
        """Test getting validation issues with pagination"""
        # Mock service response
        mock_validation_service.get_validation_issues.return_value = Mock(
            issues=[],
            total_count=0,
            critical_count=0,
            high_count=0,
            medium_count=0,
            low_count=0
        )
        
        response = client.get(
            "/validation/issues?skip=10&limit=50",
            headers={"Authorization": f"Bearer {valid_jwt_token}"}
        )
        
        assert response.status_code == 200
        
        # Verify service was called with correct parameters
        mock_validation_service.get_validation_issues.assert_called_with(
            tenant_id="test-tenant-id",
            skip=10,
            limit=50
        )
    
    def test_get_validation_scorecard_success(self, client, valid_jwt_token, mock_validation_service):
        """Test getting validation scorecard"""
        # Mock service response
        mock_validation_service.get_validation_scorecard.return_value = Mock(
            tenant_id="test-tenant-id",
            validation_cycle_id="cycle-1",
            overall_maturity_score=85.5,
            layer_scores=[],
            summary={}
        )
        
        response = client.get(
            "/validation/scorecard",
            headers={"Authorization": f"Bearer {valid_jwt_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["tenant_id"] == "test-tenant-id"
        assert data["overall_maturity_score"] == 85.5
    
    def test_get_validation_scorecard_with_cycle_id(self, client, valid_jwt_token, mock_validation_service):
        """Test getting validation scorecard with specific cycle ID"""
        # Mock service response
        mock_validation_service.get_validation_scorecard.return_value = Mock(
            tenant_id="test-tenant-id",
            validation_cycle_id="cycle-1",
            overall_maturity_score=85.5,
            layer_scores=[],
            summary={}
        )
        
        response = client.get(
            "/validation/scorecard?validation_cycle_id=cycle-1",
            headers={"Authorization": f"Bearer {valid_jwt_token}"}
        )
        
        assert response.status_code == 200
        
        # Verify service was called with correct parameters
        mock_validation_service.get_validation_scorecard.assert_called_with(
            tenant_id="test-tenant-id",
            validation_cycle_id="cycle-1"
        )
    
    def test_get_validation_scorecard_not_found(self, client, valid_jwt_token, mock_validation_service):
        """Test getting validation scorecard when not found"""
        mock_validation_service.get_validation_scorecard.side_effect = ValueError("No completed validation cycles found")
        
        response = client.get(
            "/validation/scorecard",
            headers={"Authorization": f"Bearer {valid_jwt_token}"}
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "No completed validation cycles found" in data["detail"]
    
    def test_get_traceability_matrix_success(self, client, valid_jwt_token, mock_validation_service):
        """Test getting traceability matrix"""
        # Mock service response
        mock_validation_service.get_traceability_matrix.return_value = [
            Mock(
                id="matrix-1",
                tenant_id="test-tenant-id",
                source_layer="Motivation",
                target_layer="Business",
                source_entity_type="goal",
                target_entity_type="capability",
                relationship_type="supports",
                connection_count=15,
                missing_connections=3,
                strength_score=0.83,
                last_updated="2024-01-15T10:30:00Z"
            )
        ]
        
        response = client.get(
            "/validation/traceability-matrix",
            headers={"Authorization": f"Bearer {valid_jwt_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["source_layer"] == "Motivation"
        assert data[0]["target_layer"] == "Business"
    
    def test_get_traceability_matrix_with_filters(self, client, valid_jwt_token, mock_validation_service):
        """Test getting traceability matrix with filters"""
        # Mock service response
        mock_validation_service.get_traceability_matrix.return_value = []
        
        response = client.get(
            "/validation/traceability-matrix?source_layer=Motivation&target_layer=Business",
            headers={"Authorization": f"Bearer {valid_jwt_token}"}
        )
        
        assert response.status_code == 200
        
        # Verify service was called with correct parameters
        mock_validation_service.get_traceability_matrix.assert_called_with(
            tenant_id="test-tenant-id",
            source_layer="Motivation",
            target_layer="Business"
        )
    
    def test_get_validation_history_success(self, client, valid_jwt_token, mock_validation_service):
        """Test getting validation history"""
        # Mock service response
        mock_validation_service.get_validation_history.return_value = {
            "cycles": [],
            "total_cycles": 0,
            "average_maturity_score": 0.0,
            "last_validation_date": None
        }
        
        response = client.get(
            "/validation/history",
            headers={"Authorization": f"Bearer {valid_jwt_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "cycles" in data
        assert "total_cycles" in data
        assert "average_maturity_score" in data
    
    def test_create_validation_exception_success(self, client, valid_jwt_token, mock_validation_service):
        """Test creating validation exception"""
        # Mock service response
        mock_validation_service.create_validation_exception.return_value = Mock(
            id="exception-1",
            tenant_id="test-tenant-id",
            entity_type="goal",
            entity_id="goal-1",
            rule_id="rule-1",
            reason="Test exception",
            created_by="test-user-id",
            created_at="2024-01-15T10:30:00Z",
            is_active=True,
            expires_at=None
        )
        
        response = client.post(
            "/validation/exceptions",
            headers={"Authorization": f"Bearer {valid_jwt_token}"},
            json={
                "entity_type": "goal",
                "entity_id": "goal-1",
                "reason": "Test exception",
                "rule_id": "rule-1",
                "expires_at": None
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Validation exception created successfully"
        assert "exception_id" in data
    
    def test_create_validation_exception_insufficient_permissions(self, client, viewer_jwt_token):
        """Test creating validation exception with insufficient permissions"""
        response = client.post(
            "/validation/exceptions",
            headers={"Authorization": f"Bearer {viewer_jwt_token}"},
            json={
                "entity_type": "goal",
                "entity_id": "goal-1",
                "reason": "Test exception",
                "rule_id": "rule-1",
                "expires_at": None
            }
        )
        
        assert response.status_code == 403
        data = response.json()
        assert "Insufficient permissions" in data["detail"]
    
    def test_toggle_validation_rule_success(self, client, valid_jwt_token, mock_validation_service):
        """Test toggling validation rule"""
        # Mock service response
        mock_validation_service.toggle_validation_rule.return_value = Mock(
            id="rule-1",
            name="Test Rule",
            description="Test Description",
            rule_type="traceability",
            scope="Motivation",
            rule_logic="{}",
            severity="medium",
            is_active=False,
            created_at="2024-01-15T10:00:00Z",
            updated_at="2024-01-15T10:30:00Z"
        )
        
        response = client.patch(
            "/validation/rules/rule-1",
            headers={"Authorization": f"Bearer {valid_jwt_token}"},
            json={
                "is_active": False
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Validation rule deactivated successfully"
        assert data["rule_id"] == "rule-1"
        assert data["is_active"] == False
    
    def test_toggle_validation_rule_not_found(self, client, valid_jwt_token, mock_validation_service):
        """Test toggling non-existent validation rule"""
        mock_validation_service.toggle_validation_rule.side_effect = ValueError("Validation rule rule-1 not found")
        
        response = client.patch(
            "/validation/rules/rule-1",
            headers={"Authorization": f"Bearer {valid_jwt_token}"},
            json={
                "is_active": False
            }
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Validation rule rule-1 not found" in data["detail"]
    
    def test_toggle_validation_rule_insufficient_permissions(self, client, viewer_jwt_token):
        """Test toggling validation rule with insufficient permissions"""
        response = client.patch(
            "/validation/rules/rule-1",
            headers={"Authorization": f"Bearer {viewer_jwt_token}"},
            json={
                "is_active": False
            }
        )
        
        assert response.status_code == 403
        data = response.json()
        assert "Insufficient permissions" in data["detail"]
    
    def test_get_validation_rules_success(self, client, valid_jwt_token, mock_validation_service):
        """Test getting validation rules"""
        # Mock service response
        mock_validation_service.get_validation_rules.return_value = []
        
        response = client.get(
            "/validation/rules",
            headers={"Authorization": f"Bearer {valid_jwt_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "architecture_validation_service"
        assert "version" in data
        assert "timestamp" in data
    
    def test_metrics_endpoint(self, client):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        
        assert response.status_code == 200
        data = response.json()
        assert "validation_cycles_total" in data
        assert "validation_issues_total" in data
        assert "validation_rules_active" in data
        assert "average_maturity_score" in data
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Architecture Validation Service"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"
        assert "timestamp" in data

class TestAuthentication:
    
    def test_invalid_jwt_token(self, client):
        """Test with invalid JWT token"""
        response = client.post(
            "/validation/run",
            headers={"Authorization": "Bearer invalid-token"},
            json={
                "rule_set_id": None,
                "force_full_scan": False
            }
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "Invalid token" in data["detail"]
    
    def test_expired_jwt_token(self, client):
        """Test with expired JWT token"""
        # Create expired token
        payload = {
            "user_id": "test-user-id",
            "tenant_id": "test-tenant-id",
            "role": "Admin",
            "exp": 0  # Expired
        }
        expired_token = jwt.encode(payload, "REPLACE_WITH_REAL_SECRET", algorithm="HS256")
        
        response = client.post(
            "/validation/run",
            headers={"Authorization": f"Bearer {expired_token}"},
            json={
                "rule_set_id": None,
                "force_full_scan": False
            }
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "Token has expired" in data["detail"]
    
    def test_missing_tenant_id_in_token(self, client):
        """Test with JWT token missing tenant_id"""
        payload = {
            "user_id": "test-user-id",
            "role": "Admin",
            "exp": 9999999999
        }
        invalid_token = jwt.encode(payload, "REPLACE_WITH_REAL_SECRET", algorithm="HS256")
        
        response = client.post(
            "/validation/run",
            headers={"Authorization": f"Bearer {invalid_token}"},
            json={
                "rule_set_id": None,
                "force_full_scan": False
            }
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "missing user_id or tenant_id" in data["detail"]
    
    def test_missing_authorization_header(self, client):
        """Test without authorization header"""
        response = client.post(
            "/validation/run",
            json={
                "rule_set_id": None,
                "force_full_scan": False
            }
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "Not authenticated" in data["detail"] 