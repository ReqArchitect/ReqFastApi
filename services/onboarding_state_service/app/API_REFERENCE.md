# API Reference: onboarding_state_service

## GET /onboarding/state/{user_id}
Returns onboarding status for a user (scoped to tenant).

**Response:**
```json
{
  "tenant_id": "string",
  "user_id": "string",
  "configure_capabilities": false,
  "create_initiative": false,
  "invite_teammates": false,
  "explore_traceability": false,
  "completed": false
}
```

## POST /onboarding/state/{user_id}
Update one or more onboarding steps for a user.

**Request:**
```json
{
  "configure_capabilities": true,
  "invite_teammates": true
}
```
**Response:** (same as GET)

## GET /onboarding/state/tenant/{tenant_id}
List all onboarding states for a tenant.

**Response:**
```json
[
  {
    "tenant_id": "string",
    "user_id": "string",
    "configure_capabilities": false,
    "create_initiative": false,
    "invite_teammates": false,
    "explore_traceability": false,
    "completed": false
  }
]
```

[OpenAPI JSON](./openapi.json)
