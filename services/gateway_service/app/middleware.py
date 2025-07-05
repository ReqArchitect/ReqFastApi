import time
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from collections import defaultdict

SECRET_KEY = "REPLACE_WITH_REAL_SECRET"
ALGORITHM = "HS256"

# In-memory rate limit store (for demo)
rate_limit_store = defaultdict(list)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")
        token = auth_header.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user_id = payload["user_id"]
            request.state.tenant_id = payload["tenant_id"]
            request.state.role = payload["role"]
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
        response = await call_next(request)
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit_per_minute=10):
        super().__init__(app)
        self.limit_per_minute = limit_per_minute

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        user_id = getattr(request.state, "user_id", None)
        if path.startswith("/ai_modeling/generate") and user_id:
            now = time.time()
            window = 60
            timestamps = rate_limit_store[user_id]
            # Remove old timestamps
            rate_limit_store[user_id] = [t for t in timestamps if now - t < window]
            if len(rate_limit_store[user_id]) >= self.limit_per_minute:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            rate_limit_store[user_id].append(now)
        response = await call_next(request)
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        latency = (time.time() - start) * 1000
        print(f"{request.method} {request.url.path} {response.status_code} {latency:.2f}ms")
        return response
