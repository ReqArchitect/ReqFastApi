# API Reference: gap_service

## POST /gaps
Creates a new Gap.

**Request:**
```json
{
  "tenant_id": "uuid",
  "name": "string",
  "description": "string"
}
```
**Response:** 201
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "name": "string",
  "description": "string",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

## GET /gaps
Lists all Gaps for the tenant.

## GET /gaps/{id}
Retrieves a Gap by ID.

## PUT /gaps/{id}
Updates a Gap.

## DELETE /gaps/{id}
Deletes a Gap.

## GET /gaps/{id}/traceability-check
Returns traceability status for the Gap.

## GET /gaps/{id}/impact-summary
Returns impact summary for the Gap.

[OpenAPI JSON](./app/openapi.json)
