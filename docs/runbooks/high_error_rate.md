# Runbook: High Error Rate

## Context
- Error rate exceeds SLO (1%) for any service.

## Impact
- User experience degradation, possible outages.

## Troubleshooting Steps
1. Identify affected endpoints in Grafana.
2. Check recent code changes and deployments.
3. Inspect logs for stack traces and error patterns.
4. Validate DB/Redis/3rd-party dependencies.

## Rollback
- Roll back to last known good deployment.
- Restart pods if transient.
