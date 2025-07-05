from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from typing import List

# Example OIDC config (to be replaced with real values)
OIDC_ISSUER = "https://example.com/oidc"
OIDC_AUDIENCE = "architecture_suite"
OIDC_JWKS = {}  # JWKS cache or fetch logic

async def get_current_user(request: Request, scopes: List[str] = []):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    token = auth_header.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, OIDC_JWKS, audience=OIDC_AUDIENCE, issuer=OIDC_ISSUER)
        # Check scopes/claims here
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
