# Business Process Service API Reference

## Overview

The Business Process Service API provides comprehensive management of business processes, process steps, and process links in the ReqArchitect platform. All endpoints require JWT authentication and support multi-tenancy.

## Authentication

All API endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt-token>
```

The JWT token must contain:
- `sub`: User ID
- `tenant_id`: Tenant ID
- `role`: User role (owner, admin, editor, viewer)

## Base URL

```
http://localhost:8080/api/v1
```

## Business Process Endpoints

### Create Business Process

**POST** `/business-processes/`

Creates a new business process.

**Permissions:** Editor or higher

**Request Body:**
```json
{
  "name": "Customer Order Processing",
  "description": "End-to-end customer order processing workflow",
  "process_type": "operational",
  "input_object_type": "Customer Order",
  "output_object_type": "Processed Order",
  "organizational_unit": "Sales Department",
  "goal_id": "uuid-optional",
  "capability_id": "uuid-optional",
  "actor_id": "uuid-optional",
  "role_id": "uuid-optional",
  "process_classification": "operational",
  "criticality": "high",
  "complexity": "medium",
  "automation_level": "semi_automated",
  "performance_score": 0.85,
  "effectiveness_score": 0.90,
  "efficiency_score": 0.80,
  "quality_score": 0.95,
  "status": "active",
  "priority": "high",
  "frequency": "daily",
  "duration_target": 4.5,
  "duration_average": 4.2,
  "volume_target": 100,
  "volume_actual": 95
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "name": "Customer Order Processing",
  "description": "End-to-end customer order processing workflow",
  "process_type": "operational",
  "input_object_type": "Customer Order",
  "output_object_type": "Processed Order",
  "organizational_unit": "Sales Department",
  "goal_id": "uuid-optional",
  "capability_id": "uuid-optional",
  "actor_id": "uuid-optional",
  "role_id": "uuid-optional",
  "process_classification": "operational",
  "criticality": "high",
  "complexity": "medium",
  "automation_level": "semi_automated",
  "performance_score": 0.85,
  "effectiveness_score": 0.90,
  "efficiency_score": 0.80,
  "quality_score": 0.95,
  "status": "active",
  "priority": "high",
  "frequency": "daily",
  "duration_target": 4.5,
  "duration_average": 4.2,
  "volume_target": 100,
  "volume_actual": 95,
  "tenant_id": "uuid",
  "user_id": "uuid",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### List Business Processes

**GET** `/business-processes/`

Retrieves a list of business processes with optional filtering.

**Permissions:** Viewer or higher

**Query Parameters:**
- `skip` (integer, default: 0): Number of records to skip
- `limit` (integer, default: 100, max: 1000): Number of records to return
- `process_type` (string, optional): Filter by process type
- `organizational_unit` (string, optional): Filter by organizational unit
- `status` (string, optional): Filter by status
- `criticality` (string, optional): Filter by criticality

**Response:** `200 OK`
```json
{
  "business_processes": [
    {
      "id": "uuid",
      "name": "Customer Order Processing",
      "process_type": "operational",
      "organizational_unit": "Sales Department",
      "criticality": "high",
      "status": "active",
      "performance_score": 0.85,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

### Get Business Process

**GET** `/business-processes/{business_process_id}`

Retrieves a specific business process by ID.

**Permissions:** Viewer or higher

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "name": "Customer Order Processing",
  "description": "End-to-end customer order processing workflow",
  "process_type": "operational",
  "input_object_type": "Customer Order",
  "output_object_type": "Processed Order",
  "organizational_unit": "Sales Department",
  "goal_id": "uuid-optional",
  "capability_id": "uuid-optional",
  "actor_id": "uuid-optional",
  "role_id": "uuid-optional",
  "process_classification": "operational",
  "criticality": "high",
  "complexity": "medium",
  "automation_level": "semi_automated",
  "performance_score": 0.85,
  "effectiveness_score": 0.90,
  "efficiency_score": 0.80,
  "quality_score": 0.95,
  "status": "active",
  "priority": "high",
  "frequency": "daily",
  "duration_target": 4.5,
  "duration_average": 4.2,
  "volume_target": 100,
  "volume_actual": 95,
  "tenant_id": "uuid",
  "user_id": "uuid",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Update Business Process

**PUT** `/business-processes/{business_process_id}`

Updates an existing business process.

**Permissions:** Editor or higher

**Request Body:** (All fields optional)
```json
{
  "name": "Updated Customer Order Processing",
  "description": "Updated description",
  "performance_score": 0.90,
  "status": "active"
}
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "name": "Updated Customer Order Processing",
  "description": "Updated description",
  "process_type": "operational",
  "performance_score": 0.90,
  "status": "active",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Delete Business Process

**DELETE** `/business-processes/{business_process_id}`

Deletes a business process.

**Permissions:** Admin or higher

**Response:** `204 No Content`

## Analysis Endpoints

### Get Process Flow Map

**GET** `/business-processes/{business_process_id}/flow-map`

Analyzes the process flow and complexity.

**Permissions:** Viewer or higher

**Response:** `200 OK`
```json
{
  "business_process_id": "uuid",
  "total_steps": 8,
  "automated_steps": 5,
  "manual_steps": 3,
  "decision_points": 2,
  "handoff_points": 1,
  "bottleneck_steps": 1,
  "average_step_duration": 0.5,
  "total_process_duration": 4.0,
  "flow_complexity_score": 0.75,
  "last_analyzed": "2024-01-01T00:00:00Z"
}
```

### Get Process Realization Health

**GET** `/business-processes/{business_process_id}/realization-health`

Assesses the overall health and performance of the process.

**Permissions:** Viewer or higher

**Response:** `200 OK`
```json
{
  "business_process_id": "uuid",
  "performance_score": 0.85,
  "effectiveness_score": 0.90,
  "efficiency_score": 0.80,
  "quality_score": 0.95,
  "automation_score": 0.75,
  "compliance_score": 1.0,
  "overall_health_score": 0.875,
  "last_assessed": "2024-01-01T00:00:00Z"
}
```

## Domain Query Endpoints

### Get Processes by Role

**GET** `/business-processes/by-role/{role_id}`

Retrieves all business processes associated with a specific role.

**Permissions:** Viewer or higher

**Response:** `200 OK`
```json
[
  {
    "business_process_id": "uuid",
    "name": "Customer Order Processing",
    "process_type": "operational",
    "organizational_unit": "Sales Department",
    "criticality": "high",
    "status": "active",
    "performance_score": 0.85,
    "last_updated": "2024-01-01T00:00:00Z"
  }
]
```

### Get Processes by Function

**GET** `/business-processes/by-function/{business_function_id}`

Retrieves all business processes associated with a specific business function.

**Permissions:** Viewer or higher

**Response:** `200 OK`
```json
[
  {
    "business_process_id": "uuid",
    "name": "Customer Order Processing",
    "process_type": "operational",
    "organizational_unit": "Sales Department",
    "criticality": "high",
    "status": "active",
    "performance_score": 0.85,
    "last_updated": "2024-01-01T00:00:00Z"
  }
]
```

### Get Processes by Goal

**GET** `/business-processes/by-goal/{goal_id}`

Retrieves all business processes associated with a specific goal.

**Permissions:** Viewer or higher

**Response:** `200 OK`
```json
[
  {
    "business_process_id": "uuid",
    "name": "Customer Order Processing",
    "process_type": "operational",
    "organizational_unit": "Sales Department",
    "criticality": "high",
    "status": "active",
    "performance_score": 0.85,
    "last_updated": "2024-01-01T00:00:00Z"
  }
]
```

### Get Processes by Status

**GET** `/business-processes/by-status/{status}`

Retrieves all business processes with a specific status.

**Permissions:** Viewer or higher

**Response:** `200 OK`
```json
[
  {
    "business_process_id": "uuid",
    "name": "Customer Order Processing",
    "process_type": "operational",
    "organizational_unit": "Sales Department",
    "criticality": "high",
    "status": "active",
    "performance_score": 0.85,
    "last_updated": "2024-01-01T00:00:00Z"
  }
]
```

### Get Processes by Criticality

**GET** `/business-processes/by-criticality/{criticality}`

Retrieves all business processes with a specific criticality level.

**Permissions:** Viewer or higher

**Response:** `200 OK`
```json
[
  {
    "business_process_id": "uuid",
    "name": "Customer Order Processing",
    "process_type": "operational",
    "organizational_unit": "Sales Department",
    "criticality": "high",
    "status": "active",
    "performance_score": 0.85,
    "last_updated": "2024-01-01T00:00:00Z"
  }
]
```

## Process Steps Endpoints

### Create Process Step

**POST** `/business-processes/{business_process_id}/steps/`

Creates a new process step.

**Permissions:** Editor or higher

**Request Body:**
```json
{
  "step_order": 1,
  "name": "Validate Order",
  "description": "Validate customer order details",
  "step_type": "task",
  "responsible_role_id": "uuid-optional",
  "responsible_actor_id": "uuid-optional",
  "duration_estimate": 0.5,
  "duration_actual": 0.4,
  "complexity": "medium",
  "performance_score": 0.90,
  "quality_score": 0.95,
  "efficiency_score": 0.85,
  "bottleneck_indicator": false,
  "automation_level": "automated",
  "approval_required": false
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "business_process_id": "uuid",
  "step_order": 1,
  "name": "Validate Order",
  "description": "Validate customer order details",
  "step_type": "task",
  "responsible_role_id": "uuid-optional",
  "responsible_actor_id": "uuid-optional",
  "duration_estimate": 0.5,
  "duration_actual": 0.4,
  "complexity": "medium",
  "performance_score": 0.90,
  "quality_score": 0.95,
  "efficiency_score": 0.85,
  "bottleneck_indicator": false,
  "automation_level": "automated",
  "approval_required": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### List Process Steps

**GET** `/business-processes/{business_process_id}/steps/`

Retrieves all steps for a business process.

**Permissions:** Viewer or higher

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "business_process_id": "uuid",
    "step_order": 1,
    "name": "Validate Order",
    "description": "Validate customer order details",
    "step_type": "task",
    "responsible_role_id": "uuid-optional",
    "responsible_actor_id": "uuid-optional",
    "duration_estimate": 0.5,
    "duration_actual": 0.4,
    "complexity": "medium",
    "performance_score": 0.90,
    "quality_score": 0.95,
    "efficiency_score": 0.85,
    "bottleneck_indicator": false,
    "automation_level": "automated",
    "approval_required": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### Update Process Step

**PUT** `/steps/{step_id}`

Updates a process step.

**Permissions:** Editor or higher

**Request Body:** (All fields optional)
```json
{
  "name": "Updated Step Name",
  "duration_actual": 0.3,
  "performance_score": 0.95
}
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "business_process_id": "uuid",
  "step_order": 1,
  "name": "Updated Step Name",
  "description": "Validate customer order details",
  "step_type": "task",
  "duration_actual": 0.3,
  "performance_score": 0.95,
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Delete Process Step

**DELETE** `/steps/{step_id}`

Deletes a process step.

**Permissions:** Editor or higher

**Response:** `204 No Content`

## Process Links Endpoints

### Create Process Link

**POST** `/business-processes/{business_process_id}/links/`

Creates a new process link to another ArchiMate element.

**Permissions:** Editor or higher

**Request Body:**
```json
{
  "linked_element_id": "uuid",
  "linked_element_type": "business_function",
  "link_type": "realizes",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "responsibility_level": "primary",
  "performance_impact": "high",
  "business_value_impact": "high",
  "risk_impact": "medium",
  "flow_direction": "bidirectional",
  "sequence_order": 1,
  "handoff_type": "automated"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "business_process_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "business_function",
  "link_type": "realizes",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "responsibility_level": "primary",
  "performance_impact": "high",
  "business_value_impact": "high",
  "risk_impact": "medium",
  "flow_direction": "bidirectional",
  "sequence_order": 1,
  "handoff_type": "automated",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### List Process Links

**GET** `/business-processes/{business_process_id}/links/`

Retrieves all links for a business process.

**Permissions:** Viewer or higher

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "business_process_id": "uuid",
    "linked_element_id": "uuid",
    "linked_element_type": "business_function",
    "link_type": "realizes",
    "relationship_strength": "strong",
    "dependency_level": "high",
    "interaction_frequency": "frequent",
    "interaction_type": "synchronous",
    "responsibility_level": "primary",
    "performance_impact": "high",
    "business_value_impact": "high",
    "risk_impact": "medium",
    "flow_direction": "bidirectional",
    "sequence_order": 1,
    "handoff_type": "automated",
    "created_by": "uuid",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Update Process Link

**PUT** `/links/{link_id}`

Updates a process link.

**Permissions:** Editor or higher

**Request Body:** (All fields optional)
```json
{
  "relationship_strength": "medium",
  "performance_impact": "medium"
}
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "business_process_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "business_function",
  "link_type": "realizes",
  "relationship_strength": "medium",
  "performance_impact": "medium",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Delete Process Link

**DELETE** `/links/{link_id}`

Deletes a process link.

**Permissions:** Editor or higher

**Response:** `204 No Content`

## Health and Metrics

### Health Check

**GET** `/health`

Returns the health status of the service.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "businessprocess_service",
  "version": "1.0.0",
  "timestamp": 1704067200.0
}
```

### Metrics

**GET** `/metrics`

Returns Prometheus metrics.

**Response:** `200 OK`
```
# HELP businessprocess_service_requests_total Total number of requests
# TYPE businessprocess_service_requests_total counter
businessprocess_service_requests_total{method="GET",endpoint="/api/v1/business-processes/",status="200"} 10

# HELP businessprocess_service_request_duration_seconds Request latency in seconds
# TYPE businessprocess_service_request_duration_seconds histogram
businessprocess_service_request_duration_seconds_bucket{method="GET",endpoint="/api/v1/business-processes/",le="0.1"} 8
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "name",
      "message": "Field required"
    }
  ]
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials",
  "headers": {
    "WWW-Authenticate": "Bearer"
  }
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Business process not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "error_type": "DatabaseError"
}
```

## Data Types

### Enums

#### ProcessType
- `operational`
- `management`
- `support`
- `strategic`

#### Criticality
- `low`
- `medium`
- `high`
- `critical`

#### Complexity
- `simple`
- `medium`
- `complex`
- `very_complex`

#### AutomationLevel
- `manual`
- `semi_automated`
- `automated`
- `fully_automated`

#### ProcessStatus
- `active`
- `inactive`
- `deprecated`
- `planned`

#### StepType
- `task`
- `decision`
- `handoff`
- `approval`
- `review`

#### LinkType
- `realizes`
- `supports`
- `uses`
- `produces`
- `consumes`
- `triggers`
- `enables`

## Rate Limiting

The API implements rate limiting to ensure fair usage:
- 100 requests per minute per user
- 1000 requests per hour per user
- Burst allowance of 10 requests per second

## Versioning

The API uses URL versioning:
- Current version: `/api/v1/`
- Future versions: `/api/v2/`, `/api/v3/`, etc.

## Deprecation Policy

- Deprecated endpoints will be marked with `@deprecated` in the OpenAPI spec
- Deprecated endpoints will return a `Deprecation` header
- Deprecated endpoints will be removed after 12 months
- Migration guides will be provided for breaking changes
