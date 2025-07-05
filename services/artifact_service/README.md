# artifact_service

A microservice for managing Artifact elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for Artifact
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /artifacts
- GET /artifacts
- GET /artifacts/{id}
- PUT /artifacts/{id}
- DELETE /artifacts/{id}
- GET /artifacts/{id}/traceability-check
- GET /artifacts/{id}/impact-summary

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
