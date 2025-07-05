# API Reference: ai_modeling_service

## POST /ai_modeling/generate
Accepts business context and returns ArchiMate elements.

**Request:**
```json
{
  "tenant_id": "string",
  "user_id": "string",
  "input_type": "goal",
  "input_text": "Optimize supply chain"
}
```
**Response:**
```json
{
  "id": 1,
  "input_id": 1,
  "layer": "Strategy",
  "elements": [{"type": "Goal", "name": "OptimizeSupplyChain"}],
  "traceability": "@source:goal:Optimize supply chain",
  "created_at": "2025-07-05T12:00:00Z"
}
```

## GET /ai_modeling/history/{user_id}
Returns previous generations for a user.

**Response:**
```json
[
  {
    "id": 1,
    "input_id": 1,
    "layer": "Strategy",
    "elements": [{"type": "Goal", "name": "OptimizeSupplyChain"}],
    "traceability": "@source:goal:Optimize supply chain",
    "created_at": "2025-07-05T12:00:00Z"
  }
]
```

## POST /ai_modeling/feedback
Submit feedback on a modeling output.

**Request:**
```json
{
  "output_id": 1,
  "user_id": "string",
  "rating": 5,
  "comments": "Great suggestion!"
}
```
**Response:**
```json
{"status": "ok"}
```

[OpenAPI JSON](./openapi.json)
