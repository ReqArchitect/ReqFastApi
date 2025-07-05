# Architecture Overview

## Component Diagram
- [Insert diagram here: services, orchestrator, UI, event bus]

## Data Flow & Traceability
- End-to-end traceability from Product Discovery to ArchiMate elements

## Event Bus Topology
- All services emit/consume events via Redis pub/sub

## Observability
- Prometheus, Grafana, OpenTelemetry for metrics, logs, traces
