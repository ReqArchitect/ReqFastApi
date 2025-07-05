# API Reference: courseofaction_service

## POST /courses-of-action
Creates a new CourseOfAction.

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

## GET /courses-of-action
Lists all CoursesOfAction for the tenant.

## GET /courses-of-action/{id}
Retrieves a CourseOfAction by ID.

## PUT /courses-of-action/{id}
Updates a CourseOfAction.

## DELETE /courses-of-action/{id}
Deletes a CourseOfAction.

## GET /courses-of-action/{id}/traceability-check
Returns traceability status for the CourseOfAction.

## GET /courses-of-action/{id}/impact-summary
Returns impact summary for the CourseOfAction.

[OpenAPI JSON](./app/openapi.json)
