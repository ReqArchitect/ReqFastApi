# applicationfunction_service

A microservice for managing ApplicationFunction elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for ApplicationFunction
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /application-functions
- GET /application-functions
- GET /application-functions/{id}
- PUT /application-functions/{id}
- DELETE /application-functions/{id}
- GET /application-functions/{id}/traceability-check
- GET /application-functions/{id}/impact-summary

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
