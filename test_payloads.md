# Test Payloads and Expected Responses

This document contains all the test payloads, headers, and expected responses for the FastAPI microservices integration testing.

## 🔐 Authentication Service

### User Signup

**Endpoint:** `POST /auth/signup`

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "email": "test-user@example.com",
  "password": "TestPassword123!",
  "tenant_id": "tenant-123",
  "user_id": "user-123",
  "role": "Admin"
}
```

**Expected Response (200):**
```json
{
  "message": "User created successfully",
  "user_id": "user-123",
  "email": "test-user@example.com",
  "tenant_id": "tenant-123",
  "role": "Admin"
}
```

### User Login

**Endpoint:** `POST /auth/login`

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "email": "test-user@example.com",
  "password": "TestPassword123!"
}
```

**Expected Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyLTEyMyIsInRlbmFudF9pZCI6InRlbmFudC0xMjMiLCJleHAiOjE3MDQwNzIwMDB9.signature",
  "user_id": "user-123",
  "tenant_id": "tenant-123",
  "email": "test-user@example.com",
  "role": "Admin"
}
```

### Get Current User

**Endpoint:** `GET /auth/me`

**Headers:**
```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "Content-Type": "application/json"
}
```

**Expected Response (200):**
```json
{
  "user_id": "user-123",
  "email": "test-user@example.com",
  "tenant_id": "tenant-123",
  "role": "Admin",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## 🤖 AI Modeling Service

### Generate AI Model

**Endpoint:** `POST /ai_modeling/generate`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "X-User-ID": "user-123",
  "X-Tenant-ID": "tenant-123",
  "X-Role": "Admin"
}
```

**Request Body:**
```json
{
  "tenant_id": "tenant-123",
  "user_id": "user-123",
  "input_type": "goal",
  "input_text": "Optimize supply chain efficiency and reduce operational costs by 20%"
}
```

**Expected Response (200):**
```json
{
  "model_id": "model-123",
  "tenant_id": "tenant-123",
  "user_id": "user-123",
  "layer": "Business Process",
  "status": "completed",
  "generated_at": "2024-01-01T12:00:00Z",
  "output": {
    "processes": [
      "Supply Chain Optimization",
      "Cost Reduction Strategy",
      "Inventory Management"
    ],
    "metrics": [
      "20% cost reduction",
      "30% efficiency improvement",
      "15% inventory reduction"
    ],
    "recommendations": [
      "Implement JIT inventory system",
      "Optimize supplier relationships",
      "Automate procurement processes"
    ]
  }
}
```

### Get Model Status

**Endpoint:** `GET /ai_modeling/status/{model_id}`

**Headers:**
```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "X-User-ID": "user-123",
  "X-Tenant-ID": "tenant-123"
}
```

**Expected Response (200):**
```json
{
  "model_id": "model-123",
  "status": "completed",
  "progress": 100,
  "created_at": "2024-01-01T12:00:00Z",
  "completed_at": "2024-01-01T12:05:00Z"
}
```

## 📊 Usage Service

### Get Usage Metrics

**Endpoint:** `GET /usage/tenant/{tenant_id}`

**Headers:**
```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "X-User-ID": "user-123",
  "X-Tenant-ID": "tenant-123"
}
```

**Expected Response (200):**
```json
{
  "tenant_id": "tenant-123",
  "api_calls": 15,
  "ai_generations": 3,
  "storage_used_mb": 45.2,
  "last_updated": "2024-01-01T12:00:00Z",
  "monthly_usage": {
    "current_month": "2024-01",
    "api_calls": 15,
    "ai_generations": 3,
    "storage_mb": 45.2
  }
}
```

### Log API Usage

**Endpoint:** `POST /usage/log`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "X-User-ID": "user-123",
  "X-Tenant-ID": "tenant-123"
}
```

**Request Body:**
```json
{
  "tenant_id": "tenant-123",
  "user_id": "user-123",
  "service": "ai_modeling",
  "endpoint": "/ai_modeling/generate",
  "timestamp": "2024-01-01T12:00:00Z",
  "response_time_ms": 2500,
  "status_code": 200
}
```

**Expected Response (200):**
```json
{
  "message": "Usage logged successfully",
  "usage_id": "usage-123",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🧾 Invoice Service

### Generate Invoice

**Endpoint:** `POST /invoices/generate/{tenant_id}`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "X-User-ID": "user-123",
  "X-Tenant-ID": "tenant-123"
}
```

**Request Body:**
```json
{
  "tenant_id": "tenant-123",
  "amount": 99.99,
  "currency": "USD",
  "description": "AI Modeling Service - Supply Chain Optimization",
  "line_items": [
    {
      "description": "AI Model Generation",
      "quantity": 1,
      "unit_price": 99.99,
      "total": 99.99
    }
  ],
  "metadata": {
    "model_id": "model-123",
    "service_type": "ai_modeling"
  }
}
```

**Expected Response (200):**
```json
{
  "invoice_id": "inv-123",
  "tenant_id": "tenant-123",
  "amount": 99.99,
  "currency": "USD",
  "status": "generated",
  "generated_at": "2024-01-01T12:00:00Z",
  "due_date": "2024-02-01T00:00:00Z",
  "pdf_url": "/invoices/inv-123.pdf",
  "line_items": [
    {
      "description": "AI Model Generation",
      "quantity": 1,
      "unit_price": 99.99,
      "total": 99.99
    }
  ]
}
```

### Get Invoice

**Endpoint:** `GET /invoices/{invoice_id}`

**Headers:**
```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "X-User-ID": "user-123",
  "X-Tenant-ID": "tenant-123"
}
```

**Expected Response (200):**
```json
{
  "invoice_id": "inv-123",
  "tenant_id": "tenant-123",
  "amount": 99.99,
  "currency": "USD",
  "status": "generated",
  "generated_at": "2024-01-01T12:00:00Z",
  "due_date": "2024-02-01T00:00:00Z",
  "pdf_url": "/invoices/inv-123.pdf"
}
```

## 📧 Notification Service

### Send Notification

**Endpoint:** `POST /notifications/send`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "X-User-ID": "user-123",
  "X-Tenant-ID": "tenant-123"
}
```

**Request Body:**
```json
{
  "user_id": "user-123",
  "tenant_id": "tenant-123",
  "channel": "email",
  "message": "Your AI modeling request has been completed successfully!",
  "event_type": "ai_modeling_complete",
  "metadata": {
    "model_id": "model-123",
    "completion_time": "2024-01-01T12:00:00Z",
    "layer": "Business Process"
  }
}
```

**Expected Response (200):**
```json
{
  "notification_id": "notif-123",
  "user_id": "user-123",
  "tenant_id": "tenant-123",
  "status": "sent",
  "channel": "email",
  "sent_at": "2024-01-01T12:00:00Z",
  "message": "Your AI modeling request has been completed successfully!"
}
```

### Get Notification Status

**Endpoint:** `GET /notifications/{notification_id}`

**Headers:**
```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "X-User-ID": "user-123",
  "X-Tenant-ID": "tenant-123"
}
```

**Expected Response (200):**
```json
{
  "notification_id": "notif-123",
  "user_id": "user-123",
  "tenant_id": "tenant-123",
  "status": "sent",
  "channel": "email",
  "sent_at": "2024-01-01T12:00:00Z",
  "delivered_at": "2024-01-01T12:01:00Z"
}
```

## 💰 Billing Service

### Get Billing Profile

**Endpoint:** `GET /billing/tenant/{tenant_id}`

**Headers:**
```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "X-User-ID": "user-123",
  "X-Tenant-ID": "tenant-123"
}
```

**Expected Response (200):**
```json
{
  "tenant_id": "tenant-123",
  "plan": "premium",
  "monthly_limit": 1000,
  "current_usage": 15,
  "billing_cycle": "monthly",
  "next_billing_date": "2024-02-01T00:00:00Z",
  "payment_method": {
    "type": "credit_card",
    "last4": "1234",
    "expiry": "12/25"
  },
  "invoices": [
    {
      "invoice_id": "inv-123",
      "amount": 99.99,
      "status": "paid",
      "due_date": "2024-02-01T00:00:00Z"
    }
  ]
}
```

### Create Billing Profile

**Endpoint:** `POST /billing/profile`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "X-User-ID": "user-123",
  "X-Tenant-ID": "tenant-123"
}
```

**Request Body:**
```json
{
  "tenant_id": "tenant-123",
  "plan": "premium",
  "monthly_limit": 1000,
  "billing_cycle": "monthly",
  "payment_method": {
    "type": "credit_card",
    "number": "4111111111111111",
    "expiry": "12/25",
    "cvv": "123"
  }
}
```

**Expected Response (200):**
```json
{
  "message": "Billing profile created successfully",
  "billing_id": "billing-123",
  "tenant_id": "tenant-123",
  "plan": "premium",
  "monthly_limit": 1000,
  "billing_cycle": "monthly"
}
```

## 🌐 Gateway Service

### Gateway Health Check

**Endpoint:** `GET /health`

**Headers:** None

**Expected Response (200):**
```json
{
  "status": "healthy",
  "service": "gateway",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0"
}
```

### Gateway Proxy - Auth Service

**Endpoint:** `GET /proxy/auth/me`

**Headers:**
```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "X-User-ID": "user-123",
  "X-Tenant-ID": "tenant-123"
}
```

**Expected Response (200):**
```json
{
  "user_id": "user-123",
  "email": "test-user@example.com",
  "tenant_id": "tenant-123",
  "role": "Admin",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Gateway Proxy - AI Modeling

**Endpoint:** `POST /proxy/ai_modeling/generate`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "X-User-ID": "user-123",
  "X-Tenant-ID": "tenant-123"
}
```

**Request Body:**
```json
{
  "tenant_id": "tenant-123",
  "user_id": "user-123",
  "input_type": "goal",
  "input_text": "Test via gateway"
}
```

**Expected Response (200):**
```json
{
  "model_id": "model-456",
  "tenant_id": "tenant-123",
  "user_id": "user-123",
  "layer": "Business Process",
  "status": "completed",
  "generated_at": "2024-01-01T12:00:00Z",
  "output": {
    "processes": ["Test Process"],
    "metrics": ["Test Metric"]
  }
}
```

## 🔄 Complete End-to-End Flow

### Test Scenario: Complete User Journey

1. **User Signup** → Get user credentials
2. **User Login** → Obtain JWT token
3. **AI Modeling** → Generate model with business goal
4. **Usage Logging** → Track API usage
5. **Invoice Generation** → Create invoice for service
6. **Notification** → Send completion notification
7. **Billing Check** → Verify billing profile

### Test Data Flow

```json
{
  "test_user": {
    "email": "test-user@example.com",
    "password": "TestPassword123!",
    "tenant_id": "tenant-123",
    "user_id": "user-123",
    "role": "Admin"
  },
  "ai_modeling_input": {
    "input_type": "goal",
    "input_text": "Optimize supply chain efficiency and reduce operational costs by 20%"
  },
  "expected_outputs": {
    "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "model_id": "model-123",
    "invoice_id": "inv-123",
    "notification_id": "notif-123"
  }
}
```

### Error Responses

**401 Unauthorized:**
```json
{
  "detail": "Not authenticated"
}
```

**403 Forbidden:**
```json
{
  "detail": "Not enough permissions"
}
```

**404 Not Found:**
```json
{
  "detail": "Resource not found"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error"
}
```

## 🧪 Integration Test Headers

### Standard Headers for All Requests

```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer {{jwt_token}}",
  "X-User-ID": "{{user_id}}",
  "X-Tenant-ID": "{{tenant_id}}",
  "X-Role": "{{user_role}}"
}
```

### Environment Variables

```bash
# Base URLs
BASE_URL=http://localhost:8080
AUTH_SERVICE_URL=http://localhost:8001
AI_MODELING_URL=http://localhost:8002
INVOICE_URL=http://localhost:8011
BILLING_URL=http://localhost:8010

# Test User
USER_EMAIL=test-user@example.com
USER_PASSWORD=TestPassword123!
TENANT_ID=tenant-123
USER_ID=user-123
USER_ROLE=Admin

# JWT Token (set after login)
JWT_TOKEN=
```

## 📋 Test Checklist

- [ ] All services are running and healthy
- [ ] Database is accessible and initialized
- [ ] JWT token is valid and not expired
- [ ] All required headers are included
- [ ] Request bodies match expected schema
- [ ] Response status codes are 200
- [ ] Response bodies contain expected fields
- [ ] Error handling works correctly
- [ ] Gateway proxy routes work
- [ ] Cross-service communication works 