# Billing Service API Reference

## Endpoints

### Get Tenant Billing Profile
- **GET** `/billing/tenant/{tenant_id}`
- Returns the billing profile for a tenant.

### List Subscription Plans
- **GET** `/billing/plans`
- Returns all available subscription plans.

### Submit Usage Report
- **POST** `/billing/usage_report`
- Receives usage metrics from usage_service.

### Trigger Alerts
- **POST** `/billing/trigger_alerts`
- Evaluates usage and emits alerts if thresholds are crossed.

### Upgrade Plan
- **POST** `/billing/upgrade_plan`
- Changes the tenant's plan and updates limits.

## Models
- SubscriptionPlan
- TenantBillingProfile
- BillingEvent

See `schemas.py` for model details.
