# orchestrator_service

Interprets Jira tasks and triggers model-driven code generation workflows with traceability.

## Features
- Maps Jira tasks to ArchiMate 3.2 elements
- Triggers backend, frontend, OpenAPI, and docs generation flows
- Annotates outputs with traceability tags
- Emits audit events
- Owner/Admin-only access

## Endpoints
- `POST /orchestrator/ingest_task`: Accept Jira task payload
- `POST /orchestrator/trigger_generation`: Start scaffold flow
- `GET /orchestrator/status/{task_id}`: Generation status
- `GET /orchestrator/logs/{task_id}`: Audit trail

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
