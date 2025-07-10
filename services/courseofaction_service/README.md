# Course of Action Service

## Overview

The Course of Action Service is a microservice within the ReqArchitect platform that manages ArchiMate 3.2 "Course of Action" elements in the Strategy Layer. This service provides comprehensive management of strategic approaches to achieve goals or realize capabilities, influenced by Drivers and constrained by Constraints.

## ArchiMate 3.2 Alignment

### Strategy Layer Element
- **Course of Action**: Represents intended strategic approaches to achieve goals or realize capabilities
- **Relationships**: Goal, Capability, Driver, Constraint, Assessment
- **Strategic Categories**: Transformational, Incremental, Defensive, Innovative

### Key Features
- **Strategic Planning**: Define and manage courses of action with clear objectives
- **Risk Management**: Comprehensive risk assessment and mitigation strategies
- **Performance Tracking**: Monitor progress, success probability, and outcomes
- **Alignment Analysis**: Strategic alignment with goals, capabilities, and stakeholders
- **Resource Management**: Cost tracking, budget allocation, and resource requirements

## Architecture

### Technology Stack
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based with RBAC
- **Event System**: Redis-based event emission
- **Observability**: Prometheus metrics, OpenTelemetry tracing
- **Documentation**: OpenAPI/Swagger

### Service Components
- **Models**: CourseOfAction, ActionLink with comprehensive attributes
- **API**: RESTful endpoints with CRUD operations and analysis
- **Security**: Multi-tenant with JWT authentication and RBAC
- **Validation**: Pydantic schemas with enum validation
- **Testing**: Comprehensive unit and integration tests

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- Docker (optional)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd services/courseofaction_service
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the service**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Docker Deployment
```bash
docker build -t courseofaction-service .
docker run -p 8080:8080 courseofaction-service
```

## API Usage

### Authentication
All endpoints require JWT authentication:
```bash
curl -H "Authorization: Bearer <jwt_token>" \
     http://localhost:8080/api/v1/courses-of-action
```

### Create Course of Action
```bash
curl -X POST http://localhost:8080/api/v1/courses-of-action \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cloud Migration Initiative",
    "description": "Strategic initiative to migrate legacy systems",
    "strategy_type": "transformational",
    "success_probability": 0.8,
    "risk_level": "medium",
    "time_horizon": "medium_term"
  }'
```

### Get Alignment Map
```bash
curl http://localhost:8080/api/v1/courses-of-action/{id}/alignment-map \
  -H "Authorization: Bearer <jwt_token>"
```

### Get Risk Profile
```bash
curl http://localhost:8080/api/v1/courses-of-action/{id}/risk-profile \
  -H "Authorization: Bearer <jwt_token>"
```

## Key Endpoints

### Course of Action Management
- `POST /api/v1/courses-of-action` - Create course of action
- `GET /api/v1/courses-of-action` - List with filtering
- `GET /api/v1/courses-of-action/{id}` - Get by ID
- `PUT /api/v1/courses-of-action/{id}` - Update
- `DELETE /api/v1/courses-of-action/{id}` - Delete

### Action Link Management
- `POST /api/v1/courses-of-action/{id}/links` - Create link
- `GET /api/v1/courses-of-action/{id}/links` - List links
- `PUT /api/v1/courses-of-action/links/{link_id}` - Update link
- `DELETE /api/v1/courses-of-action/links/{link_id}` - Delete link

### Analysis & Alignment
- `GET /api/v1/courses-of-action/{id}/alignment-map` - Strategic alignment
- `GET /api/v1/courses-of-action/{id}/risk-profile` - Risk assessment
- `GET /api/v1/courses-of-action/{id}/analysis` - Comprehensive analysis

### Domain-Specific Queries
- `GET /api/v1/courses-of-action/by-type/{strategy_type}` - By strategy type
- `GET /api/v1/courses-of-action/by-capability/{capability_id}` - By capability
- `GET /api/v1/courses-of-action/by-risk-level/{risk_level}` - By risk level
- `GET /api/v1/courses-of-action/active` - Active courses of action
- `GET /api/v1/courses-of-action/critical` - Critical courses of action

### Enumeration Endpoints
- `GET /api/v1/courses-of-action/strategy-types` - Available strategy types
- `GET /api/v1/courses-of-action/risk-levels` - Available risk levels
- `GET /api/v1/courses-of-action/time-horizons` - Available time horizons

## Data Models

### CourseOfAction
Core fields for strategic course of action management:
- **Basic Info**: name, description, strategy_type
- **Strategic Context**: strategic_objective, business_case, success_criteria
- **Time & Planning**: time_horizon, start_date, target_completion_date
- **Risk & Probability**: success_probability, risk_level, risk_assessment
- **Resource & Cost**: estimated_cost, actual_cost, budget_allocation
- **Performance**: current_progress, performance_metrics, outcomes_achieved
- **Alignment**: strategic_alignment_score, capability_impact_score, goal_achievement_score

### ActionLink
Relationship management between courses of action and other elements:
- **Link Info**: linked_element_id, linked_element_type, link_type
- **Relationship**: relationship_strength, dependency_level
- **Strategic Context**: strategic_importance, business_value, alignment_score
- **Implementation**: implementation_priority, resource_allocation
- **Impact**: impact_level, impact_direction, impact_confidence

## Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/courseofaction_service

# Security
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256

# Redis
REDIS_URL=redis://localhost:6379

# Observability
OTEL_ENABLED=true
OTEL_ENDPOINT=http://localhost:4317

# Service
PORT=8080
HOST=0.0.0.0
```

### Database Schema
The service creates the following tables:
- `course_of_action` - Main course of action data
- `action_link` - Relationship links to other elements

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_courseofaction.py
```

### Test Categories
- **CRUD Operations**: Create, read, update, delete courses of action
- **Action Links**: Link management and relationships
- **Analysis**: Alignment maps, risk profiles, comprehensive analysis
- **Domain Queries**: Strategy type, capability, risk level filtering
- **Validation**: Data validation and error handling
- **Authentication**: JWT authentication and RBAC
- **Health & Metrics**: Health checks and monitoring

## Monitoring & Observability

### Health Check
```bash
curl http://localhost:8080/health
```

### Metrics
```bash
curl http://localhost:8080/metrics
```

### OpenAPI Documentation
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## Security

### Authentication
- JWT-based authentication
- Required claims: tenant_id, user_id, role

### Authorization
- Role-based access control (RBAC)
- Roles: Owner, Admin, Editor, Viewer
- Permission matrix for all operations

### Multi-tenancy
- Tenant isolation via tenant_id
- All operations scoped to tenant

## Event System

### Event Types
- `course_of_action_created` - New course of action created
- `course_of_action_updated` - Course of action updated
- `course_of_action_deleted` - Course of action deleted
- `action_link_created` - New action link created
- `action_link_updated` - Action link updated
- `action_link_deleted` - Action link deleted

### Event Format
```json
{
  "event_type": "course_of_action_created",
  "service": "courseofaction_service",
  "data": {
    "course_of_action_id": "uuid",
    "tenant_id": "uuid",
    "user_id": "uuid"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Deployment

### Docker
```bash
# Build image
docker build -t courseofaction-service .

# Run container
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:password@host:5432/db \
  -e REDIS_URL=redis://host:6379 \
  courseofaction-service
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: courseofaction-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: courseofaction-service
  template:
    metadata:
      labels:
        app: courseofaction-service
    spec:
      containers:
      - name: courseofaction-service
        image: courseofaction-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: REDIS_URL
          value: "redis://redis-service:6379"
```

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run linting: `flake8 app/`
5. Run security checks: `bandit -r app/`
6. Submit pull request

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings
- Write comprehensive tests

## Support

### Documentation
- API Reference: See `API_REFERENCE.md`
- Architecture: See `ARCHITECTURE.md`
- Implementation Summary: See `COURSEOFACTION_SERVICE_IMPLEMENTATION_SUMMARY.md`

### Issues
- Report bugs via GitHub Issues
- Include logs and reproduction steps
- Provide environment details

### Contact
- Team: Architecture Services
- Repository: ReqArchitect Platform
- Documentation: Internal Wiki
