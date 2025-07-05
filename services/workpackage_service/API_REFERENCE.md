# API Reference: workpackage_service

## POST /work-packages
Creates a new WorkPackage.

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

## GET /work-packages
Lists all WorkPackages for the tenant.

## GET /work-packages/{id}
Retrieves a WorkPackage by ID.

## PUT /work-packages/{id}
Updates a WorkPackage.

## DELETE /work-packages/{id}
Deletes a WorkPackage.

## GET /work-packages/{id}/traceability-check
Returns traceability status for the WorkPackage.

## GET /work-packages/{id}/impact-summary
Returns impact summary for the WorkPackage.

[OpenAPI JSON](./app/openapi.json)
