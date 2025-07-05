# courseofaction_service

A microservice for managing CourseOfAction elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for CourseOfAction
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /courses-of-action
- GET /courses-of-action
- GET /courses-of-action/{id}
- PUT /courses-of-action/{id}
- DELETE /courses-of-action/{id}
- GET /courses-of-action/{id}/traceability-check
- GET /courses-of-action/{id}/impact-summary

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
