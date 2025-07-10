# API Debug Service

A non-intrusive microservice that safely visualizes service health, base URLs, and routed endpoint summaries across all ReqArchitect microservices without modifying any existing services or configurations.

## 🎯 Features

- **Non-intrusive Discovery**: Safely inspects running Docker containers without modification
- **Endpoint Mapping**: Discovers API endpoints from multiple sources (Swagger, API docs, health checks)
- **Health Monitoring**: Real-time service health status and availability tracking
- **Caching**: Redis-based caching to prevent excessive endpoint reloads
- **Comprehensive Reporting**: Detailed service maps with container information and network details

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │  Docker Service │    │ Endpoint Discovery│
│                 │    │                 │    │                 │
│ • Health Check  │◄──►│ • Container List│◄──►│ • Swagger/OpenAPI│
│ • API Endpoints │    │ • Port Mapping  │    │ • API Reference │
│ • Cache Mgmt    │    │ • Health Check  │    │ • Known Patterns │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Cache Service  │    │ Service Discovery│    │  Orchestrator   │
│                 │    │                 │    │                 │
│ • Redis Cache   │    │ • Container Info│    │ • Coordination  │
│ • TTL Management│    │ • Endpoint Maps │    │ • Error Handling│
│ • Serialization │    │ • Health Status │    │ • Logging       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Redis (for caching)
- Access to ReqArchitect Docker network

### Running the Service

```bash
# Build and run with Docker
docker build -t api-debug-service .
docker run -d \
  --name api-debug-service \
  --network reqarchitect-network \
  -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  api-debug-service
```

### Environment Variables

```bash
# Optional configuration
REDIS_URL=redis://localhost:6379
CACHE_TTL_SECONDS=300
DOCKER_NETWORK=reqarchitect-network
SERVICE_LABEL=reqarchitect-service=true
```

## 📋 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api-debug` | GET | Get all service endpoints |
| `/api-debug/{service}` | GET | Get endpoints for specific service |
| `/api-debug/health-summary` | GET | Get comprehensive health summary |
| `/api-debug/{service}/details` | GET | Get detailed service information |

### Utility Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Service health check |
| `/metrics` | GET | Service metrics |
| `/api-debug/refresh` | POST | Force cache refresh |
| `/api-debug/stats` | GET | Discovery statistics |
| `/api-debug/services/healthy` | GET | Get only healthy services |
| `/api-debug/services/unhealthy` | GET | Get only unhealthy services |

## 📊 Example Responses

### Get All Services

```bash
curl http://localhost:8080/api-debug
```

```json
[
  {
    "service_name": "goal_service",
    "docker_container_name": "/goal-service",
    "base_url": "http://localhost:8081",
    "status": "healthy",
    "available_endpoints": [
      {
        "path": "/goals",
        "method": "GET",
        "description": "List all goals"
      },
      {
        "path": "/goals/{id}",
        "method": "GET",
        "description": "Get goal by ID"
      }
    ],
    "last_heartbeat": "2024-01-15T10:30:00Z",
    "version_tag": "latest",
    "port": 8081,
    "container_id": "abc123...",
    "image": "reqarchitect/goal-service:latest"
  }
]
```

### Health Summary

```bash
curl http://localhost:8080/api-debug/health-summary
```

```json
{
  "total_services": 15,
  "healthy_services": 13,
  "unhealthy_services": 1,
  "unknown_services": 1,
  "services": [...],
  "last_updated": "2024-01-15T10:30:00Z",
  "cache_status": "fresh"
}
```

### Service Details

```bash
curl http://localhost:8080/api-debug/goal_service/details
```

```json
{
  "service": {
    "service_name": "goal_service",
    "base_url": "http://localhost:8081",
    "status": "healthy",
    "available_endpoints": [...],
    "container_id": "abc123...",
    "image": "reqarchitect/goal-service:latest"
  },
  "logs": [
    "2024-01-15T10:30:00Z INFO: Service started",
    "2024-01-15T10:30:01Z INFO: Health check passed"
  ],
  "network_info": {
    "id": "def456...",
    "name": "reqarchitect-network",
    "driver": "bridge",
    "containers": 15
  },
  "cache_stats": {
    "total_keys": 5,
    "cache_ttl_seconds": 300,
    "redis_connected": true
  }
}
```

## 🔍 Discovery Methods

The service uses multiple methods to discover endpoints:

1. **Swagger/OpenAPI**: Queries `/openapi.json` and `/swagger.json`
2. **API Reference**: Reads `/API_REFERENCE.md` files
3. **Known Patterns**: Uses predefined endpoint patterns for each service
4. **Health Endpoints**: Checks `/health`, `/healthz`, `/ping`

## 🛡️ Security & Safety

### Non-Intrusive Design

- **Read-Only Access**: Only inspects containers, never modifies them
- **No Restarts**: Never restarts or stops existing containers
- **No Mounts**: Doesn't mount volumes or modify container configurations
- **Safe Queries**: Uses HEAD requests to verify endpoints without side effects

### Access Control

- **Docker Socket**: Requires access to Docker socket for container inspection
- **Network Access**: Needs access to ReqArchitect Docker network
- **Redis Access**: Optional Redis connection for caching

## 📈 Monitoring & Observability

### Health Checks

```bash
# Service health
curl http://localhost:8080/health

# Discovery metrics
curl http://localhost:8080/metrics
```

### Logging

Structured JSON logging with correlation IDs:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "info",
  "logger": "api_debug_service",
  "message": "Discovered 15 services",
  "service_count": 15,
  "healthy_count": 13
}
```

### Metrics

- Service discovery success rate
- Cache hit/miss ratios
- Endpoint discovery methods used
- Container health status distribution

## 🔧 Configuration

### Service Discovery Config

```python
class ServiceDiscoveryConfig:
    docker_network: str = "reqarchitect-network"
    service_label: str = "reqarchitect-service=true"
    cache_ttl_seconds: int = 300  # 5 minutes
    health_check_timeout: int = 5
    endpoint_discovery_timeout: int = 10
    max_retries: int = 3
```

### Cache Configuration

```python
# Redis configuration
REDIS_URL = "redis://localhost:6379"
CACHE_TTL_SECONDS = 300

# Cache keys
api_debug:all_services
api_debug:service:{service_name}
api_debug:health_summary
```

## 🐳 Docker Integration

### Container Requirements

```dockerfile
# Access to Docker socket
-v /var/run/docker.sock:/var/run/docker.sock

# Network access
--network reqarchitect-network

# Redis connection (optional)
-e REDIS_URL=redis://redis:6379
```

### Service Labels

Containers should be labeled for discovery:

```yaml
labels:
  reqarchitect-service: "true"
  service.type: "microservice"
  service.layer: "application"
```

## 🚨 Error Handling

### Common Issues

1. **Docker Access Denied**
   ```
   Error: Permission denied accessing Docker socket
   Solution: Ensure proper Docker socket permissions
   ```

2. **Network Not Found**
   ```
   Error: Network reqarchitect-network not found
   Solution: Create network or update configuration
   ```

3. **Redis Connection Failed**
   ```
   Warning: Redis not available, caching disabled
   Solution: Start Redis or check connection
   ```

### Recovery Strategies

- **Graceful Degradation**: Service continues without cache if Redis unavailable
- **Retry Logic**: Automatic retries for transient failures
- **Fallback Discovery**: Multiple endpoint discovery methods
- **Error Logging**: Comprehensive error tracking and reporting

## 🔄 Cache Management

### Cache Invalidation

```bash
# Force refresh all cached data
curl -X POST http://localhost:8080/api-debug/refresh

# View cache statistics
curl http://localhost:8080/api-debug/stats
```

### Cache Keys

- `api_debug:all_services` - All service data
- `api_debug:service:{name}` - Individual service data
- `api_debug:health_summary` - Health summary data

## 📚 API Documentation

- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`
- **OpenAPI JSON**: `http://localhost:8080/openapi.json`

## 🤝 Integration

### With ReqArchitect Platform

The service integrates seamlessly with the ReqArchitect platform:

- **Gateway Service**: Can be used by gateway for service discovery
- **Monitoring**: Provides data for monitoring dashboards
- **Architecture Validation**: Supports validation service with endpoint data
- **Admin Service**: Can be used by admin service for service management

### With External Tools

- **Prometheus**: Metrics endpoint for monitoring
- **Grafana**: Dashboard data source
- **ELK Stack**: Structured logging support
- **Kubernetes**: Can run in K8s with proper RBAC

## 🧪 Testing

### Manual Testing

```bash
# Test service discovery
curl http://localhost:8080/api-debug

# Test specific service
curl http://localhost:8080/api-debug/goal_service

# Test health summary
curl http://localhost:8080/api-debug/health-summary

# Test cache refresh
curl -X POST http://localhost:8080/api-debug/refresh
```

### Automated Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=app tests/
```

## 📝 Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Run with Docker
docker-compose up -d
```

### Adding New Services

1. Update `known_endpoints` in `endpoint_discovery.py`
2. Add service patterns to discovery logic
3. Test with actual service container
4. Update documentation

## 📄 License

This service is part of the ReqArchitect platform and follows the same licensing terms.

## 🤝 Contributing

1. Follow ReqArchitect coding standards
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Ensure non-intrusive design principles
5. Test with actual Docker containers 