# businessrole_service

A microservice for managing BusinessRole elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for BusinessRole
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /business-roles
- GET /business-roles
- GET /business-roles/{id}
- PUT /business-roles/{id}
- DELETE /business-roles/{id}
- GET /business-roles/{id}/traceability-check
- GET /business-roles/{id}/impact-summary

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
