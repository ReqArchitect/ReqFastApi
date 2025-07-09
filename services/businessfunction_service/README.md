# Business Function Service

A microservice for managing ArchiMate 3.2 Business Function elements within the ReqArchitect platform.

## Overview

The Business Function Service represents internal, recurring organizational behavior grouped by skill or competency. It provides comprehensive management of business functions with full lifecycle support, multi-tenancy, RBAC, and event-driven architecture.

## ArchiMate 3.2 Alignment

- **Layer**: Business Layer
- **Element**: Business Function
- **Relationships**: Links to Business Role, Business Process, Capability, Application Service, Data Object

## Key Features

### Core Functionality
- ✅ Complete CRUD operations for Business Functions
- ✅ Function linking to related ArchiMate elements
- ✅ Multi-tenant architecture with tenant isolation
- ✅ Role-based access control (Owner/Admin/Editor/Viewer)
- ✅ JWT-based authentication and authorization

### Domain Models
- **BusinessFunction**: Comprehensive model with 40+ attributes
- **FunctionLink**: Enables relationships to other ArchiMate elements
- **Competency Areas**: Architecture Governance, Compliance Management, Strategy Analysis, Vendor Evaluation, etc.

### Operational Features
- **Performance Metrics**: Alignment, efficiency, and effectiveness scores
- **Risk Management**: Risk levels, audit tracking, compliance requirements
- **Strategic Context**: Business value, strategic importance, cost centers
- **Operational Status**: Availability targets, operational hours, maturity levels

### Analysis & Impact
- **Impact Mapping**: Comprehensive dependency analysis
- **Health Scoring**: Multi-dimensional business function health assessment
- **Domain Queries**: Filtering by competency area, organizational unit, criticality, etc.

### Observability
- **Health Checks**: `/health` endpoint with database connectivity
- **Metrics**: Prometheus metrics for monitoring
- **Tracing**: OpenTelemetry distributed tracing
- **Logging**: Structured JSON logging with correlation IDs

### Event-Driven Architecture
- **Redis Integration**: Event emission for lifecycle changes
- **Event Types**: Created, updated, deleted events
- **Event Details**: Rich metadata for downstream processing

## API Endpoints

### Core CRUD Operations
```
POST   /business-functions/                    # Create business function
GET    /business-functions/                    # List with filtering
GET    /business-functions/{id}               # Get by ID
PUT    /business-functions/{id}               # Update
DELETE /business-functions/{id}               # Delete
```

### Function Links
```
POST   /business-functions/{id}/links         # Create link
GET    /business-functions/{id}/links         # List links
GET    /links/{link_id}                       # Get link
PUT    /links/{link_id}                       # Update link
DELETE /links/{link_id}                       # Delete link
```

### Analysis & Impact
```
GET    /business-functions/{id}/impact-map    # Impact analysis
GET    /business-functions/{id}/analysis      # Health analysis
```

### Domain Queries
```
GET    /business-functions/by-competency-area/{area}
GET    /business-functions/by-organizational-unit/{unit}
GET    /business-functions/by-criticality/{level}
GET    /business-functions/by-frequency/{frequency}
GET    /business-functions/by-role/{role_id}
GET    /business-functions/by-process/{process_id}
GET    /business-functions/by-capability/{capability_id}
GET    /business-functions/active
GET    /business-functions/critical
```

### Utility Endpoints
```
GET    /health                                # Health check
GET    /metrics                               # Prometheus metrics
GET    /competency-areas                      # Available areas
GET    /frequencies                           # Available frequencies
GET    /criticalities                         # Available criticalities
```

## Data Models

### BusinessFunction Attributes
- **Core**: name, description, competency_area, organizational_unit
- **Ownership**: owner_role_id, user_id, tenant_id
- **Input/Output**: input_object_type, output_object_type, input_description, output_description
- **Operational**: frequency, criticality, complexity, maturity_level
- **Performance**: alignment_score, efficiency_score, effectiveness_score, performance_metrics
- **Resources**: required_skills, required_capabilities, resource_requirements, technology_dependencies
- **Governance**: compliance_requirements, risk_level, audit_frequency, audit_status
- **Status**: status, operational_hours, availability_target, current_availability
- **Strategic**: strategic_importance, business_value, cost_center, budget_allocation
- **Relationships**: parent_function_id, supporting_capability_id, business_process_id

### FunctionLink Attributes
- **Core**: business_function_id, linked_element_id, linked_element_type, link_type
- **Relationship**: relationship_strength, dependency_level
- **Operational**: interaction_frequency, interaction_type, data_flow_direction
- **Traceability**: created_by, created_at

## Competency Areas

The service supports 15 predefined competency areas:
- Architecture Governance
- Compliance Management
- Strategy Analysis
- Vendor Evaluation
- Risk Management
- Performance Monitoring
- Quality Assurance
- Change Management
- Capacity Planning
- Cost Management
- Security Management
- Data Management
- Technology Evaluation
- Process Optimization
- Stakeholder Management

## Security & Access Control

### RBAC Permissions
- **Owner/Admin**: Full CRUD access
- **Editor**: Create, read, update access
- **Viewer**: Read-only access

### JWT Authentication
- Tenant-scoped operations
- User identification and authorization
- Role-based permission enforcement

## Event Emission

The service emits events to Redis for:
- Business function lifecycle changes (created, updated, deleted)
- Function link lifecycle changes (created, updated, deleted)

Event structure includes:
- Event type and timestamp
- Business function ID and tenant ID
- User ID and correlation ID
- Rich details for downstream processing

## Observability

### Health Checks
- Service status and uptime
- Database connectivity
- Error rates and request counts
- Environment information

### Metrics
- Request counts by method and route
- Request latency histograms
- Error counts and rates
- Custom business metrics

### Tracing
- Distributed tracing with OpenTelemetry
- Span attributes for tenant, user, and correlation IDs
- Automatic instrumentation of FastAPI endpoints

### Logging
- Structured JSON logging
- Correlation ID tracking
- Tenant and user context
- Performance metrics in logs

## Deployment

### Environment Variables
```
DATABASE_URL=postgresql://user:password@localhost:5432/businessfunction_service
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
ENVIRONMENT=development
```

### Docker
```bash
docker build -t business-function-service .
docker run -p 8080:8080 business-function-service
```

### Local Development
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

## Testing

### Unit Tests
```bash
pytest tests/ -v
```

### Integration Tests
```bash
pytest tests/test_integration.py -v
```

### Coverage
```bash
pytest --cov=app tests/
```

## Integration Points

### Upstream Services
- **Auth Service**: JWT token validation and user management
- **Tenant Service**: Multi-tenant isolation and management

### Downstream Services
- **Event Bus**: Redis event consumption
- **Monitoring**: Prometheus metrics collection
- **Tracing**: OpenTelemetry span collection

### Related ArchiMate Elements
- **Business Role**: Owner role relationships
- **Business Process**: Process function relationships
- **Capability**: Supporting capability relationships
- **Application Service**: Service function relationships
- **Data Object**: Input/output data relationships

## Business Value

### Enterprise Architecture
- Comprehensive business function modeling
- Cross-layer relationship management
- Strategic alignment assessment
- Operational performance tracking

### Compliance & Governance
- Audit trail and compliance tracking
- Risk assessment and management
- Policy enforcement and monitoring
- Regulatory requirement mapping

### Strategic Planning
- Business value assessment
- Strategic importance evaluation
- Resource allocation tracking
- Performance optimization insights

### Operational Excellence
- Availability and performance monitoring
- Capacity planning and optimization
- Cost management and budgeting
- Quality assurance and improvement

## Future Enhancements

### Planned Features
- Advanced analytics and reporting
- Workflow integration capabilities
- Machine learning insights
- Advanced visualization support

### Integration Opportunities
- Business process automation
- Resource planning systems
- Performance management tools
- Compliance monitoring platforms 