# ReqArchitect Gateway Service

## Overview

The Enhanced Gateway Service provides intelligent routing, tenant-aware service mapping, analytics instrumentation, and fault-tolerant proxy logic for the ReqArchitect microservices architecture. It acts as a secure, observable, and modular API gateway without modifying existing service implementations.

## Key Features

### 🚀 Service Registry Integration
- Dynamic service discovery from `service_catalog.json`
- Automatic health monitoring with circuit breaker logic
- Service metadata management (timeouts, retry policies, rate limits)

### 🔐 JWT Identity Forwarding
- Secure JWT token decoding and validation
- Automatic injection of tenant_id and user_id into proxied requests
- No token regeneration - only decode and forward

### 🛡️ RBAC Enforcement (Non-Intrusive)
- Role-based access control without payload inspection
- Granular permissions per service and HTTP method
- Comprehensive audit logging of access decisions

### 📊 Observability & Analytics
- Structured JSON logging with correlation IDs
- OpenTelemetry tracing with distributed spans
- Prometheus metrics for monitoring and alerting
- Request/response latency tracking

### 🔄 Fault-Tolerant Proxy Logic
- Configurable retry policies with exponential backoff
- Circuit breaker pattern for unhealthy services
- Graceful degradation and fallback handling
- Service-specific timeout management

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client        │    │   Gateway        │    │   Microservices │
│                 │    │   Service        │    │                 │
│ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │ JWT Token   │ │    │ │ Auth         │ │    │ │ Assessment  │ │
│ │             │ │    │ │ Middleware   │ │    │ │ Service     │ │
│ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
│                 │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ ┌─────────────┐ │    │ │ RBAC         │ │    │ │ Usage       │ │
│ │ Request     │ │───▶│ │ Middleware   │ │───▶│ │ Service     │ │
│ │             │ │    │ └──────────────┘ │    │ └─────────────┘ │
│ └─────────────┘ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│                 │    │ │ Service       │ │    │ │ Billing     │ │
│ ┌─────────────┐ │    │ │ Registry      │ │    │ │ Service     │ │
│ │ Response    │ │◀───│ └──────────────┘ │◀───│ └─────────────┘ │
│ │             │ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ └─────────────┘ │    │ │ Observability│ │    │ │ ...         │ │
│                 │    │ │ Manager      │ │    │ └─────────────┘ │
└─────────────────┘    │ └──────────────┘ │    └─────────────────┘
                       └──────────────────┘
```

## Quick Start

### Prerequisites
- Python 3.8+
- Docker and Docker Compose
- Redis (for caching, optional)

### Installation

1. **Clone and navigate to the gateway service:**
```bash
cd services/gateway_service
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
export JWT_SECRET_KEY="your-secret-key"
export ENVIRONMENT="development"
export OPENTELEMETRY_ENABLED="true"
```

4. **Start the service:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker Deployment

```bash
# Build the image
docker build -t reqarchitect-gateway .

# Run with Docker Compose
docker-compose up -d
```

## Configuration

### Service Catalog (`service_catalog.json`)

The service catalog defines all available microservices and their configurations:

```json
{
  "services": {
    "assessment": {
      "service_name": "assessment_service",
      "base_path": "/assessment",
      "internal_url": "http://assessment_service:8080",
      "healthcheck_endpoint": "/health",
      "timeout_ms": 15000,
      "tenant_scope": "multi",
      "cacheable": false,
      "retry_policy": {
        "max_retries": 3,
        "backoff_ms": 1000
      },
      "rbac_required": true,
      "rate_limit": {
        "requests_per_minute": 40
      }
    }
  }
}
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `JWT_SECRET_KEY` | Secret key for JWT validation | Required |
| `ENVIRONMENT` | Deployment environment | `development` |
| `OPENTELEMETRY_ENABLED` | Enable OpenTelemetry tracing | `true` |
| `JAEGER_HOST` | Jaeger collector host | `localhost` |
| `JAEGER_PORT` | Jaeger collector port | `6831` |

## API Endpoints

### Health Checks

```bash
# Basic health check
GET /health

# Detailed gateway health with service status
GET /gateway-health

# Prometheus metrics
GET /metrics
```

### Service Management

```bash
# List all services and their status
GET /services

# Get health status for specific service
GET /services/{service_key}/health
```

### Dynamic Routing

The gateway automatically routes requests based on the service catalog:

```bash
# Route to assessment service
GET /assessment/assessments
POST /assessment/assessments

# Route to usage service
GET /usage/usage-records

# Route to billing service
GET /billing/invoices
```

## Authentication & Authorization

### JWT Token Format

```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "role": "Admin",
  "exp": 1640995200
}
```

### Required Headers

```bash
Authorization: Bearer <jwt_token>
```

### Role-Based Permissions

| Role | Permissions |
|------|-------------|
| Owner | Full access to all services |
| Admin | Full access to all services |
| Editor | Create, read, update (no delete) |
| Viewer | Read-only access |

## Observability

### Structured Logging

All requests are logged with structured JSON:

```json
{
  "event": "request_end",
  "request_id": "uuid",
  "correlation_id": "uuid",
  "method": "POST",
  "path": "/assessment/assessments",
  "user_id": "user-uuid",
  "tenant_id": "tenant-uuid",
  "service_target": "assessment",
  "status_code": 201,
  "latency_ms": 245.67,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### OpenTelemetry Tracing

Distributed tracing with spans:
- `route_trace` → `service_proxy_span` → `service_response_span`

### Metrics

Prometheus-style metrics:
- `gateway_requests_total`
- `gateway_errors_total`
- `gateway_service_calls_total`
- `gateway_rbac_denials_total`

## Circuit Breaker Logic

The gateway implements circuit breaker pattern for fault tolerance:

1. **Closed State**: Requests flow normally
2. **Open State**: Requests fail fast when threshold exceeded
3. **Half-Open State**: Limited requests allowed to test recovery

### Configuration

```json
{
  "gateway_config": {
    "circuit_breaker_threshold": 5,
    "circuit_breaker_timeout_seconds": 30,
    "health_check_interval_seconds": 60
  }
}
```

## Retry Logic

Configurable retry policies per service:

```json
{
  "retry_policy": {
    "max_retries": 3,
    "backoff_ms": 1000
  }
}
```

## Rate Limiting

Service-specific rate limits:

```json
{
  "rate_limit": {
    "requests_per_minute": 40
  }
}
```

## Examples

### Successful Request Flow

```bash
# 1. Client sends request with JWT
curl -H "Authorization: Bearer <jwt_token>" \
     -H "Content-Type: application/json" \
     -X POST \
     -d '{"name": "Security Assessment"}' \
     http://localhost:8000/assessment/assessments

# 2. Gateway validates JWT and extracts user context
# 3. RBAC middleware checks permissions
# 4. Service registry resolves target service
# 5. Request is proxied to assessment service
# 6. Response is returned to client
```

### Error Handling

```bash
# Service unavailable (503)
curl http://localhost:8000/assessment/assessments
# Response: {"detail": "Service assessment is currently unavailable"}

# Insufficient permissions (403)
curl -H "Authorization: Bearer <viewer_token>" \
     -X DELETE \
     http://localhost:8000/assessment/assessments/123
# Response: {"detail": "Insufficient permissions. Required: assessment:delete, Role: Viewer"}

# Rate limit exceeded (429)
# Response: {"detail": "Rate limit exceeded"}
```

## Monitoring & Alerting

### Health Checks

```bash
# Check overall gateway health
curl http://localhost:8000/gateway-health

# Check specific service health
curl http://localhost:8000/services/assessment/health
```

### Metrics Collection

```bash
# Get Prometheus metrics
curl http://localhost:8000/metrics
```

### Log Analysis

```bash
# View structured logs
docker logs gateway-service | jq '.'
```

## Development

### Running Tests

```bash
# Run unit tests
pytest tests/

# Run integration tests
pytest tests/integration/
```

### Adding New Services

1. **Update service catalog:**
```json
{
  "new_service": {
    "service_name": "new_service",
    "base_path": "/new_service",
    "internal_url": "http://new_service:8080",
    "healthcheck_endpoint": "/health",
    "timeout_ms": 10000,
    "tenant_scope": "multi",
    "cacheable": false,
    "retry_policy": {
      "max_retries": 3,
      "backoff_ms": 1000
    },
    "rbac_required": true,
    "rate_limit": {
      "requests_per_minute": 50
    }
  }
}
```

2. **Add RBAC permissions** in `app/rbac.py`

3. **Restart gateway service**

### Debugging

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
uvicorn app.main:app --log-level debug
```

## Production Deployment

### Docker Compose

```yaml
version: '3.8'
services:
  gateway:
    build: .
    ports:
      - "8000:8000"
    environment:
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - ENVIRONMENT=production
    depends_on:
      - redis
    networks:
      - reqarchitect

  redis:
    image: redis:7-alpine
    networks:
      - reqarchitect
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gateway-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gateway-service
  template:
    metadata:
      labels:
        app: gateway-service
    spec:
      containers:
      - name: gateway
        image: reqarchitect/gateway:latest
        ports:
        - containerPort: 8000
        env:
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: jwt-secret
              key: secret
```

## Troubleshooting

### Common Issues

1. **Service not found (404)**
   - Check service catalog configuration
   - Verify service is registered in catalog

2. **Authentication failures (401)**
   - Verify JWT token format
   - Check JWT secret key configuration

3. **Permission denied (403)**
   - Check user role and permissions
   - Verify RBAC configuration

4. **Service unavailable (503)**
   - Check service health status
   - Verify circuit breaker configuration

### Log Analysis

```bash
# View gateway logs
docker logs gateway-service

# Filter by request ID
docker logs gateway-service | grep "request_id"

# Check service health
curl http://localhost:8000/services
```

## Contributing

1. Follow the existing code structure
2. Add comprehensive tests
3. Update documentation
4. Ensure observability integration
5. Test with multiple services

## License

This project is part of the ReqArchitect platform and follows the same licensing terms. 