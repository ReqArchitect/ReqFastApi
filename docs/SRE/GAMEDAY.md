# Game-Day Exercise Plan

## Monthly Drill
- Simulate service outage, DB failover, high error rate
- Execute runbooks and remediation scripts
- Validate alerting and escalation
- Complete postmortem

## Failure Scenarios
- Pod kill, network partition, DB failover, CI/CD break

## Playbook Steps
1. Announce drill
2. Trigger failure (see chaos scripts)
3. Observe alerting and on-call response
4. Restore service and document

## Postmortem Template
- Incident summary
- Timeline
- Root cause
- Remediation
- Lessons learned
