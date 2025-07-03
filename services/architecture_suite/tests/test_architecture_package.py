import pytest
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "architecture_suite"


def test_fk_validation_fails(monkeypatch):
    # Simulate DB session returning no FK matches
    class DummySession:
        async def execute(self, *a, **k):
            class DummyResult:
                def scalar(self): return None
                def fetchone(self): return None
                def fetchall(self): return []
            return DummyResult()
        async def commit(self): pass
        async def refresh(self, e): pass
        def add(self, e): pass
    monkeypatch.setattr("app.routes.get_db", lambda: DummySession())
    payload = {
        "tenant_id": "tenant",
        "user_id": "user",
        "business_case_id": "bad",
        "initiative_id": "bad",
        "kpi_id": "bad",
        "business_model_id": "bad",
        "name": "Test",
        "description": "desc"
    }
    headers = {"Authorization": "Bearer testtoken"}
    response = client.post("/architecture-packages/?correlation_id=cid", json=payload, headers=headers)
    assert response.status_code == 400
    assert "Invalid" in response.text

def test_rbac_create_blocked_for_user(monkeypatch):
    # Simulate token_data with role 'user'
    class DummyToken:
        role = "user"
        tenant_id = "tenant"
        user_id = "user"
    monkeypatch.setattr("app.deps.get_current_user", lambda: DummyToken())
    payload = {
        "tenant_id": "tenant",
        "user_id": "user",
        "business_case_id": "id",
        "initiative_id": "id",
        "kpi_id": "id",
        "business_model_id": "id",
        "name": "Test",
        "description": "desc"
    }
    headers = {"Authorization": "Bearer testtoken"}
    response = client.post("/architecture-packages/?correlation_id=cid", json=payload, headers=headers)
    assert response.status_code == 403
    assert "Insufficient permissions" in response.text
