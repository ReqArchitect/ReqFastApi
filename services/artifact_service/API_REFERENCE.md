# API Reference: artifact_service

## POST /artifacts
Creates a new Artifact.

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

## GET /artifacts
Lists all Artifacts for the tenant.

## GET /artifacts/{id}
Retrieves an Artifact by ID.

## PUT /artifacts/{id}
Updates an Artifact.

## DELETE /artifacts/{id}
Deletes an Artifact.

## GET /artifacts/{id}/traceability-check
Returns traceability status for the Artifact.

## GET /artifacts/{id}/impact-summary
Returns impact summary for the Artifact.

[OpenAPI JSON](./app/openapi.json)
