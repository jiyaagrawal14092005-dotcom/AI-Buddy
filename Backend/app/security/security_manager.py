import os

from app.security.authentication import AuthenticationManager
from app.security.authorization import AuthorizationManager
from app.security.permissions import PermissionManager
from app.security.approval import approval_manager
from app.security.identity import IdentityManager
from app.security.user_context import UserContext
from app.security.data_isolation import DataIsolationManager
from app.security.token_manager import TokenManager
from app.security.oauth_manager import OAuthManager
from app.security.encryption import EncryptionManager
from app.security.secrets_manager import SecretsManager
from app.security.session_manager import SessionManager
from app.security.rate_limiter import RateLimiter
from app.security.input_validator import InputValidator
from app.security.tool_guard import ToolGuard
from app.security.prompt_guard import PromptGuard
from app.security.action_policy import ActionPolicy
from app.security.audit_log import AuditLogger
from app.security.security_monitor import SecurityMonitor
from app.security.key_rotation import KeyRotationManager
from app.security.security_config import SecurityConfig


class SecurityManager:
    """
    Central security controller for AI Buddy.

    SecurityManager coordinates the complete security layer:

    Authentication
        ↓
    Identity
        ↓
    User Context
        ↓
    Input Validation
        ↓
    Rate Limiting
        ↓
    Prompt Guard
        ↓
    Tool Guard
        ↓
    Action Policy
        ↓
    Permission / Approval
        ↓
    Execution
        ↓
    Audit Log
        ↓
    Security Monitoring
    """

    def __init__(
        self,
        encryption_secret: str | None = None
    ):
        # =========================================================
        # SECURITY CONFIGURATION
        # =========================================================

        self.config = SecurityConfig()

        if encryption_secret is None:
            encryption_secret = os.getenv(
                "AI_BUDDY_ENCRYPTION_SECRET"
            )

        if not encryption_secret:
            if self.config.is_production():
                raise ValueError(
                    "AI_BUDDY_ENCRYPTION_SECRET must be configured "
                    "in production."
                )

            encryption_secret = (
                "ai-buddy-development-key"
            )

        # =========================================================
        # AUTHENTICATION
        # =========================================================

        self.authentication = AuthenticationManager()

        # =========================================================
        # AUTHORIZATION
        # =========================================================

        self.authorization = AuthorizationManager()

        # =========================================================
        # PERMISSIONS
        # =========================================================

        self.permissions = PermissionManager()

        # =========================================================
        # APPROVAL
        # =========================================================

        # Use the shared approval manager so Brain,
        # SecurityManager and APIs use the same store.

        self.approval = approval_manager

        # =========================================================
        # IDENTITY
        # =========================================================

        self.identity = IdentityManager()

        # =========================================================
        # USER CONTEXT
        # =========================================================

        self.user_context = UserContext()

        # =========================================================
        # DATA ISOLATION
        # =========================================================

        self.data_isolation = DataIsolationManager()

        # =========================================================
        # TOKEN SECURITY
        # =========================================================

        self.token_manager = TokenManager()

        # =========================================================
        # OAUTH SECURITY
        # =========================================================

        self.oauth_manager = OAuthManager()

        # =========================================================
        # ENCRYPTION
        # =========================================================

        self.encryption = EncryptionManager(
            encryption_secret
        )

        # =========================================================
        # SECRETS
        # =========================================================

        self.secrets = SecretsManager()

        # =========================================================
        # SESSION MANAGEMENT
        # =========================================================

        self.sessions = SessionManager(
            session_timeout_minutes=(
                self.config.session_timeout_minutes
            )
        )

        # =========================================================
        # RATE LIMITING
        # =========================================================

        self.rate_limiter = RateLimiter(
            max_requests=self.config.max_requests,
            window_seconds=(
                self.config.rate_limit_window_seconds
            )
        )

        # =========================================================
        # INPUT VALIDATION
        # =========================================================

        self.input_validator = InputValidator(
            max_length=self.config.max_input_length
        )

        # =========================================================
        # TOOL SECURITY
        # =========================================================

        self.tool_guard = ToolGuard()

        # =========================================================
        # PROMPT SECURITY
        # =========================================================

        self.prompt_guard = PromptGuard()

        # =========================================================
        # ACTION POLICY
        # =========================================================

        self.action_policy = ActionPolicy()

        # =========================================================
        # AUDIT LOG
        # =========================================================

        self.audit_log = AuditLogger()

        # =========================================================
        # SECURITY MONITOR
        # =========================================================

        self.security_monitor = SecurityMonitor()

        # =========================================================
        # KEY ROTATION
        # =========================================================

        self.key_rotation = KeyRotationManager()

    # =============================================================
    # USER ID / USERNAME HELPERS
    # =============================================================

    def _normalize_user_id(
        self,
        user_id: str
    ) -> str:
        """
        Validate and normalize a user ID.
        """

        result = (
            self.input_validator.validate_user_id(
                user_id
            )
        )

        if not result["valid"]:
            raise ValueError(
                result["message"]
            )

        return str(user_id).strip()

    def _get_username(
        self,
        user_id: str
    ) -> str:
        """
        Resolve username from identity or current user context.
        """

        user_id = str(user_id).strip()

        identity_result = (
            self.identity.get_identity(
                user_id
            )
        )

        if (
            identity_result.get("success")
            and identity_result.get("identity")
        ):
            identity = identity_result["identity"]

            username = identity.get(
                "username"
            )

            if username:
                return str(username)

        context = (
            self.user_context.get_user()
        )

        if context.get("success"):
            current_user = context.get(
                "user"
            )

            if current_user:
                if str(
                    current_user.get("user_id")
                ) == user_id:

                    username = current_user.get(
                        "username"
                    )

                    if username:
                        return str(username)

        return user_id

    # =============================================================
    # COMPLETE REQUEST SECURITY PIPELINE
    # =============================================================

    def validate_request(
        self,
        user_id: str,
        prompt: str
    ) -> dict:
        """
        Validate an incoming AI Buddy request.

        Pipeline:

        User ID
            ↓
        Input Validation
            ↓
        Rate Limit
            ↓
        Prompt Guard
        """

        # ---------------------------------------------------------
        # USER ID
        # ---------------------------------------------------------

        user_result = (
            self.input_validator.validate_user_id(
                user_id
            )
        )

        if not user_result["valid"]:

            self._record_security_event(
                user_id=str(user_id),
                event="user_validation_failed",
                details=user_result.get(
                    "message",
                    ""
                ),
                severity="medium"
            )

            return {
                "allowed": False,
                "stage": "user_validation",
                "message": user_result["message"]
            }

        normalized_user_id = str(
            user_id
        ).strip()

        # ---------------------------------------------------------
        # INPUT VALIDATION
        # ---------------------------------------------------------

        if self.config.enable_input_validator:

            prompt_result = (
                self.input_validator.validate_text(
                    prompt
                )
            )

            if not prompt_result["valid"]:

                self._record_security_event(
                    user_id=normalized_user_id,
                    event="input_validation_failed",
                    details=prompt_result.get(
                        "message",
                        ""
                    ),
                    severity="medium"
                )

                return {
                    "allowed": False,
                    "stage": "input_validation",
                    "message": prompt_result["message"]
                }

        else:

            prompt_result = {
                "valid": True,
                "sanitized": prompt
            }

        # ---------------------------------------------------------
        # RATE LIMIT
        # ---------------------------------------------------------

        if self.config.enable_rate_limiter:

            rate_result = (
                self.rate_limiter.allow_request(
                    normalized_user_id
                )
            )

            if not rate_result["allowed"]:

                self._record_security_event(
                    user_id=normalized_user_id,
                    event="rate_limit_exceeded",
                    details=rate_result.get(
                        "message",
                        "Rate limit exceeded."
                    ),
                    severity="high"
                )

                return {
                    "allowed": False,
                    "stage": "rate_limit",
                    "message": rate_result.get(
                        "message",
                        "Rate limit exceeded."
                    ),
                    "remaining_requests": 0,
                    "retry_after_seconds": rate_result.get(
                        "retry_after_seconds"
                    )
                }

        else:

            rate_result = {
                "allowed": True,
                "remaining": None
            }

        # ---------------------------------------------------------
        # PROMPT GUARD
        # ---------------------------------------------------------

        if self.config.enable_prompt_guard:

            prompt_guard_result = (
                self.prompt_guard.check_prompt(
                    prompt_result["sanitized"]
                )
            )

            if not prompt_guard_result["allowed"]:

                self._record_security_event(
                    user_id=normalized_user_id,
                    event="prompt_blocked",
                    details=prompt_guard_result.get(
                        "message",
                        "Prompt blocked."
                    ),
                    severity="high"
                )

                return {
                    "allowed": False,
                    "stage": "prompt_guard",
                    "message": prompt_guard_result.get(
                        "message",
                        "Prompt blocked."
                    )
                }

        # ---------------------------------------------------------
        # SECURITY SUCCESS
        # ---------------------------------------------------------

        self._record_security_event(
            user_id=normalized_user_id,
            event="request_security_passed",
            details=(
                "Request passed input, rate-limit "
                "and prompt security checks."
            ),
            severity="low"
        )

        return {
            "allowed": True,
            "user_id": normalized_user_id,
            "prompt": prompt_result["sanitized"],
            "remaining_requests": (
                rate_result.get("remaining")
            ),
            "message": (
                "Request passed security checks."
            )
        }

    # =============================================================
    # TOOL ACCESS SECURITY
    # =============================================================

    def check_tool_access(
        self,
        user_id: str,
        tool_name: str,
        permission_granted: bool = False,
        approval_granted: bool = False,
        action: str | None = None
    ) -> dict:
        """
        Check whether a user can access a tool.
        """

        user_id = str(user_id).strip()

        if self.config.enable_tool_guard:

            result = (
                self.tool_guard.check_tool(
                    tool_name=tool_name,
                    user_id=user_id,
                    permission_granted=(
                        permission_granted
                    ),
                    approval_granted=(
                        approval_granted
                    ),
                    action=action
                )
            )

        else:

            result = {
                "allowed": True,
                "message": (
                    "Tool guard is disabled."
                )
            }

        if not result["allowed"]:

            self._record_security_event(
                user_id=user_id,
                event="tool_access_denied",
                details=result.get(
                    "message",
                    "Tool access denied."
                ),
                severity="medium"
            )

        else:

            self._record_security_event(
                user_id=user_id,
                event="tool_access_allowed",
                details=(
                    f"Tool '{tool_name}' access allowed."
                ),
                severity="low"
            )

        # IMPORTANT:
        # Preserve the approval requirement returned by
        # ToolGuard. Older code looked only for
        # "approval_required", while ToolGuard uses
        # "requires_approval".
        result["requires_approval"] = result.get(
            "requires_approval",
            result.get(
                "approval_required",
                False
            )
        )

        return result

    # =============================================================
    # ACTION ACCESS SECURITY
    # =============================================================

    def check_action_access(
        self,
        user_id: str,
        action: str,
        permission_granted: bool = False,
        approval_granted: bool = False
    ) -> dict:
        """
        Check whether a specific action is allowed.
        """

        user_id = str(user_id).strip()

        if self.config.enable_action_policy:

            result = (
                self.action_policy.is_allowed(
                    action=action,
                    permission_granted=(
                        permission_granted
                    ),
                    approval_granted=(
                        approval_granted
                    )
                )
            )

        else:

            result = {
                "allowed": True,
                "message": (
                    "Action policy is disabled."
                )
            }

        if not result["allowed"]:

            self._record_security_event(
                user_id=user_id,
                event="action_denied",
                details=result.get(
                    "message",
                    "Action denied."
                ),
                severity="medium"
            )

        else:

            self._record_security_event(
                user_id=user_id,
                event="action_allowed",
                details=(
                    f"Action '{action}' allowed."
                ),
                severity="low"
            )

        # IMPORTANT:
        # Preserve the approval requirement returned by
        # ActionPolicy as well.
        result["requires_approval"] = result.get(
            "requires_approval",
            result.get(
                "approval_required",
                False
            )
        )

        return result

    # =============================================================
    # COMBINED TOOL + ACTION CHECK
    # =============================================================

    def authorize_execution(
        self,
        user_id: str,
        tool_name: str,
        action: str,
        permission_granted: bool = False,
        approval_granted: bool = False
    ) -> dict:
        """
        Perform both tool and action authorization.
        """

        user_id = str(user_id).strip()

        tool_result = (
            self.check_tool_access(
                user_id=user_id,
                tool_name=tool_name,
                permission_granted=(
                    permission_granted
                ),
                approval_granted=(
                    approval_granted
                ),
                action=action
            )
        )

        if not tool_result["allowed"]:

            return {
                "allowed": False,
                "stage": "tool_guard",
                "tool": tool_name,
                "action": action,
                "requires_approval": tool_result.get(
                    "requires_approval",
                    False
                ),
                "message": tool_result.get(
                    "message",
                    "Tool access denied."
                )
            }

        action_result = (
            self.check_action_access(
                user_id=user_id,
                action=action,
                permission_granted=(
                    permission_granted
                ),
                approval_granted=(
                    approval_granted
                )
            )
        )

        if not action_result["allowed"]:

            return {
                "allowed": False,
                "stage": "action_policy",
                "tool": tool_name,
                "action": action,
                "requires_approval": action_result.get(
                    "requires_approval",
                    False
                ),
                "message": action_result.get(
                    "message",
                    "Action denied."
                )
            }

        return {
            "allowed": True,
            "tool": tool_name,
            "action": action,
            "permission_granted": (
                permission_granted
            ),
            "approval_granted": (
                approval_granted
            ),
            "message": (
                "Tool and action authorization passed."
            )
        }

    # =============================================================
    # APPROVAL POLICY
    # =============================================================

    def requires_approval(
        self,
        action_type: str
    ) -> bool:

        return self.config.requires_approval(
            action_type
        )

    def create_approval_request(
        self,
        username: str,
        action: str,
        details: dict | None = None
    ) -> dict:
        """
        Create an approval request using the shared
        ApprovalManager instance.
        """

        result = (
            self.approval.create_request(
                username=username,
                action=action,
                details=details
            )
        )

        if result.get("success"):

            self._record_security_event(
                user_id=str(username),
                event="approval_created",
                details=(
                    f"Approval created for '{action}'."
                ),
                severity="medium"
            )

        return result

    def approve_action(
        self,
        approval_id: str
    ) -> dict:

        result = (
            self.approval.approve(
                approval_id
            )
        )

        if result.get("success"):

            self._record_security_event(
                user_id="system",
                event="approval_granted",
                details=(
                    f"Approval '{approval_id}' granted."
                ),
                severity="medium"
            )

        return result

    def reject_action(
        self,
        approval_id: str
    ) -> dict:

        result = (
            self.approval.reject(
                approval_id
            )
        )

        if result.get("success"):

            self._record_security_event(
                user_id="system",
                event="approval_rejected",
                details=(
                    f"Approval '{approval_id}' rejected."
                ),
                severity="medium"
            )

        return result

    def get_approval_request(
        self,
        approval_id: str
    ) -> dict:

        return self.approval.get_request(
            approval_id
        )

    def get_pending_approvals(
        self
    ) -> list:

        return self.approval.get_pending_requests()

    def get_all_approvals(
        self
    ) -> list:

        return self.approval.get_all_requests()

    def consume_approval(
        self,
        approval_id: str
    ) -> dict:

        return self.approval.consume(
            approval_id
        )

    # =============================================================
    # PERMISSION HELPERS
    # =============================================================

    def grant_permission(
        self,
        username: str,
        permission: str
    ) -> dict:

        return self.permissions.grant_permission(
            username=username,
            permission=permission
        )

    def revoke_permission(
        self,
        username: str,
        permission: str
    ) -> dict:

        return self.permissions.revoke_permission(
            username=username,
            permission=permission
        )

    def has_permission(
        self,
        username: str,
        permission: str
    ) -> bool:

        return self.permissions.has_permission(
            username=username,
            permission=permission
        )

    def get_permissions(
        self,
        username: str
    ) -> list:

        return self.permissions.get_permissions(
            username=username
        )

    def check_permission(
        self,
        user_id: str,
        permission: str
    ) -> dict:
        """
        Check whether a user has a specific permission.
        """

        try:

            user_id = str(user_id)

            granted = self.permissions.has_permission(
                username=user_id,
                permission=permission
            )

            return {
                "allowed": granted,
                "granted": granted,
                "user_id": user_id,
                "permission": permission,
                "message": (
                    "Permission granted."
                    if granted
                    else "Permission not granted."
                )
            }

        except Exception as error:

            return {
                "allowed": False,
                "granted": False,
                "user_id": str(user_id),
                "permission": permission,
                "message": f"Permission check failed: {error}"
            }

    # =============================================================
    # USER CONTEXT
    # =============================================================

    def set_user_context(
        self,
        user_id: str,
        username: str
    ) -> dict:

        return self.user_context.set_user(
            user_id,
            username
        )

    def get_user_context(
        self
    ) -> dict:

        return self.user_context.get_user()

    def clear_user_context(
        self
    ) -> dict:

        return self.user_context.clear()

    # =============================================================
    # SESSION MANAGEMENT
    # =============================================================

    def create_user_session(
        self,
        user_id: str
    ) -> dict:

        return self.sessions.create_session(
            user_id
        )

    def validate_user_session(
        self,
        session_id: str,
        user_id: str
    ) -> bool:

        return self.sessions.validate_session(
            session_id,
            user_id
        )

    def revoke_user_session(
        self,
        session_id: str
    ) -> dict:

        return self.sessions.revoke_session(
            session_id
        )

    def revoke_all_user_sessions(
        self,
        user_id: str
    ) -> dict:

        return self.sessions.revoke_user_sessions(
            user_id
        )

    # =============================================================
    # ENCRYPTION
    # =============================================================

    def encrypt_data(
        self,
        data: str
    ) -> dict:

        return self.encryption.encrypt(
            data
        )

    def decrypt_data(
        self,
        encrypted_data: str
    ) -> dict:

        return self.encryption.decrypt(
            encrypted_data
        )

    # =============================================================
    # AUDIT LOG
    # =============================================================

    def record_audit_log(
        self,
        username: str,
        action: str,
        status: str,
        details: dict | None = None
    ) -> dict:

        if not self.config.enable_audit_log:

            return {
                "success": True,
                "recorded": False,
                "message": (
                    "Audit logging is disabled."
                )
            }

        try:

            return self.audit_log.log(
                username=username,
                action=action,
                status=status,
                details=details
            )

        except Exception as error:

            return {
                "success": False,
                "recorded": False,
                "message": (
                    f"Audit logging failed: {error}"
                )
            }

    def get_audit_logs(
        self,
        username: str | None = None
    ) -> list:

        if username is None:
            return self.audit_log.get_all()

        return self.audit_log.get_by_user(
            username
        )

    # =============================================================
    # SECURITY EVENT
    # =============================================================

    def record_security_event(
        self,
        user_id: str,
        event: str,
        details: str = "",
        severity: str = "medium"
    ) -> dict:

        return self._record_security_event(
            user_id=user_id,
            event=event,
            details=details,
            severity=severity
        )

    def _record_security_event(
        self,
        user_id: str,
        event: str,
        details: str = "",
        severity: str = "medium"
    ) -> dict:
        """
        Security monitoring must never crash the
        main AI Buddy pipeline.
        """

        if not self.config.enable_security_monitor:

            return {
                "success": True,
                "recorded": False,
                "message": (
                    "Security monitoring is disabled."
                )
            }

        try:

            return self.security_monitor.record_event(
                str(user_id),
                event,
                details=details,
                severity=severity
            )

        except Exception as error:

            return {
                "success": False,
                "recorded": False,
                "message": (
                    f"Security event recording failed: {error}"
                )
            }

    # =============================================================
    # SECURITY STATUS
    # =============================================================

    def get_security_status(
        self,
        user_id: str
    ) -> dict:
        """
        Return security monitoring status for a user.
        """

        try:

            status = (
                self.security_monitor.get_security_status(
                    str(user_id)
                )
            )

        except Exception as error:

            status = {
                "success": False,
                "message": (
                    f"Could not retrieve security status: {error}"
                )
            }

        status["config"] = {
            "prompt_guard": (
                self.config.enable_prompt_guard
            ),
            "tool_guard": (
                self.config.enable_tool_guard
            ),
            "action_policy": (
                self.config.enable_action_policy
            ),
            "audit_log": (
                self.config.enable_audit_log
            ),
            "security_monitor": (
                self.config.enable_security_monitor
            ),
            "rate_limiter": (
                self.config.enable_rate_limiter
            ),
            "input_validator": (
                self.config.enable_input_validator
            ),
            "encryption": (
                self.config.enable_encryption
            ),
            "data_isolation": (
                self.config.enable_data_isolation
            ),
            "jarvis_privacy_gate": (
                self.config.enable_jarvis_privacy_gate
            )
        }

        return status

    # =============================================================
    # SECURITY COMPONENTS
    # =============================================================

    def get_security_components(
        self
    ) -> list:
        """
        Return the complete list of security components.
        """

        return [
            "authentication",
            "authorization",
            "permissions",
            "approval",
            "identity",
            "user_context",
            "data_isolation",
            "token_manager",
            "oauth_manager",
            "encryption",
            "secrets_manager",
            "session_manager",
            "rate_limiter",
            "input_validator",
            "tool_guard",
            "prompt_guard",
            "action_policy",
            "audit_log",
            "security_monitor",
            "key_rotation"
        ]

    # =============================================================
    # COMPONENT STATUS
    # =============================================================

    def get_components_status(
        self
    ) -> dict:
        """
        Return the initialization/enabled status of all
        SecurityManager components.

        This method is intentionally read-only.
        """

        return {
            "success": True,
            "components": {
                "authentication": {
                    "initialized": (
                        self.authentication is not None
                    ),
                    "enabled": True
                },

                "authorization": {
                    "initialized": (
                        self.authorization is not None
                    ),
                    "enabled": (
                        self.config.require_authorization
                    )
                },

                "permissions": {
                    "initialized": (
                        self.permissions is not None
                    ),
                    "enabled": True
                },

                "approval": {
                    "initialized": (
                        self.approval is not None
                    ),
                    "enabled": True,
                    "shared": (
                        self.approval is approval_manager
                    )
                },

                "identity": {
                    "initialized": (
                        self.identity is not None
                    ),
                    "enabled": True
                },

                "user_context": {
                    "initialized": (
                        self.user_context is not None
                    ),
                    "enabled": True
                },

                "data_isolation": {
                    "initialized": (
                        self.data_isolation is not None
                    ),
                    "enabled": (
                        self.config.enable_data_isolation
                    )
                },

                "token_manager": {
                    "initialized": (
                        self.token_manager is not None
                    ),
                    "enabled": (
                        self.config.enable_token_manager
                    )
                },

                "oauth_manager": {
                    "initialized": (
                        self.oauth_manager is not None
                    ),
                    "enabled": True
                },

                "encryption": {
                    "initialized": (
                        self.encryption is not None
                    ),
                    "enabled": (
                        self.config.enable_encryption
                    )
                },

                "secrets_manager": {
                    "initialized": (
                        self.secrets is not None
                    ),
                    "enabled": (
                        self.config.enable_secret_manager
                    )
                },

                "session_manager": {
                    "initialized": (
                        self.sessions is not None
                    ),
                    "enabled": True
                },

                "rate_limiter": {
                    "initialized": (
                        self.rate_limiter is not None
                    ),
                    "enabled": (
                        self.config.enable_rate_limiter
                    )
                },

                "input_validator": {
                    "initialized": (
                        self.input_validator is not None
                    ),
                    "enabled": (
                        self.config.enable_input_validator
                    )
                },

                "tool_guard": {
                    "initialized": (
                        self.tool_guard is not None
                    ),
                    "enabled": (
                        self.config.enable_tool_guard
                    )
                },

                "prompt_guard": {
                    "initialized": (
                        self.prompt_guard is not None
                    ),
                    "enabled": (
                        self.config.enable_prompt_guard
                    )
                },

                "action_policy": {
                    "initialized": (
                        self.action_policy is not None
                    ),
                    "enabled": (
                        self.config.enable_action_policy
                    )
                },

                "audit_log": {
                    "initialized": (
                        self.audit_log is not None
                    ),
                    "enabled": (
                        self.config.enable_audit_log
                    )
                },

                "security_monitor": {
                    "initialized": (
                        self.security_monitor is not None
                    ),
                    "enabled": (
                        self.config.enable_security_monitor
                    )
                },

                "key_rotation": {
                    "initialized": (
                        self.key_rotation is not None
                    ),
                    "enabled": True
                }
            },

            "component_count": len(
                self.get_security_components()
            )
        }

    # =============================================================
    # GENERAL STATUS
    # =============================================================

    def get_status(
        self
    ) -> dict:
        """
        Return the overall SecurityManager status.

        This is a lightweight health/status method and does
        not expose passwords, tokens, encryption keys or secrets.
        """

        component_status = (
            self.get_components_status()
        )

        enabled_components = 0
        initialized_components = 0

        for component in (
            component_status["components"].values()
        ):
            if component.get("enabled"):
                enabled_components += 1

            if component.get("initialized"):
                initialized_components += 1

        return {
            "success": True,
            "name": "security_manager",
            "app_name": self.config.app_name,
            "environment": self.config.environment,
            "enabled": True,
            "component_count": len(
                self.get_security_components()
            ),
            "initialized_components": (
                initialized_components
            ),
            "enabled_components": (
                enabled_components
            ),
            "approval_manager_shared": (
                self.approval is approval_manager
            ),
            "security_features": {
                "prompt_guard": (
                    self.config.enable_prompt_guard
                ),
                "tool_guard": (
                    self.config.enable_tool_guard
                ),
                "action_policy": (
                    self.config.enable_action_policy
                ),
                "audit_log": (
                    self.config.enable_audit_log
                ),
                "security_monitor": (
                    self.config.enable_security_monitor
                ),
                "rate_limiter": (
                    self.config.enable_rate_limiter
                ),
                "input_validator": (
                    self.config.enable_input_validator
                ),
                "encryption": (
                    self.config.enable_encryption
                ),
                "data_isolation": (
                    self.config.enable_data_isolation
                ),
                "secret_manager": (
                    self.config.enable_secret_manager
                ),
                "token_manager": (
                    self.config.enable_token_manager
                ),
                "jarvis_privacy_gate": (
                    self.config.enable_jarvis_privacy_gate
                )
            },
            "security_failure_behavior": {
                "block_on_failure": (
                    self.config.block_on_security_failure
                ),
                "log_events": (
                    self.config.log_security_events
                )
            }
        }

    # =============================================================
    # SECURITY SUMMARY
    # =============================================================

    def get_security_summary(
        self,
        user_id: str
    ) -> dict:
        """
        Return a security summary for a user.
        """

        status = self.get_security_status(
            user_id
        )

        return {
            "success": True,
            "app_name": self.config.app_name,
            "environment": self.config.environment,
            "user_id": str(user_id),

            "authentication_enabled": (
                self.config.require_authentication
            ),

            "authorization_enabled": (
                self.config.require_authorization
            ),

            "prompt_guard_enabled": (
                self.config.enable_prompt_guard
            ),

            "tool_guard_enabled": (
                self.config.enable_tool_guard
            ),

            "action_policy_enabled": (
                self.config.enable_action_policy
            ),

            "rate_limiter_enabled": (
                self.config.enable_rate_limiter
            ),

            "input_validator_enabled": (
                self.config.enable_input_validator
            ),

            "encryption_enabled": (
                self.config.enable_encryption
            ),

            "data_isolation_enabled": (
                self.config.enable_data_isolation
            ),

            "jarvis_privacy_gate_enabled": (
                self.config.enable_jarvis_privacy_gate
            ),

            "security_monitor_enabled": (
                self.config.enable_security_monitor
            ),

            "security_components": (
                len(
                    self.get_security_components()
                )
            ),

            "status": status
        }