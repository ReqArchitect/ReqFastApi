# Business Function Service API Reference

## Overview

The Business Function Service API provides comprehensive management of ArchiMate 3.2 Business Function elements with full CRUD operations, analysis capabilities, and domain-specific queries.

## Base URL

```
http://localhost:8080
```

## Authentication

All endpoints require JWT authentication via the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

The JWT token must contain:
- `tenant_id`: UUID of the tenant
- `user_id`: UUID of the user
- `role`: User role (Owner, Admin, Editor, Viewer)

## Common Headers

```
X-Correlation-ID: <correlation_id>  # Optional, auto-generated if not provided
X-Tenant-ID: <tenant_id>            # Optional, extracted from JWT
X-User-ID: <user_id>                # Optional, extracted from JWT
```

## Response Formats

### Success Response
```json
{
  "id": "uuid",
  "name": "string",
  "description": "string",
  "competency_area": "Architecture Governance",
  "organizational_unit": "string",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Error Response
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

## Core Business Function Endpoints

### Create Business Function

**POST** `/business-functions/`

Creates a new business function.

**Request Body:**
```json
{
  "name": "Architecture Governance",
  "description": "Manages enterprise architecture governance",
  "competency_area": "Architecture Governance",
  "organizational_unit": "IT Department",
  "owner_role_id": "uuid",
  "input_object_type": "Architecture Request",
  "output_object_type": "Architecture Decision",
  "frequency": "ongoing",
  "criticality": "high",
  "complexity": "complex",
  "maturity_level": "mature",
  "alignment_score": 0.85,
  "efficiency_score": 0.78,
  "effectiveness_score": 0.92,
  "strategic_importance": "high",
  "business_value": "high",
  "risk_level": "medium",
  "status": "active"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "name": "Architecture Governance",
  "description": "Manages enterprise architecture governance",
  "competency_area": "Architecture Governance",
  "organizational_unit": "IT Department",
  "owner_role_id": "uuid",
  "input_object_type": "Architecture Request",
  "output_object_type": "Architecture Decision",
  "frequency": "ongoing",
  "criticality": "high",
  "complexity": "complex",
  "maturity_level": "mature",
  "alignment_score": 0.85,
  "efficiency_score": 0.78,
  "effectiveness_score": 0.92,
  "strategic_importance": "high",
  "business_value": "high",
  "risk_level": "medium",
  "status": "active",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### List Business Functions

**GET** `/business-functions/`

Lists business functions with filtering and pagination.

**Query Parameters:**
- `skip` (int, default: 0): Number of records to skip
- `limit` (int, default: 100, max: 1000): Number of records to return
- `competency_area` (string, optional): Filter by competency area
- `organizational_unit` (string, optional): Filter by organizational unit
- `criticality` (string, optional): Filter by criticality (low, medium, high, critical)
- `frequency` (string, optional): Filter by frequency (ongoing, daily, weekly, monthly, quarterly, annually, ad_hoc)
- `status` (string, optional): Filter by status (active, inactive, deprecated, planned)
- `owner_role_id` (UUID, optional): Filter by owner role
- `parent_function_id` (UUID, optional): Filter by parent function
- `supporting_capability_id` (UUID, optional): Filter by supporting capability
- `business_process_id` (UUID, optional): Filter by business process

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "name": "Architecture Governance",
    "description": "Manages enterprise architecture governance",
    "competency_area": "Architecture Governance",
    "organizational_unit": "IT Department",
    "criticality": "high",
    "status": "active",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### Get Business Function

**GET** `/business-functions/{function_id}`

Retrieves a specific business function by ID.

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "name": "Architecture Governance",
  "description": "Manages enterprise architecture governance",
  "competency_area": "Architecture Governance",
  "organizational_unit": "IT Department",
  "owner_role_id": "uuid",
  "input_object_type": "Architecture Request",
  "output_object_type": "Architecture Decision",
  "input_description": "Architecture change requests",
  "output_description": "Architecture decisions and approvals",
  "frequency": "ongoing",
  "criticality": "high",
  "complexity": "complex",
  "maturity_level": "mature",
  "alignment_score": 0.85,
  "efficiency_score": 0.78,
  "effectiveness_score": 0.92,
  "performance_metrics": "{\"response_time\": \"2h\", \"approval_rate\": 95}",
  "required_skills": "[\"Enterprise Architecture\", \"TOGAF\", \"Governance\"]",
  "required_capabilities": "[\"Decision Making\", \"Stakeholder Management\"]",
  "resource_requirements": "{\"fte\": 2, \"budget\": 150000}",
  "technology_dependencies": "[\"Architecture Repository\", \"Decision Management System\"]",
  "compliance_requirements": "[\"SOX\", \"GDPR\", \"ISO 27001\"]",
  "risk_level": "medium",
  "audit_frequency": "quarterly",
  "last_audit_date": "2024-01-01T00:00:00Z",
  "audit_status": "completed",
  "status": "active",
  "operational_hours": "business_hours",
  "availability_target": 99.5,
  "current_availability": 99.8,
  "strategic_importance": "high",
  "business_value": "high",
  "cost_center": "IT-ARCH-001",
  "budget_allocation": 150000.0,
  "parent_function_id": null,
  "supporting_capability_id": "uuid",
  "business_process_id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Update Business Function

**PUT** `/business-functions/{function_id}`

Updates a business function. Only provided fields will be updated.

**Request Body:**
```json
{
  "name": "Updated Architecture Governance",
  "description": "Updated description",
  "criticality": "critical",
  "alignment_score": 0.90
}
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "name": "Updated Architecture Governance",
  "description": "Updated description",
  "criticality": "critical",
  "alignment_score": 0.90,
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Delete Business Function

**DELETE** `/business-functions/{function_id}`

Deletes a business function.

**Response:** `204 No Content`

## Function Link Endpoints

### Create Function Link

**POST** `/business-functions/{function_id}/links`

Creates a link between a business function and another ArchiMate element.

**Request Body:**
```json
{
  "linked_element_id": "uuid",
  "linked_element_type": "business_role",
  "link_type": "enables",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "data_flow_direction": "bidirectional"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "business_function_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "business_role",
  "link_type": "enables",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "data_flow_direction": "bidirectional",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### List Function Links

**GET** `/business-functions/{function_id}/links`

Lists all links for a business function.

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "business_function_id": "uuid",
    "linked_element_id": "uuid",
    "linked_element_type": "business_role",
    "link_type": "enables",
    "relationship_strength": "strong",
    "dependency_level": "high",
    "interaction_frequency": "frequent",
    "interaction_type": "synchronous",
    "data_flow_direction": "bidirectional",
    "created_by": "uuid",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Get Function Link

**GET** `/links/{link_id}`

Retrieves a specific function link by ID.

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "business_function_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "business_role",
  "link_type": "enables",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "data_flow_direction": "bidirectional",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Update Function Link

**PUT** `/links/{link_id}`

Updates a function link.

**Request Body:**
```json
{
  "link_type": "supports",
  "relationship_strength": "medium",
  "dependency_level": "medium"
}
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "link_type": "supports",
  "relationship_strength": "medium",
  "dependency_level": "medium"
}
```

### Delete Function Link

**DELETE** `/links/{link_id}`

Deletes a function link.

**Response:** `204 No Content`

## Analysis Endpoints

### Get Impact Map

**GET** `/business-functions/{function_id}/impact-map`

Retrieves impact analysis for a business function.

**Response:** `200 OK`
```json
{
  "business_function_id": "uuid",
  "linked_elements_count": 15,
  "business_roles_count": 5,
  "business_processes_count": 3,
  "capabilities_count": 2,
  "application_services_count": 3,
  "data_objects_count": 2,
  "overall_impact_score": 0.75,
  "last_assessed": "2024-01-01T00:00:00Z"
}
```

### Analyze Business Function

**GET** `/business-functions/{function_id}/analysis`

Retrieves health analysis for a business function.

**Response:** `200 OK`
```json
{
  "business_function_id": "uuid",
  "alignment_score": 0.85,
  "efficiency_score": 0.78,
  "effectiveness_score": 0.92,
  "risk_score": 0.25,
  "strategic_importance_score": 0.75,
  "business_value_score": 0.80,
  "overall_health_score": 0.73,
  "last_analyzed": "2024-01-01T00:00:00Z"
}
```

## Domain Query Endpoints

### Get by Competency Area

**GET** `/business-functions/by-competency-area/{competency_area}`

Lists business functions filtered by competency area.

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "name": "Architecture Governance",
    "competency_area": "Architecture Governance",
    "organizational_unit": "IT Department",
    "criticality": "high",
    "status": "active"
  }
]
```

### Get by Organizational Unit

**GET** `/business-functions/by-organizational-unit/{organizational_unit}`

Lists business functions filtered by organizational unit.

### Get by Criticality

**GET** `/business-functions/by-criticality/{criticality}`

Lists business functions filtered by criticality level.

### Get by Frequency

**GET** `/business-functions/by-frequency/{frequency}`

Lists business functions filtered by frequency.

### Get by Status

**GET** `/business-functions/by-status/{status}`

Lists business functions filtered by status.

### Get by Role

**GET** `/business-functions/by-role/{role_id}`

Lists business functions associated with a specific role.

**Response:** `200 OK`
```json
[
  {
    "business_function_id": "uuid",
    "name": "Architecture Governance",
    "competency_area": "Architecture Governance",
    "organizational_unit": "IT Department",
    "criticality": "high",
    "status": "active",
    "alignment_score": 0.85,
    "last_updated": "2024-01-01T00:00:00Z"
  }
]
```

### Get by Process

**GET** `/business-functions/by-process/{process_id}`

Lists business functions associated with a specific process.

**Response:** `200 OK`
```json
[
  {
    "business_function_id": "uuid",
    "name": "Architecture Governance",
    "competency_area": "Architecture Governance",
    "organizational_unit": "IT Department",
    "frequency": "ongoing",
    "complexity": "complex",
    "maturity_level": "mature",
    "last_updated": "2024-01-01T00:00:00Z"
  }
]
```

### Get by Capability

**GET** `/business-functions/by-capability/{capability_id}`

Lists business functions associated with a specific capability.

### Get by Element

**GET** `/business-functions/by-element/{element_type}/{element_id}`

Lists business functions linked to a specific element.

### Get Active Functions

**GET** `/business-functions/active`

Lists all active business functions.

### Get Critical Functions

**GET** `/business-functions/critical`

Lists all critical business functions.

### Get by Complexity

**GET** `/business-functions/by-complexity/{complexity}`

Lists business functions filtered by complexity.

### Get by Maturity

**GET** `/business-functions/by-maturity/{maturity_level}`

Lists business functions filtered by maturity level.

### Get by Operational Hours

**GET** `/business-functions/by-operational-hours/{operational_hours}`

Lists business functions filtered by operational hours.

### Get by Strategic Importance

**GET** `/business-functions/by-strategic-importance/{strategic_importance}`

Lists business functions filtered by strategic importance.

### Get by Business Value

**GET** `/business-functions/by-business-value/{business_value}`

Lists business functions filtered by business value.

### Get by Risk Level

**GET** `/business-functions/by-risk-level/{risk_level}`

Lists business functions filtered by risk level.

## Utility Endpoints

### Get Competency Areas

**GET** `/competency-areas`

Lists all available competency areas.

**Response:** `200 OK`
```json
[
  "Architecture Governance",
  "Compliance Management",
  "Strategy Analysis",
  "Vendor Evaluation",
  "Risk Management",
  "Performance Monitoring",
  "Quality Assurance",
  "Change Management",
  "Capacity Planning",
  "Cost Management",
  "Security Management",
  "Data Management",
  "Technology Evaluation",
  "Process Optimization",
  "Stakeholder Management"
]
```

### Get Frequencies

**GET** `/frequencies`

Lists all available frequencies.

**Response:** `200 OK`
```json
[
  "ongoing",
  "daily",
  "weekly",
  "monthly",
  "quarterly",
  "annually",
  "ad_hoc"
]
```

### Get Criticalities

**GET** `/criticalities`

Lists all available criticalities.

**Response:** `200 OK`
```json
[
  "low",
  "medium",
  "high",
  "critical"
]
```

### Get Complexities

**GET** `/complexities`

Lists all available complexities.

**Response:** `200 OK`
```json
[
  "simple",
  "medium",
  "complex",
  "very_complex"
]
```

### Get Maturity Levels

**GET** `/maturity-levels`

Lists all available maturity levels.

**Response:** `200 OK`
```json
[
  "basic",
  "developing",
  "mature",
  "advanced"
]
```

### Get Risk Levels

**GET** `/risk-levels`

Lists all available risk levels.

**Response:** `200 OK`
```json
[
  "low",
  "medium",
  "high",
  "critical"
]
```

### Get Audit Frequencies

**GET** `/audit-frequencies`

Lists all available audit frequencies.

**Response:** `200 OK`
```json
[
  "monthly",
  "quarterly",
  "annually",
  "ad_hoc"
]
```

### Get Audit Statuses

**GET** `/audit-statuses`

Lists all available audit statuses.

**Response:** `200 OK`
```json
[
  "pending",
  "in_progress",
  "completed",
  "failed"
]
```

### Get Function Statuses

**GET** `/function-statuses`

Lists all available function statuses.

**Response:** `200 OK`
```json
[
  "active",
  "inactive",
  "deprecated",
  "planned"
]
```

### Get Operational Hours

**GET** `/operational-hours`

Lists all available operational hours.

**Response:** `200 OK`
```json
[
  "24x7",
  "business_hours",
  "on_demand"
]
```

### Get Strategic Importances

**GET** `/strategic-importances`

Lists all available strategic importances.

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

**GET** `/business-values`

Lists all available business values.

**Response:** `200 OK`
```json
[
  "low",
  "medium",
  "high",
  "critical"
]
```

### Get Link Types

**GET** `/link-types`

Lists all available link types.

**Response:** `200 OK`
```json
[
  "enables",
  "supports",
  "realizes",
  "governs",
  "influences",
  "consumes",
  "produces"
]
```

### Get Relationship Strengths

**GET** `/relationship-strengths`

Lists all available relationship strengths.

**Response:** `200 OK`
```json
[
  "strong",
  "medium",
  "weak"
]
```

### Get Dependency Levels

**GET** `/dependency-levels`

Lists all available dependency levels.

**Response:** `200 OK`
```json
[
  "high",
  "medium",
  "low"
]
```

### Get Interaction Frequencies

**GET** `/interaction-frequencies`

Lists all available interaction frequencies.

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

**GET** `/interaction-types`

Lists all available interaction types.

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

**GET** `/data-flow-directions`

Lists all available data flow directions.

**Response:** `200 OK`
```json
[
  "input",
  "output",
  "bidirectional"
]
```

## Health and Monitoring

### Health Check

**GET** `/health`

Returns service health status.

**Response:** `200 OK`
```json
{
  "service": "business_function_service",
  "version": "1.0.0",
  "status": "healthy",
  "uptime": "3600.00s",
  "total_requests": 1500,
  "error_rate": 0.02,
  "database_connected": true,
  "timestamp": "2024-01-01T00:00:00Z",
  "environment": "development"
}
```

### Metrics

**GET** `/metrics`

Returns Prometheus metrics.

**Response:** `200 OK`
```
# HELP business_function_service_requests_total Total requests
# TYPE business_function_service_requests_total counter
business_function_service_requests_total{method="GET",route="/health",status="200"} 1500
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Missing or invalid JWT token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

## Rate Limiting

The API implements rate limiting based on tenant and user. Limits are configurable per environment.

## Pagination

List endpoints support pagination with `skip` and `limit` parameters. The maximum limit is 1000 records per request.

## Filtering

Most list endpoints support filtering by various attributes. Filters are applied as AND conditions.

## Sorting

Currently, results are sorted by creation date (newest first). Custom sorting will be added in future versions. 