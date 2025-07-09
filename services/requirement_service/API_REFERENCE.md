# API Reference: requirement_service

## Authentication

All endpoints require JWT authentication via the `Authorization` header:
```
Authorization: Bearer <jwt_token>
```

The JWT token must contain:
- `user_id`: User identifier
- `tenant_id`: Tenant identifier
- `role`: User role (Owner, Admin, Editor, Viewer)

## Core Endpoints

### POST /requirements
Creates a new requirement.

**Request:**
```json
{
  "name": "User Authentication Required",
  "description": "All users must authenticate before accessing the system",
  "requirement_type": "functional",
  "priority": "high",
  "status": "draft",
  "source": "Security Policy",
  "stakeholder_id": "uuid",
  "business_case_id": "uuid",
  "initiative_id": "uuid",
  "acceptance_criteria": "Users must provide valid credentials",
  "validation_method": "test",
  "compliance_required": true
}
```

**Response:** 201
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "name": "User Authentication Required",
  "description": "All users must authenticate before accessing the system",
  "requirement_type": "functional",
  "priority": "high",
  "status": "draft",
  "source": "Security Policy",
  "stakeholder_id": "uuid",
  "business_case_id": "uuid",
  "initiative_id": "uuid",
  "acceptance_criteria": "Users must provide valid credentials",
  "validation_method": "test",
  "compliance_required": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### GET /requirements
Lists requirements with filtering and pagination.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 100, max: 1000)
- `requirement_type`: Filter by requirement type
- `status`: Filter by status
- `priority`: Filter by priority

**Response:** 200
```json
[
  {
    "id": "uuid",
    "tenant_id": "uuid",
    "user_id": "uuid",
    "name": "User Authentication Required",
    "description": "All users must authenticate before accessing the system",
    "requirement_type": "functional",
    "priority": "high",
    "status": "draft",
    "source": "Security Policy",
    "stakeholder_id": "uuid",
    "business_case_id": "uuid",
    "initiative_id": "uuid",
    "acceptance_criteria": "Users must provide valid credentials",
    "validation_method": "test",
    "compliance_required": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### GET /requirements/{id}
Retrieves a specific requirement.

**Response:** 200
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "name": "User Authentication Required",
  "description": "All users must authenticate before accessing the system",
  "requirement_type": "functional",
  "priority": "high",
  "status": "draft",
  "source": "Security Policy",
  "stakeholder_id": "uuid",
  "business_case_id": "uuid",
  "initiative_id": "uuid",
  "acceptance_criteria": "Users must provide valid credentials",
  "validation_method": "test",
  "compliance_required": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### PUT /requirements/{id}
Updates a requirement.

**Request:**
```json
{
  "name": "Updated User Authentication Required",
  "status": "active",
  "priority": "critical"
}
```

**Response:** 200
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "name": "Updated User Authentication Required",
  "description": "All users must authenticate before accessing the system",
  "requirement_type": "functional",
  "priority": "critical",
  "status": "active",
  "source": "Security Policy",
  "stakeholder_id": "uuid",
  "business_case_id": "uuid",
  "initiative_id": "uuid",
  "acceptance_criteria": "Users must provide valid credentials",
  "validation_method": "test",
  "compliance_required": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T01:00:00Z"
}
```

### DELETE /requirements/{id}
Deletes a requirement.

**Response:** 204

## Link Management

### POST /requirements/{id}/links
Creates a link between a requirement and another element.

**Request:**
```json
{
  "linked_element_id": "uuid",
  "linked_element_type": "capability",
  "link_type": "implements",
  "link_strength": "strong"
}
```

**Response:** 201
```json
{
  "id": "uuid",
  "requirement_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "capability",
  "link_type": "implements",
  "link_strength": "strong",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### GET /requirements/{id}/links
Lists all links for a requirement.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "requirement_id": "uuid",
    "linked_element_id": "uuid",
    "linked_element_type": "capability",
    "link_type": "implements",
    "link_strength": "strong",
    "created_by": "uuid",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### GET /links/{link_id}
Retrieves a specific link.

**Response:** 200
```json
{
  "id": "uuid",
  "requirement_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "capability",
  "link_type": "implements",
  "link_strength": "strong",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### PUT /links/{link_id}
Updates a link.

**Request:**
```json
{
  "link_type": "depends_on",
  "link_strength": "medium"
}
```

**Response:** 200
```json
{
  "id": "uuid",
  "requirement_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "capability",
  "link_type": "depends_on",
  "link_strength": "medium",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### DELETE /links/{link_id}
Deletes a link.

**Response:** 204

## Analysis Endpoints

### GET /requirements/{id}/traceability-check
Checks traceability status for a requirement.

**Response:** 200
```json
{
  "requirement_id": "uuid",
  "linked_elements_count": 3,
  "compliance_status": "compliant",
  "validation_status": "validated",
  "last_updated": "2024-01-01T00:00:00Z"
}
```

### GET /requirements/{id}/impact-summary
Gets impact analysis for a requirement.

**Response:** 200
```json
{
  "requirement_id": "uuid",
  "direct_impact_count": 3,
  "indirect_impact_count": 0,
  "affected_layers": ["Strategy", "Business"],
  "risk_level": "high",
  "last_assessed": "2024-01-01T00:00:00Z"
}
```

## Utility Endpoints

### GET /requirements/types
Returns available requirement types.

**Response:** 200
```json
["functional", "non-functional", "business", "technical"]
```

### GET /requirements/priorities
Returns available priorities.

**Response:** 200
```json
["low", "medium", "high", "critical"]
```

### GET /requirements/statuses
Returns available statuses.

**Response:** 200
```json
["draft", "active", "completed", "deprecated"]
```

### GET /requirements/link-types
Returns available link types.

**Response:** 200
```json
["implements", "depends_on", "conflicts_with", "enhances"]
```

### GET /requirements/link-strengths
Returns available link strengths.

**Response:** 200
```json
["weak", "medium", "strong"]
```

## System Endpoints

### GET /health
Health check endpoint.

**Response:** 200
```json
{
  "service": "requirement_service",
  "version": "1.0.0",
  "status": "healthy",
  "uptime": "3600.00s",
  "total_requests": 1000,
  "error_rate": 0.01,
  "database_connected": true,
  "timestamp": "2024-01-01T00:00:00Z",
  "environment": "production"
}
```

### GET /metrics
Prometheus metrics endpoint.

**Response:** 200 (text/plain)
```
# HELP requirement_service_requests_total Total requests
# TYPE requirement_service_requests_total counter
requirement_service_requests_total{method="GET",route="/health",status="200"} 1000
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error"
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
  "detail": "Insufficient permissions. Required: requirement:create, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Requirement not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Data Types

### Requirement Types
- `functional`: Functional requirements
- `non-functional`: Non-functional requirements
- `business`: Business requirements
- `technical`: Technical requirements

### Priorities
- `low`: Low priority
- `medium`: Medium priority
- `high`: High priority
- `critical`: Critical priority

### Statuses
- `draft`: Draft status
- `active`: Active status
- `completed`: Completed status
- `deprecated`: Deprecated status

### Link Types
- `implements`: Implements relationship
- `depends_on`: Depends on relationship
- `conflicts_with`: Conflicts with relationship
- `enhances`: Enhances relationship

### Link Strengths
- `weak`: Weak relationship
- `medium`: Medium relationship
- `strong`: Strong relationship 