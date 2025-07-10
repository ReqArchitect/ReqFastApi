# API Reference: applicationfunction_service

## Overview

The Application Function Service provides comprehensive management of ArchiMate 3.2 Application Function elements with full CRUD operations, relationship management, analysis capabilities, and domain-specific queries.

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

## Application Function Management

### Create Application Function

**POST** `/application-functions`

Creates a new ApplicationFunction.

**Request Body:**
```json
{
  "name": "User Authentication Function",
  "description": "Handles user authentication and session management",
  "purpose": "Provide secure user authentication services",
  "technology_stack": "{\"framework\": \"Spring Security\", \"database\": \"PostgreSQL\"}",
  "module_location": "/auth-service/src/main/java/com/auth",
  "function_type": "user_session_manager",
  "performance_characteristics": "{\"response_time\": \"< 200ms\", \"throughput\": \"1000 req/s\"}",
  "response_time_target": 200.0,
  "throughput_target": 1000.0,
  "availability_target": 99.9,
  "business_criticality": "high",
  "business_value": "high",
  "status": "active",
  "operational_hours": "24x7",
  "maintenance_window": "Sunday 2-4 AM UTC",
  "api_endpoints": "{\"login\": \"/api/auth/login\", \"logout\": \"/api/auth/logout\"}",
  "data_sources": "{\"user_db\": \"users table\", \"session_store\": \"Redis\"}",
  "data_sinks": "{\"audit_log\": \"audit_events table\"}",
  "error_handling": "{\"retry\": \"3 attempts\", \"fallback\": \"cached credentials\"}",
  "logging_config": "{\"level\": \"INFO\", \"format\": \"JSON\"}",
  "security_level": "high",
  "compliance_requirements": "{\"gdpr\": true, \"sox\": true}",
  "access_controls": "{\"authentication\": \"required\", \"authorization\": \"role-based\"}",
  "audit_requirements": "{\"login_events\": true, \"access_logs\": true}",
  "monitoring_config": "{\"metrics\": \"prometheus\", \"alerts\": \"grafana\"}",
  "alerting_rules": "{\"high_error_rate\": \"> 5%\", \"slow_response\": \"> 500ms\"}",
  "health_check_endpoint": "/health",
  "metrics_endpoint": "/metrics",
  "parent_function_id": "uuid-optional",
  "application_service_id": "uuid-optional",
  "data_object_id": "uuid-optional",
  "node_id": "uuid-optional",
  "supported_business_function_id": "uuid-optional"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "name": "User Authentication Function",
  "description": "Handles user authentication and session management",
  "purpose": "Provide secure user authentication services",
  "technology_stack": "{\"framework\": \"Spring Security\", \"database\": \"PostgreSQL\"}",
  "module_location": "/auth-service/src/main/java/com/auth",
  "function_type": "user_session_manager",
  "performance_characteristics": "{\"response_time\": \"< 200ms\", \"throughput\": \"1000 req/s\"}",
  "response_time_target": 200.0,
  "throughput_target": 1000.0,
  "availability_target": 99.9,
  "current_availability": 100.0,
  "business_criticality": "high",
  "business_value": "high",
  "status": "active",
  "operational_hours": "24x7",
  "maintenance_window": "Sunday 2-4 AM UTC",
  "api_endpoints": "{\"login\": \"/api/auth/login\", \"logout\": \"/api/auth/logout\"}",
  "data_sources": "{\"user_db\": \"users table\", \"session_store\": \"Redis\"}",
  "data_sinks": "{\"audit_log\": \"audit_events table\"}",
  "error_handling": "{\"retry\": \"3 attempts\", \"fallback\": \"cached credentials\"}",
  "logging_config": "{\"level\": \"INFO\", \"format\": \"JSON\"}",
  "security_level": "high",
  "compliance_requirements": "{\"gdpr\": true, \"sox\": true}",
  "access_controls": "{\"authentication\": \"required\", \"authorization\": \"role-based\"}",
  "audit_requirements": "{\"login_events\": true, \"access_logs\": true}",
  "monitoring_config": "{\"metrics\": \"prometheus\", \"alerts\": \"grafana\"}",
  "alerting_rules": "{\"high_error_rate\": \"> 5%\", \"slow_response\": \"> 500ms\"}",
  "health_check_endpoint": "/health",
  "metrics_endpoint": "/metrics",
  "parent_function_id": null,
  "application_service_id": null,
  "data_object_id": null,
  "node_id": null,
  "supported_business_function_id": null,
  "last_maintenance": null,
  "next_maintenance": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### List Application Functions

**GET** `/application-functions`

Lists all ApplicationFunctions for the tenant with filtering and pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)
- `function_type` (string, optional): Filter by function type
- `status` (string, optional): Filter by status
- `business_criticality` (string, optional): Filter by business criticality
- `business_value` (string, optional): Filter by business value
- `supported_business_function_id` (UUID, optional): Filter by business function
- `technology_stack` (string, optional): Filter by technology stack (contains)
- `performance_threshold` (float, optional): Filter by minimum availability

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440002",
    "name": "User Authentication Function",
    "description": "Handles user authentication and session management",
    "purpose": "Provide secure user authentication services",
    "function_type": "user_session_manager",
    "business_criticality": "high",
    "business_value": "high",
    "status": "active",
    "operational_hours": "24x7",
    "availability_target": 99.9,
    "current_availability": 100.0,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Application Function

**GET** `/application-functions/{function_id}`

Retrieves an ApplicationFunction by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "name": "User Authentication Function",
  "description": "Handles user authentication and session management",
  "purpose": "Provide secure user authentication services",
  "technology_stack": "{\"framework\": \"Spring Security\", \"database\": \"PostgreSQL\"}",
  "module_location": "/auth-service/src/main/java/com/auth",
  "function_type": "user_session_manager",
  "performance_characteristics": "{\"response_time\": \"< 200ms\", \"throughput\": \"1000 req/s\"}",
  "response_time_target": 200.0,
  "throughput_target": 1000.0,
  "availability_target": 99.9,
  "current_availability": 100.0,
  "business_criticality": "high",
  "business_value": "high",
  "status": "active",
  "operational_hours": "24x7",
  "maintenance_window": "Sunday 2-4 AM UTC",
  "api_endpoints": "{\"login\": \"/api/auth/login\", \"logout\": \"/api/auth/logout\"}",
  "data_sources": "{\"user_db\": \"users table\", \"session_store\": \"Redis\"}",
  "data_sinks": "{\"audit_log\": \"audit_events table\"}",
  "error_handling": "{\"retry\": \"3 attempts\", \"fallback\": \"cached credentials\"}",
  "logging_config": "{\"level\": \"INFO\", \"format\": \"JSON\"}",
  "security_level": "high",
  "compliance_requirements": "{\"gdpr\": true, \"sox\": true}",
  "access_controls": "{\"authentication\": \"required\", \"authorization\": \"role-based\"}",
  "audit_requirements": "{\"login_events\": true, \"access_logs\": true}",
  "monitoring_config": "{\"metrics\": \"prometheus\", \"alerts\": \"grafana\"}",
  "alerting_rules": "{\"high_error_rate\": \"> 5%\", \"slow_response\": \"> 500ms\"}",
  "health_check_endpoint": "/health",
  "metrics_endpoint": "/metrics",
  "parent_function_id": null,
  "application_service_id": null,
  "data_object_id": null,
  "node_id": null,
  "supported_business_function_id": null,
  "last_maintenance": null,
  "next_maintenance": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Update Application Function

**PUT** `/application-functions/{function_id}`

Updates an ApplicationFunction.

**Request Body:** (All fields optional)
```json
{
  "name": "Enhanced User Authentication Function",
  "description": "Updated description with enhanced security features",
  "availability_target": 99.99,
  "security_level": "critical"
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Enhanced User Authentication Function",
  "description": "Updated description with enhanced security features",
  "availability_target": 99.99,
  "security_level": "critical",
  "updated_at": "2024-01-15T11:30:00Z"
}
```

### Delete Application Function

**DELETE** `/application-functions/{function_id}`

Deletes an ApplicationFunction.

**Response:** `204 No Content`

## Function Link Management

### Create Function Link

**POST** `/application-functions/{function_id}/links`

Creates a link between an application function and another element.

**Request Body:**
```json
{
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_type": "business_function",
  "link_type": "supports",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "data_flow_direction": "bidirectional",
  "performance_impact": "medium",
  "latency_contribution": 50.0,
  "throughput_impact": 5.0
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "application_function_id": "550e8400-e29b-41d4-a716-446655440000",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_type": "business_function",
  "link_type": "supports",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "data_flow_direction": "bidirectional",
  "performance_impact": "medium",
  "latency_contribution": 50.0,
  "throughput_impact": 5.0,
  "created_by": "550e8400-e29b-41d4-a716-446655440002",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### List Function Links

**GET** `/application-functions/{function_id}/links`

Lists all links for an application function.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440004",
    "application_function_id": "550e8400-e29b-41d4-a716-446655440000",
    "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
    "linked_element_type": "business_function",
    "link_type": "supports",
    "relationship_strength": "strong",
    "dependency_level": "high",
    "interaction_frequency": "frequent",
    "interaction_type": "synchronous",
    "data_flow_direction": "bidirectional",
    "performance_impact": "medium",
    "latency_contribution": 50.0,
    "throughput_impact": 5.0,
    "created_by": "550e8400-e29b-41d4-a716-446655440002",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Function Link

**GET** `/application-functions/links/{link_id}`

Retrieves a function link by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "application_function_id": "550e8400-e29b-41d4-a716-446655440000",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_type": "business_function",
  "link_type": "supports",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "data_flow_direction": "bidirectional",
  "performance_impact": "medium",
  "latency_contribution": 50.0,
  "throughput_impact": 5.0,
  "created_by": "550e8400-e29b-41d4-a716-446655440002",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Update Function Link

**PUT** `/application-functions/links/{link_id}`

Updates a function link.

**Request Body:** (All fields optional)
```json
{
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "performance_impact": "low"
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "performance_impact": "low"
}
```

### Delete Function Link

**DELETE** `/application-functions/links/{link_id}`

Deletes a function link.

**Response:** `204 No Content`

## Analysis & Impact Endpoints

### Get Impact Map

**GET** `/application-functions/{function_id}/impact-map`

Returns impact mapping for the ApplicationFunction.

**Response:** `200 OK`
```json
{
  "function_id": "550e8400-e29b-41d4-a716-446655440000",
  "direct_impacts": [
    {
      "element_id": "550e8400-e29b-41d4-a716-446655440003",
      "element_type": "business_function",
      "link_type": "supports",
      "relationship_strength": "strong",
      "dependency_level": "high",
      "performance_impact": "medium"
    }
  ],
  "indirect_impacts": [],
  "risk_assessment": {
    "business_criticality": "high",
    "business_value": "high",
    "security_level": "high",
    "availability_risk": 0.0,
    "dependency_count": 1
  },
  "dependency_chain": [
    {
      "element_id": "550e8400-e29b-41d4-a716-446655440003",
      "element_type": "business_function",
      "dependency_level": "high"
    }
  ],
  "total_impact_score": 0.85
}
```

### Get Performance Score

**GET** `/application-functions/{function_id}/performance-score`

Returns performance score for the ApplicationFunction.

**Response:** `200 OK`
```json
{
  "function_id": "550e8400-e29b-41d4-a716-446655440000",
  "response_time_score": 0.85,
  "throughput_score": 0.9,
  "availability_score": 1.0,
  "overall_score": 0.925,
  "recommendations": [
    "Consider implementing high availability patterns",
    "Optimize database queries and caching"
  ],
  "performance_metrics": {
    "response_time_target": 200.0,
    "throughput_target": 1000.0,
    "availability_target": 99.9,
    "current_availability": 100.0,
    "function_type": "user_session_manager",
    "operational_hours": "24x7"
  }
}
```

### Analyze Application Function

**GET** `/application-functions/{function_id}/analysis`

Returns comprehensive analysis for the ApplicationFunction.

**Response:** `200 OK`
```json
{
  "function_id": "550e8400-e29b-41d4-a716-446655440000",
  "operational_health": {
    "overall_score": 0.8,
    "issues": [],
    "status": "healthy"
  },
  "business_alignment": {
    "alignment_score": 0.7,
    "has_business_function": true,
    "business_criticality": "high",
    "business_value": "high"
  },
  "technical_debt": {
    "debt_score": 0.2,
    "debt_items": ["No technology stack documented"],
    "priority": "medium"
  },
  "risk_factors": [
    {
      "type": "business_criticality",
      "severity": "high",
      "description": "Critical business function with high availability requirements"
    }
  ],
  "improvement_opportunities": [
    "Document technology stack and dependencies",
    "Implement comprehensive monitoring and alerting"
  ],
  "compliance_status": {
    "compliance_rate": 0.75,
    "compliant_items": ["security_level", "monitoring"],
    "non_compliant_items": ["documentation"],
    "status": "needs_attention"
  }
}
```

## Domain-Specific Query Endpoints

### Get by Function Type

**GET** `/application-functions/by-type/{function_type}`

Returns application functions filtered by type.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "User Authentication Function",
    "function_type": "user_session_manager",
    "status": "active"
  }
]
```

### Get by Status

**GET** `/application-functions/by-status/{status}`

Returns application functions filtered by status.

### Get by Business Function

**GET** `/application-functions/by-business-function/{business_function_id}`

Returns application functions filtered by business function.

### Get by Performance

**GET** `/application-functions/by-performance/{performance_threshold}`

Returns application functions with availability above the threshold.

### Get by Element

**GET** `/application-functions/by-element/{element_type}/{element_id}`

Returns application functions linked to a specific element.

### Get Active Functions

**GET** `/application-functions/active`

Returns all active application functions.

### Get Critical Functions

**GET** `/application-functions/critical`

Returns all critical application functions.

## Enumeration Endpoints

### Get Function Types

**GET** `/application-functions/function-types`

Returns all available function types.

**Response:** `200 OK`
```json
[
  "data_processing",
  "orchestration",
  "user_interaction",
  "rule_engine",
  "etl_processor",
  "user_session_manager",
  "event_handler",
  "ui_controller"
]
```

### Get Statuses

**GET** `/application-functions/statuses`

Returns all available statuses.

**Response:** `200 OK`
```json
[
  "active",
  "inactive",
  "deprecated",
  "planned",
  "maintenance"
]
```

### Get Business Criticalities

**GET** `/application-functions/business-criticalities`

Returns all available business criticality levels.

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

**GET** `/application-functions/business-values`

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

**GET** `/application-functions/operational-hours`

Returns all available operational hour types.

**Response:** `200 OK`
```json
[
  "24x7",
  "business_hours",
  "on_demand"
]
```

### Get Security Levels

**GET** `/application-functions/security-levels`

Returns all available security levels.

**Response:** `200 OK`
```json
[
  "basic",
  "standard",
  "high",
  "critical"
]
```

### Get Link Types

**GET** `/application-functions/link-types`

Returns all available link types.

**Response:** `200 OK`
```json
[
  "realizes",
  "supports",
  "enables",
  "governs",
  "influences",
  "consumes",
  "produces",
  "triggers"
]
```

### Get Relationship Strengths

**GET** `/application-functions/relationship-strengths`

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

**GET** `/application-functions/dependency-levels`

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

**GET** `/application-functions/interaction-frequencies`

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

**GET** `/application-functions/interaction-types`

Returns all available interaction types.

**Response:** `200 OK`
```json
[
  "synchronous",
  "asynchronous",
  "batch",
  "real_time",
  "event_driven"
]
```

### Get Data Flow Directions

**GET** `/application-functions/data-flow-directions`

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

**GET** `/application-functions/performance-impacts`

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

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error: Invalid function type"
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
  "detail": "Insufficient permissions. Required: application_function:create, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Application function not found"
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
- Function type
- Status
- Business criticality
- Business value
- Supported business function
- Technology stack (contains)
- Performance threshold

## Sorting

Results are sorted by `created_at` in descending order by default.

## OpenAPI Documentation

For complete OpenAPI documentation, visit:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`
