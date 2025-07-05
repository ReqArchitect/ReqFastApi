# analytics_service

Tracks tenant usage patterns and triggers billing alerts for admin dashboard and analytics.

## Features
- Stores daily usage snapshots per tenant
- Triggers billing alerts on quota/plan/trial thresholds
- Emits events to notification and audit log services
- Owner/Admin-only access

## Endpoints
- `GET /analytics/tenant/{tenant_id}/monthly`: Usage trends for a tenant
- `GET /analytics/alerts/{tenant_id}`: Active billing alerts for a tenant
- `POST /analytics/alerts/resolve/{alert_id}`: Mark alert as resolved

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
