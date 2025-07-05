# API Reference: node_service

## POST /nodes
Creates a new Node.

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

## GET /nodes
Lists all Nodes for the tenant.

## GET /nodes/{id}
Retrieves a Node by ID.

## PUT /nodes/{id}
Updates a Node.

## DELETE /nodes/{id}
Deletes a Node.

## GET /nodes/{id}/traceability-check
Returns traceability status for the Node.

## GET /nodes/{id}/impact-summary
Returns impact summary for the Node.

[OpenAPI JSON](./app/openapi.json)
