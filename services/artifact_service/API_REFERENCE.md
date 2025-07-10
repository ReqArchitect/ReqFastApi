# API Reference: artifact_service

## Overview

The Artifact Service provides comprehensive management of ArchiMate 3.2 Artifact elements with full CRUD operations, relationship management, analysis capabilities, and domain-specific queries.

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

## Artifact Management

### Create Artifact

**POST** `/api/v1/artifacts/`

Creates a new Artifact.

**Request Body:**
```json
{
  "name": "User Authentication Service",
  "description": "Spring Boot application for user authentication",
  "artifact_type": "container",
  "version": "1.2.0",
  "format": "docker",
  "storage_location": "registry.example.com/auth-service:1.2.0",
  "checksum": "sha256:abc123def456",
  "build_tool": "docker",
  "deployment_target_node_id": "550e8400-e29b-41d4-a716-446655440000",
  "associated_component_id": "550e8400-e29b-41d4-a716-446655440001",
  "lifecycle_state": "active",
  "size_mb": 150.5,
  "file_count": 25,
  "compression_ratio": 0.8,
  "deployment_environment": "production",
  "integrity_verified": true,
  "security_scan_passed": true,
  "vulnerability_count": 0,
  "security_score": 9.2,
  "dependencies": "[{\"name\": \"spring-boot\", \"version\": \"2.7.0\"}]",
  "dependent_artifacts": "[{\"name\": \"frontend-app\", \"version\": \"1.0.0\"}]",
  "build_dependencies": "[{\"name\": \"maven\", \"version\": \"3.8.0\"}]",
  "configuration": "{\"port\": 8080, \"database\": \"postgresql\"}",
  "metadata": "{\"team\": \"auth-team\", \"project\": \"user-management\"}",
  "tags": "[\"authentication\", \"security\", \"microservice\"]",
  "access_level": "read",
  "public_access": false,
  "backup_enabled": true,
  "version_control_system": "git",
  "repository_url": "https://github.com/company/auth-service",
  "branch_name": "main",
  "commit_hash": "abc123def456",
  "performance_metrics": "{\"response_time\": \"200ms\", \"throughput\": \"1000 req/s\"}",
  "load_time_avg": 200.0,
  "memory_usage": 512.0,
  "cpu_usage": 15.5,
  "compliance_status": "compliant",
  "audit_requirements": "{\"sox\": true, \"gdpr\": true}",
  "retention_policy": "{\"retention_days\": 90, \"archive_after\": 30}",
  "data_classification": "internal",
  "quality_score": 0.95,
  "test_coverage": 85.0,
  "code_quality_metrics": "{\"complexity\": \"low\", \"duplication\": \"5%\"}",
  "documentation_status": "complete",
  "operational_hours": "24x7",
  "maintenance_window": "Sunday 2-4 AM UTC",
  "incident_count": 0,
  "license_type": "open_source",
  "license_cost": 0.0,
  "usage_metrics": "{\"deployments\": 15, \"users\": 1000}"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440003",
  "user_id": "550e8400-e29b-41d4-a716-446655440004",
  "name": "User Authentication Service",
  "description": "Spring Boot application for user authentication",
  "artifact_type": "container",
  "version": "1.2.0",
  "format": "docker",
  "storage_location": "registry.example.com/auth-service:1.2.0",
  "checksum": "sha256:abc123def456",
  "build_tool": "docker",
  "deployment_target_node_id": "550e8400-e29b-41d4-a716-446655440000",
  "associated_component_id": "550e8400-e29b-41d4-a716-446655440001",
  "lifecycle_state": "active",
  "size_mb": 150.5,
  "file_count": 25,
  "compression_ratio": 0.8,
  "deployment_environment": "production",
  "integrity_verified": true,
  "security_scan_passed": true,
  "vulnerability_count": 0,
  "security_score": 9.2,
  "dependencies": "[{\"name\": \"spring-boot\", \"version\": \"2.7.0\"}]",
  "dependent_artifacts": "[{\"name\": \"frontend-app\", \"version\": \"1.0.0\"}]",
  "build_dependencies": "[{\"name\": \"maven\", \"version\": \"3.8.0\"}]",
  "configuration": "{\"port\": 8080, \"database\": \"postgresql\"}",
  "metadata": "{\"team\": \"auth-team\", \"project\": \"user-management\"}",
  "tags": "[\"authentication\", \"security\", \"microservice\"]",
  "access_level": "read",
  "public_access": false,
  "backup_enabled": true,
  "version_control_system": "git",
  "repository_url": "https://github.com/company/auth-service",
  "branch_name": "main",
  "commit_hash": "abc123def456",
  "performance_metrics": "{\"response_time\": \"200ms\", \"throughput\": \"1000 req/s\"}",
  "load_time_avg": 200.0,
  "memory_usage": 512.0,
  "cpu_usage": 15.5,
  "compliance_status": "compliant",
  "audit_requirements": "{\"sox\": true, \"gdpr\": true}",
  "retention_policy": "{\"retention_days\": 90, \"archive_after\": 30}",
  "data_classification": "internal",
  "quality_score": 0.95,
  "test_coverage": 85.0,
  "code_quality_metrics": "{\"complexity\": \"low\", \"duplication\": \"5%\"}",
  "documentation_status": "complete",
  "operational_hours": "24x7",
  "maintenance_window": "Sunday 2-4 AM UTC",
  "incident_count": 0,
  "license_type": "open_source",
  "license_cost": 0.0,
  "usage_metrics": "{\"deployments\": 15, \"users\": 1000}",
  "owner_user_id": "550e8400-e29b-41d4-a716-446655440004",
  "build_date": null,
  "deployment_date": null,
  "last_modified": "2024-01-15T10:30:00Z",
  "last_deployed": null,
  "last_incident": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### List Artifacts

**GET** `/api/v1/artifacts/`

Lists all Artifacts for the tenant with filtering and pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)
- `artifact_type` (string, optional): Filter by artifact type
- `lifecycle_state` (string, optional): Filter by lifecycle state
- `deployment_environment` (string, optional): Filter by deployment environment
- `format_filter` (string, optional): Filter by format (contains)
- `deployment_target_node_id` (UUID, optional): Filter by deployment target node
- `associated_component_id` (UUID, optional): Filter by associated component
- `integrity_verified` (boolean, optional): Filter by integrity verification status
- `security_scan_passed` (boolean, optional): Filter by security scan status
- `compliance_status` (string, optional): Filter by compliance status
- `data_classification` (string, optional): Filter by data classification
- `size_threshold` (float, optional): Filter by maximum size in MB
- `vulnerability_threshold` (int, optional): Filter by maximum vulnerability count
- `quality_threshold` (float, optional): Filter by minimum quality score
- `search_term` (string, optional): Search in name, description, and storage location

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440003",
    "user_id": "550e8400-e29b-41d4-a716-446655440004",
    "name": "User Authentication Service",
    "description": "Spring Boot application for user authentication",
    "artifact_type": "container",
    "version": "1.2.0",
    "format": "docker",
    "storage_location": "registry.example.com/auth-service:1.2.0",
    "checksum": "sha256:abc123def456",
    "build_tool": "docker",
    "deployment_target_node_id": "550e8400-e29b-41d4-a716-446655440000",
    "associated_component_id": "550e8400-e29b-41d4-a716-446655440001",
    "lifecycle_state": "active",
    "size_mb": 150.5,
    "file_count": 25,
    "compression_ratio": 0.8,
    "deployment_environment": "production",
    "integrity_verified": true,
    "security_scan_passed": true,
    "vulnerability_count": 0,
    "security_score": 9.2,
    "access_level": "read",
    "public_access": false,
    "backup_enabled": true,
    "version_control_system": "git",
    "repository_url": "https://github.com/company/auth-service",
    "branch_name": "main",
    "commit_hash": "abc123def456",
    "load_time_avg": 200.0,
    "memory_usage": 512.0,
    "cpu_usage": 15.5,
    "compliance_status": "compliant",
    "data_classification": "internal",
    "quality_score": 0.95,
    "test_coverage": 85.0,
    "documentation_status": "complete",
    "operational_hours": "24x7",
    "incident_count": 0,
    "license_type": "open_source",
    "license_cost": 0.0,
    "owner_user_id": "550e8400-e29b-41d4-a716-446655440004",
    "build_date": null,
    "deployment_date": null,
    "last_modified": "2024-01-15T10:30:00Z",
    "last_deployed": null,
    "last_incident": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Artifact

**GET** `/api/v1/artifacts/{artifact_id}`

Retrieves an Artifact by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440003",
  "user_id": "550e8400-e29b-41d4-a716-446655440004",
  "name": "User Authentication Service",
  "description": "Spring Boot application for user authentication",
  "artifact_type": "container",
  "version": "1.2.0",
  "format": "docker",
  "storage_location": "registry.example.com/auth-service:1.2.0",
  "checksum": "sha256:abc123def456",
  "build_tool": "docker",
  "deployment_target_node_id": "550e8400-e29b-41d4-a716-446655440000",
  "associated_component_id": "550e8400-e29b-41d4-a716-446655440001",
  "lifecycle_state": "active",
  "size_mb": 150.5,
  "file_count": 25,
  "compression_ratio": 0.8,
  "deployment_environment": "production",
  "integrity_verified": true,
  "security_scan_passed": true,
  "vulnerability_count": 0,
  "security_score": 9.2,
  "dependencies": "[{\"name\": \"spring-boot\", \"version\": \"2.7.0\"}]",
  "dependent_artifacts": "[{\"name\": \"frontend-app\", \"version\": \"1.0.0\"}]",
  "build_dependencies": "[{\"name\": \"maven\", \"version\": \"3.8.0\"}]",
  "configuration": "{\"port\": 8080, \"database\": \"postgresql\"}",
  "metadata": "{\"team\": \"auth-team\", \"project\": \"user-management\"}",
  "tags": "[\"authentication\", \"security\", \"microservice\"]",
  "access_level": "read",
  "public_access": false,
  "backup_enabled": true,
  "version_control_system": "git",
  "repository_url": "https://github.com/company/auth-service",
  "branch_name": "main",
  "commit_hash": "abc123def456",
  "performance_metrics": "{\"response_time\": \"200ms\", \"throughput\": \"1000 req/s\"}",
  "load_time_avg": 200.0,
  "memory_usage": 512.0,
  "cpu_usage": 15.5,
  "compliance_status": "compliant",
  "audit_requirements": "{\"sox\": true, \"gdpr\": true}",
  "retention_policy": "{\"retention_days\": 90, \"archive_after\": 30}",
  "data_classification": "internal",
  "quality_score": 0.95,
  "test_coverage": 85.0,
  "code_quality_metrics": "{\"complexity\": \"low\", \"duplication\": \"5%\"}",
  "documentation_status": "complete",
  "operational_hours": "24x7",
  "maintenance_window": "Sunday 2-4 AM UTC",
  "incident_count": 0,
  "license_type": "open_source",
  "license_cost": 0.0,
  "usage_metrics": "{\"deployments\": 15, \"users\": 1000}",
  "owner_user_id": "550e8400-e29b-41d4-a716-446655440004",
  "build_date": null,
  "deployment_date": null,
  "last_modified": "2024-01-15T10:30:00Z",
  "last_deployed": null,
  "last_incident": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Update Artifact

**PUT** `/api/v1/artifacts/{artifact_id}`

Updates an Artifact.

**Request Body:** (All fields optional)
```json
{
  "name": "Enhanced User Authentication Service",
  "description": "Updated description with enhanced security features",
  "version": "1.2.1",
  "security_score": 9.5,
  "quality_score": 0.98,
  "test_coverage": 90.0
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "name": "Enhanced User Authentication Service",
  "description": "Updated description with enhanced security features",
  "version": "1.2.1",
  "security_score": 9.5,
  "quality_score": 0.98,
  "test_coverage": 90.0,
  "updated_at": "2024-01-15T11:30:00Z"
}
```

### Delete Artifact

**DELETE** `/api/v1/artifacts/{artifact_id}`

Deletes an Artifact.

**Response:** `204 No Content`

## Artifact Link Management

### Create Artifact Link

**POST** `/api/v1/artifacts/{artifact_id}/links`

Creates a link between an artifact and another element.

**Request Body:**
```json
{
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440005",
  "linked_element_type": "application_component",
  "link_type": "implements",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "implementation_status": "active",
  "implementation_date": "2024-01-15T10:30:00Z",
  "implementation_version": "1.0.0",
  "implementation_config": "{\"deployment_method\": \"blue-green\"}",
  "deployment_status": "deployed",
  "deployment_date": "2024-01-15T10:30:00Z",
  "deployment_environment": "production",
  "deployment_method": "blue_green",
  "communication_protocol": "HTTP",
  "communication_port": 8080,
  "communication_frequency": "frequent",
  "communication_type": "synchronous",
  "performance_impact": "medium",
  "latency_contribution": 50.0,
  "bandwidth_usage": 10.5,
  "resource_consumption": 25.0,
  "business_criticality": "high",
  "business_value": "high",
  "alignment_score": 0.9,
  "implementation_priority": "high",
  "implementation_phase": "active",
  "resource_allocation": 30.0,
  "risk_level": "medium",
  "reliability_score": 0.95,
  "failure_impact": "medium",
  "recovery_time": 15,
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "logging_level": "info",
  "metrics_collection": "{\"metrics\": \"prometheus\", \"alerts\": \"grafana\"}",
  "security_requirements": "{\"encryption\": \"required\", \"authentication\": \"required\"}",
  "compliance_impact": "medium",
  "data_protection": "{\"gdpr\": true, \"sox\": true}",
  "performance_contribution": 25.0,
  "success_contribution": 30.0,
  "quality_metrics": "{\"availability\": \"99.9%\", \"performance\": \"excellent\"}"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440006",
  "artifact_id": "550e8400-e29b-41d4-a716-446655440002",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440005",
  "linked_element_type": "application_component",
  "link_type": "implements",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "implementation_status": "active",
  "implementation_date": "2024-01-15T10:30:00Z",
  "implementation_version": "1.0.0",
  "implementation_config": "{\"deployment_method\": \"blue-green\"}",
  "deployment_status": "deployed",
  "deployment_date": "2024-01-15T10:30:00Z",
  "deployment_environment": "production",
  "deployment_method": "blue_green",
  "communication_protocol": "HTTP",
  "communication_port": 8080,
  "communication_frequency": "frequent",
  "communication_type": "synchronous",
  "performance_impact": "medium",
  "latency_contribution": 50.0,
  "bandwidth_usage": 10.5,
  "resource_consumption": 25.0,
  "business_criticality": "high",
  "business_value": "high",
  "alignment_score": 0.9,
  "implementation_priority": "high",
  "implementation_phase": "active",
  "resource_allocation": 30.0,
  "risk_level": "medium",
  "reliability_score": 0.95,
  "failure_impact": "medium",
  "recovery_time": 15,
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "logging_level": "info",
  "metrics_collection": "{\"metrics\": \"prometheus\", \"alerts\": \"grafana\"}",
  "security_requirements": "{\"encryption\": \"required\", \"authentication\": \"required\"}",
  "compliance_impact": "medium",
  "data_protection": "{\"gdpr\": true, \"sox\": true}",
  "performance_contribution": 25.0,
  "success_contribution": 30.0,
  "quality_metrics": "{\"availability\": \"99.9%\", \"performance\": \"excellent\"}",
  "created_by": "550e8400-e29b-41d4-a716-446655440004",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### List Artifact Links

**GET** `/api/v1/artifacts/{artifact_id}/links`

Lists all links for an artifact.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440006",
    "artifact_id": "550e8400-e29b-41d4-a716-446655440002",
    "linked_element_id": "550e8400-e29b-41d4-a716-446655440005",
    "linked_element_type": "application_component",
    "link_type": "implements",
    "relationship_strength": "strong",
    "dependency_level": "high",
    "implementation_status": "active",
    "deployment_status": "deployed",
    "deployment_environment": "production",
    "communication_frequency": "frequent",
    "communication_type": "synchronous",
    "performance_impact": "medium",
    "business_criticality": "high",
    "business_value": "high",
    "risk_level": "medium",
    "monitoring_enabled": true,
    "alerting_enabled": true,
    "logging_level": "info",
    "created_by": "550e8400-e29b-41d4-a716-446655440004",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Artifact Link

**GET** `/api/v1/artifacts/links/{link_id}`

Retrieves an artifact link by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440006",
  "artifact_id": "550e8400-e29b-41d4-a716-446655440002",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440005",
  "linked_element_type": "application_component",
  "link_type": "implements",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "implementation_status": "active",
  "implementation_date": "2024-01-15T10:30:00Z",
  "implementation_version": "1.0.0",
  "implementation_config": "{\"deployment_method\": \"blue-green\"}",
  "deployment_status": "deployed",
  "deployment_date": "2024-01-15T10:30:00Z",
  "deployment_environment": "production",
  "deployment_method": "blue_green",
  "communication_protocol": "HTTP",
  "communication_port": 8080,
  "communication_frequency": "frequent",
  "communication_type": "synchronous",
  "performance_impact": "medium",
  "latency_contribution": 50.0,
  "bandwidth_usage": 10.5,
  "resource_consumption": 25.0,
  "business_criticality": "high",
  "business_value": "high",
  "alignment_score": 0.9,
  "implementation_priority": "high",
  "implementation_phase": "active",
  "resource_allocation": 30.0,
  "risk_level": "medium",
  "reliability_score": 0.95,
  "failure_impact": "medium",
  "recovery_time": 15,
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "logging_level": "info",
  "metrics_collection": "{\"metrics\": \"prometheus\", \"alerts\": \"grafana\"}",
  "security_requirements": "{\"encryption\": \"required\", \"authentication\": \"required\"}",
  "compliance_impact": "medium",
  "data_protection": "{\"gdpr\": true, \"sox\": true}",
  "performance_contribution": 25.0,
  "success_contribution": 30.0,
  "quality_metrics": "{\"availability\": \"99.9%\", \"performance\": \"excellent\"}",
  "created_by": "550e8400-e29b-41d4-a716-446655440004",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Update Artifact Link

**PUT** `/api/v1/artifacts/links/{link_id}`

Updates an artifact link.

**Request Body:** (All fields optional)
```json
{
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "performance_impact": "low",
  "alignment_score": 0.8
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440006",
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "performance_impact": "low",
  "alignment_score": 0.8
}
```

### Delete Artifact Link

**DELETE** `/api/v1/artifacts/links/{link_id}`

Deletes an artifact link.

**Response:** `204 No Content`

## Analysis Endpoints

### Get Dependency Map

**GET** `/api/v1/artifacts/{artifact_id}/dependency-map`

Returns dependency mapping for the Artifact.

**Response:** `200 OK`
```json
{
  "artifact_id": "550e8400-e29b-41d4-a716-446655440002",
  "direct_dependencies": [
    {
      "name": "spring-boot",
      "version": "2.7.0",
      "type": "framework"
    }
  ],
  "indirect_dependencies": [
    {
      "name": "spring-core",
      "version": "5.3.20",
      "type": "library"
    }
  ],
  "dependency_tree": {
    "artifact_id": "550e8400-e29b-41d4-a716-446655440002",
    "name": "User Authentication Service",
    "type": "container",
    "direct_dependencies": [
      {
        "name": "spring-boot",
        "version": "2.7.0"
      }
    ],
    "dependent_artifacts": [
      {
        "name": "frontend-app",
        "version": "1.0.0"
      }
    ],
    "build_dependencies": [
      {
        "name": "maven",
        "version": "3.8.0"
      }
    ]
  },
  "circular_dependencies": [],
  "total_dependencies": 3,
  "max_depth": 2
}
```

### Check Integrity

**GET** `/api/v1/artifacts/{artifact_id}/integrity-check`

Returns integrity check results for the Artifact.

**Response:** `200 OK`
```json
{
  "artifact_id": "550e8400-e29b-41d4-a716-446655440002",
  "checksum_valid": true,
  "security_scan_passed": true,
  "vulnerability_count": 0,
  "security_score": 9.2,
  "integrity_score": 0.95,
  "compliance_status": "compliant",
  "recommendations": [
    "Consider implementing additional security scanning",
    "Update dependencies to latest versions"
  ],
  "issues": [
    {
      "type": "security",
      "severity": "low",
      "description": "Minor security improvements recommended"
    }
  ]
}
```

## Domain-Specific Query Endpoints

### Get by Artifact Type

**GET** `/api/v1/artifacts/by-type/{artifact_type}`

Returns artifacts filtered by type.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "name": "User Authentication Service",
    "artifact_type": "container",
    "version": "1.2.0",
    "lifecycle_state": "active"
  }
]
```

### Get by Format

**GET** `/api/v1/artifacts/by-format/{format_filter}`

Returns artifacts filtered by format.

### Get by Deployment Target

**GET** `/api/v1/artifacts/by-deployment-target/{node_id}`

Returns artifacts filtered by deployment target node.

### Get by Component

**GET** `/api/v1/artifacts/by-component/{component_id}`

Returns artifacts filtered by associated component.

### Get by Modification Date

**GET** `/api/v1/artifacts/by-modification-date/{start_date}/{end_date}`

Returns artifacts modified between dates.

### Get Active Artifacts

**GET** `/api/v1/artifacts/active`

Returns all active artifacts.

### Get Critical Artifacts

**GET** `/api/v1/artifacts/critical`

Returns all critical artifacts.

### Get Statistics

**GET** `/api/v1/artifacts/statistics`

Returns artifact statistics for tenant.

**Response:** `200 OK`
```json
{
  "total_artifacts": 150,
  "active_artifacts": 120,
  "verified_artifacts": 100,
  "secure_artifacts": 95,
  "avg_size_mb": 250.5,
  "total_size_mb": 37575.0,
  "avg_security_score": 8.5,
  "avg_quality_score": 0.85
}
```

## Link Query Endpoints

### Get Links by Element

**GET** `/api/v1/artifacts/links/by-element/{element_type}/{element_id}`

Returns artifact links filtered by linked element.

### Get Links by Type

**GET** `/api/v1/artifacts/links/by-type/{link_type}`

Returns artifact links filtered by link type.

## Enumeration Endpoints

### Get Artifact Types

**GET** `/api/v1/artifacts/artifact-types`

Returns all available artifact types.

**Response:** `200 OK`
```json
{
  "values": [
    "source",
    "build",
    "image",
    "config",
    "script",
    "binary",
    "container",
    "package",
    "library",
    "framework"
  ]
}
```

### Get Lifecycle States

**GET** `/api/v1/artifacts/lifecycle-states`

Returns all available lifecycle states.

**Response:** `200 OK`
```json
{
  "values": [
    "active",
    "inactive",
    "deprecated",
    "archived",
    "deleted",
    "planned",
    "development",
    "testing"
  ]
}
```

### Get Deployment Environments

**GET** `/api/v1/artifacts/deployment-environments`

Returns all available deployment environments.

**Response:** `200 OK`
```json
{
  "values": [
    "production",
    "staging",
    "development",
    "testing",
    "sandbox"
  ]
}
```

### Get Access Levels

**GET** `/api/v1/artifacts/access-levels`

Returns all available access levels.

**Response:** `200 OK`
```json
{
  "values": [
    "read",
    "write",
    "admin"
  ]
}
```

### Get Compliance Statuses

**GET** `/api/v1/artifacts/compliance-statuses`

Returns all available compliance statuses.

**Response:** `200 OK`
```json
{
  "values": [
    "compliant",
    "non_compliant",
    "unknown",
    "pending"
  ]
}
```

### Get Data Classifications

**GET** `/api/v1/artifacts/data-classifications`

Returns all available data classifications.

**Response:** `200 OK`
```json
{
  "values": [
    "public",
    "internal",
    "confidential",
    "restricted"
  ]
}
```

### Get Documentation Statuses

**GET** `/api/v1/artifacts/documentation-statuses`

Returns all available documentation statuses.

**Response:** `200 OK`
```json
{
  "values": [
    "complete",
    "incomplete",
    "missing"
  ]
}
```

### Get Operational Hours

**GET** `/api/v1/artifacts/operational-hours`

Returns all available operational hour types.

**Response:** `200 OK`
```json
{
  "values": [
    "24x7",
    "business_hours",
    "on_demand"
  ]
}
```

### Get Link Types

**GET** `/api/v1/artifacts/link-types`

Returns all available link types.

**Response:** `200 OK`
```json
{
  "values": [
    "implements",
    "deployed_on",
    "depends_on",
    "contains",
    "configures",
    "supports",
    "enables",
    "governed_by"
  ]
}
```

### Get Relationship Strengths

**GET** `/api/v1/artifacts/relationship-strengths`

Returns all available relationship strengths.

**Response:** `200 OK`
```json
{
  "values": [
    "strong",
    "medium",
    "weak"
  ]
}
```

### Get Dependency Levels

**GET** `/api/v1/artifacts/dependency-levels`

Returns all available dependency levels.

**Response:** `200 OK`
```json
{
  "values": [
    "high",
    "medium",
    "low"
  ]
}
```

### Get Implementation Statuses

**GET** `/api/v1/artifacts/implementation-statuses`

Returns all available implementation statuses.

**Response:** `200 OK`
```json
{
  "values": [
    "active",
    "inactive",
    "failed",
    "pending",
    "deprecated"
  ]
}
```

### Get Deployment Statuses

**GET** `/api/v1/artifacts/deployment-statuses`

Returns all available deployment statuses.

**Response:** `200 OK`
```json
{
  "values": [
    "deployed",
    "pending",
    "failed",
    "rolled_back"
  ]
}
```

### Get Communication Frequencies

**GET** `/api/v1/artifacts/communication-frequencies`

Returns all available communication frequencies.

**Response:** `200 OK`
```json
{
  "values": [
    "frequent",
    "regular",
    "occasional",
    "rare"
  ]
}
```

### Get Communication Types

**GET** `/api/v1/artifacts/communication-types`

Returns all available communication types.

**Response:** `200 OK`
```json
{
  "values": [
    "synchronous",
    "asynchronous",
    "batch",
    "real_time"
  ]
}
```

### Get Performance Impacts

**GET** `/api/v1/artifacts/performance-impacts`

Returns all available performance impact levels.

**Response:** `200 OK`
```json
{
  "values": [
    "low",
    "medium",
    "high",
    "critical"
  ]
}
```

### Get Business Criticalities

**GET** `/api/v1/artifacts/business-criticalities`

Returns all available business criticality levels.

**Response:** `200 OK`
```json
{
  "values": [
    "low",
    "medium",
    "high",
    "critical"
  ]
}
```

### Get Risk Levels

**GET** `/api/v1/artifacts/risk-levels`

Returns all available risk levels.

**Response:** `200 OK`
```json
{
  "values": [
    "low",
    "medium",
    "high",
    "critical"
  ]
}
```

### Get Logging Levels

**GET** `/api/v1/artifacts/logging-levels`

Returns all available logging levels.

**Response:** `200 OK`
```json
{
  "values": [
    "debug",
    "info",
    "warning",
    "error"
  ]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error: Invalid artifact type"
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
  "detail": "Insufficient permissions. Required: artifact:create, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Artifact not found"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
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
- Artifact type
- Lifecycle state
- Deployment environment
- Format (contains)
- Deployment target node
- Associated component
- Integrity verification status
- Security scan status
- Compliance status
- Data classification
- Size threshold
- Vulnerability threshold
- Quality threshold
- Search term (name, description, storage location)

## Sorting

Results are sorted by `created_at` in descending order by default.

## OpenAPI Documentation

For complete OpenAPI documentation, visit:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`
