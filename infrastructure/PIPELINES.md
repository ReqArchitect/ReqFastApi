# CI/CD Promotion Pipeline

- Build, test, and security scan on every PR
- Deploy to dev on merge to develop
- Deploy to staging on merge to main (with manual approval)
- Deploy to prod on tag/release (with smoke tests and approval)
- Automated smoke tests and synthetic transactions post-deploy
- Promotion gates and rollback on failure
