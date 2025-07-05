# Runbook: CI/CD Failure

## Context
- CI/CD pipeline fails to build, test, or deploy.

## Impact
- Blocked releases, delayed fixes.

## Troubleshooting Steps
1. Review failed job logs in GitHub Actions.
2. Check for dependency or secret issues.
3. Validate runner resources and permissions.
4. Re-run failed jobs after fixing root cause.

## Rollback
- Revert to previous pipeline config or image.
