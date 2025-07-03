import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_model_tree():
    resp = client.get("/model/tree")
    assert resp.status_code == 200
    assert "tree" in resp.json()

def test_full_details():
    resp = client.get("/model/Capability/123/full-details")
    assert resp.status_code == 200
    assert resp.json()["element"] == "Capability"
