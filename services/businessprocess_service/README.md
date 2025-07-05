# businessprocess_service

A microservice for managing BusinessProcess elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for BusinessProcess
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /business-processes
- GET /business-processes
- GET /business-processes/{id}
- PUT /business-processes/{id}
- DELETE /business-processes/{id}
- GET /business-processes/{id}/traceability-check
- GET /business-processes/{id}/impact-summary

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
