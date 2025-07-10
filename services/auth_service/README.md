# Auth Service

This service provides authentication, RBAC, and session management for ReqArchitect tenants and users.

## Features
- JWT-based authentication
- Multi-tenant user management
- Role-based access control (Owner, Admin, Editor, Viewer)
- Secure password hashing
- Session-oriented endpoints for frontend UI integration
- Invitation and onboarding flows
- Redis audit event emission
- CORS support for frontend
- Rate limiting on login/signup

## API Endpoints

### Session-Oriented Endpoints

#### POST /auth/login
Authenticate user and return JWT and user context.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePass123"
}
```
**Response:**
```json
{
  "token": "JWT-xyz",
  "expires_at": "2024-01-15T12:00:00Z",
  "user": {
    "id": "123",
    "name": "Aniekan",
    "email": "user@example.com",
    "tenant_id": "reqarchitect",
    "role": "Admin"
  }
}
```

#### POST /auth/signup
Register a new user (default role: Viewer, new tenant if tenant_name provided).

**Request:**
```json
{
  "email": "newuser@example.com",
  "password": "securePass123",
  "name": "New User",
  "tenant_name": "Acme Corp"
}
```
**Response:**
```json
{
  "token": "JWT-xyz",
  "expires_at": "2024-01-15T12:00:00Z",
  "user": {
    "id": "456",
    "name": "New User",
    "email": "newuser@example.com",
    "tenant_id": "generated-tenant-id",
    "role": "Viewer"
  },
  "tenant_created": true
}
```

#### GET /auth/user
Get authenticated user profile.

**Headers:**
`Authorization: Bearer <token>`

**Response:**
```json
{
  "id": "123",
  "name": "Aniekan",
  "email": "user@example.com",
  "tenant_id": "reqarchitect",
  "role": "Admin",
  "permissions": ["can_admin"],
  "created_at": "2024-01-15T10:00:00Z"
}
```

#### POST /auth/logout
Logout (frontend-only, invalidates token in backend memory).

**Headers:**
`Authorization: Bearer <token>`

**Response:**
```json
{
  "message": "Logged out successfully",
  "timestamp": "2024-01-15T11:00:00Z"
}
```

#### POST /auth/invite
Invite a new user to the tenant (Owner/Admin only).

**Headers:**
`Authorization: Bearer <token>`

**Request:**
```json
{
  "email": "invitee@example.com",
  "role": "Editor",
  "message": "Welcome to the team!"
}
```
**Response:**
```json
{
  "invite_id": "inv-789",
  "invite_token": "invite-token-xyz",
  "expires_at": "2024-01-22T10:00:00Z",
  "email": "invitee@example.com"
}
```

#### POST /auth/accept-invite
Accept an invitation and register as a user.

**Request:**
```json
{
  "invite_token": "invite-token-xyz",
  "name": "Invited User",
  "password": "securePass123"
}
```
**Response:**
```json
{
  "token": "JWT-abc",
  "expires_at": "2024-01-22T12:00:00Z",
  "user": {
    "id": "999",
    "name": "Invited User",
    "email": "invitee@example.com",
    "tenant_id": "reqarchitect",
    "role": "Editor"
  }
}
```

#### GET /auth/roles
Get available roles and their capabilities for UI role selector.

**Response:**
```json
[
  {
    "name": "Owner",
    "description": "Full access to all tenant resources and settings.",
    "capabilities": ["Manage users", "Configure tenant", "Access all data"],
    "permissions": ["owner:all"]
  },
  {
    "name": "Admin",
    "description": "Manage users and resources, but not tenant settings.",
    "capabilities": ["Manage users", "Access most data"],
    "permissions": ["admin:manage", "admin:view"]
  },
  {
    "name": "Editor",
    "description": "Edit and create resources, but cannot manage users.",
    "capabilities": ["Edit data", "Create resources"],
    "permissions": ["editor:edit", "editor:create"]
  },
  {
    "name": "Viewer",
    "description": "Read-only access to resources.",
    "capabilities": ["View data"],
    "permissions": ["viewer:view"]
  }
]
```

### Error Response Format
```json
{
  "status_code": 400,
  "message": "Email already registered",
  "hint": "Use a different email",
  "field": "email"
}
```

## Guardrails
- No password hashes or sensitive claims are exposed
- Only default role Viewer is assigned at signup
- All signup/invite events are logged via Redis
- CORS is enabled for all auth endpoints
- Rate limiting is enforced on login/signup
- Existing JWT and RBAC logic is preserved

## Running the Service

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## Environment Variables
- `SECRET_KEY`: JWT secret
- `REDIS_URL`: Redis connection string
- `DATABASE_URL`: SQLAlchemy DB URL

## License
ReqArchitect Platform 