from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
import json
import uuid
from datetime import datetime
import redis
import os
from dotenv import load_dotenv

from .models import BusinessProcess, ProcessStep, ProcessLink
from .schemas import (
    BusinessProcessCreate, BusinessProcessUpdate,
    ProcessStepCreate, ProcessStepUpdate,
    ProcessLinkCreate, ProcessLinkUpdate,
    ProcessFlowMap, ProcessRealizationHealth
)

load_dotenv()

# Redis connection for event emission
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    decode_responses=True
)

def emit_event(event_type: str, data: Dict[str, Any]):
    """Emit event to Redis for event-driven architecture"""
    event = {
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data
    }
    redis_client.publish("business_process_events", json.dumps(event))

class BusinessProcessService:
    
    @staticmethod
    def create_business_process(
        db: Session, 
        business_process_data: BusinessProcessCreate,
        tenant_id: str,
        user_id: str
    ) -> BusinessProcess:
        """Create a new business process"""
        business_process = BusinessProcess(
            **business_process_data.dict(),
            tenant_id=tenant_id,
            user_id=user_id
        )
        db.add(business_process)
        db.commit()
        db.refresh(business_process)
        
        # Emit event
        emit_event("business_process_created", {
            "business_process_id": str(business_process.id),
            "tenant_id": tenant_id,
            "user_id": user_id,
            "process_type": business_process.process_type,
            "organizational_unit": business_process.organizational_unit
        })
        
        return business_process
    
    @staticmethod
    def get_business_process(
        db: Session, 
        business_process_id: str,
        tenant_id: str
    ) -> Optional[BusinessProcess]:
        """Get a business process by ID"""
        return db.query(BusinessProcess).filter(
            BusinessProcess.id == business_process_id,
            BusinessProcess.tenant_id == tenant_id
        ).first()
    
    @staticmethod
    def get_business_processes(
        db: Session,
        tenant_id: str,
        skip: int = 0,
        limit: int = 100,
        process_type: Optional[str] = None,
        organizational_unit: Optional[str] = None,
        status: Optional[str] = None,
        criticality: Optional[str] = None
    ) -> List[BusinessProcess]:
        """Get business processes with filtering"""
        query = db.query(BusinessProcess).filter(
            BusinessProcess.tenant_id == tenant_id
        )
        
        if process_type:
            query = query.filter(BusinessProcess.process_type == process_type)
        if organizational_unit:
            query = query.filter(BusinessProcess.organizational_unit == organizational_unit)
        if status:
            query = query.filter(BusinessProcess.status == status)
        if criticality:
            query = query.filter(BusinessProcess.criticality == criticality)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_business_process(
        db: Session,
        business_process_id: str,
        business_process_data: BusinessProcessUpdate,
        tenant_id: str
    ) -> Optional[BusinessProcess]:
        """Update a business process"""
        business_process = BusinessProcessService.get_business_process(
            db, business_process_id, tenant_id
        )
        
        if not business_process:
            return None
        
        update_data = business_process_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(business_process, field, value)
        
        business_process.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(business_process)
        
        # Emit event
        emit_event("business_process_updated", {
            "business_process_id": str(business_process.id),
            "tenant_id": tenant_id,
            "updated_fields": list(update_data.keys())
        })
        
        return business_process
    
    @staticmethod
    def delete_business_process(
        db: Session,
        business_process_id: str,
        tenant_id: str
    ) -> bool:
        """Delete a business process"""
        business_process = BusinessProcessService.get_business_process(
            db, business_process_id, tenant_id
        )
        
        if not business_process:
            return False
        
        # Emit event before deletion
        emit_event("business_process_deleted", {
            "business_process_id": str(business_process.id),
            "tenant_id": tenant_id,
            "process_type": business_process.process_type,
            "organizational_unit": business_process.organizational_unit
        })
        
        db.delete(business_process)
        db.commit()
        return True
    
    @staticmethod
    def get_business_processes_by_role(
        db: Session,
        tenant_id: str,
        role_id: str
    ) -> List[Dict[str, Any]]:
        """Get business processes by role"""
        processes = db.query(BusinessProcess).filter(
            BusinessProcess.tenant_id == tenant_id,
            BusinessProcess.role_id == role_id
        ).all()
        
        return [
            {
                "business_process_id": str(p.id),
                "name": p.name,
                "process_type": p.process_type,
                "organizational_unit": p.organizational_unit,
                "criticality": p.criticality,
                "status": p.status,
                "performance_score": p.performance_score,
                "last_updated": p.updated_at
            }
            for p in processes
        ]
    
    @staticmethod
    def get_business_processes_by_function(
        db: Session,
        tenant_id: str,
        business_function_id: str
    ) -> List[Dict[str, Any]]:
        """Get business processes by business function"""
        processes = db.query(BusinessProcess).filter(
            BusinessProcess.tenant_id == tenant_id,
            BusinessProcess.business_function_id == business_function_id
        ).all()
        
        return [
            {
                "business_process_id": str(p.id),
                "name": p.name,
                "process_type": p.process_type,
                "organizational_unit": p.organizational_unit,
                "criticality": p.criticality,
                "status": p.status,
                "performance_score": p.performance_score,
                "last_updated": p.updated_at
            }
            for p in processes
        ]
    
    @staticmethod
    def get_business_processes_by_goal(
        db: Session,
        tenant_id: str,
        goal_id: str
    ) -> List[Dict[str, Any]]:
        """Get business processes by goal"""
        processes = db.query(BusinessProcess).filter(
            BusinessProcess.tenant_id == tenant_id,
            BusinessProcess.goal_id == goal_id
        ).all()
        
        return [
            {
                "business_process_id": str(p.id),
                "name": p.name,
                "process_type": p.process_type,
                "organizational_unit": p.organizational_unit,
                "criticality": p.criticality,
                "status": p.status,
                "performance_score": p.performance_score,
                "last_updated": p.updated_at
            }
            for p in processes
        ]
    
    @staticmethod
    def get_business_processes_by_status(
        db: Session,
        tenant_id: str,
        status: str
    ) -> List[Dict[str, Any]]:
        """Get business processes by status"""
        processes = db.query(BusinessProcess).filter(
            BusinessProcess.tenant_id == tenant_id,
            BusinessProcess.status == status
        ).all()
        
        return [
            {
                "business_process_id": str(p.id),
                "name": p.name,
                "process_type": p.process_type,
                "organizational_unit": p.organizational_unit,
                "criticality": p.criticality,
                "status": p.status,
                "performance_score": p.performance_score,
                "last_updated": p.updated_at
            }
            for p in processes
        ]
    
    @staticmethod
    def get_business_processes_by_criticality(
        db: Session,
        tenant_id: str,
        criticality: str
    ) -> List[Dict[str, Any]]:
        """Get business processes by criticality"""
        processes = db.query(BusinessProcess).filter(
            BusinessProcess.tenant_id == tenant_id,
            BusinessProcess.criticality == criticality
        ).all()
        
        return [
            {
                "business_process_id": str(p.id),
                "name": p.name,
                "process_type": p.process_type,
                "organizational_unit": p.organizational_unit,
                "criticality": p.criticality,
                "status": p.status,
                "performance_score": p.performance_score,
                "last_updated": p.updated_at
            }
            for p in processes
        ]
    
    @staticmethod
    def get_process_flow_map(
        db: Session,
        business_process_id: str,
        tenant_id: str
    ) -> Optional[ProcessFlowMap]:
        """Generate process flow map analysis"""
        business_process = BusinessProcessService.get_business_process(
            db, business_process_id, tenant_id
        )
        
        if not business_process:
            return None
        
        # Get process steps
        steps = db.query(ProcessStep).filter(
            ProcessStep.business_process_id == business_process_id
        ).order_by(ProcessStep.step_order).all()
        
        total_steps = len(steps)
        automated_steps = len([s for s in steps if s.automation_level in ["automated", "fully_automated"]])
        manual_steps = len([s for s in steps if s.automation_level == "manual"])
        decision_points = len([s for s in steps if s.step_type == "decision"])
        handoff_points = len([s for s in steps if s.step_type == "handoff"])
        bottleneck_steps = len([s for s in steps if s.bottleneck_indicator])
        
        # Calculate durations
        total_duration = sum(s.duration_actual or 0 for s in steps)
        average_step_duration = total_duration / total_steps if total_steps > 0 else 0
        
        # Calculate flow complexity score
        complexity_factors = [
            total_steps * 0.2,
            decision_points * 0.3,
            handoff_points * 0.25,
            bottleneck_steps * 0.25
        ]
        flow_complexity_score = min(sum(complexity_factors), 1.0)
        
        return ProcessFlowMap(
            business_process_id=business_process_id,
            total_steps=total_steps,
            automated_steps=automated_steps,
            manual_steps=manual_steps,
            decision_points=decision_points,
            handoff_points=handoff_points,
            bottleneck_steps=bottleneck_steps,
            average_step_duration=average_step_duration,
            total_process_duration=total_duration,
            flow_complexity_score=flow_complexity_score,
            last_analyzed=datetime.utcnow()
        )
    
    @staticmethod
    def get_process_realization_health(
        db: Session,
        business_process_id: str,
        tenant_id: str
    ) -> Optional[ProcessRealizationHealth]:
        """Generate process realization health analysis"""
        business_process = BusinessProcessService.get_business_process(
            db, business_process_id, tenant_id
        )
        
        if not business_process:
            return None
        
        # Get process steps for detailed analysis
        steps = db.query(ProcessStep).filter(
            ProcessStep.business_process_id == business_process_id
        ).all()
        
        # Calculate automation score
        automation_scores = [1.0 if s.automation_level in ["automated", "fully_automated"] else 0.5 if s.automation_level == "semi_automated" else 0.0 for s in steps]
        automation_score = sum(automation_scores) / len(automation_scores) if automation_scores else 0.0
        
        # Calculate compliance score based on audit status
        compliance_score = 1.0 if business_process.audit_status == "completed" else 0.5 if business_process.audit_status == "in_progress" else 0.0
        
        # Calculate overall health score
        scores = [
            business_process.performance_score or 0.0,
            business_process.effectiveness_score or 0.0,
            business_process.efficiency_score or 0.0,
            business_process.quality_score or 0.0,
            automation_score,
            compliance_score
        ]
        overall_health_score = sum(scores) / len(scores)
        
        return ProcessRealizationHealth(
            business_process_id=business_process_id,
            performance_score=business_process.performance_score or 0.0,
            effectiveness_score=business_process.effectiveness_score or 0.0,
            efficiency_score=business_process.efficiency_score or 0.0,
            quality_score=business_process.quality_score or 0.0,
            automation_score=automation_score,
            compliance_score=compliance_score,
            overall_health_score=overall_health_score,
            last_assessed=datetime.utcnow()
        )

class ProcessStepService:
    
    @staticmethod
    def create_process_step(
        db: Session,
        business_process_id: str,
        step_data: ProcessStepCreate,
        tenant_id: str
    ) -> Optional[ProcessStep]:
        """Create a new process step"""
        # Verify business process exists and belongs to tenant
        business_process = BusinessProcessService.get_business_process(
            db, business_process_id, tenant_id
        )
        
        if not business_process:
            return None
        
        step = ProcessStep(
            **step_data.dict(),
            business_process_id=business_process_id
        )
        db.add(step)
        db.commit()
        db.refresh(step)
        
        # Emit event
        emit_event("process_step_created", {
            "step_id": str(step.id),
            "business_process_id": business_process_id,
            "tenant_id": tenant_id,
            "step_type": step.step_type,
            "step_order": step.step_order
        })
        
        return step
    
    @staticmethod
    def get_process_steps(
        db: Session,
        business_process_id: str,
        tenant_id: str
    ) -> List[ProcessStep]:
        """Get all steps for a business process"""
        # Verify business process exists and belongs to tenant
        business_process = BusinessProcessService.get_business_process(
            db, business_process_id, tenant_id
        )
        
        if not business_process:
            return []
        
        return db.query(ProcessStep).filter(
            ProcessStep.business_process_id == business_process_id
        ).order_by(ProcessStep.step_order).all()
    
    @staticmethod
    def update_process_step(
        db: Session,
        step_id: str,
        step_data: ProcessStepUpdate,
        tenant_id: str
    ) -> Optional[ProcessStep]:
        """Update a process step"""
        step = db.query(ProcessStep).join(BusinessProcess).filter(
            ProcessStep.id == step_id,
            BusinessProcess.tenant_id == tenant_id
        ).first()
        
        if not step:
            return None
        
        update_data = step_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(step, field, value)
        
        step.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(step)
        
        # Emit event
        emit_event("process_step_updated", {
            "step_id": str(step.id),
            "business_process_id": str(step.business_process_id),
            "tenant_id": tenant_id,
            "updated_fields": list(update_data.keys())
        })
        
        return step
    
    @staticmethod
    def delete_process_step(
        db: Session,
        step_id: str,
        tenant_id: str
    ) -> bool:
        """Delete a process step"""
        step = db.query(ProcessStep).join(BusinessProcess).filter(
            ProcessStep.id == step_id,
            BusinessProcess.tenant_id == tenant_id
        ).first()
        
        if not step:
            return False
        
        # Emit event before deletion
        emit_event("process_step_deleted", {
            "step_id": str(step.id),
            "business_process_id": str(step.business_process_id),
            "tenant_id": tenant_id,
            "step_type": step.step_type
        })
        
        db.delete(step)
        db.commit()
        return True

class ProcessLinkService:
    
    @staticmethod
    def create_process_link(
        db: Session,
        business_process_id: str,
        link_data: ProcessLinkCreate,
        tenant_id: str,
        user_id: str
    ) -> Optional[ProcessLink]:
        """Create a new process link"""
        # Verify business process exists and belongs to tenant
        business_process = BusinessProcessService.get_business_process(
            db, business_process_id, tenant_id
        )
        
        if not business_process:
            return None
        
        link = ProcessLink(
            **link_data.dict(),
            business_process_id=business_process_id,
            created_by=user_id
        )
        db.add(link)
        db.commit()
        db.refresh(link)
        
        # Emit event
        emit_event("process_link_created", {
            "link_id": str(link.id),
            "business_process_id": business_process_id,
            "tenant_id": tenant_id,
            "linked_element_type": link.linked_element_type,
            "link_type": link.link_type
        })
        
        return link
    
    @staticmethod
    def get_process_links(
        db: Session,
        business_process_id: str,
        tenant_id: str
    ) -> List[ProcessLink]:
        """Get all links for a business process"""
        # Verify business process exists and belongs to tenant
        business_process = BusinessProcessService.get_business_process(
            db, business_process_id, tenant_id
        )
        
        if not business_process:
            return []
        
        return db.query(ProcessLink).filter(
            ProcessLink.business_process_id == business_process_id
        ).order_by(ProcessLink.sequence_order).all()
    
    @staticmethod
    def update_process_link(
        db: Session,
        link_id: str,
        link_data: ProcessLinkUpdate,
        tenant_id: str
    ) -> Optional[ProcessLink]:
        """Update a process link"""
        link = db.query(ProcessLink).join(BusinessProcess).filter(
            ProcessLink.id == link_id,
            BusinessProcess.tenant_id == tenant_id
        ).first()
        
        if not link:
            return None
        
        update_data = link_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(link, field, value)
        
        db.commit()
        db.refresh(link)
        
        # Emit event
        emit_event("process_link_updated", {
            "link_id": str(link.id),
            "business_process_id": str(link.business_process_id),
            "tenant_id": tenant_id,
            "updated_fields": list(update_data.keys())
        })
        
        return link
    
    @staticmethod
    def delete_process_link(
        db: Session,
        link_id: str,
        tenant_id: str
    ) -> bool:
        """Delete a process link"""
        link = db.query(ProcessLink).join(BusinessProcess).filter(
            ProcessLink.id == link_id,
            BusinessProcess.tenant_id == tenant_id
        ).first()
        
        if not link:
            return False
        
        # Emit event before deletion
        emit_event("process_link_deleted", {
            "link_id": str(link.id),
            "business_process_id": str(link.business_process_id),
            "tenant_id": tenant_id,
            "linked_element_type": link.linked_element_type
        })
        
        db.delete(link)
        db.commit()
        return True 