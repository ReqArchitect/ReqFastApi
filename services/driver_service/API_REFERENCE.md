# API Reference: driver_service

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

### POST /drivers
Creates a new driver.

**Request:**
```json
{
  "name": "Digital Transformation Initiative",
  "description": "Market pressure to adopt digital technologies",
  "driver_type": "business",
  "category": "external",
  "urgency": "high",
  "impact_level": "high",
  "source": "Market Analysis",
  "stakeholder_id": "uuid",
  "business_actor_id": "uuid",
  "strategic_priority": 4,
  "time_horizon": "medium-term",
  "geographic_scope": "global",
  "compliance_required": false,
  "risk_level": "medium"
}
```

**Response:** 201
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "name": "Digital Transformation Initiative",
  "description": "Market pressure to adopt digital technologies",
  "driver_type": "business",
  "category": "external",
  "urgency": "high",
  "impact_level": "high",
  "source": "Market Analysis",
  "stakeholder_id": "uuid",
  "business_actor_id": "uuid",
  "strategic_priority": 4,
  "time_horizon": "medium-term",
  "geographic_scope": "global",
  "compliance_required": false,
  "risk_level": "medium",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### GET /drivers
Lists drivers with filtering and pagination.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 100, max: 1000)
- `driver_type`: Filter by driver type
- `category`: Filter by category
- `urgency`: Filter by urgency
- `impact_level`: Filter by impact level
- `stakeholder_id`: Filter by stakeholder
- `business_actor_id`: Filter by business actor

**Response:** 200
```json
[
  {
    "id": "uuid",
    "tenant_id": "uuid",
    "user_id": "uuid",
    "name": "Digital Transformation Initiative",
    "description": "Market pressure to adopt digital technologies",
    "driver_type": "business",
    "category": "external",
    "urgency": "high",
    "impact_level": "high",
    "source": "Market Analysis",
    "stakeholder_id": "uuid",
    "business_actor_id": "uuid",
    "strategic_priority": 4,
    "time_horizon": "medium-term",
    "geographic_scope": "global",
    "compliance_required": false,
    "risk_level": "medium",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### GET /drivers/{id}
Retrieves a specific driver.

**Response:** 200
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "name": "Digital Transformation Initiative",
  "description": "Market pressure to adopt digital technologies",
  "driver_type": "business",
  "category": "external",
  "urgency": "high",
  "impact_level": "high",
  "source": "Market Analysis",
  "stakeholder_id": "uuid",
  "business_actor_id": "uuid",
  "strategic_priority": 4,
  "time_horizon": "medium-term",
  "geographic_scope": "global",
  "compliance_required": false,
  "risk_level": "medium",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### PUT /drivers/{id}
Updates a driver.

**Request:**
```json
{
  "name": "Updated Digital Transformation Initiative",
  "urgency": "critical",
  "strategic_priority": 5
}
```

**Response:** 200
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "name": "Updated Digital Transformation Initiative",
  "description": "Market pressure to adopt digital technologies",
  "driver_type": "business",
  "category": "external",
  "urgency": "critical",
  "impact_level": "high",
  "source": "Market Analysis",
  "stakeholder_id": "uuid",
  "business_actor_id": "uuid",
  "strategic_priority": 5,
  "time_horizon": "medium-term",
  "geographic_scope": "global",
  "compliance_required": false,
  "risk_level": "medium",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T01:00:00Z"
}
```

### DELETE /drivers/{id}
Deletes a driver.

**Response:** 204

## Link Management

### POST /drivers/{id}/links
Creates a link between a driver and another element.

**Request:**
```json
{
  "linked_element_id": "uuid",
  "linked_element_type": "goal",
  "link_type": "influences",
  "link_strength": "strong",
  "influence_direction": "positive"
}
```

**Response:** 201
```json
{
  "id": "uuid",
  "driver_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "goal",
  "link_type": "influences",
  "link_strength": "strong",
  "influence_direction": "positive",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### GET /drivers/{id}/links
Lists all links for a driver.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "driver_id": "uuid",
    "linked_element_id": "uuid",
    "linked_element_type": "goal",
    "link_type": "influences",
    "link_strength": "strong",
    "influence_direction": "positive",
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
  "driver_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "goal",
  "link_type": "influences",
  "link_strength": "strong",
  "influence_direction": "positive",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### PUT /links/{link_id}
Updates a link.

**Request:**
```json
{
  "link_type": "drives",
  "influence_direction": "negative"
}
```

**Response:** 200
```json
{
  "id": "uuid",
  "driver_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "goal",
  "link_type": "drives",
  "link_strength": "strong",
  "influence_direction": "negative",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### DELETE /links/{link_id}
Deletes a link.

**Response:** 204

## Analysis Endpoints

### GET /drivers/{id}/influence-map
Gets influence map for a driver.

**Response:** 200
```json
{
  "driver_id": "uuid",
  "influenced_elements_count": 5,
  "positive_influences": 3,
  "negative_influences": 1,
  "neutral_influences": 1,
  "affected_layers": ["Motivation", "Strategy", "Business"],
  "strategic_impact_score": 4.2,
  "last_assessed": "2024-01-01T00:00:00Z"
}
```

### GET /drivers/{id}/analysis
Analyzes a driver for strategic insights.

**Response:** 200
```json
{
  "driver_id": "uuid",
  "urgency_score": 0.75,
  "impact_score": 0.75,
  "risk_score": 0.5,
  "compliance_status": "non-applicable",
  "strategic_alignment": "high",
  "time_pressure": "high",
  "last_analyzed": "2024-01-01T00:00:00Z"
}
```

## Domain-Specific Query Endpoints

### GET /drivers/by-urgency/{urgency}
Returns drivers filtered by urgency.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "driver_type": "business",
    "urgency": "high",
    "impact_level": "high"
  }
]
```

### GET /drivers/by-category/{category}
Returns drivers filtered by category.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "driver_type": "business",
    "category": "external",
    "urgency": "high"
  }
]
```

### GET /drivers/by-stakeholder/{stakeholder_id}
Returns drivers associated with a specific stakeholder.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "driver_type": "business",
    "stakeholder_id": "uuid"
  }
]
```

### GET /drivers/by-business-actor/{business_actor_id}
Returns drivers associated with a specific business actor.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "driver_type": "business",
    "business_actor_id": "uuid"
  }
]
```

### GET /drivers/by-goal/{goal_id}
Returns drivers that influence a specific goal.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "driver_type": "business",
    "urgency": "high"
  }
]
```

### GET /drivers/by-requirement/{requirement_id}
Returns drivers that influence a specific requirement.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "driver_type": "business",
    "urgency": "high"
  }
]
```

## Utility Endpoints

### GET /drivers/types
Returns available driver types.

**Response:** 200
```json
["business", "technical", "regulatory", "environmental", "social"]
```

### GET /drivers/categories
Returns available categories.

**Response:** 200
```json
["internal", "external", "strategic", "operational"]
```

### GET /drivers/urgencies
Returns available urgencies.

**Response:** 200
```json
["low", "medium", "high", "critical"]
```

### GET /drivers/impact-levels
Returns available impact levels.

**Response:** 200
```json
["low", "medium", "high", "critical"]
```

### GET /drivers/time-horizons
Returns available time horizons.

**Response:** 200
```json
["short-term", "medium-term", "long-term"]
```

### GET /drivers/geographic-scopes
Returns available geographic scopes.

**Response:** 200
```json
["local", "regional", "national", "global"]
```

### GET /drivers/risk-levels
Returns available risk levels.

**Response:** 200
```json
["low", "medium", "high", "critical"]
```

### GET /drivers/link-types
Returns available link types.

**Response:** 200
```json
["influences", "drives", "constrains", "enables"]
```

### GET /drivers/link-strengths
Returns available link strengths.

**Response:** 200
```json
["weak", "medium", "strong"]
```

### GET /drivers/influence-directions
Returns available influence directions.

**Response:** 200
```json
["positive", "negative", "neutral"]
```

## System Endpoints

### GET /health
Health check endpoint.

**Response:** 200
```json
{
  "service": "driver_service",
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
# HELP driver_service_requests_total Total requests
# TYPE driver_service_requests_total counter
driver_service_requests_total{method="GET",route="/health",status="200"} 1000
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
  "detail": "Insufficient permissions. Required: driver:create, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Driver not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Data Types

### Driver Types
- `business`: Business drivers
- `technical`: Technical drivers
- `regulatory`: Regulatory drivers
- `environmental`: Environmental drivers
- `social`: Social drivers

### Categories
- `internal`: Internal drivers
- `external`: External drivers
- `strategic`: Strategic drivers
- `operational`: Operational drivers

### Urgencies
- `low`: Low urgency
- `medium`: Medium urgency
- `high`: High urgency
- `critical`: Critical urgency

### Impact Levels
- `low`: Low impact
- `medium`: Medium impact
- `high`: High impact
- `critical`: Critical impact

### Time Horizons
- `short-term`: Short-term drivers
- `medium-term`: Medium-term drivers
- `long-term`: Long-term drivers

### Geographic Scopes
- `local`: Local scope
- `regional`: Regional scope
- `national`: National scope
- `global`: Global scope

### Risk Levels
- `low`: Low risk
- `medium`: Medium risk
- `high`: High risk
- `critical`: Critical risk

### Link Types
- `influences`: Influences relationship
- `drives`: Drives relationship
- `constrains`: Constrains relationship
- `enables`: Enables relationship

### Link Strengths
- `weak`: Weak relationship
- `medium`: Medium relationship
- `strong`: Strong relationship

### Influence Directions
- `positive`: Positive influence
- `negative`: Negative influence
- `neutral`: Neutral influence 