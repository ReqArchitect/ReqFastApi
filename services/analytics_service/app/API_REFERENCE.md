# API Reference: analytics_service

## GET /analytics/tenant/{tenant_id}/monthly
Returns usage trends for a tenant (Owner/Admin only).

**Response:**
```json
[
  {
    "id": 1,
    "tenant_id": "string",
    "date": "2025-07-01T00:00:00Z",
    "active_users": 10,
    "model_count": 5,
    "api_requests": 1000,
    "data_footprint_mb": 120.5
  }
]
```

## GET /analytics/alerts/{tenant_id}
Returns active billing alerts for a tenant (Owner/Admin only).

**Response:**
```json
[
  {
    "id": 1,
    "tenant_id": "string",
    "alert_type": "api_limit",
    "triggered_at": "2025-07-05T12:00:00Z",
    "resolved": false
  }
]
```

## POST /analytics/alerts/resolve/{alert_id}
Mark a billing alert as resolved (Owner/Admin only).

**Response:**
```json
{
  "id": 1,
  "tenant_id": "string",
  "alert_type": "api_limit",
  "triggered_at": "2025-07-05T12:00:00Z",
  "resolved": true
}
```

[OpenAPI JSON](./openapi.json)
