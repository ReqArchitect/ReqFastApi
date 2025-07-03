# admin_service

A microservice for managing platform administrators with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for Admin
- Redis event emission (stub)
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /admins
- GET /admins
- GET /admins/{id}
- PUT /admins/{id}
- DELETE /admins/{id}
