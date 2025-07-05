# device_service

A microservice for managing Device elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for Device
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /devices
- GET /devices
- GET /devices/{id}
- PUT /devices/{id}
- DELETE /devices/{id}
- GET /devices/{id}/traceability-check
- GET /devices/{id}/impact-summary

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
