from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
import httpx
from .routing import resolve_service
from .middleware import AuthMiddleware, RateLimitMiddleware, LoggingMiddleware
import asyncio

middlewares = [
    Middleware(AuthMiddleware),
    Middleware(RateLimitMiddleware, limit_per_minute=10),
    Middleware(LoggingMiddleware),
]

app = FastAPI(middleware=middlewares)

@app.get("/health")
def health():
    return {"status": "gateway ok"}

@app.post("/proxy/{service}/{path:path}")
async def proxy(service: str, path: str, request: Request):
    # Role-based access control
    role = getattr(request.state, "role", None)
    if service == "usage" and role not in ("Owner", "Admin"):
        raise HTTPException(status_code=403, detail="Forbidden")
    # Resolve service URL
    base_url = resolve_service(f"/{service}")
    if not base_url:
        raise HTTPException(status_code=404, detail="Unknown service")
    url = f"{base_url}/{path}"
    # Prepare headers
    headers = dict(request.headers)
    headers["X-User-ID"] = getattr(request.state, "user_id", "")
    headers["X-Tenant-ID"] = getattr(request.state, "tenant_id", "")
    headers["X-Role"] = getattr(request.state, "role", "")
    # Forward request
    async with httpx.AsyncClient() as client:
        body = await request.body()
        resp = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            params=request.query_params,
            timeout=30.0
        )
    return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))
