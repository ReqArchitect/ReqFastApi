# API Reference: Architecture Validation Service

## Overview

The Architecture Validation Service provides comprehensive validation and scoring of tenant-specific architecture models for alignment, traceability, and completeness across all ArchiMate 3.2 layers.

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

## Validation Management

### Run Validation Cycle

**POST** `/validation/run`

Triggers a full validation scan for the tenant.

**Request Body:**
```json
{
  "rule_set_id": "optional-rule-set-id",
  "force_full_scan": false
}
```

**Response:** `200 OK`
```json
{
  "validation_cycle_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "message": "Validation cycle 550e8400-e29b-41d4-a716-446655440000 started successfully"
}
```

**Permissions:** Owner, Admin

### Get Validation Issues

**GET** `/validation/issues`

Lists all validation issues for the tenant with filtering and pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)

**Response:** `200 OK`
```json
{
  "issues": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
      "validation_cycle_id": "550e8400-e29b-41d4-a716-446655440000",
      "entity_type": "goal",
      "entity_id": "550e8400-e29b-41d4-a716-446655440003",
      "issue_type": "missing_link",
      "severity": "high",
      "description": "Goal 'Improve Customer Satisfaction' has no links to capabilities",
      "recommended_fix": "Create 'supports' relationship to at least one capability",
      "metadata": {
        "source_element": {
          "id": "550e8400-e29b-41d4-a716-446655440003",
          "name": "Improve Customer Satisfaction",
          "type": "goal"
        },
        "expected_connections": 1,
        "actual_connections": 0,
        "relationship_type": "supports"
      },
      "timestamp": "2024-01-15T10:30:00Z",
      "is_resolved": false,
      "resolved_at": null,
      "resolved_by": null
    }
  ],
  "total_count": 1,
  "critical_count": 0,
  "high_count": 1,
  "medium_count": 0,
  "low_count": 0
}
```

### Get Validation Scorecard

**GET** `/validation/scorecard`

Returns validation scorecard with maturity score breakdown.

**Query Parameters:**
- `validation_cycle_id` (string, optional): Specific validation cycle ID

**Response:** `200 OK`
```json
{
  "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
  "validation_cycle_id": "550e8400-e29b-41d4-a716-446655440000",
  "overall_maturity_score": 85.5,
  "layer_scores": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440004",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
      "validation_cycle_id": "550e8400-e29b-41d4-a716-446655440000",
      "layer": "Motivation",
      "completeness_score": 90.0,
      "traceability_score": 85.0,
      "alignment_score": 80.0,
      "overall_score": 85.0,
      "issues_count": 2,
      "critical_issues": 0,
      "high_issues": 1,
      "medium_issues": 1,
      "low_issues": 0,
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440005",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
      "validation_cycle_id": "550e8400-e29b-41d4-a716-446655440000",
      "layer": "Business",
      "completeness_score": 95.0,
      "traceability_score": 90.0,
      "alignment_score": 85.0,
      "overall_score": 90.0,
      "issues_count": 1,
      "critical_issues": 0,
      "high_issues": 0,
      "medium_issues": 1,
      "low_issues": 0,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "summary": {
    "total_layers": 2,
    "average_score": 87.5,
    "best_layer": "Business",
    "worst_layer": "Motivation"
  }
}
```

### Get Traceability Matrix

**GET** `/validation/traceability-matrix`

Returns cross-layer traceability matrix.

**Query Parameters:**
- `source_layer` (string, optional): Source layer filter
- `target_layer` (string, optional): Target layer filter

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440006",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
    "source_layer": "Motivation",
    "target_layer": "Business",
    "source_entity_type": "goal",
    "target_entity_type": "capability",
    "relationship_type": "supports",
    "connection_count": 15,
    "missing_connections": 3,
    "strength_score": 0.83,
    "last_updated": "2024-01-15T10:30:00Z"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440007",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
    "source_layer": "Business",
    "target_layer": "Application",
    "source_entity_type": "capability",
    "target_entity_type": "application_function",
    "relationship_type": "realizes",
    "connection_count": 12,
    "missing_connections": 5,
    "strength_score": 0.71,
    "last_updated": "2024-01-15T10:30:00Z"
  }
]
```

### Get Validation History

**GET** `/validation/history`

Returns validation history for the tenant.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 50, max: 100)

**Response:** `200 OK`
```json
{
  "cycles": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
      "start_time": "2024-01-15T10:00:00Z",
      "end_time": "2024-01-15T10:30:00Z",
      "triggered_by": "550e8400-e29b-41d4-a716-446655440008",
      "rule_set_id": null,
      "total_issues_found": 5,
      "execution_status": "completed",
      "maturity_score": 85.5,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total_cycles": 1,
  "average_maturity_score": 85.5,
  "last_validation_date": "2024-01-15T10:30:00Z"
}
```

## Rule Management

### Create Validation Exception

**POST** `/validation/exceptions`

Creates a validation exception to whitelist intentional modeling gaps.

**Request Body:**
```json
{
  "entity_type": "goal",
  "entity_id": "550e8400-e29b-41d4-a716-446655440003",
  "reason": "This goal is intentionally not linked to capabilities",
  "rule_id": "550e8400-e29b-41d4-a716-446655440009",
  "expires_at": "2024-12-31T23:59:59Z"
}
```

**Response:** `200 OK`
```json
{
  "message": "Validation exception created successfully",
  "exception_id": "550e8400-e29b-41d4-a716-446655440010"
}
```

**Permissions:** Owner, Admin

### Toggle Validation Rule

**PATCH** `/validation/rules/{rule_id}`

Toggles validation rule activation.

**Request Body:**
```json
{
  "is_active": false
}
```

**Response:** `200 OK`
```json
{
  "message": "Validation rule deactivated successfully",
  "rule_id": "550e8400-e29b-41d4-a716-446655440009",
  "is_active": false
}
```

**Permissions:** Owner, Admin

### Get Validation Rules

**GET** `/validation/rules`

Returns all validation rules.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440009",
    "name": "Goal-Capability Linkage",
    "description": "All goals must link to at least one capability",
    "rule_type": "traceability",
    "scope": "Motivation",
    "rule_logic": "{\"source_type\": \"goal\", \"target_type\": \"capability\", \"relationship_type\": \"supports\", \"min_connections\": 1}",
    "severity": "high",
    "is_active": true,
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
]
```

## System Endpoints

### Health Check

**GET** `/health`

Returns service health status.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "architecture_validation_service",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "dependencies": {
    "redis": "connected",
    "database": "connected"
  }
}
```

### Service Metrics

**GET** `/metrics`

Returns service metrics.

**Response:** `200 OK`
```json
{
  "validation_cycles_total": 10,
  "validation_issues_total": 25,
  "validation_rules_active": 15,
  "validation_exceptions_total": 3,
  "average_maturity_score": 85.5,
  "uptime_seconds": 86400,
  "requests_total": 150,
  "errors_total": 2
}
```

### Service Information

**GET** `/`

Returns service information.

**Response:** `200 OK`
```json
{
  "service": "Architecture Validation Service",
  "version": "1.0.0",
  "status": "running",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error: Invalid rule configuration"
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
  "detail": "Insufficient permissions. Required roles: ['Admin', 'Owner'], User role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Validation cycle not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Validation Rule Types

### Traceability Rules

Validate relationships between elements across layers:

```json
{
  "source_type": "goal",
  "target_type": "capability",
  "relationship_type": "supports",
  "min_connections": 1
}
```

### Completeness Rules

Validate required elements and fields:

```json
{
  "element_type": "business_process",
  "required_fields": ["name", "description", "owner"],
  "min_count": 1
}
```

### Alignment Rules

Validate alignment between layers:

```json
{
  "source_layer": "Motivation",
  "target_layer": "Business",
  "alignment_criteria": {
    "name_similarity": 0.8,
    "semantic_matching": true
  }
}
```

## Issue Types

- `missing_link`: Element lacks required relationships
- `orphaned`: Element not linked to any trace path
- `stale`: Element hasn't been updated recently
- `invalid_enum`: Element has invalid classification
- `broken_traceability`: Traceability path is broken

## Severity Levels

- `low`: Minor issue, doesn't affect functionality
- `medium`: Moderate issue, may impact quality
- `high`: Significant issue, affects traceability
- `critical`: Critical issue, breaks architecture integrity

## Rate Limiting

The API implements rate limiting to ensure fair usage:
- 100 requests per hour per tenant
- 10 requests per minute per user
- Burst limit: 5 requests per second

## Pagination

List endpoints support pagination with the following parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default varies by endpoint)

## OpenAPI Documentation

For complete OpenAPI documentation, visit:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json` 