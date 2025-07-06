# CI/CD and Development Setup

This document describes the CI/CD pipeline, pre-commit hooks, and development workflow for the FastAPI microservices project.

## 🚀 Quick Start

### For New Developers

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ReqFastApi
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup-dev.sh
   ./setup-dev.sh
   ```

3. **Start developing**
   ```bash
   # Make your changes
   git add .
   git commit -m "Your commit message"  # Pre-commit hooks run automatically
   ```

## 🔧 Pre-commit Hooks

Pre-commit hooks automatically run on every commit to ensure code quality.

### What They Do

- **Code Formatting**: Black and Ruff format your Python code
- **Linting**: Flake8 and Ruff check for code quality issues
- **Docker Validation**: Hadolint checks Dockerfile syntax
- **Security**: Detect-secrets scans for hardcoded secrets
- **YAML/JSON Validation**: Ensures configuration files are valid

### Manual Usage

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
pre-commit run flake8 --all-files
pre-commit run hadolint --all-files

# Skip hooks (not recommended)
git commit --no-verify -m "Skip hooks"
```

### Hook Configuration

The hooks are configured in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      # ... more hooks

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        args: [--line-length=127]

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.11
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
```

## 🔄 GitHub Actions Workflow

The CI/CD pipeline runs on every push to `main` and pull request.

### Workflow Jobs

#### 1. Build and Test (`build-and-test`)

**What it does:**
- Sets up Python 3.11 and Docker
- Builds all microservices using Docker Compose
- Starts infrastructure services (PostgreSQL, Redis)
- Starts application services
- Runs structural tests (`test_microservices.py`)
- Tests health endpoints for all services
- Validates service functionality

**Key steps:**
```yaml
- name: Build all microservices
  run: docker-compose build gateway_service notification_service ...

- name: Start services
  run: |
    docker-compose up -d db event_bus
    # Wait for infrastructure services
    timeout 60 bash -c 'until docker exec postgres_db pg_isready -U postgres; do sleep 2; done'

- name: Test health endpoints
  run: |
    # Test each service's health endpoint
    curl -f http://localhost:8080/health  # gateway
    curl -f http://localhost:8001/health  # auth
    # ... more services
```

#### 2. Lint and Validate (`lint-and-validate`)

**What it does:**
- Runs pre-commit hooks on all files
- Lints Python files with Flake8 and Ruff
- Validates Dockerfile syntax with Hadolint
- Checks docker-compose.yml syntax

### Workflow Triggers

- **Push to `main`**: Full build and test
- **Pull Request**: Full build and test
- **Manual trigger**: Available in GitHub Actions UI

### Workflow Status

The workflow will fail if:
- ❌ Any service fails to build
- ❌ Health checks fail (exit code ≠ 0)
- ❌ Linting fails
- ❌ Dockerfile syntax is invalid
- ❌ Tests fail

## 🧪 Testing

### Automated Tests

1. **Structural Tests** (`test_microservices.py`)
   - Validates service structure
   - Checks imports and dependencies
   - Verifies Dockerfile configuration
   - Tests Docker builds

2. **Health Endpoint Tests**
   - Tests `/health` endpoints for all services
   - Validates response format
   - Checks service accessibility

3. **Integration Tests**
   - Tests service communication
   - Validates database connectivity
   - Checks Redis connectivity

### Manual Testing

```bash
# Run structural tests
python test_microservices.py

# Test health endpoints
./healthcheck.sh

# Start services and test manually
docker-compose up
curl http://localhost:8080/health
```

## 🔍 Code Quality Tools

### Python Linting

- **Black**: Code formatting (line length: 127)
- **Ruff**: Fast Python linter and formatter
- **Flake8**: Style guide enforcement

### Configuration Files

- `.flake8`: Flake8 configuration
- `pyproject.toml`: Modern Python tooling configuration
- `.pre-commit-config.yaml`: Pre-commit hooks configuration

### Docker Validation

- **Hadolint**: Dockerfile linting
- **Docker Compose**: Configuration validation

## 🚨 Common Issues and Solutions

### Pre-commit Hook Failures

**Issue**: Black formatting fails
```bash
# Solution: Run Black manually
black services/ --line-length=127
```

**Issue**: Flake8 finds issues
```bash
# Solution: Fix the issues or check .flake8 config
flake8 services/ --count --exit-zero --max-complexity=10 --max-line-length=127
```

**Issue**: Dockerfile syntax error
```bash
# Solution: Check with Hadolint
docker run --rm -i hadolint/hadolint < services/service_name/Dockerfile
```

### CI/CD Failures

**Issue**: Service health check fails
- Check if service is starting correctly
- Verify port configuration
- Check service logs: `docker-compose logs service_name`

**Issue**: Build fails
- Check Dockerfile syntax
- Verify requirements.txt dependencies
- Check for missing files

**Issue**: Database connection fails
- Verify PostgreSQL service is running
- Check database credentials
- Ensure proper `depends_on` configuration

## 📋 Development Workflow

### Daily Development

1. **Start work**
   ```bash
   git pull origin main
   docker-compose up -d  # Start services
   ```

2. **Make changes**
   ```bash
   # Edit files
   # Pre-commit hooks run automatically on commit
   ```

3. **Test changes**
   ```bash
   python test_microservices.py
   ./healthcheck.sh
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Your changes"  # Hooks run automatically
   git push origin feature-branch
   ```

### Before Creating PR

1. **Run all checks locally**
   ```bash
   pre-commit run --all-files
   python test_microservices.py
   docker-compose build
   docker-compose up -d
   ./healthcheck.sh
   ```

2. **Create PR**
   - GitHub Actions will run automatically
   - Address any CI failures
   - Request review when all checks pass

## 🔧 Configuration

### Environment Variables

Copy `env.example` to `.env` and customize:
```bash
cp env.example .env
# Edit .env with your settings
```

### Local Development

For local development without Docker:
```bash
# Install service dependencies
cd services/service_name
pip install -r requirements.txt

# Run service directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 Monitoring

### Health Checks

All services expose `/health` endpoints:
- `http://localhost:8080/health` - Gateway
- `http://localhost:8001/health` - Auth
- `http://localhost:8002/health` - AI Modeling
- `http://localhost:8010/health` - Billing
- `http://localhost:8011/health` - Invoice

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs service_name

# Follow logs in real-time
docker-compose logs -f service_name
```

## 🆘 Getting Help

1. **Check the logs**: `docker-compose logs`
2. **Run health checks**: `./healthcheck.sh`
3. **Validate configuration**: `docker-compose config`
4. **Check CI/CD status**: GitHub Actions tab
5. **Review documentation**: This file and service READMEs

## 📝 Contributing

1. Follow the development workflow above
2. Ensure all pre-commit hooks pass
3. Write tests for new features
4. Update documentation as needed
5. Create descriptive commit messages
6. Request code review for all changes 