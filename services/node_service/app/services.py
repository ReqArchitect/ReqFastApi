from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
import json
import logging
import redis
from datetime import datetime, timedelta
from uuid import UUID

from .models import Node, NodeLink
from .schemas import NodeCreate, NodeUpdate, NodeLinkCreate, NodeLinkUpdate
from .config import settings

logger = logging.getLogger(__name__)

class NodeService:
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis_client = redis_client

    def create_node(self, node_data: NodeCreate, tenant_id: UUID, user_id: UUID) -> Node:
        """Create a new node."""
        try:
            node = Node(
                tenant_id=tenant_id,
                user_id=user_id,
                **node_data.dict()
            )
            self.db.add(node)
            self.db.commit()
            self.db.refresh(node)
            
            # Emit Redis event
            self._emit_node_event("node.created", node)
            
            logger.info(f"Created node {node.id} for tenant {tenant_id}")
            return node
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating node: {e}")
            raise

    def get_node(self, node_id: UUID, tenant_id: UUID) -> Optional[Node]:
        """Get a node by ID with tenant isolation."""
        return self.db.query(Node).filter(
            and_(Node.id == node_id, Node.tenant_id == tenant_id)
        ).first()

    def list_nodes(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
        node_type: Optional[str] = None,
        environment: Optional[str] = None,
        lifecycle_state: Optional[str] = None,
        region: Optional[str] = None,
        security_level: Optional[str] = None,
        cluster_id: Optional[UUID] = None,
        performance_threshold: Optional[float] = None
    ) -> tuple[List[Node], int]:
        """List nodes with filtering and pagination."""
        query = self.db.query(Node).filter(Node.tenant_id == tenant_id)
        
        if node_type:
            query = query.filter(Node.node_type == node_type)
        if environment:
            query = query.filter(Node.environment == environment)
        if lifecycle_state:
            query = query.filter(Node.lifecycle_state == lifecycle_state)
        if region:
            query = query.filter(Node.region == region)
        if security_level:
            query = query.filter(Node.security_level == security_level)
        if cluster_id:
            query = query.filter(Node.cluster_id == cluster_id)
        if performance_threshold:
            query = query.filter(Node.current_availability >= performance_threshold)
        
        total = query.count()
        nodes = query.offset(skip).limit(limit).all()
        
        return nodes, total

    def update_node(self, node_id: UUID, node_data: NodeUpdate, tenant_id: UUID) -> Optional[Node]:
        """Update a node."""
        try:
            node = self.get_node(node_id, tenant_id)
            if not node:
                return None
            
            update_data = node_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(node, field, value)
            
            node.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(node)
            
            # Emit Redis event
            self._emit_node_event("node.updated", node)
            
            logger.info(f"Updated node {node_id}")
            return node
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating node {node_id}: {e}")
            raise

    def delete_node(self, node_id: UUID, tenant_id: UUID) -> bool:
        """Delete a node."""
        try:
            node = self.get_node(node_id, tenant_id)
            if not node:
                return False
            
            # Delete associated links first
            self.db.query(NodeLink).filter(NodeLink.node_id == node_id).delete()
            
            self.db.delete(node)
            self.db.commit()
            
            # Emit Redis event
            self._emit_node_event("node.deleted", {"id": str(node_id), "tenant_id": str(tenant_id)})
            
            logger.info(f"Deleted node {node_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting node {node_id}: {e}")
            raise

    def get_deployment_map(self, node_id: UUID, tenant_id: UUID) -> Optional[Dict[str, Any]]:
        """Get deployment map for a node."""
        node = self.get_node(node_id, tenant_id)
        if not node:
            return None
        
        # Get deployed components
        deployed_components = []
        if node.deployed_components:
            try:
                deployed_components = json.loads(node.deployed_components)
            except json.JSONDecodeError:
                deployed_components = []
        
        # Get deployment status
        links = self.db.query(NodeLink).filter(
            and_(NodeLink.node_id == node_id, NodeLink.link_type.in_(["hosts", "deploys"]))
        ).all()
        
        deployment_status = {
            "total_components": len(deployed_components),
            "active_deployments": len([l for l in links if l.deployment_status == "active"]),
            "failed_deployments": len([l for l in links if l.deployment_status == "failed"]),
            "pending_deployments": len([l for l in links if l.deployment_status == "pending"])
        }
        
        # Calculate resource allocation
        resource_allocation = self._calculate_resource_allocation(node, links)
        
        # Calculate capacity utilization
        capacity_utilization = self._calculate_capacity_utilization(node)
        
        # Calculate deployment health
        deployment_health = self._calculate_deployment_health(node, links)
        
        return {
            "node_id": str(node_id),
            "deployed_components": deployed_components,
            "deployment_status": deployment_status,
            "resource_allocation": resource_allocation,
            "capacity_utilization": capacity_utilization,
            "deployment_health": deployment_health
        }

    def get_capacity_analysis(self, node_id: UUID, tenant_id: UUID) -> Optional[Dict[str, Any]]:
        """Get capacity analysis for a node."""
        node = self.get_node(node_id, tenant_id)
        if not node:
            return None
        
        # Current capacity
        current_capacity = {
            "cpu_cores": node.cpu_cores or 0,
            "memory_gb": node.memory_gb or 0,
            "storage_gb": node.storage_gb or 0,
            "network_bandwidth_mbps": node.network_bandwidth_mbps or 0,
            "cpu_usage_pct": node.cpu_usage_pct or 0,
            "memory_usage_pct": node.memory_usage_pct or 0,
            "storage_usage_pct": node.storage_usage_pct or 0,
            "network_usage_pct": node.network_usage_pct or 0
        }
        
        # Projected capacity (simple linear projection)
        projected_capacity = self._project_capacity(node, current_capacity)
        
        # Generate recommendations
        capacity_recommendations = self._generate_capacity_recommendations(node, current_capacity)
        
        # Identify scaling opportunities
        scaling_opportunities = self._identify_scaling_opportunities(node, current_capacity)
        
        # Resource optimization suggestions
        resource_optimization = self._calculate_resource_optimization(node, current_capacity)
        
        return {
            "node_id": str(node_id),
            "current_capacity": current_capacity,
            "projected_capacity": projected_capacity,
            "capacity_recommendations": capacity_recommendations,
            "scaling_opportunities": scaling_opportunities,
            "resource_optimization": resource_optimization
        }

    def analyze_node(self, node_id: UUID, tenant_id: UUID) -> Optional[Dict[str, Any]]:
        """Comprehensive node analysis."""
        node = self.get_node(node_id, tenant_id)
        if not node:
            return None
        
        # Operational health
        operational_health = self._calculate_operational_health(node)
        
        # Performance metrics
        performance_metrics = self._calculate_performance_metrics(node)
        
        # Resource efficiency
        resource_efficiency = self._calculate_resource_efficiency(node)
        
        # Risk assessment
        risk_assessment = self._calculate_risk_assessment(node)
        
        # Improvement opportunities
        improvement_opportunities = self._identify_improvement_opportunities(node)
        
        # Compliance status
        compliance_status = self._calculate_compliance_status(node)
        
        return {
            "node_id": str(node_id),
            "operational_health": operational_health,
            "performance_metrics": performance_metrics,
            "resource_efficiency": resource_efficiency,
            "risk_assessment": risk_assessment,
            "improvement_opportunities": improvement_opportunities,
            "compliance_status": compliance_status
        }

    def get_nodes_by_type(self, node_type: str, tenant_id: UUID) -> List[Node]:
        """Get nodes filtered by type."""
        return self.db.query(Node).filter(
            and_(Node.tenant_id == tenant_id, Node.node_type == node_type)
        ).all()

    def get_nodes_by_environment(self, environment: str, tenant_id: UUID) -> List[Node]:
        """Get nodes filtered by environment."""
        return self.db.query(Node).filter(
            and_(Node.tenant_id == tenant_id, Node.environment == environment)
        ).all()

    def get_nodes_by_region(self, region: str, tenant_id: UUID) -> List[Node]:
        """Get nodes filtered by region."""
        return self.db.query(Node).filter(
            and_(Node.tenant_id == tenant_id, Node.region == region)
        ).all()

    def get_active_nodes(self, tenant_id: UUID) -> List[Node]:
        """Get all active nodes."""
        return self.db.query(Node).filter(
            and_(Node.tenant_id == tenant_id, Node.lifecycle_state == "active")
        ).all()

    def get_critical_nodes(self, tenant_id: UUID) -> List[Node]:
        """Get all critical nodes."""
        return self.db.query(Node).filter(
            and_(
                Node.tenant_id == tenant_id,
                or_(Node.security_level == "critical", Node.business_criticality == "critical")
            )
        ).all()

    def get_node_types(self) -> List[str]:
        """Get all available node types."""
        return ["vm", "container", "physical", "cloud", "edge"]

    def get_environments(self) -> List[str]:
        """Get all available environments."""
        return ["production", "staging", "development", "testing"]

    def get_lifecycle_states(self) -> List[str]:
        """Get all available lifecycle states."""
        return ["active", "inactive", "maintenance", "decommissioned", "planned"]

    def get_security_levels(self) -> List[str]:
        """Get all available security levels."""
        return ["basic", "standard", "high", "critical"]

    def get_link_types(self) -> List[str]:
        """Get all available link types."""
        return ["hosts", "deploys", "communicates_with", "depends_on", "manages"]

    def _emit_node_event(self, event_type: str, data: Any):
        """Emit Redis event for node operations."""
        try:
            event_data = {
                "event_type": event_type,
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }
            self.redis_client.publish("node_events", json.dumps(event_data))
        except Exception as e:
            logger.error(f"Error emitting Redis event: {e}")

    def _calculate_resource_allocation(self, node: Node, links: List[NodeLink]) -> Dict[str, Any]:
        """Calculate resource allocation for a node."""
        total_components = len(links)
        active_components = len([l for l in links if l.deployment_status == "active"])
        
        cpu_allocation = sum(l.resource_consumption or 0 for l in links if l.resource_consumption)
        memory_allocation = sum(l.resource_consumption or 0 for l in links if l.resource_consumption)
        
        return {
            "total_components": total_components,
            "active_components": active_components,
            "cpu_allocation_pct": min(cpu_allocation, 100.0),
            "memory_allocation_pct": min(memory_allocation, 100.0),
            "utilization_efficiency": (active_components / total_components * 100) if total_components > 0 else 0
        }

    def _calculate_capacity_utilization(self, node: Node) -> Dict[str, Any]:
        """Calculate capacity utilization for a node."""
        return {
            "cpu_utilization": node.cpu_usage_pct or 0,
            "memory_utilization": node.memory_usage_pct or 0,
            "storage_utilization": node.storage_usage_pct or 0,
            "network_utilization": node.network_usage_pct or 0,
            "overall_utilization": (
                (node.cpu_usage_pct or 0) + 
                (node.memory_usage_pct or 0) + 
                (node.storage_usage_pct or 0) + 
                (node.network_usage_pct or 0)
            ) / 4
        }

    def _calculate_deployment_health(self, node: Node, links: List[NodeLink]) -> Dict[str, Any]:
        """Calculate deployment health for a node."""
        if not links:
            return {"health_score": 0, "status": "no_deployments"}
        
        active_links = [l for l in links if l.deployment_status == "active"]
        failed_links = [l for l in links if l.deployment_status == "failed"]
        
        health_score = len(active_links) / len(links) * 100 if links else 0
        
        return {
            "health_score": health_score,
            "status": "healthy" if health_score >= 80 else "degraded" if health_score >= 50 else "unhealthy",
            "active_deployments": len(active_links),
            "failed_deployments": len(failed_links),
            "total_deployments": len(links)
        }

    def _project_capacity(self, node: Node, current_capacity: Dict[str, Any]) -> Dict[str, Any]:
        """Project capacity based on current usage trends."""
        # Simple linear projection (in real implementation, this would use historical data)
        growth_rate = 0.1  # 10% monthly growth
        
        return {
            "cpu_cores": current_capacity["cpu_cores"],
            "memory_gb": current_capacity["memory_gb"] * (1 + growth_rate),
            "storage_gb": current_capacity["storage_gb"] * (1 + growth_rate),
            "network_bandwidth_mbps": current_capacity["network_bandwidth_mbps"],
            "projected_cpu_usage": min(current_capacity["cpu_usage_pct"] * (1 + growth_rate), 100),
            "projected_memory_usage": min(current_capacity["memory_usage_pct"] * (1 + growth_rate), 100),
            "projected_storage_usage": min(current_capacity["storage_usage_pct"] * (1 + growth_rate), 100),
            "projected_network_usage": min(current_capacity["network_usage_pct"] * (1 + growth_rate), 100)
        }

    def _generate_capacity_recommendations(self, node: Node, current_capacity: Dict[str, Any]) -> List[str]:
        """Generate capacity recommendations."""
        recommendations = []
        
        if current_capacity["cpu_usage_pct"] > 80:
            recommendations.append("Consider CPU scaling or optimization")
        if current_capacity["memory_usage_pct"] > 80:
            recommendations.append("Consider memory scaling or optimization")
        if current_capacity["storage_usage_pct"] > 80:
            recommendations.append("Consider storage scaling or cleanup")
        if current_capacity["network_usage_pct"] > 80:
            recommendations.append("Consider network bandwidth upgrade")
        
        if not recommendations:
            recommendations.append("Current capacity is well-utilized")
        
        return recommendations

    def _identify_scaling_opportunities(self, node: Node, current_capacity: Dict[str, Any]) -> List[str]:
        """Identify scaling opportunities."""
        opportunities = []
        
        if current_capacity["cpu_usage_pct"] < 30:
            opportunities.append("CPU is underutilized - consider downsizing")
        if current_capacity["memory_usage_pct"] < 30:
            opportunities.append("Memory is underutilized - consider downsizing")
        if current_capacity["storage_usage_pct"] < 30:
            opportunities.append("Storage is underutilized - consider optimization")
        
        return opportunities

    def _calculate_resource_optimization(self, node: Node, current_capacity: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate resource optimization metrics."""
        return {
            "cpu_efficiency": 100 - current_capacity["cpu_usage_pct"],
            "memory_efficiency": 100 - current_capacity["memory_usage_pct"],
            "storage_efficiency": 100 - current_capacity["storage_usage_pct"],
            "network_efficiency": 100 - current_capacity["network_usage_pct"],
            "overall_efficiency": (
                (100 - current_capacity["cpu_usage_pct"]) +
                (100 - current_capacity["memory_usage_pct"]) +
                (100 - current_capacity["storage_usage_pct"]) +
                (100 - current_capacity["network_usage_pct"])
            ) / 4
        }

    def _calculate_operational_health(self, node: Node) -> Dict[str, Any]:
        """Calculate operational health score."""
        health_factors = []
        
        # Availability factor
        if node.current_availability:
            availability_score = min(node.current_availability / node.availability_target, 1.0)
            health_factors.append(availability_score)
        
        # Incident factor
        incident_score = max(0, 1 - (node.incident_count or 0) / 10)
        health_factors.append(incident_score)
        
        # SLA factor
        sla_score = max(0, 1 - (node.sla_breaches or 0) / 5)
        health_factors.append(sla_score)
        
        overall_score = sum(health_factors) / len(health_factors) if health_factors else 0
        
        return {
            "overall_score": overall_score,
            "availability_score": availability_score if node.current_availability else 0,
            "incident_score": incident_score,
            "sla_score": sla_score,
            "status": "healthy" if overall_score >= 0.8 else "degraded" if overall_score >= 0.6 else "unhealthy"
        }

    def _calculate_performance_metrics(self, node: Node) -> Dict[str, Any]:
        """Calculate performance metrics."""
        return {
            "response_time": node.cpu_usage_pct or 0,  # Simplified metric
            "throughput": node.network_usage_pct or 0,  # Simplified metric
            "availability": node.current_availability or 0,
            "resource_utilization": node.resource_utilization or 0,
            "performance_score": (
                (node.current_availability or 0) / 100 +
                (100 - (node.cpu_usage_pct or 0)) / 100 +
                (100 - (node.memory_usage_pct or 0)) / 100
            ) / 3
        }

    def _calculate_resource_efficiency(self, node: Node) -> Dict[str, Any]:
        """Calculate resource efficiency."""
        return {
            "cpu_efficiency": 100 - (node.cpu_usage_pct or 0),
            "memory_efficiency": 100 - (node.memory_usage_pct or 0),
            "storage_efficiency": 100 - (node.storage_usage_pct or 0),
            "network_efficiency": 100 - (node.network_usage_pct or 0),
            "overall_efficiency": (
                (100 - (node.cpu_usage_pct or 0)) +
                (100 - (node.memory_usage_pct or 0)) +
                (100 - (node.storage_usage_pct or 0)) +
                (100 - (node.network_usage_pct or 0))
            ) / 4
        }

    def _calculate_risk_assessment(self, node: Node) -> Dict[str, Any]:
        """Calculate risk assessment."""
        risk_factors = []
        
        # Security risk
        if node.security_level == "critical":
            risk_factors.append({"type": "security", "severity": "high", "description": "Critical security level"})
        
        # Availability risk
        if node.current_availability and node.current_availability < node.availability_target:
            risk_factors.append({"type": "availability", "severity": "medium", "description": "Below availability target"})
        
        # Incident risk
        if node.incident_count and node.incident_count > 5:
            risk_factors.append({"type": "incidents", "severity": "medium", "description": "High incident count"})
        
        return {
            "risk_factors": risk_factors,
            "overall_risk": "high" if len([r for r in risk_factors if r["severity"] == "high"]) > 0 else "medium" if risk_factors else "low"
        }

    def _identify_improvement_opportunities(self, node: Node) -> List[str]:
        """Identify improvement opportunities."""
        opportunities = []
        
        if not node.hardware_spec:
            opportunities.append("Document hardware specifications")
        if not node.host_capabilities:
            opportunities.append("Document host capabilities")
        if not node.deployed_components:
            opportunities.append("Document deployed components")
        if not node.monitoring_enabled:
            opportunities.append("Enable comprehensive monitoring")
        if not node.backup_enabled:
            opportunities.append("Enable backup and recovery")
        
        return opportunities

    def _calculate_compliance_status(self, node: Node) -> Dict[str, Any]:
        """Calculate compliance status."""
        compliant_items = []
        non_compliant_items = []
        
        if node.encryption_enabled:
            compliant_items.append("encryption")
        else:
            non_compliant_items.append("encryption")
        
        if node.monitoring_enabled:
            compliant_items.append("monitoring")
        else:
            non_compliant_items.append("monitoring")
        
        if node.backup_enabled:
            compliant_items.append("backup")
        else:
            non_compliant_items.append("backup")
        
        compliance_rate = len(compliant_items) / (len(compliant_items) + len(non_compliant_items)) if (compliant_items or non_compliant_items) else 0
        
        return {
            "compliance_rate": compliance_rate,
            "compliant_items": compliant_items,
            "non_compliant_items": non_compliant_items,
            "status": "compliant" if compliance_rate >= 0.8 else "needs_attention" if compliance_rate >= 0.5 else "non_compliant"
        }

class NodeLinkService:
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis_client = redis_client

    def create_node_link(self, node_id: UUID, link_data: NodeLinkCreate, tenant_id: UUID, user_id: UUID) -> NodeLink:
        """Create a new node link."""
        try:
            # Verify node exists and belongs to tenant
            node = self.db.query(Node).filter(
                and_(Node.id == node_id, Node.tenant_id == tenant_id)
            ).first()
            if not node:
                raise ValueError("Node not found")
            
            link = NodeLink(
                node_id=node_id,
                created_by=user_id,
                **link_data.dict()
            )
            self.db.add(link)
            self.db.commit()
            self.db.refresh(link)
            
            # Emit Redis event
            self._emit_link_event("node_link.created", link)
            
            logger.info(f"Created node link {link.id} for node {node_id}")
            return link
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating node link: {e}")
            raise

    def get_node_link(self, link_id: UUID, tenant_id: UUID) -> Optional[NodeLink]:
        """Get a node link by ID with tenant isolation."""
        return self.db.query(NodeLink).join(Node).filter(
            and_(NodeLink.id == link_id, Node.tenant_id == tenant_id)
        ).first()

    def list_node_links(self, node_id: UUID, tenant_id: UUID) -> List[NodeLink]:
        """List all links for a node."""
        return self.db.query(NodeLink).join(Node).filter(
            and_(NodeLink.node_id == node_id, Node.tenant_id == tenant_id)
        ).all()

    def update_node_link(self, link_id: UUID, link_data: NodeLinkUpdate, tenant_id: UUID) -> Optional[NodeLink]:
        """Update a node link."""
        try:
            link = self.get_node_link(link_id, tenant_id)
            if not link:
                return None
            
            update_data = link_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(link, field, value)
            
            self.db.commit()
            self.db.refresh(link)
            
            # Emit Redis event
            self._emit_link_event("node_link.updated", link)
            
            logger.info(f"Updated node link {link_id}")
            return link
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating node link {link_id}: {e}")
            raise

    def delete_node_link(self, link_id: UUID, tenant_id: UUID) -> bool:
        """Delete a node link."""
        try:
            link = self.get_node_link(link_id, tenant_id)
            if not link:
                return False
            
            self.db.delete(link)
            self.db.commit()
            
            # Emit Redis event
            self._emit_link_event("node_link.deleted", {"id": str(link_id), "tenant_id": str(tenant_id)})
            
            logger.info(f"Deleted node link {link_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting node link {link_id}: {e}")
            raise

    def _emit_link_event(self, event_type: str, data: Any):
        """Emit Redis event for node link operations."""
        try:
            event_data = {
                "event_type": event_type,
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }
            self.redis_client.publish("node_link_events", json.dumps(event_data))
        except Exception as e:
            logger.error(f"Error emitting Redis event: {e}") 