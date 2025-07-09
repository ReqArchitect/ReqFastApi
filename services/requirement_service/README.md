# requirement_service

A microservice for managing ArchiMate 3.2 Requirement elements with full lifecycle support, traceability, RBAC, event emission, observability, and multi-tenancy.

## Business Purpose

The Requirement Service represents the ArchiMate 3.2 "Requirement" element within the Motivation Layer. Requirements define what an enterprise wants to achieve and serve as the foundation for architecture design decisions. This service provides comprehensive requirement management capabilities including:

- **Requirement Lifecycle Management**: Create, track, and manage requirements through their complete lifecycle
- **Traceability**: Link requirements to other ArchiMate elements across all layers
- **Compliance Tracking**: Monitor requirement compliance and validation status
- **Impact Analysis**: Assess the impact of requirements on architecture elements
- **Multi-tenant Support**: Isolated requirement management per tenant
- **Role-based Access Control**: Granular permissions for requirement management

## ArchiMate 3.2 Alignment

**Layer**: Motivation Layer
**Element**: Requirement
**Purpose**: Represents a statement of need that must be realized by the architecture

### Key Relationships:
- **Requirement → Capability**: Requirements drive capability development
- **Requirement → Business Process**: Requirements influence business process design
- **Requirement → Application Function**: Requirements guide application functionality
- **Requirement → Technology**: Requirements inform technology decisions

## Features

- ✅ Full CRUD operations for Requirement elements
- ✅ Requirement linking to other ArchiMate elements
- ✅ Multi-tenant support with tenant isolation
- ✅ RBAC enforcement (Owner/Admin/Editor/Viewer)
- ✅ Event emission on create/update/delete operations
- ✅ Redis-based event-driven architecture
- ✅ Prometheus metrics and OpenTelemetry tracing
- ✅ JSON structured logging
- ✅ Health check and metrics endpoints
- ✅ Traceability and impact analysis
- ✅ Comprehensive validation and error handling

## Endpoints

### Core CRUD Operations
- `POST /requirements` - Create a new requirement
- `GET /requirements` - List requirements with filtering and pagination
- `GET /requirements/{id}` - Get a specific requirement
- `PUT /requirements/{id}` - Update a requirement
- `DELETE /requirements/{id}` - Delete a requirement

### Requirement Links
- `POST /requirements/{id}/links` - Create a link to another element
- `GET /requirements/{id}/links` - List all links for a requirement
- `GET /links/{link_id}` - Get a specific link
- `PUT /links/{link_id}` - Update a link
- `DELETE /links/{link_id}` - Delete a link

### Analysis and Traceability
- `GET /requirements/{id}/traceability-check` - Check traceability status
- `GET /requirements/{id}/impact-summary` - Get impact analysis

### Utility Endpoints
- `GET /requirements/types` - Get available requirement types
- `GET /requirements/priorities` - Get available priorities
- `GET /requirements/statuses` - Get available statuses
- `GET /requirements/link-types` - Get available link types
- `GET /requirements/link-strengths` - Get available link strengths

### System Endpoints
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /` - Service information

## API Reference

See [API_REFERENCE.md](./API_REFERENCE.md) for detailed API documentation.

## Architecture

### Domain Models
- **Requirement**: Core requirement entity with lifecycle management
- **RequirementLink**: Links requirements to other ArchiMate elements

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
docker build -t requirement_service .
docker run -p 8080:8080 requirement_service
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
- **Event Bus**: Emits events for requirement lifecycle changes
- **Architecture Suite**: Links requirements to architecture packages
- **Monitoring Dashboard**: Health status and metrics aggregation
- **Audit Log**: Comprehensive audit trail 