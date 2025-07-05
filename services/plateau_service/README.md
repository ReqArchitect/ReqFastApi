# plateau_service

A microservice for managing Plateau elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for Plateau
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /plateaus
- GET /plateaus
- GET /plateaus/{id}
- PUT /plateaus/{id}
- DELETE /plateaus/{id}
- GET /plateaus/{id}/traceability-check
- GET /plateaus/{id}/impact-summary

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
