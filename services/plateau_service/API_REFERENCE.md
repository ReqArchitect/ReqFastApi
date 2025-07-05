# API Reference: plateau_service

## POST /plateaus
Creates a new Plateau.

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

## GET /plateaus
Lists all Plateaus for the tenant.

## GET /plateaus/{id}
Retrieves a Plateau by ID.

## PUT /plateaus/{id}
Updates a Plateau.

## DELETE /plateaus/{id}
Deletes a Plateau.

## GET /plateaus/{id}/traceability-check
Returns traceability status for the Plateau.

## GET /plateaus/{id}/impact-summary
Returns impact summary for the Plateau.

[OpenAPI JSON](./app/openapi.json)
