# Resource Service

## Overview

The Resource Service is a microservice in the ReqArchitect platform that manages ArchiMate 3.2 Resource elements in the Strategy Layer. It provides comprehensive resource management capabilities for organizational resources including human, financial, system, and informational resources that enable strategic capabilities and business functions.

## Architecture

### ArchiMate 3.2 Alignment

This service represents the **Resource** element in the **Strategy Layer** of ArchiMate 3.2:

- **Layer**: Strategy Layer
- **Element Type**: Resource
- **Purpose**: Model organizational resources that enable strategic capabilities and business functions
- **Relationships**: Links to Goals, Constraints, Business Functions, Application Components, Nodes

### Key Features

- **Multi-tenant Architecture**: Full tenant isolation with `tenant_id` support
- **RBAC Security**: Role-based access control (Owner/Admin/Editor/Viewer)
- **JWT Authentication**: Secure API access with JWT tokens
- **Event-Driven**: Redis-based event emission for integration
- **Observability**: Health checks, metrics, and OpenTelemetry tracing
- **Comprehensive Analysis**: Impact scoring, allocation mapping, and resource analysis

## Resource Types

The service supports four main resource types:

1. **Human Resources**: People, skills, expertise (e.g., "Enterprise Architect")
2. **System Resources**: Technology systems and platforms (e.g., "Legacy CRM System")
3. **Financial Resources**: Budget allocations and funding (e.g., "Budget Unit")
4. **Knowledge Resources**: Information repositories and data assets (e.g., "Customer Insights Repository")

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Redis (for event emission)
- Docker (optional)

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/resource_service

# Security
SECRET_KEY=your-secret-key-here

# Redis (for events)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# OpenTelemetry (optional)
OTEL_ENABLED=false
OTEL_ENDPOINT=http://localhost:4317
```

### Running the Service

#### Using Docker

```bash
# Build the image
docker build -t resource-service .

# Run the container
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:password@host:5432/resource_service \
  -e SECRET_KEY=your-secret-key \
  resource-service
```

#### Using Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### API Access

The service provides a RESTful API with the following base URL:
```
http://localhost:8080/api/v1
```

All endpoints require JWT authentication with the following header:
```
Authorization: Bearer <jwt_token>
```

Required JWT claims:
- `tenant_id`: UUID of the tenant
- `user_id`: UUID of the user
- `role`: User role (Owner, Admin, Editor, Viewer)

## API Documentation

### Core Endpoints

- `POST /resources` - Create a new resource
- `GET /resources` - List resources with filtering
- `GET /resources/{id}` - Get resource by ID
- `PUT /resources/{id}` - Update resource
- `DELETE /resources/{id}` - Delete resource

### Resource Link Endpoints

- `POST /resources/{id}/links` - Create resource link
- `GET /resources/{id}/links` - List resource links
- `GET /resources/links/{link_id}` - Get link by ID
- `PUT /resources/links/{link_id}` - Update link
- `DELETE /resources/links/{link_id}` - Delete link

### Analysis Endpoints

- `GET /resources/{id}/impact-score` - Get impact score
- `GET /resources/{id}/allocation-map` - Get allocation map
- `GET /resources/{id}/analysis` - Comprehensive resource analysis

### Domain-Specific Queries

- `GET /resources/by-type/{type}` - Resources by type
- `GET /resources/by-status/{status}` - Resources by status
- `GET /resources/by-capability/{capability_id}` - Resources by capability
- `GET /resources/by-performance/{threshold}` - Resources by performance
- `GET /resources/by-element/{element_type}/{element_id}` - Resources by linked element
- `GET /resources/active` - Active resources
- `GET /resources/critical` - Critical resources

### Enumeration Endpoints

- `GET /resources/resource-types` - Available resource types
- `GET /resources/deployment-statuses` - Available deployment statuses
- `GET /resources/criticalities` - Available criticality levels
- `GET /resources/strategic-importances` - Available strategic importance levels
- `GET /resources/business-values` - Available business value levels
- `GET /resources/operational-hours` - Available operational hour types
- `GET /resources/expertise-levels` - Available expertise levels
- `GET /resources/governance-models` - Available governance models
- `GET /resources/link-types` - Available link types
- `GET /resources/relationship-strengths` - Available relationship strengths
- `GET /resources/dependency-levels` - Available dependency levels
- `GET /resources/interaction-frequencies` - Available interaction frequencies
- `GET /resources/interaction-types` - Available interaction types
- `GET /resources/data-flow-directions` - Available data flow directions
- `GET /resources/performance-impacts` - Available performance impact levels
- `GET /resources/allocation-priorities` - Available allocation priorities

## Observability

### Health Check

```bash
curl http://localhost:8080/health
```

### Metrics

```bash
curl http://localhost:8080/metrics
```

### API Documentation

- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_resource.py
```

### Code Quality

```bash
# Linting
flake8 app/

# Security scanning
bandit -r app/
```

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t resource-service:latest .

# Run with environment variables
docker run -d \
  --name resource-service \
  -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:password@host:5432/resource_service \
  -e SECRET_KEY=your-secret-key \
  -e REDIS_HOST=redis-host \
  -e REDIS_PORT=6379 \
  resource-service:latest
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resource-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: resource-service
  template:
    metadata:
      labels:
        app: resource-service
    spec:
      containers:
      - name: resource-service
        image: resource-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: resource-service-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: resource-service-secrets
              key: secret-key
```

## Security

### Authentication

All API endpoints require JWT authentication with the following claims:
- `tenant_id`: UUID of the tenant
- `user_id`: UUID of the user
- `role`: User role

### Authorization

Role-based access control (RBAC) is enforced:

- **Owner**: Full access to all operations
- **Admin**: Full access to all operations
- **Editor**: Create, read, update operations
- **Viewer**: Read-only access

### Data Validation

- Input validation using Pydantic models
- Enum validation for resource types, statuses, and other fields
- Quantity validation (must be > 0)
- Availability validation (0-100%)
- Allocation percentage validation (0-100%)

## Event-Driven Architecture

The service emits events to Redis for integration with other services:

### Event Types

- `resource.created` - Resource creation events
- `resource.updated` - Resource update events
- `resource.deleted` - Resource deletion events
- `resource_link.created` - Resource link creation events
- `resource_link.updated` - Resource link update events
- `resource_link.deleted` - Resource link deletion events

### Event Format

```json
{
  "event_type": "resource.created",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "resource_id": "550e8400-e29b-41d4-a716-446655440000",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440002"
  }
}
```

## Monitoring and Alerting

### Key Metrics

- Request count and latency
- Resource creation/update/deletion rates
- Error rates and response times
- Database connection health
- Redis connection health

### Health Checks

- Database connectivity
- Redis connectivity
- Service responsiveness
- Memory and CPU usage

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify DATABASE_URL is correct
   - Check database server is running
   - Ensure database exists and is accessible

2. **Authentication Errors**
   - Verify JWT token is valid
   - Check token contains required claims
   - Ensure token hasn't expired

3. **Redis Connection Errors**
   - Verify Redis server is running
   - Check REDIS_HOST and REDIS_PORT settings
   - Ensure Redis is accessible from the service

4. **Permission Errors**
   - Verify user role has required permissions
   - Check tenant_id matches resource tenant
   - Ensure user has access to the resource

### Logs

Service logs include:
- Request/response logging
- Error logging with stack traces
- Performance metrics
- Security events

## Contributing

1. Follow the established code patterns
2. Add tests for new functionality
3. Update documentation for API changes
4. Ensure all tests pass before submitting

## License

This service is part of the ReqArchitect platform and follows the same licensing terms.
