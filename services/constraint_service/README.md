# constraint_service

A microservice for managing ArchiMate 3.2 Constraint elements with comprehensive impact mapping, compliance tracking, RBAC, event emission, observability, and multi-tenancy.

## Business Purpose

The Constraint Service represents the ArchiMate 3.2 "Constraint" element within the Motivation Layer. Constraints capture restrictions, boundaries, and limitations that shape or restrict business goals, architectural design, and operational execution. This service provides comprehensive constraint management capabilities including:

- **Constraint Lifecycle Management**: Create, track, and manage constraints through their complete lifecycle
- **Impact Mapping**: Map how constraints affect other ArchiMate elements across all layers
- **Compliance Tracking**: Monitor regulatory and compliance constraints
- **Risk Assessment**: Analyze constraint severity, risk profiles, and mitigation strategies
- **Multi-tenant Support**: Isolated constraint management per tenant
- **Role-based Access Control**: Granular permissions for constraint management

## ArchiMate 3.2 Alignment

**Layer**: Motivation Layer
**Element**: Constraint
**Purpose**: Represents restrictions, boundaries, and limitations that shape enterprise strategy

### Key Relationships:
- **Constraint → Goal**: Constraints limit or shape goal achievement
- **Constraint → Requirement**: Constraints define requirement boundaries
- **Constraint → Capability**: Constraints restrict capability development
- **Constraint → Application Component**: Constraints limit application design
- **Constraint → Business Process**: Constraints govern process execution

## Features

- ✅ Full CRUD operations for Constraint elements
- ✅ Constraint linking to other ArchiMate elements
- ✅ Multi-tenant support with tenant isolation
- ✅ RBAC enforcement (Owner/Admin/Editor/Viewer)
- ✅ Event emission on create/update/delete operations
- ✅ Redis-based event-driven architecture
- ✅ Prometheus metrics and OpenTelemetry tracing
- ✅ JSON structured logging
- ✅ Health check and metrics endpoints
- ✅ Impact mapping and compliance analysis
- ✅ Domain-specific queries by type, scope, severity
- ✅ Comprehensive validation and error handling

## Endpoints

### Core CRUD Operations
- `POST /constraints` - Create a new constraint
- `GET /constraints` - List constraints with filtering and pagination
- `GET /constraints/{id}` - Get a specific constraint
- `PUT /constraints/{id}` - Update a constraint
- `DELETE /constraints/{id}` - Delete a constraint

### Constraint Links
- `POST /constraints/{id}/links` - Create a link to another element
- `GET /constraints/{id}/links` - List all links for a constraint
- `GET /links/{link_id}` - Get a specific link
- `PUT /links/{link_id}` - Update a link
- `DELETE /links/{link_id}` - Delete a link

### Analysis and Impact Mapping
- `GET /constraints/{id}/impact-map` - Get impact map for a constraint
- `GET /constraints/{id}/analysis` - Analyze constraint for strategic insights

### Domain-Specific Queries
- `GET /constraints/by-type/{type}` - Get constraints by type
- `GET /constraints/by-scope/{scope}` - Get constraints by scope
- `GET /constraints/by-severity/{severity}` - Get constraints by severity
- `GET /constraints/by-stakeholder/{stakeholder_id}` - Get constraints by stakeholder
- `GET /constraints/by-business-actor/{business_actor_id}` - Get constraints by business actor
- `GET /constraints/by-element/{element_type}/{element_id}` - Get constraints affecting an element
- `GET /constraints/compliance/required` - Get compliance-required constraints
- `GET /constraints/expiring/{days_ahead}` - Get expiring constraints

### Utility Endpoints
- `GET /constraints/types` - Get available constraint types
- `GET /constraints/scopes` - Get available scopes
- `GET /constraints/severities` - Get available severities
- `GET /constraints/enforcement-levels` - Get available enforcement levels
- `GET /constraints/risk-profiles` - Get available risk profiles
- `GET /constraints/mitigation-statuses` - Get available mitigation statuses
- `GET /constraints/mitigation-efforts` - Get available mitigation efforts
- `GET /constraints/impact-levels` - Get available impact levels
- `GET /constraints/review-frequencies` - Get available review frequencies
- `GET /constraints/link-types` - Get available link types
- `GET /constraints/compliance-statuses` - Get available compliance statuses

### System Endpoints
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /` - Service information

## API Reference

See [API_REFERENCE.md](./API_REFERENCE.md) for detailed API documentation.

## Architecture

### Domain Models
- **Constraint**: Core constraint entity with compliance and risk context
- **ConstraintLink**: Links constraints to other ArchiMate elements

### Key Features
- **Multi-tenant Architecture**: Complete tenant isolation
- **Event-Driven**: Redis-based event emission for integration
- **Observability**: Comprehensive logging, metrics, and tracing
- **Security**: JWT-based authentication and RBAC
- **Validation**: Pydantic-based request/response validation

## Deployment

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT secret key
- `ENVIRONMENT`: Deployment environment

### Docker
```bash
docker build -t constraint_service .
docker run -p 8080:8080 constraint_service
```

### Local Development
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## Testing

Run tests with coverage:
```bash
pytest --cov=app tests/
```

## Monitoring

The service provides comprehensive observability:
- **Health Checks**: `/health` endpoint
- **Metrics**: Prometheus-compatible metrics at `/metrics`
- **Logging**: Structured JSON logging
- **Tracing**: OpenTelemetry distributed tracing

## Integration

The service integrates with:
- **Event Bus**: Emits events for constraint lifecycle changes
- **Architecture Suite**: Links constraints to architecture packages
- **Monitoring Dashboard**: Health status and metrics aggregation
- **Audit Log**: Comprehensive audit trail 