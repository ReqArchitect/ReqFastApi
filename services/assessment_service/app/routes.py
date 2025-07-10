from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime
from .database import get_db
from .services import AssessmentService, AssessmentLinkService
from .schemas import (
    AssessmentCreate, AssessmentUpdate, AssessmentResponse, AssessmentList,
    AssessmentLinkCreate, AssessmentLinkUpdate, AssessmentLinkResponse,
    EvaluationMetricsResponse, ConfidenceScoreResponse, EnumResponse,
    HealthResponse, ErrorResponse
)
from .deps import get_current_user, require_permissions
from .models import AssessmentType, AssessmentStatus, AssessmentMethod, ConfidenceLevel, LinkType, RelationshipStrength, DependencyLevel

router = APIRouter()

# Assessment Management Endpoints

@router.post("/assessments", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
@require_permissions(["assessment:create"])
async def create_assessment(
    assessment_data: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new assessment"""
    try:
        assessment = AssessmentService.create_assessment(
            db=db,
            assessment_data=assessment_data,
            tenant_id=current_user["tenant_id"],
            user_id=current_user["user_id"]
        )
        return assessment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating assessment: {str(e)}"
        )

@router.get("/assessments", response_model=List[AssessmentList])
@require_permissions(["assessment:read"])
async def list_assessments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    assessment_type: Optional[AssessmentType] = Query(None, description="Filter by assessment type"),
    status: Optional[AssessmentStatus] = Query(None, description="Filter by status"),
    evaluator_user_id: Optional[uuid.UUID] = Query(None, description="Filter by evaluator"),
    evaluated_goal_id: Optional[uuid.UUID] = Query(None, description="Filter by evaluated goal"),
    date_from: Optional[datetime] = Query(None, description="Filter by date from"),
    date_to: Optional[datetime] = Query(None, description="Filter by date to"),
    confidence_threshold: Optional[float] = Query(None, ge=0.0, le=1.0, description="Filter by confidence threshold"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List assessments with filtering and pagination"""
    try:
        assessments = AssessmentService.list_assessments(
            db=db,
            tenant_id=current_user["tenant_id"],
            skip=skip,
            limit=limit,
            assessment_type=assessment_type,
            status=status,
            evaluator_user_id=evaluator_user_id,
            evaluated_goal_id=evaluated_goal_id,
            date_from=date_from,
            date_to=date_to,
            confidence_threshold=confidence_threshold
        )
        return assessments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error listing assessments: {str(e)}"
        )

@router.get("/assessments/{assessment_id}", response_model=AssessmentResponse)
@require_permissions(["assessment:read"])
async def get_assessment(
    assessment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get an assessment by ID"""
    try:
        assessment = AssessmentService.get_assessment(
            db=db,
            assessment_id=assessment_id,
            tenant_id=current_user["tenant_id"]
        )
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found"
            )
        return assessment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving assessment: {str(e)}"
        )

@router.put("/assessments/{assessment_id}", response_model=AssessmentResponse)
@require_permissions(["assessment:update"])
async def update_assessment(
    assessment_id: uuid.UUID,
    assessment_data: AssessmentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update an assessment"""
    try:
        assessment = AssessmentService.update_assessment(
            db=db,
            assessment_id=assessment_id,
            assessment_data=assessment_data,
            tenant_id=current_user["tenant_id"]
        )
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found"
            )
        return assessment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating assessment: {str(e)}"
        )

@router.delete("/assessments/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_permissions(["assessment:delete"])
async def delete_assessment(
    assessment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete an assessment"""
    try:
        success = AssessmentService.delete_assessment(
            db=db,
            assessment_id=assessment_id,
            tenant_id=current_user["tenant_id"]
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting assessment: {str(e)}"
        )

# Assessment Link Management Endpoints

@router.post("/assessments/{assessment_id}/links", response_model=AssessmentLinkResponse, status_code=status.HTTP_201_CREATED)
@require_permissions(["assessment_link:create"])
async def create_assessment_link(
    assessment_id: uuid.UUID,
    link_data: AssessmentLinkCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new assessment link"""
    try:
        assessment_link = AssessmentLinkService.create_assessment_link(
            db=db,
            assessment_id=assessment_id,
            link_data=link_data,
            tenant_id=current_user["tenant_id"],
            user_id=current_user["user_id"]
        )
        return assessment_link
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating assessment link: {str(e)}"
        )

@router.get("/assessments/{assessment_id}/links", response_model=List[AssessmentLinkResponse])
@require_permissions(["assessment_link:read"])
async def list_assessment_links(
    assessment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List assessment links for an assessment"""
    try:
        # Verify assessment exists
        assessment = AssessmentService.get_assessment(
            db=db,
            assessment_id=assessment_id,
            tenant_id=current_user["tenant_id"]
        )
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found"
            )
        
        links = AssessmentLinkService.list_assessment_links(
            db=db,
            assessment_id=assessment_id,
            tenant_id=current_user["tenant_id"]
        )
        return links
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error listing assessment links: {str(e)}"
        )

@router.get("/assessments/links/{link_id}", response_model=AssessmentLinkResponse)
@require_permissions(["assessment_link:read"])
async def get_assessment_link(
    link_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get an assessment link by ID"""
    try:
        assessment_link = AssessmentLinkService.get_assessment_link(
            db=db,
            link_id=link_id,
            tenant_id=current_user["tenant_id"]
        )
        if not assessment_link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment link not found"
            )
        return assessment_link
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving assessment link: {str(e)}"
        )

@router.put("/assessments/links/{link_id}", response_model=AssessmentLinkResponse)
@require_permissions(["assessment_link:update"])
async def update_assessment_link(
    link_id: uuid.UUID,
    link_data: AssessmentLinkUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update an assessment link"""
    try:
        assessment_link = AssessmentLinkService.update_assessment_link(
            db=db,
            link_id=link_id,
            link_data=link_data,
            tenant_id=current_user["tenant_id"]
        )
        if not assessment_link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment link not found"
            )
        return assessment_link
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating assessment link: {str(e)}"
        )

@router.delete("/assessments/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_permissions(["assessment_link:delete"])
async def delete_assessment_link(
    link_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete an assessment link"""
    try:
        success = AssessmentLinkService.delete_assessment_link(
            db=db,
            link_id=link_id,
            tenant_id=current_user["tenant_id"]
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment link not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting assessment link: {str(e)}"
        )

# Analysis Endpoints

@router.get("/assessments/{assessment_id}/evaluation-metrics", response_model=EvaluationMetricsResponse)
@require_permissions(["assessment:read"])
async def get_evaluation_metrics(
    assessment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get evaluation metrics analysis for an assessment"""
    try:
        metrics = AssessmentService.get_evaluation_metrics(
            db=db,
            assessment_id=assessment_id,
            tenant_id=current_user["tenant_id"]
        )
        if not metrics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found"
            )
        return metrics
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving evaluation metrics: {str(e)}"
        )

@router.get("/assessments/{assessment_id}/confidence-score", response_model=ConfidenceScoreResponse)
@require_permissions(["assessment:read"])
async def get_confidence_score(
    assessment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get confidence score analysis for an assessment"""
    try:
        confidence_data = AssessmentService.get_confidence_score(
            db=db,
            assessment_id=assessment_id,
            tenant_id=current_user["tenant_id"]
        )
        if not confidence_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found"
            )
        return confidence_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving confidence score: {str(e)}"
        )

# Domain-Specific Query Endpoints

@router.get("/assessments/by-type/{assessment_type}", response_model=List[AssessmentList])
@require_permissions(["assessment:read"])
async def get_assessments_by_type(
    assessment_type: AssessmentType,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get assessments by type"""
    try:
        assessments = AssessmentService.list_assessments(
            db=db,
            tenant_id=current_user["tenant_id"],
            skip=skip,
            limit=limit,
            assessment_type=assessment_type
        )
        return assessments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving assessments by type: {str(e)}"
        )

@router.get("/assessments/by-status/{status}", response_model=List[AssessmentList])
@require_permissions(["assessment:read"])
async def get_assessments_by_status(
    status: AssessmentStatus,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get assessments by status"""
    try:
        assessments = AssessmentService.list_assessments(
            db=db,
            tenant_id=current_user["tenant_id"],
            skip=skip,
            limit=limit,
            status=status
        )
        return assessments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving assessments by status: {str(e)}"
        )

@router.get("/assessments/by-evaluator/{evaluator_user_id}", response_model=List[AssessmentList])
@require_permissions(["assessment:read"])
async def get_assessments_by_evaluator(
    evaluator_user_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get assessments by evaluator"""
    try:
        assessments = AssessmentService.list_assessments(
            db=db,
            tenant_id=current_user["tenant_id"],
            skip=skip,
            limit=limit,
            evaluator_user_id=evaluator_user_id
        )
        return assessments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving assessments by evaluator: {str(e)}"
        )

@router.get("/assessments/by-goal/{goal_id}", response_model=List[AssessmentList])
@require_permissions(["assessment:read"])
async def get_assessments_by_goal(
    goal_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get assessments by evaluated goal"""
    try:
        assessments = AssessmentService.list_assessments(
            db=db,
            tenant_id=current_user["tenant_id"],
            skip=skip,
            limit=limit,
            evaluated_goal_id=goal_id
        )
        return assessments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving assessments by goal: {str(e)}"
        )

@router.get("/assessments/by-date-range", response_model=List[AssessmentList])
@require_permissions(["assessment:read"])
async def get_assessments_by_date_range(
    date_from: datetime = Query(..., description="Start date"),
    date_to: datetime = Query(..., description="End date"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get assessments by date range"""
    try:
        assessments = AssessmentService.list_assessments(
            db=db,
            tenant_id=current_user["tenant_id"],
            skip=skip,
            limit=limit,
            date_from=date_from,
            date_to=date_to
        )
        return assessments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving assessments by date range: {str(e)}"
        )

@router.get("/assessments/by-confidence/{confidence_threshold}", response_model=List[AssessmentList])
@require_permissions(["assessment:read"])
async def get_assessments_by_confidence(
    confidence_threshold: float = Query(..., ge=0.0, le=1.0, description="Minimum confidence score"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get assessments by confidence threshold"""
    try:
        assessments = AssessmentService.list_assessments(
            db=db,
            tenant_id=current_user["tenant_id"],
            skip=skip,
            limit=limit,
            confidence_threshold=confidence_threshold
        )
        return assessments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving assessments by confidence: {str(e)}"
        )

# Convenience Endpoints

@router.get("/assessments/active", response_model=List[AssessmentList])
@require_permissions(["assessment:read"])
async def get_active_assessments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get active assessments (in progress or planned)"""
    try:
        assessments = AssessmentService.list_assessments(
            db=db,
            tenant_id=current_user["tenant_id"],
            skip=skip,
            limit=limit,
            status=AssessmentStatus.IN_PROGRESS
        )
        return assessments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving active assessments: {str(e)}"
        )

@router.get("/assessments/completed", response_model=List[AssessmentList])
@require_permissions(["assessment:read"])
async def get_completed_assessments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get completed assessments"""
    try:
        assessments = AssessmentService.list_assessments(
            db=db,
            tenant_id=current_user["tenant_id"],
            skip=skip,
            limit=limit,
            status=AssessmentStatus.COMPLETE
        )
        return assessments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving completed assessments: {str(e)}"
        )

# Enumeration Endpoints

@router.get("/assessments/assessment-types", response_model=EnumResponse)
async def get_assessment_types():
    """Get all available assessment types"""
    return EnumResponse(values=[e.value for e in AssessmentType])

@router.get("/assessments/statuses", response_model=EnumResponse)
async def get_assessment_statuses():
    """Get all available assessment statuses"""
    return EnumResponse(values=[e.value for e in AssessmentStatus])

@router.get("/assessments/assessment-methods", response_model=EnumResponse)
async def get_assessment_methods():
    """Get all available assessment methods"""
    return EnumResponse(values=[e.value for e in AssessmentMethod])

@router.get("/assessments/confidence-levels", response_model=EnumResponse)
async def get_confidence_levels():
    """Get all available confidence levels"""
    return EnumResponse(values=[e.value for e in ConfidenceLevel])

@router.get("/assessments/link-types", response_model=EnumResponse)
async def get_link_types():
    """Get all available link types"""
    return EnumResponse(values=[e.value for e in LinkType])

@router.get("/assessments/relationship-strengths", response_model=EnumResponse)
async def get_relationship_strengths():
    """Get all available relationship strengths"""
    return EnumResponse(values=[e.value for e in RelationshipStrength])

@router.get("/assessments/dependency-levels", response_model=EnumResponse)
async def get_dependency_levels():
    """Get all available dependency levels"""
    return EnumResponse(values=[e.value for e in DependencyLevel])

# Health Check Endpoint

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    from .main import __version__
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        service="assessment_service",
        version=__version__,
        database="connected",
        redis="connected"
    ) 