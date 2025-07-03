# capability_service

A microservice for managing ArchiMate Capability elements with full traceability, RBAC, event emission, observability, and multi-tenancy.

## Features
- CRUD for Capability
- Traceability and impact summary endpoints
- Redis event emission
- RBAC and multi-tenancy
- Prometheus metrics, OpenTelemetry tracing, JSON logs
- CI/CD, Docker, test coverage >90%

## Endpoints
- POST /capabilities
- GET /capabilities
- GET /capabilities/{id}
- PUT /capabilities/{id}
- DELETE /capabilities/{id}
- GET /capabilities/{id}/traceability-check
- GET /capabilities/{id}/impact-summary

## Setup
- `docker build -t capability_service .`
- `docker run -p 8080:8080 capability_service`

## Observability
- /metrics, /health endpoints
- Prometheus/Grafana integration

## Traceability
- All Capability records link to business_case, initiative, kpi, business_model
