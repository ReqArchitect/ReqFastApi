# Application Function Service

A microservice for managing ArchiMate 3.2 Application Function elements in the ReqArchitect platform.

## Overview

The Application Function Service represents structured application behavior aligned to business functions and services. It provides comprehensive management of application functions with their relationships to other ArchiMate elements, performance characteristics, and operational insights.

## ArchiMate 3.2 Coverage

### Application Layer Element
- **Application Function**: Represents automated behavior that can be performed by an application component

### Relationships
- **Business Function**: Application functions support and realize business functions
- **Business Process**: Application functions enable and support business processes
- **Capability**: Application functions realize capabilities
- **Data Object**: Application functions consume and produce data objects
- **Application Service**: Application functions realize application services
- **Node**: Application functions are deployed on nodes

## Features

### Core Functionality
- ✅ Full CRUD operations for ApplicationFunction entities
- ✅ FunctionLink management for relationship tracking
- ✅ Multi-tenancy support with tenant isolation
- ✅ JWT-based authentication and RBAC enforcement
- ✅ Redis-based event emission for event-driven architecture

### Analysis & Insights
- ✅ Impact mapping and dependency analysis
- ✅ Performance scoring and recommendations
- ✅ Operational health assessment
- ✅ Business alignment analysis
- ✅ Technical debt evaluation
- ✅ Risk factor identification

### Function Types
- **Data Processing**: Core data transformation and processing functions
- **Orchestration**: Workflow and process coordination functions
- **User Interaction**: UI and user interface functions
- **Rule Engine**: Business logic and decision-making functions
- **ETL Processor**: Data extraction, transformation, and loading functions
- **User Session Manager**: Authentication and session management functions
- **Event Handler**: Event processing and response functions
- **UI Controller**: User interface control and navigation functions

### Performance Characteristics
- Response time targets and monitoring
- Throughput measurement and optimization
- Availability tracking and SLA management
- Performance impact analysis
- Resource utilization monitoring

## API Endpoints

### Application Function Management
- `POST /application-functions` - Create new application function
- `GET /application-functions` - List application functions with filtering
- `GET /application-functions/{id}` - Get application function by ID
- `PUT /application-functions/{id}` - Update application function
- `DELETE /application-functions/{id}` - Delete application function

### Function Link Management
- `POST /application-functions/{id}/links` - Create function link
- `GET /application-functions/{id}/links` - List function links
- `GET /application-functions/links/{link_id}` - Get function link by ID
- `PUT /application-functions/links/{link_id}` - Update function link
- `DELETE /application-functions/links/{link_id}` - Delete function link

### Analysis & Impact
- `GET /application-functions/{id}/impact-map` - Get impact mapping
- `GET /application-functions/{id}/performance-score` - Get performance score
- `GET /application-functions/{id}/analysis` - Get comprehensive analysis

### Domain-Specific Queries
- `GET /application-functions/by-type/{type}` - Filter by function type
- `GET /application-functions/by-status/{status}` - Filter by status
- `GET /application-functions/by-business-function/{id}` - Filter by business function
- `GET /application-functions/by-performance/{threshold}` - Filter by performance
- `GET /application-functions/by-element/{type}/{id}` - Filter by linked element
- `GET /application-functions/active` - Get active functions
- `GET /application-functions/critical` - Get critical functions

### Enumeration Endpoints
- `GET /application-functions/function-types` - Available function types
- `GET /application-functions/statuses` - Available statuses
- `GET /application-functions/business-criticalities` - Business criticality levels
- `GET /application-functions/business-values` - Business value levels
- `GET /application-functions/operational-hours` - Operational hour types
- `GET /application-functions/security-levels` - Security levels
- `GET /application-functions/link-types` - Link types
- `GET /application-functions/relationship-strengths` - Relationship strengths
- `GET /application-functions/dependency-levels` - Dependency levels
- `GET /application-functions/interaction-frequencies` - Interaction frequencies
- `GET /application-functions/interaction-types` - Interaction types
- `GET /application-functions/data-flow-directions` - Data flow directions
- `GET /application-functions/performance-impacts` - Performance impact levels

## Data Model

### ApplicationFunction
```python
class ApplicationFunction:
    id: UUID
    tenant_id: UUID
    user_id: UUID
    name: str
    description: Optional[str]
    purpose: Optional[str]
    technology_stack: Optional[str]
    module_location: Optional[str]
    function_type: FunctionType
    performance_characteristics: Optional[str]
    response_time_target: Optional[float]
    throughput_target: Optional[float]
    availability_target: float
    current_availability: float
    business_criticality: BusinessCriticality
    business_value: BusinessValue
    status: FunctionStatus
    operational_hours: OperationalHours
    maintenance_window: Optional[str]
    api_endpoints: Optional[str]
    data_sources: Optional[str]
    data_sinks: Optional[str]
    error_handling: Optional[str]
    logging_config: Optional[str]
    security_level: SecurityLevel
    compliance_requirements: Optional[str]
    access_controls: Optional[str]
    audit_requirements: Optional[str]
    monitoring_config: Optional[str]
    alerting_rules: Optional[str]
    health_check_endpoint: Optional[str]
    metrics_endpoint: Optional[str]
    parent_function_id: Optional[UUID]
    application_service_id: Optional[UUID]
    data_object_id: Optional[UUID]
    node_id: Optional[UUID]
    supported_business_function_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
```

### FunctionLink
```python
class FunctionLink:
    id: UUID
    application_function_id: UUID
    linked_element_id: UUID
    linked_element_type: str
    link_type: LinkType
    relationship_strength: RelationshipStrength
    dependency_level: DependencyLevel
    interaction_frequency: InteractionFrequency
    interaction_type: InteractionType
    data_flow_direction: DataFlowDirection
    performance_impact: PerformanceImpact
    latency_contribution: Optional[float]
    throughput_impact: Optional[float]
    created_by: UUID
    created_at: datetime
```

## Architecture

### Multi-Tenancy
- Tenant isolation via `tenant_id` field
- JWT token-based tenant identification
- Cross-tenant data access prevention

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- Permission matrix for all operations
- User and tenant context tracking

### Event-Driven Architecture
- Redis-based event emission
- Event types: created, updated, deleted
- Correlation ID tracking
- Event-driven integration with other services

### Observability
- Structured JSON logging
- Prometheus metrics collection
- OpenTelemetry tracing
- Health check endpoints
- Performance monitoring

### Database
- PostgreSQL with SQLAlchemy ORM
- Alembic for database migrations
- Connection pooling
- Transaction management

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/applicationfunction_service

# Security
SECRET_KEY=your-secret-key-here

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Environment
ENVIRONMENT=development
```

## Development

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- Docker (optional)

### Installation
```bash
# Clone the repository
cd services/applicationfunction_service

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost:5432/applicationfunction_service"
export SECRET_KEY="your-secret-key-here"
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
export REDIS_DB="0"

# Run the service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run linting
flake8 app/
bandit -r app/
```

### Docker
```bash
# Build image
docker build -t applicationfunction-service .

# Run container
docker run -p 8080:8080 applicationfunction-service
```

## API Documentation

Once the service is running, visit:
- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`
- **OpenAPI JSON**: `http://localhost:8080/openapi.json`

## Health & Monitoring

- **Health Check**: `GET /health`
- **Metrics**: `GET /metrics`
- **Service Info**: `GET /`

## Integration

### Event Types
- `application_function.created`
- `application_function.updated`
- `application_function.deleted`
- `function_link.created`
- `function_link.updated`
- `function_link.deleted`

### Related Services
- **Business Function Service**: For business function relationships
- **Business Process Service**: For process enablement
- **Capability Service**: For capability realization
- **Data Object Service**: For data object relationships
- **Application Service Service**: For service realization
- **Node Service**: For deployment relationships

## Security

### RBAC Permissions
- `application_function:create` - Create application functions
- `application_function:read` - Read application functions
- `application_function:update` - Update application functions
- `application_function:delete` - Delete application functions
- `function_link:create` - Create function links
- `function_link:read` - Read function links
- `function_link:update` - Update function links
- `function_link:delete` - Delete function links
- `impact:read` - Read impact analysis
- `analysis:read` - Read operational analysis
- `performance:read` - Read performance metrics

### Roles
- **Owner**: Full access to all operations
- **Admin**: Full access except deletion
- **Editor**: Create, read, update operations
- **Viewer**: Read-only access

## Performance

### Optimization Features
- Database query optimization
- Connection pooling
- Caching strategies
- Pagination support
- Filtering and sorting
- Index optimization

### Monitoring
- Request latency tracking
- Error rate monitoring
- Database connection health
- Redis connection status
- Memory and CPU usage
- Custom business metrics

## Troubleshooting

### Common Issues
1. **Database Connection**: Check DATABASE_URL and PostgreSQL status
2. **Redis Connection**: Verify Redis is running and accessible
3. **Authentication**: Ensure valid JWT token with required claims
4. **Permissions**: Verify user has required RBAC permissions
5. **Tenant Isolation**: Check tenant_id in JWT token

### Logs
- Structured JSON logging
- Correlation ID tracking
- Request/response logging
- Error stack traces
- Performance metrics

### Metrics
- Request count and latency
- Error rates by endpoint
- Database query performance
- Redis operation metrics
- Custom business metrics

## Contributing

1. Follow the established code patterns
2. Add comprehensive tests
3. Update documentation
4. Follow security best practices
5. Maintain backward compatibility

## License

This service is part of the ReqArchitect platform and follows the same licensing terms.
