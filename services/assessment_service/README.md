# Assessment Service

## Overview

The Assessment Service is a microservice that manages ArchiMate 3.2 Assessment elements in the Implementation & Migration Layer. It provides comprehensive evaluation management for goals, outcomes, performance measures, and strategic directions.

## ArchiMate 3.2 Alignment

- **Element**: Assessment
- **Layer**: Implementation & Migration Layer
- **Purpose**: Evaluations of goals, outcomes, performance measures, or strategic directions
- **Relationships**: Goal, Capability, Stakeholder, Constraint, Business Function

## Features

### Core Functionality
- ✅ Full CRUD operations for Assessment entities
- ✅ Assessment link management to other ArchiMate elements
- ✅ Multi-tenant architecture with tenant isolation
- ✅ JWT-based authentication and role-based access control
- ✅ Redis event-driven integration for lifecycle operations
- ✅ Comprehensive observability with health checks, metrics, and tracing

### Assessment Types
- **Performance**: Evaluate performance against targets
- **Compliance**: Assess compliance with standards and regulations
- **Strategic**: Evaluate strategic alignment and effectiveness
- **Risk**: Assess risk levels and mitigation strategies
- **Maturity**: Evaluate capability and process maturity
- **Capability**: Assess organizational capabilities
- **Goal**: Evaluate goal achievement and progress
- **Outcome**: Assess outcome realization and impact

### Assessment Methods
- **Quantitative**: Numerical measurements and metrics
- **Qualitative**: Descriptive analysis and observations
- **Mixed**: Combination of quantitative and qualitative approaches
- **Survey**: Structured questionnaires and feedback
- **Interview**: Direct stakeholder interviews
- **Observation**: Direct observation and monitoring
- **Document Review**: Analysis of existing documentation
- **Metrics Analysis**: Statistical analysis of performance data

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Docker (optional)

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://assessment_user:assessment_pass@localhost:5432/assessment_db

# Security
JWT_SECRET_KEY=your-secret-key-here

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Observability
OTLP_ENDPOINT=http://localhost:4317
```

### Installation

1. **Clone and setup**
```bash
cd services/assessment_service
pip install -r requirements.txt
```

2. **Database setup**
```bash
# Create database
createdb assessment_db

# Run migrations (if using Alembic)
alembic upgrade head
```

3. **Start the service**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Docker Deployment

```bash
# Build image
docker build -t assessment-service .

# Run container
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e JWT_SECRET_KEY=your-secret \
  assessment-service
```

## API Usage

### Authentication

All endpoints require JWT authentication:

```bash
curl -H "Authorization: Bearer <jwt_token>" \
  http://localhost:8080/api/v1/assessments
```

### Create Assessment

```bash
curl -X POST "http://localhost:8080/api/v1/assessments" \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Strategic Maturity Assessment (Q2)",
    "description": "Quarterly strategic maturity evaluation",
    "assessment_type": "maturity",
    "evaluator_user_id": "550e8400-e29b-41d4-a716-446655440001",
    "assessment_method": "mixed",
    "confidence_score": 0.85,
    "planned_start_date": "2024-01-15T00:00:00Z",
    "planned_end_date": "2024-01-30T00:00:00Z"
  }'
```

### List Assessments

```bash
curl -H "Authorization: Bearer <jwt_token>" \
  "http://localhost:8080/api/v1/assessments?assessment_type=maturity&status=in_progress"
```

### Get Assessment Analysis

```bash
# Get evaluation metrics
curl -H "Authorization: Bearer <jwt_token>" \
  "http://localhost:8080/api/v1/assessments/{assessment_id}/evaluation-metrics"

# Get confidence score analysis
curl -H "Authorization: Bearer <jwt_token>" \
  "http://localhost:8080/api/v1/assessments/{assessment_id}/confidence-score"
```

## Architecture

### Service Structure

```
assessment_service/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── services.py          # Business logic
│   ├── routes.py            # API endpoints
│   ├── deps.py              # Dependencies and auth
│   └── main.py              # FastAPI application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── README.md                # This file
├── API_REFERENCE.md         # Detailed API documentation
├── ARCHITECTURE.md          # Architecture documentation
└── ASSESSMENT_SERVICE_IMPLEMENTATION_SUMMARY.md
```

### Data Models

#### Assessment Entity
- **Core Fields**: name, description, assessment_type, evaluator_user_id
- **Evaluation Targets**: evaluated_goal_id, evaluated_capability_id, etc.
- **Assessment Details**: method, result_summary, metrics_scored, confidence_score
- **Timeline**: planned_start_date, planned_end_date, actual_start_date, actual_end_date
- **Status**: status, progress_percent, validation_status
- **Quality**: quality_score, evidence_quality, framework_compliance
- **Results**: key_findings, recommendations, risk_implications

#### AssessmentLink Entity
- **Link Metadata**: linked_element_id, linked_element_type, link_type
- **Relationship**: relationship_strength, dependency_level, impact_level
- **Evidence**: evidence_provided, evidence_quality, validation_status
- **Contribution**: contribution_score, contribution_description, contribution_metrics

### Security Model

#### Multi-Tenancy
- All data is isolated by `tenant_id`
- Tenant context extracted from JWT token
- Cross-tenant access prevention

#### Role-Based Access Control
- **Owner**: Full access to all operations
- **Admin**: Full access to all operations
- **Editor**: Create, read, update (no delete)
- **Viewer**: Read-only access

#### Permissions
- `assessment:create` - Create assessments
- `assessment:read` - Read assessments
- `assessment:update` - Update assessments
- `assessment:delete` - Delete assessments
- `assessment_link:create` - Create assessment links
- `assessment_link:read` - Read assessment links
- `assessment_link:update` - Update assessment links
- `assessment_link:delete` - Delete assessment links

### Event-Driven Architecture

#### Redis Events
- `assessment_created` - Assessment creation events
- `assessment_updated` - Assessment update events
- `assessment_deleted` - Assessment deletion events
- `assessment_link_created` - Link creation events
- `assessment_link_updated` - Link update events
- `assessment_link_deleted` - Link deletion events

#### Event Payload
```json
{
  "event_type": "assessment_created",
  "assessment_id": "uuid",
  "tenant_id": "uuid",
  "assessment_type": "maturity",
  "status": "planned",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Observability

### Health Checks
```bash
curl http://localhost:8080/health
```

### Metrics
```bash
curl http://localhost:8080/metrics
```

### Tracing
- OpenTelemetry integration
- Distributed tracing across services
- Span correlation for request flows

### Logging
- Structured JSON logging
- Request/response logging
- Error tracking and correlation

## Examples

### Strategic Maturity Assessment
```json
{
  "name": "Strategic Maturity Assessment (Q2)",
  "description": "Quarterly evaluation of strategic capability maturity",
  "assessment_type": "maturity",
  "assessment_method": "mixed",
  "assessment_framework": "TOGAF",
  "evaluator_user_id": "550e8400-e29b-41d4-a716-446655440001",
  "confidence_score": 0.85,
  "planned_start_date": "2024-01-15T00:00:00Z",
  "planned_end_date": "2024-01-30T00:00:00Z",
  "status": "planned"
}
```

### Goal Performance Scorecard
```json
{
  "name": "Goal Performance Scorecard: Customer Experience",
  "description": "Evaluation of customer experience goal achievement",
  "assessment_type": "goal",
  "evaluated_goal_id": "550e8400-e29b-41d4-a716-446655440002",
  "assessment_method": "quantitative",
  "metrics_scored": "{\"satisfaction_score\": {\"score\": 0.8, \"weight\": 0.4}, \"response_time\": {\"score\": 0.9, \"weight\": 0.3}, \"resolution_rate\": {\"score\": 0.85, \"weight\": 0.3}}",
  "confidence_score": 0.9,
  "status": "complete"
}
```

### GDPR Compliance Evaluation
```json
{
  "name": "GDPR Compliance Evaluation for Portal Access",
  "description": "Assessment of GDPR compliance for customer portal",
  "assessment_type": "compliance",
  "assessment_method": "document_review",
  "compliance_standards": "[\"GDPR\", \"ISO27001\"]",
  "evaluator_user_id": "550e8400-e29b-41d4-a716-446655440003",
  "confidence_score": 0.75,
  "status": "in_progress"
}
```

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Quality
```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Add new field"

# Apply migrations
alembic upgrade head
```

## Production Deployment

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: assessment-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: assessment-service
  template:
    metadata:
      labels:
        app: assessment-service
    spec:
      containers:
      - name: assessment-service
        image: assessment-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: jwt-secret
              key: secret
```

### Environment Configuration
```bash
# Production environment variables
export DATABASE_URL="postgresql://user:pass@prod-db:5432/assessment_db"
export JWT_SECRET_KEY="your-production-secret-key"
export REDIS_HOST="prod-redis"
export OTLP_ENDPOINT="http://jaeger:4317"
export LOG_LEVEL="INFO"
```

## Monitoring and Alerting

### Key Metrics
- Request rate and latency
- Assessment operation counts
- Database connection health
- Redis connection status
- Error rates and types

### Alerts
- High error rate (>5%)
- High latency (>2s)
- Database connection failures
- Redis connection failures
- Service health check failures

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check DATABASE_URL configuration
   - Verify database is running and accessible
   - Check network connectivity

2. **Redis Connection Errors**
   - Verify Redis is running
   - Check REDIS_HOST and REDIS_PORT
   - Ensure Redis authentication if configured

3. **JWT Authentication Errors**
   - Verify JWT_SECRET_KEY is set
   - Check token format and expiration
   - Validate token claims

4. **Permission Denied Errors**
   - Verify user role and permissions
   - Check tenant isolation
   - Validate resource ownership

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL="DEBUG"
uvicorn app.main:app --reload --log-level debug
```

## Contributing

1. Follow the established code style and patterns
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Ensure multi-tenant security is maintained
5. Validate ArchiMate 3.2 compliance

## License

This service is part of the ReqArchitect platform and follows the same licensing terms. 