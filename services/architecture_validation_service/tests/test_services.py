import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
from app.services import ValidationService
from app.schemas import (
    ValidationContext, ValidationIssueCreate, ValidationCycleResponse,
    IssuesListResponse, ScorecardResponse, ValidationExceptionResponse
)
from app.models import (
    ValidationCycle, ValidationIssue, ValidationRule, ValidationException,
    ValidationScorecard, TraceabilityMatrix
)
from sqlalchemy.orm import Session
import redis

@pytest.fixture
def mock_db():
    return Mock(spec=Session)

@pytest.fixture
def mock_redis():
    return Mock(spec=redis.Redis)

@pytest.fixture
def validation_service(mock_db, mock_redis):
    return ValidationService(mock_db, mock_redis)

@pytest.fixture
def mock_validation_engine():
    with patch('app.services.ValidationEngine') as mock_engine:
        mock_engine.return_value.run_validation_cycle = AsyncMock()
        yield mock_engine

class TestValidationService:
    
    @pytest.mark.asyncio
    async def test_run_validation_cycle_success(self, validation_service, mock_validation_engine):
        """Test successful validation cycle creation"""
        # Mock database operations
        validation_service.db.add = Mock()
        validation_service.db.commit = Mock()
        validation_service.db.refresh = Mock()
        
        # Mock validation engine response
        mock_validation_engine.return_value.run_validation_cycle.return_value = []
        
        # Mock asyncio.create_task
        with patch('asyncio.create_task') as mock_create_task:
            result = await validation_service.run_validation_cycle(
                tenant_id="test-tenant",
                user_id="test-user",
                rule_set_id=None
            )
            
            assert isinstance(result, ValidationCycleResponse)
            assert result.tenant_id == "test-tenant"
            assert result.triggered_by == "test-user"
            assert result.execution_status == "running"
            
            # Verify database operations
            validation_service.db.add.assert_called_once()
            validation_service.db.commit.assert_called_once()
            validation_service.db.refresh.assert_called_once()
            
            # Verify async task creation
            mock_create_task.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_run_validation_cycle_exception(self, validation_service):
        """Test validation cycle creation with exception"""
        validation_service.db.add.side_effect = Exception("Database error")
        
        with pytest.raises(Exception, match="Database error"):
            await validation_service.run_validation_cycle(
                tenant_id="test-tenant",
                user_id="test-user"
            )
    
    @pytest.mark.asyncio
    async def test_run_validation_async_success(self, validation_service, mock_validation_engine):
        """Test successful async validation execution"""
        # Mock validation context and cycle
        context = ValidationContext(
            tenant_id="test-tenant",
            user_id="test-user",
            validation_cycle_id="test-cycle",
            rule_set_id=None
        )
        
        cycle = Mock(spec=ValidationCycle)
        cycle.id = "test-cycle"
        cycle.end_time = None
        cycle.total_issues_found = 0
        cycle.execution_status = "running"
        cycle.maturity_score = None
        
        # Mock validation engine results
        mock_validation_engine.return_value.run_validation_cycle.return_value = [
            Mock(issues_found=[
                ValidationIssueCreate(
                    tenant_id="test-tenant",
                    entity_type="goal",
                    entity_id="goal-1",
                    issue_type="missing_link",
                    severity="high",
                    description="Test issue",
                    recommended_fix="Test fix"
                )
            ])
        ]
        
        await validation_service._run_validation_async(context, cycle)
        
        # Verify cycle updates
        assert cycle.end_time is not None
        assert cycle.total_issues_found == 1
        assert cycle.execution_status == "completed"
        assert cycle.maturity_score == 90.0  # Based on 1 issue
        
        # Verify database operations
        validation_service.db.add.assert_called()
        validation_service.db.commit.assert_called()
    
    @pytest.mark.asyncio
    async def test_run_validation_async_failure(self, validation_service, mock_validation_engine):
        """Test async validation execution with failure"""
        context = ValidationContext(
            tenant_id="test-tenant",
            user_id="test-user",
            validation_cycle_id="test-cycle",
            rule_set_id=None
        )
        
        cycle = Mock(spec=ValidationCycle)
        cycle.id = "test-cycle"
        cycle.execution_status = "running"
        
        # Mock validation engine to raise exception
        mock_validation_engine.return_value.run_validation_cycle.side_effect = Exception("Validation failed")
        
        await validation_service._run_validation_async(context, cycle)
        
        # Verify cycle marked as failed
        assert cycle.execution_status == "failed"
        assert cycle.end_time is not None
        
        # Verify database operations
        validation_service.db.commit.assert_called()
    
    def test_calculate_maturity_score(self, validation_service):
        """Test maturity score calculation"""
        # Test various issue counts
        assert validation_service._calculate_maturity_score(0) == 100.0
        assert validation_service._calculate_maturity_score(3) == 90.0
        assert validation_service._calculate_maturity_score(8) == 80.0
        assert validation_service._calculate_maturity_score(15) == 70.0
        assert validation_service._calculate_maturity_score(30) == 60.0
        assert validation_service._calculate_maturity_score(100) == 50.0
    
    def test_get_validation_issues_success(self, validation_service):
        """Test getting validation issues"""
        # Mock database query
        mock_issues = [
            Mock(
                id="issue-1",
                tenant_id="test-tenant",
                validation_cycle_id="cycle-1",
                entity_type="goal",
                entity_id="goal-1",
                issue_type="missing_link",
                severity="high",
                description="Test issue",
                recommended_fix="Test fix",
                metadata={},
                timestamp=datetime.utcnow(),
                is_resolved=False,
                resolved_at=None,
                resolved_by=None
            )
        ]
        
        validation_service.db.query.return_value.filter.return_value.order_by.return_value.count.return_value = 1
        validation_service.db.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = mock_issues
        
        # Mock severity counts
        validation_service.db.query.return_value.filter.return_value.count.side_effect = [0, 1, 0, 0]  # critical, high, medium, low
        
        result = validation_service.get_validation_issues(
            tenant_id="test-tenant",
            skip=0,
            limit=100
        )
        
        assert isinstance(result, IssuesListResponse)
        assert len(result.issues) == 1
        assert result.total_count == 1
        assert result.high_count == 1
        assert result.critical_count == 0
        assert result.medium_count == 0
        assert result.low_count == 0
    
    def test_get_validation_scorecard_with_cycle_id(self, validation_service):
        """Test getting validation scorecard with specific cycle ID"""
        # Mock scorecards
        mock_scorecards = [
            Mock(
                id="scorecard-1",
                tenant_id="test-tenant",
                validation_cycle_id="cycle-1",
                layer="Motivation",
                completeness_score=90.0,
                traceability_score=85.0,
                alignment_score=80.0,
                overall_score=85.0,
                issues_count=2,
                critical_issues=0,
                high_issues=1,
                medium_issues=1,
                low_issues=0,
                created_at=datetime.utcnow()
            )
        ]
        
        validation_service.db.query.return_value.filter.return_value.all.return_value = mock_scorecards
        
        result = validation_service.get_validation_scorecard(
            tenant_id="test-tenant",
            validation_cycle_id="cycle-1"
        )
        
        assert isinstance(result, ScorecardResponse)
        assert result.tenant_id == "test-tenant"
        assert result.validation_cycle_id == "cycle-1"
        assert result.overall_maturity_score == 85.0
        assert len(result.layer_scores) == 1
        assert result.layer_scores[0].layer == "Motivation"
    
    def test_get_validation_scorecard_without_cycle_id(self, validation_service):
        """Test getting validation scorecard without cycle ID"""
        # Mock latest cycle
        mock_latest_cycle = Mock(
            id="cycle-1",
            end_time=datetime.utcnow(),
            execution_status="completed"
        )
        
        validation_service.db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_latest_cycle
        
        # Mock scorecards
        mock_scorecards = [
            Mock(
                id="scorecard-1",
                tenant_id="test-tenant",
                validation_cycle_id="cycle-1",
                layer="Motivation",
                completeness_score=90.0,
                traceability_score=85.0,
                alignment_score=80.0,
                overall_score=85.0,
                issues_count=2,
                critical_issues=0,
                high_issues=1,
                medium_issues=1,
                low_issues=0,
                created_at=datetime.utcnow()
            )
        ]
        
        validation_service.db.query.return_value.filter.return_value.all.return_value = mock_scorecards
        
        result = validation_service.get_validation_scorecard(
            tenant_id="test-tenant"
        )
        
        assert isinstance(result, ScorecardResponse)
        assert result.validation_cycle_id == "cycle-1"
    
    def test_get_validation_scorecard_no_cycles(self, validation_service):
        """Test getting validation scorecard when no cycles exist"""
        validation_service.db.query.return_value.filter.return_value.order_by.return_value.first.return_value = None
        
        with pytest.raises(ValueError, match="No completed validation cycles found"):
            validation_service.get_validation_scorecard(tenant_id="test-tenant")
    
    def test_get_traceability_matrix(self, validation_service):
        """Test getting traceability matrix"""
        # Mock matrices
        mock_matrices = [
            Mock(
                id="matrix-1",
                tenant_id="test-tenant",
                source_layer="Motivation",
                target_layer="Business",
                source_entity_type="goal",
                target_entity_type="capability",
                relationship_type="supports",
                connection_count=15,
                missing_connections=3,
                strength_score=0.83,
                last_updated=datetime.utcnow()
            )
        ]
        
        validation_service.db.query.return_value.filter.return_value.all.return_value = mock_matrices
        
        result = validation_service.get_traceability_matrix(
            tenant_id="test-tenant",
            source_layer="Motivation",
            target_layer="Business"
        )
        
        assert len(result) == 1
        assert result[0].source_layer == "Motivation"
        assert result[0].target_layer == "Business"
        assert result[0].connection_count == 15
        assert result[0].missing_connections == 3
    
    def test_get_validation_history(self, validation_service):
        """Test getting validation history"""
        # Mock cycles
        mock_cycles = [
            Mock(
                id="cycle-1",
                tenant_id="test-tenant",
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow(),
                triggered_by="test-user",
                rule_set_id=None,
                total_issues_found=5,
                execution_status="completed",
                maturity_score=85.5,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        validation_service.db.query.return_value.filter.return_value.order_by.return_value.count.return_value = 1
        validation_service.db.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = mock_cycles
        
        # Mock latest validation
        validation_service.db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_cycles[0]
        
        result = validation_service.get_validation_history(
            tenant_id="test-tenant",
            skip=0,
            limit=50
        )
        
        assert "cycles" in result
        assert "total_cycles" in result
        assert "average_maturity_score" in result
        assert "last_validation_date" in result
        assert result["total_cycles"] == 1
        assert result["average_maturity_score"] == 85.5
    
    def test_create_validation_exception(self, validation_service):
        """Test creating validation exception"""
        # Mock database operations
        validation_service.db.add = Mock()
        validation_service.db.commit = Mock()
        validation_service.db.refresh = Mock()
        
        result = validation_service.create_validation_exception(
            tenant_id="test-tenant",
            user_id="test-user",
            entity_type="goal",
            entity_id="goal-1",
            reason="Test exception",
            rule_id="rule-1",
            expires_at=None
        )
        
        assert isinstance(result, ValidationExceptionResponse)
        assert result.tenant_id == "test-tenant"
        assert result.entity_type == "goal"
        assert result.entity_id == "goal-1"
        assert result.reason == "Test exception"
        assert result.created_by == "test-user"
        
        # Verify database operations
        validation_service.db.add.assert_called_once()
        validation_service.db.commit.assert_called_once()
        validation_service.db.refresh.assert_called_once()
    
    def test_toggle_validation_rule(self, validation_service):
        """Test toggling validation rule"""
        # Mock rule
        mock_rule = Mock(spec=ValidationRule)
        mock_rule.id = "rule-1"
        mock_rule.name = "Test Rule"
        mock_rule.description = "Test Description"
        mock_rule.rule_type = "traceability"
        mock_rule.scope = "Motivation"
        mock_rule.rule_logic = "{}"
        mock_rule.severity = "medium"
        mock_rule.is_active = True
        mock_rule.created_at = datetime.utcnow()
        mock_rule.updated_at = datetime.utcnow()
        
        validation_service.db.query.return_value.filter.return_value.first.return_value = mock_rule
        validation_service.db.commit = Mock()
        validation_service.db.refresh = Mock()
        
        result = validation_service.toggle_validation_rule(
            rule_id="rule-1",
            is_active=False
        )
        
        assert isinstance(result, ValidationRuleResponse)
        assert result.id == "rule-1"
        assert result.name == "Test Rule"
        assert result.is_active == False
        
        # Verify rule was updated
        assert mock_rule.is_active == False
        assert mock_rule.updated_at is not None
        
        # Verify database operations
        validation_service.db.commit.assert_called_once()
        validation_service.db.refresh.assert_called_once()
    
    def test_toggle_validation_rule_not_found(self, validation_service):
        """Test toggling non-existent validation rule"""
        validation_service.db.query.return_value.filter.return_value.first.return_value = None
        
        with pytest.raises(ValueError, match="Validation rule rule-1 not found"):
            validation_service.toggle_validation_rule(
                rule_id="rule-1",
                is_active=False
            ) 