# ReqArchitect Monitoring & Observability

This document describes the monitoring and observability features implemented across the ReqArchitect microservices architecture.

## 🎯 Overview

The monitoring system provides:
- **Real-time health monitoring** of all services
- **Centralized dashboard** for service status visualization
- **Prometheus-compatible metrics** for each service
- **Environment validation** and configuration management
- **Comprehensive logging** and error tracking

## 📊 Monitoring Dashboard Service

### Service Details
- **Service Name**: `monitoring_dashboard_service`
- **Port**: 8012
- **URL**: http://localhost:8012
- **Health Endpoint**: http://localhost:8012/health
- **Metrics Endpoint**: http://localhost:8012/metrics

### Features
- **Real-time service monitoring** with auto-refresh every 30 seconds
- **Service status visualization** with color-coded health indicators
- **Response time tracking** for each service
- **Error reporting** with detailed error messages
- **Summary statistics** (total, healthy, unhealthy services)

### Dashboard Endpoints
```bash
# Main dashboard
GET /

# Service status API
GET /api/status

# Trigger health check
POST /api/check

# Health check
GET /health

# Metrics (Prometheus format)
GET /metrics
```

## 🔍 Service Health Endpoints

All services now expose enhanced health endpoints with detailed information:

### Standard Health Response Format
```json
{
  "status": "healthy",
  "service": "service_name",
  "timestamp": "2024-01-01T12:00:00Z",
  "uptime": 3600.5,
  "version": "1.0.0",
  "environment": "development",
  "database_connected": true
}
```

### Service-Specific Health Endpoints

| Service | Port | Health URL | Metrics URL |
|---------|------|------------|-------------|
| Gateway Service | 8080 | `/health` | `/metrics` |
| Auth Service | 8001 | `/health` | `/metrics` |
| AI Modeling Service | 8002 | `/health` | `/metrics` |
| Usage Service | 8000 | `/health` | `/metrics` |
| Billing Service | 8010 | `/health` | `/metrics` |
| Invoice Service | 8011 | `/health` | `/metrics` |
| Notification Service | 8000 | `/health` | `/metrics` |
| Monitoring Dashboard | 8012 | `/health` | `/metrics` |

### Health Check Examples

```bash
# Check gateway service health
curl http://localhost:8080/health

# Check auth service health
curl http://localhost:8001/health

# Check monitoring dashboard health
curl http://localhost:8012/health
```

## 📈 Metrics Endpoints

Each service exposes Prometheus-compatible metrics:

### Gateway Service Metrics
```json
{
  "gateway_uptime_seconds": 3600.5,
  "gateway_requests_total": 1250,
  "gateway_errors_total": 5,
  "gateway_active_connections": 12
}
```

### Auth Service Metrics
```json
{
  "auth_uptime_seconds": 3600.5,
  "auth_logins_total": 150,
  "auth_logouts_total": 120,
  "auth_tokens_issued": 150,
  "auth_tokens_revoked": 5
}
```

### AI Modeling Service Metrics
```json
{
  "ai_modeling_uptime_seconds": 3600.5,
  "ai_modeling_requests_total": 75,
  "ai_modeling_generations_total": 75,
  "ai_modeling_feedback_total": 25
}
```

### Usage Service Metrics
```json
{
  "usage_uptime_seconds": 3600.5,
  "usage_requests_total": 200,
  "usage_metrics_fetched": 180,
  "usage_audit_events": 200
}
```

### Billing Service Metrics
```json
{
  "billing_uptime_seconds": 3600.5,
  "billing_requests_total": 50,
  "billing_upgrades_total": 3,
  "billing_alerts_triggered": 1
}
```

### Invoice Service Metrics
```json
{
  "invoice_uptime_seconds": 3600.5,
  "invoice_requests_total": 30,
  "invoice_generated_total": 25,
  "invoice_paid_total": 20
}
```

### Notification Service Metrics
```json
{
  "notification_uptime_seconds": 3600.5,
  "notification_requests_total": 100,
  "notification_sent_total": 95,
  "notification_delivered_total": 90
}
```

## 🔧 Environment Management

### Environment Validation

The system includes a shared environment validation utility (`shared/env_validator.py`) that:

- **Validates required environment variables** for each service
- **Provides default values** for optional configurations
- **Validates data types** (ports, URLs, booleans)
- **Generates environment summaries** for debugging

### Environment Configuration

#### Common Environment Variables
```bash
# Service Identification
SERVICE_NAME=service_name_here
SERVICE_PORT=8000

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
SECRET_KEY=your-super-secret-key-change-this-in-production

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/database_name

# Logging Configuration
LOG_LEVEL=INFO
ENVIRONMENT=development
DEBUG=false

# CORS Configuration
CORS_ORIGINS=*

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100

# Request Timeout
REQUEST_TIMEOUT=30

# Health Check Configuration
HEALTH_CHECK_INTERVAL=30

# Database Pool Configuration
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=
REDIS_DB=0
```

#### Service-Specific Environment Variables

##### Gateway Service
```bash
GATEWAY_PORT=8080
AUTH_SERVICE_URL=http://auth_service:8001
AI_MODELING_SERVICE_URL=http://ai_modeling_service:8002
USAGE_SERVICE_URL=http://usage_service:8000
BILLING_SERVICE_URL=http://billing_service:8010
INVOICE_SERVICE_URL=http://invoice_service:8011
NOTIFICATION_SERVICE_URL=http://notification_service:8000
```

##### Auth Service
```bash
AUTH_PORT=8001
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

##### AI Modeling Service
```bash
AI_MODELING_PORT=8002
OPENAI_API_KEY=your-openai-api-key-here
MODEL_NAME=gpt-4
```

##### Usage Service
```bash
USAGE_PORT=8000
USAGE_DB_NAME=usage
```

##### Billing Service
```bash
BILLING_PORT=8010
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
```

##### Invoice Service
```bash
INVOICE_PORT=8011
INVOICE_DB_NAME=invoice
PDF_STORAGE_PATH=/app/invoices
```

##### Notification Service
```bash
NOTIFICATION_PORT=8000
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

##### Monitoring Dashboard Service
```bash
MONITORING_PORT=8012
DASHBOARD_REFRESH_INTERVAL=30
```

## 🚀 Getting Started

### 1. Start All Services
```bash
# Start all services including monitoring dashboard
docker-compose up -d

# Check service status
docker-compose ps
```

### 2. Access Monitoring Dashboard
```bash
# Open in browser
http://localhost:8012

# Or check via curl
curl http://localhost:8012/health
```

### 3. Check Individual Service Health
```bash
# Gateway service
curl http://localhost:8080/health

# Auth service
curl http://localhost:8001/health

# AI Modeling service
curl http://localhost:8002/health

# Usage service (internal)
curl http://usage_service:8000/health

# Billing service
curl http://localhost:8010/health

# Invoice service
curl http://localhost:8011/health

# Notification service (internal)
curl http://notification_service:8000/health
```

### 4. View Metrics
```bash
# Gateway metrics
curl http://localhost:8080/metrics

# Auth metrics
curl http://localhost:8001/metrics

# Monitoring dashboard metrics
curl http://localhost:8012/metrics
```

## 🔄 Auto-Refresh Features

### Dashboard Auto-Refresh
- **Automatic refresh** every 30 seconds
- **Manual refresh** button available
- **Real-time status updates** without page reload
- **Loading indicators** during health checks

### Health Check Intervals
- **Docker health checks**: Every 30 seconds
- **Dashboard polling**: Every 30 seconds
- **Service startup**: Initial health check on startup
- **Background tasks**: Async health checks triggered by dashboard

## 🛠️ Troubleshooting

### Common Issues

#### 1. Service Not Responding
```bash
# Check if service is running
docker-compose ps

# Check service logs
docker-compose logs service_name

# Check health endpoint directly
curl http://localhost:PORT/health
```

#### 2. Database Connection Issues
```bash
# Check database service
docker-compose logs db

# Verify database URL in environment
echo $DATABASE_URL

# Test database connection
docker-compose exec service_name python -c "
from app.database import SessionLocal
db = SessionLocal()
db.execute('SELECT 1')
print('Database connection OK')
"
```

#### 3. Monitoring Dashboard Issues
```bash
# Check monitoring service logs
docker-compose logs monitoring_dashboard_service

# Verify service URLs are correct
docker-compose exec monitoring_dashboard_service python -c "
import aiohttp
import asyncio

async def test_services():
    services = {
        'gateway_service': 'http://gateway_service:8080',
        'auth_service': 'http://auth_service:8001'
    }
    for name, url in services.items():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{url}/health') as resp:
                    print(f'{name}: {resp.status}')
        except Exception as e:
            print(f'{name}: ERROR - {e}')

asyncio.run(test_services())
"
```

### Debug Mode

Enable debug mode for detailed logging:

```bash
# Set debug environment variable
export DEBUG=true
export LOG_LEVEL=DEBUG

# Restart services
docker-compose restart
```

## 📊 Prometheus Integration

### Metrics Format
All metrics endpoints return JSON in a format that can be easily converted to Prometheus format:

```bash
# Example: Convert JSON metrics to Prometheus format
curl http://localhost:8080/metrics | jq -r 'to_entries[] | "\(.key) \(.value)"'
```

### Prometheus Configuration
Add to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'reqarchitect-gateway'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: '/metrics'
    
  - job_name: 'reqarchitect-auth'
    static_configs:
      - targets: ['localhost:8001']
    metrics_path: '/metrics'
    
  - job_name: 'reqarchitect-ai-modeling'
    static_configs:
      - targets: ['localhost:8002']
    metrics_path: '/metrics'
    
  - job_name: 'reqarchitect-billing'
    static_configs:
      - targets: ['localhost:8010']
    metrics_path: '/metrics'
    
  - job_name: 'reqarchitect-invoice'
    static_configs:
      - targets: ['localhost:8011']
    metrics_path: '/metrics'
    
  - job_name: 'reqarchitect-monitoring'
    static_configs:
      - targets: ['localhost:8012']
    metrics_path: '/metrics'
```

## 🔐 Security Considerations

### Environment Variables
- **Never commit `.env` files** to version control
- **Use strong secrets** in production
- **Rotate secrets regularly**
- **Use environment-specific configurations**

### Health Endpoints
- **Health endpoints are public** for monitoring
- **Metrics endpoints** may contain sensitive information
- **Consider authentication** for metrics in production
- **Use HTTPS** in production environments

### Monitoring Dashboard
- **Dashboard is accessible** on port 8012
- **Consider authentication** for production use
- **Limit access** to authorized personnel
- **Monitor dashboard access** logs

## 📈 Performance Considerations

### Health Check Optimization
- **5-second timeout** for health checks
- **Concurrent health checks** for multiple services
- **Cached results** to reduce load
- **Background processing** for health checks

### Metrics Collection
- **Lightweight metrics** to minimize overhead
- **In-memory counters** for performance
- **Periodic aggregation** for historical data
- **Configurable collection intervals**

### Dashboard Performance
- **Client-side caching** for static assets
- **Efficient DOM updates** for real-time data
- **Responsive design** for mobile access
- **Optimized API calls** with proper headers

## 🔮 Future Enhancements

### Planned Features
1. **Alerting system** with email/Slack notifications
2. **Historical metrics** storage and visualization
3. **Service dependency mapping**
4. **Performance trend analysis**
5. **Automated incident response**
6. **Custom dashboard widgets**
7. **Multi-environment monitoring**
8. **Integration with external monitoring tools**

### Advanced Metrics
1. **Request latency percentiles**
2. **Error rate tracking**
3. **Resource utilization metrics**
4. **Business metrics integration**
5. **Custom service metrics**
6. **Distributed tracing support**

## 📞 Support

For monitoring and observability issues:

1. **Check service logs**: `docker-compose logs service_name`
2. **Verify health endpoints**: `curl http://localhost:PORT/health`
3. **Check environment variables**: `docker-compose exec service_name env`
4. **Review monitoring dashboard**: http://localhost:8012
5. **Validate configuration**: Use the shared environment validator

## 📝 Changelog

### Version 1.0.0
- ✅ Enhanced health endpoints for all services
- ✅ Monitoring dashboard service implementation
- ✅ Prometheus-compatible metrics endpoints
- ✅ Environment validation utility
- ✅ Real-time service status monitoring
- ✅ Comprehensive documentation 