# Business Process Service

A microservice for managing business processes in the ReqArchitect platform, representing the ArchiMate 3.2 "Business Process" element within the Business Layer.

## Overview

The Business Process Service manages sequences of business behavior performed by roles to deliver business value. It provides comprehensive CRUD operations, process analysis, and domain-specific queries for business processes, process steps, and process links.

## Features

### Core Functionality
- **Business Process Management**: Full CRUD operations for business processes
- **Process Steps**: Manage individual steps within business processes
- **Process Links**: Connect processes to other ArchiMate elements
- **Multi-tenancy**: Complete tenant isolation
- **Role-based Access Control**: Owner/Admin/Editor/Viewer permissions

### Analysis Capabilities
- **Process Flow Mapping**: Analyze process complexity and flow
- **Realization Health**: Assess process performance and effectiveness
- **Domain Queries**: Query processes by role, function, goal, status, criticality

### Technical Features
- **JWT Authentication**: Secure API access
- **Redis Event Emission**: Event-driven architecture integration
- **Observability**: Prometheus metrics, OpenTelemetry tracing, structured logging
- **Validation**: Comprehensive input validation and schema enforcement

## Architecture

### ArchiMate Alignment
- **Layer**: Business Layer
- **Element**: Business Process
- **Relationships**: 
  - Realizes Business Functions
  - Supported by Business Roles
  - Uses Application Services
  - Produces/Consumes Data Objects
  - Realizes Goals
  - Enabled by Capabilities

### Domain Models

#### BusinessProcess
Core entity representing a business process with attributes:
- Basic info: name, description, process_type, organizational_unit
- Classification: criticality, complexity, automation_level
- Performance: performance_score, effectiveness_score, efficiency_score, quality_score
- Operational: status, priority, frequency, duration metrics
- Governance: compliance, audit, risk management
- Financial: cost center, budget, ROI metrics
- Technology: automation tools, integration points, data requirements

#### ProcessStep
Sub-entity for sequencing tasks, responsibilities, and handoffs:
- Step characteristics: order, type, responsible roles/actors
- Performance: duration estimates, quality scores, bottleneck indicators
- Automation: automation level, tools, integration points
- Governance: approval requirements, quality gates, compliance checks

#### ProcessLink
Relationship entity connecting processes to other ArchiMate elements:
- Link characteristics: element type, link type, relationship strength
- Interaction: frequency, type, responsibility level
- Impact: performance, business value, risk impact
- Flow: direction, sequence, handoff type

## API Endpoints

### Business Process CRUD
- `POST /api/v1/business-processes/` - Create business process
- `GET /api/v1/business-processes/` - List business processes (with filtering)
- `GET /api/v1/business-processes/{id}` - Get specific business process
- `PUT /api/v1/business-processes/{id}` - Update business process
- `DELETE /api/v1/business-processes/{id}` - Delete business process

### Analysis Endpoints
- `GET /api/v1/business-processes/{id}/flow-map` - Process flow analysis
- `GET /api/v1/business-processes/{id}/realization-health` - Process health assessment

### Domain Queries
- `GET /api/v1/business-processes/by-role/{role_id}` - Processes by role
- `GET /api/v1/business-processes/by-function/{function_id}` - Processes by function
- `GET /api/v1/business-processes/by-goal/{goal_id}` - Processes by goal
- `GET /api/v1/business-processes/by-status/{status}` - Processes by status
- `GET /api/v1/business-processes/by-criticality/{criticality}` - Processes by criticality

### Process Steps
- `POST /api/v1/business-processes/{id}/steps/` - Create process step
- `GET /api/v1/business-processes/{id}/steps/` - List process steps
- `PUT /api/v1/steps/{step_id}` - Update process step
- `DELETE /api/v1/steps/{step_id}` - Delete process step

### Process Links
- `POST /api/v1/business-processes/{id}/links/` - Create process link
- `GET /api/v1/business-processes/{id}/links/` - List process links
- `PUT /api/v1/links/{link_id}` - Update process link
- `DELETE /api/v1/links/{link_id}` - Delete process link

### Health & Metrics
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
DATABASE_URL=postgresql://user:password@localhost:5432/businessprocess_service

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# JWT
SECRET_KEY=your-secret-key

# Observability
JAEGER_HOST=localhost
JAEGER_PORT=6831
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Docker Deployment
```bash
# Build image
docker build -t businessprocess-service .

# Run container
docker run -p 8080:8080 businessprocess-service
```

## Usage Examples

### Create Business Process
```bash
curl -X POST "http://localhost:8080/api/v1/business-processes/" \
  -H "Authorization: Bearer <jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Order Processing",
    "description": "End-to-end customer order processing workflow",
    "process_type": "operational",
    "organizational_unit": "Sales Department",
    "criticality": "high",
    "complexity": "medium",
    "automation_level": "semi_automated"
  }'
```

### Get Process Flow Map
```bash
curl -X GET "http://localhost:8080/api/v1/business-processes/{id}/flow-map" \
  -H "Authorization: Bearer <jwt-token>"
```

### Query Processes by Role
```bash
curl -X GET "http://localhost:8080/api/v1/business-processes/by-role/{role_id}" \
  -H "Authorization: Bearer <jwt-token>"
```

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_business_processes.py
```

### Test Coverage
- Unit tests for all service methods
- Integration tests for API endpoints
- Authentication and authorization tests
- Validation and error handling tests

## Monitoring

### Metrics
- Request count and latency
- Database connection health
- Redis connection status
- Process creation/update/deletion rates

### Logging
- Structured JSON logging
- Request/response logging
- Error logging with stack traces
- Performance logging

### Tracing
- OpenTelemetry integration
- Jaeger tracing
- Database query tracing
- Redis operation tracing

## Security

### Authentication
- JWT-based authentication
- Token validation and expiration
- Secure token storage

### Authorization
- Role-based access control
- Permission hierarchy: Owner > Admin > Editor > Viewer
- Tenant isolation

### Input Validation
- Pydantic schema validation
- Field-level constraints
- Enum enforcement
- SQL injection prevention

## Integration

### Event Bus
- Redis-based event emission
- Event types: created, updated, deleted
- Event payload includes relevant metadata

### External Services
- Authentication service integration
- Notification service integration
- Monitoring dashboard integration

## Development

### Code Structure
```
app/
├── __init__.py
├── database.py      # Database configuration
├── models.py        # SQLAlchemy models
├── schemas.py       # Pydantic schemas
├── deps.py          # Dependencies and auth
├── services.py      # Business logic
├── routes.py        # API endpoints
└── main.py          # FastAPI application
```

### Adding New Features
1. Update models if needed
2. Add schemas for validation
3. Implement business logic in services
4. Add API endpoints in routes
5. Write tests
6. Update documentation

## Contributing

1. Follow the established code patterns
2. Add comprehensive tests
3. Update documentation
4. Ensure security best practices
5. Follow the ReqArchitect architecture standards

## License

This service is part of the ReqArchitect platform and follows the same licensing terms.
