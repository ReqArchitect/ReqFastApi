# orchestrator_service

Central API gateway and federation layer for the architecture_suite platform.

## Endpoints
- GET /model/tree
- GET /model/{element}/{id}/full-details
- /metrics, /health

## Features
- Fan-out federation to element services
- Correlation ID propagation
- Observability: JSON logs, Prometheus, OpenTelemetry
- Docker, CI/CD, test coverage
