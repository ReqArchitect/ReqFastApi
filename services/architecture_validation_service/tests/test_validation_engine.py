import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from app.validation_engine import ValidationEngine
from app.schemas import ValidationContext, ValidationIssueCreate, IssueType, Severity
from app.models import ValidationRule, ValidationException
import json

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def mock_redis():
    return Mock()

@pytest.fixture
def validation_engine(mock_db, mock_redis):
    return ValidationEngine(mock_db, mock_redis)

@pytest.fixture
def validation_context():
    return ValidationContext(
        tenant_id="test-tenant-id",
        user_id="test-user-id",
        validation_cycle_id="test-cycle-id",
        rule_set_id=None
    )

@pytest.fixture
def traceability_rule():
    rule = Mock(spec=ValidationRule)
    rule.id = "rule-1"
    rule.name = "Goal-Capability Linkage"
    rule.rule_type = "traceability"
    rule.severity = "high"
    rule.rule_logic = json.dumps({
        "source_type": "goal",
        "target_type": "capability",
        "relationship_type": "supports",
        "min_connections": 1
    })
    return rule

@pytest.fixture
def completeness_rule():
    rule = Mock(spec=ValidationRule)
    rule.id = "rule-2"
    rule.name = "Business Process Completeness"
    rule.rule_type = "completeness"
    rule.severity = "medium"
    rule.rule_logic = json.dumps({
        "element_type": "business_process",
        "required_fields": ["name", "description", "owner"],
        "min_count": 1
    })
    return rule

@pytest.fixture
def alignment_rule():
    rule = Mock(spec=ValidationRule)
    rule.id = "rule-3"
    rule.name = "Motivation-Business Alignment"
    rule.rule_type = "alignment"
    rule.severity = "high"
    rule.rule_logic = json.dumps({
        "source_layer": "Motivation",
        "target_layer": "Business",
        "alignment_criteria": {
            "name_similarity": 0.8,
            "semantic_matching": True
        }
    })
    return rule

class TestValidationEngine:
    
    @pytest.mark.asyncio
    async def test_run_validation_cycle_success(self, validation_engine, validation_context, traceability_rule):
        """Test successful validation cycle execution"""
        # Mock database queries
        validation_engine.db.query.return_value.filter.return_value.all.return_value = [traceability_rule]
        validation_engine.db.query.return_value.filter.return_value.all.return_value = []
        
        # Mock HTTP client responses
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value.status_code = 200
            mock_client.return_value.__aenter__.return_value.get.return_value.json.return_value = [
                {"id": "goal-1", "name": "Test Goal", "type": "goal"}
            ]
            
            results = await validation_engine.run_validation_cycle(validation_context)
            
            assert len(results) == 1
            assert results[0].rule_id == "rule-1"
            assert results[0].rule_name == "Goal-Capability Linkage"
            assert not results[0].passed  # Should fail due to missing connections
    
    @pytest.mark.asyncio
    async def test_validate_traceability_missing_links(self, validation_engine, validation_context, traceability_rule):
        """Test traceability validation with missing links"""
        exceptions = set()
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value.status_code = 200
            mock_client.return_value.__aenter__.return_value.get.return_value.json.return_value = [
                {"id": "goal-1", "name": "Test Goal", "type": "goal"}
            ]
            
            issues = await validation_engine._validate_traceability(traceability_rule, validation_context, exceptions)
            
            assert len(issues) == 1
            assert issues[0].entity_type == "goal"
            assert issues[0].entity_id == "goal-1"
            assert issues[0].issue_type == IssueType.MISSING_LINK
            assert issues[0].severity == Severity.HIGH
    
    @pytest.mark.asyncio
    async def test_validate_traceability_with_exception(self, validation_engine, validation_context, traceability_rule):
        """Test traceability validation with exception"""
        exceptions = {("goal", "goal-1", "rule-1")}  # Exception for this specific case
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value.status_code = 200
            mock_client.return_value.__aenter__.return_value.get.return_value.json.return_value = [
                {"id": "goal-1", "name": "Test Goal", "type": "goal"}
            ]
            
            issues = await validation_engine._validate_traceability(traceability_rule, validation_context, exceptions)
            
            assert len(issues) == 0  # Should not create issue due to exception
    
    @pytest.mark.asyncio
    async def test_validate_completeness_missing_fields(self, validation_engine, validation_context, completeness_rule):
        """Test completeness validation with missing fields"""
        exceptions = set()
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value.status_code = 200
            mock_client.return_value.__aenter__.return_value.get.return_value.json.return_value = [
                {"id": "process-1", "name": "Test Process", "type": "business_process"}
                # Missing 'description' and 'owner' fields
            ]
            
            issues = await validation_engine._validate_completeness(completeness_rule, validation_context, exceptions)
            
            assert len(issues) == 1
            assert issues[0].entity_type == "business_process"
            assert issues[0].entity_id == "process-1"
            assert issues[0].issue_type == IssueType.INVALID_ENUM
            assert "description" in issues[0].description
            assert "owner" in issues[0].description
    
    @pytest.mark.asyncio
    async def test_validate_completeness_insufficient_count(self, validation_engine, validation_context, completeness_rule):
        """Test completeness validation with insufficient element count"""
        exceptions = set()
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value.status_code = 200
            mock_client.return_value.__aenter__.return_value.get.return_value.json.return_value = []
            # No business processes found
            
            issues = await validation_engine._validate_completeness(completeness_rule, validation_context, exceptions)
            
            assert len(issues) == 1
            assert issues[0].entity_type == "business_process"
            assert issues[0].entity_id == "count_check"
            assert issues[0].issue_type == IssueType.MISSING_LINK
            assert "0 found, 1 required" in issues[0].description
    
    @pytest.mark.asyncio
    async def test_validate_alignment_no_aligned_elements(self, validation_engine, validation_context, alignment_rule):
        """Test alignment validation with no aligned elements"""
        exceptions = set()
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value.status_code = 200
            mock_client.return_value.__aenter__.return_value.get.return_value.json.return_value = [
                {"id": "goal-1", "name": "Improve Customer Service", "type": "goal", "layer": "Motivation"},
                {"id": "capability-1", "name": "Customer Management", "type": "capability", "layer": "Business"}
            ]
            
            issues = await validation_engine._validate_alignment(alignment_rule, validation_context, exceptions)
            
            assert len(issues) == 1
            assert issues[0].entity_type == "goal"
            assert issues[0].entity_id == "goal-1"
            assert issues[0].issue_type == IssueType.BROKEN_TRACEABILITY
            assert "lacks alignment" in issues[0].description
    
    @pytest.mark.asyncio
    async def test_validate_alignment_with_aligned_elements(self, validation_engine, validation_context, alignment_rule):
        """Test alignment validation with aligned elements"""
        exceptions = set()
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value.status_code = 200
            mock_client.return_value.__aenter__.return_value.get.return_value.json.return_value = [
                {"id": "goal-1", "name": "Improve Customer Service", "type": "goal", "layer": "Motivation"},
                {"id": "capability-1", "name": "Improve Customer Service Capability", "type": "capability", "layer": "Business"}
            ]
            
            issues = await validation_engine._validate_alignment(alignment_rule, validation_context, exceptions)
            
            assert len(issues) == 0  # Should not create issues due to name similarity
    
    @pytest.mark.asyncio
    async def test_get_elements_service_error(self, validation_engine):
        """Test getting elements when service is unavailable"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value.status_code = 500
            
            elements = await validation_engine._get_elements("goal", "test-tenant")
            
            assert elements == []
    
    @pytest.mark.asyncio
    async def test_get_elements_network_error(self, validation_engine):
        """Test getting elements when network error occurs"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.side_effect = Exception("Network error")
            
            elements = await validation_engine._get_elements("goal", "test-tenant")
            
            assert elements == []
    
    def test_emit_validation_completed_event(self, validation_engine, validation_context):
        """Test emitting validation completed event"""
        validation_engine.redis.publish = Mock()
        
        validation_engine._emit_validation_completed_event(validation_context, 5, 1000.0)
        
        validation_engine.redis.publish.assert_called_once()
        call_args = validation_engine.redis.publish.call_args
        assert call_args[0][0] == "validation.completed"
        
        # Verify event data
        event_data = json.loads(call_args[0][1])
        assert event_data["validation_cycle_id"] == "test-cycle-id"
        assert event_data["tenant_id"] == "test-tenant-id"
        assert event_data["total_issues"] == 5
        assert event_data["execution_time_ms"] == 1000.0
    
    def test_emit_issue_detected_event(self, validation_engine):
        """Test emitting issue detected event"""
        validation_engine.redis.publish = Mock()
        
        issue = ValidationIssueCreate(
            tenant_id="test-tenant-id",
            entity_type="goal",
            entity_id="goal-1",
            issue_type=IssueType.MISSING_LINK,
            severity=Severity.HIGH,
            description="Test issue",
            recommended_fix="Test fix"
        )
        
        validation_engine._emit_issue_detected_event(issue)
        
        validation_engine.redis.publish.assert_called_once()
        call_args = validation_engine.redis.publish.call_args
        assert call_args[0][0] == "validation.issue_detected"
        
        # Verify event data
        event_data = json.loads(call_args[0][1])
        assert event_data["tenant_id"] == "test-tenant-id"
        assert event_data["entity_type"] == "goal"
        assert event_data["entity_id"] == "goal-1"
        assert event_data["issue_type"] == "missing_link"
        assert event_data["severity"] == "high"
    
    @pytest.mark.asyncio
    async def test_execute_rule_unknown_type(self, validation_engine, validation_context):
        """Test executing rule with unknown type"""
        rule = Mock(spec=ValidationRule)
        rule.id = "rule-unknown"
        rule.name = "Unknown Rule"
        rule.rule_type = "unknown_type"
        rule.severity = "medium"
        
        exceptions = set()
        
        result = await validation_engine._execute_rule(rule, validation_context, exceptions)
        
        assert result.rule_id == "rule-unknown"
        assert result.rule_name == "Unknown Rule"
        assert len(result.issues_found) == 0  # No issues for unknown type
        assert result.passed
    
    @pytest.mark.asyncio
    async def test_execute_rule_exception_handling(self, validation_engine, validation_context, traceability_rule):
        """Test rule execution with exception handling"""
        exceptions = set()
        
        # Mock to raise exception
        with patch.object(validation_engine, '_validate_traceability', side_effect=Exception("Test error")):
            result = await validation_engine._execute_rule(traceability_rule, validation_context, exceptions)
            
            assert result.rule_id == "rule-1"
            assert result.rule_name == "Goal-Capability Linkage"
            assert len(result.issues_found) == 1
            assert result.issues_found[0].entity_type == "system"
            assert result.issues_found[0].entity_id == "validation_engine"
            assert result.issues_found[0].issue_type == IssueType.BROKEN_TRACEABILITY
            assert not result.passed 