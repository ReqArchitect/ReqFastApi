# System Software Service

## Overview

The System Software Service is a microservice designed to manage ArchiMate 3.2 System Software elements in the Technology Layer. It provides comprehensive CRUD operations, relationship management, analysis capabilities, and domain-specific queries for software platforms that support application components.

## ArchiMate 3.2 Integration

### Technology Layer: System Software

The System Software element represents software platforms that support application components, including:

- **Operating Systems**: Ubuntu 22.04 LTS, Windows Server 2022, RHEL 9
- **Databases**: PostgreSQL 15.2, MySQL 8.0, Oracle 19c
- **Middleware**: RabbitMQ 3.10, Apache Kafka 3.4, Redis 7.0
- **Runtime Environments**: Java Runtime (JDK 17), Node.js 18, Python 3.11
- **Container Engines**: Docker Engine 24.0, Kubernetes 1.28, OpenShift 4.12

### Linked Elements

System Software can be linked to:
- **Nodes**: Physical or virtual infrastructure that hosts the software
- **Application Components**: Software components that run on the system software
- **Devices**: Hardware devices that interact with the software
- **Artifacts**: Configuration files, scripts, or documentation

## Features

### Core Functionality
- ✅ Full CRUD operations for SystemSoftware and SoftwareLink
- ✅ Multi-tenancy with tenant isolation
- ✅ Role-based access control (RBAC)
- ✅ JWT authentication and authorization
- ✅ Redis event emission for real-time updates
- ✅ Comprehensive validation and error handling

### Analysis & Monitoring
- ✅ Dependency mapping and impact analysis
- ✅ Compliance checking and vulnerability assessment
- ✅ Performance metrics and health monitoring
- ✅ Security scanning and patch management
- ✅ Operational health scoring

### Domain-Specific Queries
- ✅ Filter by software type, vendor, version
- ✅ Query by vulnerability score and lifecycle state
- ✅ Search by compliance status and certification
- ✅ Analyze by performance metrics and resource usage

### Observability
- ✅ Health check endpoints (`/health`, `/ready`, `/live`)
- ✅ Prometheus metrics (`/metrics`)
- ✅ OpenTelemetry tracing and logging
- ✅ Structured logging with correlation IDs
- ✅ Performance monitoring and alerting

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Docker (optional)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd services/systemsoftware_service
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Initialize database**
```bash
# Create database tables
python -c "from app.database import init_db; init_db()"
```

5. **Run the service**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Docker Deployment

```bash
# Build the image
docker build -t systemsoftware-service .

# Run the container
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e REDIS_HOST=redis-host \
  systemsoftware-service
```

## API Usage

### Authentication

All API endpoints require JWT authentication:

```bash
curl -H "Authorization: Bearer <jwt_token>" \
  http://localhost:8080/api/v1/system-software/
```

### Create System Software

```bash
curl -X POST "http://localhost:8080/api/v1/system-software/" \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ubuntu 22.04 LTS",
    "description": "Linux operating system for servers",
    "software_type": "os",
    "version": "22.04.3",
    "vendor": "Canonical",
    "license_type": "open_source",
    "lifecycle_state": "active",
    "vulnerability_score": 2.5,
    "update_channel": "lts",
    "deployment_environment": "production"
  }'
```

### List System Software

```bash
curl "http://localhost:8080/api/v1/system-software/?software_type=os&limit=10" \
  -H "Authorization: Bearer <jwt_token>"
```

### Get Analysis

```bash
curl "http://localhost:8080/api/v1/system-software/{id}/analysis" \
  -H "Authorization: Bearer <jwt_token>"
```

### Get Compliance Check

```bash
curl "http://localhost:8080/api/v1/system-software/{id}/compliance-check" \
  -H "Authorization: Bearer <jwt_token>"
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost:5432/systemsoftware_db` |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `JWT_SECRET_KEY` | JWT signing key | `your-secret-key-change-in-production` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `ENVIRONMENT` | Deployment environment | `production` |

### Feature Flags

| Flag | Description | Default |
|------|-------------|---------|
| `OTEL_ENABLED` | Enable OpenTelemetry tracing | `true` |
| `METRICS_ENABLED` | Enable Prometheus metrics | `true` |
| `RATE_LIMIT_ENABLED` | Enable rate limiting | `true` |
| `VALIDATION_ENABLED` | Enable input validation | `true` |

## Development

### Project Structure

```
systemsoftware_service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── deps.py              # Dependency injection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── services.py          # Business logic
│   └── routes.py            # API endpoints
├── tests/
│   └── test_systemsoftware.py
├── requirements.txt
├── Dockerfile
├── README.md
└── API_REFERENCE.md
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_systemsoftware.py::TestSystemSoftwareService::test_create_system_software
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

- **Health Check**: `GET /health`
- **Readiness Check**: `GET /ready`
- **Liveness Check**: `GET /live`

### Metrics

- **Prometheus Metrics**: `GET /metrics`
- **Custom Metrics**: Request count, latency, error rates
- **Business Metrics**: System software count, vulnerability scores

### Logging

Structured logging with correlation IDs:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "systemsoftware-service",
  "correlation_id": "uuid",
  "message": "Created system software",
  "system_software_id": "uuid",
  "tenant_id": "uuid"
}
```

### Tracing

OpenTelemetry tracing for:
- HTTP requests
- Database queries
- Redis operations
- External API calls

## Security

### Authentication & Authorization

- **JWT Authentication**: Secure token-based authentication
- **RBAC**: Role-based access control (Owner, Admin, Editor, Viewer)
- **Tenant Isolation**: Multi-tenant data isolation
- **Permission Checks**: Granular permission validation

### Data Protection

- **Input Validation**: Comprehensive input sanitization
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Content Security Policy headers
- **Rate Limiting**: Protection against abuse

### Compliance

- **Audit Logging**: Complete audit trail
- **Data Retention**: Configurable retention policies
- **Encryption**: Data encryption at rest and in transit
- **Vulnerability Scanning**: Automated security scanning

## Performance

### Optimization Features

- **Connection Pooling**: Database connection optimization
- **Caching**: Redis-based caching layer
- **Query Optimization**: Efficient database queries
- **Async Operations**: Non-blocking I/O operations

### Scalability

- **Horizontal Scaling**: Stateless service design
- **Load Balancing**: Kubernetes-ready deployment
- **Auto-scaling**: Cloud-native scaling capabilities
- **Resource Management**: Memory and CPU optimization

## Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database connectivity
python -c "from app.database import check_db_connection; print(check_db_connection())"
```

#### Redis Connection Issues
```bash
# Test Redis connection
redis-cli ping
```

#### Authentication Issues
```bash
# Verify JWT token
python -c "import jwt; jwt.decode(token, secret, algorithms=['HS256'])"
```

### Debug Mode

Enable debug mode for detailed logging:

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload
```

### Performance Monitoring

Monitor key metrics:

```bash
# Check response times
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8080/api/v1/system-software/"

# Monitor memory usage
ps aux | grep systemsoftware-service

# Check database performance
SELECT * FROM pg_stat_activity WHERE datname = 'systemsoftware_db';
```

## Integration

### Event Bus Integration

The service emits Redis events for real-time integration:

```python
# Subscribe to events
import redis
r = redis.Redis()
pubsub = r.pubsub()
pubsub.subscribe('system_software_events:tenant_id')

for message in pubsub.listen():
    print(message)
```

### External API Integration

Configure external service integration:

```bash
# Set external API configuration
export EXTERNAL_API_ENABLED=true
export EXTERNAL_API_TIMEOUT=30
export EXTERNAL_API_RETRY_ATTEMPTS=3
```

## Contributing

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests**
5. **Run the test suite**
6. **Submit a pull request**

### Code Standards

- Follow PEP 8 style guidelines
- Write comprehensive tests
- Add type hints
- Update documentation
- Follow semantic versioning

## Support

### Documentation

- **API Reference**: `/docs` (Swagger UI)
- **ReDoc**: `/redoc`
- **OpenAPI Spec**: `/openapi.json`

### Getting Help

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: README and API Reference
- **Logs**: Application logs and monitoring

### Version History

- **v1.0.0**: Initial release with full CRUD operations
- **v1.1.0**: Added analysis and compliance features
- **v1.2.0**: Enhanced monitoring and observability

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- ArchiMate 3.2 specification
- FastAPI framework
- SQLAlchemy ORM
- Redis for event bus
- OpenTelemetry for observability
