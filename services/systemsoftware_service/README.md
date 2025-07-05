# systemsoftware_service

A microservice for managing SystemSoftware elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for SystemSoftware
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /system-software
- GET /system-software
- GET /system-software/{id}
- PUT /system-software/{id}
- DELETE /system-software/{id}
- GET /system-software/{id}/traceability-check
- GET /system-software/{id}/impact-summary

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
