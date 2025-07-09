# API Reference: goal_service

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

### POST /goals
Creates a new goal.

**Request:**
```json
{
  "name": "Digital Transformation Initiative",
  "description": "Transform business operations through digital technologies",
  "goal_type": "strategic",
  "priority": "high",
  "status": "active",
  "origin_driver_id": "uuid",
  "stakeholder_id": "uuid",
  "business_actor_id": "uuid",
  "success_criteria": "Complete migration to cloud-based systems",
  "key_performance_indicators": "[\"System uptime > 99.9%\", \"Response time < 2s\"]",
  "measurement_frequency": "monthly",
  "target_date": "2024-12-31T00:00:00Z",
  "start_date": "2024-01-01T00:00:00Z",
  "review_frequency": "quarterly",
  "progress_percentage": 25,
  "progress_notes": "Phase 1 completed successfully",
  "parent_goal_id": "uuid",
  "strategic_alignment": "high",
  "business_value": "high",
  "risk_level": "medium",
  "assessment_status": "in_progress",
  "assessment_score": 75,
  "assessment_notes": "On track with minor delays"
}
```

**Response:** 201
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "name": "Digital Transformation Initiative",
  "description": "Transform business operations through digital technologies",
  "goal_type": "strategic",
  "priority": "high",
  "status": "active",
  "origin_driver_id": "uuid",
  "stakeholder_id": "uuid",
  "business_actor_id": "uuid",
  "success_criteria": "Complete migration to cloud-based systems",
  "key_performance_indicators": "[\"System uptime > 99.9%\", \"Response time < 2s\"]",
  "measurement_frequency": "monthly",
  "target_date": "2024-12-31T00:00:00Z",
  "start_date": "2024-01-01T00:00:00Z",
  "review_frequency": "quarterly",
  "progress_percentage": 25,
  "progress_notes": "Phase 1 completed successfully",
  "parent_goal_id": "uuid",
  "strategic_alignment": "high",
  "business_value": "high",
  "risk_level": "medium",
  "assessment_status": "in_progress",
  "assessment_score": 75,
  "assessment_notes": "On track with minor delays",
  "last_progress_update": null,
  "last_assessment_date": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### GET /goals
Lists goals with filtering and pagination.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 100, max: 1000)
- `goal_type`: Filter by goal type
- `priority`: Filter by priority
- `status`: Filter by status
- `stakeholder_id`: Filter by stakeholder
- `business_actor_id`: Filter by business actor
- `origin_driver_id`: Filter by origin driver
- `parent_goal_id`: Filter by parent goal

**Response:** 200
```json
[
  {
    "id": "uuid",
    "tenant_id": "uuid",
    "user_id": "uuid",
    "name": "Digital Transformation Initiative",
    "description": "Transform business operations through digital technologies",
    "goal_type": "strategic",
    "priority": "high",
    "status": "active",
    "origin_driver_id": "uuid",
    "stakeholder_id": "uuid",
    "business_actor_id": "uuid",
    "success_criteria": "Complete migration to cloud-based systems",
    "key_performance_indicators": "[\"System uptime > 99.9%\", \"Response time < 2s\"]",
    "measurement_frequency": "monthly",
    "target_date": "2024-12-31T00:00:00Z",
    "start_date": "2024-01-01T00:00:00Z",
    "review_frequency": "quarterly",
    "progress_percentage": 25,
    "progress_notes": "Phase 1 completed successfully",
    "parent_goal_id": "uuid",
    "strategic_alignment": "high",
    "business_value": "high",
    "risk_level": "medium",
    "assessment_status": "in_progress",
    "assessment_score": 75,
    "assessment_notes": "On track with minor delays",
    "last_progress_update": null,
    "last_assessment_date": null,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### GET /goals/{id}
Retrieves a specific goal.

**Response:** 200
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "name": "Digital Transformation Initiative",
  "description": "Transform business operations through digital technologies",
  "goal_type": "strategic",
  "priority": "high",
  "status": "active",
  "origin_driver_id": "uuid",
  "stakeholder_id": "uuid",
  "business_actor_id": "uuid",
  "success_criteria": "Complete migration to cloud-based systems",
  "key_performance_indicators": "[\"System uptime > 99.9%\", \"Response time < 2s\"]",
  "measurement_frequency": "monthly",
  "target_date": "2024-12-31T00:00:00Z",
  "start_date": "2024-01-01T00:00:00Z",
  "review_frequency": "quarterly",
  "progress_percentage": 25,
  "progress_notes": "Phase 1 completed successfully",
  "parent_goal_id": "uuid",
  "strategic_alignment": "high",
  "business_value": "high",
  "risk_level": "medium",
  "assessment_status": "in_progress",
  "assessment_score": 75,
  "assessment_notes": "On track with minor delays",
  "last_progress_update": null,
  "last_assessment_date": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### PUT /goals/{id}
Updates a goal.

**Request:**
```json
{
  "name": "Updated Digital Transformation Initiative",
  "progress_percentage": 50,
  "assessment_status": "completed"
}
```

**Response:** 200
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "name": "Updated Digital Transformation Initiative",
  "description": "Transform business operations through digital technologies",
  "goal_type": "strategic",
  "priority": "high",
  "status": "active",
  "origin_driver_id": "uuid",
  "stakeholder_id": "uuid",
  "business_actor_id": "uuid",
  "success_criteria": "Complete migration to cloud-based systems",
  "key_performance_indicators": "[\"System uptime > 99.9%\", \"Response time < 2s\"]",
  "measurement_frequency": "monthly",
  "target_date": "2024-12-31T00:00:00Z",
  "start_date": "2024-01-01T00:00:00Z",
  "review_frequency": "quarterly",
  "progress_percentage": 50,
  "progress_notes": "Phase 1 completed successfully",
  "parent_goal_id": "uuid",
  "strategic_alignment": "high",
  "business_value": "high",
  "risk_level": "medium",
  "assessment_status": "completed",
  "assessment_score": 75,
  "assessment_notes": "On track with minor delays",
  "last_progress_update": null,
  "last_assessment_date": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T01:00:00Z"
}
```

### DELETE /goals/{id}
Deletes a goal.

**Response:** 204

## Link Management

### POST /goals/{id}/links
Creates a link between a goal and another element.

**Request:**
```json
{
  "linked_element_id": "uuid",
  "linked_element_type": "requirement",
  "link_type": "realizes",
  "relationship_strength": "strong",
  "contribution_level": "high"
}
```

**Response:** 201
```json
{
  "id": "uuid",
  "goal_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "requirement",
  "link_type": "realizes",
  "relationship_strength": "strong",
  "contribution_level": "high",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### GET /goals/{id}/links
Lists all links for a goal.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "goal_id": "uuid",
    "linked_element_id": "uuid",
    "linked_element_type": "requirement",
    "link_type": "realizes",
    "relationship_strength": "strong",
    "contribution_level": "high",
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
  "goal_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "requirement",
  "link_type": "realizes",
  "relationship_strength": "strong",
  "contribution_level": "high",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### PUT /links/{link_id}
Updates a link.

**Request:**
```json
{
  "link_type": "supports",
  "contribution_level": "medium"
}
```

**Response:** 200
```json
{
  "id": "uuid",
  "goal_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "requirement",
  "link_type": "supports",
  "relationship_strength": "strong",
  "contribution_level": "medium",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### DELETE /links/{link_id}
Deletes a link.

**Response:** 204

## Analysis Endpoints

### GET /goals/{id}/realization-map
Gets realization map for a goal.

**Response:** 200
```json
{
  "goal_id": "uuid",
  "linked_elements_count": 5,
  "requirements_count": 2,
  "capabilities_count": 1,
  "courses_of_action_count": 1,
  "stakeholders_count": 1,
  "assessments_count": 0,
  "overall_realization_score": 0.8,
  "last_assessed": "2024-01-01T00:00:00Z"
}
```

### GET /goals/{id}/status-summary
Gets status summary for a goal.

**Response:** 200
```json
{
  "goal_id": "uuid",
  "status": "active",
  "progress_percentage": 50,
  "days_until_target": 180,
  "assessment_score": 75,
  "risk_level": "medium",
  "strategic_alignment": "high",
  "business_value": "high",
  "linked_elements_count": 5,
  "last_updated": "2024-01-01T00:00:00Z"
}
```

### GET /goals/{id}/analysis
Analyzes a goal for strategic insights.

**Response:** 200
```json
{
  "goal_id": "uuid",
  "priority_score": 0.75,
  "progress_score": 0.5,
  "risk_score": 0.5,
  "strategic_alignment_score": 1.0,
  "business_value_score": 1.0,
  "overall_health_score": 0.75,
  "last_analyzed": "2024-01-01T00:00:00Z"
}
```

## Domain-Specific Query Endpoints

### GET /goals/by-type/{type}
Returns goals filtered by type.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "goal_type": "strategic",
    "priority": "high",
    "status": "active"
  }
]
```

### GET /goals/by-priority/{priority}
Returns goals filtered by priority.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "goal_type": "strategic",
    "priority": "high",
    "status": "active"
  }
]
```

### GET /goals/by-status/{status}
Returns goals filtered by status.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "goal_type": "strategic",
    "priority": "high",
    "status": "active"
  }
]
```

### GET /goals/by-stakeholder/{stakeholder_id}
Returns goals associated with a specific stakeholder.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "goal_type": "strategic",
    "stakeholder_id": "uuid"
  }
]
```

### GET /goals/by-business-actor/{business_actor_id}
Returns goals associated with a specific business actor.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "goal_type": "strategic",
    "business_actor_id": "uuid"
  }
]
```

### GET /goals/by-driver/{driver_id}
Returns goals associated with a specific driver.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "goal_type": "strategic",
    "origin_driver_id": "uuid"
  }
]
```

### GET /goals/by-element/{element_type}/{element_id}
Returns goals that are linked to a specific element.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "goal_type": "strategic",
    "priority": "high"
  }
]
```

### GET /goals/active
Returns active goals.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "goal_type": "strategic",
    "status": "active"
  }
]
```

### GET /goals/achieved
Returns achieved goals.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "goal_type": "strategic",
    "status": "achieved"
  }
]
```

### GET /goals/due-soon/{days_ahead}
Returns goals that are due soon.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "goal_type": "strategic",
    "target_date": "2024-02-01T00:00:00Z"
  }
]
```

### GET /goals/high-priority
Returns high priority goals.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "goal_type": "strategic",
    "priority": "high"
  }
]
```

### GET /goals/by-progress/{min_progress}/{max_progress}
Returns goals within a progress range.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "Digital Transformation Initiative",
    "goal_type": "strategic",
    "progress_percentage": 50
  }
]
```

## Utility Endpoints

### GET /goals/types
Returns available goal types.

**Response:** 200
```json
["strategic", "operational", "technical", "tactical"]
```

### GET /goals/priorities
Returns available priorities.

**Response:** 200
```json
["low", "medium", "high", "critical"]
```

### GET /goals/statuses
Returns available statuses.

**Response:** 200
```json
["active", "achieved", "abandoned", "on_hold"]
```

### GET /goals/measurement-frequencies
Returns available measurement frequencies.

**Response:** 200
```json
["daily", "weekly", "monthly", "quarterly", "annually"]
```

### GET /goals/review-frequencies
Returns available review frequencies.

**Response:** 200
```json
["monthly", "quarterly", "annually", "ad_hoc"]
```

### GET /goals/strategic-alignments
Returns available strategic alignments.

**Response:** 200
```json
["high", "medium", "low"]
```

### GET /goals/business-values
Returns available business values.

**Response:** 200
```json
["high", "medium", "low"]
```

### GET /goals/risk-levels
Returns available risk levels.

**Response:** 200
```json
["low", "medium", "high", "critical"]
```

### GET /goals/assessment-statuses
Returns available assessment statuses.

**Response:** 200
```json
["pending", "in_progress", "completed", "failed"]
```

### GET /goals/link-types
Returns available link types.

**Response:** 200
```json
["realizes", "supports", "enables", "governs", "influences"]
```

### GET /goals/relationship-strengths
Returns available relationship strengths.

**Response:** 200
```json
["strong", "medium", "weak"]
```

### GET /goals/contribution-levels
Returns available contribution levels.

**Response:** 200
```json
["high", "medium", "low"]
```

## System Endpoints

### GET /health
Health check endpoint.

**Response:** 200
```json
{
  "service": "goal_service",
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
# HELP goal_service_requests_total Total requests
# TYPE goal_service_requests_total counter
goal_service_requests_total{method="GET",route="/health",status="200"} 1000
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
  "detail": "Insufficient permissions. Required: goal:create, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Goal not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Data Types

### Goal Types
- `strategic`: Strategic goals
- `operational`: Operational goals
- `technical`: Technical goals
- `tactical`: Tactical goals

### Priorities
- `low`: Low priority
- `medium`: Medium priority
- `high`: High priority
- `critical`: Critical priority

### Statuses
- `active`: Active status
- `achieved`: Achieved status
- `abandoned`: Abandoned status
- `on_hold`: On hold status

### Measurement Frequencies
- `daily`: Daily measurement
- `weekly`: Weekly measurement
- `monthly`: Monthly measurement
- `quarterly`: Quarterly measurement
- `annually`: Annual measurement

### Review Frequencies
- `monthly`: Monthly review
- `quarterly`: Quarterly review
- `annually`: Annual review
- `ad_hoc`: Ad hoc review

### Strategic Alignments
- `high`: High alignment
- `medium`: Medium alignment
- `low`: Low alignment

### Business Values
- `high`: High value
- `medium`: Medium value
- `low`: Low value

### Risk Levels
- `low`: Low risk
- `medium`: Medium risk
- `high`: High risk
- `critical`: Critical risk

### Assessment Statuses
- `pending`: Pending assessment
- `in_progress`: Assessment in progress
- `completed`: Assessment completed
- `failed`: Assessment failed

### Link Types
- `realizes`: Realizes relationship
- `supports`: Supports relationship
- `enables`: Enables relationship
- `governs`: Governs relationship
- `influences`: Influences relationship

### Relationship Strengths
- `strong`: Strong relationship
- `medium`: Medium relationship
- `weak`: Weak relationship

### Contribution Levels
- `high`: High contribution
- `medium`: Medium contribution
- `low`: Low contribution 