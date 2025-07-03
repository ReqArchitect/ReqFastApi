
![Coverage](./coverage.svg)
# Architecture Suite Microservice

This service manages `ArchitecturePackage` entities for multi-tenant SaaS platforms, supporting full traceability to Product Discovery Layer items.

## Features
- FastAPI, PostgreSQL, Alembic migrations
- JWT Auth, RBAC (superuser, admin, manager, user)
- Redis event emission on create/update/delete
- Traceability via FKs: business_case_id, initiative_id, kpi_id, business_model_id
- /health and /docs endpoints
- Structured logging (tenant_id, user_id, correlation_id)
- 12-factor config, Dockerized

## Endpoints
* `/metrics` — Prometheus metrics endpoint (see below)
- `POST /architecture-packages/` — Create
- `GET /architecture-packages/` — List (pagination, filtering)
- `GET /architecture-packages/{id}` — Retrieve
- `PUT /architecture-packages/{id}` — Update
- `DELETE /architecture-packages/{id}` — Delete
- `GET /health` — Health check

## Dev
- Run with Docker or `uvicorn app.main:app --reload`
- Test: `pytest --cov=app --cov-fail-under=90`
- Lint: `flake8 app/`

## CI/CD
- See `.github/workflows/ci.yml` for pipeline

## Observability
- All logs are structured JSON with tenant, user, correlation, and latency fields
- `/metrics` exposes Prometheus metrics: requests, latency, errors
- Correlation IDs are propagated via `X-Correlation-ID` header
