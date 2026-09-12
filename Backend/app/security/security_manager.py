from app.security.authentication import AuthenticationManager
from app.security.authorization import AuthorizationManager
from app.security.permissions import PermissionManager
from app.security.approval import ApprovalManager
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

    def __init__(
        self,
        encryption_secret: str = "ai-buddy-development-key"
    ):

        # Security configuration
        self.config = SecurityConfig()

        # Authentication and authorization
        self.authentication = AuthenticationManager()
        self.authorization = AuthorizationManager()
        self.permissions = PermissionManager()
        self.approval = ApprovalManager()

        # User identity and context
        self.identity = IdentityManager()
        self.user_context = UserContext()

        # Data and token security
        self.data_isolation = DataIsolationManager()
        self.token_manager = TokenManager()
        self.oauth_manager = OAuthManager()

        # Encryption and secrets
        self.encryption = EncryptionManager(
            encryption_secret
        )
        self.secrets = SecretsManager()

        # Session management
        self.sessions = SessionManager(
            session_timeout_minutes=
            self.config.session_timeout_minutes
        )

        # Rate limiting
        self.rate_limiter = RateLimiter(
            max_requests=self.config.max_requests,
            window_seconds=
            self.config.rate_limit_window_seconds
        )

        # Input validation
        self.input_validator = InputValidator(
            max_length=self.config.max_input_length
        )

        # AI and tool protection
        self.tool_guard = ToolGuard()
        self.prompt_guard = PromptGuard()
        self.action_policy = ActionPolicy()

        # Monitoring and auditing
        self.audit_log = AuditLogger()
        self.security_monitor = SecurityMonitor()

        # Security key management
        self.key_rotation = KeyRotationManager()

    # --------------------------------------------------
    # REQUEST SECURITY
    # --------------------------------------------------

    def validate_request(
        self,
        user_id: str,
        prompt: str
    ) -> dict:

        user_result = self.input_validator.validate_user_id(
            user_id
        )

        if not user_result["valid"]:
            return {
                "allowed": False,
                "stage": "user_validation",
                "message": user_result["message"]
            }

        prompt_result = self.input_validator.validate_text(
            prompt
        )

        if not prompt_result["valid"]:
            return {
                "allowed": False,
                "stage": "input_validation",
                "message": prompt_result["message"]
            }

        rate_result = self.rate_limiter.allow_request(
            user_id
        )

        if not rate_result["allowed"]:

            self.security_monitor.record_event(
                user_id,
                "rate_limit_exceeded",
                severity="high"
            )

            return {
                "allowed": False,
                "stage": "rate_limit",
                "message": rate_result["message"]
            }

        if self.config.enable_prompt_guard:

            prompt_guard_result = (
                self.prompt_guard.check_prompt(
                    prompt
                )
            )

            if not prompt_guard_result["allowed"]:

                self.security_monitor.record_event(
                    user_id,
                    "prompt_blocked",
                    details=prompt_guard_result["message"],
                    severity="high"
                )

                return {
                    "allowed": False,
                    "stage": "prompt_guard",
                    "message":
                        prompt_guard_result["message"]
                }

        return {
            "allowed": True,
            "user_id": user_id,
            "prompt":
                prompt_result["sanitized"],
            "remaining_requests":
                rate_result["remaining"],
            "message": "Request passed security checks."
        }

    # --------------------------------------------------
    # TOOL SECURITY
    # --------------------------------------------------

    def check_tool_access(
        self,
        user_id: str,
        tool_name: str,
        permission_granted: bool = False,
        approval_granted: bool = False
    ) -> dict:

        result = self.tool_guard.check_tool(
            tool_name=tool_name,
            user_id=user_id,
            permission_granted=permission_granted,
            approval_granted=approval_granted
        )

        if not result["allowed"]:

            self.security_monitor.record_event(
                user_id,
                "permission_denied",
                details=result["message"],
                severity="medium"
            )

        return result

    # --------------------------------------------------
    # ACTION POLICY SECURITY
    # --------------------------------------------------

    def check_action_access(
        self,
        user_id: str,
        action: str,
        permission_granted: bool = False,
        approval_granted: bool = False
    ) -> dict:

        result = self.action_policy.is_allowed(
            action=action,
            permission_granted=permission_granted,
            approval_granted=approval_granted
        )

        if not result["allowed"]:

            self.security_monitor.record_event(
                user_id,
                "action_denied",
                details=result["message"],
                severity="medium"
            )

        return result

    # --------------------------------------------------
    # USER CONTEXT
    # --------------------------------------------------

    def set_user_context(
        self,
        user_id: str,
        username: str
    ) -> dict:

        return self.user_context.set_user(
            user_id,
            username
        )

    def get_user_context(self) -> dict:

        return self.user_context.get_user()

    def clear_user_context(self) -> dict:

        return self.user_context.clear()

    # --------------------------------------------------
    # SESSION MANAGEMENT
    # --------------------------------------------------

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

    # --------------------------------------------------
    # ENCRYPTION
    # --------------------------------------------------

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

    # --------------------------------------------------
    # AUDIT LOG
    # --------------------------------------------------

    def record_audit_log(
        self,
        username: str,
        action: str,
        status: str,
        details: dict | None = None
    ) -> dict:

        return self.audit_log.log(
            username=username,
            action=action,
            status=status,
            details=details
        )

    def get_audit_logs(
        self,
        username: str | None = None
    ) -> list:

        if username is None:
            return self.audit_log.get_all()

        return self.audit_log.get_by_user(
            username
        )

    # --------------------------------------------------
    # SECURITY STATUS
    # --------------------------------------------------

    def get_security_status(
        self,
        user_id: str
    ) -> dict:

        status = self.security_monitor.get_security_status(
            user_id
        )

        status["config"] = {
            "prompt_guard":
                self.config.enable_prompt_guard,
            "tool_guard":
                self.config.enable_tool_guard,
            "audit_log":
                self.config.enable_audit_log,
            "security_monitor":
                self.config.enable_security_monitor
        }

        return status

    # --------------------------------------------------
    # SECURITY COMPONENTS
    # --------------------------------------------------

    def get_security_components(
        self
    ) -> list:

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