from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from .database import get_db
from .deps import (
    get_current_user, require_owner, require_admin, 
    require_editor, require_viewer, get_business_process,
    get_process_step, get_process_link
)
from .services import BusinessProcessService, ProcessStepService, ProcessLinkService
from .schemas import (
    BusinessProcess, BusinessProcessCreate, BusinessProcessUpdate,
    BusinessProcessList, BusinessProcessWithSteps, BusinessProcessWithLinks,
    ProcessStep, ProcessStepCreate, ProcessStepUpdate,
    ProcessLink, ProcessLinkCreate, ProcessLinkUpdate,
    ProcessFlowMap, ProcessRealizationHealth,
    BusinessProcessByRole, BusinessProcessByFunction, BusinessProcessByGoal,
    BusinessProcessByStatus, BusinessProcessByCriticality
)

router = APIRouter()

# Business Process CRUD endpoints
@router.post("/business-processes/", response_model=BusinessProcess, status_code=status.HTTP_201_CREATED)
def create_business_process(
    business_process: BusinessProcessCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_editor)
):
    """Create a new business process"""
    return BusinessProcessService.create_business_process(
        db=db,
        business_process_data=business_process,
        tenant_id=current_user["tenant_id"],
        user_id=current_user["user_id"]
    )

@router.get("/business-processes/", response_model=BusinessProcessList)
def get_business_processes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    process_type: Optional[str] = Query(None),
    organizational_unit: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    criticality: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get business processes with optional filtering"""
    business_processes = BusinessProcessService.get_business_processes(
        db=db,
        tenant_id=current_user["tenant_id"],
        skip=skip,
        limit=limit,
        process_type=process_type,
        organizational_unit=organizational_unit,
        status=status,
        criticality=criticality
    )
    
    total = len(business_processes)  # In production, use count query
    
    return BusinessProcessList(
        business_processes=business_processes,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/business-processes/{business_process_id}", response_model=BusinessProcess)
def get_business_process(
    business_process_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get a specific business process"""
    business_process = BusinessProcessService.get_business_process(
        db=db,
        business_process_id=business_process_id,
        tenant_id=current_user["tenant_id"]
    )
    
    if not business_process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business process not found"
        )
    
    return business_process

@router.put("/business-processes/{business_process_id}", response_model=BusinessProcess)
def update_business_process(
    business_process_id: str,
    business_process_update: BusinessProcessUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_editor)
):
    """Update a business process"""
    business_process = BusinessProcessService.update_business_process(
        db=db,
        business_process_id=business_process_id,
        business_process_data=business_process_update,
        tenant_id=current_user["tenant_id"]
    )
    
    if not business_process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business process not found"
        )
    
    return business_process

@router.delete("/business-processes/{business_process_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_business_process(
    business_process_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """Delete a business process"""
    success = BusinessProcessService.delete_business_process(
        db=db,
        business_process_id=business_process_id,
        tenant_id=current_user["tenant_id"]
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business process not found"
        )

# Business Process Analysis endpoints
@router.get("/business-processes/{business_process_id}/flow-map", response_model=ProcessFlowMap)
def get_process_flow_map(
    business_process_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get process flow map analysis"""
    flow_map = BusinessProcessService.get_process_flow_map(
        db=db,
        business_process_id=business_process_id,
        tenant_id=current_user["tenant_id"]
    )
    
    if not flow_map:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business process not found"
        )
    
    return flow_map

@router.get("/business-processes/{business_process_id}/realization-health", response_model=ProcessRealizationHealth)
def get_process_realization_health(
    business_process_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get process realization health analysis"""
    health = BusinessProcessService.get_process_realization_health(
        db=db,
        business_process_id=business_process_id,
        tenant_id=current_user["tenant_id"]
    )
    
    if not health:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business process not found"
        )
    
    return health

# Business Process Domain Queries
@router.get("/business-processes/by-role/{role_id}", response_model=List[BusinessProcessByRole])
def get_business_processes_by_role(
    role_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get business processes by role"""
    return BusinessProcessService.get_business_processes_by_role(
        db=db,
        tenant_id=current_user["tenant_id"],
        role_id=role_id
    )

@router.get("/business-processes/by-function/{business_function_id}", response_model=List[BusinessProcessByFunction])
def get_business_processes_by_function(
    business_function_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get business processes by business function"""
    return BusinessProcessService.get_business_processes_by_function(
        db=db,
        tenant_id=current_user["tenant_id"],
        business_function_id=business_function_id
    )

@router.get("/business-processes/by-goal/{goal_id}", response_model=List[BusinessProcessByGoal])
def get_business_processes_by_goal(
    goal_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get business processes by goal"""
    return BusinessProcessService.get_business_processes_by_goal(
        db=db,
        tenant_id=current_user["tenant_id"],
        goal_id=goal_id
    )

@router.get("/business-processes/by-status/{status}", response_model=List[BusinessProcessByStatus])
def get_business_processes_by_status(
    status: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get business processes by status"""
    return BusinessProcessService.get_business_processes_by_status(
        db=db,
        tenant_id=current_user["tenant_id"],
        status=status
    )

@router.get("/business-processes/by-criticality/{criticality}", response_model=List[BusinessProcessByCriticality])
def get_business_processes_by_criticality(
    criticality: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get business processes by criticality"""
    return BusinessProcessService.get_business_processes_by_criticality(
        db=db,
        tenant_id=current_user["tenant_id"],
        criticality=criticality
    )

# Process Steps endpoints
@router.post("/business-processes/{business_process_id}/steps/", response_model=ProcessStep, status_code=status.HTTP_201_CREATED)
def create_process_step(
    business_process_id: str,
    step: ProcessStepCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_editor)
):
    """Create a new process step"""
    process_step = ProcessStepService.create_process_step(
        db=db,
        business_process_id=business_process_id,
        step_data=step,
        tenant_id=current_user["tenant_id"]
    )
    
    if not process_step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business process not found"
        )
    
    return process_step

@router.get("/business-processes/{business_process_id}/steps/", response_model=List[ProcessStep])
def get_process_steps(
    business_process_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get all steps for a business process"""
    steps = ProcessStepService.get_process_steps(
        db=db,
        business_process_id=business_process_id,
        tenant_id=current_user["tenant_id"]
    )
    
    return steps

@router.put("/steps/{step_id}", response_model=ProcessStep)
def update_process_step(
    step_id: str,
    step_update: ProcessStepUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_editor)
):
    """Update a process step"""
    step = ProcessStepService.update_process_step(
        db=db,
        step_id=step_id,
        step_data=step_update,
        tenant_id=current_user["tenant_id"]
    )
    
    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process step not found"
        )
    
    return step

@router.delete("/steps/{step_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_process_step(
    step_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_editor)
):
    """Delete a process step"""
    success = ProcessStepService.delete_process_step(
        db=db,
        step_id=step_id,
        tenant_id=current_user["tenant_id"]
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process step not found"
        )

# Process Links endpoints
@router.post("/business-processes/{business_process_id}/links/", response_model=ProcessLink, status_code=status.HTTP_201_CREATED)
def create_process_link(
    business_process_id: str,
    link: ProcessLinkCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_editor)
):
    """Create a new process link"""
    process_link = ProcessLinkService.create_process_link(
        db=db,
        business_process_id=business_process_id,
        link_data=link,
        tenant_id=current_user["tenant_id"],
        user_id=current_user["user_id"]
    )
    
    if not process_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business process not found"
        )
    
    return process_link

@router.get("/business-processes/{business_process_id}/links/", response_model=List[ProcessLink])
def get_process_links(
    business_process_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get all links for a business process"""
    links = ProcessLinkService.get_process_links(
        db=db,
        business_process_id=business_process_id,
        tenant_id=current_user["tenant_id"]
    )
    
    return links

@router.put("/links/{link_id}", response_model=ProcessLink)
def update_process_link(
    link_id: str,
    link_update: ProcessLinkUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_editor)
):
    """Update a process link"""
    link = ProcessLinkService.update_process_link(
        db=db,
        link_id=link_id,
        link_data=link_update,
        tenant_id=current_user["tenant_id"]
    )
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process link not found"
        )
    
    return link

@router.delete("/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_process_link(
    link_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_editor)
):
    """Delete a process link"""
    success = ProcessLinkService.delete_process_link(
        db=db,
        link_id=link_id,
        tenant_id=current_user["tenant_id"]
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process link not found"
        )

# Health and metrics endpoints
@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "businessprocess_service"}

@router.get("/metrics")
def get_metrics():
    """Get service metrics"""
    return {
        "service": "businessprocess_service",
        "version": "1.0.0",
        "status": "operational"
    } 