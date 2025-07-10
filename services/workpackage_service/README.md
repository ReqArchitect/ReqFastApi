# Work Package Service

## Overview

The Work Package Service is a microservice that manages ArchiMate 3.2 Work Package elements in the Implementation & Migration Layer. Work Packages represent units of work—projects, epics, initiatives—that realize transformation efforts, close gaps, and deliver plateaus.

## ArchiMate 3.2 Alignment

- **Layer**: Implementation & Migration Layer
- **Element**: Work Package
- **Purpose**: Represents units of work that realize transformation efforts
- **Relationships**: Links to Goals, Gaps, Plateaus, Capabilities, Requirements, and Technology elements

## Features

### Core Functionality
- **CRUD Operations**: Full lifecycle management of Work Package entities
- **Package Links**: Relationship management with other ArchiMate elements
- **Multi-tenancy**: Complete tenant isolation and data segregation
- **JWT Authentication**: Secure access control with token-based authentication
- **Role-based Access Control**: Granular permissions for different user roles

### Analysis & Intelligence
- **Execution Status Analysis**: Real-time progress tracking and performance metrics
- **Gap Closure Mapping**: Traceability between work packages and gap closure
- **Risk Assessment**: Automated risk identification and mitigation tracking
- **Resource Utilization**: Effort, budget, and team utilization analysis
- **Quality Gates**: Structured quality control and validation processes

### Observability
- **Health Monitoring**: `/health` endpoint with comprehensive status checks
- **Metrics Collection**: Prometheus metrics for monitoring and alerting
- **Distributed Tracing**: OpenTelemetry integration for request tracing
- **Structured Logging**: Comprehensive logging with correlation IDs
- **Redis Event Emission**: Real-time event streaming for integration

### Domain-Specific Queries
- Filtering by package type, status, risk level, and progress
- Goal and plateau alignment tracking
- Change owner and stakeholder management
- Performance threshold analysis

## Architecture

### Technology Stack
- **Framework**: FastAPI with async/await support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for event emission and caching
- **Authentication**: JWT with role-based permissions
- **Observability**: OpenTelemetry, Prometheus, structured logging
- **Containerization**: Docker with multi-stage builds

### Service Structure
```
workpackage_service/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application setup
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── services.py          # Business logic layer
│   ├── routes.py            # API endpoint definitions
│   └── deps.py              # Authentication dependencies
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
└── README.md               # This file
```

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Docker (optional)

### Local Development

1. **Clone and Setup**
```bash
cd services/workpackage_service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment Configuration**
```bash
export DATABASE_URL="postgresql://workpackage_user:workpackage_pass@localhost:5432/workpackage_db"
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
export SECRET_KEY="your-secret-key-here"
```

3. **Database Setup**
```bash
# Create database and user
createdb workpackage_db
psql -d workpackage_db -c "CREATE USER workpackage_user WITH PASSWORD 'workpackage_pass';"
psql -d workpackage_db -c "GRANT ALL PRIVILEGES ON DATABASE workpackage_db TO workpackage_user;"
```

4. **Run the Service**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Docker Deployment

1. **Build Image**
```bash
docker build -t workpackage-service .
```

2. **Run Container**
```bash
docker run -p 8080:8080 \
  -e DATABASE_URL="postgresql://workpackage_user:workpackage_pass@db:5432/workpackage_db" \
  -e REDIS_HOST="redis" \
  -e REDIS_PORT="6379" \
  workpackage-service
```

## API Documentation

### Base URL
```
http://localhost:8080
```

### Authentication
All endpoints require JWT authentication:
```bash
curl -H "Authorization: Bearer <jwt_token>" \
  http://localhost:8080/api/v1/work-packages
```

### Key Endpoints

#### Work Package Management
- `POST /api/v1/work-packages` - Create work package
- `GET /api/v1/work-packages` - List work packages with filtering
- `GET /api/v1/work-packages/{id}` - Get work package details
- `PUT /api/v1/work-packages/{id}` - Update work package
- `DELETE /api/v1/work-packages/{id}` - Delete work package

#### Analysis Endpoints
- `GET /api/v1/work-packages/{id}/execution-status` - Execution analysis
- `GET /api/v1/work-packages/{id}/gap-closure-map` - Gap closure mapping

#### Domain Queries
- `GET /api/v1/work-packages/by-type/{type}` - Filter by package type
- `GET /api/v1/work-packages/by-status/{status}` - Filter by status
- `GET /api/v1/work-packages/by-risk/{risk}` - Filter by delivery risk
- `GET /api/v1/work-packages/active` - Get active work packages
- `GET /api/v1/work-packages/critical` - Get critical work packages

#### Package Links
- `POST /api/v1/work-packages/{id}/links` - Create package link
- `GET /api/v1/work-packages/{id}/links` - List package links
- `PUT /api/v1/work-packages/links/{link_id}` - Update package link
- `DELETE /api/v1/work-packages/links/{link_id}` - Delete package link

### Interactive Documentation
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **OpenAPI JSON**: http://localhost:8080/openapi.json

## Data Models

### Work Package
Core entity representing a unit of work:

```python
class WorkPackage:
    id: UUID                    # Primary key
    tenant_id: UUID            # Multi-tenancy
    name: str                  # Work package name
    package_type: PackageType  # project, epic, task, etc.
    current_status: PackageStatus  # planned, in_progress, completed
    progress_percent: float    # 0-100 progress
    delivery_risk: DeliveryRisk  # low, medium, high, critical
    scheduled_start: datetime  # Planned start date
    scheduled_end: datetime    # Planned end date
    estimated_effort_hours: float  # Estimated effort
    budget_allocation: float  # Budget allocation
    change_owner_id: UUID     # Change owner
    # ... additional fields
```

### Package Link
Relationships between work packages and other ArchiMate elements:

```python
class PackageLink:
    id: UUID                  # Primary key
    work_package_id: UUID     # Work package reference
    linked_element_id: UUID   # Linked element ID
    linked_element_type: str  # goal, gap, capability, etc.
    link_type: LinkType       # realizes, closes, delivers, etc.
    relationship_strength: RelationshipStrength  # strong, medium, weak
    dependency_level: DependencyLevel  # high, medium, low
    # ... additional fields
```

## Sample Data

### Work Package Examples
- **"Modernization Sprint #7"** - Project type, in progress, 75% complete
- **"Regulatory Compliance Initiative"** - Initiative type, planned, high risk
- **"Cloud Deployment Phase 2"** - Phase type, in progress, medium risk
- **"Customer Portal Redesign Epic"** - Epic type, completed, low risk
- **"Capability Recovery Task for Data Loss Gap"** - Task type, blocked, critical risk

### Package Link Examples
- Work Package → Goal: "realizes" relationship
- Work Package → Gap: "closes" relationship
- Work Package → Plateau: "delivers" relationship
- Work Package → Capability: "enables" relationship

## Monitoring & Observability

### Health Checks
```bash
curl http://localhost:8080/health
```

### Metrics
```bash
curl http://localhost:8080/metrics
```

### Logs
Structured logging with correlation IDs and contextual information.

### Tracing
OpenTelemetry integration for distributed tracing across services.

## Security

### Authentication
- JWT-based authentication
- Token validation and expiration handling
- Secure token storage and transmission

### Authorization
- Role-based access control (Owner, Admin, Editor, Viewer)
- Granular permissions for different operations
- Tenant isolation and data segregation

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Rate limiting and throttling

## Testing

### Unit Tests
```bash
pytest tests/unit/
```

### Integration Tests
```bash
pytest tests/integration/
```

### API Tests
```bash
pytest tests/api/
```

## Deployment

### Production Considerations
- Use environment variables for configuration
- Implement proper logging and monitoring
- Set up database backups and recovery
- Configure load balancing and scaling
- Implement security best practices

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: workpackage-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: workpackage-service
  template:
    metadata:
      labels:
        app: workpackage-service
    spec:
      containers:
      - name: workpackage-service
        image: workpackage-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: workpackage-secrets
              key: database-url
```

## Contributing

1. Follow the established code style and patterns
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Ensure multi-tenancy and security compliance
5. Follow the ReqArchitect architecture standards

## License

This service is part of the ReqArchitect platform and follows the same licensing terms.
