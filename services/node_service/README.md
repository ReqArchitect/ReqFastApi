# node_service

A microservice for managing Node elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for Node
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /nodes
- GET /nodes
- GET /nodes/{id}
- PUT /nodes/{id}
- DELETE /nodes/{id}
- GET /nodes/{id}/traceability-check
- GET /nodes/{id}/impact-summary

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
