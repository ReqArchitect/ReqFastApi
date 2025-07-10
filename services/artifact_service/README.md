# Artifact Service

## Overview

The Artifact Service is a microservice within the ReqArchitect platform that manages ArchiMate 3.2 **Artifact** elements in the Technology Layer. Artifacts represent deployable assets such as source files, containers, binaries, scripts, builds, and configurations that implement application components or system software.

## ArchiMate 3.2 Integration

### Technology Layer: Artifact Element

The Artifact element in ArchiMate 3.2 represents:
- **Deployable assets** that implement application components or system software
- **Physical or digital artifacts** that can be deployed on nodes
- **Implementation artifacts** that realize application components
- **Configuration artifacts** that configure system software or application components

### Key Relationships

- **Artifact** → **Application Component** (implements)
- **Artifact** → **System Software** (implements)
- **Artifact** → **Node** (deployed on)
- **Artifact** → **Device** (deployed on)

### Examples

- "Dockerfile v1.2" - Container build artifact
- "PostgreSQL Config Map" - Configuration artifact
- "Frontend React Build Artifact" - Application build artifact
- "Infra Provisioning Script" - Infrastructure artifact
- "Container Image hash:sha256-XYZ" - Container artifact

## Features

### Core Functionality

- **Full CRUD Operations**: Create, read, update, delete artifacts and artifact links
- **Multi-tenancy**: Complete tenant isolation with `tenant_id` enforcement
- **RBAC Security**: Role-based access control (Owner, Admin, Editor, Viewer)
- **JWT Authentication**: Secure token-based authentication
- **Redis Event Emission**: Real-time event streaming for system integration

### Advanced Features

- **Dependency Mapping**: Analyze artifact dependencies and relationships
- **Integrity Checking**: Verify artifact integrity, security, and compliance
- **Performance Analysis**: Monitor artifact performance metrics
- **Compliance Tracking**: Track regulatory and policy compliance
- **Security Scanning**: Vulnerability assessment and security scoring
- **Quality Metrics**: Code quality, test coverage, and documentation status

### Domain-Specific Queries

- Filter by artifact type (source, build, image, config, script, binary, container)
- Filter by format (docker, yaml, json, jar, exe, etc.)
- Filter by deployment target node
- Filter by associated component
- Filter by modification date
- Filter by integrity and security status

### Analysis Endpoints

- `/artifacts/{id}/dependency-map` - Analyze artifact dependencies
- `/artifacts/{id}/integrity-check` - Verify artifact integrity and security

## Architecture

### Technology Stack

- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache/Events**: Redis
- **Authentication**: JWT with python-jose
- **Monitoring**: Prometheus metrics, OpenTelemetry tracing
- **Documentation**: OpenAPI/Swagger

### Service Components

```
artifact_service/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application setup
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas and validation
│   ├── services.py          # Business logic and services
│   ├── routes.py            # API endpoints and routing
│   └── deps.py              # Dependency injection
├── tests/
│   └── test_artifact.py     # Comprehensive test suite
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── README.md                # This file
├── API_REFERENCE.md         # Detailed API documentation
└── ARCHITECTURE.md          # Architecture documentation
```

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Redis 6+
- Docker (optional)

### Local Development

1. **Clone and setup**:
```bash
cd services/artifact_service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment configuration**:
```bash
# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://user:password@localhost:5432/reqarchitect
REDIS_HOST=localhost
REDIS_PORT=6379
JWT_SECRET_KEY=your-secret-key-change-in-production
ENVIRONMENT=development
EOF
```

3. **Database setup**:
```bash
# Create database tables
python -c "from app.database import init_db; init_db()"
```

4. **Run the service**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Docker Deployment

```bash
# Build image
docker build -t artifact-service .

# Run container
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:password@host:5432/reqarchitect \
  -e REDIS_HOST=host \
  -e JWT_SECRET_KEY=your-secret-key \
  artifact-service
```

## API Usage

### Authentication

All API endpoints require JWT authentication:

```bash
curl -H "Authorization: Bearer <jwt_token>" \
  http://localhost:8080/api/v1/artifacts/
```

### Create Artifact

```bash
curl -X POST http://localhost:8080/api/v1/artifacts/ \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "User Authentication Service",
    "description": "Spring Boot application for user authentication",
    "artifact_type": "container",
    "version": "1.2.0",
    "format": "docker",
    "storage_location": "registry.example.com/auth-service:1.2.0",
    "checksum": "sha256:abc123def456",
    "build_tool": "docker",
    "size_mb": 150.5,
    "deployment_environment": "production",
    "integrity_verified": true,
    "security_scan_passed": true,
    "vulnerability_count": 0,
    "security_score": 9.2,
    "compliance_status": "compliant",
    "data_classification": "internal"
  }'
```

### List Artifacts

```bash
curl -H "Authorization: Bearer <jwt_token>" \
  "http://localhost:8080/api/v1/artifacts/?artifact_type=container&limit=10"
```

### Get Artifact

```bash
curl -H "Authorization: Bearer <jwt_token>" \
  http://localhost:8080/api/v1/artifacts/{artifact_id}
```

### Update Artifact

```bash
curl -X PUT http://localhost:8080/api/v1/artifacts/{artifact_id} \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "1.2.1",
    "security_score": 9.5
  }'
```

### Delete Artifact

```bash
curl -X DELETE http://localhost:8080/api/v1/artifacts/{artifact_id} \
  -H "Authorization: Bearer <jwt_token>"
```

### Analysis Endpoints

```bash
# Get dependency map
curl -H "Authorization: Bearer <jwt_token>" \
  http://localhost:8080/api/v1/artifacts/{artifact_id}/dependency-map

# Check integrity
curl -H "Authorization: Bearer <jwt_token>" \
  http://localhost:8080/api/v1/artifacts/{artifact_id}/integrity-check
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost:5432/reqarchitect` |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `JWT_SECRET_KEY` | JWT signing key | `your-secret-key-change-in-production` |
| `ENVIRONMENT` | Environment (development/production) | `production` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `OTEL_ENABLED` | OpenTelemetry tracing | `true` |
| `PROMETHEUS_ENABLED` | Prometheus metrics | `true` |

### Artifact-Specific Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `MAX_ARTIFACT_SIZE_MB` | Maximum artifact size in MB | `1000000` (1TB) |
| `MAX_FILE_COUNT` | Maximum files per artifact | `100000` |
| `ALLOWED_ARTIFACT_TYPES` | Valid artifact types | `[source, build, image, config, script, binary, container, package, library, framework]` |
| `ALLOWED_FORMATS` | Valid file formats | `[docker, yaml, json, xml, jar, war, ear, exe, dll, so, dylib, tar, zip, gz, bz2, rpm, deb, msi, pkg, apk, ipa]` |

## Development

### Code Structure

- **Models** (`models.py`): SQLAlchemy ORM models for Artifact and ArtifactLink
- **Schemas** (`schemas.py`): Pydantic models for request/response validation
- **Services** (`services.py`): Business logic and CRUD operations
- **Routes** (`routes.py`): FastAPI endpoints and API routing
- **Dependencies** (`deps.py`): Authentication, database, and Redis dependencies

### Testing

Run the comprehensive test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/ -v --cov=app --cov-report=html

# Run specific test
pytest tests/test_artifact.py::TestArtifactAPI::test_create_artifact_api -v
```

### Code Quality

```bash
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

## Monitoring & Observability

### Health Checks

```bash
# Service health
curl http://localhost:8080/health

# Response example
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "environment": "production",
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "opentelemetry": "healthy"
  }
}
```

### Metrics

```bash
# Prometheus metrics
curl http://localhost:8080/metrics

# Key metrics
artifact_service_requests_total{method="GET",endpoint="/api/v1/artifacts/",status="200"}
artifact_service_request_duration_seconds{method="POST",endpoint="/api/v1/artifacts/"}
```

### Logging

Structured logging with correlation IDs:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Created artifact 550e8400-e29b-41d4-a716-446655440001 for tenant 550e8400-e29b-41d4-a716-446655440002",
  "artifact_id": "550e8400-e29b-41d4-a716-446655440001",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440002"
}
```

### OpenTelemetry Tracing

Distributed tracing with spans for:
- HTTP requests
- Database operations
- Redis operations
- Business logic operations

## Security

### Authentication & Authorization

- **JWT Tokens**: Secure token-based authentication
- **RBAC**: Role-based access control with granular permissions
- **Tenant Isolation**: Complete multi-tenant data isolation
- **Rate Limiting**: Per-user and per-tenant rate limiting

### Data Protection

- **Input Validation**: Comprehensive Pydantic validation
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- **XSS Protection**: Content-Type headers and input sanitization
- **CORS Configuration**: Configurable cross-origin resource sharing

### Security Features

- **Integrity Verification**: Checksum validation for artifacts
- **Security Scanning**: Vulnerability assessment integration
- **Compliance Tracking**: Regulatory compliance monitoring
- **Audit Logging**: Comprehensive audit trail

## Event Integration

### Redis Event Streams

The service emits events for all artifact operations:

```json
{
  "event_type": "artifact.created",
  "artifact_id": "550e8400-e29b-41d4-a716-446655440001",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
  "user_id": "550e8400-e29b-41d4-a716-446655440003",
  "artifact_type": "container",
  "name": "User Authentication Service",
  "version": "1.2.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Event Types

- `artifact.created` - New artifact created
- `artifact.updated` - Artifact updated
- `artifact.deleted` - Artifact deleted
- `artifact_link.created` - New artifact link created
- `artifact_link.updated` - Artifact link updated
- `artifact_link.deleted` - Artifact link deleted

## Performance

### Optimization Features

- **Database Connection Pooling**: Configurable connection pool
- **Redis Caching**: Optional caching for frequently accessed data
- **Query Optimization**: Indexed queries and efficient filtering
- **Pagination**: Efficient pagination for large datasets
- **Compression**: Gzip compression for API responses

### Performance Metrics

- **Response Time**: Average response time tracking
- **Throughput**: Requests per second monitoring
- **Error Rate**: Error percentage tracking
- **Resource Usage**: CPU and memory monitoring

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```
   Error: Database connection failed
   Solution: Check DATABASE_URL and PostgreSQL service
   ```

2. **Redis Connection Failed**
   ```
   Error: Redis connection failed
   Solution: Check REDIS_HOST, REDIS_PORT, and Redis service
   ```

3. **JWT Token Invalid**
   ```
   Error: Invalid authentication token
   Solution: Verify JWT_SECRET_KEY and token format
   ```

4. **Permission Denied**
   ```
   Error: Insufficient permissions
   Solution: Check user role and required permissions
   ```

### Debug Mode

Enable debug mode for detailed logging:

```bash
export ENVIRONMENT=development
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload --log-level debug
```

### Log Analysis

```bash
# View service logs
docker logs artifact-service

# Filter error logs
docker logs artifact-service 2>&1 | grep ERROR

# Monitor real-time logs
docker logs -f artifact-service
```

## Contributing

### Development Workflow

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/artifact-enhancement`
3. **Make changes**: Follow coding standards and add tests
4. **Run tests**: `pytest tests/ -v`
5. **Submit pull request**: Include description and test coverage

### Code Standards

- **Python**: PEP 8 style guide
- **Type Hints**: Use type annotations
- **Documentation**: Docstrings for all functions
- **Testing**: Minimum 90% test coverage
- **Security**: Follow security best practices

## Support

### Documentation

- **API Reference**: See `API_REFERENCE.md` for detailed API documentation
- **Architecture**: See `ARCHITECTURE.md` for architecture details
- **OpenAPI**: Interactive docs at `/docs` when service is running

### Contact

- **Issues**: Report bugs via GitHub issues
- **Discussions**: Use GitHub discussions for questions
- **Security**: Report security issues privately

### Version History

- **v1.0.0**: Initial release with full CRUD operations
- **v1.1.0**: Added analysis endpoints and enhanced validation
- **v1.2.0**: Improved performance and monitoring features

---

**Artifact Service** - Managing ArchiMate 3.2 Artifact elements in the Technology Layer
