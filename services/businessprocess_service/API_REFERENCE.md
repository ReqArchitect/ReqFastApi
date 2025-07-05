# API Reference: businessprocess_service

## POST /business-processes
Creates a new BusinessProcess.

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

## GET /business-processes
Lists all BusinessProcesses for the tenant.

## GET /business-processes/{id}
Retrieves a BusinessProcess by ID.

## PUT /business-processes/{id}
Updates a BusinessProcess.

## DELETE /business-processes/{id}
Deletes a BusinessProcess.

## GET /business-processes/{id}/traceability-check
Returns traceability status for the BusinessProcess.

## GET /business-processes/{id}/impact-summary
Returns impact summary for the BusinessProcess.

[OpenAPI JSON](./app/openapi.json)
