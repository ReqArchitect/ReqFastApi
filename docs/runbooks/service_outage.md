# Runbook: Service Outage

## Context
- One or more services are unreachable or failing health checks.

## Impact
- User-facing downtime, degraded functionality.

## Troubleshooting Steps
1. Check service health in Grafana/Prometheus.
2. Inspect pod logs and events (`kubectl logs`, `kubectl describe pod`).
3. Validate network policies and ingress.
4. Check for recent deployments or config changes.

## Rollback
- Roll back to previous deployment via Helm/Argo.
- Restart affected pods.
