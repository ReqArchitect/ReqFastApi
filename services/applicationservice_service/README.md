# Application Service Microservice

## Overview

The Application Service microservice is part of the ReqArchitect platform and provides comprehensive management of ArchiMate 3.2 Application Service elements. This service handles the creation, management, and analysis of application services within the Application Layer of enterprise architecture.

## ArchiMate 3.2 Integration

### Application Service Element

The Application Service represents a coherent set of application behaviors that supports business processes through an explicitly defined interface. It encapsulates the functionality that applications provide to their users.

**Key Characteristics:**
- **Layer**: Application Layer
- **Element Type**: Application Service
- **Purpose**: Exposes application functionality to business processes and other application services
- **Relationships**: Can realize Application Functions, support Business Processes, enable Capabilities

### Core Properties

- **Service Type**: API, UI, Data, Integration, Messaging
- **Delivery Channel**: HTTP, HTTPS, gRPC, WebSocket, Message Queue, File Transfer
- **Authentication Method**: None, Basic, OAuth, JWT, API Key
- **Performance Targets**: Latency, Availability, Throughput
- **Business Context**: Criticality, Value, Security Level
- **Technical Specifications**: Technology Stack, Deployment Model, Scaling Strategy

## Features

### Core Functionality
- ✅ Full CRUD operations for Application Services
- ✅ Service link management and relationship tracking
- ✅ Multi-tenancy support with tenant isolation
- ✅ JWT-based authentication with RBAC
- ✅ Redis event emission for real-time updates
- ✅ OpenTelemetry tracing and observability
- ✅ Comprehensive data validation and guardrails

### Analysis & Insights
- ✅ Performance scoring and analysis
- ✅ Impact mapping and dependency analysis
- ✅ Business alignment assessment
- ✅ Technical debt analysis
- ✅ Compliance status tracking
- ✅ Risk factor identification
- ✅ Improvement opportunity recommendations

### Domain-Specific Queries
- ✅ Filter by service type, status, criticality
- ✅ Query by performance thresholds
- ✅ Find services by capability or business process
- ✅ Active and critical service identification
- ✅ Enumeration endpoints for UI dropdowns

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Docker (optional)

### Installation

1. **Clone the repository**
```bash
cd services/applicationservice_service
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

4. **Run database migrations**
```bash
alembic upgrade head
```

5. **Start the service**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Docker Deployment

```bash
# Build the image
docker build -t applicationservice-service .

# Run the container
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e REDIS_HOST=redis-host \
  applicationservice-service
```

## API Documentation

### Base URL
```
http://localhost:8080
```

### Authentication
All endpoints require JWT authentication:
```
Authorization: Bearer <jwt_token>
```

Required JWT claims:
- `tenant_id`: UUID of the tenant
- `user_id`: UUID of the user
- `role`: User role (Owner, Admin, Editor, Viewer)

### Core Endpoints

#### Create Application Service
```http
POST /application-services/
Content-Type: application/json

{
  "name": "User Authentication Service",
  "description": "Provides user authentication and authorization",
  "service_type": "api",
  "status": "active",
  "latency_target_ms": 200,
  "availability_target_pct": 99.9,
  "version": "1.0.0",
  "delivery_channel": "https",
  "authentication_method": "jwt",
  "business_value": "high",
  "business_criticality": "high",
  "technology_stack": "{\"framework\": \"FastAPI\", \"database\": \"PostgreSQL\"}",
  "deployment_model": "microservice",
  "scaling_strategy": "horizontal",
  "security_level": "high",
  "data_classification": "internal",
  "service_endpoint": "https://auth.example.com/api/v1",
  "documentation_link": "https://docs.example.com/auth",
  "support_contact": "support@example.com"
}
```

#### List Application Services
```http
GET /application-services/?skip=0&limit=100&service_type=api&status=active
```

#### Get Application Service
```http
GET /application-services/{service_id}
```

#### Update Application Service
```http
PUT /application-services/{service_id}
Content-Type: application/json

{
  "name": "Enhanced User Authentication Service",
  "availability_target_pct": 99.99,
  "security_level": "critical"
}
```

#### Delete Application Service
```http
DELETE /application-services/{service_id}
```

### Service Link Management

#### Create Service Link
```http
POST /application-services/{service_id}/links
Content-Type: application/json

{
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440000",
  "linked_element_type": "business_process",
  "link_type": "supports",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "data_flow_direction": "bidirectional",
  "performance_impact": "medium",
  "latency_contribution": 50.0,
  "availability_impact": 5.0,
  "business_criticality": "high",
  "business_value": "high",
  "alignment_score": 0.8
}
```

#### List Service Links
```http
GET /application-services/{service_id}/links
```

#### Update Service Link
```http
PUT /application-services/links/{link_id}
Content-Type: application/json

{
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "performance_impact": "low"
}
```

#### Delete Service Link
```http
DELETE /application-services/links/{link_id}
```

### Analysis Endpoints

#### Get Impact Map
```http
GET /application-services/{service_id}/impact-map
```

#### Get Performance Score
```http
GET /application-services/{service_id}/performance-score
```

#### Analyze Service
```http
GET /application-services/{service_id}/analysis
```

### Domain-Specific Queries

#### Get by Service Type
```http
GET /application-services/by-type/api
```

#### Get by Status
```http
GET /application-services/by-status/active
```

#### Get by Capability
```http
GET /application-services/by-capability/{capability_id}
```

#### Get by Performance
```http
GET /application-services/by-performance/99.5
```

#### Get Active Services
```http
GET /application-services/active
```

#### Get Critical Services
```http
GET /application-services/critical
```

### Enumeration Endpoints

#### Get Service Types
```http
GET /application-services/service-types
```

#### Get Statuses
```http
GET /application-services/statuses
```

#### Get Business Criticalities
```http
GET /application-services/business-criticalities
```

#### Get Business Values
```http
GET /application-services/business-values
```

#### Get Delivery Channels
```http
GET /application-services/delivery-channels
```

#### Get Authentication Methods
```http
GET /application-services/authentication-methods
```

#### Get Deployment Models
```http
GET /application-services/deployment-models
```

#### Get Scaling Strategies
```http
GET /application-services/scaling-strategies
```

#### Get Security Levels
```http
GET /application-services/security-levels
```

#### Get Data Classifications
```http
GET /application-services/data-classifications
```

#### Get Link Types
```http
GET /application-services/link-types
```

#### Get Relationship Strengths
```http
GET /application-services/relationship-strengths
```

#### Get Dependency Levels
```http
GET /application-services/dependency-levels
```

#### Get Interaction Frequencies
```http
GET /application-services/interaction-frequencies
```

#### Get Interaction Types
```http
GET /application-services/interaction-types
```

#### Get Data Flow Directions
```http
GET /application-services/data-flow-directions
```

#### Get Performance Impacts
```http
GET /application-services/performance-impacts
```

### Utility Endpoints

#### Health Check
```http
GET /health
```

#### Metrics
```http
GET /metrics
```

#### Service Info
```http
GET /info
```

#### Service Capabilities
```http
GET /capabilities
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost:5432/reqarchitect` |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `REDIS_DB` | Redis database | `0` |
| `JWT_SECRET_KEY` | JWT secret key | `your-secret-key-change-in-production` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `SERVICE_PORT` | Service port | `8080` |
| `SERVICE_HOST` | Service host | `0.0.0.0` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `OTEL_ENABLED` | Enable OpenTelemetry | `True` |
| `OTEL_ENDPOINT` | OpenTelemetry endpoint | `http://localhost:4317` |

### Database Schema

The service uses the following main tables:

- `application_service`: Core application service data
- `service_link`: Relationships between services and other elements

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_applicationservice.py
```

### Code Quality

```bash
# Run linting
flake8 app/

# Run type checking
mypy app/

# Run formatting
black app/
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Monitoring & Observability

### Health Checks
- Database connectivity
- Redis connectivity
- Service status

### Metrics
- Request/response times
- Error rates
- Service performance metrics

### Tracing
- OpenTelemetry integration
- Distributed tracing
- Performance analysis

### Logging
- Structured logging
- Request/response logging
- Error tracking

## Security

### Authentication
- JWT-based authentication
- Token validation and verification
- Secure token handling

### Authorization
- Role-based access control (RBAC)
- Permission-based authorization
- Tenant isolation

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Rate limiting

## Event Integration

### Redis Events
The service emits events for all CRUD operations:

- `application_service_created`
- `application_service_updated`
- `application_service_deleted`
- `service_link_created`
- `service_link_updated`
- `service_link_deleted`

### Event Format
```json
{
  "event_type": "application_service_created",
  "service_id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "service_name": "User Authentication Service",
  "service_type": "api",
  "status": "active",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Performance

### Optimization Features
- Database connection pooling
- Redis caching
- Efficient query optimization
- Pagination support
- Rate limiting

### Scalability
- Horizontal scaling support
- Stateless design
- Microservice architecture
- Container deployment ready

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check DATABASE_URL configuration
   - Verify PostgreSQL is running
   - Check network connectivity

2. **Redis Connection Errors**
   - Check REDIS_HOST and REDIS_PORT
   - Verify Redis is running
   - Check authentication if required

3. **Authentication Errors**
   - Verify JWT token format
   - Check JWT_SECRET_KEY configuration
   - Ensure required claims are present

4. **Permission Errors**
   - Verify user role and permissions
   - Check tenant isolation
   - Review RBAC configuration

### Debug Mode

Enable debug mode for detailed logging:

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation at `/docs`
- Review the API reference at `/redoc` 