# Architecture: Course of Action Service

## Overview

The Course of Action Service is a microservice within the ReqArchitect platform that manages ArchiMate 3.2 "Course of Action" elements in the Strategy Layer. This document provides a comprehensive overview of the service architecture, design decisions, and implementation details.

## ArchiMate 3.2 Alignment

### Strategy Layer Element
The service implements the **Course of Action** element from the ArchiMate 3.2 Strategy Layer:

- **Definition**: Represents intended strategic approaches to achieve goals or realize capabilities
- **Purpose**: Define strategic initiatives that are influenced by Drivers and constrained by Constraints
- **Relationships**: Goal, Capability, Driver, Constraint, Assessment
- **Strategic Categories**: Transformational, Incremental, Defensive, Innovative

### Strategic Context
Courses of Action represent the bridge between strategic intent and tactical execution:
- **Strategic Planning**: Define clear objectives and success criteria
- **Risk Management**: Comprehensive risk assessment and mitigation
- **Performance Tracking**: Monitor progress and outcomes
- **Resource Management**: Cost tracking and budget allocation
- **Stakeholder Alignment**: Governance and approval processes

## System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    ReqArchitect Platform                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   API Gateway   │  │  Auth Service   │  │   Other     │ │
│  │                 │  │                 │  │  Services   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│              Course of Action Service                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   FastAPI App   │  │   PostgreSQL    │  │    Redis    │ │
│  │   - Routes      │  │   - Models      │  │   - Events  │ │
│  │   - Services    │  │   - Migrations  │  │   - Cache   │ │
│  │   - Validation  │  │   - Indexes     │  │             │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│              Observability Stack                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Prometheus    │  │  OpenTelemetry  │  │   Logging   │ │
│  │   - Metrics     │  │   - Tracing     │  │   - JSON    │ │
│  │   - Alerts      │  │   - Spans       │  │   - Levels  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Service Components

#### 1. API Layer (FastAPI)
- **Routes**: RESTful endpoints with dependency injection
- **Validation**: Pydantic schemas with comprehensive validation
- **Authentication**: JWT-based with RBAC enforcement
- **Documentation**: OpenAPI/Swagger auto-generation

#### 2. Business Logic Layer
- **Services**: Core business logic and operations
- **Event Emission**: Redis-based event-driven architecture
- **Analysis**: Strategic alignment and risk assessment
- **Domain Queries**: Specialized filtering and queries

#### 3. Data Layer
- **Models**: SQLAlchemy ORM with comprehensive relationships
- **Database**: PostgreSQL with optimized schema
- **Migrations**: Alembic for schema versioning
- **Indexes**: Performance optimization for queries

#### 4. Integration Layer
- **Event System**: Redis pub/sub for inter-service communication
- **External APIs**: Integration with other ReqArchitect services
- **Monitoring**: Prometheus metrics and health checks

## Data Model Design

### Core Entities

#### CourseOfAction
The primary entity representing strategic courses of action:

```sql
CREATE TABLE course_of_action (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    user_id UUID NOT NULL,
    
    -- Core fields
    name VARCHAR(255) NOT NULL,
    description TEXT,
    strategy_type VARCHAR(50) NOT NULL DEFAULT 'transformational',
    origin_goal_id UUID,
    influenced_by_driver_id UUID,
    impacted_capability_id UUID,
    
    -- Strategic context
    strategic_objective TEXT,
    business_case TEXT,
    success_criteria TEXT, -- JSON
    key_performance_indicators TEXT, -- JSON
    
    -- Time and planning
    time_horizon VARCHAR(50) DEFAULT 'medium_term',
    start_date TIMESTAMP,
    target_completion_date TIMESTAMP,
    actual_completion_date TIMESTAMP,
    implementation_phase VARCHAR(50) DEFAULT 'planning',
    
    -- Risk and probability
    success_probability DECIMAL(3,2) DEFAULT 0.5,
    risk_level VARCHAR(50) DEFAULT 'medium',
    risk_assessment TEXT, -- JSON
    contingency_plans TEXT, -- JSON
    
    -- Resource and cost
    estimated_cost DECIMAL(15,2),
    actual_cost DECIMAL(15,2),
    budget_allocation DECIMAL(15,2),
    resource_requirements TEXT, -- JSON
    cost_benefit_analysis TEXT, -- JSON
    
    -- Stakeholders and governance
    stakeholders TEXT, -- JSON
    governance_model VARCHAR(50) DEFAULT 'standard',
    approval_status VARCHAR(50) DEFAULT 'draft',
    approval_date TIMESTAMP,
    approved_by UUID,
    
    -- Implementation details
    implementation_approach TEXT,
    milestones TEXT, -- JSON
    dependencies TEXT, -- JSON
    constraints TEXT, -- JSON
    
    -- Performance and outcomes
    current_progress DECIMAL(5,2) DEFAULT 0.0,
    performance_metrics TEXT, -- JSON
    outcomes_achieved TEXT, -- JSON
    lessons_learned TEXT, -- JSON
    
    -- Strategic alignment
    strategic_alignment_score DECIMAL(3,2) DEFAULT 0.0,
    capability_impact_score DECIMAL(3,2) DEFAULT 0.0,
    goal_achievement_score DECIMAL(3,2) DEFAULT 0.0,
    overall_effectiveness_score DECIMAL(3,2) DEFAULT 0.0,
    
    -- Compliance and audit
    compliance_requirements TEXT, -- JSON
    audit_trail TEXT, -- JSON
    regulatory_impact TEXT, -- JSON
    
    -- Technology and systems
    technology_requirements TEXT, -- JSON
    system_impact TEXT, -- JSON
    integration_requirements TEXT, -- JSON
    
    -- Change management
    change_management_plan TEXT, -- JSON
    communication_plan TEXT, -- JSON
    training_requirements TEXT, -- JSON
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_strategy_type (strategy_type),
    INDEX idx_risk_level (risk_level),
    INDEX idx_implementation_phase (implementation_phase),
    INDEX idx_impacted_capability (impacted_capability_id)
);
```

#### ActionLink
Relationship management between courses of action and other elements:

```sql
CREATE TABLE action_link (
    id UUID PRIMARY KEY,
    course_of_action_id UUID NOT NULL,
    linked_element_id UUID NOT NULL,
    linked_element_type VARCHAR(100) NOT NULL,
    link_type VARCHAR(50) NOT NULL,
    
    -- Relationship context
    relationship_strength VARCHAR(50) DEFAULT 'medium',
    dependency_level VARCHAR(50) DEFAULT 'medium',
    strategic_importance VARCHAR(50) DEFAULT 'medium',
    business_value VARCHAR(50) DEFAULT 'medium',
    alignment_score DECIMAL(3,2),
    
    -- Implementation context
    implementation_priority VARCHAR(50) DEFAULT 'normal',
    implementation_phase VARCHAR(50) DEFAULT 'planning',
    resource_allocation DECIMAL(5,2),
    
    -- Impact assessment
    impact_level VARCHAR(50) DEFAULT 'medium',
    impact_direction VARCHAR(50) DEFAULT 'positive',
    impact_confidence DECIMAL(3,2),
    
    -- Risk and constraints
    risk_level VARCHAR(50) DEFAULT 'medium',
    constraint_level VARCHAR(50) DEFAULT 'medium',
    risk_mitigation TEXT, -- JSON
    
    -- Performance tracking
    performance_contribution DECIMAL(5,2),
    success_contribution DECIMAL(5,2),
    outcome_measurement TEXT, -- JSON
    
    -- Traceability
    created_by UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign keys
    FOREIGN KEY (course_of_action_id) REFERENCES course_of_action(id),
    
    -- Indexes
    INDEX idx_course_of_action_id (course_of_action_id),
    INDEX idx_linked_element (linked_element_id, linked_element_type),
    INDEX idx_link_type (link_type)
);
```

### Data Relationships

#### One-to-Many Relationships
- **CourseOfAction → ActionLink**: A course of action can have multiple links to other elements
- **Tenant → CourseOfAction**: Multi-tenant isolation
- **User → CourseOfAction**: User ownership and audit trail

#### Many-to-One Relationships
- **CourseOfAction → Goal**: Origin goal relationship
- **CourseOfAction → Driver**: Influencing driver relationship
- **CourseOfAction → Capability**: Impacted capability relationship

#### Cross-Service Relationships
- **CourseOfAction ↔ Goal Service**: Goal achievement tracking
- **CourseOfAction ↔ Capability Service**: Capability impact assessment
- **CourseOfAction ↔ Driver Service**: Driver influence analysis

## API Design

### RESTful Endpoints

#### Course of Action Management
```
POST   /api/v1/courses-of-action          # Create
GET    /api/v1/courses-of-action          # List with filtering
GET    /api/v1/courses-of-action/{id}     # Get by ID
PUT    /api/v1/courses-of-action/{id}     # Update
DELETE /api/v1/courses-of-action/{id}     # Delete
```

#### Action Link Management
```
POST   /api/v1/courses-of-action/{id}/links           # Create link
GET    /api/v1/courses-of-action/{id}/links           # List links
GET    /api/v1/courses-of-action/links/{link_id}     # Get link
PUT    /api/v1/courses-of-action/links/{link_id}     # Update link
DELETE /api/v1/courses-of-action/links/{link_id}     # Delete link
```

#### Analysis & Alignment
```
GET /api/v1/courses-of-action/{id}/alignment-map     # Strategic alignment
GET /api/v1/courses-of-action/{id}/risk-profile      # Risk assessment
GET /api/v1/courses-of-action/{id}/analysis          # Comprehensive analysis
```

#### Domain-Specific Queries
```
GET /api/v1/courses-of-action/by-type/{strategy_type}     # By strategy type
GET /api/v1/courses-of-action/by-capability/{capability_id} # By capability
GET /api/v1/courses-of-action/by-risk-level/{risk_level}   # By risk level
GET /api/v1/courses-of-action/by-time-horizon/{time_horizon} # By time horizon
GET /api/v1/courses-of-action/by-element/{element_type}/{element_id} # By element
GET /api/v1/courses-of-action/active                    # Active courses
GET /api/v1/courses-of-action/critical                  # Critical courses
```

#### Enumeration Endpoints
```
GET /api/v1/courses-of-action/strategy-types          # Strategy types
GET /api/v1/courses-of-action/time-horizons           # Time horizons
GET /api/v1/courses-of-action/implementation-phases   # Implementation phases
GET /api/v1/courses-of-action/risk-levels             # Risk levels
GET /api/v1/courses-of-action/approval-statuses       # Approval statuses
GET /api/v1/courses-of-action/governance-models       # Governance models
GET /api/v1/courses-of-action/link-types              # Link types
GET /api/v1/courses-of-action/relationship-strengths  # Relationship strengths
GET /api/v1/courses-of-action/dependency-levels       # Dependency levels
GET /api/v1/courses-of-action/strategic-importances   # Strategic importances
GET /api/v1/courses-of-action/business-values         # Business values
GET /api/v1/courses-of-action/implementation-priorities # Implementation priorities
GET /api/v1/courses-of-action/impact-levels           # Impact levels
GET /api/v1/courses-of-action/impact-directions       # Impact directions
GET /api/v1/courses-of-action/constraint-levels       # Constraint levels
```

### Request/Response Patterns

#### Standard Response Format
```json
{
  "id": "uuid",
  "tenant_id": "uuid",
  "user_id": "uuid",
  "name": "string",
  "description": "string",
  "strategy_type": "enum",
  "time_horizon": "enum",
  "implementation_phase": "enum",
  "success_probability": "decimal",
  "risk_level": "enum",
  "current_progress": "decimal",
  "strategic_alignment_score": "decimal",
  "capability_impact_score": "decimal",
  "goal_achievement_score": "decimal",
  "overall_effectiveness_score": "decimal",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

#### Error Response Format
```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "timestamp"
}
```

## Security Architecture

### Authentication
- **JWT-based**: Stateless authentication with signed tokens
- **Claims**: tenant_id, user_id, role, permissions
- **Expiration**: Configurable token lifetime
- **Refresh**: Token refresh mechanism for long-lived sessions

### Authorization (RBAC)
- **Roles**: Owner, Admin, Editor, Viewer
- **Permissions**: Granular permissions per operation
- **Tenant Isolation**: All operations scoped to tenant
- **Resource-level**: Individual resource access control

### Permission Matrix
```
Operation                    Owner  Admin  Editor  Viewer
course_of_action:create     ✓      ✓      ✓      ✗
course_of_action:read       ✓      ✓      ✓      ✓
course_of_action:update     ✓      ✓      ✓      ✗
course_of_action:delete     ✓      ✓      ✗      ✗
action_link:create          ✓      ✓      ✓      ✗
action_link:read            ✓      ✓      ✓      ✓
action_link:update          ✓      ✓      ✓      ✗
action_link:delete          ✓      ✓      ✗      ✗
alignment:read              ✓      ✓      ✓      ✓
analysis:read               ✓      ✓      ✓      ✓
risk:read                   ✓      ✓      ✓      ✓
```

### Data Protection
- **Encryption**: Data at rest and in transit
- **Audit Trail**: Complete audit logging
- **Data Retention**: Configurable retention policies
- **GDPR Compliance**: Data subject rights support

## Event-Driven Architecture

### Event Types
- **Lifecycle Events**: Created, updated, deleted
- **State Changes**: Status transitions, phase changes
- **Business Events**: Approvals, milestones, completions
- **Integration Events**: Cross-service notifications

### Event Format
```json
{
  "event_type": "course_of_action_created",
  "service": "courseofaction_service",
  "version": "1.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "course_of_action_id": "uuid",
    "tenant_id": "uuid",
    "user_id": "uuid",
    "strategy_type": "transformational",
    "risk_level": "medium"
  },
  "metadata": {
    "correlation_id": "uuid",
    "user_agent": "string",
    "ip_address": "string"
  }
}
```

### Event Consumers
- **Analytics Service**: Business intelligence and reporting
- **Notification Service**: User notifications and alerts
- **Audit Service**: Compliance and audit logging
- **Integration Services**: Cross-service synchronization

## Observability

### Metrics (Prometheus)
- **HTTP Metrics**: Request count, latency, status codes
- **Business Metrics**: Courses of action by status, risk level, strategy type
- **Performance Metrics**: Database query times, cache hit rates
- **Custom Metrics**: Alignment scores, risk profiles, progress tracking

### Tracing (OpenTelemetry)
- **Distributed Tracing**: End-to-end request tracing
- **Span Attributes**: Service name, operation, duration
- **Correlation IDs**: Request correlation across services
- **Performance Analysis**: Bottleneck identification

### Logging
- **Structured Logging**: JSON format with consistent fields
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Context Enrichment**: Tenant, user, request ID
- **Log Aggregation**: Centralized log collection and analysis

### Health Checks
- **Liveness**: Service is running and responding
- **Readiness**: Service is ready to handle requests
- **Dependencies**: Database, Redis, external services
- **Custom Checks**: Business logic validation

## Performance Considerations

### Database Optimization
- **Indexes**: Strategic indexes for common queries
- **Query Optimization**: Efficient SQL with proper joins
- **Connection Pooling**: Optimized database connections
- **Caching**: Redis-based caching for frequently accessed data

### API Performance
- **Pagination**: Efficient pagination with cursor-based approach
- **Filtering**: Optimized filtering with database-level filtering
- **Response Caching**: Cache frequently requested responses
- **Compression**: GZIP compression for large responses

### Scalability
- **Horizontal Scaling**: Stateless design for easy scaling
- **Load Balancing**: Multiple instances behind load balancer
- **Database Sharding**: Tenant-based sharding strategy
- **Caching Strategy**: Multi-level caching approach

## Deployment Architecture

### Container Strategy
- **Docker**: Containerized application with multi-stage builds
- **Base Image**: Python 3.11 slim image
- **Security**: Non-root user, minimal attack surface
- **Size Optimization**: Multi-stage builds for smaller images

### Kubernetes Deployment
- **Deployment**: Rolling updates with health checks
- **Service**: Load balancer with service discovery
- **ConfigMaps**: Environment-specific configuration
- **Secrets**: Secure credential management
- **HPA**: Horizontal Pod Autoscaler for dynamic scaling

### Environment Strategy
- **Development**: Local development with hot reload
- **Staging**: Production-like environment for testing
- **Production**: High availability with redundancy
- **DR**: Disaster recovery with backup and restore

## Monitoring and Alerting

### Key Metrics
- **Availability**: 99.9% uptime target
- **Latency**: P95 < 200ms for API responses
- **Throughput**: 1000+ requests per second
- **Error Rate**: < 1% error rate

### Alerting Rules
- **High Error Rate**: > 5% error rate for 5 minutes
- **High Latency**: P95 > 500ms for 5 minutes
- **Service Down**: Health check failures
- **Database Issues**: Connection failures or slow queries

### Dashboards
- **Service Overview**: Key metrics and health status
- **Business Metrics**: Courses of action by status and type
- **Performance**: Response times and throughput
- **Errors**: Error rates and types

## Testing Strategy

### Test Types
- **Unit Tests**: Individual function and class testing
- **Integration Tests**: API endpoint and database testing
- **Contract Tests**: Service interface compatibility
- **Performance Tests**: Load and stress testing
- **Security Tests**: Authentication and authorization testing

### Test Coverage
- **Code Coverage**: > 90% line coverage target
- **API Coverage**: All endpoints tested
- **Business Logic**: All critical paths tested
- **Error Scenarios**: Edge cases and error handling

### Test Data
- **Fixtures**: Reusable test data sets
- **Factories**: Dynamic test data generation
- **Isolation**: Test data isolation per test
- **Cleanup**: Automatic test data cleanup

## Configuration Management

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/db

# Security
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Redis
REDIS_URL=redis://host:6379

# Observability
OTEL_ENABLED=true
OTEL_ENDPOINT=http://localhost:4317
PROMETHEUS_PORT=9090

# Service
PORT=8080
HOST=0.0.0.0
LOG_LEVEL=INFO
```

### Configuration Validation
- **Schema Validation**: Pydantic-based configuration validation
- **Required Fields**: Validation of required configuration
- **Type Checking**: Type validation for configuration values
- **Default Values**: Sensible defaults for optional settings

## Future Enhancements

### Planned Features
- **Advanced Analytics**: Machine learning-based insights
- **Workflow Integration**: Integration with workflow engines
- **Real-time Collaboration**: Multi-user editing and collaboration
- **Advanced Reporting**: Custom report generation
- **Mobile Support**: Mobile-optimized API endpoints

### Technical Improvements
- **GraphQL API**: Alternative to REST for complex queries
- **Event Sourcing**: Complete audit trail with event sourcing
- **CQRS**: Command Query Responsibility Segregation
- **Micro-frontends**: Frontend integration capabilities
- **API Versioning**: Semantic versioning for API evolution

## Conclusion

The Course of Action Service provides a robust, scalable, and secure foundation for managing strategic courses of action within the ReqArchitect platform. The architecture follows industry best practices for microservices, ensuring maintainability, observability, and performance while aligning with ArchiMate 3.2 standards for enterprise architecture modeling. 