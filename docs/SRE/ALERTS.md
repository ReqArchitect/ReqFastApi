# SRE Alerts & Escalation

## SLOs
- Error rate <1%
- p95 latency <200ms

## Alert Rules
- See monitoring/prometheus_alerts/sre_rules.yaml

## Escalation
- PagerDuty/Slack notification on critical alerts
- Escalate to on-call primary, then secondary
- Document all incidents in postmortems
