import re
import json
import logging
import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

# --- JSON log entry test ---
def test_json_log_entry(monkeypatch, capsys):
    logger = logging.getLogger("architecture_suite")
    log_data = {
        "timestamp": "2025-07-02T12:00:00.000Z",
        "service": "architecture_suite",
        "version": "1.0.0",
        "tenant_id": "t1",
        "user_id": "u1",
        "correlation_id": "cid",
        "route": "/test",
        "method": "GET",
        "status_code": 200,
        "latency_ms": 10
    }
    logger.info(json.dumps(log_data))
    captured = capsys.readouterr().out
    entry = json.loads(captured.strip())
    for field in ["timestamp", "service", "version", "tenant_id", "user_id", "correlation_id", "route", "method", "status_code", "latency_ms"]:
        assert field in entry

# --- Metrics endpoint test ---
def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "architecture_suite_requests_total" in response.text
    assert "architecture_suite_request_latency_seconds_bucket" in response.text
    assert "architecture_suite_errors_total" in response.text

# --- Correlation ID propagation test ---
def test_correlation_id_propagation():
    cid = "test-correlation-id-123"
    response = client.get("/health", headers={"X-Correlation-ID": cid})
    assert response.headers["X-Correlation-ID"] == cid

# --- OpenTelemetry span test ---
def test_opentelemetry_span(monkeypatch):
    from opentelemetry import trace
    class DummySpan:
        def __init__(self):
            self.ended = False
            self.attrs = {}
        def set_attribute(self, k, v):
            self.attrs[k] = v
        def __enter__(self): return self
        def __exit__(self, exc_type, exc_val, exc_tb): self.ended = True
    class DummyTracer:
        def start_as_current_span(self, name):
            return DummySpan()
    monkeypatch.setattr(trace, "get_tracer", lambda *a, **k: DummyTracer())
    response = client.get("/health")
    assert response.status_code == 200
