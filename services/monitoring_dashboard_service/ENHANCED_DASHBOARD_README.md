# Enhanced Monitoring Dashboard Service

## Overview

The Enhanced Monitoring Dashboard Service provides real-time monitoring, alerting, and visualization for the ReqArchitect platform's microservices. It includes an internal alert dispatcher, a lightweight React frontend panel, and comprehensive audit logging.

## Features

### 1. Internal Alert Dispatcher

The alert dispatcher continuously monitors platform status and automatically sends alerts when critical services show degraded or unknown status.

#### Key Features:
- **Automatic Monitoring**: Runs every 60 seconds to check platform status
- **Smart Alerting**: Only alerts for critical services with degraded/unknown status
- **Cooldown Protection**: Prevents alert spam with 5-minute cooldown per service
- **Notification Integration**: Sends formatted alerts to the notification service
- **Error Handling**: Graceful handling of network failures and service unavailability

#### Alert Payload Structure:
```json
{
  "tenant_id": "system-monitoring",
  "user_id": "monitoring-system",
  "type": "email",
  "subject": "🚨 Critical Service Alert: {service_name}",
  "message": "Formatted alert message with service details",
  "recipient": "ops@reqarchitect.com",
  "priority": "high",
  "metadata": {
    "service_name": "auth_service",
    "status": "degraded",
    "critical": true,
    "environment": "production",
    "response_time_ms": 3000
  }
}
```

#### Configuration:
- **Notification Service URL**: `http://notification_service:8006`
- **Alert Cooldown**: 300 seconds (5 minutes)
- **Monitoring Interval**: 60 seconds
- **Critical Services**: auth_service, gateway_service, ai_modeling_service

### 2. Lightweight Frontend Panel

A modern React-based dashboard with real-time service status visualization.

#### Features:
- **Live Status Cards**: Color-coded service status with detailed information
- **Auto-refresh**: Updates every 15 seconds automatically
- **Critical Services Filter**: Toggle to show only critical services
- **Responsive Design**: Works on desktop and mobile devices
- **Error Display**: Shows detailed error information for failed services
- **Performance Metrics**: Response times, uptime, and success rates

#### Status Indicators:
- 🟢 **Healthy**: Service responding normally
- 🟡 **Degraded**: Service responding but with issues
- 🔴 **Unhealthy**: Service not responding
- ⏰ **Timeout**: Service request timed out
- ❓ **Unknown**: Service status unclear

#### Frontend Technologies:
- **React 18**: Modern component-based UI
- **Tailwind CSS**: Utility-first CSS framework
- **Babel**: JSX compilation
- **CDN Dependencies**: No build process required

### 3. Comprehensive Audit Logging

All dashboard interactions and alert activities are logged for audit trails.

#### Logged Events:
- **Panel Loads**: When users access the dashboard
- **Page Loads**: Initial page access
- **Alert Sent**: When alerts are dispatched
- **Service Checks**: Platform status checks
- **Error Events**: Failed operations

#### Log Structure:
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "event": "panel_load",
  "user_agent": "Mozilla/5.0...",
  "data": {
    "services_count": 5,
    "critical_only": false,
    "summary": {...}
  },
  "ip_address": "192.168.1.100"
}
```

## API Endpoints

### Core Monitoring Endpoints

#### `GET /platform/status`
Get aggregated platform status from all microservices.

**Query Parameters:**
- `critical_only` (bool): Return only critical services
- `include_metrics` (bool): Include detailed metrics
- `force_refresh` (bool): Force refresh cache

**Response:**
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "environment": "production",
  "cache_info": {
    "last_update": "2024-01-01T12:00:00Z",
    "cache_valid": true,
    "cache_duration_seconds": 15
  },
  "summary": {
    "total_services": 9,
    "healthy_services": 7,
    "unhealthy_services": 2,
    "critical_services": 3,
    "healthy_critical_services": 2,
    "success_rate": 77.78,
    "critical_success_rate": 66.67,
    "overall_status": "degraded"
  },
  "services": {
    "auth_service": {
      "status": "degraded",
      "response_time_ms": 2500,
      "last_check": "2024-01-01T12:00:00Z",
      "critical": true,
      "error": "Database connection failed",
      "uptime": "99.5%",
      "success_rate": "50-80%"
    }
  }
}
```

### Alert Management Endpoints

#### `POST /api/alerts/process`
Manually trigger alert processing.

**Response:**
```json
{
  "processed": true,
  "alerts_sent": 1,
  "critical_issues": [
    {
      "service": "auth_service",
      "status": "degraded",
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ],
  "total_services_checked": 9,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### `GET /api/alerts/status`
Get alert dispatcher status.

**Response:**
```json
{
  "dispatcher_active": true,
  "last_alert_times": {
    "auth_service": "2024-01-01T11:55:00Z"
  },
  "cooldown_period": 300,
  "notification_service_url": "http://notification_service:8006"
}
```

### Audit Logging Endpoints

#### `POST /api/log`
Log events for audit trail.

**Request Body:**
```json
{
  "event": "panel_load",
  "user_agent": "Mozilla/5.0...",
  "services_count": 5,
  "critical_only": false
}
```

**Response:**
```json
{
  "status": "logged",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### `GET /api/logs`
Get audit logs.

**Query Parameters:**
- `limit` (int): Number of logs to return (default: 100)
- `event_type` (str): Filter by event type

**Response:**
```json
{
  "logs": [
    {
      "timestamp": "2024-01-01T12:00:00Z",
      "event": "panel_load",
      "user_agent": "Mozilla/5.0...",
      "data": {...},
      "ip_address": "192.168.1.100"
    }
  ],
  "total_logs": 150,
  "filtered_count": 50
}
```

## Architecture

### Service Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Monitoring Dashboard                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Alert         │  │   Frontend      │  │   Audit     │ │
│  │   Dispatcher    │  │   Panel         │  │   Logging   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    Platform Services                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Gateway   │  │     Auth    │  │   AI Modeling      │ │
│  │   Service   │  │   Service   │  │   Service          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  Notification Service                       │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Service Health Checks**: Dashboard polls all services every 15 seconds
2. **Status Aggregation**: Results are cached and aggregated
3. **Alert Processing**: Dispatcher checks for critical issues every 60 seconds
4. **Frontend Updates**: React panel fetches latest status every 15 seconds
5. **Audit Logging**: All interactions are logged for compliance

## Configuration

### Environment Variables

```bash
# Service Configuration
VALIDATION_ENV=production
NOTIFICATION_SERVICE_URL=http://notification_service:8006

# Alert Configuration
ALERT_COOLDOWN_SECONDS=300
MONITORING_INTERVAL_SECONDS=60

# Cache Configuration
CACHE_DURATION_SECONDS=15

# Logging Configuration
LOG_LEVEL=INFO
AUDIT_LOG_RETENTION=1000
```

### Service Configuration

Critical services are defined in the `SERVICES` configuration:

```python
SERVICES = {
    "gateway_service": {"url": "http://gateway_service:8080", "port": 8080, "critical": True},
    "auth_service": {"url": "http://auth_service:8001", "port": 8001, "critical": True},
    "ai_modeling_service": {"url": "http://ai_modeling_service:8002", "port": 8002, "critical": True},
    # ... other services
}
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
COPY tests/ ./tests/

EXPOSE 8012

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8012"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: monitoring-dashboard
spec:
  replicas: 2
  selector:
    matchLabels:
      app: monitoring-dashboard
  template:
    metadata:
      labels:
        app: monitoring-dashboard
    spec:
      containers:
      - name: monitoring-dashboard
        image: reqarchitect/monitoring-dashboard:latest
        ports:
        - containerPort: 8012
        env:
        - name: VALIDATION_ENV
          value: "production"
        - name: NOTIFICATION_SERVICE_URL
          value: "http://notification-service:8006"
        livenessProbe:
          httpGet:
            path: /health
            port: 8012
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8012
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Monitoring and Alerting

### Health Checks

The service provides health check endpoints:

- `GET /health`: Basic health status
- `GET /metrics`: Prometheus-style metrics
- `GET /platform/status`: Comprehensive platform status

### Metrics

Key metrics exposed:

- `service_uptime_seconds`: Service uptime
- `services_total`: Total number of services
- `services_healthy`: Number of healthy services
- `services_unhealthy`: Number of unhealthy services
- `service_{name}_status`: Individual service status (0/1)
- `service_{name}_response_time_ms`: Individual service response time

### Alerting Rules

The alert dispatcher automatically triggers alerts when:

1. **Critical Service Degraded**: Any critical service shows "degraded" status
2. **Critical Service Unknown**: Any critical service shows "unknown" status
3. **Response Time Threshold**: Service response time > 1000ms
4. **Success Rate Threshold**: Overall success rate < 80%

## Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest tests/test_enhanced_dashboard.py -v

# Run specific test categories
pytest tests/test_enhanced_dashboard.py::TestAlertDispatcher -v
pytest tests/test_enhanced_dashboard.py::TestFrontendPanel -v
pytest tests/test_enhanced_dashboard.py::TestIntegration -v
```

### Test Coverage

The test suite covers:

- **Alert Dispatcher**: Payload creation, alert logic, message formatting
- **Dashboard Endpoints**: Logging, audit trails, alert management
- **Frontend Panel**: Page loading, static files, API integration
- **Integration**: Complete workflows and error handling
- **Performance**: Caching, memory management, response times

## Security Considerations

### Access Control

- **Internal Service**: Only accessible within the cluster
- **No Authentication**: Designed for internal monitoring only
- **Audit Logging**: All access is logged for compliance

### Data Protection

- **In-Memory Storage**: Audit logs stored in memory (limited retention)
- **No Sensitive Data**: Only service status and metrics
- **Error Sanitization**: Error messages don't expose internal details

### Network Security

- **Internal Network**: Only accessible from within the cluster
- **HTTPS**: Use reverse proxy for external access
- **Firewall Rules**: Restrict access to monitoring team

## Troubleshooting

### Common Issues

1. **Alert Dispatcher Not Working**
   - Check notification service connectivity
   - Verify service URLs are correct
   - Check logs for network errors

2. **Frontend Not Loading**
   - Verify static files are served correctly
   - Check browser console for JavaScript errors
   - Ensure React and dependencies load properly

3. **High Memory Usage**
   - Audit logs are capped at 1000 entries
   - Restart service if memory usage is high
   - Consider database storage for logs in production

4. **Slow Response Times**
   - Check service health check timeouts
   - Verify network connectivity between services
   - Monitor cache hit rates

### Debug Endpoints

- `GET /api/alerts/status`: Check alert dispatcher status
- `GET /api/logs`: View recent audit logs
- `GET /platform/status?force_refresh=true`: Force cache refresh

## Future Enhancements

### Planned Features

1. **Database Integration**: Store audit logs in PostgreSQL
2. **Advanced Filtering**: Service type, environment, custom filters
3. **Historical Data**: Service status history and trends
4. **Custom Dashboards**: User-configurable dashboard layouts
5. **Mobile App**: Native mobile application for monitoring
6. **WebSocket Updates**: Real-time updates via WebSocket
7. **Export Functionality**: Export status reports to PDF/CSV
8. **Integration APIs**: Webhook support for external systems

### Performance Optimizations

1. **Database Caching**: Redis for high-performance caching
2. **Service Discovery**: Dynamic service discovery
3. **Load Balancing**: Multiple dashboard instances
4. **CDN Integration**: Static file delivery via CDN
5. **Compression**: Gzip compression for API responses

## Support

For issues and questions:

1. **Check Logs**: Review application logs for errors
2. **Test Endpoints**: Verify individual endpoints work
3. **Monitor Metrics**: Check service metrics and health
4. **Contact Team**: Reach out to the monitoring team

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Maintainer**: ReqArchitect Platform Team 