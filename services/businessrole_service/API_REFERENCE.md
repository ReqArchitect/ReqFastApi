# API Reference: businessrole_service

## POST /business-roles
Creates a new BusinessRole.

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

## GET /business-roles
Lists all BusinessRoles for the tenant.

## GET /business-roles/{id}
Retrieves a BusinessRole by ID.

## PUT /business-roles/{id}
Updates a BusinessRole.

## DELETE /business-roles/{id}
Deletes a BusinessRole.

## GET /business-roles/{id}/traceability-check
Returns traceability status for the BusinessRole.

## GET /business-roles/{id}/impact-summary
Returns impact summary for the BusinessRole.

[OpenAPI JSON](./app/openapi.json)
