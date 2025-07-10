from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any
import uuid
import json
import redis
from datetime import datetime, timedelta
import logging
from .models import WorkPackage, PackageLink, PackageType, PackageStatus, DeliveryRisk, LinkType
from .schemas import WorkPackageCreate, WorkPackageUpdate, PackageLinkCreate, PackageLinkUpdate
from .database import get_db

# Configure logging
logger = logging.getLogger(__name__)

# Redis configuration
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

class WorkPackageService:
    """Service class for Work Package operations"""
    
    @staticmethod
    def create_work_package(db: Session, work_package_data: WorkPackageCreate, tenant_id: uuid.UUID, user_id: uuid.UUID) -> WorkPackage:
        """Create a new work package"""
        try:
            work_package = WorkPackage(
                **work_package_data.dict(),
                tenant_id=tenant_id,
                user_id=user_id
            )
            db.add(work_package)
            db.commit()
            db.refresh(work_package)
            
            # Emit Redis event
            WorkPackageService._emit_work_package_event("created", work_package)
            
            logger.info(f"Created work package: {work_package.id}")
            return work_package
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating work package: {str(e)}")
            raise
    
    @staticmethod
    def get_work_package(db: Session, work_package_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[WorkPackage]:
        """Get a work package by ID"""
        return db.query(WorkPackage).filter(
            and_(
                WorkPackage.id == work_package_id,
                WorkPackage.tenant_id == tenant_id
            )
        ).first()
    
    @staticmethod
    def list_work_packages(
        db: Session, 
        tenant_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        package_type: Optional[PackageType] = None,
        status: Optional[PackageStatus] = None,
        delivery_risk: Optional[DeliveryRisk] = None,
        change_owner_id: Optional[uuid.UUID] = None,
        related_goal_id: Optional[uuid.UUID] = None,
        target_plateau_id: Optional[uuid.UUID] = None,
        progress_threshold: Optional[float] = None
    ) -> List[WorkPackage]:
        """List work packages with filtering"""
        query = db.query(WorkPackage).filter(WorkPackage.tenant_id == tenant_id)
        
        if package_type:
            query = query.filter(WorkPackage.package_type == package_type)
        if status:
            query = query.filter(WorkPackage.current_status == status)
        if delivery_risk:
            query = query.filter(WorkPackage.delivery_risk == delivery_risk)
        if change_owner_id:
            query = query.filter(WorkPackage.change_owner_id == change_owner_id)
        if related_goal_id:
            query = query.filter(WorkPackage.related_goal_id == related_goal_id)
        if target_plateau_id:
            query = query.filter(WorkPackage.target_plateau_id == target_plateau_id)
        if progress_threshold is not None:
            query = query.filter(WorkPackage.progress_percent >= progress_threshold)
        
        return query.order_by(desc(WorkPackage.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_work_package(
        db: Session, 
        work_package_id: uuid.UUID, 
        work_package_data: WorkPackageUpdate, 
        tenant_id: uuid.UUID
    ) -> Optional[WorkPackage]:
        """Update a work package"""
        try:
            work_package = WorkPackageService.get_work_package(db, work_package_id, tenant_id)
            if not work_package:
                return None
            
            update_data = work_package_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(work_package, field, value)
            
            work_package.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(work_package)
            
            # Emit Redis event
            WorkPackageService._emit_work_package_event("updated", work_package)
            
            logger.info(f"Updated work package: {work_package.id}")
            return work_package
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating work package: {str(e)}")
            raise
    
    @staticmethod
    def delete_work_package(db: Session, work_package_id: uuid.UUID, tenant_id: uuid.UUID) -> bool:
        """Delete a work package"""
        try:
            work_package = WorkPackageService.get_work_package(db, work_package_id, tenant_id)
            if not work_package:
                return False
            
            # Emit Redis event before deletion
            WorkPackageService._emit_work_package_event("deleted", work_package)
            
            db.delete(work_package)
            db.commit()
            
            logger.info(f"Deleted work package: {work_package_id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting work package: {str(e)}")
            raise
    
    @staticmethod
    def get_execution_status(db: Session, work_package_id: uuid.UUID, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Get execution status analysis for a work package"""
        work_package = WorkPackageService.get_work_package(db, work_package_id, tenant_id)
        if not work_package:
            return {}
        
        # Calculate progress analysis
        progress_analysis = {
            "current_progress": work_package.progress_percent,
            "is_on_track": work_package.progress_percent >= 50 if work_package.scheduled_end and work_package.scheduled_start else True,
            "estimated_completion": WorkPackageService._estimate_completion_date(work_package),
            "velocity": WorkPackageService._calculate_velocity(work_package)
        }
        
        # Calculate timeline analysis
        timeline_analysis = {
            "scheduled_duration": WorkPackageService._calculate_duration(work_package.scheduled_start, work_package.scheduled_end),
            "actual_duration": WorkPackageService._calculate_duration(work_package.actual_start, work_package.actual_end),
            "is_delayed": WorkPackageService._is_delayed(work_package),
            "days_remaining": WorkPackageService._calculate_days_remaining(work_package)
        }
        
        # Calculate risk assessment
        risk_assessment = {
            "delivery_risk": work_package.delivery_risk,
            "risk_factors": WorkPackageService._identify_risk_factors(work_package),
            "mitigation_status": WorkPackageService._assess_mitigation_status(work_package)
        }
        
        # Calculate quality gates status
        quality_gates_status = {
            "total_gates": 0,
            "passed_gates": 0,
            "failed_gates": 0,
            "pending_gates": 0
        }
        if work_package.quality_gates:
            try:
                gates = json.loads(work_package.quality_gates)
                quality_gates_status = WorkPackageService._analyze_quality_gates(gates)
            except json.JSONDecodeError:
                pass
        
        # Calculate resource utilization
        resource_utilization = {
            "effort_utilization": WorkPackageService._calculate_effort_utilization(work_package),
            "budget_utilization": WorkPackageService._calculate_budget_utilization(work_package),
            "team_utilization": WorkPackageService._calculate_team_utilization(work_package)
        }
        
        # Generate recommendations
        recommendations = WorkPackageService._generate_recommendations(work_package, progress_analysis, timeline_analysis, risk_assessment)
        
        return {
            "work_package_id": work_package_id,
            "overall_status": WorkPackageService._determine_overall_status(work_package, progress_analysis, timeline_analysis, risk_assessment),
            "progress_analysis": progress_analysis,
            "timeline_analysis": timeline_analysis,
            "risk_assessment": risk_assessment,
            "quality_gates_status": quality_gates_status,
            "resource_utilization": resource_utilization,
            "recommendations": recommendations
        }
    
    @staticmethod
    def get_gap_closure_map(db: Session, work_package_id: uuid.UUID, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Get gap closure mapping for a work package"""
        work_package = WorkPackageService.get_work_package(db, work_package_id, tenant_id)
        if not work_package:
            return {}
        
        # Get package links to gaps
        gap_links = db.query(PackageLink).filter(
            and_(
                PackageLink.work_package_id == work_package_id,
                PackageLink.linked_element_type == "gap"
            )
        ).all()
        
        gaps_addressed = []
        for link in gap_links:
            gaps_addressed.append({
                "gap_id": link.linked_element_id,
                "link_type": link.link_type,
                "relationship_strength": link.relationship_strength,
                "dependency_level": link.dependency_level,
                "impact_level": link.impact_level,
                "traceability_score": link.traceability_score,
                "is_validated": link.is_validated
            })
        
        # Calculate closure progress
        closure_progress = {
            "total_gaps": len(gaps_addressed),
            "addressed_gaps": len([g for g in gaps_addressed if g["link_type"] in ["closes", "realizes"]]),
            "partial_closure": len([g for g in gaps_addressed if g["link_type"] == "contributes_to"]),
            "closure_percentage": WorkPackageService._calculate_closure_percentage(gaps_addressed)
        }
        
        # Calculate impact assessment
        impact_assessment = {
            "high_impact_gaps": len([g for g in gaps_addressed if g["impact_level"] == "high"]),
            "critical_gaps": len([g for g in gaps_addressed if g["dependency_level"] == "high"]),
            "validated_gaps": len([g for g in gaps_addressed if g["is_validated"]]),
            "overall_impact_score": WorkPackageService._calculate_impact_score(gaps_addressed)
        }
        
        # Create traceability matrix
        traceability_matrix = {
            "high_traceability": len([g for g in gaps_addressed if g["traceability_score"] >= 0.8]),
            "medium_traceability": len([g for g in gaps_addressed if 0.5 <= g["traceability_score"] < 0.8]),
            "low_traceability": len([g for g in gaps_addressed if g["traceability_score"] < 0.5]),
            "average_traceability": sum(g["traceability_score"] for g in gaps_addressed) / len(gaps_addressed) if gaps_addressed else 0
        }
        
        # Calculate validation status
        validation_status = {
            "validated_count": len([g for g in gaps_addressed if g["is_validated"]]),
            "pending_validation": len([g for g in gaps_addressed if not g["is_validated"]]),
            "validation_rate": len([g for g in gaps_addressed if g["is_validated"]]) / len(gaps_addressed) if gaps_addressed else 0
        }
        
        return {
            "work_package_id": work_package_id,
            "gaps_addressed": gaps_addressed,
            "closure_progress": closure_progress,
            "impact_assessment": impact_assessment,
            "traceability_matrix": traceability_matrix,
            "validation_status": validation_status
        }
    
    # Helper methods for analysis
    @staticmethod
    def _estimate_completion_date(work_package: WorkPackage) -> Optional[datetime]:
        """Estimate completion date based on progress and timeline"""
        if not work_package.scheduled_start or not work_package.scheduled_end:
            return None
        
        if work_package.progress_percent >= 100:
            return work_package.actual_end or work_package.scheduled_end
        
        total_duration = (work_package.scheduled_end - work_package.scheduled_start).days
        if work_package.progress_percent > 0:
            estimated_remaining_days = (total_duration * (100 - work_package.progress_percent)) / work_package.progress_percent
            return datetime.utcnow() + timedelta(days=estimated_remaining_days)
        
        return work_package.scheduled_end
    
    @staticmethod
    def _calculate_velocity(work_package: WorkPackage) -> float:
        """Calculate work package velocity"""
        if not work_package.actual_start:
            return 0.0
        
        elapsed_days = (datetime.utcnow() - work_package.actual_start).days
        if elapsed_days <= 0:
            return 0.0
        
        return work_package.progress_percent / elapsed_days
    
    @staticmethod
    def _calculate_duration(start_date: Optional[datetime], end_date: Optional[datetime]) -> Optional[int]:
        """Calculate duration in days"""
        if not start_date or not end_date:
            return None
        return (end_date - start_date).days
    
    @staticmethod
    def _is_delayed(work_package: WorkPackage) -> bool:
        """Check if work package is delayed"""
        if not work_package.scheduled_end:
            return False
        return datetime.utcnow() > work_package.scheduled_end and work_package.progress_percent < 100
    
    @staticmethod
    def _calculate_days_remaining(work_package: WorkPackage) -> Optional[int]:
        """Calculate days remaining"""
        if not work_package.scheduled_end:
            return None
        remaining = (work_package.scheduled_end - datetime.utcnow()).days
        return max(0, remaining)
    
    @staticmethod
    def _identify_risk_factors(work_package: WorkPackage) -> List[str]:
        """Identify risk factors for the work package"""
        risk_factors = []
        
        if work_package.delivery_risk in [DeliveryRisk.HIGH, DeliveryRisk.CRITICAL]:
            risk_factors.append("High delivery risk")
        
        if work_package.progress_percent < 25 and work_package.scheduled_start and (datetime.utcnow() - work_package.scheduled_start).days > 30:
            risk_factors.append("Slow progress")
        
        if work_package.actual_effort_hours > work_package.estimated_effort_hours * 1.2 if work_package.estimated_effort_hours else False:
            risk_factors.append("Effort overrun")
        
        if work_package.actual_cost > work_package.budget_allocation * 1.1 if work_package.budget_allocation else False:
            risk_factors.append("Budget overrun")
        
        return risk_factors
    
    @staticmethod
    def _assess_mitigation_status(work_package: WorkPackage) -> str:
        """Assess risk mitigation status"""
        if not work_package.risk_mitigation_plan:
            return "no_plan"
        
        risk_factors = WorkPackageService._identify_risk_factors(work_package)
        if not risk_factors:
            return "no_risks"
        
        return "mitigation_needed"
    
    @staticmethod
    def _analyze_quality_gates(gates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze quality gates status"""
        total_gates = len(gates)
        passed_gates = len([g for g in gates if g.get("status") == "passed"])
        failed_gates = len([g for g in gates if g.get("status") == "failed"])
        pending_gates = total_gates - passed_gates - failed_gates
        
        return {
            "total_gates": total_gates,
            "passed_gates": passed_gates,
            "failed_gates": failed_gates,
            "pending_gates": pending_gates
        }
    
    @staticmethod
    def _calculate_effort_utilization(work_package: WorkPackage) -> float:
        """Calculate effort utilization percentage"""
        if not work_package.estimated_effort_hours:
            return 0.0
        return (work_package.actual_effort_hours / work_package.estimated_effort_hours) * 100
    
    @staticmethod
    def _calculate_budget_utilization(work_package: WorkPackage) -> float:
        """Calculate budget utilization percentage"""
        if not work_package.budget_allocation:
            return 0.0
        return (work_package.actual_cost / work_package.budget_allocation) * 100
    
    @staticmethod
    def _calculate_team_utilization(work_package: WorkPackage) -> float:
        """Calculate team utilization (placeholder)"""
        return 75.0  # Placeholder value
    
    @staticmethod
    def _generate_recommendations(work_package: WorkPackage, progress_analysis: Dict, timeline_analysis: Dict, risk_assessment: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if progress_analysis.get("velocity", 0) < 1.0:
            recommendations.append("Consider increasing team velocity or reducing scope")
        
        if timeline_analysis.get("is_delayed", False):
            recommendations.append("Implement recovery plan to meet deadlines")
        
        if risk_assessment.get("risk_factors"):
            recommendations.append("Review and update risk mitigation plan")
        
        if work_package.progress_percent < 50 and work_package.scheduled_start and (datetime.utcnow() - work_package.scheduled_start).days > 60:
            recommendations.append("Consider replanning or scope adjustment")
        
        return recommendations
    
    @staticmethod
    def _determine_overall_status(work_package: WorkPackage, progress_analysis: Dict, timeline_analysis: Dict, risk_assessment: Dict) -> str:
        """Determine overall execution status"""
        if work_package.current_status == PackageStatus.COMPLETED:
            return "completed"
        elif work_package.current_status == PackageStatus.CANCELLED:
            return "cancelled"
        elif timeline_analysis.get("is_delayed", False):
            return "delayed"
        elif progress_analysis.get("velocity", 0) < 0.5:
            return "at_risk"
        else:
            return "on_track"
    
    @staticmethod
    def _calculate_closure_percentage(gaps_addressed: List[Dict]) -> float:
        """Calculate gap closure percentage"""
        if not gaps_addressed:
            return 0.0
        
        closed_gaps = len([g for g in gaps_addressed if g["link_type"] in ["closes", "realizes"]])
        return (closed_gaps / len(gaps_addressed)) * 100
    
    @staticmethod
    def _calculate_impact_score(gaps_addressed: List[Dict]) -> float:
        """Calculate overall impact score"""
        if not gaps_addressed:
            return 0.0
        
        impact_scores = {
            "low": 1.0,
            "medium": 2.0,
            "high": 3.0,
            "critical": 4.0
        }
        
        total_score = sum(impact_scores.get(g["impact_level"], 1.0) for g in gaps_addressed)
        return total_score / len(gaps_addressed)
    
    @staticmethod
    def _emit_work_package_event(event_type: str, work_package: WorkPackage):
        """Emit Redis event for work package changes"""
        try:
            event_data = {
                "event_type": f"work_package_{event_type}",
                "work_package_id": str(work_package.id),
                "tenant_id": str(work_package.tenant_id),
                "package_type": work_package.package_type,
                "status": work_package.current_status,
                "timestamp": datetime.utcnow().isoformat()
            }
            redis_client.publish("work_package_events", json.dumps(event_data))
            logger.info(f"Emitted work package event: {event_type}")
        except Exception as e:
            logger.error(f"Error emitting work package event: {str(e)}")

class PackageLinkService:
    """Service class for Package Link operations"""
    
    @staticmethod
    def create_package_link(
        db: Session, 
        work_package_id: uuid.UUID, 
        link_data: PackageLinkCreate, 
        tenant_id: uuid.UUID, 
        user_id: uuid.UUID
    ) -> PackageLink:
        """Create a new package link"""
        try:
            # Verify work package exists and belongs to tenant
            work_package = WorkPackageService.get_work_package(db, work_package_id, tenant_id)
            if not work_package:
                raise ValueError("Work package not found")
            
            package_link = PackageLink(
                **link_data.dict(),
                work_package_id=work_package_id,
                created_by=user_id
            )
            db.add(package_link)
            db.commit()
            db.refresh(package_link)
            
            # Emit Redis event
            PackageLinkService._emit_package_link_event("created", package_link)
            
            logger.info(f"Created package link: {package_link.id}")
            return package_link
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating package link: {str(e)}")
            raise
    
    @staticmethod
    def get_package_link(db: Session, link_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[PackageLink]:
        """Get a package link by ID"""
        return db.query(PackageLink).join(WorkPackage).filter(
            and_(
                PackageLink.id == link_id,
                WorkPackage.tenant_id == tenant_id
            )
        ).first()
    
    @staticmethod
    def list_package_links(db: Session, work_package_id: uuid.UUID, tenant_id: uuid.UUID) -> List[PackageLink]:
        """List package links for a work package"""
        return db.query(PackageLink).join(WorkPackage).filter(
            and_(
                PackageLink.work_package_id == work_package_id,
                WorkPackage.tenant_id == tenant_id
            )
        ).all()
    
    @staticmethod
    def update_package_link(
        db: Session, 
        link_id: uuid.UUID, 
        link_data: PackageLinkUpdate, 
        tenant_id: uuid.UUID
    ) -> Optional[PackageLink]:
        """Update a package link"""
        try:
            package_link = PackageLinkService.get_package_link(db, link_id, tenant_id)
            if not package_link:
                return None
            
            update_data = link_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(package_link, field, value)
            
            package_link.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(package_link)
            
            # Emit Redis event
            PackageLinkService._emit_package_link_event("updated", package_link)
            
            logger.info(f"Updated package link: {package_link.id}")
            return package_link
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating package link: {str(e)}")
            raise
    
    @staticmethod
    def delete_package_link(db: Session, link_id: uuid.UUID, tenant_id: uuid.UUID) -> bool:
        """Delete a package link"""
        try:
            package_link = PackageLinkService.get_package_link(db, link_id, tenant_id)
            if not package_link:
                return False
            
            # Emit Redis event before deletion
            PackageLinkService._emit_package_link_event("deleted", package_link)
            
            db.delete(package_link)
            db.commit()
            
            logger.info(f"Deleted package link: {link_id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting package link: {str(e)}")
            raise
    
    @staticmethod
    def _emit_package_link_event(event_type: str, package_link: PackageLink):
        """Emit Redis event for package link changes"""
        try:
            event_data = {
                "event_type": f"package_link_{event_type}",
                "link_id": str(package_link.id),
                "work_package_id": str(package_link.work_package_id),
                "linked_element_type": package_link.linked_element_type,
                "link_type": package_link.link_type,
                "timestamp": datetime.utcnow().isoformat()
            }
            redis_client.publish("package_link_events", json.dumps(event_data))
            logger.info(f"Emitted package link event: {event_type}")
        except Exception as e:
            logger.error(f"Error emitting package link event: {str(e)}") 