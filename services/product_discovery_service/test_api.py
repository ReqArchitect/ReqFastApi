import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from product_discovery_service.api import router
import types

@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)

def test_business_case_proxy_success(client):
    payload = {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "tenant_id": "tenant-1",
        "user_id": "user-1",
        "created_at": "2025-07-13T12:00:00Z",
        "updated_at": "2025-07-13T12:00:00Z",
        "title": "Test Case",
        "description": "Test Description"
    }
    upstream_response = {
        "uuid": payload["uuid"],
        "tenant_id": payload["tenant_id"],
        "user_id": payload["user_id"],
        "created_at": payload["created_at"],
        "updated_at": payload["updated_at"],
        "title": payload["title"],
        "description": payload["description"]
    }
    # Mock httpx.AsyncClient.post to return a response with status_code 201 and the upstream_response as JSON
    class MockResponse:
        def __init__(self):
            self.status_code = 201
            self._json = upstream_response
            self.content = b'{"uuid": "123e4567-e89b-12d3-a456-426614174000", "tenant_id": "tenant-1", "user_id": "user-1", "created_at": "2025-07-13T12:00:00Z", "updated_at": "2025-07-13T12:00:00Z", "title": "Test Case", "description": "Test Description"}'
            self.headers = {"content-type": "application/json"}
        def json(self):
            return self._json
    async def mock_post(*args, **kwargs):
        return MockResponse()
    with patch("product_discovery_service.api.httpx.AsyncClient.post", new=mock_post), \
         patch("product_discovery_service.api.emit_creation_event") as mock_emit_event:
        response = client.post("/business-cases", json=payload)
        assert response.status_code == 201
        assert response.json() == upstream_response
        mock_emit_event.assert_called_once_with(
            "business_case",
            payload["uuid"],
            payload["tenant_id"],
            payload["user_id"],
            None  # redis_client is None in test
        )

def test_architecture_suite_health(client):
    # Simulate latency and 200 OK response
    class MockHealthResponse:
        def __init__(self):
            self.status_code = 200
            self.elapsed = types.SimpleNamespace(total_seconds=lambda: 0.123)
            self.json = lambda: {"status": "healthy", "latency": 0.123}
    async def mock_get(*args, **kwargs):
        return MockHealthResponse()
    from unittest.mock import patch
    with patch("product_discovery_service.api.httpx.AsyncClient.get", new=mock_get):
        response = client.get("/architecture-suite-health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert isinstance(data["latency"], float)

import pytest
from unittest.mock import patch, AsyncMock

archetypes = [
    {
        "name": "Startup Founder",
        "business_case": {
            "uuid": "11111111-1111-1111-1111-111111111111",
            "tenant_id": "tenant-startup",
            "user_id": "user-founder",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "title": "Disrupt regional freight logistics",
            "description": "Lean strategy for logistics disruption"
        },
        "initiative": {
            "uuid": "22222222-2222-2222-2222-222222222222",
            "tenant_id": "tenant-startup",
            "user_id": "user-founder",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "business_case_id": "11111111-1111-1111-1111-111111111111",
            "name": "Prototype P2P shipment tracking",
            "description": "Build MVP for shipment tracking"
        },
        "kpi": {
            "uuid": "33333333-3333-3333-3333-333333333333",
            "tenant_id": "tenant-startup",
            "user_id": "user-founder",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "initiative_id": "22222222-2222-2222-2222-222222222222",
            "metric": "Cycle time",
            "target_value": 2.5
        },
        "canvas": {
            "uuid": "44444444-4444-4444-4444-444444444444",
            "tenant_id": "tenant-startup",
            "user_id": "user-founder",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "canvas_data": {"assumptions": "Lightweight, validated"}
        }
    },
    {
        "name": "Enterprise Strategist",
        "business_case": {
            "uuid": "55555555-5555-5555-5555-555555555555",
            "tenant_id": "tenant-enterprise",
            "user_id": "user-strategist",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "title": "Expand service uptime to 99.95%",
            "description": "Governance and reliability focus"
        },
        "initiative": {
            "uuid": "66666666-6666-6666-6666-666666666666",
            "tenant_id": "tenant-enterprise",
            "user_id": "user-strategist",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "business_case_id": "55555555-5555-5555-5555-555555555555",
            "name": "Deploy cross-region failover",
            "description": "Implement failover for uptime"
        },
        "kpi": {
            "uuid": "77777777-7777-7777-7777-777777777777",
            "tenant_id": "tenant-enterprise",
            "user_id": "user-strategist",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "initiative_id": "66666666-6666-6666-6666-666666666666",
            "metric": "Downtime",
            "target_value": 20.0
        },
        "canvas": {
            "uuid": "88888888-8888-8888-8888-888888888888",
            "tenant_id": "tenant-enterprise",
            "user_id": "user-strategist",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "canvas_data": {"segments": "Compliance-centered"}
        }
    },
    {
        "name": "Product Manager",
        "business_case": {
            "uuid": "99999999-9999-9999-9999-999999999999",
            "tenant_id": "tenant-pm",
            "user_id": "user-pm",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "title": "Improve onboarding conversion",
            "description": "Conversion-focused onboarding"
        },
        "initiative": {
            "uuid": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "tenant_id": "tenant-pm",
            "user_id": "user-pm",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "business_case_id": "99999999-9999-9999-9999-999999999999",
            "name": "Revamp welcome UX flow",
            "description": "Improve onboarding experience"
        },
        "kpi": {
            "uuid": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "tenant_id": "tenant-pm",
            "user_id": "user-pm",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "initiative_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "metric": "Conversion rate",
            "target_value": 40.0
        },
        "canvas": {
            "uuid": "cccccccc-cccc-cccc-cccc-cccccccccccc",
            "tenant_id": "tenant-pm",
            "user_id": "user-pm",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "canvas_data": {"props": "Refined value props"}
        }
    }
    # Add more archetypes as needed...
]

@pytest.mark.parametrize("archetype", archetypes)
def test_archetype_proxy_and_event(client, archetype):
    with patch("product_discovery_service.api.httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("product_discovery_service.api.emit_creation_event") as mock_emit_event:
        for entity, payload in [
            ("business_case", archetype["business_case"]),
            ("initiative", archetype["initiative"]),
            ("kpi", archetype["kpi"]),
            ("business_model_canvas", archetype["canvas"])
        ]:
            mock_post.return_value.status_code = 201
            mock_post.return_value.json.return_value = payload
            mock_post.return_value.content = str(payload).encode()
            mock_post.return_value.headers = {"content-type": "application/json"}
            endpoint = {
                "business_case": "/business-cases",
                "initiative": "/initiatives",
                "kpi": "/kpis",
                "business_model_canvas": "/business-model-canvas"
            }[entity]
            response = client.post(endpoint, json=payload)
            assert response.status_code == 201
            assert response.json() == payload
            mock_emit_event.assert_called_with(
                entity,
                payload["uuid"],
                payload["tenant_id"],
                payload["user_id"],
                None
            )
            mock_emit_event.reset_mock()

import pytest
from unittest.mock import patch, AsyncMock

role_payloads = [
    {
        "role": "Enterprise Architect",
        "business_case": {
            "uuid": "ea-1111-1111-1111-1111-111111111111",
            "tenant_id": "tenant-ea",
            "user_id": "user-ea",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "title": "Enable cross-region failover",
            "description": "Architect for multi-region redundancy"
        },
        "initiative": {
            "uuid": "ea-2222-2222-2222-2222-222222222222",
            "tenant_id": "tenant-ea",
            "user_id": "user-ea",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "business_case_id": "ea-1111-1111-1111-1111-111111111111",
            "name": "Design multi-zone cluster",
            "description": "Cluster design for failover"
        },
        "kpi": {
            "uuid": "ea-3333-3333-3333-3333-333333333333",
            "tenant_id": "tenant-ea",
            "user_id": "user-ea",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "initiative_id": "ea-2222-2222-2222-2222-222222222222",
            "metric": "Uptime compliance",
            "target_value": 99.95
        },
        "canvas": {
            "uuid": "ea-4444-4444-4444-4444-444444444444",
            "tenant_id": "tenant-ea",
            "user_id": "user-ea",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "canvas_data": {"redundancy": "multi-zone", "partners": "strategic"}
        }
    },
    {
        "role": "Solution Architect",
        "business_case": {
            "uuid": "sa-1111-1111-1111-1111-111111111111",
            "tenant_id": "tenant-sa",
            "user_id": "user-sa",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "title": "Accelerate partner integration",
            "description": "Speed up integration with partners"
        },
        "initiative": {
            "uuid": "sa-2222-2222-2222-2222-222222222222",
            "tenant_id": "tenant-sa",
            "user_id": "user-sa",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "business_case_id": "sa-1111-1111-1111-1111-111111111111",
            "name": "Launch GraphQL orchestration layer",
            "description": "Orchestration for API integration"
        },
        "kpi": {
            "uuid": "sa-3333-3333-3333-3333-333333333333",
            "tenant_id": "tenant-sa",
            "user_id": "user-sa",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "initiative_id": "sa-2222-2222-2222-2222-222222222222",
            "metric": "Time-to-integrate",
            "target_value": 5.0
        },
        "canvas": {
            "uuid": "sa-4444-4444-4444-4444-444444444444",
            "tenant_id": "tenant-sa",
            "user_id": "user-sa",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "canvas_data": {"api_types": "GraphQL", "flow": "diagram"}
        }
    },
    {
        "role": "Technical Architect",
        "business_case": {
            "uuid": "ta-1111-1111-1111-1111-111111111111",
            "tenant_id": "tenant-ta",
            "user_id": "user-ta",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "title": "Reduce cold start latency",
            "description": "Optimize container startup"
        },
        "initiative": {
            "uuid": "ta-2222-2222-2222-2222-222222222222",
            "tenant_id": "tenant-ta",
            "user_id": "user-ta",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "business_case_id": "ta-1111-1111-1111-1111-111111111111",
            "name": "Refactor container networking",
            "description": "Improve networking for startup"
        },
        "kpi": {
            "uuid": "ta-3333-3333-3333-3333-333333333333",
            "tenant_id": "tenant-ta",
            "user_id": "user-ta",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "initiative_id": "ta-2222-2222-2222-2222-222222222222",
            "metric": "Startup latency",
            "target_value": 600.0
        },
        "canvas": {
            "uuid": "ta-4444-4444-4444-4444-444444444444",
            "tenant_id": "tenant-ta",
            "user_id": "user-ta",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "canvas_data": {"docker_layers": "optimized", "load_sequence": "fast"}
        }
    },
    {
        "role": "Business Analyst",
        "business_case": {
            "uuid": "ba-1111-1111-1111-1111-111111111111",
            "tenant_id": "tenant-ba",
            "user_id": "user-ba",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "title": "Validate market entry assumptions",
            "description": "Market entry validation"
        },
        "initiative": {
            "uuid": "ba-2222-2222-2222-2222-222222222222",
            "tenant_id": "tenant-ba",
            "user_id": "user-ba",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "business_case_id": "ba-1111-1111-1111-1111-111111111111",
            "name": "Survey early adopters",
            "description": "Survey for validation"
        },
        "kpi": {
            "uuid": "ba-3333-3333-3333-3333-333333333333",
            "tenant_id": "tenant-ba",
            "user_id": "user-ba",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "initiative_id": "ba-2222-2222-2222-2222-222222222222",
            "metric": "Assumptions validated",
            "target_value": 5.0
        },
        "canvas": {
            "uuid": "ba-4444-4444-4444-4444-444444444444",
            "tenant_id": "tenant-ba",
            "user_id": "user-ba",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "canvas_data": {"value_prop": "strong", "metrics": "key"}
        }
    }
]

@pytest.mark.parametrize("role_data", role_payloads)
def test_role_proxy_and_event(client, role_data):
    with patch("product_discovery_service.api.httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("product_discovery_service.api.emit_creation_event") as mock_emit_event:
        for entity, payload in [
            ("business_case", role_data["business_case"]),
            ("initiative", role_data["initiative"]),
            ("kpi", role_data["kpi"]),
            ("business_model_canvas", role_data["canvas"])
        ]:
            mock_post.return_value.status_code = 201
            mock_post.return_value.json.return_value = payload
            mock_post.return_value.content = str(payload).encode()
            mock_post.return_value.headers = {"content-type": "application/json"}
            endpoint = {
                "business_case": "/business-cases",
                "initiative": "/initiatives",
                "kpi": "/kpis",
                "business_model_canvas": "/business-model-canvas"
            }[entity]
            response = client.post(endpoint, json=payload)
            assert response.status_code == 201
            assert response.json() == payload
            mock_emit_event.assert_called_with(
                entity,
                payload["uuid"],
                payload["tenant_id"],
                payload["user_id"],
                None
            )
            mock_emit_event.reset_mock()

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from product_discovery_service.api import router

@pytest.fixture
def client():
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)

@pytest.mark.api_proxy
def test_trace_id_propagation(client):
    payload = {
        "uuid": "trace-1111-1111-1111-1111-111111111111",
        "tenant_id": "tenant-trace",
        "user_id": "user-trace",
        "created_at": "2025-07-13T12:00:00Z",
        "updated_at": "2025-07-13T12:00:00Z",
        "title": "Trace propagation",
        "description": "Test trace_id propagation"
    }
    trace_id = "test-trace-id-123"
    with patch("product_discovery_service.api.httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("product_discovery_service.api.emit_creation_event") as mock_emit_event:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = payload
        mock_post.return_value.content = str(payload).encode()
        mock_post.return_value.headers = {"content-type": "application/json"}
        def check_headers(*args, **kwargs):
            assert kwargs["headers"].get("trace_id") == trace_id
            return mock_post.return_value
        mock_post.side_effect = check_headers
        response = client.post("/business-cases", json=payload, headers={"trace_id": trace_id})
        assert response.status_code == 201
        assert response.json() == payload
        mock_emit_event.assert_called_once()

@pytest.mark.api_proxy
def test_redis_failure_simulation(client, caplog):
    payload = {
        "uuid": "redis-1111-1111-1111-1111-111111111111",
        "tenant_id": "tenant-redis",
        "user_id": "user-redis",
        "created_at": "2025-07-13T12:00:00Z",
        "updated_at": "2025-07-13T12:00:00Z",
        "title": "Redis failure",
        "description": "Test Redis failure handling"
    }
    with patch("product_discovery_service.api.httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("product_discovery_service.api.emit_creation_event", side_effect=ConnectionError("Redis down")) as mock_emit_event:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = payload
        mock_post.return_value.content = str(payload).encode()
        mock_post.return_value.headers = {"content-type": "application/json"}
        response = client.post("/business-cases", json=payload)
        assert response.status_code == 201
        assert response.json() == payload
        # Check that Redis error was logged (caplog fixture)
        assert any("Redis down" in record.message for record in caplog.records)

# Ensure all test functions are prefixed with test_ and marked for CI
# To run: pytest product_discovery_service/test_api.py -m api_proxy
