import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_capability(monkeypatch):
    # Mock DB/session, RBAC, event, etc.
    response = client.post("/capabilities", json={
        "name": "Test Capability",
        "description": "desc",
        "business_case_id": "00000000-0000-0000-0000-000000000001",
        "initiative_id": "00000000-0000-0000-0000-000000000002",
        "kpi_id": "00000000-0000-0000-0000-000000000003",
        "business_model_id": "00000000-0000-0000-0000-000000000004"
    })
    assert response.status_code == 200 or response.status_code == 201

def test_list_capabilities(monkeypatch):
    response = client.get("/capabilities")
    assert response.status_code == 200

# ...more tests for get, update, delete, traceability, impact-summary
# Aim for >90% coverage
