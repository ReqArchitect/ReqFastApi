import uuid
from datetime import datetime

def to_jsonable(obj):
    if isinstance(obj, dict):
        return {k: to_jsonable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_jsonable(v) for v in obj]
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, Mock
from services.product_discovery_service.api import router
import types

# Utility to serialize payloads for FastAPI validation
import copy

def serialize_payload(payload):
    import copy
    result = copy.deepcopy(payload)
    for key, value in result.items():
        if ("uuid" in key or "_id" in key) and not isinstance(value, str):
            result[key] = str(value)
        if key in ("created_at", "updated_at"):
            if hasattr(value, "isoformat"):
                result[key] = value.isoformat()
            elif isinstance(value, str):
                # Always enforce strict ISO format with timezone
                if value.endswith("Z"):
                    result[key] = value.replace("Z", "+00:00")
                elif "+00:00" not in value:
                    result[key] = value + "+00:00"
                else:
                    result[key] = value
    return result

# Schema field definitions for strict alignment
BUSINESS_CASE_FIELDS = [
    "uuid", "tenant_id", "user_id", "created_at", "updated_at", "title", "description"
]
INITIATIVE_FIELDS = [
    "uuid", "tenant_id", "user_id", "created_at", "updated_at", "business_case_id", "name", "description"
]
KPI_FIELDS = [
    "uuid", "tenant_id", "user_id", "created_at", "updated_at", "initiative_id", "metric", "target_value"
]
CANVAS_FIELDS = [
    "uuid", "tenant_id", "user_id", "created_at", "updated_at", "canvas_data"
]

ENTITY_FIELDS = {
    "business_case": BUSINESS_CASE_FIELDS,
    "initiative": INITIATIVE_FIELDS,
    "kpi": KPI_FIELDS,
    "business_model_canvas": CANVAS_FIELDS,
}

def filter_payload(payload, fields):
    return {k: v for k, v in payload.items() if k in fields}


from fastapi import FastAPI, Request
import logging

def get_test_app() -> FastAPI:
    app = FastAPI()

    # 🔎 Middleware for debugging incoming requests during test runs
    @app.middleware("http")
    async def log_test_request(request: Request, call_next):
        body = await request.body()
        logging.warning(f"\n📥 TEST REQUEST: {request.method} {request.url.path}")
        logging.warning(f"Headers: {dict(request.headers)}")
        logging.warning(f"Body: {body.decode()}")
        response = await call_next(request)
        logging.warning(f"📤 RESPONSE STATUS: {response.status_code}")
        return response

    # ✅ Mount router under test
    from services.product_discovery_service.api import router
    app.include_router(router)
    return app

@pytest.fixture
def client():
    return TestClient(get_test_app())

def test_business_case_proxy_success(client):
    from services.product_discovery_service.schemas import BusinessCase
    from datetime import datetime
    from uuid import uuid4
    payload_obj = BusinessCase(
        uuid=str(uuid4()),
        tenant_id="tenant-1",
        user_id="user-1",
        title="Test Case",
        description="Test Description",
        created_at=datetime.utcnow().isoformat()+"+00:00",
        updated_at=datetime.utcnow().isoformat()+"+00:00"
    )
    payload = payload_obj.model_dump()
    payload_for_post = serialize_payload(payload)
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = payload_for_post
    import json
    mock_response.content = json.dumps(payload_for_post).encode()
    mock_response.headers = {"content-type": "application/json"}
    with patch("services.product_discovery_service.api.httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("services.product_discovery_service.api.emit_creation_event") as mock_emit_event:
        mock_post.return_value = mock_response
        response = client.post("/business-cases", json=payload_for_post)
        assert response.status_code == 201
        assert response.json() == payload_for_post
        mock_emit_event.assert_called_once_with(
            "business_case",
            payload_for_post["uuid"],
            payload_for_post["tenant_id"],
            payload_for_post["user_id"],
            None
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
    with patch("services.product_discovery_service.api.httpx.AsyncClient.get", new=mock_get):
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
        "created_at": "2025-07-13T12:00:00+00:00",
        "updated_at": "2025-07-13T12:00:00+00:00",
            "title": "Disrupt regional freight logistics",
            "description": "Lean strategy for logistics disruption"
        },
        "initiative": {
            "uuid": "22222222-2222-2222-2222-222222222222",
            "tenant_id": "tenant-startup",
            "user_id": "user-founder",
        "created_at": "2025-07-13T12:00:00+00:00",
        "updated_at": "2025-07-13T12:00:00+00:00",
            "business_case_id": "11111111-1111-1111-1111-111111111111",
            "name": "Prototype P2P shipment tracking",
            "description": "Build MVP for shipment tracking"
        },
        "kpi": {
            "uuid": "33333333-3333-3333-3333-333333333333",
            "tenant_id": "tenant-startup",
            "user_id": "user-founder",
        "created_at": "2025-07-13T12:00:00+00:00",
        "updated_at": "2025-07-13T12:00:00+00:00",
            "initiative_id": "22222222-2222-2222-2222-222222222222",
            "metric": "Cycle time",
            "target_value": 2.5
        },
        "canvas": {
            "uuid": "44444444-4444-4444-4444-444444444444",
            "tenant_id": "tenant-startup",
            "user_id": "user-founder",
        "created_at": "2025-07-13T12:00:00+00:00",
        "updated_at": "2025-07-13T12:00:00+00:00",
            "canvas_data": {"assumptions": "Lightweight, validated"}
        }
    },
    {
        "name": "Enterprise Strategist",
        "business_case": {
            "uuid": "55555555-5555-5555-5555-555555555555",
            "tenant_id": "tenant-enterprise",
            "user_id": "user-strategist",
        "created_at": "2025-07-13T12:00:00+00:00",
        "updated_at": "2025-07-13T12:00:00+00:00",
            "title": "Expand service uptime to 99.95%",
            "description": "Governance and reliability focus"
        },
        "initiative": {
            "uuid": "66666666-6666-6666-6666-666666666666",
            "tenant_id": "tenant-enterprise",
            "user_id": "user-strategist",
        "created_at": "2025-07-13T12:00:00+00:00",
        "updated_at": "2025-07-13T12:00:00+00:00",
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
    with patch("services.product_discovery_service.api.httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("services.product_discovery_service.api.emit_creation_event") as mock_emit_event:
        for entity, payload in [
            ("business_case", archetype["business_case"]),
            ("initiative", archetype["initiative"]),
            ("kpi", {**archetype["kpi"], "metric": archetype["kpi"].get("metric", "Default Metric"), "target_value": archetype["kpi"].get("target_value", 1.0)}),
            ("business_model_canvas", archetype["canvas"])
        ]:
            filtered_payload = filter_payload(payload, ENTITY_FIELDS[entity])
            payload_for_post = serialize_payload(filtered_payload)
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = payload_for_post
            import json
            mock_response.content = json.dumps(payload_for_post).encode()
            mock_response.headers = {"content-type": "application/json"}
            mock_post.return_value = mock_response
            endpoint = {
                "business_case": "/business-cases",
                "initiative": "/initiatives",
                "kpi": "/kpis",
                "business_model_canvas": "/business-model-canvas"
            }[entity]
            response = client.post(endpoint, json=payload_for_post)
            assert response.status_code == 201
            assert response.json() == payload_for_post
            mock_emit_event.assert_called_with(
                entity,
                payload_for_post["uuid"],
                payload_for_post["tenant_id"],
                payload_for_post["user_id"],
                None
            )
            mock_emit_event.reset_mock()

import pytest
from unittest.mock import patch, AsyncMock

role_payloads = [
    {
        "role": "Enterprise Architect",
        "business_case": {
            "uuid": "11111111-1111-1111-1111-111111111111",
            "tenant_id": "tenant-ea",
            "user_id": "user-ea",
        "created_at": "2025-07-13T12:00:00+00:00",
        "updated_at": "2025-07-13T12:00:00+00:00",
            "title": "Enable cross-region failover",
            "description": "Architect for multi-region redundancy"
        },
        "initiative": {
            "uuid": "22222222-2222-2222-2222-222222222222",
            "tenant_id": "tenant-ea",
            "user_id": "user-ea",
        "created_at": "2025-07-13T12:00:00+00:00",
        "updated_at": "2025-07-13T12:00:00+00:00",
            "business_case_id": "11111111-1111-1111-1111-111111111111",
            "name": "Design multi-zone cluster",
            "description": "Cluster design for failover"
        },
        "kpi": {
            "uuid": "33333333-3333-3333-3333-333333333333",
            "tenant_id": "tenant-ea",
            "user_id": "user-ea",
        "created_at": "2025-07-13T12:00:00+00:00",
        "updated_at": "2025-07-13T12:00:00+00:00",
            "initiative_id": "33333333-3333-3333-3333-333333333333",
            "metric": "Uptime compliance",
            "target_value": 99.95
        },
        "canvas": {
            "uuid": "44444444-4444-4444-4444-444444444444",
            "tenant_id": "tenant-ea",
            "user_id": "user-ea",
        "created_at": "2025-07-13T12:00:00+00:00",
        "updated_at": "2025-07-13T12:00:00+00:00",
            "canvas_data": {"redundancy": "multi-zone", "partners": "strategic"}
        }
    },
    {
        "role": "Solution Architect",
        "business_case": {
            "uuid": "55555555-5555-5555-5555-555555555555",
            "tenant_id": "tenant-sa",
            "user_id": "user-sa",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "title": "Accelerate partner integration",
            "description": "Speed up integration with partners"
        },
        "initiative": {
            "uuid": "66666666-6666-6666-6666-666666666666",
            "tenant_id": "tenant-sa",
            "user_id": "user-sa",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "business_case_id": "55555555-5555-5555-5555-555555555555",
            "name": "Launch GraphQL orchestration layer",
            "description": "Orchestration for API integration"
        },
        "kpi": {
            "uuid": "77777777-7777-7777-7777-777777777777",
            "tenant_id": "tenant-sa",
            "user_id": "user-sa",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "initiative_id": "66666666-6666-6666-6666-666666666666",
            "metric": "Time-to-integrate",
            "target_value": 5.0
        },
        "canvas": {
            "uuid": "88888888-8888-8888-8888-888888888888",
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
            "uuid": "99999999-9999-9999-9999-999999999999",
            "tenant_id": "tenant-ta",
            "user_id": "user-ta",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "title": "Reduce cold start latency",
            "description": "Optimize container startup"
        },
        "initiative": {
            "uuid": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "tenant_id": "tenant-ta",
            "user_id": "user-ta",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "business_case_id": "99999999-9999-9999-9999-999999999999",
            "name": "Refactor container networking",
            "description": "Improve networking for startup"
        },
        "kpi": {
            "uuid": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "tenant_id": "tenant-ta",
            "user_id": "user-ta",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "initiative_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "metric": "Startup latency",
            "target_value": 600.0
        },
        "canvas": {
            "uuid": "cccccccc-cccc-cccc-cccc-cccccccccccc",
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
            "uuid": "dddddddd-dddd-dddd-dddd-dddddddddddd",
            "tenant_id": "tenant-ba",
            "user_id": "user-ba",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "title": "Validate market entry assumptions",
            "description": "Market entry validation"
        },
        "initiative": {
            "uuid": "eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee",
            "tenant_id": "tenant-ba",
            "user_id": "user-ba",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "business_case_id": "dddddddd-dddd-dddd-dddd-dddddddddddd",
            "name": "Survey early adopters",
            "description": "Survey for validation"
        },
        "kpi": {
            "uuid": "ffffffff-ffff-ffff-ffff-ffffffffffff",
            "tenant_id": "tenant-ba",
            "user_id": "user-ba",
            "created_at": "2025-07-13T12:00:00Z",
            "updated_at": "2025-07-13T12:00:00Z",
            "initiative_id": "eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee",
            "metric": "Assumptions validated",
            "target_value": 5.0
        },
        "canvas": {
            "uuid": "00000000-0000-0000-0000-000000000000",
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
    import copy
    from services.product_discovery_service.schemas import BusinessCase, Initiative, KPI, BusinessModelCanvas
    from datetime import datetime, timezone
    from uuid import UUID
    with patch("services.product_discovery_service.api.httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("services.product_discovery_service.api.emit_creation_event") as mock_emit_event:
        # Build each payload using Pydantic models and timezone-aware datetimes
        business_case = BusinessCase(
            **{k: v for k, v in role_data["business_case"].items() if k not in ["created_at", "updated_at", "uuid"]},
            uuid=str(role_data["business_case"].get("uuid", UUID(int=0))),
            created_at=datetime.fromisoformat(str(role_data["business_case"].get("created_at"))).astimezone(timezone.utc),
            updated_at=datetime.fromisoformat(str(role_data["business_case"].get("updated_at"))).astimezone(timezone.utc)
        ).model_dump()
        initiative = Initiative(
            **{k: v for k, v in role_data["initiative"].items() if k not in ["created_at", "updated_at", "uuid", "business_case_id"]},
            uuid=str(role_data["initiative"].get("uuid", UUID(int=0))),
            created_at=datetime.fromisoformat(str(role_data["initiative"].get("created_at"))).astimezone(timezone.utc),
            updated_at=datetime.fromisoformat(str(role_data["initiative"].get("updated_at"))).astimezone(timezone.utc),
            business_case_id=str(role_data["initiative"].get("business_case_id", UUID(int=0)))
        ).model_dump()
        kpi = KPI(
            **{k: v for k, v in role_data["kpi"].items() if k not in ["created_at", "updated_at", "uuid", "initiative_id"]},
            uuid=str(role_data["kpi"].get("uuid", UUID(int=0))),
            created_at=datetime.fromisoformat(str(role_data["kpi"].get("created_at"))).astimezone(timezone.utc),
            updated_at=datetime.fromisoformat(str(role_data["kpi"].get("updated_at"))).astimezone(timezone.utc),
            initiative_id=str(role_data["kpi"].get("initiative_id", UUID(int=0)))
        ).model_dump()
        business_model_canvas = BusinessModelCanvas(
            **{k: v for k, v in role_data["canvas"].items() if k not in ["created_at", "updated_at", "uuid"]},
            uuid=str(role_data["canvas"].get("uuid", UUID(int=0))),
            created_at=datetime.fromisoformat(str(role_data["canvas"].get("created_at"))).astimezone(timezone.utc),
            updated_at=datetime.fromisoformat(str(role_data["canvas"].get("updated_at"))).astimezone(timezone.utc)
        ).model_dump()
        entity_payloads = [
            ("business_case", business_case),
            ("initiative", initiative),
            ("kpi", kpi),
            ("business_model_canvas", business_model_canvas)
        ]
        for entity, payload in entity_payloads:
            jsonable_payload = to_jsonable(payload)
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = jsonable_payload
            import json
            mock_response.content = json.dumps(jsonable_payload).encode()
            mock_response.headers = {"content-type": "application/json"}
            mock_post.return_value = mock_response
            endpoint = {
                "business_case": "/business-cases",
                "initiative": "/initiatives",
                "kpi": "/kpis",
                "business_model_canvas": "/business-model-canvas"
            }[entity]
            response = client.post(endpoint, json=jsonable_payload)
            assert response.status_code == 201
            assert response.json() == jsonable_payload
            mock_emit_event.assert_called_with(
                entity,
                jsonable_payload["uuid"],
                jsonable_payload["tenant_id"],
                jsonable_payload["user_id"],
                None
            )
            mock_emit_event.reset_mock()

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from services.product_discovery_service.api import router

@pytest.fixture
def client():
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)

@pytest.mark.api_proxy
def test_trace_id_propagation(client):
    from services.product_discovery_service.schemas import BusinessCase
    from datetime import datetime, timezone
    trace_id = "test-trace-id-123"
    payload_obj = BusinessCase(
        uuid="123e4567-e89b-12d3-a456-426614174000",
        tenant_id="tenant-trace",
        user_id="user-trace",
        title="Trace propagation",
        description="Test trace_id propagation",
        created_at=datetime.fromisoformat("2025-07-13T12:00:00+00:00").astimezone(timezone.utc),
        updated_at=datetime.fromisoformat("2025-07-13T12:00:00+00:00").astimezone(timezone.utc)
    )
    payload_for_post = to_jsonable(payload_obj.model_dump())
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = payload_for_post
    import json
    mock_response.content = json.dumps(payload_for_post).encode()
    mock_response.headers = {"content-type": "application/json"}
    def check_headers(*args, **kwargs):
        assert kwargs["headers"].get("trace_id") == trace_id
        return mock_response
    with patch("services.product_discovery_service.api.httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("services.product_discovery_service.api.emit_creation_event") as mock_emit_event:
        mock_post.side_effect = check_headers
        response = client.post("/business-cases", json=payload_for_post, headers={"trace_id": trace_id})
        assert response.status_code == 201
        assert response.json() == payload_for_post
        mock_emit_event.assert_called_once()

@pytest.mark.api_proxy
def test_redis_failure_simulation(client, caplog):
    from services.product_discovery_service.schemas import BusinessCase
    from datetime import datetime, timezone
    payload_obj = BusinessCase(
        uuid="abcdefab-cdef-abcd-efab-cdefabcdefab",
        tenant_id="tenant-redis",
        user_id="user-redis",
        title="Redis failure",
        description="Test Redis failure handling",
        created_at=datetime.fromisoformat("2025-07-13T12:00:00+00:00").astimezone(timezone.utc),
        updated_at=datetime.fromisoformat("2025-07-13T12:00:00+00:00").astimezone(timezone.utc)
    )
    payload_for_post = to_jsonable(payload_obj.model_dump())
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = payload_for_post
    import json
    mock_response.content = json.dumps(payload_for_post).encode()
    mock_response.headers = {"content-type": "application/json"}
    with patch("services.product_discovery_service.api.httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("services.product_discovery_service.api.emit_creation_event", side_effect=ConnectionError("Redis down")) as mock_emit_event:
        mock_post.return_value = mock_response
        response = client.post("/business-cases", json=payload_for_post)
        assert response.status_code == 201
        assert response.json() == payload_for_post
        # Check that Redis error was logged (caplog fixture)
        assert any("Redis down" in record.message for record in caplog.records)

# Ensure all test functions are prefixed with test_ and marked for CI
# To run: pytest product_discovery_service/test_api.py -m api_proxy
