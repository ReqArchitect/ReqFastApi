# ReqArchitect Monitoring & Observability Setup

This README provides a quick start guide for the monitoring and observability features in the ReqArchitect microservices architecture.

## 🚀 Quick Start

### 1. Start All Services
```bash
# Start all services including the monitoring dashboard
docker-compose up -d

# Check that all services are running
docker-compose ps
```

### 2. Access the Monitoring Dashboard
Open your browser and navigate to:
```
http://localhost:8012
```

You should see a beautiful dashboard showing the real-time status of all services.

### 3. Test the Setup
Run the monitoring test script:
```bash
python test_monitoring.py
```

## 📊 What's Included

### ✅ Enhanced Health Endpoints
All services now have detailed health endpoints:
- **Service status** (healthy/unhealthy)
- **Uptime tracking**
- **Database connectivity checks**
- **Environment information**
- **Version information**

### ✅ Metrics Endpoints
Each service exposes Prometheus-compatible metrics:
- **Request counts**
- **Error rates**
- **Service-specific metrics**
- **Performance indicators**

### ✅ Monitoring Dashboard Service
A new service that provides:
- **Real-time service monitoring**
- **Beautiful web interface**
- **Auto-refresh every 30 seconds**
- **Response time tracking**
- **Error reporting**

### ✅ Environment Management
Comprehensive environment validation:
- **Required variable validation**
- **Default value management**
- **Service-specific configurations**
- **Production-ready security**

## 🔍 Service Health Check Examples

### Gateway Service
```bash
curl http://localhost:8080/health
```
Response:
```json
{
  "status": "healthy",
  "service": "gateway_service",
  "timestamp": "2024-01-01T12:00:00Z",
  "uptime": 3600.5,
  "version": "1.0.0",
  "environment": "development"
}
```

### Auth Service
```bash
curl http://localhost:8001/health
```
Response:
```json
{
  "status": "healthy",
  "service": "auth_service",
  "timestamp": "2024-01-01T12:00:00Z",
  "uptime": 3600.5,
  "version": "1.0.0",
  "environment": "development",
  "database_connected": true
}
```

### Monitoring Dashboard
```bash
curl http://localhost:8012/health
```
Response:
```json
{
  "status": "healthy",
  "service": "monitoring_dashboard",
  "timestamp": "2024-01-01T12:00:00Z",
  "uptime": 3600.5
}
```

## 📈 Metrics Examples

### Gateway Metrics
```bash
curl http://localhost:8080/metrics
```
Response:
```json
{
  "gateway_uptime_seconds": 3600.5,
  "gateway_requests_total": 1250,
  "gateway_errors_total": 5,
  "gateway_active_connections": 12
}
```

### Auth Metrics
```bash
curl http://localhost:8001/metrics
```
Response:
```json
{
  "auth_uptime_seconds": 3600.5,
  "auth_logins_total": 150,
  "auth_logouts_total": 120,
  "auth_tokens_issued": 150,
  "auth_tokens_revoked": 5
}
```

## 🖥️ Dashboard Features

### Real-Time Monitoring
- **Auto-refresh** every 30 seconds
- **Color-coded status** indicators
- **Response time** tracking
- **Error details** for failed services

### Service Overview
- **Total services** count
- **Healthy services** count
- **Unhealthy services** count
- **Last update** timestamp

### Individual Service Cards
Each service shows:
- **Service name** and status
- **URL** and port information
- **Response time** in milliseconds
- **Last check** timestamp
- **Error messages** (if any)

## 🔧 Environment Configuration

### Using the Environment Template
1. Copy the environment template:
```bash
cp env.example .env
```

2. Edit the `.env` file with your specific values:
```bash
# Edit with your preferred editor
nano .env
```

3. The template includes sections for:
- **Common configuration** (used by all services)
- **Service-specific configuration** (commented out by default)
- **Production overrides** (for production environments)

### Environment Validation
The system includes automatic environment validation:
- **Missing required variables** are detected at startup
- **Default values** are provided for optional settings
- **Data type validation** for ports, URLs, and booleans
- **Service-specific validation** rules

## 🧪 Testing

### Run the Test Suite
```bash
# Test all monitoring features
python test_monitoring.py
```

### Manual Testing
```bash
# Test individual service health
curl http://localhost:8080/health  # Gateway
curl http://localhost:8001/health  # Auth
curl http://localhost:8002/health  # AI Modeling
curl http://localhost:8010/health  # Billing
curl http://localhost:8011/health  # Invoice
curl http://localhost:8012/health  # Monitoring Dashboard

# Test metrics endpoints
curl http://localhost:8080/metrics
curl http://localhost:8012/metrics

# Test dashboard API
curl http://localhost:8012/api/status
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Services Not Starting
```bash
# Check Docker logs
docker-compose logs

# Check specific service logs
docker-compose logs gateway_service
docker-compose logs monitoring_dashboard_service
```

#### 2. Health Endpoints Not Responding
```bash
# Check if services are running
docker-compose ps

# Check service health directly
docker-compose exec gateway_service curl http://localhost:8080/health
```

#### 3. Dashboard Not Accessible
```bash
# Check if monitoring service is running
docker-compose ps monitoring_dashboard_service

# Check monitoring service logs
docker-compose logs monitoring_dashboard_service

# Verify port 8012 is not in use
netstat -tulpn | grep 8012
```

#### 4. Environment Issues
```bash
# Check environment variables
docker-compose exec gateway_service env | grep SERVICE

# Validate environment configuration
docker-compose exec gateway_service python -c "
from shared.env_validator import validate_env
try:
    config = validate_env('gateway_service')
    print('Environment validation passed')
except Exception as e:
    print(f'Environment validation failed: {e}')
"
```

### Debug Mode
Enable debug mode for detailed logging:
```bash
# Set debug environment variables
export DEBUG=true
export LOG_LEVEL=DEBUG

# Restart services
docker-compose restart
```

## 📊 Prometheus Integration

### Basic Prometheus Configuration
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
    
  - job_name: 'reqarchitect-monitoring'
    static_configs:
      - targets: ['localhost:8012']
    metrics_path: '/metrics'
```

### Convert JSON Metrics to Prometheus Format
```bash
# Example: Convert gateway metrics
curl http://localhost:8080/metrics | jq -r 'to_entries[] | "\(.key) \(.value)"'
```

## 🔐 Security Considerations

### Production Deployment
1. **Change default secrets** in the `.env` file
2. **Use HTTPS** for all endpoints
3. **Implement authentication** for the monitoring dashboard
4. **Restrict access** to monitoring endpoints
5. **Use environment-specific** configurations

### Environment Variables
- **Never commit** `.env` files to version control
- **Use strong secrets** for JWT and database passwords
- **Rotate secrets** regularly
- **Use different secrets** for each environment

## 📈 Performance Considerations

### Health Check Optimization
- **5-second timeout** for health checks
- **Concurrent health checks** for multiple services
- **Cached results** to reduce load
- **Background processing** for health checks

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

### Advanced Metrics
1. **Request latency percentiles**
2. **Error rate tracking**
3. **Resource utilization metrics**
4. **Business metrics integration**
5. **Distributed tracing support**

## 📞 Support

For monitoring and observability issues:

1. **Check service logs**: `docker-compose logs service_name`
2. **Verify health endpoints**: `curl http://localhost:PORT/health`
3. **Check environment variables**: `docker-compose exec service_name env`
4. **Review monitoring dashboard**: http://localhost:8012
5. **Run the test suite**: `python test_monitoring.py`

## 📝 Files Overview

### New Files Created
- `services/monitoring_dashboard_service/` - Monitoring dashboard service
- `shared/env_validator.py` - Environment validation utility
- `env.example` - Environment configuration template
- `test_monitoring.py` - Monitoring test suite
- `MONITORING_OBSERVABILITY.md` - Comprehensive documentation

### Modified Files
- `docker-compose.yml` - Added monitoring dashboard service
- All service `main.py` files - Enhanced health and metrics endpoints
- All service `requirements.txt` files - Added necessary dependencies

## 🎉 Success Indicators

You'll know the monitoring system is working correctly when:

1. ✅ **Dashboard accessible** at http://localhost:8012
2. ✅ **All services show as healthy** in the dashboard
3. ✅ **Health endpoints return 200** status codes
4. ✅ **Metrics endpoints return JSON** data
5. ✅ **Test suite passes** with >90% success rate
6. ✅ **Auto-refresh works** every 30 seconds
7. ✅ **Response times are reasonable** (<1000ms)

## 🚀 Next Steps

1. **Customize environment** variables for your setup
2. **Integrate with Prometheus** for metrics collection
3. **Set up Grafana** for advanced visualization
4. **Configure alerting** for production use
5. **Add custom metrics** specific to your business needs
6. **Implement authentication** for the monitoring dashboard 