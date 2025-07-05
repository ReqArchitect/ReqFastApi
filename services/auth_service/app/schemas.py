from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    user_id: str
    email: str
    role: str
    tenant_id: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: str
    password: str
    role: str
    tenant_id: str

class AuthToken(BaseModel):
    token: str
    issued_at: datetime
    expires_at: datetime
    user_id: str
    tenant_id: str
    role: str

    class Config:
        orm_mode = True
