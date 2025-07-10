from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any
import uuid
import json
import redis
from datetime import datetime, timedelta
import logging
from .models import Assessment, AssessmentLink, AssessmentType, AssessmentStatus, AssessmentMethod, ConfidenceLevel, LinkType
from .schemas import AssessmentCreate, AssessmentUpdate, AssessmentLinkCreate, AssessmentLinkUpdate
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

class AssessmentService:
    """Service class for Assessment operations"""
    
    @staticmethod
    def create_assessment(db: Session, assessment_data: AssessmentCreate, tenant_id: uuid.UUID, user_id: uuid.UUID) -> Assessment:
        """Create a new assessment"""
        try:
            assessment = Assessment(
                **assessment_data.dict(),
                tenant_id=tenant_id,
                user_id=user_id
            )
            db.add(assessment)
            db.commit()
            db.refresh(assessment)
            
            # Emit Redis event
            AssessmentService._emit_assessment_event("created", assessment)
            
            logger.info(f"Created assessment: {assessment.id}")
            return assessment
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating assessment: {str(e)}")
            raise
    
    @staticmethod
    def get_assessment(db: Session, assessment_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[Assessment]:
        """Get an assessment by ID"""
        return db.query(Assessment).filter(
            and_(
                Assessment.id == assessment_id,
                Assessment.tenant_id == tenant_id
            )
        ).first()
    
    @staticmethod
    def list_assessments(
        db: Session, 
        tenant_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        assessment_type: Optional[AssessmentType] = None,
        status: Optional[AssessmentStatus] = None,
        evaluator_user_id: Optional[uuid.UUID] = None,
        evaluated_goal_id: Optional[uuid.UUID] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        confidence_threshold: Optional[float] = None
    ) -> List[Assessment]:
        """List assessments with filtering"""
        query = db.query(Assessment).filter(Assessment.tenant_id == tenant_id)
        
        if assessment_type:
            query = query.filter(Assessment.assessment_type == assessment_type)
        if status:
            query = query.filter(Assessment.status == status)
        if evaluator_user_id:
            query = query.filter(Assessment.evaluator_user_id == evaluator_user_id)
        if evaluated_goal_id:
            query = query.filter(Assessment.evaluated_goal_id == evaluated_goal_id)
        if date_from:
            query = query.filter(Assessment.date_conducted >= date_from)
        if date_to:
            query = query.filter(Assessment.date_conducted <= date_to)
        if confidence_threshold is not None:
            query = query.filter(Assessment.confidence_score >= confidence_threshold)
        
        return query.order_by(desc(Assessment.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_assessment(
        db: Session, 
        assessment_id: uuid.UUID, 
        assessment_data: AssessmentUpdate, 
        tenant_id: uuid.UUID
    ) -> Optional[Assessment]:
        """Update an assessment"""
        try:
            assessment = AssessmentService.get_assessment(db, assessment_id, tenant_id)
            if not assessment:
                return None
            
            update_data = assessment_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(assessment, field, value)
            
            assessment.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(assessment)
            
            # Emit Redis event
            AssessmentService._emit_assessment_event("updated", assessment)
            
            logger.info(f"Updated assessment: {assessment.id}")
            return assessment
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating assessment: {str(e)}")
            raise
    
    @staticmethod
    def delete_assessment(db: Session, assessment_id: uuid.UUID, tenant_id: uuid.UUID) -> bool:
        """Delete an assessment"""
        try:
            assessment = AssessmentService.get_assessment(db, assessment_id, tenant_id)
            if not assessment:
                return False
            
            # Emit Redis event before deletion
            AssessmentService._emit_assessment_event("deleted", assessment)
            
            db.delete(assessment)
            db.commit()
            
            logger.info(f"Deleted assessment: {assessment_id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting assessment: {str(e)}")
            raise
    
    @staticmethod
    def get_evaluation_metrics(db: Session, assessment_id: uuid.UUID, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Get evaluation metrics analysis for an assessment"""
        assessment = AssessmentService.get_assessment(db, assessment_id, tenant_id)
        if not assessment:
            return {}
        
        # Calculate overall score
        overall_score = AssessmentService._calculate_overall_score(assessment)
        
        # Calculate metrics breakdown
        metrics_breakdown = AssessmentService._analyze_metrics_breakdown(assessment)
        
        # Calculate performance analysis
        performance_analysis = AssessmentService._analyze_performance(assessment)
        
        # Calculate quality analysis
        quality_analysis = AssessmentService._analyze_quality(assessment)
        
        # Calculate confidence analysis
        confidence_analysis = AssessmentService._analyze_confidence(assessment)
        
        # Generate recommendations
        recommendations = AssessmentService._generate_recommendations(assessment, overall_score, quality_analysis, confidence_analysis)
        
        return {
            "assessment_id": assessment_id,
            "overall_score": overall_score,
            "metrics_breakdown": metrics_breakdown,
            "performance_analysis": performance_analysis,
            "quality_analysis": quality_analysis,
            "confidence_analysis": confidence_analysis,
            "recommendations": recommendations
        }
    
    @staticmethod
    def get_confidence_score(db: Session, assessment_id: uuid.UUID, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Get confidence score analysis for an assessment"""
        assessment = AssessmentService.get_assessment(db, assessment_id, tenant_id)
        if not assessment:
            return {}
        
        # Calculate confidence score
        confidence_score = assessment.confidence_score
        confidence_level = assessment.confidence_level
        
        # Calculate evidence quality
        evidence_quality = AssessmentService._calculate_evidence_quality(assessment)
        
        # Get validation status
        validation_status = assessment.validation_status
        
        # Identify contributing factors
        contributing_factors = AssessmentService._identify_contributing_factors(assessment)
        
        # Generate recommendations
        recommendations = AssessmentService._generate_confidence_recommendations(assessment, confidence_score, evidence_quality)
        
        return {
            "assessment_id": assessment_id,
            "confidence_score": confidence_score,
            "confidence_level": confidence_level,
            "evidence_quality": evidence_quality,
            "validation_status": validation_status,
            "contributing_factors": contributing_factors,
            "recommendations": recommendations
        }
    
    # Helper methods for analysis
    @staticmethod
    def _calculate_overall_score(assessment: Assessment) -> float:
        """Calculate overall assessment score"""
        if not assessment.metrics_scored:
            return assessment.confidence_score
        
        try:
            metrics = json.loads(assessment.metrics_scored)
            if not metrics:
                return assessment.confidence_score
            
            # Calculate weighted average of metrics
            total_weight = 0
            weighted_sum = 0
            
            for metric_name, metric_data in metrics.items():
                if isinstance(metric_data, dict) and 'score' in metric_data and 'weight' in metric_data:
                    score = float(metric_data['score'])
                    weight = float(metric_data['weight'])
                    weighted_sum += score * weight
                    total_weight += weight
            
            if total_weight > 0:
                return weighted_sum / total_weight
            else:
                return assessment.confidence_score
        except (json.JSONDecodeError, ValueError):
            return assessment.confidence_score
    
    @staticmethod
    def _analyze_metrics_breakdown(assessment: Assessment) -> Dict[str, Any]:
        """Analyze metrics breakdown"""
        if not assessment.metrics_scored:
            return {"error": "No metrics available"}
        
        try:
            metrics = json.loads(assessment.metrics_scored)
            breakdown = {
                "total_metrics": len(metrics),
                "metrics_by_category": {},
                "score_distribution": {"excellent": 0, "good": 0, "fair": 0, "poor": 0},
                "top_performers": [],
                "areas_for_improvement": []
            }
            
            for metric_name, metric_data in metrics.items():
                if isinstance(metric_data, dict) and 'score' in metric_data:
                    score = float(metric_data['score'])
                    category = metric_data.get('category', 'general')
                    
                    # Categorize by score
                    if score >= 0.8:
                        breakdown["score_distribution"]["excellent"] += 1
                    elif score >= 0.6:
                        breakdown["score_distribution"]["good"] += 1
                    elif score >= 0.4:
                        breakdown["score_distribution"]["fair"] += 1
                    else:
                        breakdown["score_distribution"]["poor"] += 1
                    
                    # Group by category
                    if category not in breakdown["metrics_by_category"]:
                        breakdown["metrics_by_category"][category] = []
                    breakdown["metrics_by_category"][category].append({
                        "name": metric_name,
                        "score": score,
                        "weight": metric_data.get('weight', 1.0)
                    })
                    
                    # Identify top performers and areas for improvement
                    if score >= 0.8:
                        breakdown["top_performers"].append(metric_name)
                    elif score < 0.4:
                        breakdown["areas_for_improvement"].append(metric_name)
            
            return breakdown
        except (json.JSONDecodeError, ValueError):
            return {"error": "Invalid metrics format"}
    
    @staticmethod
    def _analyze_performance(assessment: Assessment) -> Dict[str, Any]:
        """Analyze assessment performance"""
        performance = {
            "completion_rate": assessment.progress_percent,
            "timeline_performance": AssessmentService._analyze_timeline_performance(assessment),
            "method_effectiveness": AssessmentService._analyze_method_effectiveness(assessment),
            "evaluator_performance": AssessmentService._analyze_evaluator_performance(assessment)
        }
        
        return performance
    
    @staticmethod
    def _analyze_timeline_performance(assessment: Assessment) -> Dict[str, Any]:
        """Analyze timeline performance"""
        timeline = {
            "planned_duration": None,
            "actual_duration": None,
            "on_schedule": True,
            "efficiency_score": 1.0
        }
        
        if assessment.planned_start_date and assessment.planned_end_date:
            planned_duration = (assessment.planned_end_date - assessment.planned_start_date).days
            timeline["planned_duration"] = planned_duration
        
        if assessment.actual_start_date and assessment.actual_end_date:
            actual_duration = (assessment.actual_end_date - assessment.actual_start_date).days
            timeline["actual_duration"] = actual_duration
            
            if assessment.planned_start_date and assessment.planned_end_date:
                planned_duration = (assessment.planned_end_date - assessment.planned_start_date).days
                if actual_duration > planned_duration:
                    timeline["on_schedule"] = False
                    timeline["efficiency_score"] = planned_duration / actual_duration if actual_duration > 0 else 0
        
        return timeline
    
    @staticmethod
    def _analyze_method_effectiveness(assessment: Assessment) -> Dict[str, Any]:
        """Analyze assessment method effectiveness"""
        method_effectiveness = {
            "method": assessment.assessment_method,
            "effectiveness_score": 0.8,  # Placeholder - would be calculated based on historical data
            "strengths": [],
            "weaknesses": []
        }
        
        # Method-specific analysis
        if assessment.assessment_method == AssessmentMethod.QUANTITATIVE:
            method_effectiveness["strengths"] = ["Objective measurement", "Statistical validity"]
            method_effectiveness["weaknesses"] = ["May miss qualitative aspects"]
        elif assessment.assessment_method == AssessmentMethod.QUALITATIVE:
            method_effectiveness["strengths"] = ["Rich insights", "Contextual understanding"]
            method_effectiveness["weaknesses"] = ["Subjective interpretation", "Limited generalizability"]
        elif assessment.assessment_method == AssessmentMethod.MIXED:
            method_effectiveness["strengths"] = ["Comprehensive approach", "Balanced perspective"]
            method_effectiveness["weaknesses"] = ["Complex implementation", "Resource intensive"]
        
        return method_effectiveness
    
    @staticmethod
    def _analyze_evaluator_performance(assessment: Assessment) -> Dict[str, Any]:
        """Analyze evaluator performance"""
        return {
            "evaluator_id": assessment.evaluator_user_id,
            "assessment_count": 1,  # Would be calculated from historical data
            "average_quality_score": assessment.quality_score,
            "confidence_trend": "stable"  # Would be calculated from historical data
        }
    
    @staticmethod
    def _analyze_quality(assessment: Assessment) -> Dict[str, Any]:
        """Analyze assessment quality"""
        quality = {
            "quality_score": assessment.quality_score,
            "validation_status": assessment.validation_status,
            "evidence_quality": AssessmentService._calculate_evidence_quality(assessment),
            "framework_compliance": AssessmentService._analyze_framework_compliance(assessment),
            "quality_factors": AssessmentService._identify_quality_factors(assessment)
        }
        
        return quality
    
    @staticmethod
    def _calculate_evidence_quality(assessment: Assessment) -> float:
        """Calculate evidence quality score"""
        if not assessment.assessment_links:
            return assessment.quality_score
        
        evidence_scores = []
        for link in assessment.assessment_links:
            evidence_scores.append(link.evidence_quality)
        
        if evidence_scores:
            return sum(evidence_scores) / len(evidence_scores)
        else:
            return assessment.quality_score
    
    @staticmethod
    def _analyze_framework_compliance(assessment: Assessment) -> Dict[str, Any]:
        """Analyze framework compliance"""
        compliance = {
            "framework": assessment.assessment_framework,
            "compliance_score": 0.8,  # Placeholder
            "compliance_standards": [],
            "gaps": []
        }
        
        if assessment.compliance_standards:
            try:
                standards = json.loads(assessment.compliance_standards)
                compliance["compliance_standards"] = standards
            except json.JSONDecodeError:
                pass
        
        return compliance
    
    @staticmethod
    def _identify_quality_factors(assessment: Assessment) -> List[str]:
        """Identify quality factors"""
        factors = []
        
        if assessment.quality_score >= 0.8:
            factors.append("High quality evidence")
        elif assessment.quality_score < 0.5:
            factors.append("Limited evidence quality")
        
        if assessment.confidence_score >= 0.8:
            factors.append("High confidence in results")
        elif assessment.confidence_score < 0.5:
            factors.append("Low confidence in results")
        
        if assessment.validation_status == "validated":
            factors.append("Validated assessment")
        elif assessment.validation_status == "pending":
            factors.append("Pending validation")
        
        return factors
    
    @staticmethod
    def _analyze_confidence(assessment: Assessment) -> Dict[str, Any]:
        """Analyze confidence analysis"""
        confidence = {
            "confidence_score": assessment.confidence_score,
            "confidence_level": assessment.confidence_level,
            "confidence_factors": AssessmentService._identify_confidence_factors(assessment),
            "uncertainty_areas": AssessmentService._identify_uncertainty_areas(assessment),
            "confidence_trend": "stable"  # Would be calculated from historical data
        }
        
        return confidence
    
    @staticmethod
    def _identify_confidence_factors(assessment: Assessment) -> List[str]:
        """Identify confidence factors"""
        factors = []
        
        if assessment.confidence_score >= 0.8:
            factors.append("Strong evidence base")
            factors.append("Clear assessment criteria")
        elif assessment.confidence_score < 0.5:
            factors.append("Limited evidence")
            factors.append("Ambiguous criteria")
        
        if assessment.assessment_method == AssessmentMethod.QUANTITATIVE:
            factors.append("Quantitative measurement")
        elif assessment.assessment_method == AssessmentMethod.QUALITATIVE:
            factors.append("Qualitative insights")
        
        return factors
    
    @staticmethod
    def _identify_uncertainty_areas(assessment: Assessment) -> List[str]:
        """Identify uncertainty areas"""
        areas = []
        
        if assessment.confidence_score < 0.7:
            areas.append("Limited sample size")
            areas.append("Subjective interpretation")
        
        if not assessment.metrics_scored:
            areas.append("No quantitative metrics")
        
        if assessment.validation_status != "validated":
            areas.append("Unvalidated assessment")
        
        return areas
    
    @staticmethod
    def _identify_contributing_factors(assessment: Assessment) -> List[Dict[str, Any]]:
        """Identify contributing factors to confidence score"""
        factors = []
        
        # Evidence quality factor
        evidence_quality = AssessmentService._calculate_evidence_quality(assessment)
        factors.append({
            "factor": "Evidence Quality",
            "score": evidence_quality,
            "weight": 0.3,
            "description": "Quality of evidence provided"
        })
        
        # Assessment method factor
        method_score = 0.8 if assessment.assessment_method in [AssessmentMethod.QUANTITATIVE, AssessmentMethod.MIXED] else 0.6
        factors.append({
            "factor": "Assessment Method",
            "score": method_score,
            "weight": 0.2,
            "description": "Effectiveness of assessment method"
        })
        
        # Validation status factor
        validation_score = 1.0 if assessment.validation_status == "validated" else 0.5
        factors.append({
            "factor": "Validation Status",
            "score": validation_score,
            "weight": 0.2,
            "description": "Assessment validation status"
        })
        
        # Evaluator experience factor (placeholder)
        factors.append({
            "factor": "Evaluator Experience",
            "score": 0.8,
            "weight": 0.3,
            "description": "Evaluator expertise and experience"
        })
        
        return factors
    
    @staticmethod
    def _generate_recommendations(assessment: Assessment, overall_score: float, quality_analysis: Dict, confidence_analysis: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if overall_score < 0.6:
            recommendations.append("Consider revising assessment criteria for better alignment")
        
        if quality_analysis.get("quality_score", 0) < 0.7:
            recommendations.append("Improve evidence collection and validation processes")
        
        if confidence_analysis.get("confidence_score", 0) < 0.7:
            recommendations.append("Enhance assessment methodology for higher confidence")
        
        if assessment.status == AssessmentStatus.IN_PROGRESS and assessment.progress_percent < 50:
            recommendations.append("Accelerate assessment progress to meet timelines")
        
        if not assessment.metrics_scored:
            recommendations.append("Implement quantitative metrics for objective measurement")
        
        return recommendations
    
    @staticmethod
    def _generate_confidence_recommendations(assessment: Assessment, confidence_score: float, evidence_quality: float) -> List[str]:
        """Generate confidence-specific recommendations"""
        recommendations = []
        
        if confidence_score < 0.7:
            recommendations.append("Increase sample size for more reliable results")
            recommendations.append("Use multiple assessment methods for triangulation")
        
        if evidence_quality < 0.7:
            recommendations.append("Improve evidence collection procedures")
            recommendations.append("Implement evidence validation processes")
        
        if assessment.validation_status != "validated":
            recommendations.append("Complete assessment validation process")
        
        if assessment.assessment_method == AssessmentMethod.QUALITATIVE:
            recommendations.append("Consider adding quantitative metrics for balance")
        
        return recommendations
    
    @staticmethod
    def _emit_assessment_event(event_type: str, assessment: Assessment):
        """Emit Redis event for assessment changes"""
        try:
            event_data = {
                "event_type": f"assessment_{event_type}",
                "assessment_id": str(assessment.id),
                "tenant_id": str(assessment.tenant_id),
                "assessment_type": assessment.assessment_type,
                "status": assessment.status,
                "timestamp": datetime.utcnow().isoformat()
            }
            redis_client.publish("assessment_events", json.dumps(event_data))
            logger.info(f"Emitted assessment event: {event_type}")
        except Exception as e:
            logger.error(f"Error emitting assessment event: {str(e)}")

class AssessmentLinkService:
    """Service class for Assessment Link operations"""
    
    @staticmethod
    def create_assessment_link(
        db: Session, 
        assessment_id: uuid.UUID, 
        link_data: AssessmentLinkCreate, 
        tenant_id: uuid.UUID, 
        user_id: uuid.UUID
    ) -> AssessmentLink:
        """Create a new assessment link"""
        try:
            # Verify assessment exists and belongs to tenant
            assessment = AssessmentService.get_assessment(db, assessment_id, tenant_id)
            if not assessment:
                raise ValueError("Assessment not found")
            
            assessment_link = AssessmentLink(
                **link_data.dict(),
                assessment_id=assessment_id,
                created_by=user_id
            )
            db.add(assessment_link)
            db.commit()
            db.refresh(assessment_link)
            
            # Emit Redis event
            AssessmentLinkService._emit_assessment_link_event("created", assessment_link)
            
            logger.info(f"Created assessment link: {assessment_link.id}")
            return assessment_link
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating assessment link: {str(e)}")
            raise
    
    @staticmethod
    def get_assessment_link(db: Session, link_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[AssessmentLink]:
        """Get an assessment link by ID"""
        return db.query(AssessmentLink).join(Assessment).filter(
            and_(
                AssessmentLink.id == link_id,
                Assessment.tenant_id == tenant_id
            )
        ).first()
    
    @staticmethod
    def list_assessment_links(db: Session, assessment_id: uuid.UUID, tenant_id: uuid.UUID) -> List[AssessmentLink]:
        """List assessment links for an assessment"""
        return db.query(AssessmentLink).join(Assessment).filter(
            and_(
                AssessmentLink.assessment_id == assessment_id,
                Assessment.tenant_id == tenant_id
            )
        ).all()
    
    @staticmethod
    def update_assessment_link(
        db: Session, 
        link_id: uuid.UUID, 
        link_data: AssessmentLinkUpdate, 
        tenant_id: uuid.UUID
    ) -> Optional[AssessmentLink]:
        """Update an assessment link"""
        try:
            assessment_link = AssessmentLinkService.get_assessment_link(db, link_id, tenant_id)
            if not assessment_link:
                return None
            
            update_data = link_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(assessment_link, field, value)
            
            assessment_link.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(assessment_link)
            
            # Emit Redis event
            AssessmentLinkService._emit_assessment_link_event("updated", assessment_link)
            
            logger.info(f"Updated assessment link: {assessment_link.id}")
            return assessment_link
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating assessment link: {str(e)}")
            raise
    
    @staticmethod
    def delete_assessment_link(db: Session, link_id: uuid.UUID, tenant_id: uuid.UUID) -> bool:
        """Delete an assessment link"""
        try:
            assessment_link = AssessmentLinkService.get_assessment_link(db, link_id, tenant_id)
            if not assessment_link:
                return False
            
            # Emit Redis event before deletion
            AssessmentLinkService._emit_assessment_link_event("deleted", assessment_link)
            
            db.delete(assessment_link)
            db.commit()
            
            logger.info(f"Deleted assessment link: {link_id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting assessment link: {str(e)}")
            raise
    
    @staticmethod
    def _emit_assessment_link_event(event_type: str, assessment_link: AssessmentLink):
        """Emit Redis event for assessment link changes"""
        try:
            event_data = {
                "event_type": f"assessment_link_{event_type}",
                "link_id": str(assessment_link.id),
                "assessment_id": str(assessment_link.assessment_id),
                "linked_element_type": assessment_link.linked_element_type,
                "link_type": assessment_link.link_type,
                "timestamp": datetime.utcnow().isoformat()
            }
            redis_client.publish("assessment_link_events", json.dumps(event_data))
            logger.info(f"Emitted assessment link event: {event_type}")
        except Exception as e:
            logger.error(f"Error emitting assessment link event: {str(e)}") 