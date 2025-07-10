# Architecture Validation Service

The Architecture Validation Service evaluates and scores tenant-specific architecture models for alignment, traceability, and completeness across all ArchiMate 3.2 layers.

## Overview

This service provides automated validation of architectural models to ensure:

- **Traceability**: All elements have proper relationships across layers
- **Completeness**: Required elements and relationships are present
- **Alignment**: Strategic goals align with implementation details
- **Quality**: Models meet enterprise architecture standards

## Features

### Core Validation Capabilities

- **Multi-layer Validation**: Validates across Motivation, Business, Application, Technology, and Implementation layers
- **Traceability Path Checking**: Ensures proper relationships between Goals → Capabilities → Components → Infrastructure
- **Completeness Scanning**: Identifies missing required elements and relationships
- **Staleness Detection**: Flags outdated elements based on modification timestamps
- **Enum/Constraint Validation**: Ensures correct classification of strategic elements
- **Orphan Detection**: Identifies elements not linked to any trace path

### Validation Rules

The service implements configurable validation rules including:

- "All Goals must link to at least one Capability"
- "Capabilities must be realized by Business Functions or Application Functions"
- "Every Plateau must be linked to at least one WorkPackage and Gap"
- "Requirements must influence at least one Course of Action or Capability"

### Scoring & Analytics

- **Maturity Scoring**: Calculates overall architecture maturity scores
- **Layer-specific Analysis**: Provides scores for each ArchiMate layer
- **Issue Tracking**: Categorizes issues by severity and type
- **Historical Analysis**: Tracks validation results over time

## Architecture

### Domain Models

- **ValidationCycle**: Tracks validation execution cycles
- **ValidationIssue**: Records specific validation issues found
- **ValidationRule**: Defines validation rules and logic
- **ValidationException**: Whitelists intentional modeling gaps
- **ValidationScorecard**: Stores layer-specific scores
- **TraceabilityMatrix**: Maps cross-layer relationships

### Service Integration

The service integrates with all other ReqArchitect microservices to:

- Fetch architectural elements from each service
- Validate relationships and traceability paths
- Emit Redis events for validation results
- Maintain audit trails of validation activities

## API Endpoints

### Validation Management

- `POST /validation/run` - Trigger full validation scan
- `GET /validation/issues` - List all validation issues
- `GET /validation/scorecard` - Get maturity score breakdown
- `GET /validation/traceability-matrix` - Cross-layer trace map
- `GET /validation/history` - Past validation cycles

### Rule Management

- `POST /validation/exceptions` - Whitelist intentional gaps
- `PATCH /validation/rules/{id}` - Toggle rule activation
- `GET /validation/rules` - List all validation rules

### System Endpoints

- `GET /health` - Service health check
- `GET /metrics` - Service metrics
- `GET /` - Service information

## Setup & Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Docker (optional)

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/architecture_validation

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET_KEY=your-secret-key

# Logging
LOG_LEVEL=INFO
```

### Local Development

1. **Clone and setup**:
   ```bash
   cd services/architecture_validation_service
   pip install -r requirements.txt
   ```

2. **Database setup**:
   ```bash
   # Create database
   createdb architecture_validation
   
   # Run migrations
   alembic upgrade head
   ```

3. **Start the service**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
   ```

### Docker Deployment

```bash
# Build image
docker build -t architecture-validation-service .

# Run container
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:password@host:5432/architecture_validation \
  -e REDIS_URL=redis://host:6379 \
  architecture-validation-service
```

## Usage Examples

### Running a Validation Cycle

```bash
curl -X POST "http://localhost:8080/validation/run" \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "rule_set_id": "optional-rule-set",
    "force_full_scan": false
  }'
```

### Getting Validation Issues

```bash
curl -X GET "http://localhost:8080/validation/issues?skip=0&limit=100" \
  -H "Authorization: Bearer <jwt_token>"
```

### Creating a Validation Exception

```bash
curl -X POST "http://localhost:8080/validation/exceptions" \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "goal",
    "entity_id": "goal-123",
    "reason": "This goal is intentionally not linked to capabilities",
    "rule_id": "rule-456",
    "expires_at": "2024-12-31T23:59:59Z"
  }'
```

### Getting Validation Scorecard

```bash
curl -X GET "http://localhost:8080/validation/scorecard" \
  -H "Authorization: Bearer <jwt_token>"
```

## Validation Rules

### Default Rules

The service includes several default validation rules:

#### Traceability Rules
- **Goal-Capability Linkage**: All goals must link to at least one capability
- **Capability-Realization**: Capabilities must be realized by business or application functions
- **Requirement-Influence**: Requirements must influence courses of action or capabilities

#### Completeness Rules
- **Plateau-WorkPackage**: Every plateau must link to work packages and gaps
- **Business Process-Role**: Business processes must have assigned roles
- **Application Service-Function**: Application services must be realized by functions

#### Alignment Rules
- **Strategic-Implementation**: Strategic elements must align with implementation details
- **Business-Application**: Business layer must properly align with application layer
- **Technology-Infrastructure**: Technology decisions must support infrastructure requirements

### Custom Rules

You can create custom validation rules by:

1. **Defining Rule Logic**: JSON-based rule definitions
2. **Setting Scope**: Specify which ArchiMate layers to validate
3. **Configuring Severity**: Set issue severity levels
4. **Managing Exceptions**: Whitelist intentional modeling gaps

## Monitoring & Observability

### Metrics

The service exposes Prometheus metrics including:

- `validation_cycles_total`: Total validation cycles run
- `validation_issues_total`: Total issues found
- `validation_rules_active`: Number of active rules
- `average_maturity_score`: Average architecture maturity score
- `validation_duration_seconds`: Validation execution time

### Logging

Structured JSON logging includes:

- Request/response logging
- Validation cycle events
- Issue detection events
- Error tracking
- Performance metrics

### Redis Events

The service emits Redis events:

- `validation.completed`: When validation cycle completes
- `validation.issue_detected`: When new issues are found

## Security

### Authentication

All endpoints require JWT authentication with:
- `tenant_id`: UUID of the tenant
- `user_id`: UUID of the user
- `role`: User role (Owner, Admin, Editor, Viewer)

### Authorization

- **Owner/Admin**: Can trigger validation cycles and manage rules
- **Editor**: Can view validation results and create exceptions
- **Viewer**: Can view validation results only

### Multi-tenancy

All data is scoped by `tenant_id` to ensure proper isolation.

## Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Test Coverage

Tests cover:
- Validation rule execution
- Cross-layer trace traversal
- Exception handling
- RBAC enforcement
- Redis event emission
- Database operations

## Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Ensure multi-tenancy compliance
5. Follow security best practices

## License

This service is part of the ReqArchitect platform and follows the same licensing terms. 