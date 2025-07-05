# onboarding_state_service

Tracks onboarding progress for each user under a tenant.

## Features
- Persistent onboarding checklist per user/tenant
- API to get/update onboarding state
- Emits audit events on step changes
- Prevents cross-tenant access

## Endpoints
- `GET /onboarding/state/{user_id}`: Get onboarding state for a user
- `POST /onboarding/state/{user_id}`: Update onboarding steps for a user
- `GET /onboarding/state/tenant/{tenant_id}`: List all onboarding states for a tenant

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
