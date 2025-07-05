# API Reference: orchestrator_service

## POST /orchestrator/ingest_task
Accepts a Jira task payload and maps it to ArchiMate elements.

**Request:**
```json
{
  "task_id": "JIRA-4567",
  "title": "Implement DigitalOps2025 Initiative",
  "description": "...",
  "jira_type": "Epic",
  "linked_elements": []
}
```
**Response:**
```json
{
  "task_id": "JIRA-4567",
  "title": "Implement DigitalOps2025 Initiative",
  "description": "...",
  "jira_type": "Epic",
  "linked_elements": ["Initiative:DigitalOps2025"]
}
```

## POST /orchestrator/trigger_generation
Triggers a code/documentation generation workflow for a Jira task.

**Request:**
```json
{
  "task_id": "JIRA-4567",
  "generation_type": "backend",
  "model_links": ["Initiative:DigitalOps2025"],
  "status": "pending"
}
```
**Response:**
```json
{
  "task_id": "JIRA-4567",
  "generation_type": "backend",
  "model_links": ["Initiative:DigitalOps2025"],
  "status": "completed"
}
```

## GET /orchestrator/status/{task_id}
Returns generation status for a Jira task.

**Response:**
```json
[
  {
    "task_id": "JIRA-4567",
    "generation_type": "backend",
    "model_links": ["Initiative:DigitalOps2025"],
    "status": "completed"
  }
]
```

## GET /orchestrator/logs/{task_id}
Returns audit logs for a Jira task.

**Response:**
```json
{
  "logs": ["@source:Jira#JIRA-4567 @trace:Initiative:DigitalOps2025"]
}
```

[OpenAPI JSON](./openapi.json)
