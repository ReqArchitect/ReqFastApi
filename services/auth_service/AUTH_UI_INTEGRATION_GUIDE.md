# Auth Service UI Integration Guide

This guide describes how to integrate the ReqArchitect Auth Service with frontend applications for login, signup, onboarding, role selection, and session management.

## 1. Login Flow
- **Endpoint:** `POST /auth/login`
- **Request:**
  ```json
  { "email": "user@example.com", "password": "securePass123" }
  ```
- **Response:**
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
- **Frontend:** Store `token` in memory or secure storage. Use for all authenticated requests.

## 2. Signup Flow
- **Endpoint:** `POST /auth/signup`
- **Request:**
  ```json
  { "email": "newuser@example.com", "password": "securePass123", "name": "New User", "tenant_name": "Acme Corp" }
  ```
- **Response:**
  ```json
  {
    "token": "JWT-xyz",
    "expires_at": "2024-01-15T12:00:00Z",
    "user": { ... },
    "tenant_created": true
  }
  ```
- **Frontend:** Onboard user and optionally redirect to dashboard.

## 3. User Profile
- **Endpoint:** `GET /auth/user`
- **Headers:** `Authorization: Bearer <token>`
- **Response:**
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
- **Frontend:** Use for session display, role-based UI, and access control.

## 4. Logout
- **Endpoint:** `POST /auth/logout`
- **Headers:** `Authorization: Bearer <token>`
- **Response:**
  ```json
  { "message": "Logged out successfully", "timestamp": "2024-01-15T11:00:00Z" }
  ```
- **Frontend:** Remove token from storage and redirect to login.

## 5. Invite & Accept Invite
- **Invite:**
  - **Endpoint:** `POST /auth/invite` (Owner/Admin only)
  - **Request:**
    ```json
    { "email": "invitee@example.com", "role": "Editor", "message": "Welcome!" }
    ```
  - **Response:**
    ```json
    { "invite_id": "inv-789", "invite_token": "invite-token-xyz", "expires_at": "2024-01-22T10:00:00Z", "email": "invitee@example.com" }
    ```
- **Accept Invite:**
  - **Endpoint:** `POST /auth/accept-invite`
  - **Request:**
    ```json
    { "invite_token": "invite-token-xyz", "name": "Invited User", "password": "securePass123" }
    ```
  - **Response:**
    ```json
    { "token": "JWT-abc", "expires_at": "2024-01-22T12:00:00Z", "user": { ... } }
    ```

## 6. Role Selector
- **Endpoint:** `GET /auth/roles`
- **Response:**
  ```json
  [
    { "name": "Owner", "description": "Full access...", "capabilities": [ ... ], "permissions": [ ... ] },
    ...
  ]
  ```
- **Frontend:** Use for dropdowns and role-based UI.

## 7. Error Handling
- **Error Format:**
  ```json
  { "status_code": 400, "message": "Email already registered", "hint": "Use a different email", "field": "email" }
  ```
- **Frontend:** Display `message` and `hint` to user. Highlight `field` if present.

## 8. Guardrails
- No password hashes or sensitive claims are exposed
- Only default role Viewer is assigned at signup
- All signup/invite events are logged via Redis
- CORS is enabled for all auth endpoints
- Rate limiting is enforced on login/signup
- Existing JWT and RBAC logic is preserved

## 9. Security
- Always use HTTPS in production
- Never store JWT in localStorage if XSS is a risk
- Use short-lived tokens and refresh as needed

## 10. Example Flows
- See README and API_REFERENCE for more examples and details. 