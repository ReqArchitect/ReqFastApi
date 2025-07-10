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
        redis_client.publish("application_function_events", json.dumps(event))
    except Exception as e:
        # Log error but don't fail the operation
        print(f"Failed to emit event: {e}")

# Application Function CRUD operations
def create_application_function(
    db: Session, 
    function_in: schemas.ApplicationFunctionCreate, 
    tenant_id: UUID, 
    user_id: UUID
) -> models.ApplicationFunction:
    """Create a new application function"""
    db_function = models.ApplicationFunction(
        **function_in.dict(),
        tenant_id=tenant_id,
        user_id=user_id
    )
    db.add(db_function)
    db.commit()
    db.refresh(db_function)
    
    # Emit event
    emit_event("application_function.created", {
        "function_id": str(db_function.id),
        "tenant_id": str(tenant_id),
        "user_id": str(user_id)
    })
    
    return db_function

def get_application_function(db: Session, function_id: UUID, tenant_id: UUID) -> models.ApplicationFunction:
    """Get application function by ID"""
    function = db.query(models.ApplicationFunction).filter(
        and_(
            models.ApplicationFunction.id == function_id,
            models.ApplicationFunction.tenant_id == tenant_id
        )
    ).first()
    
    if not function:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application function not found"
        )
    
    return function

def get_application_functions(
    db: Session,
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    function_type: Optional[str] = None,
    status: Optional[str] = None,
    business_criticality: Optional[str] = None,
    business_value: Optional[str] = None,
    supported_business_function_id: Optional[UUID] = None,
    technology_stack: Optional[str] = None,
    performance_threshold: Optional[float] = None
) -> List[models.ApplicationFunction]:
    """Get application functions with filtering"""
    query = db.query(models.ApplicationFunction).filter(
        models.ApplicationFunction.tenant_id == tenant_id
    )
    
    if function_type:
        query = query.filter(models.ApplicationFunction.function_type == function_type)
    if status:
        query = query.filter(models.ApplicationFunction.status == status)
    if business_criticality:
        query = query.filter(models.ApplicationFunction.business_criticality == business_criticality)
    if business_value:
        query = query.filter(models.ApplicationFunction.business_value == business_value)
    if supported_business_function_id:
        query = query.filter(models.ApplicationFunction.supported_business_function_id == supported_business_function_id)
    if technology_stack:
        query = query.filter(models.ApplicationFunction.technology_stack.contains(technology_stack))
    if performance_threshold:
        query = query.filter(models.ApplicationFunction.current_availability >= performance_threshold)
    
    return query.offset(skip).limit(limit).all()

def update_application_function(
    db: Session, 
    function: models.ApplicationFunction, 
    function_in: schemas.ApplicationFunctionUpdate
) -> models.ApplicationFunction:
    """Update application function"""
    update_data = function_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(function, field, value)
    
    function.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(function)
    
    # Emit event
    emit_event("application_function.updated", {
        "function_id": str(function.id),
        "tenant_id": str(function.tenant_id)
    })
    
    return function

def delete_application_function(db: Session, function: models.ApplicationFunction):
    """Delete application function"""
    # Emit event before deletion
    emit_event("application_function.deleted", {
        "function_id": str(function.id),
        "tenant_id": str(function.tenant_id)
    })
    
    db.delete(function)
    db.commit()

# Function Link operations
def create_function_link(
    db: Session, 
    link_in: schemas.FunctionLinkCreate, 
    function_id: UUID, 
    user_id: UUID
) -> models.FunctionLink:
    """Create a function link"""
    db_link = models.FunctionLink(
        **link_in.dict(),
        application_function_id=function_id,
        created_by=user_id
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    # Emit event
    emit_event("function_link.created", {
        "link_id": str(db_link.id),
        "function_id": str(function_id),
        "user_id": str(user_id)
    })
    
    return db_link

def get_function_link(db: Session, link_id: UUID, tenant_id: UUID) -> models.FunctionLink:
    """Get function link by ID"""
    link = db.query(models.FunctionLink).join(models.ApplicationFunction).filter(
        and_(
            models.FunctionLink.id == link_id,
            models.ApplicationFunction.tenant_id == tenant_id
        )
    ).first()
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Function link not found"
        )
    
    return link

def get_function_links(db: Session, function_id: UUID, tenant_id: UUID) -> List[models.FunctionLink]:
    """Get all links for a function"""
    return db.query(models.FunctionLink).join(models.ApplicationFunction).filter(
        and_(
            models.FunctionLink.application_function_id == function_id,
            models.ApplicationFunction.tenant_id == tenant_id
        )
    ).all()

def update_function_link(
    db: Session, 
    link: models.FunctionLink, 
    link_in: schemas.FunctionLinkUpdate
) -> models.FunctionLink:
    """Update function link"""
    update_data = link_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(link, field, value)
    
    db.commit()
    db.refresh(link)
    
    # Emit event
    emit_event("function_link.updated", {
        "link_id": str(link.id),
        "function_id": str(link.application_function_id)
    })
    
    return link

def delete_function_link(db: Session, link: models.FunctionLink):
    """Delete function link"""
    # Emit event before deletion
    emit_event("function_link.deleted", {
        "link_id": str(link.id),
        "function_id": str(link.application_function_id)
    })
    
    db.delete(link)
    db.commit()

# Analysis and impact operations
def get_impact_map(db: Session, function_id: UUID, tenant_id: UUID) -> schemas.ImpactMap:
    """Get impact map for application function"""
    function = get_application_function(db, function_id, tenant_id)
    
    # Get direct impacts through links
    direct_links = get_function_links(db, function_id, tenant_id)
    direct_impacts = []
    
    for link in direct_links:
        impact = {
            "element_id": str(link.linked_element_id),
            "element_type": link.linked_element_type,
            "link_type": link.link_type,
            "relationship_strength": link.relationship_strength,
            "dependency_level": link.dependency_level,
            "performance_impact": link.performance_impact
        }
        direct_impacts.append(impact)
    
    # Calculate indirect impacts (simplified)
    indirect_impacts = []
    
    # Risk assessment
    risk_assessment = {
        "business_criticality": function.business_criticality,
        "business_value": function.business_value,
        "security_level": function.security_level,
        "availability_risk": 100 - function.current_availability,
        "dependency_count": len(direct_links)
    }
    
    # Dependency chain
    dependency_chain = []
    for link in direct_links:
        if link.dependency_level in ["high", "medium"]:
            dependency_chain.append({
                "element_id": str(link.linked_element_id),
                "element_type": link.linked_element_type,
                "dependency_level": link.dependency_level
            })
    
    # Calculate total impact score
    total_impact_score = calculate_impact_score(function, direct_impacts, indirect_impacts)
    
    return schemas.ImpactMap(
        function_id=function_id,
        direct_impacts=direct_impacts,
        indirect_impacts=indirect_impacts,
        risk_assessment=risk_assessment,
        dependency_chain=dependency_chain,
        total_impact_score=total_impact_score
    )

def get_performance_score(db: Session, function_id: UUID, tenant_id: UUID) -> schemas.PerformanceScore:
    """Get performance score for application function"""
    function = get_application_function(db, function_id, tenant_id)
    
    # Calculate performance scores
    response_time_score = calculate_response_time_score(function)
    throughput_score = calculate_throughput_score(function)
    availability_score = function.current_availability / 100.0
    
    # Overall score (weighted average)
    overall_score = (response_time_score * 0.3 + throughput_score * 0.3 + availability_score * 0.4)
    
    # Generate recommendations
    recommendations = generate_performance_recommendations(function, response_time_score, throughput_score, availability_score)
    
    # Performance metrics
    performance_metrics = {
        "response_time_target": function.response_time_target,
        "throughput_target": function.throughput_target,
        "availability_target": function.availability_target,
        "current_availability": function.current_availability,
        "function_type": function.function_type,
        "operational_hours": function.operational_hours
    }
    
    return schemas.PerformanceScore(
        function_id=function_id,
        response_time_score=response_time_score,
        throughput_score=throughput_score,
        availability_score=availability_score,
        overall_score=overall_score,
        recommendations=recommendations,
        performance_metrics=performance_metrics
    )

def analyze_application_function(db: Session, function_id: UUID, tenant_id: UUID) -> schemas.ApplicationFunctionAnalysis:
    """Analyze application function for operational insights"""
    function = get_application_function(db, function_id, tenant_id)
    
    # Operational health assessment
    operational_health = assess_operational_health(function)
    
    # Business alignment assessment
    business_alignment = assess_business_alignment(function)
    
    # Technical debt assessment
    technical_debt = assess_technical_debt(function)
    
    # Risk factors
    risk_factors = identify_risk_factors(function)
    
    # Improvement opportunities
    improvement_opportunities = identify_improvement_opportunities(function)
    
    # Compliance status
    compliance_status = assess_compliance_status(function)
    
    return schemas.ApplicationFunctionAnalysis(
        function_id=function_id,
        operational_health=operational_health,
        business_alignment=business_alignment,
        technical_debt=technical_debt,
        risk_factors=risk_factors,
        improvement_opportunities=improvement_opportunities,
        compliance_status=compliance_status
    )

# Domain-specific query operations
def get_application_functions_by_type(db: Session, tenant_id: UUID, function_type: str) -> List[models.ApplicationFunction]:
    """Get application functions by type"""
    return get_application_functions(db, tenant_id, function_type=function_type)

def get_application_functions_by_status(db: Session, tenant_id: UUID, status: str) -> List[models.ApplicationFunction]:
    """Get application functions by status"""
    return get_application_functions(db, tenant_id, status=status)

def get_application_functions_by_business_function(db: Session, tenant_id: UUID, business_function_id: UUID) -> List[models.ApplicationFunction]:
    """Get application functions by business function"""
    return get_application_functions(db, tenant_id, supported_business_function_id=business_function_id)

def get_application_functions_by_performance(db: Session, tenant_id: UUID, performance_threshold: float) -> List[models.ApplicationFunction]:
    """Get application functions by performance threshold"""
    return get_application_functions(db, tenant_id, performance_threshold=performance_threshold)

def get_application_functions_by_element(db: Session, tenant_id: UUID, element_type: str, element_id: UUID) -> List[models.ApplicationFunction]:
    """Get application functions by linked element"""
    links = db.query(models.FunctionLink).join(models.ApplicationFunction).filter(
        and_(
            models.FunctionLink.linked_element_type == element_type,
            models.FunctionLink.linked_element_id == element_id,
            models.ApplicationFunction.tenant_id == tenant_id
        )
    ).all()
    
    function_ids = [link.application_function_id for link in links]
    return db.query(models.ApplicationFunction).filter(
        and_(
            models.ApplicationFunction.id.in_(function_ids),
            models.ApplicationFunction.tenant_id == tenant_id
        )
    ).all()

def get_active_application_functions(db: Session, tenant_id: UUID) -> List[models.ApplicationFunction]:
    """Get active application functions"""
    return get_application_functions(db, tenant_id, status="active")

def get_critical_application_functions(db: Session, tenant_id: UUID) -> List[models.ApplicationFunction]:
    """Get critical application functions"""
    return get_application_functions(db, tenant_id, business_criticality="critical")

# Helper functions for analysis
def calculate_impact_score(function: models.ApplicationFunction, direct_impacts: List[Dict], indirect_impacts: List[Dict]) -> float:
    """Calculate total impact score"""
    base_score = 0.0
    
    # Business criticality impact
    criticality_scores = {"low": 0.1, "medium": 0.3, "high": 0.6, "critical": 1.0}
    base_score += criticality_scores.get(function.business_criticality, 0.3)
    
    # Business value impact
    value_scores = {"low": 0.1, "medium": 0.3, "high": 0.6, "critical": 1.0}
    base_score += value_scores.get(function.business_value, 0.3)
    
    # Availability impact
    availability_impact = (100 - function.current_availability) / 100.0
    base_score += availability_impact * 0.5
    
    # Dependency impact
    dependency_impact = len(direct_impacts) * 0.1
    base_score += min(dependency_impact, 0.5)
    
    return min(base_score, 1.0)

def calculate_response_time_score(function: models.ApplicationFunction) -> float:
    """Calculate response time score"""
    if not function.response_time_target:
        return 0.8  # Default score if no target set
    
    # Simplified scoring - in real implementation, would compare actual vs target
    return 0.85

def calculate_throughput_score(function: models.ApplicationFunction) -> float:
    """Calculate throughput score"""
    if not function.throughput_target:
        return 0.8  # Default score if no target set
    
    # Simplified scoring - in real implementation, would compare actual vs target
    return 0.9

def generate_performance_recommendations(function: models.ApplicationFunction, response_time_score: float, throughput_score: float, availability_score: float) -> List[str]:
    """Generate performance recommendations"""
    recommendations = []
    
    if availability_score < 0.95:
        recommendations.append("Consider implementing high availability patterns")
        recommendations.append("Review monitoring and alerting configuration")
    
    if response_time_score < 0.8:
        recommendations.append("Optimize database queries and caching")
        recommendations.append("Consider implementing async processing")
    
    if throughput_score < 0.8:
        recommendations.append("Implement horizontal scaling")
        recommendations.append("Review resource allocation")
    
    if function.security_level == "basic":
        recommendations.append("Upgrade security level to standard or higher")
    
    if not function.monitoring_config:
        recommendations.append("Implement comprehensive monitoring")
    
    return recommendations

def assess_operational_health(function: models.ApplicationFunction) -> Dict[str, Any]:
    """Assess operational health"""
    health_score = 0.0
    issues = []
    
    # Availability health
    if function.current_availability < function.availability_target:
        health_score += 0.3
        issues.append("Below availability target")
    else:
        health_score += 0.8
    
    # Security health
    if function.security_level in ["basic"]:
        health_score += 0.4
        issues.append("Basic security level")
    else:
        health_score += 0.8
    
    # Monitoring health
    if not function.monitoring_config:
        health_score += 0.2
        issues.append("No monitoring configured")
    else:
        health_score += 0.8
    
    return {
        "overall_score": health_score / 3.0,
        "issues": issues,
        "status": "healthy" if health_score / 3.0 > 0.7 else "needs_attention"
    }

def assess_business_alignment(function: models.ApplicationFunction) -> Dict[str, Any]:
    """Assess business alignment"""
    alignment_score = 0.0
    
    # Business function alignment
    if function.supported_business_function_id:
        alignment_score += 0.4
    else:
        alignment_score += 0.1
    
    # Business criticality alignment
    if function.business_criticality in ["high", "critical"]:
        alignment_score += 0.3
    else:
        alignment_score += 0.1
    
    # Business value alignment
    if function.business_value in ["high", "critical"]:
        alignment_score += 0.3
    else:
        alignment_score += 0.1
    
    return {
        "alignment_score": alignment_score,
        "has_business_function": bool(function.supported_business_function_id),
        "business_criticality": function.business_criticality,
        "business_value": function.business_value
    }

def assess_technical_debt(function: models.ApplicationFunction) -> Dict[str, Any]:
    """Assess technical debt"""
    debt_score = 0.0
    debt_items = []
    
    # Technology stack debt
    if not function.technology_stack:
        debt_score += 0.2
        debt_items.append("No technology stack documented")
    
    # Documentation debt
    if not function.description or not function.purpose:
        debt_score += 0.2
        debt_items.append("Incomplete documentation")
    
    # Monitoring debt
    if not function.monitoring_config:
        debt_score += 0.3
        debt_items.append("No monitoring configuration")
    
    # Security debt
    if function.security_level == "basic":
        debt_score += 0.3
        debt_items.append("Basic security level")
    
    return {
        "debt_score": debt_score,
        "debt_items": debt_items,
        "priority": "high" if debt_score > 0.5 else "medium" if debt_score > 0.2 else "low"
    }

def identify_risk_factors(function: models.ApplicationFunction) -> List[Dict[str, Any]]:
    """Identify risk factors"""
    risks = []
    
    # Availability risk
    if function.current_availability < function.availability_target:
        risks.append({
            "type": "availability",
            "severity": "high",
            "description": f"Current availability {function.current_availability}% below target {function.availability_target}%"
        })
    
    # Security risk
    if function.security_level == "basic":
        risks.append({
            "type": "security",
            "severity": "medium",
            "description": "Basic security level may not be sufficient"
        })
    
    # Business criticality risk
    if function.business_criticality == "critical" and function.current_availability < 99.0:
        risks.append({
            "type": "business_criticality",
            "severity": "critical",
            "description": "Critical business function with low availability"
        })
    
    return risks

def identify_improvement_opportunities(function: models.ApplicationFunction) -> List[str]:
    """Identify improvement opportunities"""
    opportunities = []
    
    if not function.monitoring_config:
        opportunities.append("Implement comprehensive monitoring and alerting")
    
    if function.security_level == "basic":
        opportunities.append("Upgrade security controls and access management")
    
    if not function.technology_stack:
        opportunities.append("Document technology stack and dependencies")
    
    if not function.api_endpoints:
        opportunities.append("Document API endpoints and interfaces")
    
    if function.operational_hours == "business_hours" and function.business_criticality in ["high", "critical"]:
        opportunities.append("Consider 24x7 operational model for critical function")
    
    return opportunities

def assess_compliance_status(function: models.ApplicationFunction) -> Dict[str, Any]:
    """Assess compliance status"""
    compliance_items = []
    non_compliant_items = []
    
    # Security compliance
    if function.security_level in ["standard", "high", "critical"]:
        compliance_items.append("security_level")
    else:
        non_compliant_items.append("security_level")
    
    # Monitoring compliance
    if function.monitoring_config:
        compliance_items.append("monitoring")
    else:
        non_compliant_items.append("monitoring")
    
    # Documentation compliance
    if function.description and function.purpose:
        compliance_items.append("documentation")
    else:
        non_compliant_items.append("documentation")
    
    compliance_rate = len(compliance_items) / (len(compliance_items) + len(non_compliant_items))
    
    return {
        "compliance_rate": compliance_rate,
        "compliant_items": compliance_items,
        "non_compliant_items": non_compliant_items,
        "status": "compliant" if compliance_rate >= 0.8 else "needs_attention"
    } 