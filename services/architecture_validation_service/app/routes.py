from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.schemas import (
    ValidationRunRequest, ValidationRunResponse, IssuesListResponse,
    ScorecardResponse, TraceabilityMatrixResponse, ValidationHistoryResponse,
    ExceptionCreateRequest, RuleToggleRequest, ValidationRuleResponse
)
from app.services import ValidationService
from app.deps import get_current_user, require_admin_or_owner, get_validation_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/validation", tags=["validation"])

@router.post("/run", response_model=ValidationRunResponse)
async def run_validation_cycle(
    request: ValidationRunRequest,
    current_user: dict = Depends(require_admin_or_owner()),
    validation_service: ValidationService = Depends(get_validation_service)
):
    """Trigger a full validation scan"""
    try:
        tenant_id = current_user["tenant_id"]
        user_id = current_user["user_id"]
        
        logger.info(f"Starting validation cycle for tenant {tenant_id} by user {user_id}")
        
        cycle = await validation_service.run_validation_cycle(
            tenant_id=tenant_id,
            user_id=user_id,
            rule_set_id=request.rule_set_id
        )
        
        return ValidationRunResponse(
            validation_cycle_id=cycle.id,
            status=cycle.execution_status,
            message=f"Validation cycle {cycle.id} started successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to start validation cycle: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start validation cycle: {str(e)}"
        )

@router.get("/issues", response_model=IssuesListResponse)
async def get_validation_issues(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    current_user: dict = Depends(get_current_user),
    validation_service: ValidationService = Depends(get_validation_service)
):
    """Get all validation issues for the tenant"""
    try:
        tenant_id = current_user["tenant_id"]
        
        issues = validation_service.get_validation_issues(
            tenant_id=tenant_id,
            skip=skip,
            limit=limit
        )
        
        return issues
        
    except Exception as e:
        logger.error(f"Failed to get validation issues: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get validation issues: {str(e)}"
        )

@router.get("/scorecard", response_model=ScorecardResponse)
async def get_validation_scorecard(
    validation_cycle_id: Optional[str] = Query(None, description="Specific validation cycle ID"),
    current_user: dict = Depends(get_current_user),
    validation_service: ValidationService = Depends(get_validation_service)
):
    """Get validation scorecard with maturity score breakdown"""
    try:
        tenant_id = current_user["tenant_id"]
        
        scorecard = validation_service.get_validation_scorecard(
            tenant_id=tenant_id,
            validation_cycle_id=validation_cycle_id
        )
        
        return scorecard
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to get validation scorecard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get validation scorecard: {str(e)}"
        )

@router.get("/traceability-matrix", response_model=List[TraceabilityMatrixResponse])
async def get_traceability_matrix(
    source_layer: Optional[str] = Query(None, description="Source layer filter"),
    target_layer: Optional[str] = Query(None, description="Target layer filter"),
    current_user: dict = Depends(get_current_user),
    validation_service: ValidationService = Depends(get_validation_service)
):
    """Get cross-layer traceability matrix"""
    try:
        tenant_id = current_user["tenant_id"]
        
        matrix = validation_service.get_traceability_matrix(
            tenant_id=tenant_id,
            source_layer=source_layer,
            target_layer=target_layer
        )
        
        return matrix
        
    except Exception as e:
        logger.error(f"Failed to get traceability matrix: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get traceability matrix: {str(e)}"
        )

@router.get("/history", response_model=ValidationHistoryResponse)
async def get_validation_history(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of records to return"),
    current_user: dict = Depends(get_current_user),
    validation_service: ValidationService = Depends(get_validation_service)
):
    """Get validation history for the tenant"""
    try:
        tenant_id = current_user["tenant_id"]
        
        history = validation_service.get_validation_history(
            tenant_id=tenant_id,
            skip=skip,
            limit=limit
        )
        
        return ValidationHistoryResponse(**history)
        
    except Exception as e:
        logger.error(f"Failed to get validation history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get validation history: {str(e)}"
        )

@router.post("/exceptions")
async def create_validation_exception(
    request: ExceptionCreateRequest,
    current_user: dict = Depends(require_admin_or_owner()),
    validation_service: ValidationService = Depends(get_validation_service)
):
    """Create a validation exception (whitelist intentional modeling gaps)"""
    try:
        tenant_id = current_user["tenant_id"]
        user_id = current_user["user_id"]
        
        exception = validation_service.create_validation_exception(
            tenant_id=tenant_id,
            user_id=user_id,
            entity_type=request.entity_type,
            entity_id=request.entity_id,
            reason=request.reason,
            rule_id=request.rule_id,
            expires_at=request.expires_at
        )
        
        logger.info(f"Created validation exception for {request.entity_type}:{request.entity_id}")
        
        return {
            "message": "Validation exception created successfully",
            "exception_id": exception.id
        }
        
    except Exception as e:
        logger.error(f"Failed to create validation exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create validation exception: {str(e)}"
        )

@router.patch("/rules/{rule_id}")
async def toggle_validation_rule(
    rule_id: str,
    request: RuleToggleRequest,
    current_user: dict = Depends(require_admin_or_owner()),
    validation_service: ValidationService = Depends(get_validation_service)
):
    """Toggle validation rule activation"""
    try:
        rule = validation_service.toggle_validation_rule(
            rule_id=rule_id,
            is_active=request.is_active
        )
        
        action = "activated" if request.is_active else "deactivated"
        logger.info(f"Validation rule {rule_id} {action} by user {current_user['user_id']}")
        
        return {
            "message": f"Validation rule {action} successfully",
            "rule_id": rule_id,
            "is_active": request.is_active
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to toggle validation rule: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to toggle validation rule: {str(e)}"
        )

@router.get("/rules", response_model=List[ValidationRuleResponse])
async def get_validation_rules(
    current_user: dict = Depends(get_current_user),
    validation_service: ValidationService = Depends(get_validation_service)
):
    """Get all validation rules"""
    try:
        # This would be implemented in the service layer
        # For now, return a placeholder
        return []
        
    except Exception as e:
        logger.error(f"Failed to get validation rules: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get validation rules: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "architecture_validation_service",
        "timestamp": "2024-01-15T10:30:00Z"
    }

@router.get("/metrics")
async def get_metrics():
    """Get service metrics"""
    return {
        "validation_cycles_total": 0,
        "validation_issues_total": 0,
        "validation_rules_active": 0,
        "validation_exceptions_total": 0,
        "average_maturity_score": 0.0
    } 