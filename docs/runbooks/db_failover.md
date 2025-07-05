# Runbook: DB Failover

## Context
- Primary database is unavailable or degraded.

## Impact
- Data unavailability, possible data loss if not replicated.

## Troubleshooting Steps
1. Check DB cluster status and replica health.
2. Validate backup/restore status.
3. Inspect application DB connection errors.

## Rollback
- Promote replica to primary.
- Restore from latest backup if needed.
