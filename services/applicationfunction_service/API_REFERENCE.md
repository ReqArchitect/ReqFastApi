# API Reference: applicationfunction_service

## POST /application-functions
Creates a new ApplicationFunction.

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

## GET /application-functions
Lists all ApplicationFunctions for the tenant.

## GET /application-functions/{id}
Retrieves an ApplicationFunction by ID.

## PUT /application-functions/{id}
Updates an ApplicationFunction.

## DELETE /application-functions/{id}
Deletes an ApplicationFunction.

## GET /application-functions/{id}/traceability-check
Returns traceability status for the ApplicationFunction.

## GET /application-functions/{id}/impact-summary
Returns impact summary for the ApplicationFunction.

[OpenAPI JSON](./app/openapi.json)
