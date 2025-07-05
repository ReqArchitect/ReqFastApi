# Billing Service

Manages subscription plans, tenant billing profiles, usage-based billing, and alerts for ReqArchitect.

## Features
- Multi-plan support (Free, Pro, Enterprise)
- Usage tracking and limit enforcement
- Billing events and alerting
- Secure tenant scoping and admin controls
- Prorated upgrades and trial management
- Integration stubs for Stripe/payment gateway

## Endpoints
- `GET /billing/tenant/{tenant_id}`: Get tenant billing profile
- `GET /billing/plans`: List available plans
- `POST /billing/usage_report`: Submit usage metrics
- `POST /billing/trigger_alerts`: Evaluate usage and trigger alerts
- `POST /billing/upgrade_plan`: Upgrade tenant plan

## Security
- Only Owner/Admin can view or change billing profile
- Tenant context validated on all endpoints
- Payment data should be encrypted in production

## Observability
- Billing events, plan changes, and alert triggers are logged
- Metrics: active tenants per plan, upgrade rate, churn
