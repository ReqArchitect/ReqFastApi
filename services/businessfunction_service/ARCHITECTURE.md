# Business Function Service Architecture

## Overview

The Business Function Service is a microservice within the ReqArchitect platform that manages ArchiMate 3.2 Business Function elements. It follows a clean architecture pattern with clear separation of concerns, event-driven design, and comprehensive observability.

## Architecture Principles

### Clean Architecture
- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and business rules
- **Infrastructure Layer**: External dependencies and persistence
- **Interface Layer**: API endpoints and controllers

### Event-Driven Design
- **Redis Integration**: Event emission for lifecycle changes
- **Loose Coupling**: Services communicate via events
- **Scalability**: Horizontal scaling through event-driven patterns

### Multi-Tenancy
- **Tenant Isolation**: Complete data separation by tenant
- **JWT Authentication**: Tenant-scoped operations
- **RBAC**: Role-based access control per tenant

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Business Function Service                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Routes    │  │  Services   │  │   Models    │        │
│  │   (API)     │  │ (Business)  │  │ (Domain)    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Schemas   │  │   Dependencies │ │  Database   │        │
│  │ (Validation)│  │ (Auth/RBAC)  │ │ (PostgreSQL) │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Observability│  │   Events    │  │   Health    │        │
│  │ (Metrics/   │  │   (Redis)   │  │   Checks    │        │
│  │  Tracing)   │  │             │  │             │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Routes Layer (API Controllers)
**File**: `app/routes.py`

**Responsibilities**:
- HTTP request/response handling
- Input validation and serialization
- Authentication and authorization
- Error handling and status codes

**Key Components**:
- FastAPI router with comprehensive endpoints
- RBAC permission checking
- Tenant and user context extraction
- Response formatting and error handling

**Endpoints**:
- CRUD operations for Business Functions
- Function link management
- Analysis and impact mapping
- Domain-specific queries
- Utility endpoints for enums

### 2. Services Layer (Business Logic)
**File**: `app/services.py`

**Responsibilities**:
- Core business logic implementation
- Domain operations and validations
- Event emission for lifecycle changes
- Data transformation and aggregation

**Key Components**:
- Business function CRUD operations
- Function link management
- Impact analysis and health scoring
- Domain query implementations
- Redis event emission

**Business Rules**:
- Tenant isolation enforcement
- Data validation and integrity
- Performance score calculations
- Risk assessment algorithms
- Strategic importance evaluation

### 3. Models Layer (Domain Entities)
**File**: `app/models.py`

**Responsibilities**:
- Database entity definitions
- Relationship mappings
- Domain object modeling
- Data persistence structure

**Key Components**:
- `BusinessFunction`: Core domain entity
- `FunctionLink`: Relationship entity
- SQLAlchemy ORM mappings
- Database constraints and indexes

**Domain Model**:
- 40+ attributes for comprehensive modeling
- Enumerated types for consistency
- Audit fields for traceability
- Relationship mappings for ArchiMate elements

### 4. Schemas Layer (Data Validation)
**File**: `app/schemas.py`

**Responsibilities**:
- Request/response data validation
- Pydantic model definitions
- Input sanitization and transformation
- API contract enforcement

**Key Components**:
- Request/response schemas
- Enum definitions for consistency
- Validation rules and constraints
- Data transformation logic

**Validation Rules**:
- Score ranges (0.0 to 1.0)
- Availability percentages (0.0 to 100.0)
- Budget allocation (non-negative)
- String length constraints
- UUID format validation

### 5. Dependencies Layer (Infrastructure)
**File**: `app/deps.py`

**Responsibilities**:
- Dependency injection
- Authentication and authorization
- Database session management
- RBAC permission checking

**Key Components**:
- JWT token validation
- Tenant and user extraction
- Role-based permission matrix
- Database session management

**Security Model**:
- JWT-based authentication
- Role-based access control
- Tenant isolation
- Permission granularity

### 6. Database Layer (Persistence)
**File**: `app/database.py`

**Responsibilities**:
- Database connection management
- SQLAlchemy configuration
- Session lifecycle management
- Connection pooling

**Key Components**:
- PostgreSQL connection setup
- SQLAlchemy engine configuration
- Session factory management
- Environment-based configuration

## Data Architecture

### Database Schema

#### BusinessFunction Table
```sql
CREATE TABLE business_function (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    user_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    competency_area VARCHAR(100) NOT NULL,
    organizational_unit VARCHAR(255) NOT NULL,
    owner_role_id UUID,
    input_object_type VARCHAR(100),
    output_object_type VARCHAR(100),
    input_description TEXT,
    output_description TEXT,
    frequency VARCHAR(50) NOT NULL DEFAULT 'ongoing',
    criticality VARCHAR(50) NOT NULL DEFAULT 'medium',
    complexity VARCHAR(50) DEFAULT 'medium',
    maturity_level VARCHAR(50) DEFAULT 'basic',
    alignment_score FLOAT DEFAULT 0.0,
    efficiency_score FLOAT DEFAULT 0.0,
    effectiveness_score FLOAT DEFAULT 0.0,
    performance_metrics TEXT,
    required_skills TEXT,
    required_capabilities TEXT,
    resource_requirements TEXT,
    technology_dependencies TEXT,
    compliance_requirements TEXT,
    risk_level VARCHAR(50) DEFAULT 'medium',
    audit_frequency VARCHAR(50) DEFAULT 'annually',
    last_audit_date TIMESTAMP,
    audit_status VARCHAR(50) DEFAULT 'pending',
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    operational_hours VARCHAR(50) DEFAULT 'business_hours',
    availability_target FLOAT DEFAULT 99.0,
    current_availability FLOAT DEFAULT 100.0,
    strategic_importance VARCHAR(50) DEFAULT 'medium',
    business_value VARCHAR(50) DEFAULT 'medium',
    cost_center VARCHAR(100),
    budget_allocation FLOAT,
    parent_function_id UUID,
    supporting_capability_id UUID,
    business_process_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### FunctionLink Table
```sql
CREATE TABLE function_link (
    id UUID PRIMARY KEY,
    business_function_id UUID NOT NULL,
    linked_element_id UUID NOT NULL,
    linked_element_type VARCHAR(100) NOT NULL,
    link_type VARCHAR(50) NOT NULL,
    relationship_strength VARCHAR(50) DEFAULT 'medium',
    dependency_level VARCHAR(50) DEFAULT 'medium',
    interaction_frequency VARCHAR(50) DEFAULT 'regular',
    interaction_type VARCHAR(50) DEFAULT 'synchronous',
    data_flow_direction VARCHAR(50) DEFAULT 'bidirectional',
    created_by UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes and Constraints
```sql
-- Performance indexes
CREATE INDEX idx_business_function_tenant ON business_function(tenant_id);
CREATE INDEX idx_business_function_competency ON business_function(competency_area);
CREATE INDEX idx_business_function_organizational ON business_function(organizational_unit);
CREATE INDEX idx_business_function_criticality ON business_function(criticality);
CREATE INDEX idx_business_function_status ON business_function(status);
CREATE INDEX idx_business_function_owner ON business_function(owner_role_id);

-- Foreign key constraints
ALTER TABLE business_function ADD CONSTRAINT fk_business_function_tenant 
    FOREIGN KEY (tenant_id) REFERENCES tenant(id);
ALTER TABLE business_function ADD CONSTRAINT fk_business_function_user 
    FOREIGN KEY (user_id) REFERENCES user(id);
ALTER TABLE business_function ADD CONSTRAINT fk_business_function_owner_role 
    FOREIGN KEY (owner_role_id) REFERENCES business_role(id);
ALTER TABLE business_function ADD CONSTRAINT fk_business_function_parent 
    FOREIGN KEY (parent_function_id) REFERENCES business_function(id);
ALTER TABLE business_function ADD CONSTRAINT fk_business_function_capability 
    FOREIGN KEY (supporting_capability_id) REFERENCES capability(id);
ALTER TABLE business_function ADD CONSTRAINT fk_business_function_process 
    FOREIGN KEY (business_process_id) REFERENCES business_process(id);

-- Function link constraints
ALTER TABLE function_link ADD CONSTRAINT fk_function_link_business_function 
    FOREIGN KEY (business_function_id) REFERENCES business_function(id);
ALTER TABLE function_link ADD CONSTRAINT fk_function_link_created_by 
    FOREIGN KEY (created_by) REFERENCES user(id);
```

## Event Architecture

### Event Types
```json
{
  "event_type": "business_function.created",
  "business_function_id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "timestamp": "2024-01-01T00:00:00Z",
  "details": {
    "name": "Architecture Governance",
    "competency_area": "Architecture Governance",
    "organizational_unit": "IT Department",
    "criticality": "high",
    "status": "active"
  }
}
```

### Event Channels
- **business_function_events**: All business function lifecycle events
- **function_link_events**: All function link lifecycle events

### Event Consumers
- **Monitoring Service**: Performance tracking and alerting
- **Analytics Service**: Business intelligence and reporting
- **Notification Service**: User notifications and alerts
- **Audit Service**: Compliance and audit trail

## Security Architecture

### Authentication Flow
1. **JWT Token Validation**: Extract and validate JWT token
2. **Tenant Extraction**: Extract tenant_id from token
3. **User Validation**: Validate user_id and permissions
4. **Role Verification**: Check user role for endpoint access

### RBAC Permission Matrix
```python
permissions = {
    "business_function:create": ["Owner", "Admin", "Editor"],
    "business_function:read": ["Owner", "Admin", "Editor", "Viewer"],
    "business_function:update": ["Owner", "Admin", "Editor"],
    "business_function:delete": ["Owner", "Admin"],
    "function_link:create": ["Owner", "Admin", "Editor"],
    "function_link:read": ["Owner", "Admin", "Editor", "Viewer"],
    "function_link:update": ["Owner", "Admin", "Editor"],
    "function_link:delete": ["Owner", "Admin"],
    "impact:read": ["Owner", "Admin", "Editor", "Viewer"],
    "analysis:read": ["Owner", "Admin", "Editor", "Viewer"]
}
```

### Data Protection
- **Tenant Isolation**: Complete data separation by tenant
- **Input Validation**: Comprehensive input sanitization
- **SQL Injection Prevention**: Parameterized queries
- **XSS Prevention**: Output encoding and validation

## Observability Architecture

### Metrics Collection
```python
# Prometheus metrics
REQUESTS_TOTAL = Counter(
    "business_function_service_requests_total",
    "Total requests",
    ["method", "route", "status"]
)
REQUEST_LATENCY = Histogram(
    "business_function_service_request_latency_seconds_bucket",
    "Request latency",
    ["method", "route"]
)
ERRORS_TOTAL = Counter(
    "business_function_service_errors_total",
    "Total errors",
    ["method", "route"]
)
```

### Tracing Implementation
```python
# OpenTelemetry tracing
with tracer.start_as_current_span(f"{method} {route}") as span:
    span.set_attribute("tenant_id", tenant_id)
    span.set_attribute("user_id", user_id)
    span.set_attribute("correlation_id", correlation_id)
```

### Logging Strategy
```python
# Structured JSON logging
{
    "timestamp": "2024-01-01T00:00:00Z",
    "service": "business_function_service",
    "version": "1.0.0",
    "tenant_id": "uuid",
    "user_id": "uuid",
    "correlation_id": "uuid",
    "route": "/business-functions/",
    "method": "POST",
    "status_code": 201,
    "latency_ms": 150
}
```

## Performance Architecture

### Caching Strategy
- **Redis Integration**: Event emission and caching
- **Database Connection Pooling**: Optimized connection management
- **Query Optimization**: Indexed queries and efficient joins

### Scalability Patterns
- **Horizontal Scaling**: Stateless service design
- **Database Sharding**: Tenant-based data distribution
- **Load Balancing**: Multiple service instances
- **Event-Driven**: Asynchronous processing

### Performance Monitoring
- **Request Latency**: Response time tracking
- **Throughput**: Requests per second
- **Error Rates**: Error percentage monitoring
- **Resource Utilization**: CPU, memory, database usage

## Deployment Architecture

### Container Strategy
```dockerfile
# Multi-stage build for optimization
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Environment Configuration
```bash
# Required environment variables
DATABASE_URL=postgresql://user:password@localhost:5432/businessfunction_service
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
ENVIRONMENT=development
```

### Health Checks
```python
# Health check implementation
{
    "service": "business_function_service",
    "version": "1.0.0",
    "status": "healthy",
    "uptime": "3600.00s",
    "total_requests": 1500,
    "error_rate": 0.02,
    "database_connected": true,
    "timestamp": "2024-01-01T00:00:00Z",
    "environment": "development"
}
```

## Integration Architecture

### Upstream Dependencies
- **Auth Service**: JWT token validation
- **Tenant Service**: Multi-tenant management
- **User Service**: User management and roles

### Downstream Consumers
- **Event Bus**: Redis event consumption
- **Monitoring**: Prometheus metrics collection
- **Tracing**: OpenTelemetry span collection
- **Logging**: Centralized log aggregation

### Related Services
- **Business Role Service**: Owner role relationships
- **Business Process Service**: Process function relationships
- **Capability Service**: Supporting capability relationships
- **Application Service**: Service function relationships
- **Data Object Service**: Input/output data relationships

## Testing Architecture

### Test Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: Service interaction testing
- **API Tests**: Endpoint functionality testing
- **Performance Tests**: Load and stress testing

### Test Coverage
- **Business Logic**: 100% service layer coverage
- **API Endpoints**: 100% route coverage
- **Data Validation**: 100% schema validation coverage
- **Security**: Authentication and authorization testing

## Monitoring and Alerting

### Key Metrics
- **Request Rate**: Requests per second
- **Response Time**: Average and percentile latencies
- **Error Rate**: Error percentage
- **Database Performance**: Query execution times
- **Resource Usage**: CPU, memory, disk usage

### Alerting Rules
- **High Error Rate**: > 5% error rate
- **High Latency**: > 2s average response time
- **Database Issues**: Connection failures
- **Service Unavailable**: Health check failures

## Disaster Recovery

### Backup Strategy
- **Database Backups**: Daily automated backups
- **Configuration Backups**: Environment configuration
- **Code Backups**: Version control and deployment artifacts

### Recovery Procedures
- **Service Restart**: Automatic restart on failure
- **Database Recovery**: Point-in-time recovery
- **Data Restoration**: Backup restoration procedures
- **Service Migration**: Failover to backup instances

## Security Considerations

### Data Protection
- **Encryption**: Data encryption at rest and in transit
- **Access Control**: Role-based access control
- **Audit Logging**: Comprehensive audit trails
- **Input Validation**: Strict input sanitization

### Compliance
- **GDPR**: Data protection and privacy
- **SOX**: Financial reporting compliance
- **ISO 27001**: Information security management
- **Industry Standards**: Best practice compliance

## Future Enhancements

### Planned Improvements
- **GraphQL API**: Alternative query interface
- **Real-time Updates**: WebSocket support
- **Advanced Analytics**: Machine learning insights
- **Workflow Integration**: Process automation

### Scalability Enhancements
- **Microservice Splitting**: Domain-based service separation
- **Event Sourcing**: Complete event-driven architecture
- **CQRS**: Command-query responsibility segregation
- **Distributed Tracing**: Enhanced observability 