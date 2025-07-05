# API Reference: device_service

## POST /devices
Creates a new Device.

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

## GET /devices
Lists all Devices for the tenant.

## GET /devices/{id}
Retrieves a Device by ID.

## PUT /devices/{id}
Updates a Device.

## DELETE /devices/{id}
Deletes a Device.

## GET /devices/{id}/traceability-check
Returns traceability status for the Device.

## GET /devices/{id}/impact-summary
Returns impact summary for the Device.

[OpenAPI JSON](./app/openapi.json)
