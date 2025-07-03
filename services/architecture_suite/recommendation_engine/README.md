# Recommendation Engine

This service provides AI-driven architecture suggestions based on KPI metrics and usage patterns.

## Endpoint
- `GET /recommendations/{package_id}`: Returns scored recommendations for a given package.

## Inference Logic
- Consumes metrics from the main service (stubbed for now)
- Rule-based and ML model hooks for future extension
