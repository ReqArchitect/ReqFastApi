# ReqArchitect Microservices Validation

This directory contains comprehensive validation tools for testing the ReqArchitect FastAPI microservices platform.

## Overview

The validation suite tests the following services:
- **auth_service** (Port 8001) - Authentication and user management
- **usage_service** (Port 8000) - Usage metrics and system health
- **billing_service** (Port 8010) - Billing profiles and subscription management
- **invoice_service** (Port 8011) - Invoice generation and management
- **notification_service** (Port 8000) - Notification delivery and templates
- **audit_log_service** (Port 8000) - Audit logging and event tracking
- **ai_modeling_service** (Port 8002) - AI-powered architecture modeling

## Prerequisites

1. **Docker** and **Docker Compose** installed and running
2. **Python 3.8+** with pip
3. **Git** (for cloning the repository)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r test_requirements.txt
```

### 2. Run Full Validation

```bash
python run_validation.py
```

This will:
- Start all services using docker-compose
- Wait for services to be ready
- Run comprehensive API tests
- Generate a detailed report
- Optionally stop services when done

### 3. Manual Testing

If you prefer to run tests manually:

```bash
# Start services
docker-compose up -d

# Wait for services to be ready, then run tests
python test_microservices.py

# Stop services when done
docker-compose down
```

## Test Coverage

### Health Checks
- ✅ Service availability
- ✅ Database connectivity
- ✅ Uptime metrics

### Authentication Service
- ✅ User login/logout
- ✅ JWT token validation
- ✅ Role-based access control
- ✅ Token refresh

### Usage Service
- ✅ Tenant usage metrics
- ✅ System health monitoring
- ✅ Audit event tracking

### Billing Service
- ✅ Billing profile management
- ✅ Subscription plans
- ✅ Usage reporting
- ✅ Plan upgrades

### Invoice Service
- ✅ Invoice generation (stub)
- ✅ Invoice listing
- ✅ Payment status updates

### Notification Service
- ✅ Notification sending
- ✅ Template management
- ✅ User notification history

### Audit Log Service
- ✅ Event logging
- ✅ Log retrieval

### AI Modeling Service
- ✅ Architecture generation
- ✅ User history tracking
- ✅ Feedback submission

## Test Data

The validation uses the following test data:

```python
TEST_DATA = {
    "tenant_id": "test-tenant-123",
    "user_id": "test-user-456", 
    "email": "test@example.com",
    "password": "testpass123",
    "role": "Admin"
}
```

## Expected Results

### Successful Validation
- All services respond to health checks
- Authentication flow works end-to-end
- API endpoints return expected status codes
- Response schemas match expectations

### Common Issues
- **Service not starting**: Check Docker logs with `docker-compose logs <service_name>`
- **Database connection errors**: Ensure PostgreSQL is running and accessible
- **Authentication failures**: Verify JWT secret configuration
- **Port conflicts**: Check if ports 8000-8012 are available

## Manual Testing with curl

### Health Check
```bash
curl http://localhost:8001/health
```

### Authentication
```bash
# Login
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123", "role": "Admin", "tenant_id": "test-tenant-123"}'

# Get user info (with token)
curl http://localhost:8001/auth/me \
  -H "Authorization: Bearer <your_token>"
```

### Usage Metrics
```bash
curl http://localhost:8000/usage/tenant/test-tenant-123 \
  -H "X-Tenant-ID: test-tenant-123" \
  -H "X-User-ID: test-user-456" \
  -H "X-Role: Admin"
```

### Billing
```bash
curl http://localhost:8010/billing/plans
```

### Notifications
```bash
curl -X POST http://localhost:8000/notifications/send \
  -H "Content-Type: application/json" \
  -d '{"notification_id": "test-123", "user_id": "test-user-456", "tenant_id": "test-tenant-123", "channel": "email", "message": "Test", "event_type": "test"}'
```

## Report Generation

After running tests, a detailed report is generated in `microservices_validation_report.md` containing:

- Service-by-service test results
- Endpoint validation status
- Error details and troubleshooting
- Overall success metrics

## Troubleshooting

### Service Won't Start
```bash
# Check Docker status
docker-compose ps

# View service logs
docker-compose logs auth_service

# Check for port conflicts
netstat -tulpn | grep :8001
```

### Database Issues
```bash
# Check PostgreSQL container
docker-compose logs postgres_db

# Test database connection
docker exec -it postgres_db psql -U reqadmin -d reqarchitect
```

### Authentication Problems
```bash
# Check JWT secret configuration
docker-compose exec auth_service env | grep JWT_SECRET

# Verify token format
echo "your_token_here" | cut -d'.' -f2 | base64 -d | jq
```

## Development

### Adding New Tests

1. Add new test methods to `MicroserviceTester` class
2. Update the `SERVICES` configuration
3. Add test data to `TEST_DATA` if needed
4. Update the report generation logic

### Custom Test Data

Modify the `TEST_DATA` dictionary in `test_microservices.py` to use your own test credentials and tenant information.

### Service Configuration

Update service URLs and ports in the `SERVICES` configuration if your setup differs from the default.

## Security Notes

- Test credentials are for validation only
- JWT tokens expire after 60 minutes
- All test data is isolated to the test environment
- No production data is accessed during validation

## Support

For issues with the validation suite:
1. Check the troubleshooting section above
2. Review service logs with `docker-compose logs`
3. Verify Docker and Python versions
4. Ensure all prerequisites are met

## License

This validation suite is part of the ReqArchitect platform and follows the same licensing terms. 