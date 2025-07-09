# API Reference: constraint_service

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

### POST /constraints
Creates a new constraint.

**Request:**
```json
{
  "name": "GDPR Data Protection",
  "description": "European data protection regulation compliance",
  "constraint_type": "regulatory",
  "scope": "global",
  "severity": "high",
  "enforcement_level": "mandatory",
  "stakeholder_id": "uuid",
  "business_actor_id": "uuid",
  "risk_profile": "high",
  "compliance_required": true,
  "regulatory_framework": "GDPR",
  "mitigation_strategy": "Implement data encryption and access controls",
  "mitigation_status": "in_progress",
  "mitigation_effort": "high",
  "business_impact": "high",
  "technical_impact": "medium",
  "operational_impact": "medium",
  "effective_date": "2024-01-01T00:00:00Z",
  "expiry_date": "2025-01-01T00:00:00Z",
  "review_frequency": "quarterly"
}
```

**Response:** 201
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "name": "GDPR Data Protection",
  "description": "European data protection regulation compliance",
  "constraint_type": "regulatory",
  "scope": "global",
  "severity": "high",
  "enforcement_level": "mandatory",
  "stakeholder_id": "uuid",
  "business_actor_id": "uuid",
  "risk_profile": "high",
  "compliance_required": true,
  "regulatory_framework": "GDPR",
  "mitigation_strategy": "Implement data encryption and access controls",
  "mitigation_status": "in_progress",
  "mitigation_effort": "high",
  "business_impact": "high",
  "technical_impact": "medium",
  "operational_impact": "medium",
  "effective_date": "2024-01-01T00:00:00Z",
  "expiry_date": "2025-01-01T00:00:00Z",
  "review_frequency": "quarterly",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### GET /constraints
Lists constraints with filtering and pagination.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 100, max: 1000)
- `constraint_type`: Filter by constraint type
- `scope`: Filter by scope
- `severity`: Filter by severity
- `enforcement_level`: Filter by enforcement level
- `stakeholder_id`: Filter by stakeholder
- `business_actor_id`: Filter by business actor
- `compliance_required`: Filter by compliance requirement

**Response:** 200
```json
[
  {
    "id": "uuid",
    "tenant_id": "uuid",
    "user_id": "uuid",
    "name": "GDPR Data Protection",
    "description": "European data protection regulation compliance",
    "constraint_type": "regulatory",
    "scope": "global",
    "severity": "high",
    "enforcement_level": "mandatory",
    "stakeholder_id": "uuid",
    "business_actor_id": "uuid",
    "risk_profile": "high",
    "compliance_required": true,
    "regulatory_framework": "GDPR",
    "mitigation_strategy": "Implement data encryption and access controls",
    "mitigation_status": "in_progress",
    "mitigation_effort": "high",
    "business_impact": "high",
    "technical_impact": "medium",
    "operational_impact": "medium",
    "effective_date": "2024-01-01T00:00:00Z",
    "expiry_date": "2025-01-01T00:00:00Z",
    "review_frequency": "quarterly",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### GET /constraints/{id}
Retrieves a specific constraint.

**Response:** 200
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "name": "GDPR Data Protection",
  "description": "European data protection regulation compliance",
  "constraint_type": "regulatory",
  "scope": "global",
  "severity": "high",
  "enforcement_level": "mandatory",
  "stakeholder_id": "uuid",
  "business_actor_id": "uuid",
  "risk_profile": "high",
  "compliance_required": true,
  "regulatory_framework": "GDPR",
  "mitigation_strategy": "Implement data encryption and access controls",
  "mitigation_status": "in_progress",
  "mitigation_effort": "high",
  "business_impact": "high",
  "technical_impact": "medium",
  "operational_impact": "medium",
  "effective_date": "2024-01-01T00:00:00Z",
  "expiry_date": "2025-01-01T00:00:00Z",
  "review_frequency": "quarterly",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### PUT /constraints/{id}
Updates a constraint.

**Request:**
```json
{
  "name": "Updated GDPR Data Protection",
  "severity": "critical",
  "mitigation_status": "implemented"
}
```

**Response:** 200
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "name": "Updated GDPR Data Protection",
  "description": "European data protection regulation compliance",
  "constraint_type": "regulatory",
  "scope": "global",
  "severity": "critical",
  "enforcement_level": "mandatory",
  "stakeholder_id": "uuid",
  "business_actor_id": "uuid",
  "risk_profile": "high",
  "compliance_required": true,
  "regulatory_framework": "GDPR",
  "mitigation_strategy": "Implement data encryption and access controls",
  "mitigation_status": "implemented",
  "mitigation_effort": "high",
  "business_impact": "high",
  "technical_impact": "medium",
  "operational_impact": "medium",
  "effective_date": "2024-01-01T00:00:00Z",
  "expiry_date": "2025-01-01T00:00:00Z",
  "review_frequency": "quarterly",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T01:00:00Z"
}
```

### DELETE /constraints/{id}
Deletes a constraint.

**Response:** 204

## Link Management

### POST /constraints/{id}/links
Creates a link between a constraint and another element.

**Request:**
```json
{
  "linked_element_id": "uuid",
  "linked_element_type": "goal",
  "link_type": "constrains",
  "impact_level": "high",
  "compliance_status": "compliant"
}
```

**Response:** 201
```json
{
  "id": "uuid",
  "constraint_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "goal",
  "link_type": "constrains",
  "impact_level": "high",
  "compliance_status": "compliant",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### GET /constraints/{id}/links
Lists all links for a constraint.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "constraint_id": "uuid",
    "linked_element_id": "uuid",
    "linked_element_type": "goal",
    "link_type": "constrains",
    "impact_level": "high",
    "compliance_status": "compliant",
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
  "constraint_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "goal",
  "link_type": "constrains",
  "impact_level": "high",
  "compliance_status": "compliant",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### PUT /links/{link_id}
Updates a link.

**Request:**
```json
{
  "link_type": "limits",
  "compliance_status": "non_compliant"
}
```

**Response:** 200
```json
{
  "id": "uuid",
  "constraint_id": "uuid",
  "linked_element_id": "uuid",
  "linked_element_type": "goal",
  "link_type": "limits",
  "impact_level": "high",
  "compliance_status": "non_compliant",
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### DELETE /links/{link_id}
Deletes a link.

**Response:** 204

## Analysis Endpoints

### GET /constraints/{id}/impact-map
Gets impact map for a constraint.

**Response:** 200
```json
{
  "constraint_id": "uuid",
  "impacted_elements_count": 5,
  "compliant_elements": 3,
  "non_compliant_elements": 1,
  "partially_compliant_elements": 1,
  "exempt_elements": 0,
  "affected_layers": ["Motivation", "Strategy", "Business"],
  "overall_compliance_score": 0.8,
  "last_assessed": "2024-01-01T00:00:00Z"
}
```

### GET /constraints/{id}/analysis
Analyzes a constraint for strategic insights.

**Response:** 200
```json
{
  "constraint_id": "uuid",
  "severity_score": 0.75,
  "risk_score": 0.75,
  "compliance_score": 1.0,
  "business_impact_score": 0.75,
  "technical_impact_score": 0.5,
  "operational_impact_score": 0.5,
  "mitigation_effort_score": 0.75,
  "overall_impact_score": 0.58,
  "last_analyzed": "2024-01-01T00:00:00Z"
}
```

## Domain-Specific Query Endpoints

### GET /constraints/by-type/{type}
Returns constraints filtered by type.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "GDPR Data Protection",
    "constraint_type": "regulatory",
    "severity": "high",
    "enforcement_level": "mandatory"
  }
]
```

### GET /constraints/by-scope/{scope}
Returns constraints filtered by scope.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "GDPR Data Protection",
    "constraint_type": "regulatory",
    "scope": "global",
    "severity": "high"
  }
]
```

### GET /constraints/by-severity/{severity}
Returns constraints filtered by severity.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "GDPR Data Protection",
    "constraint_type": "regulatory",
    "severity": "high",
    "enforcement_level": "mandatory"
  }
]
```

### GET /constraints/by-stakeholder/{stakeholder_id}
Returns constraints associated with a specific stakeholder.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "GDPR Data Protection",
    "constraint_type": "regulatory",
    "stakeholder_id": "uuid"
  }
]
```

### GET /constraints/by-business-actor/{business_actor_id}
Returns constraints associated with a specific business actor.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "GDPR Data Protection",
    "constraint_type": "regulatory",
    "business_actor_id": "uuid"
  }
]
```

### GET /constraints/by-element/{element_type}/{element_id}
Returns constraints that affect a specific element.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "GDPR Data Protection",
    "constraint_type": "regulatory",
    "severity": "high"
  }
]
```

### GET /constraints/compliance/required
Returns constraints that require compliance.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "GDPR Data Protection",
    "constraint_type": "regulatory",
    "compliance_required": true,
    "regulatory_framework": "GDPR"
  }
]
```

### GET /constraints/expiring/{days_ahead}
Returns constraints that are expiring soon.

**Response:** 200
```json
[
  {
    "id": "uuid",
    "name": "GDPR Data Protection",
    "constraint_type": "regulatory",
    "expiry_date": "2024-02-01T00:00:00Z"
  }
]
```

## Utility Endpoints

### GET /constraints/types
Returns available constraint types.

**Response:** 200
```json
["technical", "regulatory", "organizational", "environmental", "financial"]
```

### GET /constraints/scopes
Returns available scopes.

**Response:** 200
```json
["global", "domain", "project", "component"]
```

### GET /constraints/severities
Returns available severities.

**Response:** 200
```json
["low", "medium", "high", "critical"]
```

### GET /constraints/enforcement-levels
Returns available enforcement levels.

**Response:** 200
```json
["mandatory", "recommended", "optional"]
```

### GET /constraints/risk-profiles
Returns available risk profiles.

**Response:** 200
```json
["low", "medium", "high", "critical"]
```

### GET /constraints/mitigation-statuses
Returns available mitigation statuses.

**Response:** 200
```json
["pending", "in_progress", "implemented", "verified"]
```

### GET /constraints/mitigation-efforts
Returns available mitigation efforts.

**Response:** 200
```json
["low", "medium", "high", "critical"]
```

### GET /constraints/impact-levels
Returns available impact levels.

**Response:** 200
```json
["low", "medium", "high", "critical"]
```

### GET /constraints/review-frequencies
Returns available review frequencies.

**Response:** 200
```json
["monthly", "quarterly", "annually", "ad_hoc"]
```

### GET /constraints/link-types
Returns available link types.

**Response:** 200
```json
["constrains", "limits", "restricts", "governs", "regulates"]
```

### GET /constraints/compliance-statuses
Returns available compliance statuses.

**Response:** 200
```json
["compliant", "non_compliant", "partially_compliant", "exempt"]
```

## System Endpoints

### GET /health
Health check endpoint.

**Response:** 200
```json
{
  "service": "constraint_service",
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
# HELP constraint_service_requests_total Total requests
# TYPE constraint_service_requests_total counter
constraint_service_requests_total{method="GET",route="/health",status="200"} 1000
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
  "detail": "Insufficient permissions. Required: constraint:create, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Constraint not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Data Types

### Constraint Types
- `technical`: Technical constraints
- `regulatory`: Regulatory constraints
- `organizational`: Organizational constraints
- `environmental`: Environmental constraints
- `financial`: Financial constraints

### Scopes
- `global`: Global scope
- `domain`: Domain scope
- `project`: Project scope
- `component`: Component scope

### Severities
- `low`: Low severity
- `medium`: Medium severity
- `high`: High severity
- `critical`: Critical severity

### Enforcement Levels
- `mandatory`: Mandatory enforcement
- `recommended`: Recommended enforcement
- `optional`: Optional enforcement

### Risk Profiles
- `low`: Low risk
- `medium`: Medium risk
- `high`: High risk
- `critical`: Critical risk

### Mitigation Statuses
- `pending`: Pending mitigation
- `in_progress`: Mitigation in progress
- `implemented`: Mitigation implemented
- `verified`: Mitigation verified

### Mitigation Efforts
- `low`: Low effort
- `medium`: Medium effort
- `high`: High effort
- `critical`: Critical effort

### Impact Levels
- `low`: Low impact
- `medium`: Medium impact
- `high`: High impact
- `critical`: Critical impact

### Review Frequencies
- `monthly`: Monthly review
- `quarterly`: Quarterly review
- `annually`: Annual review
- `ad_hoc`: Ad hoc review

### Link Types
- `constrains`: Constrains relationship
- `limits`: Limits relationship
- `restricts`: Restricts relationship
- `governs`: Governs relationship
- `regulates`: Regulates relationship

### Compliance Statuses
- `compliant`: Compliant status
- `non_compliant`: Non-compliant status
- `partially_compliant`: Partially compliant status
- `exempt`: Exempt status 