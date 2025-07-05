# dataobject_service

A microservice for managing DataObject elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for DataObject
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /data-objects
- GET /data-objects
- GET /data-objects/{id}
- PUT /data-objects/{id}
- DELETE /data-objects/{id}
- GET /data-objects/{id}/traceability-check
- GET /data-objects/{id}/impact-summary

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
