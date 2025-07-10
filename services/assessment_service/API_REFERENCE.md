# API Reference: assessment_service

## Overview

The Assessment Service provides comprehensive management of ArchiMate 3.2 Assessment elements with full CRUD operations, relationship management, analysis capabilities, and domain-specific queries.

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

## Assessment Management

### Create Assessment

**POST** `/api/v1/assessments`

Creates a new Assessment.

**Request Body:**
```json
{
  "name": "Strategic Maturity Assessment (Q2)",
  "description": "Quarterly strategic maturity evaluation",
  "assessment_type": "maturity",
  "evaluated_goal_id": "550e8400-e29b-41d4-a716-446655440001",
  "evaluated_capability_id": "550e8400-e29b-41d4-a716-446655440002",
  "evaluated_business_function_id": "550e8400-e29b-41d4-a716-446655440003",
  "evaluated_stakeholder_id": "550e8400-e29b-41d4-a716-446655440004",
  "evaluated_constraint_id": "550e8400-e29b-41d4-a716-446655440005",
  "evaluator_user_id": "550e8400-e29b-41d4-a716-446655440006",
  "assessment_method": "mixed",
  "result_summary": "Strategic maturity shows improvement in key areas",
  "metrics_scored": "{\"strategic_alignment\": {\"score\": 0.8, \"weight\": 0.3}, \"execution_capability\": {\"score\": 0.75, \"weight\": 0.3}, \"innovation_culture\": {\"score\": 0.7, \"weight\": 0.2}, \"risk_management\": {\"score\": 0.85, \"weight\": 0.2}}",
  "confidence_level": "high",
  "confidence_score": 0.85,
  "date_conducted": "2024-01-15T10:30:00Z",
  "planned_start_date": "2024-01-15T00:00:00Z",
  "planned_end_date": "2024-01-30T00:00:00Z",
  "actual_start_date": "2024-01-15T09:00:00Z",
  "actual_end_date": "2024-01-28T17:00:00Z",
  "status": "complete",
  "progress_percent": 100.0,
  "assessment_framework": "TOGAF",
  "assessment_criteria": "[\"Strategic Alignment\", \"Execution Capability\", \"Innovation Culture\", \"Risk Management\"]",
  "assessment_questions": "[\"How well aligned is the strategy with business objectives?\", \"What is the organization's capability to execute strategic initiatives?\", \"How mature is the innovation culture?\", \"How effective is risk management?\"",
  "assessment_responses": "{\"strategic_alignment\": \"Strong alignment with clear objectives\", \"execution_capability\": \"Good capability with room for improvement\", \"innovation_culture\": \"Developing culture with potential\", \"risk_management\": \"Effective risk management processes\"}",
  "key_findings": "[\"Strong strategic alignment\", \"Good execution capability\", \"Innovation culture needs development\", \"Effective risk management\"]",
  "recommendations": "[\"Invest in innovation programs\", \"Enhance execution processes\", \"Strengthen strategic communication\"]",
  "risk_implications": "{\"low_risk\": [\"Strong foundation\"], \"medium_risk\": [\"Innovation gap\"], \"high_risk\": [\"None identified\"]}",
  "improvement_opportunities": "[\"Innovation culture development\", \"Process optimization\", \"Communication enhancement\"]",
  "quality_score": 0.9,
  "validation_status": "validated",
  "validated_by": "550e8400-e29b-41d4-a716-446655440007",
  "validation_date": "2024-01-29T10:00:00Z",
  "stakeholders": "[\"550e8400-e29b-41d4-a716-446655440008\", \"550e8400-e29b-41d4-a716-446655440009\"]",
  "participants": "[\"550e8400-e29b-41d4-a716-446655440010\", \"550e8400-e29b-41d4-a716-446655440011\"]",
  "reviewers": "[\"550e8400-e29b-41d4-a716-446655440012\"]",
  "compliance_standards": "[\"ISO27001\", \"COBIT\"]",
  "regulatory_requirements": "[\"GDPR\", \"SOX\"]",
  "audit_trail": "[\"Assessment initiated\", \"Data collected\", \"Analysis completed\", \"Validation performed\"]",
  "report_template": "strategic_maturity_report",
  "report_generated": true,
  "report_url": "https://reports.example.com/assessment/12345",
  "communication_plan": "{\"stakeholders\": [\"Executives\", \"Managers\"], \"frequency\": \"quarterly\", \"channels\": [\"email\", \"presentation\"]}",
  "tags": "[\"strategic\", \"maturity\", \"quarterly\"]",
  "priority": 2,
  "complexity": "medium"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440013",
  "user_id": "550e8400-e29b-41d4-a716-446655440014",
  "name": "Strategic Maturity Assessment (Q2)",
  "description": "Quarterly strategic maturity evaluation",
  "assessment_type": "maturity",
  "evaluated_goal_id": "550e8400-e29b-41d4-a716-446655440001",
  "evaluated_capability_id": "550e8400-e29b-41d4-a716-446655440002",
  "evaluated_business_function_id": "550e8400-e29b-41d4-a716-446655440003",
  "evaluated_stakeholder_id": "550e8400-e29b-41d4-a716-446655440004",
  "evaluated_constraint_id": "550e8400-e29b-41d4-a716-446655440005",
  "evaluator_user_id": "550e8400-e29b-41d4-a716-446655440006",
  "assessment_method": "mixed",
  "result_summary": "Strategic maturity shows improvement in key areas",
  "metrics_scored": "{\"strategic_alignment\": {\"score\": 0.8, \"weight\": 0.3}, \"execution_capability\": {\"score\": 0.75, \"weight\": 0.3}, \"innovation_culture\": {\"score\": 0.7, \"weight\": 0.2}, \"risk_management\": {\"score\": 0.85, \"weight\": 0.2}}",
  "confidence_level": "high",
  "confidence_score": 0.85,
  "date_conducted": "2024-01-15T10:30:00Z",
  "planned_start_date": "2024-01-15T00:00:00Z",
  "planned_end_date": "2024-01-30T00:00:00Z",
  "actual_start_date": "2024-01-15T09:00:00Z",
  "actual_end_date": "2024-01-28T17:00:00Z",
  "status": "complete",
  "progress_percent": 100.0,
  "assessment_framework": "TOGAF",
  "assessment_criteria": "[\"Strategic Alignment\", \"Execution Capability\", \"Innovation Culture\", \"Risk Management\"]",
  "assessment_questions": "[\"How well aligned is the strategy with business objectives?\", \"What is the organization's capability to execute strategic initiatives?\", \"How mature is the innovation culture?\", \"How effective is risk management?\"",
  "assessment_responses": "{\"strategic_alignment\": \"Strong alignment with clear objectives\", \"execution_capability\": \"Good capability with room for improvement\", \"innovation_culture\": \"Developing culture with potential\", \"risk_management\": \"Effective risk management processes\"}",
  "key_findings": "[\"Strong strategic alignment\", \"Good execution capability\", \"Innovation culture needs development\", \"Effective risk management\"]",
  "recommendations": "[\"Invest in innovation programs\", \"Enhance execution processes\", \"Strengthen strategic communication\"]",
  "risk_implications": "{\"low_risk\": [\"Strong foundation\"], \"medium_risk\": [\"Innovation gap\"], \"high_risk\": [\"None identified\"]}",
  "improvement_opportunities": "[\"Innovation culture development\", \"Process optimization\", \"Communication enhancement\"]",
  "quality_score": 0.9,
  "validation_status": "validated",
  "validated_by": "550e8400-e29b-41d4-a716-446655440007",
  "validation_date": "2024-01-29T10:00:00Z",
  "stakeholders": "[\"550e8400-e29b-41d4-a716-446655440008\", \"550e8400-e29b-41d4-a716-446655440009\"]",
  "participants": "[\"550e8400-e29b-41d4-a716-446655440010\", \"550e8400-e29b-41d4-a716-446655440011\"]",
  "reviewers": "[\"550e8400-e29b-41d4-a716-446655440012\"]",
  "compliance_standards": "[\"ISO27001\", \"COBIT\"]",
  "regulatory_requirements": "[\"GDPR\", \"SOX\"]",
  "audit_trail": "[\"Assessment initiated\", \"Data collected\", \"Analysis completed\", \"Validation performed\"]",
  "report_template": "strategic_maturity_report",
  "report_generated": true,
  "report_url": "https://reports.example.com/assessment/12345",
  "communication_plan": "{\"stakeholders\": [\"Executives\", \"Managers\"], \"frequency\": \"quarterly\", \"channels\": [\"email\", \"presentation\"]}",
  "tags": "[\"strategic\", \"maturity\", \"quarterly\"]",
  "priority": 2,
  "complexity": "medium",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### List Assessments

**GET** `/api/v1/assessments`

Lists all Assessments for the tenant with filtering and pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)
- `assessment_type` (string, optional): Filter by assessment type
- `status` (string, optional): Filter by status
- `evaluator_user_id` (UUID, optional): Filter by evaluator
- `evaluated_goal_id` (UUID, optional): Filter by evaluated goal
- `date_from` (datetime, optional): Filter by date from
- `date_to` (datetime, optional): Filter by date to
- `confidence_threshold` (float, optional): Filter by minimum confidence score

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Strategic Maturity Assessment (Q2)",
    "assessment_type": "maturity",
    "status": "complete",
    "progress_percent": 100.0,
    "confidence_level": "high",
    "confidence_score": 0.85,
    "evaluator_user_id": "550e8400-e29b-41d4-a716-446655440006",
    "date_conducted": "2024-01-15T10:30:00Z",
    "quality_score": 0.9,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Assessment

**GET** `/api/v1/assessments/{assessment_id}`

Retrieves an Assessment by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440013",
  "user_id": "550e8400-e29b-41d4-a716-446655440014",
  "name": "Strategic Maturity Assessment (Q2)",
  "description": "Quarterly strategic maturity evaluation",
  "assessment_type": "maturity",
  "evaluated_goal_id": "550e8400-e29b-41d4-a716-446655440001",
  "evaluated_capability_id": "550e8400-e29b-41d4-a716-446655440002",
  "evaluated_business_function_id": "550e8400-e29b-41d4-a716-446655440003",
  "evaluated_stakeholder_id": "550e8400-e29b-41d4-a716-446655440004",
  "evaluated_constraint_id": "550e8400-e29b-41d4-a716-446655440005",
  "evaluator_user_id": "550e8400-e29b-41d4-a716-446655440006",
  "assessment_method": "mixed",
  "result_summary": "Strategic maturity shows improvement in key areas",
  "metrics_scored": "{\"strategic_alignment\": {\"score\": 0.8, \"weight\": 0.3}, \"execution_capability\": {\"score\": 0.75, \"weight\": 0.3}, \"innovation_culture\": {\"score\": 0.7, \"weight\": 0.2}, \"risk_management\": {\"score\": 0.85, \"weight\": 0.2}}",
  "confidence_level": "high",
  "confidence_score": 0.85,
  "date_conducted": "2024-01-15T10:30:00Z",
  "planned_start_date": "2024-01-15T00:00:00Z",
  "planned_end_date": "2024-01-30T00:00:00Z",
  "actual_start_date": "2024-01-15T09:00:00Z",
  "actual_end_date": "2024-01-28T17:00:00Z",
  "status": "complete",
  "progress_percent": 100.0,
  "assessment_framework": "TOGAF",
  "assessment_criteria": "[\"Strategic Alignment\", \"Execution Capability\", \"Innovation Culture\", \"Risk Management\"]",
  "assessment_questions": "[\"How well aligned is the strategy with business objectives?\", \"What is the organization's capability to execute strategic initiatives?\", \"How mature is the innovation culture?\", \"How effective is risk management?\"",
  "assessment_responses": "{\"strategic_alignment\": \"Strong alignment with clear objectives\", \"execution_capability\": \"Good capability with room for improvement\", \"innovation_culture\": \"Developing culture with potential\", \"risk_management\": \"Effective risk management processes\"}",
  "key_findings": "[\"Strong strategic alignment\", \"Good execution capability\", \"Innovation culture needs development\", \"Effective risk management\"]",
  "recommendations": "[\"Invest in innovation programs\", \"Enhance execution processes\", \"Strengthen strategic communication\"]",
  "risk_implications": "{\"low_risk\": [\"Strong foundation\"], \"medium_risk\": [\"Innovation gap\"], \"high_risk\": [\"None identified\"]}",
  "improvement_opportunities": "[\"Innovation culture development\", \"Process optimization\", \"Communication enhancement\"]",
  "quality_score": 0.9,
  "validation_status": "validated",
  "validated_by": "550e8400-e29b-41d4-a716-446655440007",
  "validation_date": "2024-01-29T10:00:00Z",
  "stakeholders": "[\"550e8400-e29b-41d4-a716-446655440008\", \"550e8400-e29b-41d4-a716-446655440009\"]",
  "participants": "[\"550e8400-e29b-41d4-a716-446655440010\", \"550e8400-e29b-41d4-a716-446655440011\"]",
  "reviewers": "[\"550e8400-e29b-41d4-a716-446655440012\"]",
  "compliance_standards": "[\"ISO27001\", \"COBIT\"]",
  "regulatory_requirements": "[\"GDPR\", \"SOX\"]",
  "audit_trail": "[\"Assessment initiated\", \"Data collected\", \"Analysis completed\", \"Validation performed\"]",
  "report_template": "strategic_maturity_report",
  "report_generated": true,
  "report_url": "https://reports.example.com/assessment/12345",
  "communication_plan": "{\"stakeholders\": [\"Executives\", \"Managers\"], \"frequency\": \"quarterly\", \"channels\": [\"email\", \"presentation\"]}",
  "tags": "[\"strategic\", \"maturity\", \"quarterly\"]",
  "priority": 2,
  "complexity": "medium",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Update Assessment

**PUT** `/api/v1/assessments/{assessment_id}`

Updates an Assessment.

**Request Body:** (All fields optional)
```json
{
  "name": "Updated Strategic Maturity Assessment (Q2)",
  "description": "Updated quarterly strategic maturity evaluation",
  "confidence_score": 0.9,
  "quality_score": 0.95,
  "status": "complete"
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Updated Strategic Maturity Assessment (Q2)",
  "description": "Updated quarterly strategic maturity evaluation",
  "confidence_score": 0.9,
  "quality_score": 0.95,
  "status": "complete",
  "updated_at": "2024-01-15T11:30:00Z"
}
```

### Delete Assessment

**DELETE** `/api/v1/assessments/{assessment_id}`

Deletes an Assessment.

**Response:** `204 No Content`

## Assessment Link Management

### Create Assessment Link

**POST** `/api/v1/assessments/{assessment_id}/links`

Creates a link between an assessment and another element.

**Request Body:**
```json
{
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440015",
  "linked_element_type": "goal",
  "link_type": "evaluates",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "impact_level": "high",
  "impact_description": "Direct evaluation of strategic goal achievement",
  "impact_metrics": "{\"goal_alignment\": 0.9, \"performance_impact\": 0.85}",
  "evidence_provided": "[\"Performance data\", \"Stakeholder interviews\", \"Documentation review\"]",
  "evidence_quality": 0.9,
  "validation_status": "validated",
  "validated_by": "550e8400-e29b-41d4-a716-446655440007",
  "validation_date": "2024-01-29T10:00:00Z",
  "contribution_score": 0.85,
  "contribution_description": "Significant contribution to strategic goal evaluation",
  "contribution_metrics": "{\"strategic_alignment\": 0.9, \"execution_capability\": 0.8}"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440016",
  "assessment_id": "550e8400-e29b-41d4-a716-446655440000",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440015",
  "linked_element_type": "goal",
  "link_type": "evaluates",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "impact_level": "high",
  "impact_description": "Direct evaluation of strategic goal achievement",
  "impact_metrics": "{\"goal_alignment\": 0.9, \"performance_impact\": 0.85}",
  "evidence_provided": "[\"Performance data\", \"Stakeholder interviews\", \"Documentation review\"]",
  "evidence_quality": 0.9,
  "validation_status": "validated",
  "validated_by": "550e8400-e29b-41d4-a716-446655440007",
  "validation_date": "2024-01-29T10:00:00Z",
  "contribution_score": 0.85,
  "contribution_description": "Significant contribution to strategic goal evaluation",
  "contribution_metrics": "{\"strategic_alignment\": 0.9, \"execution_capability\": 0.8}",
  "created_by": "550e8400-e29b-41d4-a716-446655440014",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### List Assessment Links

**GET** `/api/v1/assessments/{assessment_id}/links`

Lists all links for an assessment.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440016",
    "assessment_id": "550e8400-e29b-41d4-a716-446655440000",
    "linked_element_id": "550e8400-e29b-41d4-a716-446655440015",
    "linked_element_type": "goal",
    "link_type": "evaluates",
    "relationship_strength": "strong",
    "dependency_level": "high",
    "impact_level": "high",
    "impact_description": "Direct evaluation of strategic goal achievement",
    "impact_metrics": "{\"goal_alignment\": 0.9, \"performance_impact\": 0.85}",
    "evidence_provided": "[\"Performance data\", \"Stakeholder interviews\", \"Documentation review\"]",
    "evidence_quality": 0.9,
    "validation_status": "validated",
    "validated_by": "550e8400-e29b-41d4-a716-446655440007",
    "validation_date": "2024-01-29T10:00:00Z",
    "contribution_score": 0.85,
    "contribution_description": "Significant contribution to strategic goal evaluation",
    "contribution_metrics": "{\"strategic_alignment\": 0.9, \"execution_capability\": 0.8}",
    "created_by": "550e8400-e29b-41d4-a716-446655440014",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Assessment Link

**GET** `/api/v1/assessments/links/{link_id}`

Retrieves an assessment link by ID.

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440016",
  "assessment_id": "550e8400-e29b-41d4-a716-446655440000",
  "linked_element_id": "550e8400-e29b-41d4-a716-446655440015",
  "linked_element_type": "goal",
  "link_type": "evaluates",
  "relationship_strength": "strong",
  "dependency_level": "high",
  "impact_level": "high",
  "impact_description": "Direct evaluation of strategic goal achievement",
  "impact_metrics": "{\"goal_alignment\": 0.9, \"performance_impact\": 0.85}",
  "evidence_provided": "[\"Performance data\", \"Stakeholder interviews\", \"Documentation review\"]",
  "evidence_quality": 0.9,
  "validation_status": "validated",
  "validated_by": "550e8400-e29b-41d4-a716-446655440007",
  "validation_date": "2024-01-29T10:00:00Z",
  "contribution_score": 0.85,
  "contribution_description": "Significant contribution to strategic goal evaluation",
  "contribution_metrics": "{\"strategic_alignment\": 0.9, \"execution_capability\": 0.8}",
  "created_by": "550e8400-e29b-41d4-a716-446655440014",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Update Assessment Link

**PUT** `/api/v1/assessments/links/{link_id}`

Updates an assessment link.

**Request Body:** (All fields optional)
```json
{
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "impact_level": "medium",
  "evidence_quality": 0.85
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440016",
  "relationship_strength": "medium",
  "dependency_level": "medium",
  "impact_level": "medium",
  "evidence_quality": 0.85
}
```

### Delete Assessment Link

**DELETE** `/api/v1/assessments/links/{link_id}`

Deletes an assessment link.

**Response:** `204 No Content`

## Analysis Endpoints

### Get Evaluation Metrics

**GET** `/api/v1/assessments/{assessment_id}/evaluation-metrics`

Returns evaluation metrics analysis for the Assessment.

**Response:** `200 OK`
```json
{
  "assessment_id": "550e8400-e29b-41d4-a716-446655440000",
  "overall_score": 0.825,
  "metrics_breakdown": {
    "total_metrics": 4,
    "metrics_by_category": {
      "strategic": [
        {
          "name": "strategic_alignment",
          "score": 0.8,
          "weight": 0.3
        }
      ],
      "execution": [
        {
          "name": "execution_capability",
          "score": 0.75,
          "weight": 0.3
        }
      ],
      "culture": [
        {
          "name": "innovation_culture",
          "score": 0.7,
          "weight": 0.2
        }
      ],
      "risk": [
        {
          "name": "risk_management",
          "score": 0.85,
          "weight": 0.2
        }
      ]
    },
    "score_distribution": {
      "excellent": 1,
      "good": 2,
      "fair": 1,
      "poor": 0
    },
    "top_performers": ["risk_management"],
    "areas_for_improvement": ["innovation_culture"]
  },
  "performance_analysis": {
    "completion_rate": 100.0,
    "timeline_performance": {
      "planned_duration": 15,
      "actual_duration": 13,
      "on_schedule": true,
      "efficiency_score": 1.15
    },
    "method_effectiveness": {
      "method": "mixed",
      "effectiveness_score": 0.8,
      "strengths": ["Comprehensive approach", "Balanced perspective"],
      "weaknesses": ["Complex implementation", "Resource intensive"]
    },
    "evaluator_performance": {
      "evaluator_id": "550e8400-e29b-41d4-a716-446655440006",
      "assessment_count": 1,
      "average_quality_score": 0.9,
      "confidence_trend": "stable"
    }
  },
  "quality_analysis": {
    "quality_score": 0.9,
    "validation_status": "validated",
    "evidence_quality": 0.9,
    "framework_compliance": {
      "framework": "TOGAF",
      "compliance_score": 0.8,
      "compliance_standards": ["ISO27001", "COBIT"],
      "gaps": []
    },
    "quality_factors": [
      "High quality evidence",
      "High confidence in results",
      "Validated assessment"
    ]
  },
  "confidence_analysis": {
    "confidence_score": 0.85,
    "confidence_level": "high",
    "confidence_factors": [
      "Strong evidence base",
      "Clear assessment criteria",
      "Quantitative measurement"
    ],
    "uncertainty_areas": [],
    "confidence_trend": "stable"
  },
  "recommendations": [
    "Invest in innovation programs",
    "Enhance execution processes",
    "Strengthen strategic communication"
  ]
}
```

### Get Confidence Score

**GET** `/api/v1/assessments/{assessment_id}/confidence-score`

Returns confidence score analysis for the Assessment.

**Response:** `200 OK`
```json
{
  "assessment_id": "550e8400-e29b-41d4-a716-446655440000",
  "confidence_score": 0.85,
  "confidence_level": "high",
  "evidence_quality": 0.9,
  "validation_status": "validated",
  "contributing_factors": [
    {
      "factor": "Evidence Quality",
      "score": 0.9,
      "weight": 0.3,
      "description": "Quality of evidence provided"
    },
    {
      "factor": "Assessment Method",
      "score": 0.8,
      "weight": 0.2,
      "description": "Effectiveness of assessment method"
    },
    {
      "factor": "Validation Status",
      "score": 1.0,
      "weight": 0.2,
      "description": "Assessment validation status"
    },
    {
      "factor": "Evaluator Experience",
      "score": 0.8,
      "weight": 0.3,
      "description": "Evaluator expertise and experience"
    }
  ],
  "recommendations": [
    "Maintain high evidence quality standards",
    "Continue using mixed assessment methods",
    "Ensure regular validation processes"
  ]
}
```

## Domain-Specific Query Endpoints

### Get by Assessment Type

**GET** `/api/v1/assessments/by-type/{assessment_type}`

Returns assessments filtered by type.

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Strategic Maturity Assessment (Q2)",
    "assessment_type": "maturity",
    "status": "complete"
  }
]
```

### Get by Status

**GET** `/api/v1/assessments/by-status/{status}`

Returns assessments filtered by status.

### Get by Evaluator

**GET** `/api/v1/assessments/by-evaluator/{evaluator_user_id}`

Returns assessments filtered by evaluator.

### Get by Goal

**GET** `/api/v1/assessments/by-goal/{goal_id}`

Returns assessments filtered by evaluated goal.

### Get by Date Range

**GET** `/api/v1/assessments/by-date-range`

Returns assessments filtered by date range.

**Query Parameters:**
- `date_from` (datetime, required): Start date
- `date_to` (datetime, required): End date

### Get by Confidence Threshold

**GET** `/api/v1/assessments/by-confidence/{confidence_threshold}`

Returns assessments with confidence score above threshold.

### Get Active Assessments

**GET** `/api/v1/assessments/active`

Returns all active assessments (in progress or planned).

### Get Completed Assessments

**GET** `/api/v1/assessments/completed`

Returns all completed assessments.

## Enumeration Endpoints

### Get Assessment Types

**GET** `/api/v1/assessments/assessment-types`

Returns all available assessment types.

**Response:** `200 OK`
```json
{
  "values": [
    "performance",
    "compliance",
    "strategic",
    "risk",
    "maturity",
    "capability",
    "goal",
    "outcome"
  ]
}
```

### Get Statuses

**GET** `/api/v1/assessments/statuses`

Returns all available statuses.

**Response:** `200 OK`
```json
{
  "values": [
    "planned",
    "in_progress",
    "complete",
    "cancelled",
    "on_hold",
    "draft",
    "review"
  ]
}
```

### Get Assessment Methods

**GET** `/api/v1/assessments/assessment-methods`

Returns all available assessment methods.

**Response:** `200 OK`
```json
{
  "values": [
    "quantitative",
    "qualitative",
    "mixed",
    "survey",
    "interview",
    "observation",
    "document_review",
    "metrics_analysis"
  ]
}
```

### Get Confidence Levels

**GET** `/api/v1/assessments/confidence-levels`

Returns all available confidence levels.

**Response:** `200 OK`
```json
{
  "values": [
    "very_low",
    "low",
    "medium",
    "high",
    "very_high"
  ]
}
```

### Get Link Types

**GET** `/api/v1/assessments/link-types`

Returns all available link types.

**Response:** `200 OK`
```json
{
  "values": [
    "evaluates",
    "measures",
    "validates",
    "supports",
    "influences",
    "constrains",
    "enables",
    "impacts"
  ]
}
```

### Get Relationship Strengths

**GET** `/api/v1/assessments/relationship-strengths`

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

**GET** `/api/v1/assessments/dependency-levels`

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

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error: Invalid assessment type"
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
  "detail": "Insufficient permissions. Required: assessment:create, Role: Viewer"
}
```

### 404 Not Found
```json
{
  "detail": "Assessment not found"
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
- Assessment type
- Status
- Evaluator
- Evaluated goal
- Date range
- Confidence threshold

## Sorting

Results are sorted by `created_at` in descending order by default.

## OpenAPI Documentation

For complete OpenAPI documentation, visit:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json` 