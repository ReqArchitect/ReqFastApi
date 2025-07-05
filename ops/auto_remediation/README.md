# Automated Remediation Scripts

- `pod_restart.sh`: Restart a deployment on alert
- `db_readonly_remediation.sh`: Fix DB stuck in read-only
- `pipeline_rollback.sh`: Roll back deployment to previous image

Link these scripts to Prometheus alertmanager or CI/CD failure hooks.
