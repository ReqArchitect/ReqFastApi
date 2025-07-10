# Business Role Service

A microservice for managing business roles in the ReqArchitect platform, representing the ArchiMate 3.2 "Business Role" element within the Business Layer.

## Overview

The Business Role Service manages organizational responsibilities performed by individuals or groups, providing comprehensive CRUD operations, analysis capabilities, and integration with other ArchiMate elements.

## Features

### Core Functionality
- **Business Role Management**: Full CRUD operations for business roles
- **Role Link Management**: Create and manage relationships between roles and other elements
- **Multi-tenancy**: Complete tenant isolation for all operations
- **RBAC**: Role-based access control with Owner/Admin/Editor/Viewer permissions
- **JWT Authentication**: Secure token-based authentication

### Analysis Capabilities
- **Responsibility Mapping**: Analyze role responsibilities and linked elements
- **Alignment Scoring**: Calculate strategic and capability alignment scores
- **Performance Metrics**: Track role performance and effectiveness
- **Domain Queries**: Filter roles by organizational unit, type, importance, etc.

### Observability
- **Health Checks**: `/health` endpoint for service status
- **Metrics**: Prometheus metrics for monitoring
- **Tracing**: OpenTelemetry integration with Jaeger
- **Structured Logging**: Comprehensive logging with correlation IDs

### Event-Driven Architecture
- **Redis Integration**: Event emission for role lifecycle changes
- **Event Types**: Created, updated, deleted events for roles and links
- **Event Details**: Rich event payloads with relevant metadata

## Architecture

### Domain Models

#### BusinessRole
Represents a business role with comprehensive attributes:

- **Core Fields**: name, description, organizational_unit, role_type
- **Classification**: role_classification, authority_level, decision_making_authority
- **Strategic Context**: strategic_importance, business_value, capability_alignment
- **Performance**: performance_score, effectiveness_score, efficiency_score
- **Operational**: criticality, complexity, workload_level, availability_requirement
- **Resources**: headcount_requirement, current_headcount, skill_gaps
- **Governance**: compliance_requirements, risk_level, audit_frequency
- **Financial**: cost_center, budget_allocation, salary_range, total_compensation

#### RoleLink
Represents relationships between business roles and other elements:

- **Link Details**: linked_element_id, linked_element_type, link_type
- **Relationship Strength**: relationship_strength, dependency_level
- **Interaction**: interaction_frequency, interaction_type, responsibility_level
- **Accountability**: accountability_level, performance_impact, decision_authority

### Role Types
- Architecture Lead
- Compliance Officer
- Strategy Analyst
- Vendor Manager
- Data Custodian
- Security Officer
- Risk Manager
- Quality Assurance Lead
- Change Manager
- Capacity Planner
- Cost Manager
- Performance Analyst
- Stakeholder Manager
- Technology Evaluator
- Process Optimizer

## API Endpoints

### Business Role Management
- `POST /api/v1/business-roles` - Create a new business role
- `GET /api/v1/business-roles/{role_id}` - Get a business role by ID
- `GET /api/v1/business-roles` - List business roles with filtering
- `PUT /api/v1/business-roles/{role_id}` - Update a business role
- `DELETE /api/v1/business-roles/{role_id}` - Delete a business role

### Role Link Management
- `POST /api/v1/business-roles/{role_id}/links` - Create a role link
- `GET /api/v1/business-roles/{role_id}/links` - Get role links
- `GET /api/v1/role-links/{link_id}` - Get a role link by ID
- `PUT /api/v1/role-links/{link_id}` - Update a role link
- `DELETE /api/v1/role-links/{link_id}` - Delete a role link

### Analysis Endpoints
- `GET /api/v1/business-roles/{role_id}/responsibility-map` - Get responsibility map
- `GET /api/v1/business-roles/{role_id}/alignment-score` - Get alignment analysis

### Domain Query Endpoints
- `GET /api/v1/business-roles/organizational-unit/{unit}` - Filter by organizational unit
- `GET /api/v1/business-roles/role-type/{type}` - Filter by role type
- `GET /api/v1/business-roles/strategic-importance/{importance}` - Filter by strategic importance
- `GET /api/v1/business-roles/authority-level/{level}` - Filter by authority level
- `GET /api/v1/business-roles/status/{status}` - Filter by status
- `GET /api/v1/business-roles/stakeholder/{stakeholder_id}` - Filter by stakeholder
- `GET /api/v1/business-roles/capability/{capability_id}` - Filter by capability
- `GET /api/v1/business-roles/function/{function_id}` - Filter by business function
- `GET /api/v1/business-roles/process/{process_id}` - Filter by business process
- `GET /api/v1/business-roles/element/{element_type}/{element_id}` - Filter by linked element
- `GET /api/v1/business-roles/active` - Get active roles
- `GET /api/v1/business-roles/critical` - Get critical roles
- `GET /api/v1/business-roles/classification/{classification}` - Filter by classification
- `GET /api/v1/business-roles/criticality/{criticality}` - Filter by criticality
- `GET /api/v1/business-roles/workload/{workload_level}` - Filter by workload
- `GET /api/v1/business-roles/availability/{requirement}` - Filter by availability
- `GET /api/v1/business-roles/risk-level/{risk_level}` - Filter by risk level
- `GET /api/v1/business-roles/business-value/{value}` - Filter by business value
- `GET /api/v1/business-roles/decision-authority/{authority}` - Filter by decision authority
- `GET /api/v1/business-roles/approval-authority/{authority}` - Filter by approval authority

### Observability Endpoints
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /` - Service information

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- Docker (optional)

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/businessrole_service

# Authentication
SECRET_KEY=your-secret-key

# Redis
REDIS_URL=redis://localhost:6379/0

# Observability
JAEGER_HOST=localhost
JAEGER_PORT=6831
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Docker Deployment
```bash
# Build the image
docker build -t business-role-service .

# Run the container
docker run -p 8080:8080 business-role-service
```

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_business_roles.py
```

### Test Coverage
- Unit tests for all service functions
- Integration tests for API endpoints
- Authentication and authorization tests
- Validation tests for all schemas
- Event emission tests

## Security

### Authentication
- JWT-based authentication
- Token validation on all protected endpoints
- Automatic token extraction from Authorization header

### Authorization
- Role-based access control (RBAC)
- Permission matrix for different operations
- Tenant isolation for all data access

### Data Validation
- Comprehensive input validation using Pydantic
- Enum validation for all categorical fields
- Range validation for numeric fields
- Required field validation

## Monitoring

### Metrics
- Request count by method, endpoint, and status
- Request latency distribution
- Database connection metrics
- Custom business metrics

### Logging
- Structured logging with correlation IDs
- Request/response logging
- Error logging with stack traces
- Performance logging

### Tracing
- Distributed tracing with OpenTelemetry
- Jaeger integration for trace visualization
- Span correlation across services

## Integration

### Event Bus
- Redis pub/sub for event emission
- Event types: business_role.created, business_role.updated, business_role.deleted
- Event types: role_link.created, role_link.updated, role_link.deleted
- Rich event payloads with relevant metadata

### Database
- PostgreSQL with SQLAlchemy ORM
- Alembic for database migrations
- Connection pooling and optimization

### External Services
- Integration with other ReqArchitect microservices
- Cross-service queries and relationships
- Event-driven communication patterns

## Deployment

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: business-role-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: business-role-service
  template:
    metadata:
      labels:
        app: business-role-service
    spec:
      containers:
      - name: business-role-service
        image: business-role-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: auth-secret
              key: secret
```

### Health Checks
- Readiness probe: `/health`
- Liveness probe: `/health`
- Startup probe: `/health`

## Contributing

1. Follow the established code patterns
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Ensure proper error handling and validation
5. Follow security best practices

## License

This service is part of the ReqArchitect platform and follows the same licensing terms.
