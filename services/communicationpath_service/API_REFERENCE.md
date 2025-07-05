# API Reference: communicationpath_service

## POST /communication-paths
Creates a new CommunicationPath.

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

## GET /communication-paths
Lists all CommunicationPaths for the tenant.

## GET /communication-paths/{id}
Retrieves a CommunicationPath by ID.

## PUT /communication-paths/{id}
Updates a CommunicationPath.

## DELETE /communication-paths/{id}
Deletes a CommunicationPath.

## GET /communication-paths/{id}/traceability-check
Returns traceability status for the CommunicationPath.

## GET /communication-paths/{id}/impact-summary
Returns impact summary for the CommunicationPath.

[OpenAPI JSON](./app/openapi.json)
