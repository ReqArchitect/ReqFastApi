# gap_service

A microservice for managing Gap elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for Gap
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /gaps
- GET /gaps
- GET /gaps/{id}
- PUT /gaps/{id}
- DELETE /gaps/{id}
- GET /gaps/{id}/traceability-check
- GET /gaps/{id}/impact-summary

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
