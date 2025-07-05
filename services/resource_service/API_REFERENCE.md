# API Reference: resource_service

## POST /resources
Creates a new Resource.

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

## GET /resources
Lists all Resources for the tenant.

## GET /resources/{id}
Retrieves a Resource by ID.

## PUT /resources/{id}
Updates a Resource.

## DELETE /resources/{id}
Deletes a Resource.

## GET /resources/{id}/traceability-check
Returns traceability status for the Resource.

## GET /resources/{id}/impact-summary
Returns impact summary for the Resource.

[OpenAPI JSON](./app/openapi.json)
