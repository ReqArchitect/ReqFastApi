import logging
from typing import Dict, List, Optional, Set
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class Role(Enum):
    OWNER = "Owner"
    ADMIN = "Admin"
    EDITOR = "Editor"
    VIEWER = "Viewer"

class Permission(Enum):
    # Assessment permissions
    ASSESSMENT_CREATE = "assessment:create"
    ASSESSMENT_READ = "assessment:read"
    ASSESSMENT_UPDATE = "assessment:update"
    ASSESSMENT_DELETE = "assessment:delete"
    
    # Work Package permissions
    WORKPACKAGE_CREATE = "workpackage:create"
    WORKPACKAGE_READ = "workpackage:read"
    WORKPACKAGE_UPDATE = "workpackage:update"
    WORKPACKAGE_DELETE = "workpackage:delete"
    
    # Architecture Suite permissions
    ARCHITECTURE_SUITE_CREATE = "architecture_suite:create"
    ARCHITECTURE_SUITE_READ = "architecture_suite:read"
    ARCHITECTURE_SUITE_UPDATE = "architecture_suite:update"
    ARCHITECTURE_SUITE_DELETE = "architecture_suite:delete"
    
    # Capability permissions
    CAPABILITY_CREATE = "capability:create"
    CAPABILITY_READ = "capability:read"
    CAPABILITY_UPDATE = "capability:update"
    CAPABILITY_DELETE = "capability:delete"
    
    # Goal permissions
    GOAL_CREATE = "goal:create"
    GOAL_READ = "goal:read"
    GOAL_UPDATE = "goal:update"
    GOAL_DELETE = "goal:delete"
    
    # Business Function permissions
    BUSINESS_FUNCTION_CREATE = "business_function:create"
    BUSINESS_FUNCTION_READ = "business_function:read"
    BUSINESS_FUNCTION_UPDATE = "business_function:update"
    BUSINESS_FUNCTION_DELETE = "business_function:delete"
    
    # Business Process permissions
    BUSINESS_PROCESS_CREATE = "business_process:create"
    BUSINESS_PROCESS_READ = "business_process:read"
    BUSINESS_PROCESS_UPDATE = "business_process:update"
    BUSINESS_PROCESS_DELETE = "business_process:delete"
    
    # Business Role permissions
    BUSINESS_ROLE_CREATE = "business_role:create"
    BUSINESS_ROLE_READ = "business_role:read"
    BUSINESS_ROLE_UPDATE = "business_role:update"
    BUSINESS_ROLE_DELETE = "business_role:delete"
    
    # Constraint permissions
    CONSTRAINT_CREATE = "constraint:create"
    CONSTRAINT_READ = "constraint:read"
    CONSTRAINT_UPDATE = "constraint:update"
    CONSTRAINT_DELETE = "constraint:delete"
    
    # Driver permissions
    DRIVER_CREATE = "driver:create"
    DRIVER_READ = "driver:read"
    DRIVER_UPDATE = "driver:update"
    DRIVER_DELETE = "driver:delete"
    
    # Requirement permissions
    REQUIREMENT_CREATE = "requirement:create"
    REQUIREMENT_READ = "requirement:read"
    REQUIREMENT_UPDATE = "requirement:update"
    REQUIREMENT_DELETE = "requirement:delete"
    
    # Application Function permissions
    APPLICATION_FUNCTION_CREATE = "application_function:create"
    APPLICATION_FUNCTION_READ = "application_function:read"
    APPLICATION_FUNCTION_UPDATE = "application_function:update"
    APPLICATION_FUNCTION_DELETE = "application_function:delete"
    
    # Auth permissions
    AUTH_CREATE = "auth:create"
    AUTH_READ = "auth:read"
    AUTH_UPDATE = "auth:update"
    AUTH_DELETE = "auth:delete"
    
    # AI Modeling permissions
    AI_MODELING_CREATE = "ai_modeling:create"
    AI_MODELING_READ = "ai_modeling:read"
    AI_MODELING_UPDATE = "ai_modeling:update"
    AI_MODELING_DELETE = "ai_modeling:delete"
    
    # Usage permissions
    USAGE_CREATE = "usage:create"
    USAGE_READ = "usage:read"
    USAGE_UPDATE = "usage:update"
    USAGE_DELETE = "usage:delete"
    
    # Billing permissions
    BILLING_CREATE = "billing:create"
    BILLING_READ = "billing:read"
    BILLING_UPDATE = "billing:update"
    BILLING_DELETE = "billing:delete"
    
    # Invoice permissions
    INVOICE_CREATE = "invoice:create"
    INVOICE_READ = "invoice:read"
    INVOICE_UPDATE = "invoice:update"
    INVOICE_DELETE = "invoice:delete"
    
    # Orchestrator permissions
    ORCHESTRATOR_CREATE = "orchestrator:create"
    ORCHESTRATOR_READ = "orchestrator:read"
    ORCHESTRATOR_UPDATE = "orchestrator:update"
    ORCHESTRATOR_DELETE = "orchestrator:delete"
    
    # Onboarding permissions
    ONBOARDING_CREATE = "onboarding:create"
    ONBOARDING_READ = "onboarding:read"
    ONBOARDING_UPDATE = "onboarding:update"
    ONBOARDING_DELETE = "onboarding:delete"
    
    # Audit Log permissions
    AUDIT_LOG_CREATE = "audit_log:create"
    AUDIT_LOG_READ = "audit_log:read"
    AUDIT_LOG_UPDATE = "audit_log:update"
    AUDIT_LOG_DELETE = "audit_log:delete"

@dataclass
class RBACContext:
    user_id: str
    tenant_id: str
    role: Role
    permissions: Set[Permission]

class RBACValidator:
    """Non-intrusive RBAC validation without payload inspection"""
    
    def __init__(self):
        self._role_permissions = self._initialize_role_permissions()
    
    def _initialize_role_permissions(self) -> Dict[Role, Set[Permission]]:
        """Initialize role-based permission mappings"""
        return {
            Role.OWNER: {
                # Full access to all permissions
                Permission.ASSESSMENT_CREATE, Permission.ASSESSMENT_READ, Permission.ASSESSMENT_UPDATE, Permission.ASSESSMENT_DELETE,
                Permission.WORKPACKAGE_CREATE, Permission.WORKPACKAGE_READ, Permission.WORKPACKAGE_UPDATE, Permission.WORKPACKAGE_DELETE,
                Permission.ARCHITECTURE_SUITE_CREATE, Permission.ARCHITECTURE_SUITE_READ, Permission.ARCHITECTURE_SUITE_UPDATE, Permission.ARCHITECTURE_SUITE_DELETE,
                Permission.CAPABILITY_CREATE, Permission.CAPABILITY_READ, Permission.CAPABILITY_UPDATE, Permission.CAPABILITY_DELETE,
                Permission.GOAL_CREATE, Permission.GOAL_READ, Permission.GOAL_UPDATE, Permission.GOAL_DELETE,
                Permission.BUSINESS_FUNCTION_CREATE, Permission.BUSINESS_FUNCTION_READ, Permission.BUSINESS_FUNCTION_UPDATE, Permission.BUSINESS_FUNCTION_DELETE,
                Permission.BUSINESS_PROCESS_CREATE, Permission.BUSINESS_PROCESS_READ, Permission.BUSINESS_PROCESS_UPDATE, Permission.BUSINESS_PROCESS_DELETE,
                Permission.BUSINESS_ROLE_CREATE, Permission.BUSINESS_ROLE_READ, Permission.BUSINESS_ROLE_UPDATE, Permission.BUSINESS_ROLE_DELETE,
                Permission.CONSTRAINT_CREATE, Permission.CONSTRAINT_READ, Permission.CONSTRAINT_UPDATE, Permission.CONSTRAINT_DELETE,
                Permission.DRIVER_CREATE, Permission.DRIVER_READ, Permission.DRIVER_UPDATE, Permission.DRIVER_DELETE,
                Permission.REQUIREMENT_CREATE, Permission.REQUIREMENT_READ, Permission.REQUIREMENT_UPDATE, Permission.REQUIREMENT_DELETE,
                Permission.APPLICATION_FUNCTION_CREATE, Permission.APPLICATION_FUNCTION_READ, Permission.APPLICATION_FUNCTION_UPDATE, Permission.APPLICATION_FUNCTION_DELETE,
                Permission.AUTH_CREATE, Permission.AUTH_READ, Permission.AUTH_UPDATE, Permission.AUTH_DELETE,
                Permission.AI_MODELING_CREATE, Permission.AI_MODELING_READ, Permission.AI_MODELING_UPDATE, Permission.AI_MODELING_DELETE,
                Permission.USAGE_CREATE, Permission.USAGE_READ, Permission.USAGE_UPDATE, Permission.USAGE_DELETE,
                Permission.BILLING_CREATE, Permission.BILLING_READ, Permission.BILLING_UPDATE, Permission.BILLING_DELETE,
                Permission.INVOICE_CREATE, Permission.INVOICE_READ, Permission.INVOICE_UPDATE, Permission.INVOICE_DELETE,
                Permission.ORCHESTRATOR_CREATE, Permission.ORCHESTRATOR_READ, Permission.ORCHESTRATOR_UPDATE, Permission.ORCHESTRATOR_DELETE,
                Permission.ONBOARDING_CREATE, Permission.ONBOARDING_READ, Permission.ONBOARDING_UPDATE, Permission.ONBOARDING_DELETE,
                Permission.AUDIT_LOG_CREATE, Permission.AUDIT_LOG_READ, Permission.AUDIT_LOG_UPDATE, Permission.AUDIT_LOG_DELETE,
            },
            Role.ADMIN: {
                # Full access to all permissions (same as Owner)
                Permission.ASSESSMENT_CREATE, Permission.ASSESSMENT_READ, Permission.ASSESSMENT_UPDATE, Permission.ASSESSMENT_DELETE,
                Permission.WORKPACKAGE_CREATE, Permission.WORKPACKAGE_READ, Permission.WORKPACKAGE_UPDATE, Permission.WORKPACKAGE_DELETE,
                Permission.ARCHITECTURE_SUITE_CREATE, Permission.ARCHITECTURE_SUITE_READ, Permission.ARCHITECTURE_SUITE_UPDATE, Permission.ARCHITECTURE_SUITE_DELETE,
                Permission.CAPABILITY_CREATE, Permission.CAPABILITY_READ, Permission.CAPABILITY_UPDATE, Permission.CAPABILITY_DELETE,
                Permission.GOAL_CREATE, Permission.GOAL_READ, Permission.GOAL_UPDATE, Permission.GOAL_DELETE,
                Permission.BUSINESS_FUNCTION_CREATE, Permission.BUSINESS_FUNCTION_READ, Permission.BUSINESS_FUNCTION_UPDATE, Permission.BUSINESS_FUNCTION_DELETE,
                Permission.BUSINESS_PROCESS_CREATE, Permission.BUSINESS_PROCESS_READ, Permission.BUSINESS_PROCESS_UPDATE, Permission.BUSINESS_PROCESS_DELETE,
                Permission.BUSINESS_ROLE_CREATE, Permission.BUSINESS_ROLE_READ, Permission.BUSINESS_ROLE_UPDATE, Permission.BUSINESS_ROLE_DELETE,
                Permission.CONSTRAINT_CREATE, Permission.CONSTRAINT_READ, Permission.CONSTRAINT_UPDATE, Permission.CONSTRAINT_DELETE,
                Permission.DRIVER_CREATE, Permission.DRIVER_READ, Permission.DRIVER_UPDATE, Permission.DRIVER_DELETE,
                Permission.REQUIREMENT_CREATE, Permission.REQUIREMENT_READ, Permission.REQUIREMENT_UPDATE, Permission.REQUIREMENT_DELETE,
                Permission.APPLICATION_FUNCTION_CREATE, Permission.APPLICATION_FUNCTION_READ, Permission.APPLICATION_FUNCTION_UPDATE, Permission.APPLICATION_FUNCTION_DELETE,
                Permission.AUTH_CREATE, Permission.AUTH_READ, Permission.AUTH_UPDATE, Permission.AUTH_DELETE,
                Permission.AI_MODELING_CREATE, Permission.AI_MODELING_READ, Permission.AI_MODELING_UPDATE, Permission.AI_MODELING_DELETE,
                Permission.USAGE_CREATE, Permission.USAGE_READ, Permission.USAGE_UPDATE, Permission.USAGE_DELETE,
                Permission.BILLING_CREATE, Permission.BILLING_READ, Permission.BILLING_UPDATE, Permission.BILLING_DELETE,
                Permission.INVOICE_CREATE, Permission.INVOICE_READ, Permission.INVOICE_UPDATE, Permission.INVOICE_DELETE,
                Permission.ORCHESTRATOR_CREATE, Permission.ORCHESTRATOR_READ, Permission.ORCHESTRATOR_UPDATE, Permission.ORCHESTRATOR_DELETE,
                Permission.ONBOARDING_CREATE, Permission.ONBOARDING_READ, Permission.ONBOARDING_UPDATE, Permission.ONBOARDING_DELETE,
                Permission.AUDIT_LOG_CREATE, Permission.AUDIT_LOG_READ, Permission.AUDIT_LOG_UPDATE, Permission.AUDIT_LOG_DELETE,
            },
            Role.EDITOR: {
                # Create, read, update permissions (no delete)
                Permission.ASSESSMENT_CREATE, Permission.ASSESSMENT_READ, Permission.ASSESSMENT_UPDATE,
                Permission.WORKPACKAGE_CREATE, Permission.WORKPACKAGE_READ, Permission.WORKPACKAGE_UPDATE,
                Permission.ARCHITECTURE_SUITE_CREATE, Permission.ARCHITECTURE_SUITE_READ, Permission.ARCHITECTURE_SUITE_UPDATE,
                Permission.CAPABILITY_CREATE, Permission.CAPABILITY_READ, Permission.CAPABILITY_UPDATE,
                Permission.GOAL_CREATE, Permission.GOAL_READ, Permission.GOAL_UPDATE,
                Permission.BUSINESS_FUNCTION_CREATE, Permission.BUSINESS_FUNCTION_READ, Permission.BUSINESS_FUNCTION_UPDATE,
                Permission.BUSINESS_PROCESS_CREATE, Permission.BUSINESS_PROCESS_READ, Permission.BUSINESS_PROCESS_UPDATE,
                Permission.BUSINESS_ROLE_CREATE, Permission.BUSINESS_ROLE_READ, Permission.BUSINESS_ROLE_UPDATE,
                Permission.CONSTRAINT_CREATE, Permission.CONSTRAINT_READ, Permission.CONSTRAINT_UPDATE,
                Permission.DRIVER_CREATE, Permission.DRIVER_READ, Permission.DRIVER_UPDATE,
                Permission.REQUIREMENT_CREATE, Permission.REQUIREMENT_READ, Permission.REQUIREMENT_UPDATE,
                Permission.APPLICATION_FUNCTION_CREATE, Permission.APPLICATION_FUNCTION_READ, Permission.APPLICATION_FUNCTION_UPDATE,
                Permission.AUTH_CREATE, Permission.AUTH_READ, Permission.AUTH_UPDATE,
                Permission.AI_MODELING_CREATE, Permission.AI_MODELING_READ, Permission.AI_MODELING_UPDATE,
                Permission.USAGE_CREATE, Permission.USAGE_READ, Permission.USAGE_UPDATE,
                Permission.BILLING_CREATE, Permission.BILLING_READ, Permission.BILLING_UPDATE,
                Permission.INVOICE_CREATE, Permission.INVOICE_READ, Permission.INVOICE_UPDATE,
                Permission.ORCHESTRATOR_CREATE, Permission.ORCHESTRATOR_READ, Permission.ORCHESTRATOR_UPDATE,
                Permission.ONBOARDING_CREATE, Permission.ONBOARDING_READ, Permission.ONBOARDING_UPDATE,
                Permission.AUDIT_LOG_CREATE, Permission.AUDIT_LOG_READ, Permission.AUDIT_LOG_UPDATE,
            },
            Role.VIEWER: {
                # Read-only permissions
                Permission.ASSESSMENT_READ,
                Permission.WORKPACKAGE_READ,
                Permission.ARCHITECTURE_SUITE_READ,
                Permission.CAPABILITY_READ,
                Permission.GOAL_READ,
                Permission.BUSINESS_FUNCTION_READ,
                Permission.BUSINESS_PROCESS_READ,
                Permission.BUSINESS_ROLE_READ,
                Permission.CONSTRAINT_READ,
                Permission.DRIVER_READ,
                Permission.REQUIREMENT_READ,
                Permission.APPLICATION_FUNCTION_READ,
                Permission.AUTH_READ,
                Permission.AI_MODELING_READ,
                Permission.USAGE_READ,
                Permission.BILLING_READ,
                Permission.INVOICE_READ,
                Permission.ORCHESTRATOR_READ,
                Permission.ONBOARDING_READ,
                Permission.AUDIT_LOG_READ,
            }
        }
    
    def create_context(self, user_id: str, tenant_id: str, role: str) -> RBACContext:
        """Create RBAC context from user information"""
        try:
            role_enum = Role(role)
            permissions = self._role_permissions.get(role_enum, set())
            return RBACContext(
                user_id=user_id,
                tenant_id=tenant_id,
                role=role_enum,
                permissions=permissions
            )
        except ValueError:
            # Invalid role, return viewer permissions
            logger.warning(f"Invalid role '{role}' for user {user_id}, defaulting to Viewer")
            return RBACContext(
                user_id=user_id,
                tenant_id=tenant_id,
                role=Role.VIEWER,
                permissions=self._role_permissions[Role.VIEWER]
            )
    
    def has_permission(self, context: RBACContext, permission: Permission) -> bool:
        """Check if user has specific permission"""
        return permission in context.permissions
    
    def validate_request_permission(self, context: RBACContext, service: str, method: str) -> bool:
        """Validate if user has permission for the requested service and method"""
        # Map HTTP method to permission type
        method_permission_map = {
            "GET": "read",
            "POST": "create",
            "PUT": "update",
            "PATCH": "update",
            "DELETE": "delete"
        }
        
        permission_type = method_permission_map.get(method, "read")
        permission_name = f"{service}:{permission_type}"
        
        try:
            permission = Permission(permission_name)
            has_perm = self.has_permission(context, permission)
            
            if not has_perm:
                logger.warning(
                    f"Permission denied: user {context.user_id} (role: {context.role.value}) "
                    f"attempted {method} on {service} - required: {permission_name}"
                )
            
            return has_perm
            
        except ValueError:
            # Unknown permission, log and deny
            logger.warning(f"Unknown permission: {permission_name}")
            return False
    
    def log_access_attempt(self, context: RBACContext, service: str, method: str, path: str, allowed: bool):
        """Log access attempt for audit purposes"""
        log_data = {
            "user_id": context.user_id,
            "tenant_id": context.tenant_id,
            "role": context.role.value,
            "service": service,
            "method": method,
            "path": path,
            "allowed": allowed,
            "timestamp": "2024-01-15T10:30:00Z"  # Would be actual timestamp
        }
        
        if allowed:
            logger.info(f"Access granted: {log_data}")
        else:
            logger.warning(f"Access denied: {log_data}")

# Global RBAC validator instance
rbac_validator = RBACValidator() 