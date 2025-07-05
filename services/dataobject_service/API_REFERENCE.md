# API Reference: dataobject_service

## POST /data-objects
Creates a new DataObject.

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

## GET /data-objects
Lists all DataObjects for the tenant.

## GET /data-objects/{id}
Retrieves a DataObject by ID.

## PUT /data-objects/{id}
Updates a DataObject.

## DELETE /data-objects/{id}
Deletes a DataObject.

## GET /data-objects/{id}/traceability-check
Returns traceability status for the DataObject.

## GET /data-objects/{id}/impact-summary
Returns impact summary for the DataObject.

[OpenAPI JSON](./app/openapi.json)
