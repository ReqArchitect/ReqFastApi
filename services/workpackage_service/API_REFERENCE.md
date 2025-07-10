# API Reference: workpackage_service

## Overview

The Work Package Service provides comprehensive management of ArchiMate 3.2 Work Package elements with full CRUD operations, relationship management, analysis capabilities, and domain-specific queries.

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

## Work Package Management

### Create Work Package

**POST** `/api/v1/work-packages`

Creates a new WorkPackage.

**Request Body:**
```json
{
  "name": "Modernization Sprint #7",
  "description": "Sprint focused on modernizing legacy systems",
  "package_type": "sprint",
  "strategic_driver_id": "550e8400-e29b-41d4-a716-446655440001",
  "related_goal_id": "550e8400-e29b-41d4-a716-446655440002",
  "target_plateau_id": "550e8400-e29b-41d4-a716-446655440003",
  "impacted_capabilities": "[\"550e8400-e29b-41d4-a716-446655440004\"]",
  "impacted_application_components": "[\"550e8400-e29b-41d4-a716-446655440005\"]",
  "impacted_technology_nodes": "[\"550e8400-e29b-41d4-a716-446655440006\"]",
  "scheduled_start": "2024-01-15T10:00:00Z",
  "scheduled_end": "2024-02-15T18:00:00Z",
  "current_status": "in_progress",
  "progress_percent": 75.0,
  "delivery_risk": "medium",
  "quality_gates": "[{\"name\": \"Code Review\", \"status\": \"passed\"}]",
  "risk_mitigation_plan": "Enhanced testing and monitoring",
  "estimated_effort_hours": 160.0,
  "actual_effort_hours": 120.0,
  "budget_allocation": 50000.0,
  "actual_cost": 45000.0,
  "change_owner_id": "550e8400-e29b-41d4-a716-446655440007",
  "team_members": "[\"550e8400-e29b-41d4-a716-446655440008\"]",
  "stakeholders": "[\"550e8400-e29b-41d4-a716-446655440009\"]",
  "dependencies": "[\"550e8400-e29b-41d4-a716-446655440010\"]",
  "blockers": "[]",
  "quality_metrics": "{\"code_coverage\": \"85%\", \"test_pass_rate\": \"95%\"}",
  "compliance_requirements": "[\"SOX\", \"GDPR\"]",
  "audit_trail": "[{\"event\": \"created\", \"timestamp\": \"2024-01-15T10:00:00Z\"}]",
  "kpis": "{\"velocity\": \"15 story points/sprint\", \"quality_score\": \"92%\"}",
  "reporting_frequency": "weekly",
  "escalation_path": "{\"level1\": \"team_lead\", \"level2\": \"project_manager\"}",
  "tags": "[\"modernization\", \"legacy\", \"sprint\"]",
  "priority": 2,
  "complexity": "medium"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440011",
  "user_id": "550e8400-e29b-41d4-a716-446655440012",
  "name": "Modernization Sprint #7",
  "description": "Sprint focused on modernizing legacy systems",
  "package_type": "sprint",
  "strategic_driver_id": "550e8400-e29b-41d4-a716-446655440001",
  "related_goal_id": "550e8400-e29b-41d4-a716-446655440002",
  "target_plateau_id": "550e8400-e29b-41d4-a716-446655440003",
  "impacted_capabilities": "[\"550e8400-e29b-41d4-a716-446655440004\"]",
  "impacted_application_components": "[\"550e8400-e29b-41d4-a716-446655440005\"]",
  "impacted_technology_nodes": "[\"550e8400-e29b-41d4-a716-446655440006\"]",
  "scheduled_start": "2024-01-15T10:00:00Z",
  "scheduled_end": "2024-02-15T18:00:00Z",
  "actual_start": null,
  "actual_end": null,
  "current_status": "in_progress",
  "progress_percent": 75.0,
  "delivery_risk": "medium",
  "quality_gates": "[{\"name\": \"Code Review\", \"status\": \"passed\"}]",
  "risk_mitigation_plan": "Enhanced testing and monitoring",
  "estimated_effort_hours": 160.0,
  "actual_effort_hours": 120.0,
  "budget_allocation": 50000.0,
  "actual_cost": 45000.0,
  "change_owner_id": "550e8400-e29b-41d4-a716-446655440007",
  "team_members": "[\"550e8400-e29b-41d4-a716-446655440008\"]",
  "stakeholders": "[\"550e8400-e29b-41d4-a716-446655440009\"]",
  "dependencies": "[\"550e8400-e29b-41d4-a716-446655440010\"]",
  "blockers": "[]",
  "quality_metrics": "{\"code_coverage\": \"85%\", \"test_pass_rate\": \"95%\"}",
  "compliance_requirements": "[\"SOX\", \"GDPR\"]",
  "audit_trail": "[{\"event\": \"created\", \"timestamp\": \"2024-01-15T10:00:00Z\"}]",
  "kpis": "{\"velocity\": \"15 story points/sprint\", \"quality_score\": \"92%\"}",
  "reporting_frequency": "weekly",
  "escalation_path": "{\"level1\": \"team_lead\", \"level2\": \"project_manager\"}",
  "tags": "[\"modernization\", \"legacy\", \"sprint\"]",
  "priority": 2,
  "complexity": "medium",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### List Work Packages

**GET** `/api/v1/work-packages`

Lists all WorkPackages for the tenant with filtering and pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)
- `package_type` (string, optional): Filter by package type
- `status` (string, optional): Filter by status
- `delivery_risk` (string, optional): Filter by delivery risk
- `change_owner_id` (UUID, optional): Filter by change owner
- `related_goal_id` (UUID, optional): Filter by related goal
- `target_plateau_id` (UUID, optional): Filter by target plateau
- `progress_threshold` (float, optional): Filter by minimum progress

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Modernization Sprint #7",
    "package_type": "sprint",
    "current_status": "in_progress",
    "progress_percent": 75.0,
    "delivery_risk": "medium",
    "scheduled_start": "2024-01-15T10:00:00Z",
    "scheduled_end": "2024-02-15T18:00:00Z",
    "estimated_effort_hours": 160.0,
    "budget_allocation": 50000.0,
    "priority": 2,
    "created_at": "2024-01-15T10:00:00Z"
  }
]
```

### Get Work Package

**GET** `/api/v1/work-packages/{work_package_id}`

Retrieves a WorkPackage by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440011",
  "user_id": "550e8400-e29b-41d4-a716-446655440012",
  "name": "Modernization Sprint #7",
  "description": "Sprint focused on modernizing legacy systems",
  "package_type": "sprint",
  "strategic_driver_id": "550e8400-e29b-41d4-a716-446655440001",
  "related_goal_id": "550e8400-e29b-41d4-a716-446655440002",
  "target_plateau_id": "550e8400-e29b-41d4-a716-446655440003",
  "impacted_capabilities": "[\"550e8400-e29b-41d4-a716-446655440004\"]",
  "impacted_application_components": "[\"550e8400-e29b-41d4-a716-446655440005\"]",
  "impacted_technology_nodes": "[\"550e8400-e29b-41d4-a716-446655440006\"]",
  "scheduled_start": "2024-01-15T10:00:00Z",
  "scheduled_end": "2024-02-15T18:00:00Z",
  "actual_start": null,
  "actual_end": null,
  "current_status": "in_progress",
  "progress_percent": 75.0,
  "delivery_risk": "medium",
  "quality_gates": "[{\"name\": \"Code Review\", \"status\": \"passed\"}]",
  "risk_mitigation_plan": "Enhanced testing and monitoring",
  "estimated_effort_hours": 160.0,
  "actual_effort_hours": 120.0,
  "budget_allocation": 50000.0,
  "actual_cost": 45000.0,
  "change_owner_id": "550e8400-e29b-41d4-a716-446655440007",
  "team_members": "[\"550e8400-e29b-41d4-a716-446655440008\"]",
  "stakeholders": "[\"550e8400-e29b-41d4-a716-446655440009\"]",
  "dependencies": "[\"550e8400-e29b-41d4-a716-446655440010\"]",
  "blockers": "[]",
  "quality_metrics": "{\"code_coverage\": \"85%\", \"test_pass_rate\": \"95%\"}",
  "compliance_requirements": "[\"SOX\", \"GDPR\"]",
  "audit_trail": "[{\"event\": \"created\", \"timestamp\": \"2024-01-15T10:00:00Z\"}]",
  "kpis": "{\"velocity\": \"15 story points/sprint\", \"quality_score\": \"92%\"}",
  "reporting_frequency": "weekly",
  "escalation_path": "{\"level1\": \"team_lead\", \"level2\": \"project_manager\"}",
  "tags": "[\"modernization\", \"legacy\", \"sprint\"]",
  "priority": 2,
  "complexity": "medium",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### Update Work Package

**PUT** `/api/v1/work-packages/{work_package_id}`

Updates a WorkPackage.

**Request Body:** (All fields optional)
```json
{
  "name": "Enhanced Modernization Sprint #7",
  "description": "Updated description with enhanced scope",
  "progress_percent": 85.0,
  "delivery_risk": "low",
  "actual_effort_hours": 140.0
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Enhanced Modernization Sprint #7",
  "description": "Updated description with enhanced scope",
  "progress_percent": 85.0,
  "delivery_risk": "low",
  "actual_effort_hours": 140.0,
  "updated_at": "2024-01-15T11:00:00Z"
}
```

### Delete Work Package

**DELETE** `/api/v1/work-packages/{work_package_id}`

Deletes a WorkPackage.

**Response:** `204 No Content`

## Package Link Management

### Create Package Link

**POST** `/api/v1/work-packages/{work_package_id}/links`

Creates a link between a work package and another element.

**Request Body:**
```json
{
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440013",
  "linked_element_type": "gap",
  "link_type": "closes",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "impact_level": "high",
  "impact_description": "This work package directly addresses the data loss gap",
  "impact_metrics": "{\"gap_closure_percentage\": \"75%\", \"risk_reduction\": \"60%\"}",
  "traceability_score": 0.9,
  "traceability_evidence": "[{\"type\": \"requirement\", \"id\": \"REQ-001\"}]",
  "is_validated": true,
  "validation_date": "2024-01-15T10:00:00Z",
  "validated_by": "550e8400-e29b-41d4-a716-446655440012"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440014",
  "work_package_id": "550e8400-e29b-41d4-a716-446655440000",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440013",
  "linked_element_type": "gap",
  "link_type": "closes",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "impact_level": "high",
  "impact_description": "This work package directly addresses the data loss gap",
  "impact_metrics": "{\"gap_closure_percentage\": \"75%\", \"risk_reduction\": \"60%\"}",
  "traceability_score": 0.9,
  "traceability_evidence": "[{\"type\": \"requirement\", \"id\": \"REQ-001\"}]",
  "is_validated": true,
  "validation_date": "2024-01-15T10:00:00Z",
  "validated_by": "550e8400-e29b-41d4-a716-446655440012",
  "created_by": "550e8400-e29b-41d4-a716-446655440012",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### List Package Links

**GET** `/api/v1/work-packages/{work_package_id}/links`

Lists all links for a work package.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440014",
    "work_package_id": "550e8400-e29b-41d4-a716-446655440000",
    "linked_element_id": "550e8400-e29b-41d4-a716-446655440013",
    "linked_element_type": "gap",
    "link_type": "closes",
    "relationship_strength": "strong",
    "dependency_level": "high",
    "impact_level": "high",
    "impact_description": "This work package directly addresses the data loss gap",
    "impact_metrics": "{\"gap_closure_percentage\": \"75%\", \"risk_reduction\": \"60%\"}",
    "traceability_score": 0.9,
    "traceability_evidence": "[{\"type\": \"requirement\", \"id\": \"REQ-001\"}]",
    "is_validated": true,
    "validation_date": "2024-01-15T10:00:00Z",
    "validated_by": "550e8400-e29b-41d4-a716-446655440012",
    "created_by": "550e8400-e29b-41d4-a716-446655440012",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
]
```

### Get Package Link

**GET** `/api/v1/work-packages/links/{link_id}`

Retrieves a package link by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440014",
  "work_package_id": "550e8400-e29b-41d4-a716-446655440000",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440013",
  "linked_element_type": "gap",
  "link_type": "closes",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "impact_level": "high",
  "impact_description": "This work package directly addresses the data loss gap",
  "impact_metrics": "{\"gap_closure_percentage\": \"75%\", \"risk_reduction\": \"60%\"}",
  "traceability_score": 0.9,
  "traceability_evidence": "[{\"type\": \"requirement\", \"id\": \"REQ-001\"}]",
  "is_validated": true,
  "validation_date": "2024-01-15T10:00:00Z",
  "validated_by": "550e8400-e29b-41d4-a716-446655440012",
  "created_by": "550e8400-e29b-41d4-a716-446655440012",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### Update Package Link

**PUT** `/api/v1/work-packages/links/{link_id}`

Updates a package link.

**Request Body:** (All fields optional)
```json
{
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "impact_level": "medium",
  "traceability_score": 0.8
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440014",
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "impact_level": "medium",
  "traceability_score": 0.8
}
```

### Delete Package Link

**DELETE** `/api/v1/work-packages/links/{link_id}`

Deletes a package link.

**Response:** `204 No Content`

## Analysis & Impact Endpoints

### Get Execution Status

**GET** `/api/v1/work-packages/{work_package_id}/execution-status`

Returns execution status analysis for the WorkPackage.

**Response:** `200 OK`
```json
{
  "work_package_id": "550e8400-e29b-41d4-a716-446655440000",
  "overall_status": "on_track",
  "progress_analysis": {
    "current_progress": 75.0,
    "is_on_track": true,
    "estimated_completion": "2024-02-10T18:00:00Z",
    "velocity": 1.5
  },
  "timeline_analysis": {
    "scheduled_duration": 31,
    "actual_duration": 25,
    "is_delayed": false,
    "days_remaining": 15
  },
  "risk_assessment": {
    "delivery_risk": "medium",
    "risk_factors": ["Effort overrun"],
    "mitigation_status": "mitigation_needed"
  },
  "quality_gates_status": {
    "total_gates": 3,
    "passed_gates": 2,
    "failed_gates": 0,
    "pending_gates": 1
  },
  "resource_utilization": {
    "effort_utilization": 87.5,
    "budget_utilization": 90.0,
    "team_utilization": 75.0
  },
  "recommendations": [
    "Monitor effort utilization closely",
    "Consider additional quality gates"
  ]
}
```

### Get Gap Closure Map

**GET** `/api/v1/work-packages/{work_package_id}/gap-closure-map`

Returns gap closure mapping for the WorkPackage.

**Response:** `200 OK`
```json
{
  "work_package_id": "550e8400-e29b-41d4-a716-446655440000",
  "gaps_addressed": [
    {
      "gap_id": "550e8400-e29b-41d4-a716-446655440013",
      "link_type": "closes",
      "relationship_strength": "strong",
      "dependency_level": "high",
      "impact_level": "high",
      "traceability_score": 0.9,
      "is_validated": true
    }
  ],
  "closure_progress": {
    "total_gaps": 1,
    "addressed_gaps": 1,
    "partial_closure": 0,
    "closure_percentage": 100.0
  },
  "impact_assessment": {
    "high_impact_gaps": 1,
    "critical_gaps": 1,
    "validated_gaps": 1,
    "overall_impact_score": 4.0
  },
  "traceability_matrix": {
    "high_traceability": 1,
    "medium_traceability": 0,
    "low_traceability": 0,
    "average_traceability": 0.9
  },
  "validation_status": {
    "validated_count": 1,
    "pending_validation": 0,
    "validation_rate": 1.0
  }
}
```

## Domain-Specific Query Endpoints

### Get by Package Type

**GET** `/api/v1/work-packages/by-type/{package_type}`

Returns work packages filtered by type.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Modernization Sprint #7",
    "package_type": "sprint",
    "current_status": "in_progress"
  }
]
```

### Get by Status

**GET** `/api/v1/work-packages/by-status/{status}`

Returns work packages filtered by status.

### Get by Delivery Risk

**GET** `/api/v1/work-packages/by-risk/{delivery_risk}`

Returns work packages filtered by delivery risk.

### Get by Goal

**GET** `/api/v1/work-packages/by-goal/{goal_id}`

Returns work packages filtered by related goal.

### Get by Plateau

**GET** `/api/v1/work-packages/by-plateau/{plateau_id}`

Returns work packages filtered by target plateau.

### Get by Change Owner

**GET** `/api/v1/work-packages/by-owner/{owner_id}`

Returns work packages filtered by change owner.

### Get by Progress

**GET** `/api/v1/work-packages/by-progress/{progress_threshold}`

Returns work packages with progress above the threshold.

### Get by Element

**GET** `/api/v1/work-packages/by-element/{element_type}/{element_id}`

Returns work packages linked to a specific element.

### Get Active Work Packages

**GET** `/api/v1/work-packages/active`

Returns all active work packages.

### Get Critical Work Packages

**GET** `/api/v1/work-packages/critical`

Returns all critical work packages.

## Enumeration Endpoints

### Get Package Types

**GET** `/api/v1/work-packages/package-types`

Returns all available package types.

**Response:** `200 OK`
```json
[
  "project",
  "epic",
  "task",
  "release",
  "phase",
  "sprint",
  "initiative",
  "milestone"
]
```

### Get Statuses

**GET** `/api/v1/work-packages/statuses`

Returns all available statuses.

**Response:** `200 OK`
```json
[
  "planned",
  "in_progress",
  "on_hold",
  "completed",
  "cancelled",
  "delayed",
  "blocked"
]
```

### Get Delivery Risks

**GET** `/api/v1/work-packages/delivery-risks`

Returns all available delivery risk levels.

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

**GET** `/api/v1/work-packages/link-types`

Returns all available link types.

**Response:** `200 OK`
```json
[
  "realizes",
  "closes",
  "delivers",
  "supports",
  "enables",
  "impacts",
  "depends_on",
  "contributes_to"
]
```

### Get Relationship Strengths

**GET** `/api/v1/work-packages/relationship-strengths`

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

**GET** `/api/v1/work-packages/dependency-levels`

Returns all available dependency levels.

**Response:** `200 OK`
```json
[
  "high",
  "medium",
  "low"
]
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error: Invalid package type"
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
  "detail": "Insufficient permissions. Required: work_package:create, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Work package not found"
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
- Package type
- Status
- Delivery risk
- Change owner
- Related goal
- Target plateau
- Progress threshold

## Sorting

Results are sorted by `created_at` in descending order by default.

## OpenAPI Documentation

For complete OpenAPI documentation, visit:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`
