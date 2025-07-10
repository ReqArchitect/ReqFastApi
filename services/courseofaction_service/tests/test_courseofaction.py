import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from uuid import uuid4
from datetime import datetime
import json

from app.main import app
from app.database import get_db
from app.models import Base, CourseOfAction, ActionLink
from app.schemas import StrategyType, TimeHorizon, RiskLevel, ImplementationPhase

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
test_tenant_id = str(uuid4())
test_user_id = str(uuid4())
test_course_of_action_id = str(uuid4())

@pytest.fixture
def sample_course_of_action():
    return {
        "name": "Cloud Migration Initiative",
        "description": "Strategic initiative to migrate legacy systems to cloud infrastructure",
        "strategy_type": StrategyType.TRANSFORMATIONAL,
        "origin_goal_id": str(uuid4()),
        "influenced_by_driver_id": str(uuid4()),
        "impacted_capability_id": str(uuid4()),
        "strategic_objective": "Achieve 99.9% uptime and reduce infrastructure costs by 30%",
        "business_case": "Cost reduction and improved scalability",
        "success_criteria": json.dumps(["99.9% uptime", "30% cost reduction", "Zero data loss"]),
        "key_performance_indicators": json.dumps(["uptime", "cost_savings", "migration_speed"]),
        "time_horizon": TimeHorizon.MEDIUM_TERM,
        "start_date": "2024-01-01T00:00:00Z",
        "target_completion_date": "2024-12-31T23:59:59Z",
        "implementation_phase": ImplementationPhase.PLANNING,
        "success_probability": 0.8,
        "risk_level": RiskLevel.MEDIUM,
        "risk_assessment": json.dumps({"data_migration": "high", "downtime": "medium"}),
        "contingency_plans": json.dumps(["rollback_plan", "parallel_systems"]),
        "estimated_cost": 1000000.0,
        "budget_allocation": 1200000.0,
        "resource_requirements": json.dumps({"developers": 5, "devops": 3, "qa": 2}),
        "cost_benefit_analysis": json.dumps({"roi": "150%", "payback_period": "18 months"}),
        "stakeholders": json.dumps(["cto", "cio", "business_units"]),
        "governance_model": "enhanced",
        "approval_status": "pending",
        "implementation_approach": "Phased migration with parallel systems",
        "milestones": json.dumps(["planning", "pilot", "full_migration", "validation"]),
        "dependencies": json.dumps(["infrastructure_ready", "team_training", "vendor_selection"]),
        "constraints": json.dumps(["budget_limit", "timeline", "compliance_requirements"]),
        "current_progress": 15.0,
        "performance_metrics": json.dumps({"progress": "15%", "budget_spent": "10%"}),
        "outcomes_achieved": json.dumps(["team_assembled", "vendor_selected"]),
        "lessons_learned": json.dumps(["early_planning_critical", "stakeholder_engagement_key"]),
        "strategic_alignment_score": 0.85,
        "capability_impact_score": 0.9,
        "goal_achievement_score": 0.8,
        "overall_effectiveness_score": 0.85,
        "compliance_requirements": json.dumps(["gdpr", "sox", "industry_standards"]),
        "audit_trail": json.dumps(["created", "updated", "approved"]),
        "regulatory_impact": json.dumps(["data_protection", "financial_regulations"]),
        "technology_requirements": json.dumps(["cloud_platform", "migration_tools", "monitoring"]),
        "system_impact": json.dumps(["legacy_systems", "data_warehouse", "reporting"]),
        "integration_requirements": json.dumps(["api_gateway", "data_pipeline", "monitoring"]),
        "change_management_plan": json.dumps(["communication", "training", "support"]),
        "communication_plan": json.dumps(["weekly_updates", "stakeholder_meetings", "progress_reports"]),
        "training_requirements": json.dumps(["cloud_platform", "new_processes", "tools"])
    }

@pytest.fixture
def sample_action_link():
    return {
        "linked_element_id": str(uuid4()),
        "linked_element_type": "goal",
        "link_type": "realizes",
        "relationship_strength": "strong",
        "dependency_level": "high",
        "strategic_importance": "high",
        "business_value": "high",
        "alignment_score": 0.9,
        "implementation_priority": "high",
        "implementation_phase": ImplementationPhase.PLANNING,
        "resource_allocation": 25.0,
        "impact_level": "high",
        "impact_direction": "positive",
        "impact_confidence": 0.85,
        "risk_level": RiskLevel.MEDIUM,
        "constraint_level": "medium",
        "risk_mitigation": json.dumps(["monitoring", "backup_plans"]),
        "performance_contribution": 30.0,
        "success_contribution": 25.0,
        "outcome_measurement": json.dumps(["kpi_tracking", "regular_assessment"])
    }

class TestCourseOfActionCRUD:
    """Test Course of Action CRUD operations"""
    
    def test_create_course_of_action(self, sample_course_of_action):
        """Test creating a course of action"""
        response = client.post(
            "/api/v1/courses-of-action",
            json=sample_course_of_action,
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_course_of_action["name"]
        assert data["strategy_type"] == sample_course_of_action["strategy_type"]
        assert "id" in data
        assert "tenant_id" in data
        assert "user_id" in data
    
    def test_get_course_of_action(self, sample_course_of_action):
        """Test getting a course of action by ID"""
        # First create a course of action
        create_response = client.post(
            "/api/v1/courses-of-action",
            json=sample_course_of_action,
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        course_of_action_id = create_response.json()["id"]
        
        # Then get it
        response = client.get(
            f"/api/v1/courses-of-action/{course_of_action_id}",
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == course_of_action_id
        assert data["name"] == sample_course_of_action["name"]
    
    def test_update_course_of_action(self, sample_course_of_action):
        """Test updating a course of action"""
        # First create a course of action
        create_response = client.post(
            "/api/v1/courses-of-action",
            json=sample_course_of_action,
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        course_of_action_id = create_response.json()["id"]
        
        # Then update it
        update_data = {
            "name": "Updated Cloud Migration Initiative",
            "description": "Updated description",
            "success_probability": 0.9
        }
        response = client.put(
            f"/api/v1/courses-of-action/{course_of_action_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
        assert data["success_probability"] == update_data["success_probability"]
    
    def test_delete_course_of_action(self, sample_course_of_action):
        """Test deleting a course of action"""
        # First create a course of action
        create_response = client.post(
            "/api/v1/courses-of-action",
            json=sample_course_of_action,
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        course_of_action_id = create_response.json()["id"]
        
        # Then delete it
        response = client.delete(
            f"/api/v1/courses-of-action/{course_of_action_id}",
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(
            f"/api/v1/courses-of-action/{course_of_action_id}",
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert get_response.status_code == 404
    
    def test_list_courses_of_action(self, sample_course_of_action):
        """Test listing courses of action with filtering"""
        # Create multiple courses of action
        for i in range(3):
            course_data = sample_course_of_action.copy()
            course_data["name"] = f"Course of Action {i+1}"
            client.post(
                "/api/v1/courses-of-action",
                json=course_data,
                headers={"Authorization": f"Bearer {self._create_test_token()}"}
            )
        
        # Test listing with filters
        response = client.get(
            "/api/v1/courses-of-action?strategy_type=transformational&limit=10",
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        assert all(course["strategy_type"] == "transformational" for course in data)
    
    def _create_test_token(self):
        """Create a test JWT token"""
        import jwt
        payload = {
            "tenant_id": test_tenant_id,
            "user_id": test_user_id,
            "role": "Admin"
        }
        return jwt.encode(payload, "test_secret", algorithm="HS256")

class TestActionLinkCRUD:
    """Test Action Link CRUD operations"""
    
    def test_create_action_link(self, sample_course_of_action, sample_action_link):
        """Test creating an action link"""
        # First create a course of action
        create_response = client.post(
            "/api/v1/courses-of-action",
            json=sample_course_of_action,
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        course_of_action_id = create_response.json()["id"]
        
        # Then create an action link
        response = client.post(
            f"/api/v1/courses-of-action/{course_of_action_id}/links",
            json=sample_action_link,
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["course_of_action_id"] == course_of_action_id
        assert data["linked_element_id"] == sample_action_link["linked_element_id"]
        assert data["link_type"] == sample_action_link["link_type"]
    
    def test_get_action_links(self, sample_course_of_action, sample_action_link):
        """Test getting action links for a course of action"""
        # First create a course of action
        create_response = client.post(
            "/api/v1/courses-of-action",
            json=sample_course_of_action,
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        course_of_action_id = create_response.json()["id"]
        
        # Create multiple action links
        for i in range(3):
            link_data = sample_action_link.copy()
            link_data["linked_element_id"] = str(uuid4())
            client.post(
                f"/api/v1/courses-of-action/{course_of_action_id}/links",
                json=link_data,
                headers={"Authorization": f"Bearer {self._create_test_token()}"}
            )
        
        # Get all action links
        response = client.get(
            f"/api/v1/courses-of-action/{course_of_action_id}/links",
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    def _create_test_token(self):
        """Create a test JWT token"""
        import jwt
        payload = {
            "tenant_id": test_tenant_id,
            "user_id": test_user_id,
            "role": "Admin"
        }
        return jwt.encode(payload, "test_secret", algorithm="HS256")

class TestAnalysisEndpoints:
    """Test analysis and alignment endpoints"""
    
    def test_get_alignment_map(self, sample_course_of_action):
        """Test getting alignment map"""
        # Create a course of action
        create_response = client.post(
            "/api/v1/courses-of-action",
            json=sample_course_of_action,
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        course_of_action_id = create_response.json()["id"]
        
        # Get alignment map
        response = client.get(
            f"/api/v1/courses-of-action/{course_of_action_id}/alignment-map",
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "course_of_action_id" in data
        assert "strategic_alignment" in data
        assert "capability_alignment" in data
        assert "goal_alignment" in data
        assert "overall_alignment_score" in data
        assert "recommendations" in data
    
    def test_get_risk_profile(self, sample_course_of_action):
        """Test getting risk profile"""
        # Create a course of action
        create_response = client.post(
            "/api/v1/courses-of-action",
            json=sample_course_of_action,
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        course_of_action_id = create_response.json()["id"]
        
        # Get risk profile
        response = client.get(
            f"/api/v1/courses-of-action/{course_of_action_id}/risk-profile",
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "course_of_action_id" in data
        assert "overall_risk_score" in data
        assert "risk_breakdown" in data
        assert "risk_factors" in data
        assert "mitigation_strategies" in data
        assert "recommendations" in data
    
    def test_analyze_course_of_action(self, sample_course_of_action):
        """Test comprehensive analysis"""
        # Create a course of action
        create_response = client.post(
            "/api/v1/courses-of-action",
            json=sample_course_of_action,
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        course_of_action_id = create_response.json()["id"]
        
        # Get analysis
        response = client.get(
            f"/api/v1/courses-of-action/{course_of_action_id}/analysis",
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "course_of_action_id" in data
        assert "strategic_analysis" in data
        assert "performance_analysis" in data
        assert "risk_analysis" in data
        assert "cost_analysis" in data
        assert "implementation_analysis" in data
        assert "outcome_analysis" in data
        assert "recommendations" in data
    
    def _create_test_token(self):
        """Create a test JWT token"""
        import jwt
        payload = {
            "tenant_id": test_tenant_id,
            "user_id": test_user_id,
            "role": "Admin"
        }
        return jwt.encode(payload, "test_secret", algorithm="HS256")

class TestDomainSpecificQueries:
    """Test domain-specific query endpoints"""
    
    def test_get_by_strategy_type(self, sample_course_of_action):
        """Test getting courses of action by strategy type"""
        # Create courses of action with different strategy types
        strategy_types = ["transformational", "incremental", "defensive"]
        for strategy_type in strategy_types:
            course_data = sample_course_of_action.copy()
            course_data["strategy_type"] = strategy_type
            client.post(
                "/api/v1/courses-of-action",
                json=course_data,
                headers={"Authorization": f"Bearer {self._create_test_token()}"}
            )
        
        # Test getting by strategy type
        response = client.get(
            "/api/v1/courses-of-action/by-type/transformational",
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert all(course["strategy_type"] == "transformational" for course in data)
    
    def test_get_by_risk_level(self, sample_course_of_action):
        """Test getting courses of action by risk level"""
        # Create courses of action with different risk levels
        risk_levels = ["low", "medium", "high"]
        for risk_level in risk_levels:
            course_data = sample_course_of_action.copy()
            course_data["risk_level"] = risk_level
            course_data["name"] = f"Course {risk_level}"
            client.post(
                "/api/v1/courses-of-action",
                json=course_data,
                headers={"Authorization": f"Bearer {self._create_test_token()}"}
            )
        
        # Test getting by risk level
        response = client.get(
            "/api/v1/courses-of-action/by-risk-level/high",
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert all(course["risk_level"] == "high" for course in data)
    
    def test_get_active_courses_of_action(self, sample_course_of_action):
        """Test getting active courses of action"""
        # Create courses of action with different phases
        phases = ["planning", "active", "completed"]
        for phase in phases:
            course_data = sample_course_of_action.copy()
            course_data["implementation_phase"] = phase
            course_data["name"] = f"Course {phase}"
            client.post(
                "/api/v1/courses-of-action",
                json=course_data,
                headers={"Authorization": f"Bearer {self._create_test_token()}"}
            )
        
        # Test getting active courses
        response = client.get(
            "/api/v1/courses-of-action/active",
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert all(course["implementation_phase"] == "active" for course in data)
    
    def _create_test_token(self):
        """Create a test JWT token"""
        import jwt
        payload = {
            "tenant_id": test_tenant_id,
            "user_id": test_user_id,
            "role": "Admin"
        }
        return jwt.encode(payload, "test_secret", algorithm="HS256")

class TestEnumerationEndpoints:
    """Test enumeration endpoints"""
    
    def test_get_strategy_types(self):
        """Test getting strategy types"""
        response = client.get("/api/v1/courses-of-action/strategy-types")
        assert response.status_code == 200
        data = response.json()
        assert "transformational" in data
        assert "incremental" in data
        assert "defensive" in data
        assert "innovative" in data
    
    def test_get_risk_levels(self):
        """Test getting risk levels"""
        response = client.get("/api/v1/courses-of-action/risk-levels")
        assert response.status_code == 200
        data = response.json()
        assert "low" in data
        assert "medium" in data
        assert "high" in data
        assert "critical" in data
    
    def test_get_time_horizons(self):
        """Test getting time horizons"""
        response = client.get("/api/v1/courses-of-action/time-horizons")
        assert response.status_code == 200
        data = response.json()
        assert "short_term" in data
        assert "medium_term" in data
        assert "long_term" in data

class TestValidation:
    """Test validation and error handling"""
    
    def test_invalid_success_probability(self):
        """Test validation of success probability"""
        course_data = {
            "name": "Test Course",
            "success_probability": 1.5  # Invalid value > 1.0
        }
        response = client.post(
            "/api/v1/courses-of-action",
            json=course_data,
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_invalid_current_progress(self):
        """Test validation of current progress"""
        course_data = {
            "name": "Test Course",
            "current_progress": 150.0  # Invalid value > 100.0
        }
        response = client.post(
            "/api/v1/courses-of-action",
            json=course_data,
            headers={"Authorization": f"Bearer {self._create_test_token()}"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_missing_authentication(self):
        """Test missing authentication"""
        response = client.get("/api/v1/courses-of-action")
        assert response.status_code == 401
    
    def test_invalid_token(self):
        """Test invalid JWT token"""
        response = client.get(
            "/api/v1/courses-of-action",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
    
    def _create_test_token(self):
        """Create a test JWT token"""
        import jwt
        payload = {
            "tenant_id": test_tenant_id,
            "user_id": test_user_id,
            "role": "Admin"
        }
        return jwt.encode(payload, "test_secret", algorithm="HS256")

class TestHealthAndMetrics:
    """Test health and metrics endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "courseofaction_service"
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        # Metrics should be in Prometheus format
        assert "courseofaction_http_requests_total" in response.text
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Course of Action Service"
        assert data["version"] == "1.0.0"
        assert "docs" in data
        assert "health" in data
        assert "metrics" in data 