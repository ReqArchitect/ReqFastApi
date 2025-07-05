# communicationpath_service

A microservice for managing CommunicationPath elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for CommunicationPath
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /communication-paths
- GET /communication-paths
- GET /communication-paths/{id}
- PUT /communication-paths/{id}
- DELETE /communication-paths/{id}
- GET /communication-paths/{id}/traceability-check
- GET /communication-paths/{id}/impact-summary

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
