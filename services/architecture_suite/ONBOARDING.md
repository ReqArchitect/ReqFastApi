# Onboarding Playbook: architecture_suite

## 1. Clone & Setup
```sh
git clone <repo-url>
cd services/architecture_suite
cp .env.example .env
```

## 2. Local Development
- Start PostgreSQL and Redis (Docker Compose or local)
- Run Alembic migrations:
  ```sh
  alembic upgrade head
  ```
- Start the service:
  ```sh
  uvicorn app.main:app --reload
  ```
- Access docs at: http://localhost:8000/docs

## 3. Testing
- Run all tests:
  ```sh
  pytest --cov=app --cov-fail-under=90
  ```
- Lint and security scan:
  ```sh
  flake8 app/
  bandit -r app/
  ```
- Load test:
  ```sh
  locust -f locustfile.py --headless -u 100 -r 10 -t 1m --host=http://localhost:8000
  ```

## 4. Staging/Production
- Set up `.env.staging` or `.env.prod` and secrets (Vault/SealedSecrets)
- Deploy via Helm:
  ```sh
  helm upgrade --install architecture-suite ./helm -f .env.staging
  ```
- Or via GitHub Actions (see `.github/workflows/deploy.yml`)

## 5. CI/CD & Deployment
- On push to `main`, deploys to staging
- On tag push (v*.*.*), deploys to production
- Canary rollout and rollback managed by Flagger/Helm

## 6. Smoke Tests
- Health: `curl http://<host>/health`
- CRUD: `curl -X POST http://<host>/architecture-packages/`
- Metrics: `curl http://<host>/metrics`

## 7. Troubleshooting
- Check logs for JSON entries with correlation_id
- Review Prometheus and Grafana dashboards in `monitoring/`
