# Node Service

## Overview

The Node Service is a microservice component of the ReqArchitect platform that manages ArchiMate 3.2 Node elements in the Technology Layer. It provides comprehensive management of computational resources that host application components, including physical servers, virtual machines, containers, and cloud infrastructure units.

## ArchiMate 3.2 Integration

### Technology Layer: Node Element

The Node Service represents the **Node** element in the ArchiMate 3.2 Technology Layer:

- **Element Type**: Node
- **Layer**: Technology Layer
- **Description**: A computational resource that hosts and/or executes software components
- **Examples**: 
  - "Azure Kubernetes Node"
  - "On-prem VM Host"
  - "Edge Gateway Container"
  - "Staging Server (EU-West)"

### Relationships

Nodes can be linked to:
- **Application Components** (hosts, deploys)
- **System Software** (hosts, manages)
- **Devices** (communicates_with, depends_on)
- **Artifacts** (stores, manages)

## Features

### Core Functionality
- ✅ **Full CRUD Operations**: Create, read, update, delete nodes and node links
- ✅ **Multi-tenancy**: Complete tenant isolation and data segregation
- ✅ **RBAC Enforcement**: Role-based access control (Owner/Admin/Editor/Viewer)
- ✅ **JWT Authentication**: Secure token-based authentication
- ✅ **Redis Event Emission**: Real-time event publishing for system integration

### Node Management
- **Node Types**: VM, Container, Physical, Cloud, Edge
- **Environments**: Production, Staging, Development, Testing
- **Lifecycle States**: Active, Inactive, Maintenance, Decommissioned, Planned
- **Performance Monitoring**: CPU, Memory, Storage, Network utilization
- **Security Levels**: Basic, Standard, High, Critical

### Analysis & Insights
- **Deployment Mapping**: Visualize deployed components and their relationships
- **Capacity Analysis**: Resource utilization and scaling recommendations
- **Operational Health**: Availability, performance, and risk assessment
- **Compliance Status**: Security and regulatory compliance tracking

### Advanced Features
- **Resource Optimization**: Identify underutilized resources and scaling opportunities
- **Cost Management**: Track operational costs and resource allocation
- **Maintenance Planning**: Schedule and track maintenance windows
- **Incident Management**: Track incidents and SLA breaches

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
cd services/node_service
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
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Docker Deployment

```bash
# Build the image
docker build -t node-service .

# Run the container
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e REDIS_HOST=redis-host \
  node-service
```

## API Usage

### Authentication

All API endpoints require JWT authentication:

```bash
curl -H "Authorization: Bearer <your-jwt-token>" \
  http://localhost:8080/nodes/
```

### Create a Node

```bash
curl -X POST "http://localhost:8080/nodes/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production Web Server",
    "description": "Primary web server for production environment",
    "node_type": "vm",
    "environment": "production",
    "operating_system": "Ubuntu 20.04",
    "hardware_spec": "{\"cpu\": \"8 cores\", \"memory\": \"16GB\"}",
    "region": "us-east-1",
    "availability_target": 99.9,
    "cpu_cores": 8,
    "memory_gb": 16.0,
    "storage_gb": 500.0,
    "security_level": "high"
  }'
```

### List Nodes with Filtering

```bash
curl "http://localhost:8080/nodes/?node_type=vm&environment=production&limit=10" \
  -H "Authorization: Bearer <token>"
```

### Get Deployment Map

```bash
curl "http://localhost:8080/nodes/{node_id}/deployment-map" \
  -H "Authorization: Bearer <token>"
```

### Get Capacity Analysis

```bash
curl "http://localhost:8080/nodes/{node_id}/capacity-analysis" \
  -H "Authorization: Bearer <token>"
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/node_service` |
| `REDIS_HOST` | Redis host address | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `JWT_SECRET_KEY` | JWT signing secret | `your-secret-key-here` |
| `ENVIRONMENT` | Application environment | `production` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Node-Specific Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `NODE_DEFAULT_AVAILABILITY_TARGET` | Default availability target | `99.9` |
| `NODE_DEFAULT_SECURITY_LEVEL` | Default security level | `standard` |
| `NODE_DEFAULT_LIFECYCLE_STATE` | Default lifecycle state | `active` |

## Development

### Project Structure

```
node_service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── deps.py              # Dependencies and auth
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── services.py          # Business logic
│   └── routes.py            # API endpoints
├── tests/
│   └── test_node.py         # Comprehensive tests
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── README.md               # This file
└── API_REFERENCE.md        # Detailed API documentation
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_node.py

# Run with verbose output
pytest -v
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

# Metrics
curl http://localhost:8080/metrics
```

### Prometheus Metrics

The service exposes the following metrics:
- `node_service_requests_total`: Total request count
- `node_service_request_duration_seconds`: Request latency
- Custom business metrics for node operations

### OpenTelemetry Tracing

Distributed tracing is enabled with:
- FastAPI instrumentation
- SQLAlchemy instrumentation
- Redis instrumentation
- Custom span attributes for business operations

### Logging

Structured logging with configurable levels:
- `DEBUG`: Development debugging
- `INFO`: General information
- `WARNING`: Warning messages
- `ERROR`: Error conditions

## Security

### Authentication & Authorization

- **JWT Tokens**: Secure token-based authentication
- **RBAC**: Role-based access control with granular permissions
- **Tenant Isolation**: Complete data segregation between tenants
- **Rate Limiting**: Protection against abuse

### Data Protection

- **Encryption**: Database and transport encryption
- **Input Validation**: Comprehensive input sanitization
- **SQL Injection Protection**: Parameterized queries
- **XSS Protection**: Output encoding

### Compliance

- **GDPR**: Data protection and privacy controls
- **SOX**: Financial reporting compliance
- **ISO 27001**: Information security management
- **SOC 2**: Security, availability, and confidentiality

## Performance

### Optimization Features

- **Database Connection Pooling**: Efficient database connections
- **Redis Caching**: Fast data access and session storage
- **Async Operations**: Non-blocking I/O operations
- **Pagination**: Efficient large dataset handling

### Scalability

- **Horizontal Scaling**: Stateless design for easy scaling
- **Load Balancing**: Ready for load balancer deployment
- **Microservice Architecture**: Independent service scaling
- **Resource Optimization**: Automatic resource utilization analysis

## Event Integration

### Redis Event Channels

The service emits events on the following channels:
- `node_events`: Node lifecycle events
- `node_link_events`: Node link relationship events

### Event Types

- `node.created`: Node creation events
- `node.updated`: Node modification events
- `node.deleted`: Node deletion events
- `node_link.created`: Link creation events
- `node_link.updated`: Link modification events
- `node_link.deleted`: Link deletion events

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check `DATABASE_URL` configuration
   - Verify PostgreSQL is running
   - Check network connectivity

2. **Redis Connection Failed**
   - Check `REDIS_HOST` and `REDIS_PORT`
   - Verify Redis is running
   - Check authentication if required

3. **Authentication Errors**
   - Verify JWT token is valid
   - Check token expiration
   - Ensure proper permissions

4. **Performance Issues**
   - Monitor database connection pool
   - Check Redis memory usage
   - Review application logs

### Debug Mode

Enable debug mode for detailed logging:

```bash
export ENVIRONMENT=development
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload
```

## Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests for new functionality**
5. **Run the test suite**
6. **Submit a pull request**

### Code Standards

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed

## Support

### Getting Help

- **Documentation**: Check this README and API_REFERENCE.md
- **Issues**: Report bugs via GitHub issues
- **Discussions**: Use GitHub discussions for questions
- **Email**: Contact the development team

### Version History

- **v1.0.0**: Initial release with full CRUD operations
- **v1.1.0**: Added analysis and capacity features
- **v1.2.0**: Enhanced security and monitoring

### Roadmap

- [ ] Advanced capacity planning algorithms
- [ ] Integration with cloud provider APIs
- [ ] Real-time performance monitoring
- [ ] Automated scaling recommendations
- [ ] Enhanced compliance reporting

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Node Service** - Empowering ArchiMate 3.2 Node management in the Technology Layer
