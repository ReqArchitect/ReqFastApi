# Architecture: Resource Service

## Overview

The Resource Service is a microservice in the ReqArchitect platform that manages ArchiMate 3.2 Resource elements in the Strategy Layer. It provides comprehensive resource management capabilities for organizational resources including human, financial, system, and informational resources that enable strategic capabilities and business functions.

## ArchiMate 3.2 Alignment

### Strategy Layer - Resource Element

The Resource Service represents the **Resource** element in the **Strategy Layer** of ArchiMate 3.2:

- **Layer**: Strategy Layer
- **Element Type**: Resource
- **Purpose**: Model organizational resources that enable strategic capabilities and business functions
- **Relationships**: Links to Goals, Constraints, Business Functions, Application Components, Nodes

### Resource Types

The service supports four main resource types:

1. **Human Resources** (`human`): People, skills, expertise
   - Example: "Enterprise Architect", "Business Analyst", "Project Manager"
   - Attributes: skills_required, expertise_level, capabilities_provided

2. **System Resources** (`system`): Technology systems and platforms
   - Example: "Legacy CRM System", "Cloud Compute Unit", "Database Cluster"
   - Attributes: technology_stack, system_requirements, integration_points

3. **Financial Resources** (`financial`): Budget allocations and funding
   - Example: "Budget Unit", "Capital Allocation", "Operating Budget"
   - Attributes: cost_per_unit, total_cost, budget_allocation, cost_center

4. **Knowledge Resources** (`knowledge`): Information repositories and data assets
   - Example: "Customer Insights Repository", "Technical Documentation", "Best Practices Library"
   - Attributes: capabilities_provided, dependencies, audit_requirements

## System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client Apps   │    │   API Gateway   │    │  Resource       │
│                 │◄──►│                 │◄──►│  Service        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Event Bus     │◄──►│     Redis       │◄──►│   PostgreSQL    │
│   (Redis)       │    │   (Events)      │    │   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Component Architecture

```
Resource Service
├── API Layer (FastAPI)
│   ├── Authentication & Authorization
│   ├── Request/Response Handling
│   ├── Validation & Serialization
│   └── Error Handling
├── Business Logic Layer
│   ├── Resource Management
│   ├── Link Management
│   ├── Analysis & Impact Assessment
│   └── Domain-Specific Queries
├── Data Access Layer
│   ├── SQLAlchemy ORM
│   ├── Database Models
│   └── Repository Pattern
├── Event Layer
│   ├── Redis Event Emission
│   └── Event-Driven Integration
└── Observability Layer
    ├── Health Checks
    ├── Prometheus Metrics
    ├── OpenTelemetry Tracing
    └── Structured Logging
```

## Data Model

### Core Entities

#### Resource Entity

```sql
CREATE TABLE resource (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    user_id UUID NOT NULL,
    
    -- Core resource fields
    name VARCHAR(255) NOT NULL,
    description TEXT,
    resource_type VARCHAR(50) NOT NULL DEFAULT 'human',
    quantity FLOAT DEFAULT 1.0,
    unit_of_measure VARCHAR(50) DEFAULT 'unit',
    
    -- Availability and allocation
    availability FLOAT DEFAULT 100.0,
    allocated_quantity FLOAT DEFAULT 0.0,
    available_quantity FLOAT DEFAULT 1.0,
    
    -- Location and deployment
    location VARCHAR(255),
    deployment_status VARCHAR(50) DEFAULT 'active',
    
    -- Criticality and importance
    criticality VARCHAR(50) DEFAULT 'medium',
    strategic_importance VARCHAR(50) DEFAULT 'medium',
    business_value VARCHAR(50) DEFAULT 'medium',
    
    -- Cost and financial aspects
    cost_per_unit FLOAT,
    total_cost FLOAT,
    budget_allocation FLOAT,
    cost_center VARCHAR(100),
    
    -- Skills and capabilities
    skills_required TEXT,
    capabilities_provided TEXT,
    expertise_level VARCHAR(50) DEFAULT 'intermediate',
    
    -- Performance and metrics
    performance_metrics TEXT,
    utilization_rate FLOAT DEFAULT 0.0,
    efficiency_score FLOAT DEFAULT 0.0,
    effectiveness_score FLOAT DEFAULT 0.0,
    
    -- Operational characteristics
    operational_hours VARCHAR(50) DEFAULT 'business_hours',
    maintenance_schedule VARCHAR(255),
    last_maintenance TIMESTAMP,
    next_maintenance TIMESTAMP,
    
    -- Technology and system aspects
    technology_stack TEXT,
    system_requirements TEXT,
    integration_points TEXT,
    dependencies TEXT,
    
    -- Governance and compliance
    governance_model VARCHAR(50) DEFAULT 'standard',
    compliance_requirements TEXT,
    audit_requirements TEXT,
    risk_assessment TEXT,
    
    -- Relationships and associations
    associated_capability_id UUID,
    parent_resource_id UUID,
    business_function_id UUID,
    application_component_id UUID,
    node_id UUID,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### ResourceLink Entity

```sql
CREATE TABLE resource_link (
    id UUID PRIMARY KEY,
    resource_id UUID NOT NULL,
    linked_element_id UUID NOT NULL,
    linked_element_type VARCHAR(100) NOT NULL,
    link_type VARCHAR(50) NOT NULL,
    relationship_strength VARCHAR(50) DEFAULT 'medium',
    dependency_level VARCHAR(50) DEFAULT 'medium',
    
    -- Allocation context
    allocation_percentage FLOAT DEFAULT 0.0,
    allocation_start_date TIMESTAMP,
    allocation_end_date TIMESTAMP,
    allocation_priority VARCHAR(50) DEFAULT 'normal',
    
    -- Operational context
    interaction_frequency VARCHAR(50) DEFAULT 'regular',
    interaction_type VARCHAR(50) DEFAULT 'synchronous',
    data_flow_direction VARCHAR(50) DEFAULT 'bidirectional',
    
    -- Performance impact
    performance_impact VARCHAR(50) DEFAULT 'low',
    efficiency_contribution FLOAT,
    effectiveness_contribution FLOAT,
    
    -- Traceability
    created_by UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Relationships

#### Resource Relationships

- **Parent-Child**: Resources can have parent-child relationships (hierarchical)
- **Capability Association**: Resources can be associated with capabilities
- **Business Function Association**: Resources can be associated with business functions
- **Application Component Association**: Resources can be associated with application components
- **Node Association**: Resources can be associated with nodes

#### ResourceLink Relationships

- **Goal Links**: Resources can link to strategic goals
- **Constraint Links**: Resources can link to business constraints
- **Business Function Links**: Resources can link to business functions
- **Application Component Links**: Resources can link to application components
- **Node Links**: Resources can link to technology nodes

## Security Architecture

### Authentication

- **JWT-based Authentication**: All API endpoints require valid JWT tokens
- **Token Claims**: tenant_id, user_id, role
- **Token Validation**: Signature verification, expiration checking

### Authorization

#### Role-Based Access Control (RBAC)

| Permission | Owner | Admin | Editor | Viewer |
|------------|-------|-------|--------|--------|
| resource:create | ✅ | ✅ | ✅ | ❌ |
| resource:read | ✅ | ✅ | ✅ | ✅ |
| resource:update | ✅ | ✅ | ✅ | ❌ |
| resource:delete | ✅ | ✅ | ❌ | ❌ |
| resource_link:create | ✅ | ✅ | ✅ | ❌ |
| resource_link:read | ✅ | ✅ | ✅ | ✅ |
| resource_link:update | ✅ | ✅ | ✅ | ❌ |
| resource_link:delete | ✅ | ✅ | ❌ | ❌ |
| impact:read | ✅ | ✅ | ✅ | ✅ |
| analysis:read | ✅ | ✅ | ✅ | ✅ |
| allocation:read | ✅ | ✅ | ✅ | ✅ |

### Multi-Tenancy

- **Tenant Isolation**: All data is scoped by tenant_id
- **Cross-Tenant Protection**: No data leakage between tenants
- **Tenant Validation**: JWT token tenant_id must match resource tenant_id

### Data Validation

- **Input Validation**: Pydantic models for request validation
- **Enum Validation**: Resource types, statuses, criticality levels
- **Range Validation**: Quantities, percentages, scores
- **Business Rules**: Allocation percentages, availability ranges

## Event-Driven Architecture

### Event Types

#### Resource Events

- `resource.created`: Resource creation events
- `resource.updated`: Resource update events
- `resource.deleted`: Resource deletion events

#### ResourceLink Events

- `resource_link.created`: Resource link creation events
- `resource_link.updated`: Resource link update events
- `resource_link.deleted`: Resource link deletion events

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

### Event Consumers

- **Analytics Service**: Resource utilization analytics
- **Notification Service**: Resource change notifications
- **Audit Service**: Resource change audit trails
- **Integration Services**: External system synchronization

## Observability

### Health Checks

- **Database Connectivity**: PostgreSQL connection health
- **Redis Connectivity**: Event emission capability
- **Service Responsiveness**: API endpoint availability
- **Memory Usage**: Resource consumption monitoring

### Metrics

#### Prometheus Metrics

- `resource_service_requests_total`: Request count by method, endpoint, status
- `resource_service_request_duration_seconds`: Request latency
- `resource_creation_rate`: Resource creation rate
- `resource_update_rate`: Resource update rate
- `resource_deletion_rate`: Resource deletion rate
- `resource_link_creation_rate`: Link creation rate

#### Business Metrics

- **Resource Utilization**: Average utilization across resources
- **Resource Allocation**: Allocation percentage distribution
- **Resource Performance**: Efficiency and effectiveness scores
- **Resource Costs**: Total cost and budget allocation tracking

### Tracing

#### OpenTelemetry Integration

- **FastAPI Instrumentation**: Automatic request tracing
- **SQLAlchemy Instrumentation**: Database query tracing
- **Custom Spans**: Business logic operation tracing
- **Trace Propagation**: Distributed tracing across services

### Logging

#### Structured Logging

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "resource_service",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "operation": "create_resource",
  "resource_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Resource created successfully"
}
```

## Performance Considerations

### Database Optimization

- **Indexing**: Primary keys, foreign keys, frequently queried fields
- **Query Optimization**: Efficient joins and filtering
- **Connection Pooling**: SQLAlchemy connection pool configuration
- **Read Replicas**: For read-heavy workloads

### Caching Strategy

- **Redis Caching**: Frequently accessed resource data
- **Cache Invalidation**: Event-driven cache invalidation
- **Cache TTL**: Appropriate time-to-live settings

### API Performance

- **Pagination**: Efficient pagination for large datasets
- **Filtering**: Optimized database queries with filters
- **Response Compression**: Gzip compression for large responses
- **Rate Limiting**: Protection against abuse

## Scalability

### Horizontal Scaling

- **Stateless Design**: No session state, any instance can handle requests
- **Load Balancing**: Multiple service instances behind load balancer
- **Database Scaling**: Read replicas, connection pooling
- **Event Scaling**: Redis cluster for high-throughput events

### Vertical Scaling

- **Resource Allocation**: CPU and memory allocation
- **Database Resources**: PostgreSQL resource allocation
- **Redis Resources**: Memory and connection limits

## Deployment Architecture

### Container Deployment

```yaml
# Docker Compose
version: '3.8'
services:
  resource-service:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/resource_service
      - REDIS_HOST=redis
      - SECRET_KEY=your-secret-key
    depends_on:
      - postgres
      - redis
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
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
```

## Integration Patterns

### Service-to-Service Communication

- **Synchronous**: REST API calls for immediate responses
- **Asynchronous**: Event-driven communication via Redis
- **Circuit Breaker**: Protection against cascading failures
- **Retry Logic**: Exponential backoff for transient failures

### External System Integration

- **API Gateway**: Centralized routing and authentication
- **Service Mesh**: Advanced traffic management and observability
- **Event Bus**: Decoupled service communication
- **Message Queues**: Reliable message delivery

## Monitoring and Alerting

### Key Metrics

- **Request Rate**: Requests per second
- **Response Time**: P95, P99 latency
- **Error Rate**: 4xx and 5xx error percentages
- **Resource Utilization**: CPU, memory, disk usage
- **Database Performance**: Query latency, connection pool usage
- **Event Processing**: Redis event emission success rate

### Alerting Rules

- **High Error Rate**: > 5% error rate for 5 minutes
- **High Latency**: > 2s response time for 5 minutes
- **Service Down**: Health check failures
- **Database Issues**: Connection failures or high query latency
- **Event Processing**: Failed event emissions

## Disaster Recovery

### Backup Strategy

- **Database Backups**: Daily automated PostgreSQL backups
- **Configuration Backups**: Infrastructure as Code backups
- **Event Logging**: Event persistence for replay capability

### Recovery Procedures

- **Service Recovery**: Automated service restart
- **Database Recovery**: Point-in-time recovery
- **Data Consistency**: Event replay for data consistency
- **Rollback Procedures**: Previous version deployment

## Security Considerations

### Data Protection

- **Encryption at Rest**: Database encryption
- **Encryption in Transit**: TLS for all communications
- **Sensitive Data**: PII and sensitive information handling
- **Audit Logging**: Comprehensive audit trails

### Network Security

- **Network Policies**: Kubernetes network policies
- **Firewall Rules**: Ingress/egress traffic control
- **VPN Access**: Secure remote access
- **DDoS Protection**: Rate limiting and traffic filtering

## Compliance

### Data Governance

- **Data Retention**: Configurable retention policies
- **Data Classification**: Resource data classification
- **Access Logging**: Comprehensive access audit trails
- **Privacy Controls**: GDPR and privacy compliance

### Regulatory Compliance

- **SOX Compliance**: Financial resource tracking
- **GDPR Compliance**: Personal data protection
- **Industry Standards**: ISO 27001, SOC 2 compliance
- **Audit Requirements**: Comprehensive audit capabilities

## Future Enhancements

### Planned Features

- **Advanced Analytics**: Machine learning for resource optimization
- **Predictive Modeling**: Resource demand forecasting
- **Cost Optimization**: Automated cost optimization recommendations
- **Integration APIs**: Enhanced external system integration
- **Mobile Support**: Mobile-optimized interfaces
- **Real-time Dashboards**: Live resource monitoring dashboards

### Technology Evolution

- **GraphQL Support**: Flexible query capabilities
- **gRPC Integration**: High-performance service communication
- **Event Sourcing**: Complete event history for resources
- **CQRS Pattern**: Command-Query Responsibility Segregation
- **Microservices Evolution**: Further service decomposition 