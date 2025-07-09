# ReqArchitect Continuous Validation Framework

A comprehensive automated validation system for monitoring the health and functionality of all ReqArchitect microservices.

## 🎯 Features

- **Automated Health Checks**: Periodic monitoring of all service endpoints
- **JWT Authentication Support**: Automatic token generation for authenticated endpoints
- **Retry Logic**: Resilient testing with configurable retry attempts
- **Container Status Monitoring**: Docker container health tracking
- **Comprehensive Reporting**: JSON and Markdown report generation
- **Dashboard Generation**: Real-time status dashboard
- **Regression Detection**: Flag new errors and broken endpoints
- **Cross-Platform Support**: Works on Windows, Linux, and macOS

## 📋 Requirements

- Python 3.8+
- Docker Desktop
- ReqArchitect microservices running via Docker Compose

## 🚀 Quick Start

### 1. Install Dependencies

**Linux/macOS:**
```bash
chmod +x run_validation.sh
./run_validation.sh install
```

**Windows:**
```powershell
.\run_validation.ps1 install
```

### 2. Check Services

**Linux/macOS:**
```bash
./run_validation.sh check
```

**Windows:**
```powershell
.\run_validation.ps1 check
```

### 3. Run Validation

**Single Run:**
```bash
./run_validation.sh run-once
```

**Continuous Monitoring:**
```bash
./run_validation.sh scheduler
```

## 📊 Usage Examples

### Run Validation Once
```bash
# Linux/macOS
./run_validation.sh run-once

# Windows
.\run_validation.ps1 run-once
```

### Show Current Dashboard
```bash
# Linux/macOS
./run_validation.sh dashboard

# Windows
.\run_validation.ps1 dashboard
```

### Start Continuous Monitoring
```bash
# Linux/macOS
./run_validation.sh scheduler

# Windows
.\run_validation.ps1 scheduler
```

### View Recent Reports
```bash
# Linux/macOS
./run_validation.sh reports

# Windows
.\run_validation.ps1 reports
```

## ⚙️ Configuration

The framework uses `validation_config.json` for configuration:

```json
{
  "services": {
    "service_name": {
      "port": 8000,
      "endpoints": [
        {
          "path": "/health",
          "method": "GET",
          "expected_status": 200
        }
      ]
    }
  },
  "test_data": {
    "tenant_id": "test-tenant-123",
    "user_id": "test-user-456",
    "email": "test@example.com",
    "password": "testpass123"
  },
  "validation_settings": {
    "retry_attempts": 3,
    "retry_delay": 2,
    "timeout": 30,
    "check_interval_minutes": 15,
    "history_retention_days": 7
  },
  "jwt_settings": {
    "enabled": true,
    "secret": "supersecret",
    "algorithm": "HS256",
    "expiration_hours": 24
  }
}
```

## 📁 Output Structure

```
validation_outputs/
├── validation_results_20250109_160000.json
├── validation_report_20250109_160000.md
├── validation_results_20250109_161500.json
└── validation_report_20250109_161500.md
```

## 📈 Dashboard Example

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ReqArchitect Platform - Validation Dashboard              ║
║                              2025-01-09 16:00:00                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Overall Success Rate: 57.9% (22/38)                                       ║
║  Total Services: 9                                                          ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Service Health Status:                                                      ║
║                                                                              ║
║  🟢 gateway_service              100.0% uptime | 100.0% success | running  ║
║  🟡 auth_service                  60.0% uptime |  60.0% success | running  ║
║  🔴 ai_modeling_service          40.0% uptime |  40.0% success | running  ║
║  🟡 usage_service                50.0% uptime |  50.0% success | running  ║
║  🟡 notification_service         50.0% uptime |  50.0% success | running  ║
║  🟡 audit_log_service            50.0% uptime |  50.0% success | running  ║
║  🟡 billing_service              60.0% uptime |  60.0% success | running  ║
║  🟢 invoice_service             100.0% uptime | 100.0% success | running  ║
║  🟡 monitoring_dashboard_service 66.7% uptime |  66.7% success | running  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 🔧 Advanced Usage

### Direct Python Execution

```bash
# Run validation once
python continuous_validation_framework.py --run-once

# Show dashboard
python continuous_validation_framework.py --dashboard

# Start scheduler
python continuous_validation_framework.py --scheduler

# Use custom config
python continuous_validation_framework.py --config custom_config.json --run-once
```

### Custom Configuration

Create a custom configuration file:

```json
{
  "services": {
    "custom_service": {
      "port": 9000,
      "endpoints": [
        {"path": "/health", "method": "GET", "expected_status": 200}
      ]
    }
  },
  "validation_settings": {
    "check_interval_minutes": 5,
    "retry_attempts": 5
  }
}
```

## 📊 Metrics Tracked

### Service Health Metrics
- **Uptime Percentage**: Service availability over time
- **Error Rate**: Percentage of failed requests
- **API Success Ratio**: Successful API calls vs total calls
- **Average Response Time**: Mean response time in milliseconds
- **Container Status**: Docker container health status

### Validation Results
- **Total Tests**: Number of endpoints tested
- **Successful Tests**: Number of successful validations
- **Failed Tests**: Number of failed validations
- **Success Rate**: Overall validation success percentage

## 🔍 Regression Detection

The framework automatically detects:

- **New 500 Errors**: Previously working endpoints returning server errors
- **Broken Stubs**: Missing or non-functional endpoints
- **Schema Drift**: Unexpected response formats
- **Authentication Failures**: JWT token or header issues
- **Container Issues**: Docker container health problems

## 📝 Logging

Logs are written to `validation_framework.log`:

```
2025-01-09 16:00:00 - __main__ - INFO - Starting validation cycle...
2025-01-09 16:00:01 - __main__ - INFO - Validating gateway_service...
2025-01-09 16:00:01 - __main__ - INFO -   ✅ GET /health: 200 (22.2ms)
2025-01-09 16:00:01 - __main__ - INFO -   ❌ GET /metrics: 500 (13.31ms)
```

## 🛠️ Troubleshooting

### Common Issues

1. **Docker Not Running**
   ```bash
   # Start Docker Desktop
   # Then run validation
   ./run_validation.sh check
   ```

2. **Services Not Responding**
   ```bash
   # Check if services are up
   docker-compose ps
   
   # Restart services if needed
   docker-compose restart
   ```

3. **Python Dependencies Missing**
   ```bash
   # Install dependencies
   ./run_validation.sh install
   ```

4. **JWT Authentication Issues**
   - Check JWT secret in configuration
   - Verify token expiration settings
   - Ensure PyJWT is installed

### Debug Mode

Enable debug logging by modifying the Python script:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 🔄 Continuous Integration

### GitHub Actions Example

```yaml
name: Validation Framework
on:
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Start Services
        run: docker-compose up -d
      - name: Install Dependencies
        run: pip install -r validation_requirements.txt
      - name: Run Validation
        run: python continuous_validation_framework.py --run-once
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: validation-results
          path: validation_outputs/
```

## 📚 API Reference

### ValidationResult
```python
@dataclass
class ValidationResult:
    service_name: str
    endpoint: str
    method: str
    status_code: Optional[int]
    response_time: Optional[float]
    success: bool
    error_message: Optional[str]
    timestamp: str
    retry_count: int = 0
    response_body: Optional[Dict] = None
```

### ServiceHealth
```python
@dataclass
class ServiceHealth:
    service_name: str
    uptime_percentage: float
    error_rate: float
    api_success_ratio: float
    average_response_time: float
    total_requests: int
    failed_requests: int
    last_check: str
    container_status: str
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `validation_framework.log`
3. Create an issue with detailed error information
4. Include configuration and environment details 