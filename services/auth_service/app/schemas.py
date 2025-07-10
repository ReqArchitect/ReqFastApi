from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
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

# Frontend UI Integration Schemas

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=1, description="User password")

class LoginResponse(BaseModel):
    token: str = Field(..., description="JWT access token")
    expires_at: datetime = Field(..., description="Token expiration time")
    user: Dict[str, Any] = Field(..., description="User profile information")

class SignupRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (minimum 8 characters)")
    name: str = Field(..., min_length=1, description="User full name")
    tenant_name: Optional[str] = Field(None, description="Tenant name for new tenant creation")

class SignupResponse(BaseModel):
    token: str = Field(..., description="JWT access token")
    expires_at: datetime = Field(..., description="Token expiration time")
    user: Dict[str, Any] = Field(..., description="User profile information")
    tenant_created: bool = Field(..., description="Whether a new tenant was created")

class UserProfile(BaseModel):
    id: str = Field(..., description="User ID")
    name: str = Field(..., description="User full name")
    email: str = Field(..., description="User email address")
    tenant_id: str = Field(..., description="Tenant ID")
    role: str = Field(..., description="User role")
    permissions: List[str] = Field(..., description="User permissions")
    created_at: datetime = Field(..., description="User creation timestamp")

class InviteRequest(BaseModel):
    email: EmailStr = Field(..., description="Email address to invite")
    role: str = Field(..., description="Role to assign to invited user")
    message: Optional[str] = Field(None, description="Optional invitation message")

class InviteResponse(BaseModel):
    invite_id: str = Field(..., description="Invitation ID")
    invite_token: str = Field(..., description="Invitation token")
    expires_at: datetime = Field(..., description="Invitation expiration time")
    email: str = Field(..., description="Invited email address")

class AcceptInviteRequest(BaseModel):
    invite_token: str = Field(..., description="Invitation token")
    name: str = Field(..., min_length=1, description="User full name")
    password: str = Field(..., min_length=8, description="User password")

class AcceptInviteResponse(BaseModel):
    token: str = Field(..., description="JWT access token")
    expires_at: datetime = Field(..., description="Token expiration time")
    user: Dict[str, Any] = Field(..., description="User profile information")

class RoleInfo(BaseModel):
    name: str = Field(..., description="Role name")
    description: str = Field(..., description="Role description")
    capabilities: List[str] = Field(..., description="Role capabilities")
    permissions: List[str] = Field(..., description="Role permissions")

class ErrorResponse(BaseModel):
    status_code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Error message")
    hint: Optional[str] = Field(None, description="Helpful hint for resolution")
    field: Optional[str] = Field(None, description="Field that caused the error")

class LogoutResponse(BaseModel):
    message: str = Field(..., description="Logout confirmation message")
    timestamp: datetime = Field(..., description="Logout timestamp")
