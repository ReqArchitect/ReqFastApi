# API Reference: node_service

## Overview

The Node Service provides comprehensive management of ArchiMate 3.2 Node elements with full CRUD operations, relationship management, analysis capabilities, and domain-specific queries.

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

## Node Management

### Create Node

**POST** `/nodes`

Creates a new Node.

**Request Body:**
```json
{
  "name": "Production Web Server",
  "description": "Primary web server for production environment",
  "node_type": "vm",
  "environment": "production",
  "operating_system": "Ubuntu 20.04",
  "hardware_spec": "{\"cpu\": \"8 cores\", \"memory\": \"16GB\"}",
  "region": "us-east-1",
  "availability_zone": "us-east-1a",
  "cluster_id": "550e8400-e29b-41d4-a716-446655440000",
  "host_capabilities": "{\"gpu\": false, \"ssd\": true}",
  "deployed_components": "{\"web_app\": \"v2.1.0\", \"database\": \"v1.5.2\"}",
  "availability_target": 99.9,
  "lifecycle_state": "active",
  "cpu_cores": 8,
  "memory_gb": 16.0,
  "storage_gb": 500.0,
  "network_bandwidth_mbps": 1000.0,
  "ip_address": "192.168.1.100",
  "mac_address": "00:1B:44:11:3A:B7",
  "hostname": "web-server-01",
  "domain": "example.com",
  "subnet": "192.168.1.0/24",
  "gateway": "192.168.1.1",
  "dns_servers": "[\"8.8.8.8\", \"8.8.4.4\"]",
  "cloud_provider": "AWS",
  "cloud_instance_id": "i-1234567890abcdef0",
  "cloud_instance_type": "t3.large",
  "cloud_tags": "{\"Environment\": \"Production\", \"Team\": \"Web\"}",
  "security_level": "high",
  "compliance_requirements": "{\"gdpr\": true, \"sox\": true}",
  "encryption_enabled": true,
  "backup_enabled": true,
  "monitoring_enabled": true,
  "maintenance_window": "Sunday 2-4 AM UTC",
  "monthly_cost": 150.0,
  "cost_center": "IT-Infrastructure",
  "resource_pool": "Production-Pool",
  "capacity_planning": "{\"growth_rate\": \"15%\", \"upgrade_planned\": \"2024-Q2\"}",
  "network_interfaces": "{\"eth0\": \"192.168.1.100\", \"eth1\": \"10.0.0.100\"}",
  "firewall_rules": "{\"inbound\": [\"80\", \"443\"], \"outbound\": [\"all\"]}",
  "load_balancer_config": "{\"health_check\": \"/health\", \"session_affinity\": true}",
  "vpn_config": "{\"enabled\": true, \"type\": \"IPSec\"}",
  "container_runtime": "Docker",
  "virtualization_type": "VM",
  "hypervisor": "VMware ESXi",
  "container_orchestrator": "Kubernetes"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "name": "Production Web Server",
  "description": "Primary web server for production environment",
  "node_type": "vm",
  "environment": "production",
  "region": "us-east-1",
  "availability_target": 99.9,
  "current_availability": 100.0,
  "resource_utilization": 75.5,
  "lifecycle_state": "active",
  "cpu_cores": 8,
  "cpu_usage_pct": 65.2,
  "memory_gb": 16.0,
  "memory_usage_pct": 78.9,
  "storage_gb": 500.0,
  "storage_usage_pct": 45.3,
  "network_bandwidth_mbps": 1000.0,
  "network_usage_pct": 32.1,
  "ip_address": "192.168.1.100",
  "mac_address": "00:1B:44:11:3A:B7",
  "hostname": "web-server-01",
  "domain": "example.com",
  "subnet": "192.168.1.0/24",
  "gateway": "192.168.1.1",
  "dns_servers": "[\"8.8.8.8\", \"8.8.4.4\"]",
  "cloud_provider": "AWS",
  "cloud_instance_id": "i-1234567890abcdef0",
  "cloud_instance_type": "t3.large",
  "cloud_tags": "{\"Environment\": \"Production\", \"Team\": \"Web\"}",
  "security_level": "high",
  "compliance_requirements": "{\"gdpr\": true, \"sox\": true}",
  "encryption_enabled": true,
  "backup_enabled": true,
  "monitoring_enabled": true,
  "maintenance_window": "Sunday 2-4 AM UTC",
  "last_maintenance": null,
  "next_maintenance": null,
  "incident_count": 0,
  "last_incident": null,
  "sla_breaches": 0,
  "monthly_cost": 150.0,
  "cost_center": "IT-Infrastructure",
  "resource_pool": "Production-Pool",
  "capacity_planning": "{\"growth_rate\": \"15%\", \"upgrade_planned\": \"2024-Q2\"}",
  "network_interfaces": "{\"eth0\": \"192.168.1.100\", \"eth1\": \"10.0.0.100\"}",
  "firewall_rules": "{\"inbound\": [\"80\", \"443\"], \"outbound\": [\"all\"]}",
  "load_balancer_config": "{\"health_check\": \"/health\", \"session_affinity\": true}",
  "vpn_config": "{\"enabled\": true, \"type\": \"IPSec\"}",
  "container_runtime": "Docker",
  "virtualization_type": "VM",
  "hypervisor": "VMware ESXi",
  "container_orchestrator": "Kubernetes",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### List Nodes

**GET** `/nodes`

Lists all Nodes for the tenant with filtering and pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)
- `node_type` (string, optional): Filter by node type
- `environment` (string, optional): Filter by environment
- `lifecycle_state` (string, optional): Filter by lifecycle state
- `region` (string, optional): Filter by region
- `security_level` (string, optional): Filter by security level
- `cluster_id` (UUID, optional): Filter by cluster ID
- `performance_threshold` (float, optional): Filter by minimum availability

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440002",
    "name": "Production Web Server",
    "description": "Primary web server for production environment",
    "node_type": "vm",
    "environment": "production",
    "region": "us-east-1",
    "availability_target": 99.9,
    "current_availability": 100.0,
    "lifecycle_state": "active",
    "cpu_cores": 8,
    "memory_gb": 16.0,
    "security_level": "high",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Node

**GET** `/nodes/{node_id}`

Retrieves a Node by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440002",
  "name": "Production Web Server",
  "description": "Primary web server for production environment",
  "node_type": "vm",
  "environment": "production",
  "operating_system": "Ubuntu 20.04",
  "hardware_spec": "{\"cpu\": \"8 cores\", \"memory\": \"16GB\"}",
  "region": "us-east-1",
  "availability_zone": "us-east-1a",
  "cluster_id": "550e8400-e29b-41d4-a716-446655440000",
  "host_capabilities": "{\"gpu\": false, \"ssd\": true}",
  "deployed_components": "{\"web_app\": \"v2.1.0\", \"database\": \"v1.5.2\"}",
  "availability_target": 99.9,
  "current_availability": 100.0,
  "resource_utilization": 75.5,
  "lifecycle_state": "active",
  "cpu_cores": 8,
  "cpu_usage_pct": 65.2,
  "memory_gb": 16.0,
  "memory_usage_pct": 78.9,
  "storage_gb": 500.0,
  "storage_usage_pct": 45.3,
  "network_bandwidth_mbps": 1000.0,
  "network_usage_pct": 32.1,
  "ip_address": "192.168.1.100",
  "mac_address": "00:1B:44:11:3A:B7",
  "hostname": "web-server-01",
  "domain": "example.com",
  "subnet": "192.168.1.0/24",
  "gateway": "192.168.1.1",
  "dns_servers": "[\"8.8.8.8\", \"8.8.4.4\"]",
  "cloud_provider": "AWS",
  "cloud_instance_id": "i-1234567890abcdef0",
  "cloud_instance_type": "t3.large",
  "cloud_tags": "{\"Environment\": \"Production\", \"Team\": \"Web\"}",
  "security_level": "high",
  "compliance_requirements": "{\"gdpr\": true, \"sox\": true}",
  "encryption_enabled": true,
  "backup_enabled": true,
  "monitoring_enabled": true,
  "maintenance_window": "Sunday 2-4 AM UTC",
  "last_maintenance": null,
  "next_maintenance": null,
  "incident_count": 0,
  "last_incident": null,
  "sla_breaches": 0,
  "monthly_cost": 150.0,
  "cost_center": "IT-Infrastructure",
  "resource_pool": "Production-Pool",
  "capacity_planning": "{\"growth_rate\": \"15%\", \"upgrade_planned\": \"2024-Q2\"}",
  "network_interfaces": "{\"eth0\": \"192.168.1.100\", \"eth1\": \"10.0.0.100\"}",
  "firewall_rules": "{\"inbound\": [\"80\", \"443\"], \"outbound\": [\"all\"]}",
  "load_balancer_config": "{\"health_check\": \"/health\", \"session_affinity\": true}",
  "vpn_config": "{\"enabled\": true, \"type\": \"IPSec\"}",
  "container_runtime": "Docker",
  "virtualization_type": "VM",
  "hypervisor": "VMware ESXi",
  "container_orchestrator": "Kubernetes",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Update Node

**PUT** `/nodes/{node_id}`

Updates a Node.

**Request Body:** (All fields optional)
```json
{
  "name": "Enhanced Production Web Server",
  "description": "Updated description with enhanced security features",
  "availability_target": 99.99,
  "security_level": "critical",
  "cpu_cores": 16,
  "memory_gb": 32.0
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Enhanced Production Web Server",
  "description": "Updated description with enhanced security features",
  "availability_target": 99.99,
  "security_level": "critical",
  "cpu_cores": 16,
  "memory_gb": 32.0,
  "updated_at": "2024-01-15T11:30:00Z"
}
```

### Delete Node

**DELETE** `/nodes/{node_id}`

Deletes a Node.

**Response:** `204 No Content`

## Node Link Management

### Create Node Link

**POST** `/nodes/{node_id}/links`

Creates a link between a node and another element.

**Request Body:**
```json
{
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_type": "application_component",
  "link_type": "hosts",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "deployment_status": "active",
  "deployment_version": "v2.1.0",
  "deployment_config": "{\"replicas\": 3, \"resources\": {\"cpu\": \"500m\", \"memory\": \"1Gi\"}}",
  "communication_protocol": "HTTP",
  "communication_port": 8080,
  "communication_frequency": "frequent",
  "communication_type": "synchronous",
  "performance_impact": "medium",
  "latency_contribution": 25.0,
  "bandwidth_usage": 50.0,
  "resource_consumption": 30.0,
  "business_criticality": "high",
  "business_value": "high",
  "alignment_score": 0.85,
  "implementation_priority": "high",
  "implementation_phase": "active",
  "resource_allocation": 25.0,
  "risk_level": "medium",
  "reliability_score": 0.95,
  "failure_impact": "medium",
  "recovery_time": 15,
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "logging_level": "info",
  "metrics_collection": "{\"cpu\": true, \"memory\": true, \"network\": true}",
  "security_requirements": "{\"encryption\": true, \"authentication\": true}",
  "compliance_impact": "medium",
  "data_protection": "{\"backup\": true, \"retention\": \"7 years\"}",
  "performance_contribution": 25.0,
  "success_contribution": 30.0,
  "quality_metrics": "{\"uptime\": 99.9, \"response_time\": \"< 200ms\"}"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "node_id": "550e8400-e29b-41d4-a716-446655440000",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_type": "application_component",
  "link_type": "hosts",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "deployment_status": "active",
  "deployment_version": "v2.1.0",
  "deployment_config": "{\"replicas\": 3, \"resources\": {\"cpu\": \"500m\", \"memory\": \"1Gi\"}}",
  "communication_protocol": "HTTP",
  "communication_port": 8080,
  "communication_frequency": "frequent",
  "communication_type": "synchronous",
  "performance_impact": "medium",
  "latency_contribution": 25.0,
  "bandwidth_usage": 50.0,
  "resource_consumption": 30.0,
  "business_criticality": "high",
  "business_value": "high",
  "alignment_score": 0.85,
  "implementation_priority": "high",
  "implementation_phase": "active",
  "resource_allocation": 25.0,
  "risk_level": "medium",
  "reliability_score": 0.95,
  "failure_impact": "medium",
  "recovery_time": 15,
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "logging_level": "info",
  "metrics_collection": "{\"cpu\": true, \"memory\": true, \"network\": true}",
  "security_requirements": "{\"encryption\": true, \"authentication\": true}",
  "compliance_impact": "medium",
  "data_protection": "{\"backup\": true, \"retention\": \"7 years\"}",
  "performance_contribution": 25.0,
  "success_contribution": 30.0,
  "quality_metrics": "{\"uptime\": 99.9, \"response_time\": \"< 200ms\"}",
  "deployment_date": null,
  "created_by": "550e8400-e29b-41d4-a716-446655440002",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### List Node Links

**GET** `/nodes/{node_id}/links`

Lists all links for a node.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440004",
    "node_id": "550e8400-e29b-41d4-a716-446655440000",
    "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
    "linked_element_type": "application_component",
    "link_type": "hosts",
    "relationship_strength": "strong",
    "dependency_level": "high",
    "deployment_status": "active",
    "communication_protocol": "HTTP",
    "communication_port": 8080,
    "communication_frequency": "frequent",
    "communication_type": "synchronous",
    "performance_impact": "medium",
    "latency_contribution": 25.0,
    "bandwidth_usage": 50.0,
    "resource_consumption": 30.0,
    "business_criticality": "high",
    "business_value": "high",
    "alignment_score": 0.85,
    "implementation_priority": "high",
    "implementation_phase": "active",
    "resource_allocation": 25.0,
    "risk_level": "medium",
    "reliability_score": 0.95,
    "failure_impact": "medium",
    "recovery_time": 15,
    "monitoring_enabled": true,
    "alerting_enabled": true,
    "logging_level": "info",
    "metrics_collection": "{\"cpu\": true, \"memory\": true, \"network\": true}",
    "security_requirements": "{\"encryption\": true, \"authentication\": true}",
    "compliance_impact": "medium",
    "data_protection": "{\"backup\": true, \"retention\": \"7 years\"}",
    "performance_contribution": 25.0,
    "success_contribution": 30.0,
    "quality_metrics": "{\"uptime\": 99.9, \"response_time\": \"< 200ms\"}",
    "deployment_date": null,
    "created_by": "550e8400-e29b-41d4-a716-446655440002",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Node Link

**GET** `/nodes/links/{link_id}`

Retrieves a node link by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "node_id": "550e8400-e29b-41d4-a716-446655440000",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_type": "application_component",
  "link_type": "hosts",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "deployment_status": "active",
  "deployment_version": "v2.1.0",
  "deployment_config": "{\"replicas\": 3, \"resources\": {\"cpu\": \"500m\", \"memory\": \"1Gi\"}}",
  "communication_protocol": "HTTP",
  "communication_port": 8080,
  "communication_frequency": "frequent",
  "communication_type": "synchronous",
  "performance_impact": "medium",
  "latency_contribution": 25.0,
  "bandwidth_usage": 50.0,
  "resource_consumption": 30.0,
  "business_criticality": "high",
  "business_value": "high",
  "alignment_score": 0.85,
  "implementation_priority": "high",
  "implementation_phase": "active",
  "resource_allocation": 25.0,
  "risk_level": "medium",
  "reliability_score": 0.95,
  "failure_impact": "medium",
  "recovery_time": 15,
  "monitoring_enabled": true,
  "alerting_enabled": true,
  "logging_level": "info",
  "metrics_collection": "{\"cpu\": true, \"memory\": true, \"network\": true}",
  "security_requirements": "{\"encryption\": true, \"authentication\": true}",
  "compliance_impact": "medium",
  "data_protection": "{\"backup\": true, \"retention\": \"7 years\"}",
  "performance_contribution": 25.0,
  "success_contribution": 30.0,
  "quality_metrics": "{\"uptime\": 99.9, \"response_time\": \"< 200ms\"}",
  "deployment_date": null,
  "created_by": "550e8400-e29b-41d4-a716-446655440002",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Update Node Link

**PUT** `/nodes/links/{link_id}`

Updates a node link.

**Request Body:** (All fields optional)
```json
{
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "performance_impact": "low",
  "resource_allocation": 20.0
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "performance_impact": "low",
  "resource_allocation": 20.0
}
```

### Delete Node Link

**DELETE** `/nodes/links/{link_id}`

Deletes a node link.

**Response:** `204 No Content`

## Analysis & Impact Endpoints

### Get Deployment Map

**GET** `/nodes/{node_id}/deployment-map`

Returns deployment mapping for the Node.

**Response:** `200 OK`
```json
{
  "node_id": "550e8400-e29b-41d4-a716-446655440000",
  "deployed_components": [
    {
      "name": "web-app",
      "version": "v2.1.0",
      "status": "active",
      "resource_usage": {
        "cpu": "65%",
        "memory": "78%",
        "storage": "45%"
      }
    }
  ],
  "deployment_status": {
    "total_components": 1,
    "active_deployments": 1,
    "failed_deployments": 0,
    "pending_deployments": 0
  },
  "resource_allocation": {
    "total_components": 1,
    "active_components": 1,
    "cpu_allocation_pct": 30.0,
    "memory_allocation_pct": 25.0,
    "utilization_efficiency": 100.0
  },
  "capacity_utilization": {
    "cpu_utilization": 65.2,
    "memory_utilization": 78.9,
    "storage_utilization": 45.3,
    "network_utilization": 32.1,
    "overall_utilization": 55.4
  },
  "deployment_health": {
    "health_score": 100.0,
    "status": "healthy",
    "active_deployments": 1,
    "failed_deployments": 0,
    "total_deployments": 1
  }
}
```

### Get Capacity Analysis

**GET** `/nodes/{node_id}/capacity-analysis`

Returns capacity analysis for the Node.

**Response:** `200 OK`
```json
{
  "node_id": "550e8400-e29b-41d4-a716-446655440000",
  "current_capacity": {
    "cpu_cores": 8,
    "memory_gb": 16.0,
    "storage_gb": 500.0,
    "network_bandwidth_mbps": 1000.0,
    "cpu_usage_pct": 65.2,
    "memory_usage_pct": 78.9,
    "storage_usage_pct": 45.3,
    "network_usage_pct": 32.1
  },
  "projected_capacity": {
    "cpu_cores": 8,
    "memory_gb": 17.6,
    "storage_gb": 575.0,
    "network_bandwidth_mbps": 1000.0,
    "projected_cpu_usage": 71.7,
    "projected_memory_usage": 86.8,
    "projected_storage_usage": 52.1,
    "projected_network_usage": 35.3
  },
  "capacity_recommendations": [
    "Consider memory scaling due to high utilization",
    "Monitor CPU usage trends for potential scaling"
  ],
  "scaling_opportunities": [
    "Memory is well-utilized - consider optimization",
    "Storage has room for growth"
  ],
  "resource_optimization": {
    "cpu_efficiency": 34.8,
    "memory_efficiency": 21.1,
    "storage_efficiency": 54.7,
    "network_efficiency": 67.9,
    "overall_efficiency": 44.6
  }
}
```

### Analyze Node

**GET** `/nodes/{node_id}/analysis`

Returns comprehensive analysis for the Node.

**Response:** `200 OK`
```json
{
  "node_id": "550e8400-e29b-41d4-a716-446655440000",
  "operational_health": {
    "overall_score": 0.85,
    "availability_score": 1.0,
    "incident_score": 1.0,
    "sla_score": 1.0,
    "status": "healthy"
  },
  "performance_metrics": {
    "response_time": 65.2,
    "throughput": 32.1,
    "availability": 100.0,
    "resource_utilization": 75.5,
    "performance_score": 0.78
  },
  "resource_efficiency": {
    "cpu_efficiency": 34.8,
    "memory_efficiency": 21.1,
    "storage_efficiency": 54.7,
    "network_efficiency": 67.9,
    "overall_efficiency": 44.6
  },
  "risk_assessment": {
    "risk_factors": [
      {
        "type": "security",
        "severity": "high",
        "description": "High security level with critical business function"
      }
    ],
    "overall_risk": "medium"
  },
  "improvement_opportunities": [
    "Document hardware specifications and dependencies",
    "Implement comprehensive monitoring and alerting",
    "Optimize memory utilization"
  ],
  "compliance_status": {
    "compliance_rate": 1.0,
    "compliant_items": ["encryption", "monitoring", "backup"],
    "non_compliant_items": [],
    "status": "compliant"
  }
}
```

## Domain-Specific Query Endpoints

### Get by Node Type

**GET** `/nodes/by-type/{node_type}`

Returns nodes filtered by type.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Production Web Server",
    "node_type": "vm",
    "environment": "production",
    "status": "active"
  }
]
```

### Get by Environment

**GET** `/nodes/by-environment/{environment}`

Returns nodes filtered by environment.

### Get by Region

**GET** `/nodes/by-region/{region}`

Returns nodes filtered by region.

### Get Active Nodes

**GET** `/nodes/active`

Returns all active nodes.

### Get Critical Nodes

**GET** `/nodes/critical`

Returns all critical nodes.

## Enumeration Endpoints

### Get Node Types

**GET** `/nodes/node-types`

Returns all available node types.

**Response:** `200 OK`
```json
[
  "vm",
  "container",
  "physical",
  "cloud",
  "edge"
]
```

### Get Environments

**GET** `/nodes/environments`

Returns all available environments.

**Response:** `200 OK`
```json
[
  "production",
  "staging",
  "development",
  "testing"
]
```

### Get Lifecycle States

**GET** `/nodes/lifecycle-states`

Returns all available lifecycle states.

**Response:** `200 OK`
```json
[
  "active",
  "inactive",
  "maintenance",
  "decommissioned",
  "planned"
]
```

### Get Security Levels

**GET** `/nodes/security-levels`

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

### Get Link Types

**GET** `/nodes/link-types`

Returns all available link types.

**Response:** `200 OK`
```json
[
  "hosts",
  "deploys",
  "communicates_with",
  "depends_on",
  "manages"
]
```

### Get Relationship Strengths

**GET** `/nodes/relationship-strengths`

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

**GET** `/nodes/dependency-levels`

Returns all available dependency levels.

**Response:** `200 OK`
```json
[
  "high",
  "medium",
  "low"
]
```

### Get Deployment Statuses

**GET** `/nodes/deployment-statuses`

Returns all available deployment statuses.

**Response:** `200 OK`
```json
[
  "active",
  "inactive",
  "failed",
  "pending"
]
```

### Get Communication Frequencies

**GET** `/nodes/communication-frequencies`

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

**GET** `/nodes/communication-types`

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

**GET** `/nodes/performance-impacts`

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
  "detail": "Validation error: Invalid node type"
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
  "detail": "Insufficient permissions. Required: node:create, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Node not found"
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
- Node type
- Environment
- Lifecycle state
- Region
- Security level
- Cluster ID
- Performance threshold

## Sorting

Results are sorted by `created_at` in descending order by default.

## OpenAPI Documentation

For complete OpenAPI documentation, visit:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`
