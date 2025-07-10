import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import (
    ValidationCycle, ValidationIssue, ValidationRule, 
    ValidationException, ValidationScorecard, TraceabilityMatrix
)
from app.schemas import (
    ValidationContext, ValidationResult, ValidationIssueCreate,
    ValidationCycleCreate, ValidationCycleResponse, ValidationIssueResponse,
    ValidationRuleResponse, ValidationExceptionResponse, ValidationScorecardResponse,
    TraceabilityMatrixResponse, IssuesListResponse, ScorecardResponse
)
from app.validation_engine import ValidationEngine
import redis
import json

logger = logging.getLogger(__name__)

class ValidationService:
    """Service layer for validation operations"""
    
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis = redis_client
        self.validation_engine = ValidationEngine(db, redis_client)
    
    async def run_validation_cycle(self, tenant_id: str, user_id: str, rule_set_id: Optional[str] = None) -> ValidationCycleResponse:
        """Run a complete validation cycle"""
        try:
            # Create validation cycle
            cycle = ValidationCycle(
                tenant_id=tenant_id,
                triggered_by=user_id,
                rule_set_id=rule_set_id,
                execution_status="running"
            )
            self.db.add(cycle)
            self.db.commit()
            self.db.refresh(cycle)
            
            # Create validation context
            context = ValidationContext(
                tenant_id=tenant_id,
                user_id=user_id,
                validation_cycle_id=cycle.id,
                rule_set_id=rule_set_id
            )
            
            # Run validation in background
            asyncio.create_task(self._run_validation_async(context, cycle))
            
            return ValidationCycleResponse(
                id=cycle.id,
                tenant_id=cycle.tenant_id,
                start_time=cycle.start_time,
                end_time=cycle.end_time,
                triggered_by=cycle.triggered_by,
                rule_set_id=cycle.rule_set_id,
                total_issues_found=cycle.total_issues_found,
                execution_status=cycle.execution_status,
                maturity_score=cycle.maturity_score,
                created_at=cycle.created_at,
                updated_at=cycle.updated_at
            )
            
        except Exception as e:
            logger.error(f"Failed to start validation cycle: {e}")
            raise
    
    async def _run_validation_async(self, context: ValidationContext, cycle: ValidationCycle):
        """Run validation asynchronously"""
        try:
            # Run validation engine
            results = await self.validation_engine.run_validation_cycle(context)
            
            # Process results and create issues
            total_issues = 0
            for result in results:
                for issue_data in result.issues_found:
                    issue = ValidationIssue(
                        tenant_id=issue_data.tenant_id,
                        validation_cycle_id=cycle.id,
                        entity_type=issue_data.entity_type,
                        entity_id=issue_data.entity_id,
                        issue_type=issue_data.issue_type.value,
                        severity=issue_data.severity.value,
                        description=issue_data.description,
                        recommended_fix=issue_data.recommended_fix,
                        metadata=issue_data.metadata
                    )
                    self.db.add(issue)
                    total_issues += 1
            
            # Update cycle status
            cycle.end_time = datetime.utcnow()
            cycle.total_issues_found = total_issues
            cycle.execution_status = "completed"
            
            # Calculate maturity score
            cycle.maturity_score = self._calculate_maturity_score(total_issues)
            
            self.db.commit()
            
            logger.info(f"Validation cycle {cycle.id} completed with {total_issues} issues")
            
        except Exception as e:
            logger.error(f"Validation cycle {cycle.id} failed: {e}")
            cycle.execution_status = "failed"
            cycle.end_time = datetime.utcnow()
            self.db.commit()
    
    def _calculate_maturity_score(self, total_issues: int) -> float:
        """Calculate maturity score based on issues found"""
        # Simple scoring algorithm - can be enhanced
        if total_issues == 0:
            return 100.0
        elif total_issues <= 5:
            return 90.0
        elif total_issues <= 10:
            return 80.0
        elif total_issues <= 20:
            return 70.0
        elif total_issues <= 50:
            return 60.0
        else:
            return 50.0
    
    def get_validation_issues(self, tenant_id: str, skip: int = 0, limit: int = 100) -> IssuesListResponse:
        """Get validation issues for a tenant"""
        try:
            # Get issues with pagination
            issues_query = self.db.query(ValidationIssue).filter(
                ValidationIssue.tenant_id == tenant_id
            ).order_by(desc(ValidationIssue.timestamp))
            
            total_count = issues_query.count()
            issues = issues_query.offset(skip).limit(limit).all()
            
            # Count by severity
            critical_count = self.db.query(ValidationIssue).filter(
                ValidationIssue.tenant_id == tenant_id,
                ValidationIssue.severity == "critical"
            ).count()
            
            high_count = self.db.query(ValidationIssue).filter(
                ValidationIssue.tenant_id == tenant_id,
                ValidationIssue.severity == "high"
            ).count()
            
            medium_count = self.db.query(ValidationIssue).filter(
                ValidationIssue.tenant_id == tenant_id,
                ValidationIssue.severity == "medium"
            ).count()
            
            low_count = self.db.query(ValidationIssue).filter(
                ValidationIssue.tenant_id == tenant_id,
                ValidationIssue.severity == "low"
            ).count()
            
            return IssuesListResponse(
                issues=[ValidationIssueResponse(
                    id=issue.id,
                    tenant_id=issue.tenant_id,
                    validation_cycle_id=issue.validation_cycle_id,
                    entity_type=issue.entity_type,
                    entity_id=issue.entity_id,
                    issue_type=issue.issue_type,
                    severity=issue.severity,
                    description=issue.description,
                    recommended_fix=issue.recommended_fix,
                    metadata=issue.metadata,
                    timestamp=issue.timestamp,
                    is_resolved=issue.is_resolved,
                    resolved_at=issue.resolved_at,
                    resolved_by=issue.resolved_by
                ) for issue in issues],
                total_count=total_count,
                critical_count=critical_count,
                high_count=high_count,
                medium_count=medium_count,
                low_count=low_count
            )
            
        except Exception as e:
            logger.error(f"Failed to get validation issues: {e}")
            raise
    
    def get_validation_scorecard(self, tenant_id: str, validation_cycle_id: Optional[str] = None) -> ScorecardResponse:
        """Get validation scorecard for a tenant"""
        try:
            # Get the latest validation cycle if not specified
            if not validation_cycle_id:
                latest_cycle = self.db.query(ValidationCycle).filter(
                    ValidationCycle.tenant_id == tenant_id,
                    ValidationCycle.execution_status == "completed"
                ).order_by(desc(ValidationCycle.end_time)).first()
                
                if not latest_cycle:
                    raise ValueError("No completed validation cycles found")
                
                validation_cycle_id = latest_cycle.id
            
            # Get scorecards for all layers
            scorecards = self.db.query(ValidationScorecard).filter(
                ValidationScorecard.tenant_id == tenant_id,
                ValidationScorecard.validation_cycle_id == validation_cycle_id
            ).all()
            
            # Calculate overall score
            if scorecards:
                overall_score = sum(sc.overall_score for sc in scorecards) / len(scorecards)
            else:
                overall_score = 0.0
            
            return ScorecardResponse(
                tenant_id=tenant_id,
                validation_cycle_id=validation_cycle_id,
                overall_maturity_score=overall_score,
                layer_scores=[ValidationScorecardResponse(
                    id=sc.id,
                    tenant_id=sc.tenant_id,
                    validation_cycle_id=sc.validation_cycle_id,
                    layer=sc.layer,
                    completeness_score=sc.completeness_score,
                    traceability_score=sc.traceability_score,
                    alignment_score=sc.alignment_score,
                    overall_score=sc.overall_score,
                    issues_count=sc.issues_count,
                    critical_issues=sc.critical_issues,
                    high_issues=sc.high_issues,
                    medium_issues=sc.medium_issues,
                    low_issues=sc.low_issues,
                    created_at=sc.created_at
                ) for sc in scorecards],
                summary={
                    "total_layers": len(scorecards),
                    "average_score": overall_score,
                    "best_layer": max(scorecards, key=lambda x: x.overall_score).layer if scorecards else None,
                    "worst_layer": min(scorecards, key=lambda x: x.overall_score).layer if scorecards else None
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to get validation scorecard: {e}")
            raise
    
    def get_traceability_matrix(self, tenant_id: str, source_layer: Optional[str] = None, 
                               target_layer: Optional[str] = None) -> List[TraceabilityMatrixResponse]:
        """Get traceability matrix for a tenant"""
        try:
            query = self.db.query(TraceabilityMatrix).filter(
                TraceabilityMatrix.tenant_id == tenant_id
            )
            
            if source_layer:
                query = query.filter(TraceabilityMatrix.source_layer == source_layer)
            
            if target_layer:
                query = query.filter(TraceabilityMatrix.target_layer == target_layer)
            
            matrices = query.all()
            
            return [TraceabilityMatrixResponse(
                id=matrix.id,
                tenant_id=matrix.tenant_id,
                source_layer=matrix.source_layer,
                target_layer=matrix.target_layer,
                source_entity_type=matrix.source_entity_type,
                target_entity_type=matrix.target_entity_type,
                relationship_type=matrix.relationship_type,
                connection_count=matrix.connection_count,
                missing_connections=matrix.missing_connections,
                strength_score=matrix.strength_score,
                last_updated=matrix.last_updated
            ) for matrix in matrices]
            
        except Exception as e:
            logger.error(f"Failed to get traceability matrix: {e}")
            raise
    
    def get_validation_history(self, tenant_id: str, skip: int = 0, limit: int = 50) -> Dict[str, Any]:
        """Get validation history for a tenant"""
        try:
            # Get validation cycles
            cycles_query = self.db.query(ValidationCycle).filter(
                ValidationCycle.tenant_id == tenant_id
            ).order_by(desc(ValidationCycle.start_time))
            
            total_cycles = cycles_query.count()
            cycles = cycles_query.offset(skip).limit(limit).all()
            
            # Calculate average maturity score
            completed_cycles = [c for c in cycles if c.maturity_score is not None]
            average_score = sum(c.maturity_score for c in completed_cycles) / len(completed_cycles) if completed_cycles else 0.0
            
            # Get last validation date
            last_validation = self.db.query(ValidationCycle).filter(
                ValidationCycle.tenant_id == tenant_id,
                ValidationCycle.execution_status == "completed"
            ).order_by(desc(ValidationCycle.end_time)).first()
            
            return {
                "cycles": [ValidationCycleResponse(
                    id=cycle.id,
                    tenant_id=cycle.tenant_id,
                    start_time=cycle.start_time,
                    end_time=cycle.end_time,
                    triggered_by=cycle.triggered_by,
                    rule_set_id=cycle.rule_set_id,
                    total_issues_found=cycle.total_issues_found,
                    execution_status=cycle.execution_status,
                    maturity_score=cycle.maturity_score,
                    created_at=cycle.created_at,
                    updated_at=cycle.updated_at
                ) for cycle in cycles],
                "total_cycles": total_cycles,
                "average_maturity_score": average_score,
                "last_validation_date": last_validation.end_time if last_validation else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get validation history: {e}")
            raise
    
    def create_validation_exception(self, tenant_id: str, user_id: str, entity_type: str, 
                                   entity_id: str, reason: str, rule_id: Optional[str] = None,
                                   expires_at: Optional[datetime] = None) -> ValidationExceptionResponse:
        """Create a validation exception"""
        try:
            exception = ValidationException(
                tenant_id=tenant_id,
                entity_type=entity_type,
                entity_id=entity_id,
                rule_id=rule_id,
                reason=reason,
                created_by=user_id,
                expires_at=expires_at
            )
            
            self.db.add(exception)
            self.db.commit()
            self.db.refresh(exception)
            
            return ValidationExceptionResponse(
                id=exception.id,
                tenant_id=exception.tenant_id,
                entity_type=exception.entity_type,
                entity_id=exception.entity_id,
                rule_id=exception.rule_id,
                reason=exception.reason,
                created_by=exception.created_by,
                created_at=exception.created_at,
                is_active=exception.is_active,
                expires_at=exception.expires_at
            )
            
        except Exception as e:
            logger.error(f"Failed to create validation exception: {e}")
            raise
    
    def toggle_validation_rule(self, rule_id: str, is_active: bool) -> ValidationRuleResponse:
        """Toggle validation rule activation"""
        try:
            rule = self.db.query(ValidationRule).filter(ValidationRule.id == rule_id).first()
            if not rule:
                raise ValueError(f"Validation rule {rule_id} not found")
            
            rule.is_active = is_active
            rule.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(rule)
            
            return ValidationRuleResponse(
                id=rule.id,
                name=rule.name,
                description=rule.description,
                rule_type=rule.rule_type,
                scope=rule.scope,
                rule_logic=rule.rule_logic,
                severity=rule.severity,
                is_active=rule.is_active,
                created_at=rule.created_at,
                updated_at=rule.updated_at
            )
            
        except Exception as e:
            logger.error(f"Failed to toggle validation rule: {e}")
            raise 