# API Reference: courseofaction_service

## Overview

The Course of Action Service provides comprehensive management of ArchiMate 3.2 Course of Action elements with full CRUD operations, relationship management, analysis capabilities, and domain-specific queries.

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

## Course of Action Management

### Create Course of Action

**POST** `/api/v1/courses-of-action`

Creates a new CourseOfAction.

**Request Body:**
```json
{
  "name": "Cloud Migration Initiative",
  "description": "Strategic initiative to migrate legacy systems to cloud infrastructure",
  "strategy_type": "transformational",
  "origin_goal_id": "550e8400-e29b-41d4-a716-446655440000",
  "influenced_by_driver_id": "550e8400-e29b-41d4-a716-446655440001",
  "impacted_capability_id": "550e8400-e29b-41d4-a716-446655440002",
  "strategic_objective": "Achieve 99.9% uptime and reduce infrastructure costs by 30%",
  "business_case": "Cost reduction and improved scalability",
  "success_criteria": "{\"uptime\": \"99.9%\", \"cost_reduction\": \"30%\", \"data_loss\": \"0%\"}",
  "key_performance_indicators": "{\"uptime\": \"target\", \"cost_savings\": \"measure\", \"migration_speed\": \"track\"}",
  "time_horizon": "medium_term",
  "start_date": "2024-01-01T00:00:00Z",
  "target_completion_date": "2024-12-31T23:59:59Z",
  "implementation_phase": "planning",
  "success_probability": 0.8,
  "risk_level": "medium",
  "risk_assessment": "{\"data_migration\": \"high\", \"downtime\": \"medium\"}",
  "contingency_plans": "[\"rollback_plan\", \"parallel_systems\"]",
  "estimated_cost": 1000000.0,
  "budget_allocation": 1200000.0,
  "resource_requirements": "{\"developers\": 5, \"devops\": 3, \"qa\": 2}",
  "cost_benefit_analysis": "{\"roi\": \"150%\", \"payback_period\": \"18 months\"}",
  "stakeholders": "[\"cto\", \"cio\", \"business_units\"]",
  "governance_model": "enhanced",
  "approval_status": "pending",
  "implementation_approach": "Phased migration with parallel systems",
  "milestones": "[\"planning\", \"pilot\", \"full_migration\", \"validation\"]",
  "dependencies": "[\"infrastructure_ready\", \"team_training\", \"vendor_selection\"]",
  "constraints": "[\"budget_limit\", \"timeline\", \"compliance_requirements\"]",
  "current_progress": 15.0,
  "performance_metrics": "{\"progress\": \"15%\", \"budget_spent\": \"10%\"}",
  "outcomes_achieved": "[\"team_assembled\", \"vendor_selected\"]",
  "lessons_learned": "[\"early_planning_critical\", \"stakeholder_engagement_key\"]",
  "strategic_alignment_score": 0.85,
  "capability_impact_score": 0.9,
  "goal_achievement_score": 0.8,
  "overall_effectiveness_score": 0.85,
  "compliance_requirements": "[\"gdpr\", \"sox\", \"industry_standards\"]",
  "audit_trail": "[\"created\", \"updated\", \"approved\"]",
  "regulatory_impact": "[\"data_protection\", \"financial_regulations\"]",
  "technology_requirements": "[\"cloud_platform\", \"migration_tools\", \"monitoring\"]",
  "system_impact": "[\"legacy_systems\", \"data_warehouse\", \"reporting\"]",
  "integration_requirements": "[\"api_gateway\", \"data_pipeline\", \"monitoring\"]",
  "change_management_plan": "[\"communication\", \"training\", \"support\"]",
  "communication_plan": "[\"weekly_updates\", \"stakeholder_meetings\", \"progress_reports\"]",
  "training_requirements": "[\"cloud_platform\", \"new_processes\", \"tools\"]"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440004",
  "user_id": "550e8400-e29b-41d4-a716-446655440005",
  "name": "Cloud Migration Initiative",
  "description": "Strategic initiative to migrate legacy systems to cloud infrastructure",
  "strategy_type": "transformational",
  "origin_goal_id": "550e8400-e29b-41d4-a716-446655440000",
  "influenced_by_driver_id": "550e8400-e29b-41d4-a716-446655440001",
  "impacted_capability_id": "550e8400-e29b-41d4-a716-446655440002",
  "strategic_objective": "Achieve 99.9% uptime and reduce infrastructure costs by 30%",
  "business_case": "Cost reduction and improved scalability",
  "success_criteria": "{\"uptime\": \"99.9%\", \"cost_reduction\": \"30%\", \"data_loss\": \"0%\"}",
  "key_performance_indicators": "{\"uptime\": \"target\", \"cost_savings\": \"measure\", \"migration_speed\": \"track\"}",
  "time_horizon": "medium_term",
  "start_date": "2024-01-01T00:00:00Z",
  "target_completion_date": "2024-12-31T23:59:59Z",
  "actual_completion_date": null,
  "implementation_phase": "planning",
  "success_probability": 0.8,
  "risk_level": "medium",
  "risk_assessment": "{\"data_migration\": \"high\", \"downtime\": \"medium\"}",
  "contingency_plans": "[\"rollback_plan\", \"parallel_systems\"]",
  "estimated_cost": 1000000.0,
  "actual_cost": null,
  "budget_allocation": 1200000.0,
  "resource_requirements": "{\"developers\": 5, \"devops\": 3, \"qa\": 2}",
  "cost_benefit_analysis": "{\"roi\": \"150%\", \"payback_period\": \"18 months\"}",
  "stakeholders": "[\"cto\", \"cio\", \"business_units\"]",
  "governance_model": "enhanced",
  "approval_status": "pending",
  "approval_date": null,
  "approved_by": null,
  "implementation_approach": "Phased migration with parallel systems",
  "milestones": "[\"planning\", \"pilot\", \"full_migration\", \"validation\"]",
  "dependencies": "[\"infrastructure_ready\", \"team_training\", \"vendor_selection\"]",
  "constraints": "[\"budget_limit\", \"timeline\", \"compliance_requirements\"]",
  "current_progress": 15.0,
  "performance_metrics": "{\"progress\": \"15%\", \"budget_spent\": \"10%\"}",
  "outcomes_achieved": "[\"team_assembled\", \"vendor_selected\"]",
  "lessons_learned": "[\"early_planning_critical\", \"stakeholder_engagement_key\"]",
  "strategic_alignment_score": 0.85,
  "capability_impact_score": 0.9,
  "goal_achievement_score": 0.8,
  "overall_effectiveness_score": 0.85,
  "compliance_requirements": "[\"gdpr\", \"sox\", \"industry_standards\"]",
  "audit_trail": "[\"created\", \"updated\", \"approved\"]",
  "regulatory_impact": "[\"data_protection\", \"financial_regulations\"]",
  "technology_requirements": "[\"cloud_platform\", \"migration_tools\", \"monitoring\"]",
  "system_impact": "[\"legacy_systems\", \"data_warehouse\", \"reporting\"]",
  "integration_requirements": "[\"api_gateway\", \"data_pipeline\", \"monitoring\"]",
  "change_management_plan": "[\"communication\", \"training\", \"support\"]",
  "communication_plan": "[\"weekly_updates\", \"stakeholder_meetings\", \"progress_reports\"]",
  "training_requirements": "[\"cloud_platform\", \"new_processes\", \"tools\"]",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### List Courses of Action

**GET** `/api/v1/courses-of-action`

Lists all CoursesOfAction for the tenant with filtering and pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)
- `strategy_type` (string, optional): Filter by strategy type
- `risk_level` (string, optional): Filter by risk level
- `time_horizon` (string, optional): Filter by time horizon
- `implementation_phase` (string, optional): Filter by implementation phase
- `impacted_capability_id` (UUID, optional): Filter by impacted capability
- `approval_status` (string, optional): Filter by approval status

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440003",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440004",
    "user_id": "550e8400-e29b-41d4-a716-446655440005",
    "name": "Cloud Migration Initiative",
    "description": "Strategic initiative to migrate legacy systems to cloud infrastructure",
    "strategy_type": "transformational",
    "time_horizon": "medium_term",
    "implementation_phase": "planning",
    "success_probability": 0.8,
    "risk_level": "medium",
    "current_progress": 15.0,
    "strategic_alignment_score": 0.85,
    "capability_impact_score": 0.9,
    "goal_achievement_score": 0.8,
    "overall_effectiveness_score": 0.85,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Course of Action

**GET** `/api/v1/courses-of-action/{course_of_action_id}`

Retrieves a CourseOfAction by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440004",
  "user_id": "550e8400-e29b-41d4-a716-446655440005",
  "name": "Cloud Migration Initiative",
  "description": "Strategic initiative to migrate legacy systems to cloud infrastructure",
  "strategy_type": "transformational",
  "origin_goal_id": "550e8400-e29b-41d4-a716-446655440000",
  "influenced_by_driver_id": "550e8400-e29b-41d4-a716-446655440001",
  "impacted_capability_id": "550e8400-e29b-41d4-a716-446655440002",
  "strategic_objective": "Achieve 99.9% uptime and reduce infrastructure costs by 30%",
  "business_case": "Cost reduction and improved scalability",
  "success_criteria": "{\"uptime\": \"99.9%\", \"cost_reduction\": \"30%\", \"data_loss\": \"0%\"}",
  "key_performance_indicators": "{\"uptime\": \"target\", \"cost_savings\": \"measure\", \"migration_speed\": \"track\"}",
  "time_horizon": "medium_term",
  "start_date": "2024-01-01T00:00:00Z",
  "target_completion_date": "2024-12-31T23:59:59Z",
  "actual_completion_date": null,
  "implementation_phase": "planning",
  "success_probability": 0.8,
  "risk_level": "medium",
  "risk_assessment": "{\"data_migration\": \"high\", \"downtime\": \"medium\"}",
  "contingency_plans": "[\"rollback_plan\", \"parallel_systems\"]",
  "estimated_cost": 1000000.0,
  "actual_cost": null,
  "budget_allocation": 1200000.0,
  "resource_requirements": "{\"developers\": 5, \"devops\": 3, \"qa\": 2}",
  "cost_benefit_analysis": "{\"roi\": \"150%\", \"payback_period\": \"18 months\"}",
  "stakeholders": "[\"cto\", \"cio\", \"business_units\"]",
  "governance_model": "enhanced",
  "approval_status": "pending",
  "approval_date": null,
  "approved_by": null,
  "implementation_approach": "Phased migration with parallel systems",
  "milestones": "[\"planning\", \"pilot\", \"full_migration\", \"validation\"]",
  "dependencies": "[\"infrastructure_ready\", \"team_training\", \"vendor_selection\"]",
  "constraints": "[\"budget_limit\", \"timeline\", \"compliance_requirements\"]",
  "current_progress": 15.0,
  "performance_metrics": "{\"progress\": \"15%\", \"budget_spent\": \"10%\"}",
  "outcomes_achieved": "[\"team_assembled\", \"vendor_selected\"]",
  "lessons_learned": "[\"early_planning_critical\", \"stakeholder_engagement_key\"]",
  "strategic_alignment_score": 0.85,
  "capability_impact_score": 0.9,
  "goal_achievement_score": 0.8,
  "overall_effectiveness_score": 0.85,
  "compliance_requirements": "[\"gdpr\", \"sox\", \"industry_standards\"]",
  "audit_trail": "[\"created\", \"updated\", \"approved\"]",
  "regulatory_impact": "[\"data_protection\", \"financial_regulations\"]",
  "technology_requirements": "[\"cloud_platform\", \"migration_tools\", \"monitoring\"]",
  "system_impact": "[\"legacy_systems\", \"data_warehouse\", \"reporting\"]",
  "integration_requirements": "[\"api_gateway\", \"data_pipeline\", \"monitoring\"]",
  "change_management_plan": "[\"communication\", \"training\", \"support\"]",
  "communication_plan": "[\"weekly_updates\", \"stakeholder_meetings\", \"progress_reports\"]",
  "training_requirements": "[\"cloud_platform\", \"new_processes\", \"tools\"]",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Update Course of Action

**PUT** `/api/v1/courses-of-action/{course_of_action_id}`

Updates a CourseOfAction.

**Request Body:** (All fields optional)
```json
{
  "name": "Enhanced Cloud Migration Initiative",
  "description": "Updated description with enhanced security features",
  "success_probability": 0.9,
  "current_progress": 25.0,
  "risk_level": "low"
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "name": "Enhanced Cloud Migration Initiative",
  "description": "Updated description with enhanced security features",
  "success_probability": 0.9,
  "current_progress": 25.0,
  "risk_level": "low",
  "updated_at": "2024-01-15T11:30:00Z"
}
```

### Delete Course of Action

**DELETE** `/api/v1/courses-of-action/{course_of_action_id}`

Deletes a CourseOfAction.

**Response:** `204 No Content`

## Action Link Management

### Create Action Link

**POST** `/api/v1/courses-of-action/{course_of_action_id}/links`

Creates a link between a course of action and another element.

**Request Body:**
```json
{
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440006",
  "linked_element_type": "goal",
  "link_type": "realizes",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "strategic_importance": "high",
  "business_value": "high",
  "alignment_score": 0.9,
  "implementation_priority": "high",
  "implementation_phase": "planning",
  "resource_allocation": 25.0,
  "impact_level": "high",
  "impact_direction": "positive",
  "impact_confidence": 0.85,
  "risk_level": "medium",
  "constraint_level": "medium",
  "risk_mitigation": "[\"monitoring\", \"backup_plans\"]",
  "performance_contribution": 30.0,
  "success_contribution": 25.0,
  "outcome_measurement": "[\"kpi_tracking\", \"regular_assessment\"]"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440007",
  "course_of_action_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440006",
  "linked_element_type": "goal",
  "link_type": "realizes",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "strategic_importance": "high",
  "business_value": "high",
  "alignment_score": 0.9,
  "implementation_priority": "high",
  "implementation_phase": "planning",
  "resource_allocation": 25.0,
  "impact_level": "high",
  "impact_direction": "positive",
  "impact_confidence": 0.85,
  "risk_level": "medium",
  "constraint_level": "medium",
  "risk_mitigation": "[\"monitoring\", \"backup_plans\"]",
  "performance_contribution": 30.0,
  "success_contribution": 25.0,
  "outcome_measurement": "[\"kpi_tracking\", \"regular_assessment\"]",
  "created_by": "550e8400-e29b-41d4-a716-446655440005",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### List Action Links

**GET** `/api/v1/courses-of-action/{course_of_action_id}/links`

Lists all action links for a course of action.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440007",
    "course_of_action_id": "550e8400-e29b-41d4-a716-446655440003",
    "linked_element_id": "550e8400-e29b-41d4-a716-446655440006",
    "linked_element_type": "goal",
    "link_type": "realizes",
    "relationship_strength": "strong",
    "dependency_level": "high",
    "strategic_importance": "high",
    "business_value": "high",
    "alignment_score": 0.9,
    "implementation_priority": "high",
    "implementation_phase": "planning",
    "resource_allocation": 25.0,
    "impact_level": "high",
    "impact_direction": "positive",
    "impact_confidence": 0.85,
    "risk_level": "medium",
    "constraint_level": "medium",
    "risk_mitigation": "[\"monitoring\", \"backup_plans\"]",
    "performance_contribution": 30.0,
    "success_contribution": 25.0,
    "outcome_measurement": "[\"kpi_tracking\", \"regular_assessment\"]",
    "created_by": "550e8400-e29b-41d4-a716-446655440005",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Action Link

**GET** `/api/v1/courses-of-action/links/{link_id}`

Retrieves an action link by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440007",
  "course_of_action_id": "550e8400-e29b-41d4-a716-446655440003",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440006",
  "linked_element_type": "goal",
  "link_type": "realizes",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "strategic_importance": "high",
  "business_value": "high",
  "alignment_score": 0.9,
  "implementation_priority": "high",
  "implementation_phase": "planning",
  "resource_allocation": 25.0,
  "impact_level": "high",
  "impact_direction": "positive",
  "impact_confidence": 0.85,
  "risk_level": "medium",
  "constraint_level": "medium",
  "risk_mitigation": "[\"monitoring\", \"backup_plans\"]",
  "performance_contribution": 30.0,
  "success_contribution": 25.0,
  "outcome_measurement": "[\"kpi_tracking\", \"regular_assessment\"]",
  "created_by": "550e8400-e29b-41d4-a716-446655440005",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Update Action Link

**PUT** `/api/v1/courses-of-action/links/{link_id}`

Updates an action link.

**Request Body:** (All fields optional)
```json
{
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "alignment_score": 0.8,
  "impact_confidence": 0.9
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440007",
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "alignment_score": 0.8,
  "impact_confidence": 0.9
}
```

### Delete Action Link

**DELETE** `/api/v1/courses-of-action/links/{link_id}`

Deletes an action link.

**Response:** `204 No Content`

## Analysis & Alignment Endpoints

### Get Alignment Map

**GET** `/api/v1/courses-of-action/{course_of_action_id}/alignment-map`

Returns alignment mapping for the CourseOfAction.

**Response:** `200 OK`
```json
{
  "course_of_action_id": "550e8400-e29b-41d4-a716-446655440003",
  "strategic_alignment": {
    "score": 0.85,
    "factors": ["goal_alignment", "capability_alignment", "stakeholder_alignment"],
    "status": "high"
  },
  "capability_alignment": {
    "score": 0.9,
    "capability_id": "550e8400-e29b-41d4-a716-446655440002",
    "status": "high"
  },
  "goal_alignment": {
    "score": 0.8,
    "goal_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "high"
  },
  "overall_alignment_score": 0.85,
  "alignment_factors": [
    {
      "factor": "strategic_alignment",
      "score": 0.85
    },
    {
      "factor": "capability_impact",
      "score": 0.9
    },
    {
      "factor": "goal_achievement",
      "score": 0.8
    }
  ],
  "recommendations": [
    "Continue monitoring strategic alignment",
    "Enhance capability impact assessment",
    "Strengthen goal achievement tracking"
  ]
}
```

### Get Risk Profile

**GET** `/api/v1/courses-of-action/{course_of_action_id}/risk-profile`

Returns risk profile for the CourseOfAction.

**Response:** `200 OK`
```json
{
  "course_of_action_id": "550e8400-e29b-41d4-a716-446655440003",
  "overall_risk_score": 0.4,
  "risk_breakdown": {
    "risk_level": "medium",
    "success_probability": 0.8,
    "progress_risk": 0.85
  },
  "risk_factors": [
    {
      "factor": "overall_risk_level",
      "severity": "medium",
      "description": "Medium risk level: medium"
    }
  ],
  "mitigation_strategies": [
    {
      "strategy": "success_improvement",
      "description": "Review and improve success criteria and implementation approach"
    }
  ],
  "contingency_plans": [
    "rollback_plan",
    "parallel_systems"
  ],
  "risk_monitoring": {
    "monitoring_frequency": "monthly",
    "key_metrics": ["progress", "success_probability", "risk_level"],
    "alert_thresholds": {
      "risk_score": 0.7,
      "progress_stall": 0
    }
  },
  "recommendations": [
    "Review and revise success criteria",
    "Accelerate implementation progress"
  ]
}
```

### Analyze Course of Action

**GET** `/api/v1/courses-of-action/{course_of_action_id}/analysis`

Returns comprehensive analysis for the CourseOfAction.

**Response:** `200 OK`
```json
{
  "course_of_action_id": "550e8400-e29b-41d4-a716-446655440003",
  "strategic_analysis": {
    "strategy_type": "transformational",
    "time_horizon": "medium_term",
    "strategic_objective": "Achieve 99.9% uptime and reduce infrastructure costs by 30%",
    "business_case": "Cost reduction and improved scalability",
    "alignment_score": 0.85
  },
  "performance_analysis": {
    "current_progress": 15.0,
    "success_probability": 0.8,
    "implementation_phase": "planning",
    "performance_metrics": {
      "progress": "15%",
      "budget_spent": "10%"
    }
  },
  "risk_analysis": {
    "risk_level": "medium",
    "risk_assessment": {
      "data_migration": "high",
      "downtime": "medium"
    },
    "contingency_plans": [
      "rollback_plan",
      "parallel_systems"
    ]
  },
  "cost_analysis": {
    "estimated_cost": 1000000.0,
    "actual_cost": null,
    "budget_allocation": 1200000.0,
    "cost_benefit_analysis": {
      "roi": "150%",
      "payback_period": "18 months"
    }
  },
  "implementation_analysis": {
    "implementation_approach": "Phased migration with parallel systems",
    "milestones": [
      "planning",
      "pilot",
      "full_migration",
      "validation"
    ],
    "dependencies": [
      "infrastructure_ready",
      "team_training",
      "vendor_selection"
    ],
    "constraints": [
      "budget_limit",
      "timeline",
      "compliance_requirements"
    ]
  },
  "outcome_analysis": {
    "outcomes_achieved": [
      "team_assembled",
      "vendor_selected"
    ],
    "lessons_learned": [
      "early_planning_critical",
      "stakeholder_engagement_key"
    ],
    "overall_effectiveness_score": 0.85
  },
  "recommendations": [
    "Accelerate implementation progress",
    "Review and improve success criteria",
    "Implement comprehensive risk mitigation",
    "Improve strategic alignment"
  ]
}
```

## Domain-Specific Query Endpoints

### Get by Strategy Type

**GET** `/api/v1/courses-of-action/by-type/{strategy_type}`

Returns courses of action filtered by strategy type.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440003",
    "name": "Cloud Migration Initiative",
    "strategy_type": "transformational",
    "implementation_phase": "planning",
    "success_probability": 0.8,
    "risk_level": "medium"
  }
]
```

### Get by Capability

**GET** `/api/v1/courses-of-action/by-capability/{capability_id}`

Returns courses of action filtered by impacted capability.

### Get by Risk Level

**GET** `/api/v1/courses-of-action/by-risk-level/{risk_level}`

Returns courses of action filtered by risk level.

### Get by Time Horizon

**GET** `/api/v1/courses-of-action/by-time-horizon/{time_horizon}`

Returns courses of action filtered by time horizon.

### Get by Element

**GET** `/api/v1/courses-of-action/by-element/{element_type}/{element_id}`

Returns courses of action linked to a specific element.

### Get Active Courses of Action

**GET** `/api/v1/courses-of-action/active`

Returns all active courses of action.

### Get Critical Courses of Action

**GET** `/api/v1/courses-of-action/critical`

Returns all critical courses of action.

## Enumeration Endpoints

### Get Strategy Types

**GET** `/api/v1/courses-of-action/strategy-types`

Returns all available strategy types.

**Response:** `200 OK`
```json
[
  "transformational",
  "incremental",
  "defensive",
  "innovative"
]
```

### Get Time Horizons

**GET** `/api/v1/courses-of-action/time-horizons`

Returns all available time horizons.

**Response:** `200 OK`
```json
[
  "short_term",
  "medium_term",
  "long_term"
]
```

### Get Implementation Phases

**GET** `/api/v1/courses-of-action/implementation-phases`

Returns all available implementation phases.

**Response:** `200 OK`
```json
[
  "planning",
  "active",
  "completed",
  "suspended"
]
```

### Get Risk Levels

**GET** `/api/v1/courses-of-action/risk-levels`

Returns all available risk levels.

**Response:** `200 OK`
```json
[
  "low",
  "medium",
  "high",
  "critical"
]
```

### Get Approval Statuses

**GET** `/api/v1/courses-of-action/approval-statuses`

Returns all available approval statuses.

**Response:** `200 OK`
```json
[
  "draft",
  "pending",
  "approved",
  "rejected",
  "completed"
]
```

### Get Governance Models

**GET** `/api/v1/courses-of-action/governance-models`

Returns all available governance models.

**Response:** `200 OK`
```json
[
  "basic",
  "standard",
  "enhanced",
  "critical"
]
```

### Get Link Types

**GET** `/api/v1/courses-of-action/link-types`

Returns all available link types.

**Response:** `200 OK`
```json
[
  "realizes",
  "supports",
  "enables",
  "influences",
  "constrains",
  "triggers",
  "requires"
]
```

### Get Relationship Strengths

**GET** `/api/v1/courses-of-action/relationship-strengths`

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

**GET** `/api/v1/courses-of-action/dependency-levels`

Returns all available dependency levels.

**Response:** `200 OK`
```json
[
  "high",
  "medium",
  "low"
]
```

### Get Strategic Importances

**GET** `/api/v1/courses-of-action/strategic-importances`

Returns all available strategic importance levels.

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

**GET** `/api/v1/courses-of-action/business-values`

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

### Get Implementation Priorities

**GET** `/api/v1/courses-of-action/implementation-priorities`

Returns all available implementation priorities.

**Response:** `200 OK`
```json
[
  "low",
  "normal",
  "high",
  "critical"
]
```

### Get Impact Levels

**GET** `/api/v1/courses-of-action/impact-levels`

Returns all available impact levels.

**Response:** `200 OK`
```json
[
  "low",
  "medium",
  "high",
  "critical"
]
```

### Get Impact Directions

**GET** `/api/v1/courses-of-action/impact-directions`

Returns all available impact directions.

**Response:** `200 OK`
```json
[
  "positive",
  "negative",
  "neutral"
]
```

### Get Constraint Levels

**GET** `/api/v1/courses-of-action/constraint-levels`

Returns all available constraint levels.

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
  "detail": "Validation error: Invalid strategy type"
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
  "detail": "Insufficient permissions. Required: course_of_action:create, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Course of action not found"
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
- Strategy type
- Risk level
- Time horizon
- Implementation phase
- Impacted capability
- Approval status

## Sorting

Results are sorted by `created_at` in descending order by default.

## OpenAPI Documentation

For complete OpenAPI documentation, visit:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`
