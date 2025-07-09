# Platform Status Endpoint Documentation

## Overview

The `/platform/status` endpoint in the monitoring_dashboard_service provides a comprehensive aggregation of health status from all ReqArchitect microservices. This endpoint is designed for observability, monitoring dashboards, and CI/CD integration.

## Endpoint Details

- **URL**: `GET /platform/status`
- **Service**: `monitoring_dashboard_service` (port 8012)
- **Purpose**: Aggregate health status from all microservices
- **Cache Duration**: 15 seconds
- **Timeout**: 5 seconds per service

## Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `critical_only` | boolean | `false` | Return only critical services |
| `include_metrics` | boolean | `true` | Include detailed metrics from services |
| `force_refresh` | boolean | `false` | Force refresh cache (bypass 15s cache) |

## Response Structure

```json
{
  "timestamp": "2025-01-09T16:00:00.000Z",
  "environment": "development",
  "cache_info": {
    "last_update": "2025-01-09T16:00:00.000Z",
    "cache_valid": true,
    "cache_duration_seconds": 15
  },
  "summary": {
    "total_services": 9,
    "healthy_services": 7,
    "unhealthy_services": 2,
    "critical_services": 3,
    "healthy_critical_services": 3,
    "success_rate": 77.78,
    "critical_success_rate": 100.0,
    "overall_status": "degraded"
  },
  "services": {
    "auth_service": {
      "status": "healthy",
      "response_time_ms": 45.2,
      "last_check": "2025-01-09T16:00:00.000Z",
      "critical": true,
      "success_rate": "100%",
      "uptime": "99.9%",
      "uptime_seconds": 86400
    },
    "ai_modeling_service": {
      "status": "degraded",
      "response_time_ms": 1200.5,
      "last_check": "2025-01-09T16:00:00.000Z",
      "critical": true,
      "success_rate": "50-80%",
      "error": "High response time"
    },
    "gateway_service": {
      "status": "healthy",
      "response_time_ms": 23.1,
      "last_check": "2025-01-09T16:00:00.000Z",
      "critical": true,
      "success_rate": "100%"
    }
  }
}
```

## Service Status Values

| Status | Description | Success Rate |
|--------|-------------|--------------|
| `healthy` | Service responding normally | 100% |
| `degraded` | Service responding but with issues | 50-80% |
| `unhealthy` | Service not responding properly | 0% |
| `timeout` | Service request timed out | 0% |
| `unknown` | Service unreachable | 0% |

## Critical Services

The following services are marked as critical and will cause build failures if unhealthy:

- **auth_service** (port 8001)
- **gateway_service** (port 8080)  
- **ai_modeling_service** (port 8002)

## Usage Examples

### Basic Platform Status

```bash
curl http://localhost:8012/platform/status
```

### Critical Services Only

```bash
curl "http://localhost:8012/platform/status?critical_only=true"
```

### Force Cache Refresh

```bash
curl "http://localhost:8012/platform/status?force_refresh=true"
```

### Without Detailed Metrics

```bash
curl "http://localhost:8012/platform/status?include_metrics=false"
```

### Combined Parameters

```bash
curl "http://localhost:8012/platform/status?critical_only=true&force_refresh=true"
```

## Python Integration

```python
import requests

def get_platform_status(critical_only=False, include_metrics=True, force_refresh=False):
    """Get platform status from monitoring dashboard"""
    url = "http://localhost:8012/platform/status"
    params = {
        "critical_only": critical_only,
        "include_metrics": include_metrics,
        "force_refresh": force_refresh
    }
    
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    
    return response.json()

# Usage examples
status = get_platform_status()
critical_status = get_platform_status(critical_only=True)
fresh_status = get_platform_status(force_refresh=True)
```

## JavaScript/Node.js Integration

```javascript
async function getPlatformStatus(options = {}) {
    const {
        criticalOnly = false,
        includeMetrics = true,
        forceRefresh = false
    } = options;
    
    const params = new URLSearchParams({
        critical_only: criticalOnly,
        include_metrics: includeMetrics,
        force_refresh: forceRefresh
    });
    
    const response = await fetch(`http://localhost:8012/platform/status?${params}`);
    
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
}

// Usage examples
const status = await getPlatformStatus();
const criticalStatus = await getPlatformStatus({ criticalOnly: true });
const freshStatus = await getPlatformStatus({ forceRefresh: true });
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Check Platform Status
  run: |
    curl -f http://localhost:8012/platform/status > platform_status.json
    jq '.summary.overall_status' platform_status.json
    
    # Fail if critical services are unhealthy
    if [ "$(jq -r '.summary.critical_success_rate' platform_status.json)" != "100" ]; then
      echo "Critical services unhealthy"
      exit 1
    fi
```

### GitLab CI

```yaml
check_platform_status:
  script:
    - curl -f http://localhost:8012/platform/status > platform_status.json
    - |
      if [ "$(jq -r '.summary.overall_status' platform_status.json)" != "healthy" ]; then
        echo "Platform status is not healthy"
        exit 1
      fi
```

### Jenkins Pipeline

```groovy
stage('Check Platform Status') {
    steps {
        script {
            def response = httpRequest(
                url: 'http://localhost:8012/platform/status',
                validResponseCodes: '200'
            )
            
            def status = readJSON text: response.content
            
            if (status.summary.overall_status != 'healthy') {
                error "Platform status is ${status.summary.overall_status}"
            }
        }
    }
}
```

## Monitoring and Alerting

### Prometheus Metrics

The endpoint provides metrics that can be scraped by Prometheus:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'reqarchitect-platform'
    static_configs:
      - targets: ['localhost:8012']
    metrics_path: '/platform/status'
    scrape_interval: 30s
```

### Grafana Dashboard

Create a Grafana dashboard using the platform status metrics:

```json
{
  "dashboard": {
    "title": "ReqArchitect Platform Status",
    "panels": [
      {
        "title": "Overall Success Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "reqarchitect_platform_success_rate",
            "legendFormat": "Success Rate"
          }
        ]
      },
      {
        "title": "Critical Services Health",
        "type": "stat",
        "targets": [
          {
            "expr": "reqarchitect_critical_success_rate",
            "legendFormat": "Critical Success Rate"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules

```yaml
# alertmanager.yml
groups:
  - name: reqarchitect-platform
    rules:
      - alert: PlatformDegraded
        expr: reqarchitect_platform_success_rate < 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Platform success rate is {{ $value }}%"
      
      - alert: CriticalServicesDown
        expr: reqarchitect_critical_success_rate < 100
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Critical services are unhealthy"
```

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 500 | Internal server error |
| 503 | Service unavailable |

### Error Response Format

```json
{
  "error": "Service unavailable",
  "timestamp": "2025-01-09T16:00:00.000Z",
  "details": "Failed to check service health"
}
```

## Performance Considerations

### Caching Strategy

- **Cache Duration**: 15 seconds
- **Cache Invalidation**: Automatic after 15 seconds or manual via `force_refresh=true`
- **Concurrent Requests**: Multiple requests within cache window use cached data

### Timeout Handling

- **Per Service**: 5 seconds timeout
- **Overall Request**: 30 seconds timeout
- **Graceful Degradation**: Unreachable services marked as "unknown"

### Resource Usage

- **Memory**: ~1MB per cached response
- **CPU**: Minimal impact during cache hits
- **Network**: Only during cache refresh

## Security Considerations

### Access Control

```python
# Example with authentication
@app.get("/platform/status")
async def get_platform_status(
    current_user: User = Depends(get_current_user),
    critical_only: bool = Query(False),
    include_metrics: bool = Query(True),
    force_refresh: bool = Query(False)
):
    # Check user permissions
    if not current_user.has_permission("monitoring:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # ... rest of implementation
```

### Rate Limiting

```python
# Example with rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/platform/status")
@limiter.limit("10/minute")
async def get_platform_status(request: Request, ...):
    # ... implementation
```

## Troubleshooting

### Common Issues

1. **Service Unreachable**
   ```bash
   # Check if monitoring service is running
   curl http://localhost:8012/health
   
   # Check Docker containers
   docker-compose ps
   ```

2. **Slow Response Times**
   ```bash
   # Check individual service health
   curl http://localhost:8001/health  # auth_service
   curl http://localhost:8080/health  # gateway_service
   ```

3. **Cache Issues**
   ```bash
   # Force refresh cache
   curl "http://localhost:8012/platform/status?force_refresh=true"
   ```

### Debug Mode

Enable debug logging by setting environment variable:

```bash
export LOG_LEVEL=DEBUG
```

### Health Check Endpoint

```bash
# Check monitoring service health
curl http://localhost:8012/health

# Expected response
{
  "status": "healthy",
  "service": "monitoring_dashboard",
  "timestamp": "2025-01-09T16:00:00.000Z",
  "uptime": 86400.0
}
```

## API Versioning

The endpoint supports versioning through URL path:

```bash
# Current version (v1)
curl http://localhost:8012/platform/status

# Future version
curl http://localhost:8012/v2/platform/status
```

## Migration Guide

### From Legacy Endpoints

If migrating from existing monitoring endpoints:

```python
# Old way
response = requests.get("http://localhost:8012/api/status")

# New way
response = requests.get("http://localhost:8012/platform/status")
```

### Backward Compatibility

The old `/api/status` endpoint is maintained for backward compatibility but `/platform/status` is recommended for new integrations.

## Contributing

To extend the platform status endpoint:

1. Add new services to `SERVICES` configuration
2. Update critical service list if needed
3. Add new metrics collection if required
4. Update tests in `test_platform_status.py`
5. Update documentation

## Support

For issues with the platform status endpoint:

1. Check service logs: `docker-compose logs monitoring_dashboard_service`
2. Verify all services are running: `docker-compose ps`
3. Test individual service health endpoints
4. Check network connectivity between services 