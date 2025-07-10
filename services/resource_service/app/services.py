from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from uuid import UUID
from . import models, schemas
from fastapi import HTTPException, status
import json
import redis
import os
from datetime import datetime

# Redis connection for event emission
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    decode_responses=True
)

def emit_event(event_type: str, data: Dict[str, Any]):
    """Emit event to Redis for event-driven architecture"""
    try:
        event = {
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        redis_client.publish("resource_events", json.dumps(event))
    except Exception as e:
        # Log error but don't fail the operation
        print(f"Failed to emit event: {e}")

# Resource CRUD operations
def create_resource(
    db: Session, 
    resource_in: schemas.ResourceCreate, 
    tenant_id: UUID, 
    user_id: UUID
) -> models.Resource:
    """Create a new resource"""
    db_resource = models.Resource(
        **resource_in.dict(),
        tenant_id=tenant_id,
        user_id=user_id,
        available_quantity=resource_in.quantity
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    
    # Emit event
    emit_event("resource.created", {
        "resource_id": str(db_resource.id),
        "tenant_id": str(tenant_id),
        "user_id": str(user_id)
    })
    
    return db_resource

def get_resource(db: Session, resource_id: UUID, tenant_id: UUID) -> models.Resource:
    """Get resource by ID"""
    resource = db.query(models.Resource).filter(
        and_(
            models.Resource.id == resource_id,
            models.Resource.tenant_id == tenant_id
        )
    ).first()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    return resource

def get_resources(
    db: Session,
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    resource_type: Optional[str] = None,
    deployment_status: Optional[str] = None,
    criticality: Optional[str] = None,
    strategic_importance: Optional[str] = None,
    associated_capability_id: Optional[UUID] = None,
    availability_threshold: Optional[float] = None,
    utilization_threshold: Optional[float] = None
) -> List[models.Resource]:
    """Get resources with filtering"""
    query = db.query(models.Resource).filter(
        models.Resource.tenant_id == tenant_id
    )
    
    if resource_type:
        query = query.filter(models.Resource.resource_type == resource_type)
    if deployment_status:
        query = query.filter(models.Resource.deployment_status == deployment_status)
    if criticality:
        query = query.filter(models.Resource.criticality == criticality)
    if strategic_importance:
        query = query.filter(models.Resource.strategic_importance == strategic_importance)
    if associated_capability_id:
        query = query.filter(models.Resource.associated_capability_id == associated_capability_id)
    if availability_threshold:
        query = query.filter(models.Resource.availability >= availability_threshold)
    if utilization_threshold:
        query = query.filter(models.Resource.utilization_rate >= utilization_threshold)
    
    return query.offset(skip).limit(limit).all()

def update_resource(
    db: Session, 
    resource: models.Resource, 
    resource_in: schemas.ResourceUpdate
) -> models.Resource:
    """Update resource"""
    update_data = resource_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(resource, field, value)
    
    # Update available quantity if quantity changed
    if 'quantity' in update_data:
        resource.available_quantity = resource.quantity - resource.allocated_quantity
    
    resource.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(resource)
    
    # Emit event
    emit_event("resource.updated", {
        "resource_id": str(resource.id),
        "tenant_id": str(resource.tenant_id)
    })
    
    return resource

def delete_resource(db: Session, resource: models.Resource):
    """Delete resource"""
    # Emit event before deletion
    emit_event("resource.deleted", {
        "resource_id": str(resource.id),
        "tenant_id": str(resource.tenant_id)
    })
    
    db.delete(resource)
    db.commit()

# Resource Link operations
def create_resource_link(
    db: Session, 
    link_in: schemas.ResourceLinkCreate, 
    resource_id: UUID, 
    user_id: UUID
) -> models.ResourceLink:
    """Create a resource link"""
    db_link = models.ResourceLink(
        **link_in.dict(),
        resource_id=resource_id,
        created_by=user_id
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    # Emit event
    emit_event("resource_link.created", {
        "link_id": str(db_link.id),
        "resource_id": str(resource_id),
        "user_id": str(user_id)
    })
    
    return db_link

def get_resource_link(db: Session, link_id: UUID, tenant_id: UUID) -> models.ResourceLink:
    """Get resource link by ID"""
    link = db.query(models.ResourceLink).join(models.Resource).filter(
        and_(
            models.ResourceLink.id == link_id,
            models.Resource.tenant_id == tenant_id
        )
    ).first()
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource link not found"
        )
    
    return link

def get_resource_links(db: Session, resource_id: UUID, tenant_id: UUID) -> List[models.ResourceLink]:
    """Get all links for a resource"""
    return db.query(models.ResourceLink).join(models.Resource).filter(
        and_(
            models.ResourceLink.resource_id == resource_id,
            models.Resource.tenant_id == tenant_id
        )
    ).all()

def update_resource_link(
    db: Session, 
    link: models.ResourceLink, 
    link_in: schemas.ResourceLinkUpdate
) -> models.ResourceLink:
    """Update resource link"""
    update_data = link_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(link, field, value)
    
    db.commit()
    db.refresh(link)
    
    # Emit event
    emit_event("resource_link.updated", {
        "link_id": str(link.id),
        "resource_id": str(link.resource_id)
    })
    
    return link

def delete_resource_link(db: Session, link: models.ResourceLink):
    """Delete resource link"""
    # Emit event before deletion
    emit_event("resource_link.deleted", {
        "link_id": str(link.id),
        "resource_id": str(link.resource_id)
    })
    
    db.delete(link)
    db.commit()

# Analysis and impact operations
def get_impact_score(db: Session, resource_id: UUID, tenant_id: UUID) -> schemas.ImpactScore:
    """Get impact score for resource"""
    resource = get_resource(db, resource_id, tenant_id)
    
    # Calculate impact scores
    strategic_impact_score = calculate_strategic_impact(resource)
    operational_impact_score = calculate_operational_impact(resource)
    financial_impact_score = calculate_financial_impact(resource)
    risk_impact_score = calculate_risk_impact(resource)
    
    # Overall impact score (weighted average)
    overall_impact_score = (
        strategic_impact_score * 0.3 +
        operational_impact_score * 0.3 +
        financial_impact_score * 0.2 +
        risk_impact_score * 0.2
    )
    
    # Impact factors
    impact_factors = identify_impact_factors(resource)
    
    # Recommendations
    recommendations = generate_impact_recommendations(resource, strategic_impact_score, operational_impact_score, financial_impact_score, risk_impact_score)
    
    return schemas.ImpactScore(
        resource_id=resource_id,
        strategic_impact_score=strategic_impact_score,
        operational_impact_score=operational_impact_score,
        financial_impact_score=financial_impact_score,
        risk_impact_score=risk_impact_score,
        overall_impact_score=overall_impact_score,
        impact_factors=impact_factors,
        recommendations=recommendations
    )

def get_allocation_map(db: Session, resource_id: UUID, tenant_id: UUID) -> schemas.AllocationMap:
    """Get allocation map for resource"""
    resource = get_resource(db, resource_id, tenant_id)
    
    # Get allocation breakdown
    links = get_resource_links(db, resource_id, tenant_id)
    allocation_breakdown = []
    total_allocated = 0.0
    
    for link in links:
        allocation = {
            "element_id": str(link.linked_element_id),
            "element_type": link.linked_element_type,
            "link_type": link.link_type,
            "allocation_percentage": link.allocation_percentage,
            "allocation_priority": link.allocation_priority,
            "performance_impact": link.performance_impact
        }
        allocation_breakdown.append(allocation)
        total_allocated += link.allocation_percentage
    
    # Utilization analysis
    utilization_analysis = analyze_utilization(resource, links)
    
    # Capacity planning
    capacity_planning = analyze_capacity(resource, links)
    
    # Optimization opportunities
    optimization_opportunities = identify_optimization_opportunities(resource, links)
    
    # Allocation metrics
    allocation_metrics = calculate_allocation_metrics(resource, links)
    
    return schemas.AllocationMap(
        resource_id=resource_id,
        total_allocated=total_allocated,
        allocation_breakdown=allocation_breakdown,
        utilization_analysis=utilization_analysis,
        capacity_planning=capacity_planning,
        optimization_opportunities=optimization_opportunities,
        allocation_metrics=allocation_metrics
    )

def analyze_resource(db: Session, resource_id: UUID, tenant_id: UUID) -> schemas.ResourceAnalysis:
    """Analyze resource for operational insights"""
    resource = get_resource(db, resource_id, tenant_id)
    
    # Performance analysis
    performance_analysis = analyze_performance(resource)
    
    # Cost analysis
    cost_analysis = analyze_costs(resource)
    
    # Utilization analysis
    utilization_analysis = analyze_utilization_detailed(resource)
    
    # Risk assessment
    risk_assessment = assess_risks(resource)
    
    # Optimization recommendations
    optimization_recommendations = generate_optimization_recommendations(resource)
    
    # Strategic alignment
    strategic_alignment = assess_strategic_alignment(resource)
    
    return schemas.ResourceAnalysis(
        resource_id=resource_id,
        performance_analysis=performance_analysis,
        cost_analysis=cost_analysis,
        utilization_analysis=utilization_analysis,
        risk_assessment=risk_assessment,
        optimization_recommendations=optimization_recommendations,
        strategic_alignment=strategic_alignment
    )

# Domain-specific query operations
def get_resources_by_type(db: Session, tenant_id: UUID, resource_type: str) -> List[models.Resource]:
    """Get resources by type"""
    return get_resources(db, tenant_id, resource_type=resource_type)

def get_resources_by_status(db: Session, tenant_id: UUID, deployment_status: str) -> List[models.Resource]:
    """Get resources by status"""
    return get_resources(db, tenant_id, deployment_status=deployment_status)

def get_resources_by_capability(db: Session, tenant_id: UUID, capability_id: UUID) -> List[models.Resource]:
    """Get resources by capability"""
    return get_resources(db, tenant_id, associated_capability_id=capability_id)

def get_resources_by_performance(db: Session, tenant_id: UUID, performance_threshold: float) -> List[models.Resource]:
    """Get resources by performance threshold"""
    return get_resources(db, tenant_id, utilization_threshold=performance_threshold)

def get_resources_by_element(db: Session, tenant_id: UUID, element_type: str, element_id: UUID) -> List[models.Resource]:
    """Get resources by linked element"""
    links = db.query(models.ResourceLink).join(models.Resource).filter(
        and_(
            models.ResourceLink.linked_element_type == element_type,
            models.ResourceLink.linked_element_id == element_id,
            models.Resource.tenant_id == tenant_id
        )
    ).all()
    
    resource_ids = [link.resource_id for link in links]
    return db.query(models.Resource).filter(
        and_(
            models.Resource.id.in_(resource_ids),
            models.Resource.tenant_id == tenant_id
        )
    ).all()

def get_active_resources(db: Session, tenant_id: UUID) -> List[models.Resource]:
    """Get active resources"""
    return get_resources(db, tenant_id, deployment_status="active")

def get_critical_resources(db: Session, tenant_id: UUID) -> List[models.Resource]:
    """Get critical resources"""
    return get_resources(db, tenant_id, criticality="critical")

# Helper functions for analysis
def calculate_strategic_impact(resource: models.Resource) -> float:
    """Calculate strategic impact score"""
    base_score = 0.0
    
    # Strategic importance impact
    importance_scores = {"low": 0.2, "medium": 0.5, "high": 0.8, "critical": 1.0}
    base_score += importance_scores.get(resource.strategic_importance, 0.5)
    
    # Business value impact
    value_scores = {"low": 0.2, "medium": 0.5, "high": 0.8, "critical": 1.0}
    base_score += value_scores.get(resource.business_value, 0.5)
    
    # Availability impact
    availability_impact = resource.availability / 100.0
    base_score += availability_impact * 0.3
    
    return min(base_score / 2.3, 1.0)

def calculate_operational_impact(resource: models.Resource) -> float:
    """Calculate operational impact score"""
    base_score = 0.0
    
    # Utilization impact
    utilization_impact = resource.utilization_rate / 100.0
    base_score += utilization_impact * 0.4
    
    # Efficiency impact
    base_score += resource.efficiency_score * 0.3
    
    # Effectiveness impact
    base_score += resource.effectiveness_score * 0.3
    
    return min(base_score, 1.0)

def calculate_financial_impact(resource: models.Resource) -> float:
    """Calculate financial impact score"""
    if not resource.total_cost:
        return 0.5  # Default score if no cost data
    
    # Simplified scoring based on cost
    if resource.total_cost < 10000:
        return 0.3
    elif resource.total_cost < 100000:
        return 0.6
    else:
        return 0.9

def calculate_risk_impact(resource: models.Resource) -> float:
    """Calculate risk impact score"""
    base_score = 0.0
    
    # Criticality impact
    criticality_scores = {"low": 0.2, "medium": 0.5, "high": 0.8, "critical": 1.0}
    base_score += criticality_scores.get(resource.criticality, 0.5)
    
    # Availability risk
    availability_risk = (100 - resource.availability) / 100.0
    base_score += availability_risk * 0.5
    
    return min(base_score, 1.0)

def identify_impact_factors(resource: models.Resource) -> List[Dict[str, Any]]:
    """Identify impact factors for resource"""
    factors = []
    
    # Strategic factors
    if resource.strategic_importance in ["high", "critical"]:
        factors.append({
            "type": "strategic",
            "factor": "high_strategic_importance",
            "impact": "high",
            "description": f"Resource has {resource.strategic_importance} strategic importance"
        })
    
    # Operational factors
    if resource.utilization_rate > 80:
        factors.append({
            "type": "operational",
            "factor": "high_utilization",
            "impact": "medium",
            "description": f"Resource utilization is {resource.utilization_rate}%"
        })
    
    # Financial factors
    if resource.total_cost and resource.total_cost > 100000:
        factors.append({
            "type": "financial",
            "factor": "high_cost",
            "impact": "high",
            "description": f"Resource cost is ${resource.total_cost:,.2f}"
        })
    
    # Risk factors
    if resource.criticality in ["high", "critical"]:
        factors.append({
            "type": "risk",
            "factor": "high_criticality",
            "impact": "high",
            "description": f"Resource has {resource.criticality} criticality"
        })
    
    return factors

def generate_impact_recommendations(resource: models.Resource, strategic_score: float, operational_score: float, financial_score: float, risk_score: float) -> List[str]:
    """Generate impact-based recommendations"""
    recommendations = []
    
    if strategic_score < 0.5:
        recommendations.append("Consider increasing strategic alignment")
        recommendations.append("Review business value contribution")
    
    if operational_score < 0.5:
        recommendations.append("Optimize resource utilization")
        recommendations.append("Improve efficiency and effectiveness")
    
    if financial_score > 0.8:
        recommendations.append("Review cost optimization opportunities")
        recommendations.append("Consider cost-benefit analysis")
    
    if risk_score > 0.7:
        recommendations.append("Implement risk mitigation strategies")
        recommendations.append("Enhance monitoring and alerting")
    
    if resource.availability < 95:
        recommendations.append("Improve resource availability")
        recommendations.append("Implement redundancy strategies")
    
    return recommendations

def analyze_utilization(resource: models.Resource, links: List[models.ResourceLink]) -> Dict[str, Any]:
    """Analyze resource utilization"""
    total_allocation = sum(link.allocation_percentage for link in links)
    
    return {
        "current_utilization": resource.utilization_rate,
        "total_allocation": total_allocation,
        "available_capacity": 100 - total_allocation,
        "utilization_efficiency": resource.efficiency_score,
        "utilization_effectiveness": resource.effectiveness_score,
        "allocation_count": len(links)
    }

def analyze_capacity(resource: models.Resource, links: List[models.ResourceLink]) -> Dict[str, Any]:
    """Analyze resource capacity"""
    total_allocation = sum(link.allocation_percentage for link in links)
    
    return {
        "total_capacity": resource.quantity,
        "allocated_capacity": resource.allocated_quantity,
        "available_capacity": resource.available_quantity,
        "allocation_percentage": (resource.allocated_quantity / resource.quantity) * 100 if resource.quantity > 0 else 0,
        "capacity_utilization": total_allocation,
        "capacity_planning_recommendations": generate_capacity_recommendations(resource, total_allocation)
    }

def identify_optimization_opportunities(resource: models.Resource, links: List[models.ResourceLink]) -> List[str]:
    """Identify optimization opportunities"""
    opportunities = []
    
    total_allocation = sum(link.allocation_percentage for link in links)
    
    if total_allocation > 100:
        opportunities.append("Resource overallocation detected - review allocations")
    
    if resource.utilization_rate < 50:
        opportunities.append("Low utilization - consider resource consolidation")
    
    if resource.efficiency_score < 0.6:
        opportunities.append("Low efficiency - implement process improvements")
    
    if resource.availability < 95:
        opportunities.append("Low availability - implement redundancy")
    
    if resource.total_cost and resource.total_cost > 100000:
        opportunities.append("High cost - review cost optimization opportunities")
    
    return opportunities

def calculate_allocation_metrics(resource: models.Resource, links: List[models.ResourceLink]) -> Dict[str, Any]:
    """Calculate allocation metrics"""
    total_allocation = sum(link.allocation_percentage for link in links)
    high_priority_allocations = sum(link.allocation_percentage for link in links if link.allocation_priority in ["high", "critical"])
    
    return {
        "total_allocation_percentage": total_allocation,
        "high_priority_allocation_percentage": high_priority_allocations,
        "allocation_count": len(links),
        "average_allocation_percentage": total_allocation / len(links) if links else 0,
        "allocation_efficiency": min(total_allocation / 100.0, 1.0) if total_allocation > 0 else 0
    }

def analyze_performance(resource: models.Resource) -> Dict[str, Any]:
    """Analyze resource performance"""
    return {
        "efficiency_score": resource.efficiency_score,
        "effectiveness_score": resource.effectiveness_score,
        "utilization_rate": resource.utilization_rate,
        "availability": resource.availability,
        "performance_category": categorize_performance(resource),
        "performance_trends": "stable",  # Placeholder for trend analysis
        "performance_recommendations": generate_performance_recommendations(resource)
    }

def analyze_costs(resource: models.Resource) -> Dict[str, Any]:
    """Analyze resource costs"""
    return {
        "cost_per_unit": resource.cost_per_unit,
        "total_cost": resource.total_cost,
        "budget_allocation": resource.budget_allocation,
        "cost_center": resource.cost_center,
        "cost_efficiency": calculate_cost_efficiency(resource),
        "cost_recommendations": generate_cost_recommendations(resource)
    }

def analyze_utilization_detailed(resource: models.Resource) -> Dict[str, Any]:
    """Detailed utilization analysis"""
    return {
        "current_utilization": resource.utilization_rate,
        "available_quantity": resource.available_quantity,
        "allocated_quantity": resource.allocated_quantity,
        "utilization_efficiency": resource.efficiency_score,
        "utilization_effectiveness": resource.effectiveness_score,
        "utilization_recommendations": generate_utilization_recommendations(resource)
    }

def assess_risks(resource: models.Resource) -> Dict[str, Any]:
    """Assess resource risks"""
    return {
        "criticality_level": resource.criticality,
        "availability_risk": 100 - resource.availability,
        "utilization_risk": max(0, resource.utilization_rate - 90),
        "cost_risk": calculate_cost_risk(resource),
        "risk_factors": identify_risk_factors(resource),
        "risk_recommendations": generate_risk_recommendations(resource)
    }

def generate_optimization_recommendations(resource: models.Resource) -> List[str]:
    """Generate optimization recommendations"""
    recommendations = []
    
    if resource.utilization_rate < 50:
        recommendations.append("Consider resource consolidation")
    
    if resource.efficiency_score < 0.6:
        recommendations.append("Implement process improvements")
    
    if resource.availability < 95:
        recommendations.append("Implement redundancy strategies")
    
    if resource.total_cost and resource.total_cost > 100000:
        recommendations.append("Review cost optimization opportunities")
    
    return recommendations

def assess_strategic_alignment(resource: models.Resource) -> Dict[str, Any]:
    """Assess strategic alignment"""
    return {
        "strategic_importance": resource.strategic_importance,
        "business_value": resource.business_value,
        "alignment_score": calculate_strategic_alignment_score(resource),
        "alignment_factors": identify_alignment_factors(resource),
        "alignment_recommendations": generate_alignment_recommendations(resource)
    }

# Helper functions for detailed analysis
def categorize_performance(resource: models.Resource) -> str:
    """Categorize resource performance"""
    if resource.efficiency_score >= 0.8 and resource.effectiveness_score >= 0.8:
        return "excellent"
    elif resource.efficiency_score >= 0.6 and resource.effectiveness_score >= 0.6:
        return "good"
    elif resource.efficiency_score >= 0.4 and resource.effectiveness_score >= 0.4:
        return "fair"
    else:
        return "poor"

def generate_performance_recommendations(resource: models.Resource) -> List[str]:
    """Generate performance recommendations"""
    recommendations = []
    
    if resource.efficiency_score < 0.6:
        recommendations.append("Improve operational efficiency")
    
    if resource.effectiveness_score < 0.6:
        recommendations.append("Enhance effectiveness measures")
    
    if resource.utilization_rate < 50:
        recommendations.append("Increase resource utilization")
    
    return recommendations

def calculate_cost_efficiency(resource: models.Resource) -> float:
    """Calculate cost efficiency"""
    if not resource.total_cost or resource.total_cost <= 0:
        return 0.5
    
    # Simplified cost efficiency calculation
    if resource.total_cost < 10000:
        return 0.9
    elif resource.total_cost < 100000:
        return 0.7
    else:
        return 0.4

def generate_cost_recommendations(resource: models.Resource) -> List[str]:
    """Generate cost recommendations"""
    recommendations = []
    
    if resource.total_cost and resource.total_cost > 100000:
        recommendations.append("Review cost optimization opportunities")
        recommendations.append("Consider cost-benefit analysis")
    
    return recommendations

def generate_utilization_recommendations(resource: models.Resource) -> List[str]:
    """Generate utilization recommendations"""
    recommendations = []
    
    if resource.utilization_rate < 50:
        recommendations.append("Increase resource utilization")
        recommendations.append("Consider resource consolidation")
    
    if resource.utilization_rate > 90:
        recommendations.append("Monitor for potential overload")
        recommendations.append("Consider capacity expansion")
    
    return recommendations

def calculate_cost_risk(resource: models.Resource) -> float:
    """Calculate cost risk"""
    if not resource.total_cost:
        return 0.0
    
    if resource.total_cost > 100000:
        return 0.8
    elif resource.total_cost > 50000:
        return 0.5
    else:
        return 0.2

def identify_risk_factors(resource: models.Resource) -> List[Dict[str, Any]]:
    """Identify risk factors"""
    factors = []
    
    if resource.criticality in ["high", "critical"]:
        factors.append({
            "type": "criticality",
            "level": resource.criticality,
            "description": f"Resource has {resource.criticality} criticality"
        })
    
    if resource.availability < 95:
        factors.append({
            "type": "availability",
            "level": "medium",
            "description": f"Low availability: {resource.availability}%"
        })
    
    if resource.total_cost and resource.total_cost > 100000:
        factors.append({
            "type": "cost",
            "level": "high",
            "description": f"High cost: ${resource.total_cost:,.2f}"
        })
    
    return factors

def generate_risk_recommendations(resource: models.Resource) -> List[str]:
    """Generate risk recommendations"""
    recommendations = []
    
    if resource.criticality in ["high", "critical"]:
        recommendations.append("Implement redundancy strategies")
        recommendations.append("Enhance monitoring and alerting")
    
    if resource.availability < 95:
        recommendations.append("Improve availability measures")
        recommendations.append("Implement backup systems")
    
    return recommendations

def calculate_strategic_alignment_score(resource: models.Resource) -> float:
    """Calculate strategic alignment score"""
    base_score = 0.0
    
    importance_scores = {"low": 0.2, "medium": 0.5, "high": 0.8, "critical": 1.0}
    base_score += importance_scores.get(resource.strategic_importance, 0.5)
    
    value_scores = {"low": 0.2, "medium": 0.5, "high": 0.8, "critical": 1.0}
    base_score += value_scores.get(resource.business_value, 0.5)
    
    return min(base_score / 2.0, 1.0)

def identify_alignment_factors(resource: models.Resource) -> List[Dict[str, Any]]:
    """Identify alignment factors"""
    factors = []
    
    if resource.strategic_importance in ["high", "critical"]:
        factors.append({
            "type": "strategic_importance",
            "level": resource.strategic_importance,
            "description": f"High strategic importance: {resource.strategic_importance}"
        })
    
    if resource.business_value in ["high", "critical"]:
        factors.append({
            "type": "business_value",
            "level": resource.business_value,
            "description": f"High business value: {resource.business_value}"
        })
    
    return factors

def generate_alignment_recommendations(resource: models.Resource) -> List[str]:
    """Generate alignment recommendations"""
    recommendations = []
    
    if resource.strategic_importance == "low":
        recommendations.append("Review strategic importance alignment")
    
    if resource.business_value == "low":
        recommendations.append("Assess business value contribution")
    
    return recommendations

def generate_capacity_recommendations(resource: models.Resource, total_allocation: float) -> List[str]:
    """Generate capacity planning recommendations"""
    recommendations = []
    
    if total_allocation > 100:
        recommendations.append("Resource is overallocated - review allocations")
    
    if total_allocation < 50:
        recommendations.append("Consider increasing resource utilization")
    
    if resource.available_quantity < resource.quantity * 0.1:
        recommendations.append("Consider capacity expansion")
    
    return recommendations 