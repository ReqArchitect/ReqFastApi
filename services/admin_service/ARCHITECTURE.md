# Architecture: admin_service

## Data Model
- Admin: UUID PK, tenant_id, business_case_id, initiative_id, kpi_id, business_model_id, name, email, description, timestamps

## Event Flow
- On create/update/delete, emits Redis event (admin.*)

## Traceability
- All FKs link to Product Discovery Layer

## Observability
- JSON logs, Prometheus metrics, OpenTelemetry tracing
