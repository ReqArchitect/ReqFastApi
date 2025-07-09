# goal_service

A microservice for managing ArchiMate 3.2 Goal elements with comprehensive realization mapping, progress tracking, RBAC, event emission, observability, and multi-tenancy.

## Business Purpose

The Goal Service represents the ArchiMate 3.2 "Goal" element within the Motivation Layer. Goals capture desired outcomes or strategic targets that guide enterprise architecture and business strategy. This service provides comprehensive goal management capabilities including:

- **Goal Lifecycle Management**: Create, track, and manage goals through their complete lifecycle
- **Realization Mapping**: Map how goals are realized through Requirements, Capabilities, and Courses of Action
- **Progress Tracking**: Monitor goal progress, milestones, and success criteria
- **Strategic Alignment**: Assess goal alignment with business strategy and drivers
- **Multi-tenant Support**: Isolated goal management per tenant
- **Role-based Access Control**: Granular permissions for goal management

## ArchiMate 3.2 Alignment

**Layer**: Motivation Layer
**Element**: Goal
**Purpose**: Represents desired outcomes or strategic targets that guide enterprise architecture

### Key Relationships:
- **Goal ← Driver**: Goals are motivated by drivers
- **Goal → Requirement**: Goals are realized through requirements
- **Goal → Capability**: Goals are enabled by capabilities
- **Goal → Course of Action**: Goals are achieved through courses of action
- **Goal → Stakeholder**: Goals are owned by stakeholders
- **Goal → Assessment**: Goals are evaluated through assessments

## Features

- ✅ Full CRUD operations for Goal elements
- ✅ Goal linking to other ArchiMate elements
- ✅ Multi-tenant support with tenant isolation
- ✅ RBAC enforcement (Owner/Admin/Editor/Viewer)
- ✅ Event emission on create/update/delete operations
- ✅ Redis-based event-driven architecture
- ✅ Prometheus metrics and OpenTelemetry tracing
- ✅ JSON structured logging
- ✅ Health check and metrics endpoints
- ✅ Realization mapping and progress analysis
- ✅ Domain-specific queries by type, priority, status
- ✅ Comprehensive validation and error handling

## Endpoints

### Core CRUD Operations
- `POST /goals` - Create a new goal
- `GET /goals` - List goals with filtering and pagination
- `GET /goals/{id}` - Get a specific goal
- `PUT /goals/{id}` - Update a goal
- `DELETE /goals/{id}` - Delete a goal

### Goal Links
- `POST /goals/{id}/links` - Create a link to another element
- `GET /goals/{id}/links` - List all links for a goal
- `GET /links/{link_id}` - Get a specific link
- `PUT /links/{link_id}` - Update a link
- `DELETE /links/{link_id}` - Delete a link

### Analysis and Realization Mapping
- `GET /goals/{id}/realization-map` - Get realization map for a goal
- `GET /goals/{id}/status-summary` - Get status summary for a goal
- `GET /goals/{id}/analysis` - Analyze goal for strategic insights

### Domain-Specific Queries
- `GET /goals/by-type/{type}` - Get goals by type
- `GET /goals/by-priority/{priority}` - Get goals by priority
- `GET /goals/by-status/{status}` - Get goals by status
- `GET /goals/by-stakeholder/{stakeholder_id}` - Get goals by stakeholder
- `GET /goals/by-business-actor/{business_actor_id}` - Get goals by business actor
- `GET /goals/by-driver/{driver_id}` - Get goals by driver
- `GET /goals/by-element/{element_type}/{element_id}` - Get goals linked to an element
- `GET /goals/active` - Get active goals
- `GET /goals/achieved` - Get achieved goals
- `GET /goals/due-soon/{days_ahead}` - Get goals due soon
- `GET /goals/high-priority` - Get high priority goals
- `GET /goals/by-progress/{min_progress}/{max_progress}` - Get goals by progress range

### Utility Endpoints
- `GET /goals/types` - Get available goal types
- `GET /goals/priorities` - Get available priorities
- `GET /goals/statuses` - Get available statuses
- `GET /goals/measurement-frequencies` - Get available measurement frequencies
- `GET /goals/review-frequencies` - Get available review frequencies
- `GET /goals/strategic-alignments` - Get available strategic alignments
- `GET /goals/business-values` - Get available business values
- `GET /goals/risk-levels` - Get available risk levels
- `GET /goals/assessment-statuses` - Get available assessment statuses
- `GET /goals/link-types` - Get available link types
- `GET /goals/relationship-strengths` - Get available relationship strengths
- `GET /goals/contribution-levels` - Get available contribution levels

### System Endpoints
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /` - Service information

## API Reference

See [API_REFERENCE.md](./API_REFERENCE.md) for detailed API documentation.

## Architecture

### Domain Models
- **Goal**: Core goal entity with strategic context and progress tracking
- **GoalLink**: Links goals to other ArchiMate elements

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
docker build -t goal_service .
docker run -p 8080:8080 goal_service
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
- **Event Bus**: Emits events for goal lifecycle changes
- **Architecture Suite**: Links goals to architecture packages
- **Monitoring Dashboard**: Health status and metrics aggregation
- **Audit Log**: Comprehensive audit trail 