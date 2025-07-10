# API Reference: resource_service

## Overview

The Resource Service provides comprehensive management of ArchiMate 3.2 Resource elements in the Strategy Layer with full CRUD operations, relationship management, analysis capabilities, and domain-specific queries.

## Base URL

```
http://localhost:8080
```

## Authentication

All endpoints require JWT authentication with the following header:
```
Authorization: Bearer <jwt_token>
```

Required JWT claims:
- `tenant_id`: UUID of the tenant
- `user_id`: UUID of the user
- `role`: User role (Owner, Admin, Editor, Viewer)

## Resource Management

### Create Resource

**POST** `/api/v1/resources`

Creates a new Resource.

**Request Body:**
```json
{
  "name": "Enterprise Architect",
  "description": "Senior enterprise architect with 10+ years experience",
  "resource_type": "human",
  "quantity": 2.0,
  "unit_of_measure": "FTE",
  "availability": 95.0,
  "location": "Headquarters",
  "deployment_status": "active",
  "criticality": "high",
  "strategic_importance": "high",
  "business_value": "high",
  "cost_per_unit": 150000.0,
  "total_cost": 300000.0,
  "budget_allocation": 300000.0,
  "cost_center": "IT-ARCH",
  "skills_required": "{\"enterprise_architecture\": \"expert\", \"togaf\": \"certified\", \"archimate\": \"proficient\"}",
  "capabilities_provided": "{\"strategic_planning\": true, \"architecture_governance\": true, \"technology_roadmapping\": true}",
  "expertise_level": "expert",
  "performance_metrics": "{\"projects_delivered\": 15, \"stakeholder_satisfaction\": 4.5}",
  "utilization_rate": 85.0,
  "efficiency_score": 0.9,
  "effectiveness_score": 0.85,
  "operational_hours": "business_hours",
  "maintenance_schedule": "Quarterly reviews",
  "technology_stack": "{\"tools\": [\"Sparx EA\", \"ArchiMate\", \"Visio\"]}",
  "system_requirements": "{\"hardware\": \"High-end workstation\", \"software\": \"Enterprise architecture tools\"}",
  "integration_points": "{\"portfolio_management\": \"PPM system\", \"governance\": \"GRC platform\"}",
  "dependencies": "{\"business_units\": \"Stakeholder engagement\", \"technology_teams\": \"Implementation support\"}",
  "governance_model": "enhanced",
  "compliance_requirements": "{\"sox\": true, \"gdpr\": true}",
  "audit_requirements": "{\"quarterly_reviews\": true, \"annual_assessments\": true}",
  "risk_assessment": "{\"key_person_risk\": \"medium\", \"knowledge_transfer\": \"planned\"}",
  "parent_resource_id": null,
  "associated_capability_id": "550e8400-e29b-41d4-a716-446655440001",
  "business_function_id": "550e8400-e29b-41d4-a716-446655440002",
  "application_component_id": null,
  "node_id": null
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "name": "Enterprise Architect",
  "description": "Senior enterprise architect with 10+ years experience",
  "resource_type": "human",
  "quantity": 2.0,
  "unit_of_measure": "FTE",
  "availability": 95.0,
  "allocated_quantity": 0.0,
  "available_quantity": 2.0,
  "location": "Headquarters",
  "deployment_status": "active",
  "criticality": "high",
  "strategic_importance": "high",
  "business_value": "high",
  "cost_per_unit": 150000.0,
  "total_cost": 300000.0,
  "budget_allocation": 300000.0,
  "cost_center": "IT-ARCH",
  "skills_required": "{\"enterprise_architecture\": \"expert\", \"togaf\": \"certified\", \"archimate\": \"proficient\"}",
  "capabilities_provided": "{\"strategic_planning\": true, \"architecture_governance\": true, \"technology_roadmapping\": true}",
  "expertise_level": "expert",
  "performance_metrics": "{\"projects_delivered\": 15, \"stakeholder_satisfaction\": 4.5}",
  "utilization_rate": 85.0,
  "efficiency_score": 0.9,
  "effectiveness_score": 0.85,
  "operational_hours": "business_hours",
  "maintenance_schedule": "Quarterly reviews",
  "technology_stack": "{\"tools\": [\"Sparx EA\", \"ArchiMate\", \"Visio\"]}",
  "system_requirements": "{\"hardware\": \"High-end workstation\", \"software\": \"Enterprise architecture tools\"}",
  "integration_points": "{\"portfolio_management\": \"PPM system\", \"governance\": \"GRC platform\"}",
  "dependencies": "{\"business_units\": \"Stakeholder engagement\", \"technology_teams\": \"Implementation support\"}",
  "governance_model": "enhanced",
  "compliance_requirements": "{\"sox\": true, \"gdpr\": true}",
  "audit_requirements": "{\"quarterly_reviews\": true, \"annual_assessments\": true}",
  "risk_assessment": "{\"key_person_risk\": \"medium\", \"knowledge_transfer\": \"planned\"}",
  "parent_resource_id": null,
  "associated_capability_id": "550e8400-e29b-41d4-a716-446655440001",
  "business_function_id": "550e8400-e29b-41d4-a716-446655440002",
  "application_component_id": null,
  "node_id": null,
  "last_maintenance": null,
  "next_maintenance": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### List Resources

**GET** `/api/v1/resources`

Lists all Resources for the tenant with filtering and pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)
- `resource_type` (string, optional): Filter by resource type
- `deployment_status` (string, optional): Filter by deployment status
- `criticality` (string, optional): Filter by criticality
- `strategic_importance` (string, optional): Filter by strategic importance
- `associated_capability_id` (UUID, optional): Filter by associated capability
- `availability_threshold` (float, optional): Filter by minimum availability
- `utilization_threshold` (float, optional): Filter by minimum utilization

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440002",
    "name": "Enterprise Architect",
    "description": "Senior enterprise architect with 10+ years experience",
    "resource_type": "human",
    "quantity": 2.0,
    "unit_of_measure": "FTE",
    "availability": 95.0,
    "allocated_quantity": 0.0,
    "available_quantity": 2.0,
    "location": "Headquarters",
    "deployment_status": "active",
    "criticality": "high",
    "strategic_importance": "high",
    "business_value": "high",
    "cost_per_unit": 150000.0,
    "total_cost": 300000.0,
    "budget_allocation": 300000.0,
    "cost_center": "IT-ARCH",
    "skills_required": "{\"enterprise_architecture\": \"expert\", \"togaf\": \"certified\", \"archimate\": \"proficient\"}",
    "capabilities_provided": "{\"strategic_planning\": true, \"architecture_governance\": true, \"technology_roadmapping\": true}",
    "expertise_level": "expert",
    "performance_metrics": "{\"projects_delivered\": 15, \"stakeholder_satisfaction\": 4.5}",
    "utilization_rate": 85.0,
    "efficiency_score": 0.9,
    "effectiveness_score": 0.85,
    "operational_hours": "business_hours",
    "maintenance_schedule": "Quarterly reviews",
    "technology_stack": "{\"tools\": [\"Sparx EA\", \"ArchiMate\", \"Visio\"]}",
    "system_requirements": "{\"hardware\": \"High-end workstation\", \"software\": \"Enterprise architecture tools\"}",
    "integration_points": "{\"portfolio_management\": \"PPM system\", \"governance\": \"GRC platform\"}",
    "dependencies": "{\"business_units\": \"Stakeholder engagement\", \"technology_teams\": \"Implementation support\"}",
    "governance_model": "enhanced",
    "compliance_requirements": "{\"sox\": true, \"gdpr\": true}",
    "audit_requirements": "{\"quarterly_reviews\": true, \"annual_assessments\": true}",
    "risk_assessment": "{\"key_person_risk\": \"medium\", \"knowledge_transfer\": \"planned\"}",
    "parent_resource_id": null,
    "associated_capability_id": "550e8400-e29b-41d4-a716-446655440001",
    "business_function_id": "550e8400-e29b-41d4-a716-446655440002",
    "application_component_id": null,
    "node_id": null,
    "last_maintenance": null,
    "next_maintenance": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Resource

**GET** `/api/v1/resources/{resource_id}`

Retrieves a Resource by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "name": "Enterprise Architect",
  "description": "Senior enterprise architect with 10+ years experience",
  "resource_type": "human",
  "quantity": 2.0,
  "unit_of_measure": "FTE",
  "availability": 95.0,
  "allocated_quantity": 0.0,
  "available_quantity": 2.0,
  "location": "Headquarters",
  "deployment_status": "active",
  "criticality": "high",
  "strategic_importance": "high",
  "business_value": "high",
  "cost_per_unit": 150000.0,
  "total_cost": 300000.0,
  "budget_allocation": 300000.0,
  "cost_center": "IT-ARCH",
  "skills_required": "{\"enterprise_architecture\": \"expert\", \"togaf\": \"certified\", \"archimate\": \"proficient\"}",
  "capabilities_provided": "{\"strategic_planning\": true, \"architecture_governance\": true, \"technology_roadmapping\": true}",
  "expertise_level": "expert",
  "performance_metrics": "{\"projects_delivered\": 15, \"stakeholder_satisfaction\": 4.5}",
  "utilization_rate": 85.0,
  "efficiency_score": 0.9,
  "effectiveness_score": 0.85,
  "operational_hours": "business_hours",
  "maintenance_schedule": "Quarterly reviews",
  "technology_stack": "{\"tools\": [\"Sparx EA\", \"ArchiMate\", \"Visio\"]}",
  "system_requirements": "{\"hardware\": \"High-end workstation\", \"software\": \"Enterprise architecture tools\"}",
  "integration_points": "{\"portfolio_management\": \"PPM system\", \"governance\": \"GRC platform\"}",
  "dependencies": "{\"business_units\": \"Stakeholder engagement\", \"technology_teams\": \"Implementation support\"}",
  "governance_model": "enhanced",
  "compliance_requirements": "{\"sox\": true, \"gdpr\": true}",
  "audit_requirements": "{\"quarterly_reviews\": true, \"annual_assessments\": true}",
  "risk_assessment": "{\"key_person_risk\": \"medium\", \"knowledge_transfer\": \"planned\"}",
  "parent_resource_id": null,
  "associated_capability_id": "550e8400-e29b-41d4-a716-446655440001",
  "business_function_id": "550e8400-e29b-41d4-a716-446655440002",
  "application_component_id": null,
  "node_id": null,
  "last_maintenance": null,
  "next_maintenance": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Update Resource

**PUT** `/api/v1/resources/{resource_id}`

Updates a Resource.

**Request Body:** (All fields optional)
```json
{
  "name": "Senior Enterprise Architect",
  "description": "Updated description with enhanced responsibilities",
  "utilization_rate": 90.0,
  "efficiency_score": 0.95,
  "effectiveness_score": 0.9
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Senior Enterprise Architect",
  "description": "Updated description with enhanced responsibilities",
  "utilization_rate": 90.0,
  "efficiency_score": 0.95,
  "effectiveness_score": 0.9,
  "updated_at": "2024-01-15T11:30:00Z"
}
```

### Delete Resource

**DELETE** `/api/v1/resources/{resource_id}`

Deletes a Resource.

**Response:** `204 No Content`

## Resource Link Management

### Create Resource Link

**POST** `/api/v1/resources/{resource_id}/links`

Creates a link between a resource and another element.

**Request Body:**
```json
{
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_type": "business_function",
  "link_type": "enables",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "allocation_percentage": 75.0,
  "allocation_start_date": "2024-01-01T00:00:00Z",
  "allocation_end_date": "2024-12-31T23:59:59Z",
  "allocation_priority": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "data_flow_direction": "bidirectional",
  "performance_impact": "medium",
  "efficiency_contribution": 85.0,
  "effectiveness_contribution": 80.0
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "resource_id": "550e8400-e29b-41d4-a716-446655440000",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_type": "business_function",
  "link_type": "enables",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "allocation_percentage": 75.0,
  "allocation_start_date": "2024-01-01T00:00:00Z",
  "allocation_end_date": "2024-12-31T23:59:59Z",
  "allocation_priority": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "data_flow_direction": "bidirectional",
  "performance_impact": "medium",
  "efficiency_contribution": 85.0,
  "effectiveness_contribution": 80.0,
  "created_by": "550e8400-e29b-41d4-a716-446655440002",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### List Resource Links

**GET** `/api/v1/resources/{resource_id}/links`

Lists all links for a resource.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440004",
    "resource_id": "550e8400-e29b-41d4-a716-446655440000",
    "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
    "linked_element_type": "business_function",
    "link_type": "enables",
    "relationship_strength": "strong",
    "dependency_level": "high",
    "allocation_percentage": 75.0,
    "allocation_start_date": "2024-01-01T00:00:00Z",
    "allocation_end_date": "2024-12-31T23:59:59Z",
    "allocation_priority": "high",
    "interaction_frequency": "frequent",
    "interaction_type": "synchronous",
    "data_flow_direction": "bidirectional",
    "performance_impact": "medium",
    "efficiency_contribution": 85.0,
    "effectiveness_contribution": 80.0,
    "created_by": "550e8400-e29b-41d4-a716-446655440002",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Resource Link

**GET** `/api/v1/resources/links/{link_id}`

Retrieves a resource link by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "resource_id": "550e8400-e29b-41d4-a716-446655440000",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_type": "business_function",
  "link_type": "enables",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "allocation_percentage": 75.0,
  "allocation_start_date": "2024-01-01T00:00:00Z",
  "allocation_end_date": "2024-12-31T23:59:59Z",
  "allocation_priority": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "data_flow_direction": "bidirectional",
  "performance_impact": "medium",
  "efficiency_contribution": 85.0,
  "effectiveness_contribution": 80.0,
  "created_by": "550e8400-e29b-41d4-a716-446655440002",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Update Resource Link

**PUT** `/api/v1/resources/links/{link_id}`

Updates a resource link.

**Request Body:** (All fields optional)
```json
{
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "allocation_percentage": 60.0,
  "performance_impact": "low"
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "allocation_percentage": 60.0,
  "performance_impact": "low"
}
```

### Delete Resource Link

**DELETE** `/api/v1/resources/links/{link_id}`

Deletes a resource link.

**Response:** `204 No Content`

## Analysis & Impact Endpoints

### Get Impact Score

**GET** `/api/v1/resources/{resource_id}/impact-score`

Returns impact score for the Resource.

**Response:** `200 OK`
```json
{
  "resource_id": "550e8400-e29b-41d4-a716-446655440000",
  "strategic_impact_score": 0.85,
  "operational_impact_score": 0.9,
  "financial_impact_score": 0.7,
  "risk_impact_score": 0.8,
  "overall_impact_score": 0.8125,
  "impact_factors": [
    {
      "type": "strategic",
      "factor": "high_strategic_importance",
      "impact": "high",
      "description": "Resource has high strategic importance"
    },
    {
      "type": "operational",
      "factor": "high_utilization",
      "impact": "medium",
      "description": "Resource utilization is 85.0%"
    },
    {
      "type": "financial",
      "factor": "high_cost",
      "impact": "high",
      "description": "Resource cost is $300,000.00"
    },
    {
      "type": "risk",
      "factor": "high_criticality",
      "impact": "high",
      "description": "Resource has high criticality"
    }
  ],
  "recommendations": [
    "Consider increasing strategic alignment",
    "Review business value contribution",
    "Optimize resource utilization",
    "Improve efficiency and effectiveness",
    "Review cost optimization opportunities",
    "Consider cost-benefit analysis",
    "Implement risk mitigation strategies",
    "Enhance monitoring and alerting",
    "Improve resource availability",
    "Implement redundancy strategies"
  ]
}
```

### Get Allocation Map

**GET** `/api/v1/resources/{resource_id}/allocation-map`

Returns allocation map for the Resource.

**Response:** `200 OK`
```json
{
  "resource_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_allocated": 75.0,
  "allocation_breakdown": [
    {
      "element_id": "550e8400-e29b-41d4-a716-446655440003",
      "element_type": "business_function",
      "link_type": "enables",
      "allocation_percentage": 75.0,
      "allocation_priority": "high",
      "performance_impact": "medium"
    }
  ],
  "utilization_analysis": {
    "current_utilization": 85.0,
    "total_allocation": 75.0,
    "available_capacity": 25.0,
    "utilization_efficiency": 0.9,
    "utilization_effectiveness": 0.85,
    "allocation_count": 1
  },
  "capacity_planning": {
    "total_capacity": 2.0,
    "allocated_capacity": 0.0,
    "available_capacity": 2.0,
    "allocation_percentage": 0.0,
    "capacity_utilization": 75.0,
    "capacity_planning_recommendations": [
      "Consider increasing resource utilization"
    ]
  },
  "optimization_opportunities": [
    "Low utilization - consider resource consolidation",
    "Low efficiency - implement process improvements"
  ],
  "allocation_metrics": {
    "total_allocation_percentage": 75.0,
    "high_priority_allocation_percentage": 75.0,
    "allocation_count": 1,
    "average_allocation_percentage": 75.0,
    "allocation_efficiency": 0.75
  }
}
```

### Analyze Resource

**GET** `/api/v1/resources/{resource_id}/analysis`

Returns comprehensive analysis for the Resource.

**Response:** `200 OK`
```json
{
  "resource_id": "550e8400-e29b-41d4-a716-446655440000",
  "performance_analysis": {
    "efficiency_score": 0.9,
    "effectiveness_score": 0.85,
    "utilization_rate": 85.0,
    "availability": 95.0,
    "performance_category": "excellent",
    "performance_trends": "stable",
    "performance_recommendations": [
      "Improve operational efficiency",
      "Enhance effectiveness measures",
      "Increase resource utilization"
    ]
  },
  "cost_analysis": {
    "cost_per_unit": 150000.0,
    "total_cost": 300000.0,
    "budget_allocation": 300000.0,
    "cost_center": "IT-ARCH",
    "cost_efficiency": 0.4,
    "cost_recommendations": [
      "Review cost optimization opportunities",
      "Consider cost-benefit analysis"
    ]
  },
  "utilization_analysis": {
    "current_utilization": 85.0,
    "available_quantity": 2.0,
    "allocated_quantity": 0.0,
    "utilization_efficiency": 0.9,
    "utilization_effectiveness": 0.85,
    "utilization_recommendations": [
      "Increase resource utilization",
      "Consider resource consolidation"
    ]
  },
  "risk_assessment": {
    "criticality_level": "high",
    "availability_risk": 5.0,
    "utilization_risk": 0.0,
    "cost_risk": 0.8,
    "risk_factors": [
      {
        "type": "criticality",
        "level": "high",
        "description": "Resource has high criticality"
      },
      {
        "type": "cost",
        "level": "high",
        "description": "High cost: $300,000.00"
      }
    ],
    "risk_recommendations": [
      "Implement redundancy strategies",
      "Enhance monitoring and alerting",
      "Improve availability measures",
      "Implement backup systems"
    ]
  },
  "optimization_recommendations": [
    "Consider resource consolidation",
    "Implement process improvements",
    "Implement redundancy strategies",
    "Review cost optimization opportunities"
  ],
  "strategic_alignment": {
    "strategic_importance": "high",
    "business_value": "high",
    "alignment_score": 0.9,
    "alignment_factors": [
      {
        "type": "strategic_importance",
        "level": "high",
        "description": "High strategic importance: high"
      },
      {
        "type": "business_value",
        "level": "high",
        "description": "High business value: high"
      }
    ],
    "alignment_recommendations": []
  }
}
```

## Domain-Specific Query Endpoints

### Get by Resource Type

**GET** `/api/v1/resources/by-type/{resource_type}`

Returns resources filtered by type.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Enterprise Architect",
    "resource_type": "human",
    "deployment_status": "active"
  }
]
```

### Get by Status

**GET** `/api/v1/resources/by-status/{deployment_status}`

Returns resources filtered by status.

### Get by Capability

**GET** `/api/v1/resources/by-capability/{capability_id}`

Returns resources filtered by capability.

### Get by Performance

**GET** `/api/v1/resources/by-performance/{performance_threshold}`

Returns resources with utilization above the threshold.

### Get by Element

**GET** `/api/v1/resources/by-element/{element_type}/{element_id}`

Returns resources linked to a specific element.

### Get Active Resources

**GET** `/api/v1/resources/active`

Returns all active resources.

### Get Critical Resources

**GET** `/api/v1/resources/critical`

Returns all critical resources.

## Enumeration Endpoints

### Get Resource Types

**GET** `/api/v1/resources/resource-types`

Returns all available resource types.

**Response:** `200 OK`
```json
[
  "human",
  "system",
  "financial",
  "knowledge"
]
```

### Get Deployment Statuses

**GET** `/api/v1/resources/deployment-statuses`

Returns all available deployment statuses.

**Response:** `200 OK`
```json
[
  "active",
  "inactive",
  "planned",
  "retired"
]
```

### Get Criticalities

**GET** `/api/v1/resources/criticalities`

Returns all available criticality levels.

**Response:** `200 OK`
```json
[
  "low",
  "medium",
  "high",
  "critical"
]
```

### Get Strategic Importances

**GET** `/api/v1/resources/strategic-importances`

Returns all available strategic importance levels.

**Response:** `200 OK`
```json
[
  "low",
  "medium",
  "high",
  "critical"
]
```

### Get Business Values

**GET** `/api/v1/resources/business-values`

Returns all available business value levels.

**Response:** `200 OK`
```json
[
  "low",
  "medium",
  "high",
  "critical"
]
```

### Get Operational Hours

**GET** `/api/v1/resources/operational-hours`

Returns all available operational hour types.

**Response:** `200 OK`
```json
[
  "24x7",
  "business_hours",
  "on_demand"
]
```

### Get Expertise Levels

**GET** `/api/v1/resources/expertise-levels`

Returns all available expertise levels.

**Response:** `200 OK`
```json
[
  "beginner",
  "intermediate",
  "expert",
  "specialist"
]
```

### Get Governance Models

**GET** `/api/v1/resources/governance-models`

Returns all available governance models.

**Response:** `200 OK`
```json
[
  "basic",
  "standard",
  "enhanced",
  "critical"
]
```

### Get Link Types

**GET** `/api/v1/resources/link-types`

Returns all available link types.

**Response:** `200 OK`
```json
[
  "enables",
  "supports",
  "realizes",
  "governs",
  "influences",
  "consumes",
  "produces",
  "requires"
]
```

### Get Relationship Strengths

**GET** `/api/v1/resources/relationship-strengths`

Returns all available relationship strengths.

**Response:** `200 OK`
```json
[
  "strong",
  "medium",
  "weak"
]
```

### Get Dependency Levels

**GET** `/api/v1/resources/dependency-levels`

Returns all available dependency levels.

**Response:** `200 OK`
```json
[
  "high",
  "medium",
  "low"
]
```

### Get Interaction Frequencies

**GET** `/api/v1/resources/interaction-frequencies`

Returns all available interaction frequencies.

**Response:** `200 OK`
```json
[
  "frequent",
  "regular",
  "occasional",
  "rare"
]
```

### Get Interaction Types

**GET** `/api/v1/resources/interaction-types`

Returns all available interaction types.

**Response:** `200 OK`
```json
[
  "synchronous",
  "asynchronous",
  "batch",
  "real_time"
]
```

### Get Data Flow Directions

**GET** `/api/v1/resources/data-flow-directions`

Returns all available data flow directions.

**Response:** `200 OK`
```json
[
  "input",
  "output",
  "bidirectional"
]
```

### Get Performance Impacts

**GET** `/api/v1/resources/performance-impacts`

Returns all available performance impact levels.

**Response:** `200 OK`
```json
[
  "low",
  "medium",
  "high",
  "critical"
]
```

### Get Allocation Priorities

**GET** `/api/v1/resources/allocation-priorities`

Returns all available allocation priorities.

**Response:** `200 OK`
```json
[
  "low",
  "normal",
  "high",
  "critical"
]
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error: Invalid resource type"
}
```

### 401 Unauthorized
```json
{
  "detail": "Missing or invalid authorization header"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions. Required: resource:create, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage:
- 1000 requests per hour per tenant
- 100 requests per minute per user
- Burst limit: 10 requests per second

## Pagination

List endpoints support pagination with the following parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 1000)

## Filtering

List endpoints support filtering by:
- Resource type
- Deployment status
- Criticality
- Strategic importance
- Associated capability
- Availability threshold
- Utilization threshold

## Sorting

Results are sorted by `created_at` in descending order by default.

## OpenAPI Documentation

For complete OpenAPI documentation, visit:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`
