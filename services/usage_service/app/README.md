# usage_service

Backend service for admin dashboard usage and health metrics.

## Features
- Usage metrics per tenant (active users, model count, API requests, data footprint)
- System health (uptime %, error rate %, p95 latency)
- Recent audit events
- Role-based access (Owner/Admin only)
- Emits audit log on fetch

## Endpoints
- `GET /usage/tenant/{tenant_id}`: Usage metrics for a tenant
- `GET /usage/system_health`: System SLA/health
- `GET /usage/activity/{tenant_id}`: Recent audit events for a tenant

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
