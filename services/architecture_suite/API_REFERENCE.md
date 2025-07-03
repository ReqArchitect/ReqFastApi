# API Reference: architecture_suite

## Authentication
All endpoints require JWT Bearer token. RBAC enforced: `manager` for write, `user` for read.

## Endpoints

### POST /architecture-packages/
Create a new ArchitecturePackage.
**Request:**
```json
{
  "tenant_id": "uuid",
  "user_id": "uuid",
  "business_case_id": "uuid",
  "initiative_id": "uuid",
  "kpi_id": "uuid",
  "business_model_id": "uuid",
  "name": "string",
  "description": "string"
}
```
**Response:** 201
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "business_case_id": "uuid",
  "initiative_id": "uuid",
  "kpi_id": "uuid",
  "business_model_id": "uuid",
  "name": "string",
  "description": "string",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### GET /architecture-packages/
List packages (pagination, filtering).
**Query:** `?skip=0&limit=10&tenant_id=...`
**Response:** 200
```json
[
  { ...ArchitecturePackageOut... }
]
```

### GET /architecture-packages/{id}
Retrieve a package by ID.
**Response:** 200
```json
{ ...ArchitecturePackageOut... }
```

### PUT /architecture-packages/{id}
Update a package (manager only).
**Request:**
```json
{
  "name": "string",
  "description": "string"
}
```
**Response:** 200
```json
{ ...ArchitecturePackageOut... }
```

### DELETE /architecture-packages/{id}
Delete a package (manager only).
**Response:** 204

### POST /architecture-packages/{id}/link-element
Link an ArchiMate element to a package.
**Request:**
```json
{
  "element_type": "ApplicationComponent",
  "element_id": "uuid",
  "traceability_fk": "business_case_id"
}
```
**Response:** 200
```json
{ "linked": true, "link_id": "uuid" }
```

### GET /architecture-packages/{id}/impact-summary
Aggregate KPI impact for a package.
**Response:** 200
```json
{
  "package_id": "uuid",
  "kpi_count": 3,
  "aligned": 3,
  "coverage": 1.0,
  "goal_alignment_score": 1.0
}
```

### GET /architecture-packages/traceability-check/{id}
Check traceability for a package.
**Response:** 200
```json
{
  "package_id": "uuid",
  "missing_links": ["kpi_id"]
}
```

### GET /metrics
Prometheus metrics endpoint.
**Response:**
```
# HELP architecture_suite_requests_total ...
# TYPE architecture_suite_requests_total counter
...
```

### GET /health
Health and metrics snapshot.
**Response:**
```json
{
  "service": "architecture_suite",
  "version": "1.0.0",
  "uptime": "123.45s",
  "total_requests": 100,
  "error_rate": 0.01
}
```
