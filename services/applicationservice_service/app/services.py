from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
from uuid import UUID
import json
import redis
from datetime import datetime, timedelta
import logging

from .models import ApplicationService, ServiceLink
from .schemas import (
    ApplicationServiceCreate, ApplicationServiceUpdate, ApplicationServiceResponse,
    ServiceLinkCreate, ServiceLinkUpdate, ServiceLinkResponse,
    ImpactMapResponse, PerformanceScoreResponse, ServiceAnalysisResponse
)

logger = logging.getLogger(__name__)

class ApplicationServiceService:
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis = redis_client

    def create_application_service(
        self, 
        service_data: ApplicationServiceCreate, 
        tenant_id: UUID, 
        user_id: UUID
    ) -> ApplicationServiceResponse:
        """Create a new application service."""
        try:
            # Create service instance
            db_service = ApplicationService(
                **service_data.dict(),
                tenant_id=tenant_id,
                user_id=user_id
            )
            
            self.db.add(db_service)
            self.db.commit()
            self.db.refresh(db_service)
            
            # Emit Redis event
            self._emit_service_event("created", db_service)
            
            return ApplicationServiceResponse.from_orm(db_service)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating application service: {e}")
            raise

    def get_application_service(
        self, 
        service_id: UUID, 
        tenant_id: UUID
    ) -> Optional[ApplicationServiceResponse]:
        """Get application service by ID."""
        try:
            service = self.db.query(ApplicationService).filter(
                and_(
                    ApplicationService.id == service_id,
                    ApplicationService.tenant_id == tenant_id
                )
            ).first()
            
            if not service:
                return None
                
            return ApplicationServiceResponse.from_orm(service)
            
        except Exception as e:
            logger.error(f"Error getting application service: {e}")
            raise

    def list_application_services(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
        service_type: Optional[str] = None,
        status: Optional[str] = None,
        business_criticality: Optional[str] = None,
        business_value: Optional[str] = None,
        capability_id: Optional[UUID] = None,
        technology_stack: Optional[str] = None,
        performance_threshold: Optional[float] = None
    ) -> List[ApplicationServiceResponse]:
        """List application services with filtering."""
        try:
            query = self.db.query(ApplicationService).filter(
                ApplicationService.tenant_id == tenant_id
            )
            
            # Apply filters
            if service_type:
                query = query.filter(ApplicationService.service_type == service_type)
            if status:
                query = query.filter(ApplicationService.status == status)
            if business_criticality:
                query = query.filter(ApplicationService.business_criticality == business_criticality)
            if business_value:
                query = query.filter(ApplicationService.business_value == business_value)
            if capability_id:
                query = query.filter(ApplicationService.capability_id == capability_id)
            if technology_stack:
                query = query.filter(ApplicationService.technology_stack.contains(technology_stack))
            if performance_threshold:
                query = query.filter(ApplicationService.current_availability_pct >= performance_threshold)
            
            # Apply pagination and ordering
            services = query.order_by(desc(ApplicationService.created_at)).offset(skip).limit(limit).all()
            
            return [ApplicationServiceResponse.from_orm(service) for service in services]
            
        except Exception as e:
            logger.error(f"Error listing application services: {e}")
            raise

    def update_application_service(
        self,
        service_id: UUID,
        service_data: ApplicationServiceUpdate,
        tenant_id: UUID
    ) -> Optional[ApplicationServiceResponse]:
        """Update application service."""
        try:
            service = self.db.query(ApplicationService).filter(
                and_(
                    ApplicationService.id == service_id,
                    ApplicationService.tenant_id == tenant_id
                )
            ).first()
            
            if not service:
                return None
            
            # Update fields
            update_data = service_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(service, field, value)
            
            service.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(service)
            
            # Emit Redis event
            self._emit_service_event("updated", service)
            
            return ApplicationServiceResponse.from_orm(service)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating application service: {e}")
            raise

    def delete_application_service(
        self, 
        service_id: UUID, 
        tenant_id: UUID
    ) -> bool:
        """Delete application service."""
        try:
            service = self.db.query(ApplicationService).filter(
                and_(
                    ApplicationService.id == service_id,
                    ApplicationService.tenant_id == tenant_id
                )
            ).first()
            
            if not service:
                return False
            
            # Emit Redis event before deletion
            self._emit_service_event("deleted", service)
            
            self.db.delete(service)
            self.db.commit()
            
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting application service: {e}")
            raise

    def get_impact_map(self, service_id: UUID, tenant_id: UUID) -> Optional[ImpactMapResponse]:
        """Get impact mapping for application service."""
        try:
            service = self.db.query(ApplicationService).filter(
                and_(
                    ApplicationService.id == service_id,
                    ApplicationService.tenant_id == tenant_id
                )
            ).first()
            
            if not service:
                return None
            
            # Get direct impacts (links)
            direct_impacts = []
            links = self.db.query(ServiceLink).filter(
                ServiceLink.application_service_id == service_id
            ).all()
            
            for link in links:
                direct_impacts.append({
                    "element_id": str(link.linked_element_id),
                    "element_type": link.linked_element_type,
                    "link_type": link.link_type,
                    "relationship_strength": link.relationship_strength,
                    "dependency_level": link.dependency_level,
                    "performance_impact": link.performance_impact
                })
            
            # Calculate risk assessment
            risk_assessment = {
                "business_criticality": service.business_criticality,
                "business_value": service.business_value,
                "security_level": service.security_level,
                "availability_risk": 100.0 - (service.current_availability_pct or service.availability_target_pct),
                "dependency_count": len(direct_impacts)
            }
            
            # Calculate total impact score
            total_impact_score = self._calculate_impact_score(service, direct_impacts)
            
            return ImpactMapResponse(
                service_id=service_id,
                direct_impacts=direct_impacts,
                indirect_impacts=[],  # Could be expanded with recursive analysis
                risk_assessment=risk_assessment,
                dependency_chain=[],  # Could be expanded with dependency chain analysis
                total_impact_score=total_impact_score
            )
            
        except Exception as e:
            logger.error(f"Error getting impact map: {e}")
            raise

    def get_performance_score(self, service_id: UUID, tenant_id: UUID) -> Optional[PerformanceScoreResponse]:
        """Get performance score for application service."""
        try:
            service = self.db.query(ApplicationService).filter(
                and_(
                    ApplicationService.id == service_id,
                    ApplicationService.tenant_id == tenant_id
                )
            ).first()
            
            if not service:
                return None
            
            # Calculate scores
            latency_score = self._calculate_latency_score(service)
            availability_score = self._calculate_availability_score(service)
            throughput_score = self._calculate_throughput_score(service)
            
            # Calculate overall score
            overall_score = (latency_score + availability_score + throughput_score) / 3
            
            # Generate recommendations
            recommendations = self._generate_performance_recommendations(service, overall_score)
            
            # Performance metrics
            performance_metrics = {
                "latency_target_ms": service.latency_target_ms,
                "availability_target_pct": service.availability_target_pct,
                "current_latency_ms": service.current_latency_ms,
                "current_availability_pct": service.current_availability_pct,
                "throughput_rps": service.throughput_rps,
                "service_type": service.service_type,
                "delivery_channel": service.delivery_channel
            }
            
            return PerformanceScoreResponse(
                service_id=service_id,
                latency_score=latency_score,
                availability_score=availability_score,
                throughput_score=throughput_score,
                overall_score=overall_score,
                recommendations=recommendations,
                performance_metrics=performance_metrics
            )
            
        except Exception as e:
            logger.error(f"Error getting performance score: {e}")
            raise

    def analyze_service(self, service_id: UUID, tenant_id: UUID) -> Optional[ServiceAnalysisResponse]:
        """Analyze application service comprehensively."""
        try:
            service = self.db.query(ApplicationService).filter(
                and_(
                    ApplicationService.id == service_id,
                    ApplicationService.tenant_id == tenant_id
                )
            ).first()
            
            if not service:
                return None
            
            # Operational health analysis
            operational_health = self._analyze_operational_health(service)
            
            # Business alignment analysis
            business_alignment = self._analyze_business_alignment(service)
            
            # Technical debt analysis
            technical_debt = self._analyze_technical_debt(service)
            
            # Risk factors
            risk_factors = self._identify_risk_factors(service)
            
            # Improvement opportunities
            improvement_opportunities = self._identify_improvement_opportunities(service)
            
            # Compliance status
            compliance_status = self._analyze_compliance_status(service)
            
            return ServiceAnalysisResponse(
                service_id=service_id,
                operational_health=operational_health,
                business_alignment=business_alignment,
                technical_debt=technical_debt,
                risk_factors=risk_factors,
                improvement_opportunities=improvement_opportunities,
                compliance_status=compliance_status
            )
            
        except Exception as e:
            logger.error(f"Error analyzing service: {e}")
            raise

    def _emit_service_event(self, event_type: str, service: ApplicationService):
        """Emit Redis event for service changes."""
        try:
            event_data = {
                "event_type": f"application_service_{event_type}",
                "service_id": str(service.id),
                "tenant_id": str(service.tenant_id),
                "user_id": str(service.user_id),
                "service_name": service.name,
                "service_type": service.service_type,
                "status": service.status,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.redis.publish("application_service_events", json.dumps(event_data))
            logger.info(f"Emitted {event_type} event for service {service.id}")
            
        except Exception as e:
            logger.error(f"Error emitting service event: {e}")

    def _calculate_impact_score(self, service: ApplicationService, direct_impacts: List[Dict]) -> float:
        """Calculate total impact score."""
        base_score = 0.5
        
        # Business criticality impact
        criticality_scores = {"low": 0.1, "medium": 0.3, "high": 0.6, "critical": 0.9}
        base_score += criticality_scores.get(service.business_criticality, 0.3)
        
        # Business value impact
        value_scores = {"low": 0.1, "medium": 0.3, "high": 0.6, "critical": 0.9}
        base_score += value_scores.get(service.business_value, 0.3)
        
        # Dependency impact
        dependency_impact = len(direct_impacts) * 0.05
        base_score += min(dependency_impact, 0.3)
        
        return min(base_score, 1.0)

    def _calculate_latency_score(self, service: ApplicationService) -> float:
        """Calculate latency performance score."""
        if not service.current_latency_ms or not service.latency_target_ms:
            return 0.8  # Default score if no metrics available
        
        ratio = service.latency_target_ms / service.current_latency_ms
        return min(ratio, 1.0)

    def _calculate_availability_score(self, service: ApplicationService) -> float:
        """Calculate availability performance score."""
        current_availability = service.current_availability_pct or service.availability_target_pct
        target_availability = service.availability_target_pct
        
        if current_availability >= target_availability:
            return 1.0
        else:
            return current_availability / target_availability

    def _calculate_throughput_score(self, service: ApplicationService) -> float:
        """Calculate throughput performance score."""
        if not service.throughput_rps:
            return 0.8  # Default score if no metrics available
        
        # Simple scoring based on throughput (could be enhanced with targets)
        if service.throughput_rps > 1000:
            return 1.0
        elif service.throughput_rps > 500:
            return 0.8
        elif service.throughput_rps > 100:
            return 0.6
        else:
            return 0.4

    def _generate_performance_recommendations(self, service: ApplicationService, overall_score: float) -> List[str]:
        """Generate performance improvement recommendations."""
        recommendations = []
        
        if overall_score < 0.7:
            recommendations.append("Consider implementing caching strategies to improve response times")
            recommendations.append("Review and optimize database queries")
            recommendations.append("Implement horizontal scaling for better throughput")
        
        if service.current_availability_pct and service.current_availability_pct < service.availability_target_pct:
            recommendations.append("Implement high availability patterns and failover mechanisms")
            recommendations.append("Review monitoring and alerting configuration")
        
        if not service.technology_stack:
            recommendations.append("Document technology stack and dependencies")
        
        if not service.api_documentation:
            recommendations.append("Create comprehensive API documentation")
        
        return recommendations

    def _analyze_operational_health(self, service: ApplicationService) -> Dict[str, Any]:
        """Analyze operational health of the service."""
        health_score = 0.8  # Base score
        
        # Availability impact
        if service.current_availability_pct:
            if service.current_availability_pct >= service.availability_target_pct:
                health_score += 0.1
            else:
                health_score -= 0.2
        
        # Incident impact
        if service.incident_count > 0:
            health_score -= min(service.incident_count * 0.05, 0.3)
        
        # SLA breaches impact
        if service.sla_breaches > 0:
            health_score -= min(service.sla_breaches * 0.1, 0.4)
        
        issues = []
        if service.current_availability_pct and service.current_availability_pct < service.availability_target_pct:
            issues.append("Availability below target")
        
        if service.incident_count > 5:
            issues.append("High incident count")
        
        status = "healthy" if health_score >= 0.7 else "degraded" if health_score >= 0.5 else "unhealthy"
        
        return {
            "overall_score": max(health_score, 0.0),
            "issues": issues,
            "status": status
        }

    def _analyze_business_alignment(self, service: ApplicationService) -> Dict[str, Any]:
        """Analyze business alignment of the service."""
        alignment_score = 0.5  # Base score
        
        # Business process alignment
        if service.business_process_id:
            alignment_score += 0.2
        
        # Capability alignment
        if service.capability_id:
            alignment_score += 0.2
        
        # Business value alignment
        if service.business_value in ["high", "critical"]:
            alignment_score += 0.1
        
        has_business_function = bool(service.business_process_id or service.capability_id)
        
        return {
            "alignment_score": min(alignment_score, 1.0),
            "has_business_function": has_business_function,
            "business_criticality": service.business_criticality,
            "business_value": service.business_value
        }

    def _analyze_technical_debt(self, service: ApplicationService) -> Dict[str, Any]:
        """Analyze technical debt of the service."""
        debt_score = 0.0
        debt_items = []
        
        # Missing documentation
        if not service.documentation_link:
            debt_score += 0.2
            debt_items.append("Missing documentation link")
        
        if not service.api_documentation:
            debt_score += 0.2
            debt_items.append("Missing API documentation")
        
        # Missing technology stack
        if not service.technology_stack:
            debt_score += 0.3
            debt_items.append("No technology stack documented")
        
        # Missing service endpoint
        if not service.service_endpoint:
            debt_score += 0.1
            debt_items.append("No service endpoint documented")
        
        priority = "low" if debt_score < 0.3 else "medium" if debt_score < 0.6 else "high"
        
        return {
            "debt_score": min(debt_score, 1.0),
            "debt_items": debt_items,
            "priority": priority
        }

    def _identify_risk_factors(self, service: ApplicationService) -> List[Dict[str, Any]]:
        """Identify risk factors for the service."""
        risk_factors = []
        
        # Business criticality risk
        if service.business_criticality in ["high", "critical"]:
            risk_factors.append({
                "type": "business_criticality",
                "severity": service.business_criticality,
                "description": f"Critical business service with {service.business_criticality} availability requirements"
            })
        
        # Security risk
        if service.security_level in ["high", "critical"]:
            risk_factors.append({
                "type": "security",
                "severity": service.security_level,
                "description": f"High security requirements with {service.security_level} level"
            })
        
        # Availability risk
        if service.current_availability_pct and service.current_availability_pct < service.availability_target_pct:
            risk_factors.append({
                "type": "availability",
                "severity": "high",
                "description": f"Availability below target: {service.current_availability_pct}% vs {service.availability_target_pct}%"
            })
        
        return risk_factors

    def _identify_improvement_opportunities(self, service: ApplicationService) -> List[str]:
        """Identify improvement opportunities for the service."""
        opportunities = []
        
        if not service.technology_stack:
            opportunities.append("Document technology stack and dependencies")
        
        if not service.api_documentation:
            opportunities.append("Create comprehensive API documentation")
        
        if not service.monitoring_config:
            opportunities.append("Implement comprehensive monitoring and alerting")
        
        if service.current_availability_pct and service.current_availability_pct < service.availability_target_pct:
            opportunities.append("Implement high availability patterns and failover mechanisms")
        
        if not service.backup_strategy:
            opportunities.append("Define backup and disaster recovery strategy")
        
        return opportunities

    def _analyze_compliance_status(self, service: ApplicationService) -> Dict[str, Any]:
        """Analyze compliance status of the service."""
        compliant_items = []
        non_compliant_items = []
        
        # Security compliance
        if service.security_level in ["high", "critical"]:
            compliant_items.append("security_level")
        else:
            non_compliant_items.append("security_level")
        
        # Documentation compliance
        if service.documentation_link:
            compliant_items.append("documentation")
        else:
            non_compliant_items.append("documentation")
        
        # Monitoring compliance
        if service.monitoring_config:
            compliant_items.append("monitoring")
        else:
            non_compliant_items.append("monitoring")
        
        compliance_rate = len(compliant_items) / (len(compliant_items) + len(non_compliant_items)) if (len(compliant_items) + len(non_compliant_items)) > 0 else 0.0
        
        status = "compliant" if compliance_rate >= 0.8 else "needs_attention" if compliance_rate >= 0.6 else "non_compliant"
        
        return {
            "compliance_rate": compliance_rate,
            "compliant_items": compliant_items,
            "non_compliant_items": non_compliant_items,
            "status": status
        }


class ServiceLinkService:
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis = redis_client

    def create_service_link(
        self,
        service_id: UUID,
        link_data: ServiceLinkCreate,
        tenant_id: UUID,
        user_id: UUID
    ) -> ServiceLinkResponse:
        """Create a new service link."""
        try:
            # Verify service exists and belongs to tenant
            service = self.db.query(ApplicationService).filter(
                and_(
                    ApplicationService.id == service_id,
                    ApplicationService.tenant_id == tenant_id
                )
            ).first()
            
            if not service:
                raise ValueError("Application service not found")
            
            # Create link
            db_link = ServiceLink(
                **link_data.dict(),
                application_service_id=service_id,
                created_by=user_id
            )
            
            self.db.add(db_link)
            self.db.commit()
            self.db.refresh(db_link)
            
            # Emit Redis event
            self._emit_link_event("created", db_link)
            
            return ServiceLinkResponse.from_orm(db_link)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating service link: {e}")
            raise

    def get_service_link(
        self,
        link_id: UUID,
        tenant_id: UUID
    ) -> Optional[ServiceLinkResponse]:
        """Get service link by ID."""
        try:
            link = self.db.query(ServiceLink).join(ApplicationService).filter(
                and_(
                    ServiceLink.id == link_id,
                    ApplicationService.tenant_id == tenant_id
                )
            ).first()
            
            if not link:
                return None
                
            return ServiceLinkResponse.from_orm(link)
            
        except Exception as e:
            logger.error(f"Error getting service link: {e}")
            raise

    def list_service_links(
        self,
        service_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[ServiceLinkResponse]:
        """List service links for an application service."""
        try:
            links = self.db.query(ServiceLink).join(ApplicationService).filter(
                and_(
                    ServiceLink.application_service_id == service_id,
                    ApplicationService.tenant_id == tenant_id
                )
            ).offset(skip).limit(limit).all()
            
            return [ServiceLinkResponse.from_orm(link) for link in links]
            
        except Exception as e:
            logger.error(f"Error listing service links: {e}")
            raise

    def update_service_link(
        self,
        link_id: UUID,
        link_data: ServiceLinkUpdate,
        tenant_id: UUID
    ) -> Optional[ServiceLinkResponse]:
        """Update service link."""
        try:
            link = self.db.query(ServiceLink).join(ApplicationService).filter(
                and_(
                    ServiceLink.id == link_id,
                    ApplicationService.tenant_id == tenant_id
                )
            ).first()
            
            if not link:
                return None
            
            # Update fields
            update_data = link_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(link, field, value)
            
            self.db.commit()
            self.db.refresh(link)
            
            # Emit Redis event
            self._emit_link_event("updated", link)
            
            return ServiceLinkResponse.from_orm(link)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating service link: {e}")
            raise

    def delete_service_link(
        self,
        link_id: UUID,
        tenant_id: UUID
    ) -> bool:
        """Delete service link."""
        try:
            link = self.db.query(ServiceLink).join(ApplicationService).filter(
                and_(
                    ServiceLink.id == link_id,
                    ApplicationService.tenant_id == tenant_id
                )
            ).first()
            
            if not link:
                return False
            
            # Emit Redis event before deletion
            self._emit_link_event("deleted", link)
            
            self.db.delete(link)
            self.db.commit()
            
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting service link: {e}")
            raise

    def _emit_link_event(self, event_type: str, link: ServiceLink):
        """Emit Redis event for link changes."""
        try:
            event_data = {
                "event_type": f"service_link_{event_type}",
                "link_id": str(link.id),
                "application_service_id": str(link.application_service_id),
                "linked_element_id": str(link.linked_element_id),
                "linked_element_type": link.linked_element_type,
                "link_type": link.link_type,
                "created_by": str(link.created_by),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.redis.publish("service_link_events", json.dumps(event_data))
            logger.info(f"Emitted {event_type} event for link {link.id}")
            
        except Exception as e:
            logger.error(f"Error emitting link event: {e}") 