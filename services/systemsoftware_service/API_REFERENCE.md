# API Reference: systemsoftware_service

## Overview

The System Software Service API provides comprehensive management of ArchiMate 3.2 System Software elements with full CRUD operations, relationship management, analysis capabilities, and domain-specific queries.

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

## System Software Management

### Create System Software

**POST** `/api/v1/system-software/`

Creates a new SystemSoftware.

**Request Body:**
```json
{
  "name": "Ubuntu 22.04 LTS",
  "description": "Linux operating system for servers",
  "software_type": "os",
  "version": "22.04.3",
  "vendor": "Canonical",
  "license_type": "open_source",
  "supported_node_id": "550e8400-e29b-41d4-a716-446655440000",
  "capabilities_provided": "{\"file_system\": \"ext4\", \"networking\": \"systemd-networkd\"}",
  "compliance_certifications": "{\"iso\": \"27001\", \"soc\": \"2\"}",
  "lifecycle_state": "active",
  "vulnerability_score": 2.5,
  "security_patches_available": false,
  "compliance_status": "compliant",
  "update_channel": "lts",
  "last_patch_date": "2024-01-10T00:00:00Z",
  "next_patch_date": "2024-02-10T00:00:00Z",
  "auto_update_enabled": true,
  "update_frequency": "monthly",
  "resource_usage": 45.5,
  "uptime_percentage": 99.9,
  "response_time_avg": 150.0,
  "configuration": "{\"ssh\": \"enabled\", \"firewall\": \"ufw\"}",
  "deployment_environment": "production",
  "deployment_method": "package_manager",
  "dependencies": "{\"packages\": [\"openssl\", \"nginx\"]}",
  "dependent_components": "{\"apps\": [\"web-app\", \"api-service\"]}",
  "integration_points": "{\"apis\": [\"rest-api\", \"grpc-api\"]}",
  "license_cost": 0.0,
  "license_seats": 100,
  "license_usage": 75,
  "documentation_url": "https://ubuntu.com/docs",
  "support_contact": "support@canonical.com",
  "support_level": "standard",
  "backup_enabled": true,
  "backup_frequency": "daily",
  "backup_retention_days": 30,
  "disaster_recovery_plan": "{\"rto\": \"4h\", \"rpo\": \"1h\"}",
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "monitoring_endpoints": "{\"health\": \"/health\", \"metrics\": \"/metrics\"}",
  "alerting_rules": "{\"high_cpu\": \"> 80%\", \"high_memory\": \"> 85%\"}",
  "maintenance_window": "Sunday 2-4 AM UTC",
  "cpu_requirements": 2.0,
  "memory_requirements": 4.0,
  "storage_requirements": 20.0,
  "network_requirements": 100.0,
  "max_concurrent_users": 1000,
  "max_data_volume": 1000.0,
  "scalability_limits": "{\"max_instances\": 10, \"max_connections\": 10000}",
  "capacity_planning": "{\"growth_rate\": \"10%\", \"upgrade_cycle\": \"2y\"}"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "name": "Ubuntu 22.04 LTS",
  "description": "Linux operating system for servers",
  "software_type": "os",
  "version": "22.04.3",
  "vendor": "Canonical",
  "license_type": "open_source",
  "supported_node_id": "550e8400-e29b-41d4-a716-446655440000",
  "capabilities_provided": "{\"file_system\": \"ext4\", \"networking\": \"systemd-networkd\"}",
  "compliance_certifications": "{\"iso\": \"27001\", \"soc\": \"2\"}",
  "lifecycle_state": "active",
  "vulnerability_score": 2.5,
  "security_patches_available": false,
  "last_security_audit": null,
  "compliance_status": "compliant",
  "update_channel": "lts",
  "last_patch_date": "2024-01-10T00:00:00Z",
  "next_patch_date": "2024-02-10T00:00:00Z",
  "auto_update_enabled": true,
  "update_frequency": "monthly",
  "performance_metrics": null,
  "resource_usage": 45.5,
  "uptime_percentage": 99.9,
  "response_time_avg": 150.0,
  "configuration": "{\"ssh\": \"enabled\", \"firewall\": \"ufw\"}",
  "deployment_environment": "production",
  "deployment_method": "package_manager",
  "dependencies": "{\"packages\": [\"openssl\", \"nginx\"]}",
  "dependent_components": "{\"apps\": [\"web-app\", \"api-service\"]}",
  "integration_points": "{\"apis\": [\"rest-api\", \"grpc-api\"]}",
  "license_expiry": null,
  "license_cost": 0.0,
  "license_seats": 100,
  "license_usage": 75,
  "support_expiry": null,
  "documentation_url": "https://ubuntu.com/docs",
  "support_contact": "support@canonical.com",
  "support_level": "standard",
  "backup_enabled": true,
  "backup_frequency": "daily",
  "backup_retention_days": 30,
  "disaster_recovery_plan": "{\"rto\": \"4h\", \"rpo\": \"1h\"}",
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "monitoring_endpoints": "{\"health\": \"/health\", \"metrics\": \"/metrics\"}",
  "alerting_rules": "{\"high_cpu\": \"> 80%\", \"high_memory\": \"> 85%\"}",
  "installation_date": null,
  "last_maintenance": null,
  "next_maintenance": null,
  "incident_count": 0,
  "last_incident": null,
  "data_retention_policy": null,
  "access_controls": null,
  "audit_requirements": null,
  "regulatory_compliance": null,
  "maintenance_window": "Sunday 2-4 AM UTC",
  "cpu_requirements": 2.0,
  "memory_requirements": 4.0,
  "storage_requirements": 20.0,
  "network_requirements": 100.0,
  "max_concurrent_users": 1000,
  "max_data_volume": 1000.0,
  "scalability_limits": "{\"max_instances\": 10, \"max_connections\": 10000}",
  "capacity_planning": "{\"growth_rate\": \"10%\", \"upgrade_cycle\": \"2y\"}",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### List System Software

**GET** `/api/v1/system-software/`

Lists all SystemSoftware for the tenant with filtering and pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)
- `software_type` (string, optional): Filter by software type
- `vendor` (string, optional): Filter by vendor (contains)
- `lifecycle_state` (string, optional): Filter by lifecycle state
- `vulnerability_threshold` (float, optional): Filter by maximum vulnerability score

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440002",
    "name": "Ubuntu 22.04 LTS",
    "description": "Linux operating system for servers",
    "software_type": "os",
    "version": "22.04.3",
    "vendor": "Canonical",
    "license_type": "open_source",
    "lifecycle_state": "active",
    "vulnerability_score": 2.5,
    "resource_usage": 45.5,
    "uptime_percentage": 99.9,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get System Software

**GET** `/api/v1/system-software/{system_software_id}`

Retrieves a SystemSoftware by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "name": "Ubuntu 22.04 LTS",
  "description": "Linux operating system for servers",
  "software_type": "os",
  "version": "22.04.3",
  "vendor": "Canonical",
  "license_type": "open_source",
  "supported_node_id": "550e8400-e29b-41d4-a716-446655440000",
  "capabilities_provided": "{\"file_system\": \"ext4\", \"networking\": \"systemd-networkd\"}",
  "compliance_certifications": "{\"iso\": \"27001\", \"soc\": \"2\"}",
  "lifecycle_state": "active",
  "vulnerability_score": 2.5,
  "security_patches_available": false,
  "last_security_audit": null,
  "compliance_status": "compliant",
  "update_channel": "lts",
  "last_patch_date": "2024-01-10T00:00:00Z",
  "next_patch_date": "2024-02-10T00:00:00Z",
  "auto_update_enabled": true,
  "update_frequency": "monthly",
  "performance_metrics": null,
  "resource_usage": 45.5,
  "uptime_percentage": 99.9,
  "response_time_avg": 150.0,
  "configuration": "{\"ssh\": \"enabled\", \"firewall\": \"ufw\"}",
  "deployment_environment": "production",
  "deployment_method": "package_manager",
  "dependencies": "{\"packages\": [\"openssl\", \"nginx\"]}",
  "dependent_components": "{\"apps\": [\"web-app\", \"api-service\"]}",
  "integration_points": "{\"apis\": [\"rest-api\", \"grpc-api\"]}",
  "license_expiry": null,
  "license_cost": 0.0,
  "license_seats": 100,
  "license_usage": 75,
  "support_expiry": null,
  "documentation_url": "https://ubuntu.com/docs",
  "support_contact": "support@canonical.com",
  "support_level": "standard",
  "backup_enabled": true,
  "backup_frequency": "daily",
  "backup_retention_days": 30,
  "disaster_recovery_plan": "{\"rto\": \"4h\", \"rpo\": \"1h\"}",
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "monitoring_endpoints": "{\"health\": \"/health\", \"metrics\": \"/metrics\"}",
  "alerting_rules": "{\"high_cpu\": \"> 80%\", \"high_memory\": \"> 85%\"}",
  "installation_date": null,
  "last_maintenance": null,
  "next_maintenance": null,
  "incident_count": 0,
  "last_incident": null,
  "data_retention_policy": null,
  "access_controls": null,
  "audit_requirements": null,
  "regulatory_compliance": null,
  "maintenance_window": "Sunday 2-4 AM UTC",
  "cpu_requirements": 2.0,
  "memory_requirements": 4.0,
  "storage_requirements": 20.0,
  "network_requirements": 100.0,
  "max_concurrent_users": 1000,
  "max_data_volume": 1000.0,
  "scalability_limits": "{\"max_instances\": 10, \"max_connections\": 10000}",
  "capacity_planning": "{\"growth_rate\": \"10%\", \"upgrade_cycle\": \"2y\"}",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Update System Software

**PUT** `/api/v1/system-software/{system_software_id}`

Updates a SystemSoftware.

**Request Body:** (All fields optional)
```json
{
  "name": "Ubuntu 22.04.3 LTS",
  "description": "Updated Linux operating system for servers",
  "vulnerability_score": 1.5,
  "resource_usage": 50.0,
  "security_patches_available": true
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Ubuntu 22.04.3 LTS",
  "description": "Updated Linux operating system for servers",
  "vulnerability_score": 1.5,
  "resource_usage": 50.0,
  "security_patches_available": true,
  "updated_at": "2024-01-15T11:30:00Z"
}
```

### Delete System Software

**DELETE** `/api/v1/system-software/{system_software_id}`

Deletes a SystemSoftware.

**Response:** `204 No Content`

## Software Link Management

### Create Software Link

**POST** `/api/v1/system-software/{system_software_id}/links`

Creates a link between a system software and another element.

**Request Body:**
```json
{
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_type": "node",
  "link_type": "runs_on",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "integration_status": "active",
  "integration_version": "1.0",
  "integration_config": "{\"protocol\": \"tcp\", \"port\": 22}",
  "communication_protocol": "SSH",
  "communication_port": 22,
  "communication_frequency": "frequent",
  "communication_type": "synchronous",
  "performance_impact": "medium",
  "latency_contribution": 10.0,
  "bandwidth_usage": 5.0,
  "resource_consumption": 15.0,
  "business_criticality": "high",
  "business_value": "high",
  "alignment_score": 0.9,
  "implementation_priority": "high",
  "implementation_phase": "active",
  "resource_allocation": 25.0,
  "risk_level": "medium",
  "reliability_score": 0.95,
  "failure_impact": "high",
  "recovery_time": 30,
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "logging_level": "info",
  "metrics_collection": "{\"cpu\": true, \"memory\": true, \"disk\": true}",
  "security_requirements": "{\"encryption\": \"required\", \"authentication\": \"required\"}",
  "compliance_impact": "medium",
  "data_protection": "{\"backup\": \"required\", \"retention\": \"7y\"}",
  "performance_contribution": 20.0,
  "success_contribution": 25.0,
  "quality_metrics": "{\"availability\": \"99.9%\", \"performance\": \"excellent\"}"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "system_software_id": "550e8400-e29b-41d4-a716-446655440000",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_type": "node",
  "link_type": "runs_on",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "integration_status": "active",
  "integration_version": "1.0",
  "integration_config": "{\"protocol\": \"tcp\", \"port\": 22}",
  "communication_protocol": "SSH",
  "communication_port": 22,
  "communication_frequency": "frequent",
  "communication_type": "synchronous",
  "performance_impact": "medium",
  "latency_contribution": 10.0,
  "bandwidth_usage": 5.0,
  "resource_consumption": 15.0,
  "business_criticality": "high",
  "business_value": "high",
  "alignment_score": 0.9,
  "implementation_priority": "high",
  "implementation_phase": "active",
  "resource_allocation": 25.0,
  "risk_level": "medium",
  "reliability_score": 0.95,
  "failure_impact": "high",
  "recovery_time": 30,
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "logging_level": "info",
  "metrics_collection": "{\"cpu\": true, \"memory\": true, \"disk\": true}",
  "security_requirements": "{\"encryption\": \"required\", \"authentication\": \"required\"}",
  "compliance_impact": "medium",
  "data_protection": "{\"backup\": \"required\", \"retention\": \"7y\"}",
  "performance_contribution": 20.0,
  "success_contribution": 25.0,
  "quality_metrics": "{\"availability\": \"99.9%\", \"performance\": \"excellent\"}",
  "integration_date": null,
  "created_by": "550e8400-e29b-41d4-a716-446655440002",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### List Software Links

**GET** `/api/v1/system-software/{system_software_id}/links`

Lists all links for a system software.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440004",
    "system_software_id": "550e8400-e29b-41d4-a716-446655440000",
    "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
    "linked_element_type": "node",
    "link_type": "runs_on",
    "relationship_strength": "strong",
    "dependency_level": "high",
    "integration_status": "active",
    "integration_version": "1.0",
    "integration_config": "{\"protocol\": \"tcp\", \"port\": 22}",
    "communication_protocol": "SSH",
    "communication_port": 22,
    "communication_frequency": "frequent",
    "communication_type": "synchronous",
    "performance_impact": "medium",
    "latency_contribution": 10.0,
    "bandwidth_usage": 5.0,
    "resource_consumption": 15.0,
    "business_criticality": "high",
    "business_value": "high",
    "alignment_score": 0.9,
    "implementation_priority": "high",
    "implementation_phase": "active",
    "resource_allocation": 25.0,
    "risk_level": "medium",
    "reliability_score": 0.95,
    "failure_impact": "high",
    "recovery_time": 30,
    "monitoring_enabled": true,
    "alerting_enabled": true,
    "logging_level": "info",
    "metrics_collection": "{\"cpu\": true, \"memory\": true, \"disk\": true}",
    "security_requirements": "{\"encryption\": \"required\", \"authentication\": \"required\"}",
    "compliance_impact": "medium",
    "data_protection": "{\"backup\": \"required\", \"retention\": \"7y\"}",
    "performance_contribution": 20.0,
    "success_contribution": 25.0,
    "quality_metrics": "{\"availability\": \"99.9%\", \"performance\": \"excellent\"}",
    "integration_date": null,
    "created_by": "550e8400-e29b-41d4-a716-446655440002",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Software Link

**GET** `/api/v1/system-software/links/{link_id}`

Retrieves a software link by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "system_software_id": "550e8400-e29b-41d4-a716-446655440000",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_type": "node",
  "link_type": "runs_on",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "integration_status": "active",
  "integration_version": "1.0",
  "integration_config": "{\"protocol\": \"tcp\", \"port\": 22}",
  "communication_protocol": "SSH",
  "communication_port": 22,
  "communication_frequency": "frequent",
  "communication_type": "synchronous",
  "performance_impact": "medium",
  "latency_contribution": 10.0,
  "bandwidth_usage": 5.0,
  "resource_consumption": 15.0,
  "business_criticality": "high",
  "business_value": "high",
  "alignment_score": 0.9,
  "implementation_priority": "high",
  "implementation_phase": "active",
  "resource_allocation": 25.0,
  "risk_level": "medium",
  "reliability_score": 0.95,
  "failure_impact": "high",
  "recovery_time": 30,
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "logging_level": "info",
  "metrics_collection": "{\"cpu\": true, \"memory\": true, \"disk\": true}",
  "security_requirements": "{\"encryption\": \"required\", \"authentication\": \"required\"}",
  "compliance_impact": "medium",
  "data_protection": "{\"backup\": \"required\", \"retention\": \"7y\"}",
  "performance_contribution": 20.0,
  "success_contribution": 25.0,
  "quality_metrics": "{\"availability\": \"99.9%\", \"performance\": \"excellent\"}",
  "integration_date": null,
  "created_by": "550e8400-e29b-41d4-a716-446655440002",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Update Software Link

**PUT** `/api/v1/system-software/links/{link_id}`

Updates a software link.

**Request Body:** (All fields optional)
```json
{
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "performance_impact": "low"
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "performance_impact": "low"
}
```

### Delete Software Link

**DELETE** `/api/v1/system-software/links/{link_id}`

Deletes a software link.

**Response:** `204 No Content`

## Analysis & Impact Endpoints

### Get Dependency Map

**GET** `/api/v1/system-software/{system_software_id}/dependency-map`

Returns dependency mapping for the SystemSoftware.

**Response:** `200 OK`
```json
{
  "system_software_id": "550e8400-e29b-41d4-a716-446655440000",
  "dependencies": [
    {
      "name": "openssl",
      "version": "3.0.2",
      "type": "package",
      "status": "active"
    },
    {
      "name": "nginx",
      "version": "1.18.0",
      "type": "package",
      "status": "active"
    }
  ],
  "dependent_components": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440005",
      "name": "web-app",
      "type": "application_component",
      "dependency_level": "high"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440006",
      "name": "api-service",
      "type": "application_component",
      "dependency_level": "medium"
    }
  ],
  "integration_points": [
    {
      "name": "rest-api",
      "protocol": "HTTP",
      "port": 8080,
      "status": "active"
    },
    {
      "name": "grpc-api",
      "protocol": "gRPC",
      "port": 9090,
      "status": "active"
    }
  ],
  "dependency_health": {
    "overall_score": 0.85,
    "status": "healthy",
    "issues": []
  }
}
```

### Get Compliance Check

**GET** `/api/v1/system-software/{system_software_id}/compliance-check`

Returns compliance check for the SystemSoftware.

**Response:** `200 OK`
```json
{
  "system_software_id": "550e8400-e29b-41d4-a716-446655440000",
  "compliance_status": {
    "compliance_rate": 0.85,
    "compliant_items": ["vulnerability", "certifications", "monitoring"],
    "non_compliant_items": ["documentation"],
    "status": "compliant"
  },
  "vulnerability_assessment": {
    "score": 2.5,
    "severity": "low",
    "risk_level": "low",
    "recommendations": ["Continue monitoring", "Apply available patches"]
  },
  "certification_status": {
    "certifications": [
      {
        "name": "ISO 27001",
        "status": "certified",
        "expiry": "2025-01-15T00:00:00Z"
      },
      {
        "name": "SOC 2",
        "status": "certified",
        "expiry": "2024-12-31T00:00:00Z"
      }
    ],
    "certification_count": 2,
    "has_certifications": true
  },
  "compliance_recommendations": [
    "Update documentation to match current configuration",
    "Schedule regular security audits",
    "Implement automated compliance monitoring"
  ]
}
```

### Analyze System Software

**GET** `/api/v1/system-software/{system_software_id}/analysis`

Returns comprehensive analysis for the SystemSoftware.

**Response:** `200 OK`
```json
{
  "system_software_id": "550e8400-e29b-41d4-a716-446655440000",
  "operational_health": {
    "overall_score": 0.9,
    "status": "healthy",
    "issues": []
  },
  "security_status": {
    "security_score": 0.85,
    "status": "secure",
    "issues": []
  },
  "performance_metrics": {
    "resource_usage": 45.5,
    "uptime_percentage": 99.9,
    "response_time_avg": 150.0,
    "cpu_requirements": 2.0,
    "memory_requirements": 4.0,
    "storage_requirements": 20.0,
    "network_requirements": 100.0
  },
  "risk_assessment": {
    "overall_risk": "low",
    "risk_factors": []
  },
  "improvement_opportunities": [
    "Implement automated backup verification",
    "Add more comprehensive monitoring",
    "Document disaster recovery procedures"
  ],
  "compliance_status": {
    "compliance_rate": 0.85,
    "compliant_items": ["vulnerability", "certifications", "monitoring"],
    "non_compliant_items": ["documentation"],
    "status": "compliant"
  }
}
```

## Domain-Specific Query Endpoints

### Get by Software Type

**GET** `/api/v1/system-software/by-type/{software_type}`

Returns system software filtered by type.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Ubuntu 22.04 LTS",
    "software_type": "os",
    "version": "22.04.3",
    "status": "active"
  }
]
```

### Get by Vendor

**GET** `/api/v1/system-software/by-vendor/{vendor}`

Returns system software filtered by vendor.

### Get by Vulnerability Score

**GET** `/api/v1/system-software/by-vulnerability/{max_score}`

Returns system software with vulnerability score below threshold.

### Get by Lifecycle State

**GET** `/api/v1/system-software/by-lifecycle/{lifecycle_state}`

Returns system software filtered by lifecycle state.

### Get Active System Software

**GET** `/api/v1/system-software/active`

Returns all active system software.

### Get Critical System Software

**GET** `/api/v1/system-software/critical`

Returns critical system software (high vulnerability or business critical).

## Enumeration Endpoints

### Get Software Types

**GET** `/api/v1/system-software/software-types`

Returns all available software types.

**Response:** `200 OK`
```json
[
  "os",
  "database",
  "middleware",
  "runtime",
  "container_engine"
]
```

### Get License Types

**GET** `/api/v1/system-software/license-types`

Returns all available license types.

**Response:** `200 OK`
```json
[
  "proprietary",
  "open_source",
  "commercial",
  "freeware"
]
```

### Get Lifecycle States

**GET** `/api/v1/system-software/lifecycle-states`

Returns all available lifecycle states.

**Response:** `200 OK`
```json
[
  "active",
  "inactive",
  "deprecated",
  "end_of_life",
  "planned"
]
```

### Get Compliance Statuses

**GET** `/api/v1/system-software/compliance-statuses`

Returns all available compliance statuses.

**Response:** `200 OK`
```json
[
  "compliant",
  "non_compliant",
  "unknown",
  "pending"
]
```

### Get Update Channels

**GET** `/api/v1/system-software/update-channels`

Returns all available update channels.

**Response:** `200 OK`
```json
[
  "stable",
  "beta",
  "alpha",
  "lts"
]
```

### Get Update Frequencies

**GET** `/api/v1/system-software/update-frequencies`

Returns all available update frequencies.

**Response:** `200 OK`
```json
[
  "daily",
  "weekly",
  "monthly",
  "quarterly",
  "yearly"
]
```

### Get Deployment Environments

**GET** `/api/v1/system-software/deployment-environments`

Returns all available deployment environments.

**Response:** `200 OK`
```json
[
  "production",
  "staging",
  "development",
  "testing"
]
```

### Get Support Levels

**GET** `/api/v1/system-software/support-levels`

Returns all available support levels.

**Response:** `200 OK`
```json
[
  "basic",
  "standard",
  "premium",
  "enterprise"
]
```

## Link-specific Enumeration Endpoints

### Get Link Types

**GET** `/api/v1/system-software/link-types`

Returns all available link types.

**Response:** `200 OK`
```json
[
  "runs_on",
  "depends_on",
  "integrates_with",
  "manages",
  "supports"
]
```

### Get Relationship Strengths

**GET** `/api/v1/system-software/relationship-strengths`

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

**GET** `/api/v1/system-software/dependency-levels`

Returns all available dependency levels.

**Response:** `200 OK`
```json
[
  "high",
  "medium",
  "low"
]
```

### Get Integration Statuses

**GET** `/api/v1/system-software/integration-statuses`

Returns all available integration statuses.

**Response:** `200 OK`
```json
[
  "active",
  "inactive",
  "failed",
  "pending",
  "deprecated"
]
```

### Get Communication Frequencies

**GET** `/api/v1/system-software/communication-frequencies`

Returns all available communication frequencies.

**Response:** `200 OK`
```json
[
  "frequent",
  "regular",
  "occasional",
  "rare"
]
```

### Get Communication Types

**GET** `/api/v1/system-software/communication-types`

Returns all available communication types.

**Response:** `200 OK`
```json
[
  "synchronous",
  "asynchronous",
  "batch",
  "real_time"
]
```

### Get Performance Impacts

**GET** `/api/v1/system-software/performance-impacts`

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

### Get Business Values

**GET** `/api/v1/system-software/business-values`

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

### Get Business Criticalities

**GET** `/api/v1/system-software/business-criticalities`

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

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error: Invalid software type"
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
  "detail": "Insufficient permissions. Required: system_software:create, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "System software not found"
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
- Software type
- Vendor (contains)
- Lifecycle state
- Vulnerability threshold

## Sorting

Results are sorted by `created_at` in descending order by default.

## OpenAPI Documentation

For complete OpenAPI documentation, visit:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`
