# Business Role Service API Reference

## Overview

The Business Role Service API provides comprehensive management of business roles within the ReqArchitect platform. This API follows RESTful principles and includes authentication, authorization, and comprehensive validation.

## Authentication

All API endpoints require JWT authentication via the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

The JWT token must contain:
- `tenant_id`: UUID of the tenant
- `user_id`: UUID of the user
- `role`: User role (Owner, Admin, Editor, Viewer)

## Base URL

```
http://localhost:8080/api/v1
```

## Business Role Endpoints

### Create Business Role

**POST** `/business-roles`

Creates a new business role.

**Request Body:**
```json
{
  "name": "Enterprise Architect",
  "description": "Responsible for enterprise architecture strategy and governance",
  "organizational_unit": "IT Department",
  "role_type": "Architecture Lead",
  "responsibilities": "Define enterprise architecture standards, review architectural decisions",
  "required_skills": "[\"TOGAF\", \"ArchiMate\", \"Enterprise Architecture\"]",
  "required_capabilities": "[\"Strategic Planning\", \"Technical Leadership\"]",
  "stakeholder_id": "123e4567-e89b-12d3-a456-426614174000",
  "role_classification": "strategic",
  "authority_level": "senior",
  "decision_making_authority": "full",
  "approval_authority": "partial",
  "strategic_importance": "high",
  "business_value": "high",
  "capability_alignment": 0.85,
  "strategic_alignment": 0.90,
  "performance_score": 0.88,
  "effectiveness_score": 0.92,
  "efficiency_score": 0.85,
  "satisfaction_score": 0.90,
  "criticality": "high",
  "complexity": "complex",
  "workload_level": "standard",
  "availability_requirement": "business_hours",
  "headcount_requirement": 2,
  "current_headcount": 1,
  "skill_gaps": "[\"Cloud Architecture\", \"DevOps\"]",
  "training_requirements": "[\"AWS Solutions Architect\", \"Azure Fundamentals\"]",
  "compliance_requirements": "[\"SOX\", \"GDPR\"]",
  "risk_level": "medium",
  "audit_frequency": "quarterly",
  "status": "active",
  "operational_hours": "business_hours",
  "availability_target": 99.5,
  "current_availability": 100.0,
  "cost_center": "IT-ARCH-001",
  "budget_allocation": 250000.00,
  "salary_range_min": 120000.00,
  "salary_range_max": 180000.00,
  "total_compensation": 200000.00,
  "reporting_to_role_id": "123e4567-e89b-12d3-a456-426614174001",
  "supporting_capability_id": "123e4567-e89b-12d3-a456-426614174002",
  "business_function_id": "123e4567-e89b-12d3-a456-426614174003",
  "business_process_id": "123e4567-e89b-12d3-a456-426614174004"
}
```

**Response:** `201 Created`
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174005",
  "tenant_id": "123e4567-e89b-12d3-a456-426614174006",
  "user_id": "123e4567-e89b-12d3-a456-426614174007",
  "name": "Enterprise Architect",
  "description": "Responsible for enterprise architecture strategy and governance",
  "organizational_unit": "IT Department",
  "role_type": "Architecture Lead",
  "responsibilities": "Define enterprise architecture standards, review architectural decisions",
  "required_skills": "[\"TOGAF\", \"ArchiMate\", \"Enterprise Architecture\"]",
  "required_capabilities": "[\"Strategic Planning\", \"Technical Leadership\"]",
  "stakeholder_id": "123e4567-e89b-12d3-a456-426614174000",
  "role_classification": "strategic",
  "authority_level": "senior",
  "decision_making_authority": "full",
  "approval_authority": "partial",
  "strategic_importance": "high",
  "business_value": "high",
  "capability_alignment": 0.85,
  "strategic_alignment": 0.90,
  "performance_score": 0.88,
  "effectiveness_score": 0.92,
  "efficiency_score": 0.85,
  "satisfaction_score": 0.90,
  "performance_metrics": null,
  "criticality": "high",
  "complexity": "complex",
  "workload_level": "standard",
  "availability_requirement": "business_hours",
  "headcount_requirement": 2,
  "current_headcount": 1,
  "skill_gaps": "[\"Cloud Architecture\", \"DevOps\"]",
  "training_requirements": "[\"AWS Solutions Architect\", \"Azure Fundamentals\"]",
  "compliance_requirements": "[\"SOX\", \"GDPR\"]",
  "risk_level": "medium",
  "audit_frequency": "quarterly",
  "last_audit_date": null,
  "audit_status": "pending",
  "status": "active",
  "operational_hours": "business_hours",
  "availability_target": 99.5,
  "current_availability": 100.0,
  "cost_center": "IT-ARCH-001",
  "budget_allocation": 250000.00,
  "salary_range_min": 120000.00,
  "salary_range_max": 180000.00,
  "total_compensation": 200000.00,
  "reporting_to_role_id": "123e4567-e89b-12d3-a456-426614174001",
  "supporting_capability_id": "123e4567-e89b-12d3-a456-426614174002",
  "business_function_id": "123e4567-e89b-12d3-a456-426614174003",
  "business_process_id": "123e4567-e89b-12d3-a456-426614174004",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Get Business Role

**GET** `/business-roles/{role_id}`

Retrieves a business role by ID.

**Response:** `200 OK`
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174005",
  "tenant_id": "123e4567-e89b-12d3-a456-426614174006",
  "user_id": "123e4567-e89b-12d3-a456-426614174007",
  "name": "Enterprise Architect",
  "description": "Responsible for enterprise architecture strategy and governance",
  "organizational_unit": "IT Department",
  "role_type": "Architecture Lead",
  "responsibilities": "Define enterprise architecture standards, review architectural decisions",
  "required_skills": "[\"TOGAF\", \"ArchiMate\", \"Enterprise Architecture\"]",
  "required_capabilities": "[\"Strategic Planning\", \"Technical Leadership\"]",
  "stakeholder_id": "123e4567-e89b-12d3-a456-426614174000",
  "role_classification": "strategic",
  "authority_level": "senior",
  "decision_making_authority": "full",
  "approval_authority": "partial",
  "strategic_importance": "high",
  "business_value": "high",
  "capability_alignment": 0.85,
  "strategic_alignment": 0.90,
  "performance_score": 0.88,
  "effectiveness_score": 0.92,
  "efficiency_score": 0.85,
  "satisfaction_score": 0.90,
  "performance_metrics": null,
  "criticality": "high",
  "complexity": "complex",
  "workload_level": "standard",
  "availability_requirement": "business_hours",
  "headcount_requirement": 2,
  "current_headcount": 1,
  "skill_gaps": "[\"Cloud Architecture\", \"DevOps\"]",
  "training_requirements": "[\"AWS Solutions Architect\", \"Azure Fundamentals\"]",
  "compliance_requirements": "[\"SOX\", \"GDPR\"]",
  "risk_level": "medium",
  "audit_frequency": "quarterly",
  "last_audit_date": null,
  "audit_status": "pending",
  "status": "active",
  "operational_hours": "business_hours",
  "availability_target": 99.5,
  "current_availability": 100.0,
  "cost_center": "IT-ARCH-001",
  "budget_allocation": 250000.00,
  "salary_range_min": 120000.00,
  "salary_range_max": 180000.00,
  "total_compensation": 200000.00,
  "reporting_to_role_id": "123e4567-e89b-12d3-a456-426614174001",
  "supporting_capability_id": "123e4567-e89b-12d3-a456-426614174002",
  "business_function_id": "123e4567-e89b-12d3-a456-426614174003",
  "business_process_id": "123e4567-e89b-12d3-a456-426614174004",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### List Business Roles

**GET** `/business-roles`

Retrieves a list of business roles with filtering and pagination.

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum number of records to return (default: 100, max: 1000)
- `organizational_unit` (string, optional): Filter by organizational unit
- `role_type` (string, optional): Filter by role type
- `strategic_importance` (string, optional): Filter by strategic importance
- `authority_level` (string, optional): Filter by authority level
- `status` (string, optional): Filter by status
- `stakeholder_id` (UUID, optional): Filter by stakeholder ID
- `supporting_capability_id` (UUID, optional): Filter by supporting capability ID
- `business_function_id` (UUID, optional): Filter by business function ID
- `business_process_id` (UUID, optional): Filter by business process ID
- `role_classification` (string, optional): Filter by role classification
- `criticality` (string, optional): Filter by criticality

**Response:** `200 OK`
```json
{
  "business_roles": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174005",
      "tenant_id": "123e4567-e89b-12d3-a456-426614174006",
      "user_id": "123e4567-e89b-12d3-a456-426614174007",
      "name": "Enterprise Architect",
      "description": "Responsible for enterprise architecture strategy and governance",
      "organizational_unit": "IT Department",
      "role_type": "Architecture Lead",
      "responsibilities": "Define enterprise architecture standards, review architectural decisions",
      "required_skills": "[\"TOGAF\", \"ArchiMate\", \"Enterprise Architecture\"]",
      "required_capabilities": "[\"Strategic Planning\", \"Technical Leadership\"]",
      "stakeholder_id": "123e4567-e89b-12d3-a456-426614174000",
      "role_classification": "strategic",
      "authority_level": "senior",
      "decision_making_authority": "full",
      "approval_authority": "partial",
      "strategic_importance": "high",
      "business_value": "high",
      "capability_alignment": 0.85,
      "strategic_alignment": 0.90,
      "performance_score": 0.88,
      "effectiveness_score": 0.92,
      "efficiency_score": 0.85,
      "satisfaction_score": 0.90,
      "performance_metrics": null,
      "criticality": "high",
      "complexity": "complex",
      "workload_level": "standard",
      "availability_requirement": "business_hours",
      "headcount_requirement": 2,
      "current_headcount": 1,
      "skill_gaps": "[\"Cloud Architecture\", \"DevOps\"]",
      "training_requirements": "[\"AWS Solutions Architect\", \"Azure Fundamentals\"]",
      "compliance_requirements": "[\"SOX\", \"GDPR\"]",
      "risk_level": "medium",
      "audit_frequency": "quarterly",
      "last_audit_date": null,
      "audit_status": "pending",
      "status": "active",
      "operational_hours": "business_hours",
      "availability_target": 99.5,
      "current_availability": 100.0,
      "cost_center": "IT-ARCH-001",
      "budget_allocation": 250000.00,
      "salary_range_min": 120000.00,
      "salary_range_max": 180000.00,
      "total_compensation": 200000.00,
      "reporting_to_role_id": "123e4567-e89b-12d3-a456-426614174001",
      "supporting_capability_id": "123e4567-e89b-12d3-a456-426614174002",
      "business_function_id": "123e4567-e89b-12d3-a456-426614174003",
      "business_process_id": "123e4567-e89b-12d3-a456-426614174004",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

### Update Business Role

**PUT** `/business-roles/{role_id}`

Updates an existing business role.

**Request Body:** (Partial update - only include fields to update)
```json
{
  "name": "Senior Enterprise Architect",
  "description": "Updated description for senior enterprise architect role",
  "strategic_importance": "critical",
  "capability_alignment": 0.95,
  "performance_score": 0.92
}
```

**Response:** `200 OK`
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174005",
  "tenant_id": "123e4567-e89b-12d3-a456-426614174006",
  "user_id": "123e4567-e89b-12d3-a456-426614174007",
  "name": "Senior Enterprise Architect",
  "description": "Updated description for senior enterprise architect role",
  "organizational_unit": "IT Department",
  "role_type": "Architecture Lead",
  "responsibilities": "Define enterprise architecture standards, review architectural decisions",
  "required_skills": "[\"TOGAF\", \"ArchiMate\", \"Enterprise Architecture\"]",
  "required_capabilities": "[\"Strategic Planning\", \"Technical Leadership\"]",
  "stakeholder_id": "123e4567-e89b-12d3-a456-426614174000",
  "role_classification": "strategic",
  "authority_level": "senior",
  "decision_making_authority": "full",
  "approval_authority": "partial",
  "strategic_importance": "critical",
  "business_value": "high",
  "capability_alignment": 0.95,
  "strategic_alignment": 0.90,
  "performance_score": 0.92,
  "effectiveness_score": 0.92,
  "efficiency_score": 0.85,
  "satisfaction_score": 0.90,
  "performance_metrics": null,
  "criticality": "high",
  "complexity": "complex",
  "workload_level": "standard",
  "availability_requirement": "business_hours",
  "headcount_requirement": 2,
  "current_headcount": 1,
  "skill_gaps": "[\"Cloud Architecture\", \"DevOps\"]",
  "training_requirements": "[\"AWS Solutions Architect\", \"Azure Fundamentals\"]",
  "compliance_requirements": "[\"SOX\", \"GDPR\"]",
  "risk_level": "medium",
  "audit_frequency": "quarterly",
  "last_audit_date": null,
  "audit_status": "pending",
  "status": "active",
  "operational_hours": "business_hours",
  "availability_target": 99.5,
  "current_availability": 100.0,
  "cost_center": "IT-ARCH-001",
  "budget_allocation": 250000.00,
  "salary_range_min": 120000.00,
  "salary_range_max": 180000.00,
  "total_compensation": 200000.00,
  "reporting_to_role_id": "123e4567-e89b-12d3-a456-426614174001",
  "supporting_capability_id": "123e4567-e89b-12d3-a456-426614174002",
  "business_function_id": "123e4567-e89b-12d3-a456-426614174003",
  "business_process_id": "123e4567-e89b-12d3-a456-426614174004",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:45:00Z"
}
```

### Delete Business Role

**DELETE** `/business-roles/{role_id}`

Deletes a business role.

**Response:** `200 OK`
```json
{
  "message": "Business role deleted successfully"
}
```

## Role Link Endpoints

### Create Role Link

**POST** `/business-roles/{role_id}/links`

Creates a link between a business role and another element.

**Request Body:**
```json
{
  "linked_element_id": "123e4567-e89b-12d3-a456-426614174010",
  "linked_element_type": "business_function",
  "link_type": "performs",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "responsibility_level": "primary",
  "accountability_level": "full",
  "performance_impact": "high",
  "decision_authority": "full"
}
```

**Response:** `201 Created`
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174015",
  "business_role_id": "123e4567-e89b-12d3-a456-426614174005",
  "linked_element_id": "123e4567-e89b-12d3-a456-426614174010",
  "linked_element_type": "business_function",
  "link_type": "performs",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "responsibility_level": "primary",
  "accountability_level": "full",
  "performance_impact": "high",
  "decision_authority": "full",
  "created_by": "123e4567-e89b-12d3-a456-426614174007",
  "created_at": "2024-01-15T12:00:00Z"
}
```

### Get Role Links

**GET** `/business-roles/{role_id}/links`

Retrieves all links for a business role.

**Response:** `200 OK`
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174015",
    "business_role_id": "123e4567-e89b-12d3-a456-426614174005",
    "linked_element_id": "123e4567-e89b-12d3-a456-426614174010",
    "linked_element_type": "business_function",
    "link_type": "performs",
    "relationship_strength": "strong",
    "dependency_level": "high",
    "interaction_frequency": "frequent",
    "interaction_type": "synchronous",
    "responsibility_level": "primary",
    "accountability_level": "full",
    "performance_impact": "high",
    "decision_authority": "full",
    "created_by": "123e4567-e89b-12d3-a456-426614174007",
    "created_at": "2024-01-15T12:00:00Z"
  }
]
```

### Get Role Link

**GET** `/role-links/{link_id}`

Retrieves a specific role link by ID.

**Response:** `200 OK`
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174015",
  "business_role_id": "123e4567-e89b-12d3-a456-426614174005",
  "linked_element_id": "123e4567-e89b-12d3-a456-426614174010",
  "linked_element_type": "business_function",
  "link_type": "performs",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "responsibility_level": "primary",
  "accountability_level": "full",
  "performance_impact": "high",
  "decision_authority": "full",
  "created_by": "123e4567-e89b-12d3-a456-426614174007",
  "created_at": "2024-01-15T12:00:00Z"
}
```

### Update Role Link

**PUT** `/role-links/{link_id}`

Updates a role link.

**Request Body:** (Partial update)
```json
{
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "performance_impact": "medium"
}
```

**Response:** `200 OK`
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174015",
  "business_role_id": "123e4567-e89b-12d3-a456-426614174005",
  "linked_element_id": "123e4567-e89b-12d3-a456-426614174010",
  "linked_element_type": "business_function",
  "link_type": "performs",
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "interaction_frequency": "frequent",
  "interaction_type": "synchronous",
  "responsibility_level": "primary",
  "accountability_level": "full",
  "performance_impact": "medium",
  "decision_authority": "full",
  "created_by": "123e4567-e89b-12d3-a456-426614174007",
  "created_at": "2024-01-15T12:00:00Z"
}
```

### Delete Role Link

**DELETE** `/role-links/{link_id}`

Deletes a role link.

**Response:** `200 OK`
```json
{
  "message": "Role link deleted successfully"
}
```

## Analysis Endpoints

### Get Responsibility Map

**GET** `/business-roles/{role_id}/responsibility-map`

Analyzes the responsibility map for a business role.

**Response:** `200 OK`
```json
{
  "business_role_id": "123e4567-e89b-12d3-a456-426614174005",
  "linked_elements_count": 5,
  "business_functions_count": 2,
  "business_processes_count": 1,
  "application_services_count": 1,
  "data_objects_count": 1,
  "stakeholders_count": 0,
  "overall_responsibility_score": 0.85,
  "last_assessed": "2024-01-15T12:30:00Z"
}
```

### Get Alignment Score

**GET** `/business-roles/{role_id}/alignment-score`

Analyzes the alignment scores for a business role.

**Response:** `200 OK`
```json
{
  "business_role_id": "123e4567-e89b-12d3-a456-426614174005",
  "capability_alignment": 0.85,
  "strategic_alignment": 0.90,
  "performance_score": 0.88,
  "effectiveness_score": 0.92,
  "efficiency_score": 0.85,
  "satisfaction_score": 0.90,
  "overall_alignment_score": 0.88,
  "last_analyzed": "2024-01-15T12:30:00Z"
}
```

## Domain Query Endpoints

### Get Business Roles by Organizational Unit

**GET** `/business-roles/organizational-unit/{organizational_unit}`

**Response:** `200 OK`
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174005",
    "tenant_id": "123e4567-e89b-12d3-a456-426614174006",
    "user_id": "123e4567-e89b-12d3-a456-426614174007",
    "name": "Enterprise Architect",
    "description": "Responsible for enterprise architecture strategy and governance",
    "organizational_unit": "IT Department",
    "role_type": "Architecture Lead",
    "responsibilities": "Define enterprise architecture standards, review architectural decisions",
    "required_skills": "[\"TOGAF\", \"ArchiMate\", \"Enterprise Architecture\"]",
    "required_capabilities": "[\"Strategic Planning\", \"Technical Leadership\"]",
    "stakeholder_id": "123e4567-e89b-12d3-a456-426614174000",
    "role_classification": "strategic",
    "authority_level": "senior",
    "decision_making_authority": "full",
    "approval_authority": "partial",
    "strategic_importance": "high",
    "business_value": "high",
    "capability_alignment": 0.85,
    "strategic_alignment": 0.90,
    "performance_score": 0.88,
    "effectiveness_score": 0.92,
    "efficiency_score": 0.85,
    "satisfaction_score": 0.90,
    "performance_metrics": null,
    "criticality": "high",
    "complexity": "complex",
    "workload_level": "standard",
    "availability_requirement": "business_hours",
    "headcount_requirement": 2,
    "current_headcount": 1,
    "skill_gaps": "[\"Cloud Architecture\", \"DevOps\"]",
    "training_requirements": "[\"AWS Solutions Architect\", \"Azure Fundamentals\"]",
    "compliance_requirements": "[\"SOX\", \"GDPR\"]",
    "risk_level": "medium",
    "audit_frequency": "quarterly",
    "last_audit_date": null,
    "audit_status": "pending",
    "status": "active",
    "operational_hours": "business_hours",
    "availability_target": 99.5,
    "current_availability": 100.0,
    "cost_center": "IT-ARCH-001",
    "budget_allocation": 250000.00,
    "salary_range_min": 120000.00,
    "salary_range_max": 180000.00,
    "total_compensation": 200000.00,
    "reporting_to_role_id": "123e4567-e89b-12d3-a456-426614174001",
    "supporting_capability_id": "123e4567-e89b-12d3-a456-426614174002",
    "business_function_id": "123e4567-e89b-12d3-a456-426614174003",
    "business_process_id": "123e4567-e89b-12d3-a456-426614174004",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:45:00Z"
  }
]
```

### Get Business Roles by Role Type

**GET** `/business-roles/role-type/{role_type}`

### Get Business Roles by Strategic Importance

**GET** `/business-roles/strategic-importance/{strategic_importance}`

### Get Business Roles by Authority Level

**GET** `/business-roles/authority-level/{authority_level}`

### Get Business Roles by Status

**GET** `/business-roles/status/{status}`

### Get Business Roles by Stakeholder

**GET** `/business-roles/stakeholder/{stakeholder_id}`

### Get Business Roles by Capability

**GET** `/business-roles/capability/{capability_id}`

### Get Business Roles by Function

**GET** `/business-roles/function/{function_id}`

### Get Business Roles by Process

**GET** `/business-roles/process/{process_id}`

### Get Business Roles by Element

**GET** `/business-roles/element/{element_type}/{element_id}`

### Get Active Business Roles

**GET** `/business-roles/active`

### Get Critical Business Roles

**GET** `/business-roles/critical`

### Get Business Roles by Classification

**GET** `/business-roles/classification/{role_classification}`

### Get Business Roles by Criticality

**GET** `/business-roles/criticality/{criticality}`

### Get Business Roles by Workload

**GET** `/business-roles/workload/{workload_level}`

### Get Business Roles by Availability

**GET** `/business-roles/availability/{availability_requirement}`

### Get Business Roles by Risk Level

**GET** `/business-roles/risk-level/{risk_level}`

### Get Business Roles by Business Value

**GET** `/business-roles/business-value/{business_value}`

### Get Business Roles by Decision Authority

**GET** `/business-roles/decision-authority/{decision_making_authority}`

### Get Business Roles by Approval Authority

**GET** `/business-roles/approval-authority/{approval_authority}`

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error"
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
  "detail": "Insufficient permissions. Required: business_role:read, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Business role not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Data Types

### Enums

#### RoleType
- `Architecture Lead`
- `Compliance Officer`
- `Strategy Analyst`
- `Vendor Manager`
- `Data Custodian`
- `Security Officer`
- `Risk Manager`
- `Quality Assurance Lead`
- `Change Manager`
- `Capacity Planner`
- `Cost Manager`
- `Performance Analyst`
- `Stakeholder Manager`
- `Technology Evaluator`
- `Process Optimizer`

#### RoleClassification
- `strategic`
- `tactical`
- `operational`
- `support`

#### AuthorityLevel
- `executive`
- `senior`
- `standard`
- `junior`
- `trainee`

#### DecisionMakingAuthority
- `full`
- `partial`
- `limited`
- `none`

#### ApprovalAuthority
- `full`
- `partial`
- `limited`
- `none`

#### StrategicImportance
- `low`
- `medium`
- `high`
- `critical`

#### BusinessValue
- `low`
- `medium`
- `high`
- `critical`

#### Criticality
- `low`
- `medium`
- `high`
- `critical`

#### Complexity
- `simple`
- `medium`
- `complex`
- `very_complex`

#### WorkloadLevel
- `light`
- `standard`
- `heavy`
- `overloaded`

#### AvailabilityRequirement
- `24x7`
- `business_hours`
- `on_demand`

#### RiskLevel
- `low`
- `medium`
- `high`
- `critical`

#### AuditFrequency
- `monthly`
- `quarterly`
- `annually`
- `ad_hoc`

#### AuditStatus
- `pending`
- `in_progress`
- `completed`
- `failed`

#### RoleStatus
- `active`
- `inactive`
- `deprecated`
- `planned`

#### OperationalHours
- `24x7`
- `business_hours`
- `on_demand`

#### LinkType
- `performs`
- `owns`
- `manages`
- `supports`
- `collaborates`
- `reports_to`
- `supervises`

#### RelationshipStrength
- `strong`
- `medium`
- `weak`

#### DependencyLevel
- `high`
- `medium`
- `low`

#### InteractionFrequency
- `frequent`
- `regular`
- `occasional`
- `rare`

#### InteractionType
- `synchronous`
- `asynchronous`
- `batch`
- `real_time`

#### ResponsibilityLevel
- `primary`
- `secondary`
- `shared`
- `advisory`

#### AccountabilityLevel
- `full`
- `partial`
- `shared`
- `advisory`

#### PerformanceImpact
- `high`
- `medium`
- `low`
- `minimal`
