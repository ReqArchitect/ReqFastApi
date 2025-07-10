from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from typing import List, Optional, Dict, Any
import json
import logging
import redis
from datetime import datetime, timedelta
import uuid

from .models import SystemSoftware, SoftwareLink
from .schemas import (
    SystemSoftwareCreate, SystemSoftwareUpdate,
    SoftwareLinkCreate, SoftwareLinkUpdate,
    DependencyMapResponse, ComplianceCheckResponse,
    SystemSoftwareAnalysisResponse
)
from .config import settings

logger = logging.getLogger(__name__)

class SystemSoftwareService:
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis_client = redis_client
    
    def create_system_software(self, tenant_id: uuid.UUID, user_id: uuid.UUID, 
                              system_software_data: SystemSoftwareCreate) -> SystemSoftware:
        """Create a new SystemSoftware."""
        try:
            system_software = SystemSoftware(
                tenant_id=tenant_id,
                user_id=user_id,
                **system_software_data.dict()
            )
            
            self.db.add(system_software)
            self.db.commit()
            self.db.refresh(system_software)
            
            # Emit Redis event
            self._emit_system_software_event("created", system_software)
            
            logger.info(f"Created system software: {system_software.id}")
            return system_software
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating system software: {e}")
            raise
    
    def get_system_software(self, system_software_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[SystemSoftware]:
        """Get SystemSoftware by ID."""
        return self.db.query(SystemSoftware).filter(
            and_(
                SystemSoftware.id == system_software_id,
                SystemSoftware.tenant_id == tenant_id
            )
        ).first()
    
    def list_system_software(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100,
                           software_type: Optional[str] = None,
                           vendor: Optional[str] = None,
                           lifecycle_state: Optional[str] = None,
                           vulnerability_threshold: Optional[float] = None) -> List[SystemSoftware]:
        """List SystemSoftware with filtering."""
        query = self.db.query(SystemSoftware).filter(SystemSoftware.tenant_id == tenant_id)
        
        if software_type:
            query = query.filter(SystemSoftware.software_type == software_type)
        if vendor:
            query = query.filter(SystemSoftware.vendor.ilike(f"%{vendor}%"))
        if lifecycle_state:
            query = query.filter(SystemSoftware.lifecycle_state == lifecycle_state)
        if vulnerability_threshold is not None:
            query = query.filter(SystemSoftware.vulnerability_score <= vulnerability_threshold)
        
        return query.offset(skip).limit(limit).all()
    
    def update_system_software(self, system_software_id: uuid.UUID, tenant_id: uuid.UUID,
                              system_software_data: SystemSoftwareUpdate) -> Optional[SystemSoftware]:
        """Update SystemSoftware."""
        try:
            system_software = self.get_system_software(system_software_id, tenant_id)
            if not system_software:
                return None
            
            update_data = system_software_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(system_software, field, value)
            
            system_software.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(system_software)
            
            # Emit Redis event
            self._emit_system_software_event("updated", system_software)
            
            logger.info(f"Updated system software: {system_software_id}")
            return system_software
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating system software: {e}")
            raise
    
    def delete_system_software(self, system_software_id: uuid.UUID, tenant_id: uuid.UUID) -> bool:
        """Delete SystemSoftware."""
        try:
            system_software = self.get_system_software(system_software_id, tenant_id)
            if not system_software:
                return False
            
            # Delete associated links first
            self.db.query(SoftwareLink).filter(
                SoftwareLink.system_software_id == system_software_id
            ).delete()
            
            self.db.delete(system_software)
            self.db.commit()
            
            # Emit Redis event
            self._emit_system_software_event("deleted", system_software)
            
            logger.info(f"Deleted system software: {system_software_id}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting system software: {e}")
            raise
    
    def get_dependency_map(self, system_software_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[DependencyMapResponse]:
        """Get dependency map for SystemSoftware."""
        system_software = self.get_system_software(system_software_id, tenant_id)
        if not system_software:
            return None
        
        # Parse dependencies from JSON strings
        dependencies = []
        if system_software.dependencies:
            try:
                dependencies = json.loads(system_software.dependencies)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON in dependencies for system software: {system_software_id}")
        
        dependent_components = []
        if system_software.dependent_components:
            try:
                dependent_components = json.loads(system_software.dependent_components)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON in dependent_components for system software: {system_software_id}")
        
        integration_points = []
        if system_software.integration_points:
            try:
                integration_points = json.loads(system_software.integration_points)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON in integration_points for system software: {system_software_id}")
        
        # Calculate dependency health
        dependency_health = self._calculate_dependency_health(system_software)
        
        return DependencyMapResponse(
            system_software_id=system_software_id,
            dependencies=dependencies,
            dependent_components=dependent_components,
            integration_points=integration_points,
            dependency_health=dependency_health
        )
    
    def get_compliance_check(self, system_software_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[ComplianceCheckResponse]:
        """Get compliance check for SystemSoftware."""
        system_software = self.get_system_software(system_software_id, tenant_id)
        if not system_software:
            return None
        
        # Compliance status analysis
        compliance_status = self._analyze_compliance_status(system_software)
        
        # Vulnerability assessment
        vulnerability_assessment = self._analyze_vulnerabilities(system_software)
        
        # Certification status
        certification_status = self._analyze_certifications(system_software)
        
        # Compliance recommendations
        compliance_recommendations = self._generate_compliance_recommendations(system_software)
        
        return ComplianceCheckResponse(
            system_software_id=system_software_id,
            compliance_status=compliance_status,
            vulnerability_assessment=vulnerability_assessment,
            certification_status=certification_status,
            compliance_recommendations=compliance_recommendations
        )
    
    def analyze_system_software(self, system_software_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[SystemSoftwareAnalysisResponse]:
        """Comprehensive analysis of SystemSoftware."""
        system_software = self.get_system_software(system_software_id, tenant_id)
        if not system_software:
            return None
        
        # Operational health analysis
        operational_health = self._analyze_operational_health(system_software)
        
        # Security status analysis
        security_status = self._analyze_security_status(system_software)
        
        # Performance metrics analysis
        performance_metrics = self._analyze_performance_metrics(system_software)
        
        # Risk assessment
        risk_assessment = self._analyze_risk_factors(system_software)
        
        # Improvement opportunities
        improvement_opportunities = self._identify_improvement_opportunities(system_software)
        
        # Compliance status
        compliance_status = self._analyze_compliance_status(system_software)
        
        return SystemSoftwareAnalysisResponse(
            system_software_id=system_software_id,
            operational_health=operational_health,
            security_status=security_status,
            performance_metrics=performance_metrics,
            risk_assessment=risk_assessment,
            improvement_opportunities=improvement_opportunities,
            compliance_status=compliance_status
        )
    
    def get_by_software_type(self, tenant_id: uuid.UUID, software_type: str) -> List[SystemSoftware]:
        """Get SystemSoftware by type."""
        return self.db.query(SystemSoftware).filter(
            and_(
                SystemSoftware.tenant_id == tenant_id,
                SystemSoftware.software_type == software_type
            )
        ).all()
    
    def get_by_vendor(self, tenant_id: uuid.UUID, vendor: str) -> List[SystemSoftware]:
        """Get SystemSoftware by vendor."""
        return self.db.query(SystemSoftware).filter(
            and_(
                SystemSoftware.tenant_id == tenant_id,
                SystemSoftware.vendor.ilike(f"%{vendor}%")
            )
        ).all()
    
    def get_by_vulnerability_score(self, tenant_id: uuid.UUID, max_score: float) -> List[SystemSoftware]:
        """Get SystemSoftware with vulnerability score below threshold."""
        return self.db.query(SystemSoftware).filter(
            and_(
                SystemSoftware.tenant_id == tenant_id,
                SystemSoftware.vulnerability_score <= max_score
            )
        ).all()
    
    def get_by_lifecycle_state(self, tenant_id: uuid.UUID, lifecycle_state: str) -> List[SystemSoftware]:
        """Get SystemSoftware by lifecycle state."""
        return self.db.query(SystemSoftware).filter(
            and_(
                SystemSoftware.tenant_id == tenant_id,
                SystemSoftware.lifecycle_state == lifecycle_state
            )
        ).all()
    
    def get_active_system_software(self, tenant_id: uuid.UUID) -> List[SystemSoftware]:
        """Get all active SystemSoftware."""
        return self.db.query(SystemSoftware).filter(
            and_(
                SystemSoftware.tenant_id == tenant_id,
                SystemSoftware.lifecycle_state == "active"
            )
        ).all()
    
    def get_critical_system_software(self, tenant_id: uuid.UUID) -> List[SystemSoftware]:
        """Get critical SystemSoftware (high vulnerability score or business critical)."""
        return self.db.query(SystemSoftware).filter(
            and_(
                SystemSoftware.tenant_id == tenant_id,
                or_(
                    SystemSoftware.vulnerability_score >= 7.0,
                    SystemSoftware.lifecycle_state == "active"
                )
            )
        ).all()
    
    # Private helper methods
    def _emit_system_software_event(self, event_type: str, system_software: SystemSoftware):
        """Emit Redis event for system software changes."""
        try:
            event_data = {
                "event_type": f"system_software_{event_type}",
                "system_software_id": str(system_software.id),
                "tenant_id": str(system_software.tenant_id),
                "software_type": system_software.software_type,
                "name": system_software.name,
                "version": system_software.version,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.redis_client.publish(
                f"system_software_events:{system_software.tenant_id}",
                json.dumps(event_data)
            )
            
            logger.info(f"Emitted system software event: {event_type} for {system_software.id}")
            
        except Exception as e:
            logger.error(f"Error emitting system software event: {e}")
    
    def _calculate_dependency_health(self, system_software: SystemSoftware) -> Dict[str, Any]:
        """Calculate dependency health score."""
        health_score = 1.0
        
        # Check for missing dependencies
        if not system_software.dependencies:
            health_score -= 0.2
        
        # Check for high vulnerability scores
        if system_software.vulnerability_score and system_software.vulnerability_score > 7.0:
            health_score -= 0.3
        elif system_software.vulnerability_score and system_software.vulnerability_score > 4.0:
            health_score -= 0.1
        
        # Check for outdated software
        if system_software.lifecycle_state == "deprecated":
            health_score -= 0.4
        elif system_software.lifecycle_state == "end_of_life":
            health_score -= 0.6
        
        # Check for missing patches
        if system_software.security_patches_available:
            health_score -= 0.2
        
        return {
            "overall_score": max(0.0, health_score),
            "status": "healthy" if health_score >= 0.7 else "warning" if health_score >= 0.4 else "critical",
            "issues": self._identify_dependency_issues(system_software)
        }
    
    def _identify_dependency_issues(self, system_software: SystemSoftware) -> List[str]:
        """Identify dependency issues."""
        issues = []
        
        if not system_software.dependencies:
            issues.append("No dependencies documented")
        
        if system_software.vulnerability_score and system_software.vulnerability_score > 7.0:
            issues.append(f"High vulnerability score: {system_software.vulnerability_score}")
        
        if system_software.lifecycle_state in ["deprecated", "end_of_life"]:
            issues.append(f"Software is {system_software.lifecycle_state}")
        
        if system_software.security_patches_available:
            issues.append("Security patches available but not applied")
        
        return issues
    
    def _analyze_compliance_status(self, system_software: SystemSoftware) -> Dict[str, Any]:
        """Analyze compliance status."""
        compliance_rate = 0.0
        compliant_items = []
        non_compliant_items = []
        
        # Check various compliance aspects
        if system_software.compliance_certifications:
            compliance_rate += 0.2
            compliant_items.append("certifications")
        else:
            non_compliant_items.append("certifications")
        
        if system_software.compliance_status == "compliant":
            compliance_rate += 0.3
            compliant_items.append("overall_status")
        elif system_software.compliance_status == "non_compliant":
            non_compliant_items.append("overall_status")
        
        if system_software.vulnerability_score and system_software.vulnerability_score <= 4.0:
            compliance_rate += 0.2
            compliant_items.append("vulnerability")
        else:
            non_compliant_items.append("vulnerability")
        
        if system_software.monitoring_enabled:
            compliance_rate += 0.15
            compliant_items.append("monitoring")
        else:
            non_compliant_items.append("monitoring")
        
        if system_software.backup_enabled:
            compliance_rate += 0.15
            compliant_items.append("backup")
        else:
            non_compliant_items.append("backup")
        
        return {
            "compliance_rate": compliance_rate,
            "compliant_items": compliant_items,
            "non_compliant_items": non_compliant_items,
            "status": "compliant" if compliance_rate >= 0.8 else "needs_attention" if compliance_rate >= 0.6 else "non_compliant"
        }
    
    def _analyze_vulnerabilities(self, system_software: SystemSoftware) -> Dict[str, Any]:
        """Analyze vulnerability assessment."""
        if not system_software.vulnerability_score:
            return {
                "score": None,
                "severity": "unknown",
                "risk_level": "unknown",
                "recommendations": ["Implement vulnerability scanning"]
            }
        
        if system_software.vulnerability_score >= 9.0:
            severity = "critical"
            risk_level = "critical"
        elif system_software.vulnerability_score >= 7.0:
            severity = "high"
            risk_level = "high"
        elif system_software.vulnerability_score >= 4.0:
            severity = "medium"
            risk_level = "medium"
        else:
            severity = "low"
            risk_level = "low"
        
        recommendations = []
        if system_software.vulnerability_score >= 7.0:
            recommendations.append("Immediate patch application required")
            recommendations.append("Consider temporary workarounds")
        elif system_software.vulnerability_score >= 4.0:
            recommendations.append("Schedule patch application")
        else:
            recommendations.append("Continue monitoring")
        
        if system_software.security_patches_available:
            recommendations.append("Apply available security patches")
        
        return {
            "score": system_software.vulnerability_score,
            "severity": severity,
            "risk_level": risk_level,
            "recommendations": recommendations
        }
    
    def _analyze_certifications(self, system_software: SystemSoftware) -> Dict[str, Any]:
        """Analyze certification status."""
        certifications = []
        if system_software.compliance_certifications:
            try:
                certifications = json.loads(system_software.compliance_certifications)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON in compliance_certifications for system software: {system_software.id}")
        
        return {
            "certifications": certifications,
            "certification_count": len(certifications),
            "has_certifications": len(certifications) > 0
        }
    
    def _generate_compliance_recommendations(self, system_software: SystemSoftware) -> List[str]:
        """Generate compliance recommendations."""
        recommendations = []
        
        if not system_software.compliance_certifications:
            recommendations.append("Document compliance certifications")
        
        if system_software.vulnerability_score and system_software.vulnerability_score > 4.0:
            recommendations.append("Address security vulnerabilities")
        
        if not system_software.monitoring_enabled:
            recommendations.append("Enable monitoring and alerting")
        
        if not system_software.backup_enabled:
            recommendations.append("Enable backup and recovery")
        
        if system_software.lifecycle_state in ["deprecated", "end_of_life"]:
            recommendations.append("Plan migration to supported software")
        
        return recommendations
    
    def _analyze_operational_health(self, system_software: SystemSoftware) -> Dict[str, Any]:
        """Analyze operational health."""
        health_score = 1.0
        issues = []
        
        # Check uptime
        if system_software.uptime_percentage and system_software.uptime_percentage < 99.0:
            health_score -= 0.2
            issues.append(f"Low uptime: {system_software.uptime_percentage}%")
        
        # Check resource usage
        if system_software.resource_usage and system_software.resource_usage > 80.0:
            health_score -= 0.1
            issues.append(f"High resource usage: {system_software.resource_usage}%")
        
        # Check response time
        if system_software.response_time_avg and system_software.response_time_avg > 1000.0:
            health_score -= 0.1
            issues.append(f"Slow response time: {system_software.response_time_avg}ms")
        
        # Check incident count
        if system_software.incident_count > 5:
            health_score -= 0.2
            issues.append(f"High incident count: {system_software.incident_count}")
        
        return {
            "overall_score": max(0.0, health_score),
            "status": "healthy" if health_score >= 0.8 else "warning" if health_score >= 0.6 else "critical",
            "issues": issues
        }
    
    def _analyze_security_status(self, system_software: SystemSoftware) -> Dict[str, Any]:
        """Analyze security status."""
        security_score = 1.0
        issues = []
        
        # Check vulnerability score
        if system_software.vulnerability_score and system_software.vulnerability_score > 7.0:
            security_score -= 0.4
            issues.append(f"Critical vulnerability: {system_software.vulnerability_score}")
        elif system_software.vulnerability_score and system_software.vulnerability_score > 4.0:
            security_score -= 0.2
            issues.append(f"Medium vulnerability: {system_software.vulnerability_score}")
        
        # Check for available patches
        if system_software.security_patches_available:
            security_score -= 0.2
            issues.append("Security patches available but not applied")
        
        # Check monitoring
        if not system_software.monitoring_enabled:
            security_score -= 0.1
            issues.append("Security monitoring disabled")
        
        # Check alerting
        if not system_software.alerting_enabled:
            security_score -= 0.1
            issues.append("Security alerting disabled")
        
        return {
            "security_score": max(0.0, security_score),
            "status": "secure" if security_score >= 0.8 else "warning" if security_score >= 0.6 else "critical",
            "issues": issues
        }
    
    def _analyze_performance_metrics(self, system_software: SystemSoftware) -> Dict[str, Any]:
        """Analyze performance metrics."""
        return {
            "resource_usage": system_software.resource_usage,
            "uptime_percentage": system_software.uptime_percentage,
            "response_time_avg": system_software.response_time_avg,
            "cpu_requirements": system_software.cpu_requirements,
            "memory_requirements": system_software.memory_requirements,
            "storage_requirements": system_software.storage_requirements,
            "network_requirements": system_software.network_requirements
        }
    
    def _analyze_risk_factors(self, system_software: SystemSoftware) -> Dict[str, Any]:
        """Analyze risk factors."""
        risk_factors = []
        overall_risk = "low"
        
        if system_software.vulnerability_score and system_software.vulnerability_score > 7.0:
            risk_factors.append({
                "type": "vulnerability",
                "severity": "high",
                "description": f"High vulnerability score: {system_software.vulnerability_score}"
            })
            overall_risk = "high"
        
        if system_software.lifecycle_state in ["deprecated", "end_of_life"]:
            risk_factors.append({
                "type": "lifecycle",
                "severity": "medium",
                "description": f"Software is {system_software.lifecycle_state}"
            })
            overall_risk = "medium" if overall_risk == "low" else overall_risk
        
        if system_software.incident_count > 5:
            risk_factors.append({
                "type": "operational",
                "severity": "medium",
                "description": f"High incident count: {system_software.incident_count}"
            })
            overall_risk = "medium" if overall_risk == "low" else overall_risk
        
        return {
            "overall_risk": overall_risk,
            "risk_factors": risk_factors
        }
    
    def _identify_improvement_opportunities(self, system_software: SystemSoftware) -> List[str]:
        """Identify improvement opportunities."""
        opportunities = []
        
        if not system_software.dependencies:
            opportunities.append("Document software dependencies")
        
        if not system_software.capabilities_provided:
            opportunities.append("Document provided capabilities")
        
        if system_software.vulnerability_score and system_software.vulnerability_score > 4.0:
            opportunities.append("Implement security improvements")
        
        if not system_software.monitoring_enabled:
            opportunities.append("Implement comprehensive monitoring")
        
        if not system_software.backup_enabled:
            opportunities.append("Implement backup and recovery procedures")
        
        if system_software.lifecycle_state in ["deprecated", "end_of_life"]:
            opportunities.append("Plan migration to supported software")
        
        return opportunities

class SoftwareLinkService:
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis_client = redis_client
    
    def create_software_link(self, system_software_id: uuid.UUID, tenant_id: uuid.UUID,
                           user_id: uuid.UUID, link_data: SoftwareLinkCreate) -> Optional[SoftwareLink]:
        """Create a new SoftwareLink."""
        try:
            # Verify system software exists
            system_software = self.db.query(SystemSoftware).filter(
                and_(
                    SystemSoftware.id == system_software_id,
                    SystemSoftware.tenant_id == tenant_id
                )
            ).first()
            
            if not system_software:
                return None
            
            software_link = SoftwareLink(
                system_software_id=system_software_id,
                created_by=user_id,
                **link_data.dict()
            )
            
            self.db.add(software_link)
            self.db.commit()
            self.db.refresh(software_link)
            
            # Emit Redis event
            self._emit_software_link_event("created", software_link)
            
            logger.info(f"Created software link: {software_link.id}")
            return software_link
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating software link: {e}")
            raise
    
    def get_software_link(self, link_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[SoftwareLink]:
        """Get SoftwareLink by ID."""
        return self.db.query(SoftwareLink).join(SystemSoftware).filter(
            and_(
                SoftwareLink.id == link_id,
                SystemSoftware.tenant_id == tenant_id
            )
        ).first()
    
    def list_software_links(self, system_software_id: uuid.UUID, tenant_id: uuid.UUID) -> List[SoftwareLink]:
        """List SoftwareLinks for a SystemSoftware."""
        return self.db.query(SoftwareLink).join(SystemSoftware).filter(
            and_(
                SoftwareLink.system_software_id == system_software_id,
                SystemSoftware.tenant_id == tenant_id
            )
        ).all()
    
    def update_software_link(self, link_id: uuid.UUID, tenant_id: uuid.UUID,
                           link_data: SoftwareLinkUpdate) -> Optional[SoftwareLink]:
        """Update SoftwareLink."""
        try:
            software_link = self.get_software_link(link_id, tenant_id)
            if not software_link:
                return None
            
            update_data = link_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(software_link, field, value)
            
            self.db.commit()
            self.db.refresh(software_link)
            
            # Emit Redis event
            self._emit_software_link_event("updated", software_link)
            
            logger.info(f"Updated software link: {link_id}")
            return software_link
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating software link: {e}")
            raise
    
    def delete_software_link(self, link_id: uuid.UUID, tenant_id: uuid.UUID) -> bool:
        """Delete SoftwareLink."""
        try:
            software_link = self.get_software_link(link_id, tenant_id)
            if not software_link:
                return False
            
            self.db.delete(software_link)
            self.db.commit()
            
            # Emit Redis event
            self._emit_software_link_event("deleted", software_link)
            
            logger.info(f"Deleted software link: {link_id}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting software link: {e}")
            raise
    
    def _emit_software_link_event(self, event_type: str, software_link: SoftwareLink):
        """Emit Redis event for software link changes."""
        try:
            event_data = {
                "event_type": f"software_link_{event_type}",
                "link_id": str(software_link.id),
                "system_software_id": str(software_link.system_software_id),
                "linked_element_id": str(software_link.linked_element_id),
                "linked_element_type": software_link.linked_element_type,
                "link_type": software_link.link_type,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Get tenant_id from system software
            system_software = self.db.query(SystemSoftware).filter(
                SystemSoftware.id == software_link.system_software_id
            ).first()
            
            if system_software:
                self.redis_client.publish(
                    f"software_link_events:{system_software.tenant_id}",
                    json.dumps(event_data)
                )
            
            logger.info(f"Emitted software link event: {event_type} for {software_link.id}")
            
        except Exception as e:
            logger.error(f"Error emitting software link event: {e}") 