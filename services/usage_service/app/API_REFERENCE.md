# API Reference: usage_service

## GET /usage/tenant/{tenant_id}
Returns usage metrics for a tenant (Owner/Admin only).

**Response:**
```json
{
  "tenant_id": "string",
  "active_users": 0,
  "model_count": 0,
  "api_requests": 0,
  "data_footprint": 0.0
}
```

## GET /usage/system_health
Returns system SLA/health metrics (Owner/Admin only).

**Response:**
```json
{
  "uptime_percent": 99.99,
  "error_rate_percent": 0.01,
  "p95_latency_ms": 120.0,
  "collected_at": "2025-07-05T12:00:00Z"
}
```

## GET /usage/activity/{tenant_id}
Returns recent audit events for a tenant (Owner/Admin only).

**Response:**
```json
[
  {
    "id": 1,
    "tenant_id": "string",
    "user_id": "string",
    "event_type": "fetch_usage_metrics",
    "event_time": "2025-07-05T12:00:00Z",
    "details": ""
  }
]
```

[OpenAPI JSON](./openapi.json)
