

from fastapi import APIRouter, Request, Response, status, Depends
from .schemas import BusinessCase, Initiative, KPI, BusinessModelCanvas
from .eventing import emit_creation_event
import httpx
import os

router = APIRouter()

ARCHITECTURE_SUITE_URL = os.getenv("ARCHITECTURE_SUITE_URL", "http://architecture_suite:8004")

def get_redis_client():
    # TODO: Implement actual Redis client retrieval
    pass

def proxy_headers(request: Request):
    # Forward all headers, especially Authorization
    return {k: v for k, v in request.headers.items()}

@router.post("/business-cases", tags=["Proxy Endpoints"], summary="Delegated proxy to architecture_suite", openapi_extra={"x-service-role": "creator", "x-host-service": "architecture_suite"})
async def create_business_case(payload: BusinessCase, request: Request, redis_client=Depends(get_redis_client)):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{ARCHITECTURE_SUITE_URL}/business-cases", json=payload.dict(), headers=proxy_headers(request))
    if resp.status_code == 201:
        data = resp.json()
        emit_creation_event("business_case", data["uuid"], data["tenant_id"], data["user_id"], redis_client)
    return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get("content-type", "application/json"))

@router.post("/initiatives", tags=["Proxy Endpoints"], summary="Delegated proxy to architecture_suite", openapi_extra={"x-service-role": "creator", "x-host-service": "architecture_suite"})
async def create_initiative(payload: Initiative, request: Request, redis_client=Depends(get_redis_client)):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{ARCHITECTURE_SUITE_URL}/initiatives", json=payload.dict(), headers=proxy_headers(request))
    if resp.status_code == 201:
        data = resp.json()
        emit_creation_event("initiative", data["uuid"], data["tenant_id"], data["user_id"], redis_client)
    return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get("content-type", "application/json"))

@router.post("/kpis", tags=["Proxy Endpoints"], summary="Delegated proxy to architecture_suite", openapi_extra={"x-service-role": "creator", "x-host-service": "architecture_suite"})
async def create_kpi(payload: KPI, request: Request, redis_client=Depends(get_redis_client)):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{ARCHITECTURE_SUITE_URL}/kpis", json=payload.dict(), headers=proxy_headers(request))
    if resp.status_code == 201:
        data = resp.json()
        emit_creation_event("kpi", data["uuid"], data["tenant_id"], data["user_id"], redis_client)
    return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get("content-type", "application/json"))

@router.post("/business-model-canvas", tags=["Proxy Endpoints"], summary="Delegated proxy to architecture_suite", openapi_extra={"x-service-role": "creator", "x-host-service": "architecture_suite"})
async def create_business_model_canvas(payload: BusinessModelCanvas, request: Request, redis_client=Depends(get_redis_client)):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{ARCHITECTURE_SUITE_URL}/business-model-canvas", json=payload.dict(), headers=proxy_headers(request))
    if resp.status_code == 201:
        data = resp.json()
        emit_creation_event("business_model_canvas", data["uuid"], data["tenant_id"], data["user_id"], redis_client)
    return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get("content-type", "application/json"))

# Healthcheck endpoint for dashboard observability
@router.get("/architecture-suite-health", tags=["Health"], summary="Check architecture_suite health")
async def check_architecture_suite():
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{ARCHITECTURE_SUITE_URL}/health")
        return {
            "status": "healthy",
            "latency": res.elapsed.total_seconds()
        }
    except Exception as e:
        return {"status": "unreachable", "error": str(e)}
