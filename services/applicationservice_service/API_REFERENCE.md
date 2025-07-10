# API Reference: applicationservice_service

## Overview

The Application Service API provides comprehensive management of ArchiMate 3.2 Application Service elements with full CRUD operations, relationship management, analysis capabilities, and domain-specific queries.

## Base URL

```
http://localhost:8080
```

## Authentication

All endpoints require JWT authentication with the following header:
```
Authorization: Bearer <jwt_token>
```

Required JWT claims:
- `tenant_id`: UUID of the tenant
- `user_id`: UUID of the user
- `role`: User role (Owner, Admin, Editor, Viewer)

## Application Service Management

### Create Application Service

**POST** `/application-services`

Creates a new ApplicationService.

**Request Body:**
```json
{
  "name": "User Authentication Service",
  "description": "Provides secure user authentication and authorization",
  "service_type": "api",
  "exposed_function_id": "550e8400-e29b-41d4-a716-446655440000",
  "exposed_dataobject_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "active",
  "latency_target_ms": 200,
  "availability_target_pct": 99.9,
  "consumer_role_id": "550e8400-e29b-41d4-a716-446655440002",
  "version": "1.0.0",
  "delivery_channel": "https",
  "service_endpoint": "https://auth.example.com/api/v1",
  "authentication_method": "jwt",
  "rate_limiting": "{\"requests_per_minute\": 1000, \"burst_limit\": 100}",
  "caching_strategy": "{\"ttl\": 3600, \"cache_headers\": true}",
  "load_balancing": "{\"algorithm\": \"round_robin\", \"health_checks\": true}",
  "business_process_id": "550e8400-e29b-41d4-a716-446655440003",
  "capability_id": "550e8400-e29b-41d4-a716-446655440004",
  "business_value": "high",
  "business_criticality": "high",
  "technology_stack": "{\"framework\": \"FastAPI\", \"database\": \"PostgreSQL\", \"cache\": \"Redis\"}",
  "deployment_model": "microservice",
  "scaling_strategy": "horizontal",
  "backup_strategy": "{\"frequency\": \"daily\", \"retention\": \"30_days\"}",
  "security_level": "high",
  "compliance_requirements": "{\"gdpr\": true, \"sox\": true, \"pci\": false}",
  "data_classification": "internal",
  "encryption_requirements": "{\"at_rest\": true, \"in_transit\": true}",
  "documentation_link": "https://docs.example.com/auth",
  "api_documentation": "{\"openapi\": \"3.0.0\", \"endpoints\": [\"login\", \"logout\", \"refresh\"]}",
  "support_contact": "support@example.com",
  "maintenance_window": "Sunday 2-4 AM UTC"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440005",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440006",
  "user_id": "550e8400-e29b-41d4-a716-446655440007",
  "name": "User Authentication Service",
  "description": "Provides secure user authentication and authorization",
  "service_type": "api",
  "exposed_function_id": "550e8400-e29b-41d4-a716-446655440000",
  "exposed_dataobject_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "active",
  "latency_target_ms": 200,
  "availability_target_pct": 99.9,
  "consumer_role_id": "550e8400-e29b-41d4-a716-446655440002",
  "version": "1.0.0",
  "delivery_channel": "https",
  "service_endpoint": "https://auth.example.com/api/v1",
  "authentication_method": "jwt",
  "rate_limiting": "{\"requests_per_minute\": 1000, \"burst_limit\": 100}",
  "caching_strategy": "{\"ttl\": 3600, \"cache_headers\": true}",
  "load_balancing": "{\"algorithm\": \"round_robin\", \"health_checks\": true}",
  "current_latency_ms": null,
  "current_availability_pct": null,
  "uptime_percentage": null,
  "error_rate": null,
  "throughput_rps": null,
  "dependencies": null,
  "required_services": null,
  "optional_services": null,
  "business_process_id": "550e8400-e29b-41d4-a716-446655440003",
  "capability_id": "550e8400-e29b-41d4-a716-446655440004",
  "business_value": "high",
  "business_criticality": "high",
  "technology_stack": "{\"framework\": \"FastAPI\", \"database\": \"PostgreSQL\", \"cache\": \"Redis\"}",
  "deployment_model": "microservice",
  "scaling_strategy": "horizontal",
  "backup_strategy": "{\"frequency\": \"daily\", \"retention\": \"30_days\"}",
  "security_level": "high",
  "compliance_requirements": "{\"gdpr\": true, \"sox\": true, \"pci\": false}",
  "data_classification": "internal",
  "encryption_requirements": "{\"at_rest\": true, \"in_transit\": true}",
  "documentation_link": "https://docs.example.com/auth",
  "api_documentation": "{\"openapi\": \"3.0.0\", \"endpoints\": [\"login\", \"logout\", \"refresh\"]}",
  "support_contact": "support@example.com",
  "maintenance_window": "Sunday 2-4 AM UTC",
  "last_deployment": null,
  "next_deployment": null,
  "incident_count": 0,
  "last_incident": null,
  "sla_breaches": 0,
  "response_time_p95": null,
  "response_time_p99": null,
  "success_rate": null,
  "user_satisfaction": null,
  "monthly_cost": null,
  "resource_utilization": null,
  "capacity_planning": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### List Application Services

**GET** `/application-services`

Lists all ApplicationServices for the tenant with filtering and pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)
- `service_type` (string, optional): Filter by service type
- `status` (string, optional): Filter by status
- `business_criticality` (string, optional): Filter by business criticality
- `business_value` (string, optional): Filter by business value
- `capability_id` (UUID, optional): Filter by capability
- `technology_stack` (string, optional): Filter by technology stack (contains)
- `performance_threshold` (float, optional): Filter by minimum availability

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440005",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440006",
    "user_id": "550e8400-e29b-41d4-a716-446655440007",
    "name": "User Authentication Service",
    "description": "Provides secure user authentication and authorization",
    "service_type": "api",
    "status": "active",
    "latency_target_ms": 200,
    "availability_target_pct": 99.9,
    "version": "1.0.0",
    "delivery_channel": "https",
    "business_value": "high",
    "business_criticality": "high",
    "deployment_model": "microservice",
    "scaling_strategy": "horizontal",
    "security_level": "high",
    "data_classification": "internal",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Application Service

**GET** `/application-services/{service_id}`

Retrieves an ApplicationService by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440005",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440006",
  "user_id": "550e8400-e29b-41d4-a716-446655440007",
  "name": "User Authentication Service",
  "description": "Provides secure user authentication and authorization",
  "service_type": "api",
  "exposed_function_id": "550e8400-e29b-41d4-a716-446655440000",
  "exposed_dataobject_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "active",
  "latency_target_ms": 200,
  "availability_target_pct": 99.9,
  "consumer_role_id": "550e8400-e29b-41d4-a716-446655440002",
  "version": "1.0.0",
  "delivery_channel": "https",
  "service_endpoint": "https://auth.example.com/api/v1",
  "authentication_method": "jwt",
  "rate_limiting": "{\"requests_per_minute\": 1000, \"burst_limit\": 100}",
  "caching_strategy": "{\"ttl\": 3600, \"cache_headers\": true}",
  "load_balancing": "{\"algorithm\": \"round_robin\", \"health_checks\": true}",
  "current_latency_ms": 180,
  "current_availability_pct": 99.95,
  "uptime_percentage": 99.98,
  "error_rate": 0.02,
  "throughput_rps": 1500.0,
  "dependencies": "{\"database\": \"postgres\", \"cache\": \"redis\"}",
  "required_services": "{\"user_service\": \"required\"}",
  "optional_services": "{\"analytics_service\": \"optional\"}",
  "business_process_id": "550e8400-e29b-41d4-a716-446655440003",
  "capability_id": "550e8400-e29b-41d4-a716-446655440004",
  "business_value": "high",
  "business_criticality": "high",
  "technology_stack": "{\"framework\": \"FastAPI\", \"database\": \"PostgreSQL\", \"cache\": \"Redis\"}",
  "deployment_model": "microservice",
  "scaling_strategy": "horizontal",
  "backup_strategy": "{\"frequency\": \"daily\", \"retention\": \"30_days\"}",
  "security_level": "high",
  "compliance_requirements": "{\"gdpr\": true, \"sox\": true, \"pci\": false}",
  "data_classification": "internal",
  "encryption_requirements": "{\"at_rest\": true, \"in_transit\": true}",
  "documentation_link": "https://docs.example.com/auth",
  "api_documentation": "{\"openapi\": \"3.0.0\", \"endpoints\": [\"login\", \"logout\", \"refresh\"]}",
  "support_contact": "support@example.com",
  "maintenance_window": "Sunday 2-4 AM UTC",
  "last_deployment": "2024-01-10T15:00:00Z",
  "next_deployment": "2024-01-20T15:00:00Z",
  "incident_count": 2,
  "last_incident": "2024-01-12T08:30:00Z",
  "sla_breaches": 0,
  "response_time_p95": 250,
  "response_time_p99": 450,
  "success_rate": 99.98,
  "user_satisfaction": 4.8,
  "monthly_cost": 2500.0,
  "resource_utilization": 65.5,
  "capacity_planning": "{\"current_capacity\": 70, \"planned_capacity\": 85}",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Update Application Service

**PUT** `/application-services/{service_id}`

Updates an ApplicationService.

**Request Body:** (All fields optional)
```json
{
  "name": "Enhanced User Authentication Service",
  "description": "Updated description with enhanced security features",
  "availability_target_pct": 99.99,
  "security_level": "critical",
  "technology_stack": "{\"framework\": \"FastAPI\", \"database\": \"PostgreSQL\", \"cache\": \"Redis\", \"monitoring\": \"Prometheus\"}"
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440005",
  "name": "Enhanced User Authentication Service",
  "description": "Updated description with enhanced security features",
  "availability_target_pct": 99.99,
  "security_level": "critical",
  "technology_stack": "{\"framework\": \"FastAPI\", \"database\": \"PostgreSQL\", \"cache\": \"Redis\", \"monitoring\": \"Prometheus\"}",
  "updated_at": "2024-01-15T11:30:00Z"
}
```

### Delete Application Service

**DELETE** `/application-services/{service_id}`

Deletes an ApplicationService.

**Response:** `204 No Content`

## Service Link Management

### Create Service Link

**POST** `/application-services/{service_id}/links`

Creates a link between an application service and another element.

**Request Body:**
```json
{
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440008",
  "linked_element_type": "business_process",
  "link_type": "supports",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "data_flow_direction": "bidirectional",
  "performance_impact": "medium",
  "latency_contribution": 50.0,
  "availability_impact": 5.0,
  "throughput_impact": 10.0,
  "error_propagation": 2.0,
  "business_criticality": "high",
  "business_value": "high",
  "alignment_score": 0.8,
  "implementation_priority": "high",
  "implementation_phase": "active",
  "resource_allocation": 25.0,
  "risk_level": "medium",
  "reliability_score": 0.9,
  "failure_impact": "high",
  "recovery_time": 30,
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "logging_level": "info",
  "metrics_collection": "{\"prometheus\": true, \"grafana\": true}",
  "security_requirements": "{\"encryption\": \"required\", \"authentication\": \"jwt\"}",
  "compliance_impact": "medium",
  "data_protection": "{\"gdpr\": true, \"sox\": false}",
  "performance_contribution": 15.0,
  "success_contribution": 20.0,
  "quality_metrics": "{\"response_time\": \"p95\", \"availability\": \"99.9%\"}"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440009",
  "application_service_id": "550e8400-e29b-41d4-a716-446655440005",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440008",
  "linked_element_type": "business_process",
  "link_type": "supports",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "data_flow_direction": "bidirectional",
  "performance_impact": "medium",
  "latency_contribution": 50.0,
  "availability_impact": 5.0,
  "throughput_impact": 10.0,
  "error_propagation": 2.0,
  "business_criticality": "high",
  "business_value": "high",
  "alignment_score": 0.8,
  "implementation_priority": "high",
  "implementation_phase": "active",
  "resource_allocation": 25.0,
  "risk_level": "medium",
  "reliability_score": 0.9,
  "failure_impact": "high",
  "recovery_time": 30,
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "logging_level": "info",
  "metrics_collection": "{\"prometheus\": true, \"grafana\": true}",
  "security_requirements": "{\"encryption\": \"required\", \"authentication\": \"jwt\"}",
  "compliance_impact": "medium",
  "data_protection": "{\"gdpr\": true, \"sox\": false}",
  "performance_contribution": 15.0,
  "success_contribution": 20.0,
  "quality_metrics": "{\"response_time\": \"p95\", \"availability\": \"99.9%\"}",
  "created_by": "550e8400-e29b-41d4-a716-446655440007",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### List Service Links

**GET** `/application-services/{service_id}/links`

Lists all links for an application service.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440009",
    "application_service_id": "550e8400-e29b-41d4-a716-446655440005",
    "linked_element_id": "550e8400-e29b-41d4-a716-446655440008",
    "linked_element_type": "business_process",
    "link_type": "supports",
    "relationship_strength": "strong",
    "dependency_level": "high",
    "interaction_frequency": "frequent",
    "interaction_type": "synchronous",
    "data_flow_direction": "bidirectional",
    "performance_impact": "medium",
    "latency_contribution": 50.0,
    "availability_impact": 5.0,
    "throughput_impact": 10.0,
    "error_propagation": 2.0,
    "business_criticality": "high",
    "business_value": "high",
    "alignment_score": 0.8,
    "implementation_priority": "high",
    "implementation_phase": "active",
    "resource_allocation": 25.0,
    "risk_level": "medium",
    "reliability_score": 0.9,
    "failure_impact": "high",
    "recovery_time": 30,
    "monitoring_enabled": true,
    "alerting_enabled": true,
    "logging_level": "info",
    "metrics_collection": "{\"prometheus\": true, \"grafana\": true}",
    "security_requirements": "{\"encryption\": \"required\", \"authentication\": \"jwt\"}",
    "compliance_impact": "medium",
    "data_protection": "{\"gdpr\": true, \"sox\": false}",
    "performance_contribution": 15.0,
    "success_contribution": 20.0,
    "quality_metrics": "{\"response_time\": \"p95\", \"availability\": \"99.9%\"}",
    "created_by": "550e8400-e29b-41d4-a716-446655440007",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Service Link

**GET** `/application-services/links/{link_id}`

Retrieves a service link by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440009",
  "application_service_id": "550e8400-e29b-41d4-a716-446655440005",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440008",
  "linked_element_type": "business_process",
  "link_type": "supports",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "data_flow_direction": "bidirectional",
  "performance_impact": "medium",
  "latency_contribution": 50.0,
  "availability_impact": 5.0,
  "throughput_impact": 10.0,
  "error_propagation": 2.0,
  "business_criticality": "high",
  "business_value": "high",
  "alignment_score": 0.8,
  "implementation_priority": "high",
  "implementation_phase": "active",
  "resource_allocation": 25.0,
  "risk_level": "medium",
  "reliability_score": 0.9,
  "failure_impact": "high",
  "recovery_time": 30,
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "logging_level": "info",
  "metrics_collection": "{\"prometheus\": true, \"grafana\": true}",
  "security_requirements": "{\"encryption\": \"required\", \"authentication\": \"jwt\"}",
  "compliance_impact": "medium",
  "data_protection": "{\"gdpr\": true, \"sox\": false}",
  "performance_contribution": 15.0,
  "success_contribution": 20.0,
  "quality_metrics": "{\"response_time\": \"p95\", \"availability\": \"99.9%\"}",
  "created_by": "550e8400-e29b-41d4-a716-446655440007",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Update Service Link

**PUT** `/application-services/links/{link_id}`

Updates a service link.

**Request Body:** (All fields optional)
```json
{
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "performance_impact": "low",
  "alignment_score": 0.6
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440009",
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "performance_impact": "low",
  "alignment_score": 0.6
}
```

### Delete Service Link

**DELETE** `/application-services/links/{link_id}`

Deletes a service link.

**Response:** `204 No Content`

## Analysis & Impact Endpoints

### Get Impact Map

**GET** `/application-services/{service_id}/impact-map`

Returns impact mapping for the ApplicationService.

**Response:** `200 OK`
```json
{
  "service_id": "550e8400-e29b-41d4-a716-446655440005",
  "direct_impacts": [
    {
      "element_id": "550e8400-e29b-41d4-a716-446655440008",
      "element_type": "business_process",
      "link_type": "supports",
      "relationship_strength": "strong",
      "dependency_level": "high",
      "performance_impact": "medium"
    }
  ],
  "indirect_impacts": [],
  "risk_assessment": {
    "business_criticality": "high",
    "business_value": "high",
    "security_level": "high",
    "availability_risk": 0.05,
    "dependency_count": 1
  },
  "dependency_chain": [
    {
      "element_id": "550e8400-e29b-41d4-a716-446655440008",
      "element_type": "business_process",
      "dependency_level": "high"
    }
  ],
  "total_impact_score": 0.85
}
```

### Get Performance Score

**GET** `/application-services/{service_id}/performance-score`

Returns performance score for the ApplicationService.

**Response:** `200 OK`
```json
{
  "service_id": "550e8400-e29b-41d4-a716-446655440005",
  "latency_score": 0.9,
  "availability_score": 0.95,
  "throughput_score": 0.85,
  "overall_score": 0.9,
  "recommendations": [
    "Consider implementing caching strategies to improve response times",
    "Review and optimize database queries",
    "Implement horizontal scaling for better throughput"
  ],
  "performance_metrics": {
    "latency_target_ms": 200,
    "availability_target_pct": 99.9,
    "current_latency_ms": 180,
    "current_availability_pct": 99.95,
    "throughput_rps": 1500.0,
    "service_type": "api",
    "delivery_channel": "https"
  }
}
```

### Analyze Application Service

**GET** `/application-services/{service_id}/analysis`

Returns comprehensive analysis for the ApplicationService.

**Response:** `200 OK`
```json
{
  "service_id": "550e8400-e29b-41d4-a716-446655440005",
  "operational_health": {
    "overall_score": 0.85,
    "issues": [],
    "status": "healthy"
  },
  "business_alignment": {
    "alignment_score": 0.8,
    "has_business_process": true,
    "has_capability": true,
    "business_criticality": "high",
    "business_value": "high"
  },
  "technical_debt": {
    "debt_score": 0.15,
    "debt_items": ["No technology stack documented"],
    "priority": "low"
  },
  "risk_factors": [
    {
      "type": "business_criticality",
      "severity": "high",
      "description": "Critical business service with high availability requirements"
    }
  ],
  "improvement_opportunities": [
    "Document technology stack and dependencies",
    "Implement comprehensive monitoring and alerting"
  ],
  "compliance_status": {
    "compliance_rate": 0.8,
    "compliant_items": ["security_level", "monitoring"],
    "non_compliant_items": ["documentation"],
    "status": "needs_attention"
  }
}
```

## Domain-Specific Query Endpoints

### Get by Service Type

**GET** `/application-services/by-type/{service_type}`

Returns application services filtered by type.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440005",
    "name": "User Authentication Service",
    "service_type": "api",
    "status": "active"
  }
]
```

### Get by Status

**GET** `/application-services/by-status/{status}`

Returns application services filtered by status.

### Get by Capability

**GET** `/application-services/by-capability/{capability_id}`

Returns application services filtered by capability.

### Get by Performance

**GET** `/application-services/by-performance/{performance_threshold}`

Returns application services with availability above the threshold.

### Get by Element

**GET** `/application-services/by-element/{element_type}/{element_id}`

Returns application services linked to a specific element.

### Get Active Services

**GET** `/application-services/active`

Returns all active application services.

### Get Critical Services

**GET** `/application-services/critical`

Returns all critical application services.

## Enumeration Endpoints

### Get Service Types

**GET** `/application-services/service-types`

Returns all available service types.

**Response:** `200 OK`
```json
[
  "ui",
  "api",
  "data",
  "integration",
  "messaging"
]
```

### Get Statuses

**GET** `/application-services/statuses`

Returns all available statuses.

**Response:** `200 OK`
```json
[
  "active",
  "inactive",
  "deprecated",
  "planned",
  "maintenance"
]
```

### Get Business Criticalities

**GET** `/application-services/business-criticalities`

Returns all available business criticality levels.

**Response:** `200 OK`
```json
[
  "low",
  "medium",
  "high",
  "critical"
]
```

### Get Business Values

**GET** `/application-services/business-values`

Returns all available business value levels.

**Response:** `200 OK`
```json
[
  "low",
  "medium",
  "high",
  "critical"
]
```

### Get Delivery Channels

**GET** `/application-services/delivery-channels`

Returns all available delivery channels.

**Response:** `200 OK`
```json
[
  "http",
  "https",
  "grpc",
  "websocket",
  "message_queue",
  "file_transfer"
]
```

### Get Authentication Methods

**GET** `/application-services/authentication-methods`

Returns all available authentication methods.

**Response:** `200 OK`
```json
[
  "none",
  "basic",
  "oauth",
  "jwt",
  "api_key"
]
```

### Get Deployment Models

**GET** `/application-services/deployment-models`

Returns all available deployment models.

**Response:** `200 OK`
```json
[
  "monolithic",
  "microservice",
  "serverless",
  "container"
]
```

### Get Scaling Strategies

**GET** `/application-services/scaling-strategies`

Returns all available scaling strategies.

**Response:** `200 OK`
```json
[
  "horizontal",
  "vertical",
  "auto"
]
```

### Get Security Levels

**GET** `/application-services/security-levels`

Returns all available security levels.

**Response:** `200 OK`
```json
[
  "basic",
  "standard",
  "high",
  "critical"
]
```

### Get Data Classifications

**GET** `/application-services/data-classifications`

Returns all available data classification levels.

**Response:** `200 OK`
```json
[
  "public",
  "internal",
  "confidential",
  "restricted"
]
```

### Get Link Types

**GET** `/application-services/link-types`

Returns all available link types.

**Response:** `200 OK`
```json
[
  "realizes",
  "supports",
  "enables",
  "consumes",
  "produces",
  "triggers",
  "requires"
]
```

### Get Relationship Strengths

**GET** `/application-services/relationship-strengths`

Returns all available relationship strengths.

**Response:** `200 OK`
```json
[
  "strong",
  "medium",
  "weak"
]
```

### Get Dependency Levels

**GET** `/application-services/dependency-levels`

Returns all available dependency levels.

**Response:** `200 OK`
```json
[
  "high",
  "medium",
  "low"
]
```

### Get Interaction Frequencies

**GET** `/application-services/interaction-frequencies`

Returns all available interaction frequencies.

**Response:** `200 OK`
```json
[
  "frequent",
  "regular",
  "occasional",
  "rare"
]
```

### Get Interaction Types

**GET** `/application-services/interaction-types`

Returns all available interaction types.

**Response:** `200 OK`
```json
[
  "synchronous",
  "asynchronous",
  "batch",
  "real_time",
  "event_driven"
]
```

### Get Data Flow Directions

**GET** `/application-services/data-flow-directions`

Returns all available data flow directions.

**Response:** `200 OK`
```json
[
  "input",
  "output",
  "bidirectional"
]
```

### Get Performance Impacts

**GET** `/application-services/performance-impacts`

Returns all available performance impact levels.

**Response:** `200 OK`
```json
[
  "low",
  "medium",
  "high",
  "critical"
]
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error: Invalid service type"
}
```

### 401 Unauthorized
```json
{
  "detail": "Missing or invalid authorization header"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions. Required: application_service:create, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Application service not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage:
- 1000 requests per hour per tenant
- 100 requests per minute per user
- Burst limit: 10 requests per second

## Pagination

List endpoints support pagination with the following parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 1000)

## Filtering

List endpoints support filtering by:
- Service type
- Status
- Business criticality
- Business value
- Capability
- Technology stack (contains)
- Performance threshold

## Sorting

Results are sorted by `created_at` in descending order by default.

## OpenAPI Documentation

For complete OpenAPI documentation, visit:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json` 