from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Auth Service", version="0.1.0")

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://idp.example.com/oauth2/authorize",
    tokenUrl="https://idp.example.com/oauth2/token"
)

class UserInfo(BaseModel):
    sub: str
    email: str
    name: str
    roles: list
    tenant_id: Optional[str]

@app.get("/userinfo", response_model=UserInfo)
def get_userinfo(token: str = Depends(oauth2_scheme)):
    # Stub: decode JWT, fetch claims from IdP
    # In production, validate token and fetch user info from IdP
    return UserInfo(sub="user-123", email="user@example.com", name="Test User", roles=["manager"], tenant_id="tenant-1")
