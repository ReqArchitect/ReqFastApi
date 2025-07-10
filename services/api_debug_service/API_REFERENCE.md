# API Reference: api_debug_service

## Overview

The API Debug Service provides non-intrusive discovery and visualization of API endpoints across all ReqArchitect microservices. It safely inspects running Docker containers and discovers endpoints without modifying any existing services.

## Base URL

```
http://localhost:8080
```

## Authentication

This service does not require authentication as it operates in a trusted internal network environment.

## Core Endpoints

### Get All Service Endpoints

**GET** `/api-debug`

Returns a comprehensive list of all discovered ReqArchitect services with their endpoints, health status, and metadata.

**Query Parameters:**
- `use_cache` (boolean, optional): Use cached data if available (default: true)
- `refresh` (boolean, optional): Force refresh cache (default: false)

**Response:** `200 OK`
```json
[
  {
    "service_name": "goal_service",
    "docker_container_name": "/goal-service",
    "base_url": "http://localhost:8081",
    "status": "healthy",
    "available_endpoints": [
      {
        "path": "/goals",
        "method": "GET",
        "description": "List all goals"
      },
      {
        "path": "/goals/{id}",
        "method": "GET",
        "description": "Get goal by ID"
      },
      {
        "path": "/goals",
        "method": "POST",
        "description": "Create new goal"
      },
      {
        "path": "/goals/{id}",
        "method": "PUT",
        "description": "Update goal"
      },
      {
        "path": "/goals/{id}",
        "method": "DELETE",
        "description": "Delete goal"
      },
      {
        "path": "/goals/{id}/assessment",
        "method": "GET",
        "description": "Get goal assessment"
      },
      {
        "path": "/goals/by-status/{status}",
        "method": "GET",
        "description": "Get goals by status"
      },
      {
        "path": "/goals/critical",
        "method": "GET",
        "description": "Get critical goals"
      },
      {
        "path": "/goals/active",
        "method": "GET",
        "description": "Get active goals"
      }
    ],
    "last_heartbeat": "2024-01-15T10:30:00Z",
    "version_tag": "latest",
    "port": 8081,
    "container_id": "abc123def456789",
    "image": "reqarchitect/goal-service:latest",
    "labels": {
      "reqarchitect-service": "true",
      "service.type": "microservice"
    }
  },
  {
    "service_name": "workpackage_service",
    "docker_container_name": "/workpackage-service",
    "base_url": "http://localhost:8082",
    "status": "healthy",
    "available_endpoints": [
      {
        "path": "/work-packages",
        "method": "GET",
        "description": "List all work packages"
      },
      {
        "path": "/work-packages/{id}",
        "method": "GET",
        "description": "Get work package by ID"
      },
      {
        "path": "/work-packages",
        "method": "POST",
        "description": "Create new work package"
      },
      {
        "path": "/work-packages/{id}",
        "method": "PUT",
        "description": "Update work package"
      },
      {
        "path": "/work-packages/{id}",
        "method": "DELETE",
        "description": "Delete work package"
      },
      {
        "path": "/work-packages/active",
        "method": "GET",
        "description": "Get active work packages"
      },
      {
        "path": "/work-packages/by-status/{status}",
        "method": "GET",
        "description": "Get work packages by status"
      }
    ],
    "last_heartbeat": "2024-01-15T10:30:00Z",
    "version_tag": "latest",
    "port": 8082,
    "container_id": "def456ghi789012",
    "image": "reqarchitect/workpackage-service:latest",
    "labels": {
      "reqarchitect-service": "true",
      "service.type": "microservice"
    }
  }
]
```

### Get Service Endpoints

**GET** `/api-debug/{service_name}`

Returns detailed endpoint information for a specific service.

**Path Parameters:**
- `service_name` (string, required): Name of the service to query

**Query Parameters:**
- `use_cache` (boolean, optional): Use cached data if available (default: true)

**Response:** `200 OK`
```json
{
  "service_name": "goal_service",
  "docker_container_name": "/goal-service",
  "base_url": "http://localhost:8081",
  "status": "healthy",
  "available_endpoints": [
    {
      "path": "/goals",
      "method": "GET",
      "description": "List all goals"
    },
    {
      "path": "/goals/{id}",
      "method": "GET",
      "description": "Get goal by ID"
    },
    {
      "path": "/goals",
      "method": "POST",
      "description": "Create new goal"
    },
    {
      "path": "/goals/{id}",
      "method": "PUT",
      "description": "Update goal"
    },
    {
      "path": "/goals/{id}",
      "method": "DELETE",
      "description": "Delete goal"
    },
    {
      "path": "/goals/{id}/assessment",
      "method": "GET",
      "description": "Get goal assessment"
    },
    {
      "path": "/goals/by-status/{status}",
      "method": "GET",
      "description": "Get goals by status"
    },
    {
      "path": "/goals/critical",
      "method": "GET",
      "description": "Get critical goals"
    },
    {
      "path": "/goals/active",
      "method": "GET",
      "description": "Get active goals"
    }
  ],
  "last_heartbeat": "2024-01-15T10:30:00Z",
  "version_tag": "latest",
  "port": 8081,
  "container_id": "abc123def456789",
  "image": "reqarchitect/goal-service:latest",
  "labels": {
    "reqarchitect-service": "true",
    "service.type": "microservice"
  }
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Service 'unknown_service' not found or not accessible"
}
```

### Get Health Summary

**GET** `/api-debug/health-summary`

Returns a comprehensive health summary of all services including counts and detailed status information.

**Query Parameters:**
- `use_cache` (boolean, optional): Use cached data if available (default: true)
- `refresh` (boolean, optional): Force refresh cache (default: false)

**Response:** `200 OK`
```json
{
  "total_services": 15,
  "healthy_services": 13,
  "unhealthy_services": 1,
  "unknown_services": 1,
  "services": [
    {
      "service_name": "goal_service",
      "docker_container_name": "/goal-service",
      "base_url": "http://localhost:8081",
      "status": "healthy",
      "available_endpoints": [...],
      "last_heartbeat": "2024-01-15T10:30:00Z",
      "version_tag": "latest",
      "port": 8081,
      "container_id": "abc123def456789",
      "image": "reqarchitect/goal-service:latest",
      "labels": {
        "reqarchitect-service": "true",
        "service.type": "microservice"
      }
    }
  ],
  "last_updated": "2024-01-15T10:30:00Z",
  "cache_status": "fresh"
}
```

## Detailed Service Information

### Get Service Details

**GET** `/api-debug/{service_name}/details`

Returns comprehensive information about a specific service including container logs, network information, and cache statistics.

**Path Parameters:**
- `service_name` (string, required): Name of the service to query

**Query Parameters:**
- `include_logs` (boolean, optional): Include container logs (default: true)
- `log_lines` (integer, optional): Number of log lines to include (default: 20)

**Response:** `200 OK`
```json
{
  "service": {
    "service_name": "goal_service",
    "docker_container_name": "/goal-service",
    "base_url": "http://localhost:8081",
    "status": "healthy",
    "available_endpoints": [...],
    "last_heartbeat": "2024-01-15T10:30:00Z",
    "version_tag": "latest",
    "port": 8081,
    "container_id": "abc123def456789",
    "image": "reqarchitect/goal-service:latest",
    "labels": {
      "reqarchitect-service": "true",
      "service.type": "microservice"
    }
  },
  "logs": [
    "2024-01-15T10:30:00Z INFO: Service started successfully",
    "2024-01-15T10:30:01Z INFO: Health check passed",
    "2024-01-15T10:30:02Z INFO: Database connection established",
    "2024-01-15T10:30:03Z INFO: API endpoints registered",
    "2024-01-15T10:30:04Z INFO: Service ready to accept requests"
  ],
  "network_info": {
    "id": "def456ghi789012",
    "name": "reqarchitect-network",
    "driver": "bridge",
    "ipam_config": [
      {
        "subnet": "172.18.0.0/16",
        "gateway": "172.18.0.1"
      }
    ],
    "containers": 15
  },
  "cache_stats": {
    "total_keys": 5,
    "cache_ttl_seconds": 300,
    "redis_connected": true,
    "key_ttls": {
      "api_debug:all_services": 285,
      "api_debug:service:goal_service": 290,
      "api_debug:health_summary": 295
    }
  }
}
```

## Utility Endpoints

### Health Check

**GET** `/health`

Returns the health status of the API debug service.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "api_debug_service",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

### Get Metrics

**GET** `/metrics`

Returns service metrics and statistics.

**Response:** `200 OK`
```json
{
  "service": "api_debug_service",
  "timestamp": "2024-01-15T10:30:00Z",
  "stats": {
    "cache": {
      "total_keys": 5,
      "cache_ttl_seconds": 300,
      "redis_connected": true,
      "key_ttls": {
        "api_debug:all_services": 285,
        "api_debug:service:goal_service": 290,
        "api_debug:health_summary": 295
      }
    },
    "network": {
      "id": "def456ghi789012",
      "name": "reqarchitect-network",
      "driver": "bridge",
      "containers": 15
    },
    "config": {
      "docker_network": "reqarchitect-network",
      "service_label": "reqarchitect-service=true",
      "cache_ttl_seconds": 300,
      "health_check_timeout": 5,
      "endpoint_discovery_timeout": 10,
      "max_retries": 3
    },
    "discovery_methods": [
      "swagger_openapi",
      "api_reference_md",
      "known_patterns",
      "health_endpoint"
    ]
  }
}
```

### Refresh Cache

**POST** `/api-debug/refresh`

Forces a refresh of all cached data by invalidating the cache and re-discovering all services.

**Response:** `200 OK`
```json
{
  "message": "Cache refreshed successfully",
  "status": "success"
}
```

### Get Discovery Statistics

**GET** `/api-debug/stats`

Returns detailed statistics about the discovery service including cache information, network details, and configuration.

**Response:** `200 OK`
```json
{
  "cache": {
    "total_keys": 5,
    "cache_ttl_seconds": 300,
    "redis_connected": true,
    "key_ttls": {
      "api_debug:all_services": 285,
      "api_debug:service:goal_service": 290,
      "api_debug:health_summary": 295
    }
  },
  "network": {
    "id": "def456ghi789012",
    "name": "reqarchitect-network",
    "driver": "bridge",
    "ipam_config": [
      {
        "subnet": "172.18.0.0/16",
        "gateway": "172.18.0.1"
      }
    ],
    "containers": 15
  },
  "config": {
    "docker_network": "reqarchitect-network",
    "service_label": "reqarchitect-service=true",
    "cache_ttl_seconds": 300,
    "health_check_timeout": 5,
    "endpoint_discovery_timeout": 10,
    "max_retries": 3
  },
  "discovery_methods": [
    "swagger_openapi",
    "api_reference_md",
    "known_patterns",
    "health_endpoint"
  ]
}
```

## Filtered Endpoints

### Get Healthy Services

**GET** `/api-debug/services/healthy`

Returns only services that are currently healthy.

**Response:** `200 OK`
```json
[
  {
    "service_name": "goal_service",
    "docker_container_name": "/goal-service",
    "base_url": "http://localhost:8081",
    "status": "healthy",
    "available_endpoints": [...],
    "last_heartbeat": "2024-01-15T10:30:00Z",
    "version_tag": "latest",
    "port": 8081,
    "container_id": "abc123def456789",
    "image": "reqarchitect/goal-service:latest",
    "labels": {
      "reqarchitect-service": "true",
      "service.type": "microservice"
    }
  }
]
```

### Get Unhealthy Services

**GET** `/api-debug/services/unhealthy`

Returns only services that are currently unhealthy.

**Response:** `200 OK`
```json
[
  {
    "service_name": "problematic_service",
    "docker_container_name": "/problematic-service",
    "base_url": "http://localhost:8089",
    "status": "unhealthy",
    "available_endpoints": [],
    "last_heartbeat": "2024-01-15T10:25:00Z",
    "version_tag": "latest",
    "port": 8089,
    "container_id": "xyz789abc123456",
    "image": "reqarchitect/problematic-service:latest",
    "labels": {
      "reqarchitect-service": "true",
      "service.type": "microservice"
    }
  }
]
```

## Data Models

### ServiceEndpointMap

```json
{
  "service_name": "string",
  "docker_container_name": "string",
  "base_url": "string",
  "status": "healthy|unhealthy|unknown",
  "available_endpoints": [
    {
      "path": "string",
      "method": "GET|POST|PUT|DELETE|PATCH",
      "description": "string"
    }
  ],
  "last_heartbeat": "datetime",
  "version_tag": "string",
  "port": "integer",
  "container_id": "string",
  "image": "string",
  "labels": {
    "key": "value"
  }
}
```

### HealthSummary

```json
{
  "total_services": "integer",
  "healthy_services": "integer",
  "unhealthy_services": "integer",
  "unknown_services": "integer",
  "services": ["ServiceEndpointMap"],
  "last_updated": "datetime",
  "cache_status": "string"
}
```

### EndpointInfo

```json
{
  "path": "string",
  "method": "GET|POST|PUT|DELETE|PATCH",
  "description": "string"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Service 'service_name' not found or not accessible"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error discovering services",
  "error": "Detailed error message"
}
```

## Discovery Methods

The service uses multiple methods to discover endpoints:

1. **Swagger/OpenAPI**: Queries `/openapi.json` and `/swagger.json`
2. **API Reference**: Reads `/API_REFERENCE.md` files
3. **Known Patterns**: Uses predefined endpoint patterns for each service
4. **Health Endpoints**: Checks `/health`, `/healthz`, `/ping`

## Caching

The service implements Redis-based caching with configurable TTL:

- **Cache TTL**: 300 seconds (5 minutes) by default
- **Cache Keys**: 
  - `api_debug:all_services`
  - `api_debug:service:{service_name}`
  - `api_debug:health_summary`
- **Cache Invalidation**: Manual refresh via `/api-debug/refresh`

## Rate Limiting

No rate limiting is implemented as this is an internal service.

## Pagination

No pagination is implemented as the service returns complete datasets.

## Filtering

Filtering is available through query parameters:

- `use_cache`: Control cache usage
- `refresh`: Force cache refresh
- `include_logs`: Control log inclusion
- `log_lines`: Control log line count

## OpenAPI Documentation

For complete OpenAPI documentation, visit:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json` 