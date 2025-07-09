# Architecture: goal_service

## Overview

The Goal Service is a microservice within the ReqArchitect platform that manages ArchiMate 3.2 Goal elements. It provides comprehensive goal lifecycle management, realization mapping, progress tracking, and strategic analysis capabilities.

## Architecture Principles

### 1. Domain-Driven Design
- **Goal Domain**: Core business entity representing strategic targets
- **GoalLink Domain**: Relationship management between goals and other elements
- **Bounded Context**: Clear boundaries around goal management

### 2. Multi-Tenant Architecture
- Complete tenant isolation at the database level
- Tenant-scoped queries and operations
- Tenant-specific event emission

### 3. Event-Driven Architecture
- Redis-based event emission for integration
- Asynchronous communication with other services
- Event sourcing for audit trails

### 4. Observability-First
- Structured JSON logging
- Prometheus metrics collection
- OpenTelemetry distributed tracing
- Health checks and monitoring

## Technology Stack

### Core Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations

### Database
- **PostgreSQL**: Primary database for goal data
- **Alembic**: Database migration management

### Event System
- **Redis**: Event bus for inter-service communication
- **JSON**: Event payload format

### Observability
- **Prometheus**: Metrics collection and export
- **OpenTelemetry**: Distributed tracing
- **Structured Logging**: JSON-formatted logs

### Security
- **JWT**: Authentication and authorization
- **RBAC**: Role-based access control
- **Tenant Isolation**: Multi-tenant security

## Data Model

### Goal Entity
```sql
CREATE TABLE goal (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    user_id UUID NOT NULL,
    
    -- Core fields
    name VARCHAR(255) NOT NULL,
    description TEXT,
    goal_type VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    
    -- Strategic context
    origin_driver_id UUID,
    stakeholder_id UUID,
    business_actor_id UUID,
    
    -- Success criteria and measurement
    success_criteria TEXT,
    key_performance_indicators TEXT,
    measurement_frequency VARCHAR(20),
    
    -- Timeline and milestones
    target_date TIMESTAMP,
    start_date TIMESTAMP,
    completion_date TIMESTAMP,
    review_frequency VARCHAR(20),
    
    -- Progress tracking
    progress_percentage INTEGER DEFAULT 0,
    progress_notes TEXT,
    last_progress_update TIMESTAMP,
    
    -- Alignment and dependencies
    parent_goal_id UUID,
    strategic_alignment VARCHAR(20),
    business_value VARCHAR(20),
    risk_level VARCHAR(20) DEFAULT 'medium',
    
    -- Assessment and evaluation
    assessment_status VARCHAR(20) DEFAULT 'pending',
    assessment_score INTEGER,
    assessment_notes TEXT,
    last_assessment_date TIMESTAMP,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### GoalLink Entity
```sql
CREATE TABLE goal_link (
    id UUID PRIMARY KEY,
    goal_id UUID NOT NULL,
    linked_element_id UUID NOT NULL,
    linked_element_type VARCHAR(100) NOT NULL,
    link_type VARCHAR(50) NOT NULL,
    relationship_strength VARCHAR(20) DEFAULT 'medium',
    contribution_level VARCHAR(20) DEFAULT 'medium',
    
    -- Traceability
    created_by UUID NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (goal_id) REFERENCES goal(id)
);
```

## Service Architecture

### 1. API Layer (routes.py)
- **RESTful Endpoints**: Standard CRUD operations
- **Validation**: Pydantic-based request/response validation
- **Authentication**: JWT token validation
- **Authorization**: RBAC permission checking
- **Error Handling**: Consistent error responses

### 2. Business Logic Layer (services.py)
- **Domain Logic**: Goal lifecycle management
- **Event Emission**: Redis-based event publishing
- **Analysis**: Realization mapping and goal analysis
- **Queries**: Domain-specific query methods

### 3. Data Access Layer (models.py)
- **SQLAlchemy Models**: Database entity definitions
- **Relationships**: Foreign key relationships
- **Constraints**: Database-level constraints

### 4. Dependency Injection (deps.py)
- **Database Sessions**: SQLAlchemy session management
- **Authentication**: JWT token parsing
- **Authorization**: RBAC permission checking
- **Tenant Isolation**: Tenant context extraction

## Security Architecture

### Authentication
```python
def get_current_user(request: Request) -> UUID:
    """Extract user_id from JWT token"""
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ", 1)[1]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return UUID(payload.get("user_id"))
```

### Authorization
```python
def rbac_check(permission: str):
    """RBAC permission checker"""
    permissions = {
        "goal:create": ["Owner", "Admin", "Editor"],
        "goal:read": ["Owner", "Admin", "Editor", "Viewer"],
        "goal:update": ["Owner", "Admin", "Editor"],
        "goal:delete": ["Owner", "Admin"]
    }
```

### Multi-Tenant Security
- Tenant isolation at the database level
- Tenant-scoped queries
- Tenant-specific event emission

## Event Architecture

### Event Types
```python
# Goal lifecycle events
"goal.created"
"goal.updated"
"goal.deleted"

# Goal link events
"goal_link.created"
"goal_link.updated"
"goal_link.deleted"
```

### Event Payload
```json
{
    "event_type": "goal.created",
    "goal_id": "uuid",
    "tenant_id": "uuid",
    "user_id": "uuid",
    "timestamp": "2024-01-01T00:00:00Z",
    "details": {
        "name": "Digital Transformation Initiative",
        "goal_type": "strategic",
        "priority": "high",
        "status": "active"
    }
}
```

### Event Publishing
```python
def emit_event(event_type: str, goal_id: UUID, tenant_id: UUID, user_id: UUID, details: dict = None):
    event = {
        "event_type": event_type,
        "goal_id": str(goal_id),
        "tenant_id": str(tenant_id),
        "user_id": str(user_id),
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {}
    }
    redis_client.publish("goal_events", json.dumps(event))
```

## Observability Architecture

### Logging
```python
class JsonLogFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%fZ"),
            "service": "goal_service",
            "version": "1.0.0",
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log)
```

### Metrics
```python
REQUESTS_TOTAL = Counter(
    "goal_service_requests_total",
    "Total requests",
    ["method", "route", "status"]
)
REQUEST_LATENCY = Histogram(
    "goal_service_request_latency_seconds_bucket",
    "Request latency",
    ["method", "route"]
)
```

### Tracing
```python
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer("goal_service")
FastAPIInstrumentor.instrument_app(app)
```

## Integration Points

### 1. Event Bus Integration
- **Redis**: Primary event bus
- **Event Types**: Goal lifecycle events
- **Consumers**: Other microservices

### 2. Database Integration
- **PostgreSQL**: Primary data store
- **Alembic**: Migration management
- **Connection Pooling**: SQLAlchemy session management

### 3. Authentication Integration
- **JWT**: Token-based authentication
- **Shared Secret**: SECRET_KEY environment variable
- **Token Validation**: JWT decode and validation

### 4. Monitoring Integration
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **Alerting**: Prometheus alerting rules

## Deployment Architecture

### Containerization
```dockerfile
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
DATABASE_URL=postgresql://user:password@localhost:5432/goal_service
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
ENVIRONMENT=production
```

### Health Checks
```python
@app.get("/health")
async def health():
    return {
        "service": "goal_service",
        "version": "1.0.0",
        "status": "healthy",
        "uptime": f"{uptime:.2f}s",
        "database_connected": db_connected
    }
```

## Performance Considerations

### 1. Database Optimization
- **Indexes**: On frequently queried fields
- **Connection Pooling**: SQLAlchemy session management
- **Query Optimization**: Efficient domain queries

### 2. Caching Strategy
- **Redis**: Event caching and session storage
- **Application Cache**: In-memory caching for frequently accessed data

### 3. Scalability
- **Horizontal Scaling**: Stateless service design
- **Load Balancing**: Multiple service instances
- **Database Sharding**: Tenant-based sharding

## Security Considerations

### 1. Data Protection
- **Encryption**: Data encryption at rest and in transit
- **Access Control**: RBAC and tenant isolation
- **Audit Logging**: Comprehensive audit trails

### 2. Input Validation
- **Pydantic Validation**: Request/response validation
- **SQL Injection Prevention**: Parameterized queries
- **XSS Prevention**: Input sanitization

### 3. Authentication & Authorization
- **JWT Security**: Secure token handling
- **Role-Based Access**: Granular permissions
- **Tenant Isolation**: Multi-tenant security

## Monitoring & Alerting

### 1. Health Monitoring
- **Health Checks**: `/health` endpoint
- **Database Connectivity**: Connection monitoring
- **Service Status**: Overall service health

### 2. Performance Monitoring
- **Request Latency**: Response time tracking
- **Error Rates**: Error percentage monitoring
- **Throughput**: Requests per second

### 3. Business Metrics
- **Goal Creation Rate**: Goals created per day
- **Goal Achievement Rate**: Goals achieved per day
- **Link Creation Rate**: Goal links created per day

## Disaster Recovery

### 1. Data Backup
- **Database Backups**: Regular PostgreSQL backups
- **Event Logging**: Event persistence for replay
- **Configuration Backup**: Environment configuration

### 2. Service Recovery
- **Health Checks**: Automatic service restart
- **Circuit Breakers**: Failure isolation
- **Graceful Degradation**: Service degradation strategies

## Testing Strategy

### 1. Unit Testing
- **Service Logic**: Business logic testing
- **Model Validation**: Data model testing
- **Utility Functions**: Helper function testing

### 2. Integration Testing
- **API Testing**: Endpoint testing
- **Database Testing**: Data persistence testing
- **Event Testing**: Event emission testing

### 3. Performance Testing
- **Load Testing**: High-load scenarios
- **Stress Testing**: Resource exhaustion testing
- **Endurance Testing**: Long-running tests 