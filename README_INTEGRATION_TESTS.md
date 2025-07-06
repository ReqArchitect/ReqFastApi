# FastAPI Microservices Integration Testing

This directory contains a comprehensive integration testing suite for the FastAPI microservices architecture, designed specifically for Windows environments.

## 📁 Files Overview

- **`integration_tests.py`** - Main Python integration test suite
- **`run_integration_tests.bat`** - Windows batch script to run tests
- **`healthcheck.ps1`** - PowerShell health check script
- **`postman_collection.json`** - Complete Postman collection for manual testing
- **`test_payloads.md`** - Detailed test payloads and expected responses

## 🚀 Quick Start (Windows)

### Prerequisites

1. **Docker Desktop** - Install and start Docker Desktop
2. **Python 3.8+** - Install Python from [python.org](https://python.org)
3. **PowerShell 5.1+** - Should be included with Windows 10/11
4. **curl** - Should be included with Windows 10/11

### Running Integration Tests

```cmd
# Run complete integration test suite
run_integration_tests.bat

# Only start services (don't run tests)
run_integration_tests.bat -s

# Only run tests (assumes services are running)
run_integration_tests.bat -t

# Show service logs after tests
run_integration_tests.bat -l

# Keep services running after tests
run_integration_tests.bat --no-cleanup
```

### Manual Health Checks

```powershell
# Run health checks using PowerShell
powershell -ExecutionPolicy Bypass -File healthcheck.ps1

# Run with verbose output
powershell -ExecutionPolicy Bypass -File healthcheck.ps1 -Verbose
```

## 🧪 Integration Test Flow

The integration test suite follows this complete user journey:

### 1. User Authentication
```python
# User signup
POST /auth/signup
{
  "email": "test-user@example.com",
  "password": "TestPassword123!",
  "tenant_id": "tenant-123",
  "user_id": "user-123",
  "role": "Admin"
}

# User login
POST /auth/login
{
  "email": "test-user@example.com",
  "password": "TestPassword123!"
}
```

### 2. AI Modeling Service
```python
# Generate AI model
POST /ai_modeling/generate
{
  "tenant_id": "tenant-123",
  "user_id": "user-123",
  "input_type": "goal",
  "input_text": "Optimize supply chain efficiency and reduce operational costs by 20%"
}
```

### 3. Usage Tracking
```python
# Log API usage
POST /usage/log
{
  "tenant_id": "tenant-123",
  "user_id": "user-123",
  "service": "ai_modeling",
  "endpoint": "/ai_modeling/generate",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 4. Invoice Generation
```python
# Generate invoice
POST /invoices/generate/{tenant_id}
{
  "tenant_id": "tenant-123",
  "amount": 99.99,
  "currency": "USD",
  "description": "AI Modeling Service - Supply Chain Optimization"
}
```

### 5. Notification Service
```python
# Send notification
POST /notifications/send
{
  "user_id": "user-123",
  "tenant_id": "tenant-123",
  "channel": "email",
  "message": "Your AI modeling request has been completed successfully!",
  "event_type": "ai_modeling_complete"
}
```

### 6. Billing Integration
```python
# Get billing profile
GET /billing/tenant/{tenant_id}
```

## 📊 Test Results

The integration test suite provides detailed reporting:

```
🚀 Starting Complete Integration Test Suite
========================================================

👤 Test user created: test-abc123@example.com
🏢 Tenant ID: tenant-abc123
🆔 User ID: user-abc123

==================== User Signup ====================
✅ User signup successful: test-abc123@example.com
✅ User Signup PASSED

==================== User Login ====================
✅ User login successful, JWT token obtained
✅ User Login PASSED

==================== AI Modeling ====================
✅ AI modeling successful: Business Process
✅ AI Modeling PASSED

==================== Usage Logging ====================
✅ Usage service accessible
✅ Usage Logging PASSED

==================== Invoice Generation ====================
✅ Invoice generated successfully: inv-abc123
✅ Invoice Generation PASSED

==================== Notification ====================
✅ Notification sent successfully: notif-abc123
✅ Notification PASSED

==================== Billing Integration ====================
✅ Billing profile retrieved successfully
✅ Billing Integration PASSED

==================== Gateway Integration ====================
✅ Gateway integration successful
✅ Gateway Integration PASSED

========================================================
INTEGRATION TEST SUMMARY
========================================================
✅ Passed: 8/8 tests
❌ Failed: 0/8 tests
📊 Success Rate: 100.0%
🎉 ALL INTEGRATION TESTS PASSED!
```

## 🔧 Service Ports

| Service | Port | External Access |
|---------|------|----------------|
| Gateway Service | 8080 | ✅ Yes |
| Auth Service | 8001 | ✅ Yes |
| AI Modeling Service | 8002 | ✅ Yes |
| Invoice Service | 8011 | ✅ Yes |
| Billing Service | 8010 | ✅ Yes |
| Usage Service | 8000 | ❌ Internal |
| Notification Service | 8000 | ❌ Internal |
| PostgreSQL | 5432 | ❌ Internal |
| Redis | 6379 | ❌ Internal |

## 📋 Health Check Endpoints

All services expose health endpoints:

```bash
# Gateway Service
curl http://localhost:8080/health

# Auth Service
curl http://localhost:8001/health

# AI Modeling Service
curl http://localhost:8002/health

# Invoice Service
curl http://localhost:8011/health

# Billing Service
curl http://localhost:8010/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "service_name",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **Docker not running**
   ```cmd
   # Start Docker Desktop manually or via command line
   start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
   ```

2. **Port conflicts**
   ```cmd
   # Check what's using a port
   netstat -ano | findstr :8080
   
   # Kill process using port
   taskkill /PID <PID> /F
   ```

3. **Python dependencies missing**
   ```cmd
   # Install required packages
   pip install requests pytest
   ```

4. **PowerShell execution policy**
   ```powershell
   # Allow script execution
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### Debug Mode

Run tests with verbose output:

```cmd
# Enable verbose logging
set VERBOSE=1
run_integration_tests.bat

# Show service logs
run_integration_tests.bat -l
```

### Manual Testing

Use the Postman collection for manual testing:

1. Import `postman_collection.json` into Postman
2. Set environment variables:
   - `base_url`: `http://localhost:8080`
   - `auth_service_url`: `http://localhost:8001`
   - `ai_modeling_url`: `http://localhost:8002`
   - `invoice_url`: `http://localhost:8011`
   - `billing_url`: `http://localhost:8010`

3. Run the "Complete User Journey" collection

## 🔄 CI/CD Integration

The integration tests can be integrated into CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Run Integration Tests
  run: |
    run_integration_tests.bat
  env:
    DOCKER_BUILDKIT: 1
```

## 📈 Performance Testing

For load testing, use the included Locust configuration:

```cmd
# Install Locust
pip install locust

# Run load test
locust -f services/architecture_suite/locustfile.py --host=http://localhost:8080
```

## 🔐 Security Testing

The integration tests include security validations:

- JWT token validation
- Authentication headers
- Authorization checks
- Input validation
- Error handling

## 📝 Logging

All services log to stdout/stderr. View logs with:

```cmd
# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs gateway_service

# Follow logs in real-time
docker-compose logs -f
```

## 🎯 Best Practices

1. **Always run health checks first**
2. **Use the Windows batch script for consistency**
3. **Check Docker Desktop is running before tests**
4. **Monitor resource usage during tests**
5. **Clean up containers after testing**
6. **Use the Postman collection for manual verification**

## 📞 Support

For issues with the integration tests:

1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Check service logs for errors
4. Ensure Docker Desktop is running
5. Verify ports are not in use by other applications

## 🔄 Updates

To update the integration test suite:

1. Update `integration_tests.py` for new test scenarios
2. Update `postman_collection.json` for new endpoints
3. Update `test_payloads.md` for new request/response formats
4. Test with `run_integration_tests.bat` before committing 