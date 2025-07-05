# API Reference: systemsoftware_service

## POST /system-software
Creates a new SystemSoftware.

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

## GET /system-software
Lists all SystemSoftware for the tenant.

## GET /system-software/{id}
Retrieves a SystemSoftware by ID.

## PUT /system-software/{id}
Updates a SystemSoftware.

## DELETE /system-software/{id}
Deletes a SystemSoftware.

## GET /system-software/{id}/traceability-check
Returns traceability status for the SystemSoftware.

## GET /system-software/{id}/impact-summary
Returns impact summary for the SystemSoftware.

[OpenAPI JSON](./app/openapi.json)
