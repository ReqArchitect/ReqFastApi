# resource_service

A microservice for managing Resource elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for Resource
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /resources
- GET /resources
- GET /resources/{id}
- PUT /resources/{id}
- DELETE /resources/{id}
- GET /resources/{id}/traceability-check
- GET /resources/{id}/impact-summary

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
