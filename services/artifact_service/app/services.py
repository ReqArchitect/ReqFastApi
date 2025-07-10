from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import List, Optional, Dict, Any
import uuid
import json
import logging
from datetime import datetime, timedelta
import redis
from opentelemetry import trace

from .models import Artifact, ArtifactLink
from .schemas import ArtifactCreate, ArtifactUpdate, ArtifactLinkCreate, ArtifactLinkUpdate
from .config import settings

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

class ArtifactService:
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis_client = redis_client

    def create_artifact(self, artifact_data: ArtifactCreate, tenant_id: uuid.UUID, user_id: uuid.UUID) -> Artifact:
        """Create a new artifact."""
        with tracer.start_as_current_span("create_artifact"):
            try:
                artifact = Artifact(
                    **artifact_data.dict(),
                    tenant_id=tenant_id,
                    user_id=user_id,
                    owner_user_id=user_id
                )
                
                self.db.add(artifact)
                self.db.commit()
                self.db.refresh(artifact)
                
                # Emit Redis event
                self._emit_artifact_event("artifact.created", artifact)
                
                logger.info(f"Created artifact {artifact.id} for tenant {tenant_id}")
                return artifact
                
            except Exception as e:
                self.db.rollback()
                logger.error(f"Error creating artifact: {e}")
                raise

    def get_artifact(self, artifact_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[Artifact]:
        """Get an artifact by ID."""
        with tracer.start_as_current_span("get_artifact"):
            return self.db.query(Artifact).filter(
                and_(
                    Artifact.id == artifact_id,
                    Artifact.tenant_id == tenant_id
                )
            ).first()

    def list_artifacts(
        self,
        tenant_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        artifact_type: Optional[str] = None,
        lifecycle_state: Optional[str] = None,
        deployment_environment: Optional[str] = None,
        format_filter: Optional[str] = None,
        deployment_target_node_id: Optional[uuid.UUID] = None,
        associated_component_id: Optional[uuid.UUID] = None,
        integrity_verified: Optional[bool] = None,
        security_scan_passed: Optional[bool] = None,
        compliance_status: Optional[str] = None,
        data_classification: Optional[str] = None,
        size_threshold: Optional[float] = None,
        vulnerability_threshold: Optional[int] = None,
        quality_threshold: Optional[float] = None,
        search_term: Optional[str] = None
    ) -> List[Artifact]:
        """List artifacts with filtering."""
        with tracer.start_as_current_span("list_artifacts"):
            query = self.db.query(Artifact).filter(Artifact.tenant_id == tenant_id)
            
            if artifact_type:
                query = query.filter(Artifact.artifact_type == artifact_type)
            if lifecycle_state:
                query = query.filter(Artifact.lifecycle_state == lifecycle_state)
            if deployment_environment:
                query = query.filter(Artifact.deployment_environment == deployment_environment)
            if format_filter:
                query = query.filter(Artifact.format.contains(format_filter))
            if deployment_target_node_id:
                query = query.filter(Artifact.deployment_target_node_id == deployment_target_node_id)
            if associated_component_id:
                query = query.filter(Artifact.associated_component_id == associated_component_id)
            if integrity_verified is not None:
                query = query.filter(Artifact.integrity_verified == integrity_verified)
            if security_scan_passed is not None:
                query = query.filter(Artifact.security_scan_passed == security_scan_passed)
            if compliance_status:
                query = query.filter(Artifact.compliance_status == compliance_status)
            if data_classification:
                query = query.filter(Artifact.data_classification == data_classification)
            if size_threshold is not None:
                query = query.filter(Artifact.size_mb <= size_threshold)
            if vulnerability_threshold is not None:
                query = query.filter(Artifact.vulnerability_count <= vulnerability_threshold)
            if quality_threshold is not None:
                query = query.filter(Artifact.quality_score >= quality_threshold)
            if search_term:
                query = query.filter(
                    or_(
                        Artifact.name.contains(search_term),
                        Artifact.description.contains(search_term),
                        Artifact.storage_location.contains(search_term)
                    )
                )
            
            return query.order_by(desc(Artifact.created_at)).offset(skip).limit(limit).all()

    def update_artifact(self, artifact_id: uuid.UUID, artifact_data: ArtifactUpdate, tenant_id: uuid.UUID) -> Optional[Artifact]:
        """Update an artifact."""
        with tracer.start_as_current_span("update_artifact"):
            try:
                artifact = self.get_artifact(artifact_id, tenant_id)
                if not artifact:
                    return None
                
                update_data = artifact_data.dict(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(artifact, field, value)
                
                artifact.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(artifact)
                
                # Emit Redis event
                self._emit_artifact_event("artifact.updated", artifact)
                
                logger.info(f"Updated artifact {artifact_id} for tenant {tenant_id}")
                return artifact
                
            except Exception as e:
                self.db.rollback()
                logger.error(f"Error updating artifact {artifact_id}: {e}")
                raise

    def delete_artifact(self, artifact_id: uuid.UUID, tenant_id: uuid.UUID) -> bool:
        """Delete an artifact."""
        with tracer.start_as_current_span("delete_artifact"):
            try:
                artifact = self.get_artifact(artifact_id, tenant_id)
                if not artifact:
                    return False
                
                # Emit Redis event before deletion
                self._emit_artifact_event("artifact.deleted", artifact)
                
                self.db.delete(artifact)
                self.db.commit()
                
                logger.info(f"Deleted artifact {artifact_id} for tenant {tenant_id}")
                return True
                
            except Exception as e:
                self.db.rollback()
                logger.error(f"Error deleting artifact {artifact_id}: {e}")
                raise

    def get_artifact_dependency_map(self, artifact_id: uuid.UUID, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Get dependency map for an artifact."""
        with tracer.start_as_current_span("get_artifact_dependency_map"):
            artifact = self.get_artifact(artifact_id, tenant_id)
            if not artifact:
                return {}
            
            # Parse dependencies
            direct_dependencies = []
            if artifact.dependencies:
                try:
                    direct_dependencies = json.loads(artifact.dependencies)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON in dependencies for artifact {artifact_id}")
            
            # Get dependent artifacts
            dependent_artifacts = []
            if artifact.dependent_artifacts:
                try:
                    dependent_artifacts = json.loads(artifact.dependent_artifacts)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON in dependent_artifacts for artifact {artifact_id}")
            
            # Build dependency tree
            dependency_tree = {
                "artifact_id": str(artifact_id),
                "name": artifact.name,
                "type": artifact.artifact_type,
                "direct_dependencies": direct_dependencies,
                "dependent_artifacts": dependent_artifacts,
                "build_dependencies": json.loads(artifact.build_dependencies) if artifact.build_dependencies else []
            }
            
            # Analyze circular dependencies
            circular_dependencies = self._detect_circular_dependencies(dependency_tree)
            
            return {
                "artifact_id": artifact_id,
                "direct_dependencies": direct_dependencies,
                "indirect_dependencies": self._get_indirect_dependencies(direct_dependencies),
                "dependency_tree": dependency_tree,
                "circular_dependencies": circular_dependencies,
                "total_dependencies": len(direct_dependencies),
                "max_depth": self._calculate_dependency_depth(dependency_tree)
            }

    def check_artifact_integrity(self, artifact_id: uuid.UUID, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Check artifact integrity and security."""
        with tracer.start_as_current_span("check_artifact_integrity"):
            artifact = self.get_artifact(artifact_id, tenant_id)
            if not artifact:
                return {}
            
            # Calculate integrity score
            integrity_score = self._calculate_integrity_score(artifact)
            
            # Security analysis
            security_analysis = self._analyze_security(artifact)
            
            # Compliance check
            compliance_check = self._check_compliance(artifact)
            
            # Generate recommendations
            recommendations = self._generate_integrity_recommendations(artifact, integrity_score, security_analysis)
            
            # Identify issues
            issues = self._identify_integrity_issues(artifact, integrity_score, security_analysis, compliance_check)
            
            return {
                "artifact_id": artifact_id,
                "checksum_valid": artifact.integrity_verified,
                "security_scan_passed": artifact.security_scan_passed,
                "vulnerability_count": artifact.vulnerability_count,
                "security_score": artifact.security_score or 0.0,
                "integrity_score": integrity_score,
                "compliance_status": artifact.compliance_status,
                "recommendations": recommendations,
                "issues": issues
            }

    def get_artifacts_by_type(self, artifact_type: str, tenant_id: uuid.UUID) -> List[Artifact]:
        """Get artifacts by type."""
        return self.list_artifacts(tenant_id, artifact_type=artifact_type)

    def get_artifacts_by_format(self, format_filter: str, tenant_id: uuid.UUID) -> List[Artifact]:
        """Get artifacts by format."""
        return self.list_artifacts(tenant_id, format_filter=format_filter)

    def get_artifacts_by_deployment_target(self, node_id: uuid.UUID, tenant_id: uuid.UUID) -> List[Artifact]:
        """Get artifacts by deployment target node."""
        return self.list_artifacts(tenant_id, deployment_target_node_id=node_id)

    def get_artifacts_by_component(self, component_id: uuid.UUID, tenant_id: uuid.UUID) -> List[Artifact]:
        """Get artifacts by associated component."""
        return self.list_artifacts(tenant_id, associated_component_id=component_id)

    def get_artifacts_by_modification_date(self, start_date: datetime, end_date: datetime, tenant_id: uuid.UUID) -> List[Artifact]:
        """Get artifacts modified between dates."""
        return self.db.query(Artifact).filter(
            and_(
                Artifact.tenant_id == tenant_id,
                Artifact.last_modified >= start_date,
                Artifact.last_modified <= end_date
            )
        ).order_by(desc(Artifact.last_modified)).all()

    def get_active_artifacts(self, tenant_id: uuid.UUID) -> List[Artifact]:
        """Get all active artifacts."""
        return self.list_artifacts(tenant_id, lifecycle_state="active")

    def get_critical_artifacts(self, tenant_id: uuid.UUID) -> List[Artifact]:
        """Get critical artifacts (high business value or security score)."""
        return self.db.query(Artifact).filter(
            and_(
                Artifact.tenant_id == tenant_id,
                or_(
                    Artifact.data_classification == "restricted",
                    Artifact.security_score >= 8.0,
                    Artifact.business_criticality == "critical"
                )
            )
        ).all()

    def get_artifact_statistics(self, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Get artifact statistics for tenant."""
        stats = self.db.query(
            func.count(Artifact.id).label("total_artifacts"),
            func.count(Artifact.id).filter(Artifact.lifecycle_state == "active").label("active_artifacts"),
            func.count(Artifact.id).filter(Artifact.integrity_verified == True).label("verified_artifacts"),
            func.count(Artifact.id).filter(Artifact.security_scan_passed == True).label("secure_artifacts"),
            func.avg(Artifact.size_mb).label("avg_size_mb"),
            func.sum(Artifact.size_mb).label("total_size_mb"),
            func.avg(Artifact.security_score).label("avg_security_score"),
            func.avg(Artifact.quality_score).label("avg_quality_score")
        ).filter(Artifact.tenant_id == tenant_id).first()
        
        return {
            "total_artifacts": stats.total_artifacts or 0,
            "active_artifacts": stats.active_artifacts or 0,
            "verified_artifacts": stats.verified_artifacts or 0,
            "secure_artifacts": stats.secure_artifacts or 0,
            "avg_size_mb": float(stats.avg_size_mb) if stats.avg_size_mb else 0.0,
            "total_size_mb": float(stats.total_size_mb) if stats.total_size_mb else 0.0,
            "avg_security_score": float(stats.avg_security_score) if stats.avg_security_score else 0.0,
            "avg_quality_score": float(stats.avg_quality_score) if stats.avg_quality_score else 0.0
        }

    def _emit_artifact_event(self, event_type: str, artifact: Artifact):
        """Emit Redis event for artifact changes."""
        try:
            event_data = {
                "event_type": event_type,
                "artifact_id": str(artifact.id),
                "tenant_id": str(artifact.tenant_id),
                "user_id": str(artifact.user_id),
                "artifact_type": artifact.artifact_type,
                "name": artifact.name,
                "version": artifact.version,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.redis_client.publish(
                f"artifact_events:{artifact.tenant_id}",
                json.dumps(event_data)
            )
            
            logger.info(f"Emitted {event_type} event for artifact {artifact.id}")
            
        except Exception as e:
            logger.error(f"Error emitting artifact event: {e}")

    def _detect_circular_dependencies(self, dependency_tree: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect circular dependencies in artifact dependency tree."""
        # Simplified circular dependency detection
        # In a real implementation, this would traverse the dependency graph
        return []

    def _get_indirect_dependencies(self, direct_dependencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get indirect dependencies for artifacts."""
        # Simplified indirect dependency resolution
        # In a real implementation, this would traverse the dependency graph
        return []

    def _calculate_dependency_depth(self, dependency_tree: Dict[str, Any]) -> int:
        """Calculate the maximum depth of the dependency tree."""
        # Simplified depth calculation
        return len(dependency_tree.get("direct_dependencies", []))

    def _calculate_integrity_score(self, artifact: Artifact) -> float:
        """Calculate integrity score for artifact."""
        score = 0.0
        factors = 0
        
        if artifact.integrity_verified:
            score += 0.3
        factors += 1
        
        if artifact.security_scan_passed:
            score += 0.3
        factors += 1
        
        if artifact.checksum:
            score += 0.2
        factors += 1
        
        if artifact.vulnerability_count == 0:
            score += 0.2
        factors += 1
        
        return score / factors if factors > 0 else 0.0

    def _analyze_security(self, artifact: Artifact) -> Dict[str, Any]:
        """Analyze security aspects of artifact."""
        return {
            "security_score": artifact.security_score or 0.0,
            "vulnerability_count": artifact.vulnerability_count,
            "security_scan_passed": artifact.security_scan_passed,
            "data_classification": artifact.data_classification,
            "public_access": artifact.public_access
        }

    def _check_compliance(self, artifact: Artifact) -> Dict[str, Any]:
        """Check compliance status of artifact."""
        return {
            "compliance_status": artifact.compliance_status,
            "audit_requirements": json.loads(artifact.audit_requirements) if artifact.audit_requirements else {},
            "retention_policy": json.loads(artifact.retention_policy) if artifact.retention_policy else {}
        }

    def _generate_integrity_recommendations(self, artifact: Artifact, integrity_score: float, security_analysis: Dict[str, Any]) -> List[str]:
        """Generate integrity recommendations."""
        recommendations = []
        
        if integrity_score < 0.7:
            recommendations.append("Improve artifact integrity verification")
        
        if not artifact.integrity_verified:
            recommendations.append("Implement checksum verification")
        
        if not artifact.security_scan_passed:
            recommendations.append("Address security vulnerabilities")
        
        if artifact.vulnerability_count > 0:
            recommendations.append(f"Fix {artifact.vulnerability_count} security vulnerabilities")
        
        if artifact.security_score and artifact.security_score < 7.0:
            recommendations.append("Improve security posture")
        
        return recommendations

    def _identify_integrity_issues(self, artifact: Artifact, integrity_score: float, security_analysis: Dict[str, Any], compliance_check: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify integrity issues."""
        issues = []
        
        if not artifact.integrity_verified:
            issues.append({
                "type": "integrity",
                "severity": "high",
                "description": "Artifact integrity not verified"
            })
        
        if not artifact.security_scan_passed:
            issues.append({
                "type": "security",
                "severity": "high",
                "description": "Security scan failed"
            })
        
        if artifact.vulnerability_count > 0:
            issues.append({
                "type": "security",
                "severity": "medium",
                "description": f"{artifact.vulnerability_count} vulnerabilities detected"
            })
        
        if artifact.compliance_status == "non_compliant":
            issues.append({
                "type": "compliance",
                "severity": "medium",
                "description": "Artifact is non-compliant"
            })
        
        return issues

class ArtifactLinkService:
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis_client = redis_client

    def create_artifact_link(self, artifact_id: uuid.UUID, link_data: ArtifactLinkCreate, tenant_id: uuid.UUID, user_id: uuid.UUID) -> ArtifactLink:
        """Create a new artifact link."""
        with tracer.start_as_current_span("create_artifact_link"):
            try:
                # Verify artifact exists and belongs to tenant
                artifact = self.db.query(Artifact).filter(
                    and_(
                        Artifact.id == artifact_id,
                        Artifact.tenant_id == tenant_id
                    )
                ).first()
                
                if not artifact:
                    raise ValueError("Artifact not found")
                
                link = ArtifactLink(
                    **link_data.dict(),
                    artifact_id=artifact_id,
                    created_by=user_id
                )
                
                self.db.add(link)
                self.db.commit()
                self.db.refresh(link)
                
                # Emit Redis event
                self._emit_link_event("artifact_link.created", link)
                
                logger.info(f"Created artifact link {link.id} for artifact {artifact_id}")
                return link
                
            except Exception as e:
                self.db.rollback()
                logger.error(f"Error creating artifact link: {e}")
                raise

    def get_artifact_links(self, artifact_id: uuid.UUID, tenant_id: uuid.UUID) -> List[ArtifactLink]:
        """Get all links for an artifact."""
        with tracer.start_as_current_span("get_artifact_links"):
            return self.db.query(ArtifactLink).join(Artifact).filter(
                and_(
                    ArtifactLink.artifact_id == artifact_id,
                    Artifact.tenant_id == tenant_id
                )
            ).all()

    def get_artifact_link(self, link_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[ArtifactLink]:
        """Get an artifact link by ID."""
        with tracer.start_as_current_span("get_artifact_link"):
            return self.db.query(ArtifactLink).join(Artifact).filter(
                and_(
                    ArtifactLink.id == link_id,
                    Artifact.tenant_id == tenant_id
                )
            ).first()

    def update_artifact_link(self, link_id: uuid.UUID, link_data: ArtifactLinkUpdate, tenant_id: uuid.UUID) -> Optional[ArtifactLink]:
        """Update an artifact link."""
        with tracer.start_as_current_span("update_artifact_link"):
            try:
                link = self.get_artifact_link(link_id, tenant_id)
                if not link:
                    return None
                
                update_data = link_data.dict(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(link, field, value)
                
                self.db.commit()
                self.db.refresh(link)
                
                # Emit Redis event
                self._emit_link_event("artifact_link.updated", link)
                
                logger.info(f"Updated artifact link {link_id}")
                return link
                
            except Exception as e:
                self.db.rollback()
                logger.error(f"Error updating artifact link {link_id}: {e}")
                raise

    def delete_artifact_link(self, link_id: uuid.UUID, tenant_id: uuid.UUID) -> bool:
        """Delete an artifact link."""
        with tracer.start_as_current_span("delete_artifact_link"):
            try:
                link = self.get_artifact_link(link_id, tenant_id)
                if not link:
                    return False
                
                # Emit Redis event before deletion
                self._emit_link_event("artifact_link.deleted", link)
                
                self.db.delete(link)
                self.db.commit()
                
                logger.info(f"Deleted artifact link {link_id}")
                return True
                
            except Exception as e:
                self.db.rollback()
                logger.error(f"Error deleting artifact link {link_id}: {e}")
                raise

    def get_links_by_element(self, element_id: uuid.UUID, element_type: str, tenant_id: uuid.UUID) -> List[ArtifactLink]:
        """Get artifact links by linked element."""
        with tracer.start_as_current_span("get_links_by_element"):
            return self.db.query(ArtifactLink).join(Artifact).filter(
                and_(
                    ArtifactLink.linked_element_id == element_id,
                    ArtifactLink.linked_element_type == element_type,
                    Artifact.tenant_id == tenant_id
                )
            ).all()

    def get_links_by_type(self, link_type: str, tenant_id: uuid.UUID) -> List[ArtifactLink]:
        """Get artifact links by link type."""
        with tracer.start_as_current_span("get_links_by_type"):
            return self.db.query(ArtifactLink).join(Artifact).filter(
                and_(
                    ArtifactLink.link_type == link_type,
                    Artifact.tenant_id == tenant_id
                )
            ).all()

    def _emit_link_event(self, event_type: str, link: ArtifactLink):
        """Emit Redis event for artifact link changes."""
        try:
            event_data = {
                "event_type": event_type,
                "link_id": str(link.id),
                "artifact_id": str(link.artifact_id),
                "linked_element_id": str(link.linked_element_id),
                "linked_element_type": link.linked_element_type,
                "link_type": link.link_type,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Get tenant_id from artifact
            artifact = self.db.query(Artifact).filter(Artifact.id == link.artifact_id).first()
            if artifact:
                self.redis_client.publish(
                    f"artifact_link_events:{artifact.tenant_id}",
                    json.dumps(event_data)
                )
            
            logger.info(f"Emitted {event_type} event for link {link.id}")
            
        except Exception as e:
            logger.error(f"Error emitting artifact link event: {e}") 