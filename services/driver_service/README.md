# driver_service

A microservice for managing ArchiMate 3.2 Driver elements with comprehensive influence mapping, strategic analysis, RBAC, event emission, observability, and multi-tenancy.

## Business Purpose

The Driver Service represents the ArchiMate 3.2 "Driver" element within the Motivation Layer. Drivers capture external and internal influences that shape enterprise strategy and decision-making. This service provides comprehensive driver management capabilities including:

- **Driver Lifecycle Management**: Create, track, and manage drivers through their complete lifecycle
- **Influence Mapping**: Map how drivers influence other ArchiMate elements across all layers
- **Strategic Analysis**: Analyze driver impact, urgency, and strategic alignment
- **Compliance Tracking**: Monitor regulatory and compliance drivers
- **Multi-tenant Support**: Isolated driver management per tenant
- **Role-based Access Control**: Granular permissions for driver management

## ArchiMate 3.2 Alignment

**Layer**: Motivation Layer
**Element**: Driver
**Purpose**: Represents external or internal influences that shape enterprise strategy

### Key Relationships:
- **Driver → Goal**: Drivers influence goal setting and prioritization
- **Driver → Requirement**: Drivers shape requirement definition
- **Driver → Capability**: Drivers influence capability development
- **Driver → Business Actor**: Drivers affect business actor behavior

## Features

- ✅ Full CRUD operations for Driver elements
- ✅ Driver linking to other ArchiMate elements
- ✅ Multi-tenant support with tenant isolation
- ✅ RBAC enforcement (Owner/Admin/Editor/Viewer)
- ✅ Event emission on create/update/delete operations
- ✅ Redis-based event-driven architecture
- ✅ Prometheus metrics and OpenTelemetry tracing
- ✅ JSON structured logging
- ✅ Health check and metrics endpoints
- ✅ Influence mapping and strategic analysis
- ✅ Domain-specific queries by urgency, category, stakeholder
- ✅ Comprehensive validation and error handling

## Endpoints

### Core CRUD Operations
- `POST /drivers` - Create a new driver
- `GET /drivers` - List drivers with filtering and pagination
- `GET /drivers/{id}` - Get a specific driver
- `PUT /drivers/{id}` - Update a driver
- `DELETE /drivers/{id}` - Delete a driver

### Driver Links
- `POST /drivers/{id}/links` - Create a link to another element
- `GET /drivers/{id}/links` - List all links for a driver
- `GET /links/{link_id}` - Get a specific link
- `PUT /links/{link_id}` - Update a link
- `DELETE /links/{link_id}` - Delete a link

### Analysis and Influence Mapping
- `GET /drivers/{id}/influence-map` - Get influence map for a driver
- `GET /drivers/{id}/analysis` - Analyze driver for strategic insights

### Domain-Specific Queries
- `GET /drivers/by-urgency/{urgency}` - Get drivers by urgency
- `GET /drivers/by-category/{category}` - Get drivers by category
- `GET /drivers/by-stakeholder/{stakeholder_id}` - Get drivers by stakeholder
- `GET /drivers/by-business-actor/{business_actor_id}` - Get drivers by business actor
- `GET /drivers/by-goal/{goal_id}` - Get drivers influencing a goal
- `GET /drivers/by-requirement/{requirement_id}` - Get drivers influencing a requirement

### Utility Endpoints
- `GET /drivers/types` - Get available driver types
- `GET /drivers/categories` - Get available categories
- `GET /drivers/urgencies` - Get available urgencies
- `GET /drivers/impact-levels` - Get available impact levels
- `GET /drivers/time-horizons` - Get available time horizons
- `GET /drivers/geographic-scopes` - Get available geographic scopes
- `GET /drivers/risk-levels` - Get available risk levels
- `GET /drivers/link-types` - Get available link types
- `GET /drivers/link-strengths` - Get available link strengths
- `GET /drivers/influence-directions` - Get available influence directions

### System Endpoints
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /` - Service information

## API Reference

See [API_REFERENCE.md](./API_REFERENCE.md) for detailed API documentation.

## Architecture

### Domain Models
- **Driver**: Core driver entity with strategic context
- **DriverLink**: Links drivers to other ArchiMate elements

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
docker build -t driver_service .
docker run -p 8080:8080 driver_service
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
- **Event Bus**: Emits events for driver lifecycle changes
- **Architecture Suite**: Links drivers to architecture packages
- **Monitoring Dashboard**: Health status and metrics aggregation
- **Audit Log**: Comprehensive audit trail 