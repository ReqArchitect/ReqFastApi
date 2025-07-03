# Architecture: capability_service

## Data Model
- Capability: UUID PK, tenant_id, business_case_id, initiative_id, kpi_id, business_model_id, name, description, timestamps

## Event Flow
- On create/update/delete, emits Redis event (capability.*)

## Traceability
- All FKs link to Product Discovery Layer
- /traceability-check endpoint verifies FK integrity

## Observability
- JSON logs, Prometheus metrics, OpenTelemetry tracing
