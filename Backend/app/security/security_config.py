import os


class SecurityConfig:
    """
    Central security configuration for AI Buddy.

    Values can be overridden through environment variables.
    """

    def __init__(self):
        # ---------------------------------------------------------
        # Application
        # ---------------------------------------------------------
        self.app_name = os.getenv(
            "APP_NAME",
            "AI Buddy"
        )

        self.environment = os.getenv(
            "APP_ENV",
            "development"
        ).lower()

        # ---------------------------------------------------------
        # Session Security
        # ---------------------------------------------------------
        self.session_timeout_minutes = self._get_int(
            "SESSION_TIMEOUT_MINUTES",
            60,
            minimum=1
        )

        self.max_sessions_per_user = self._get_int(
            "MAX_SESSIONS_PER_USER",
            5,
            minimum=1
        )

        # ---------------------------------------------------------
        # Rate Limiting
        # ---------------------------------------------------------
        self.max_requests = self._get_int(
            "MAX_REQUESTS_PER_WINDOW",
            10,
            minimum=1
        )

        self.rate_limit_window_seconds = self._get_int(
            "RATE_LIMIT_WINDOW_SECONDS",
            60,
            minimum=1
        )

        # ---------------------------------------------------------
        # Input Security
        # ---------------------------------------------------------
        self.max_input_length = self._get_int(
            "MAX_INPUT_LENGTH",
            2000,
            minimum=1
        )

        self.max_url_length = self._get_int(
            "MAX_URL_LENGTH",
            2048,
            minimum=100
        )

        # ---------------------------------------------------------
        # Approval Policy
        # ---------------------------------------------------------
        self.require_approval_for_email = self._get_bool(
            "REQUIRE_APPROVAL_EMAIL",
            True
        )

        self.require_approval_for_calendar = self._get_bool(
            "REQUIRE_APPROVAL_CALENDAR",
            True
        )

        self.require_approval_for_file = self._get_bool(
            "REQUIRE_APPROVAL_FILE",
            True
        )

        self.require_approval_for_browser = self._get_bool(
            "REQUIRE_APPROVAL_BROWSER",
            True
        )

        self.require_approval_for_shopping = self._get_bool(
            "REQUIRE_APPROVAL_SHOPPING",
            True
        )

        self.require_approval_for_booking = self._get_bool(
            "REQUIRE_APPROVAL_BOOKING",
            True
        )

        self.require_approval_for_social_post = self._get_bool(
            "REQUIRE_APPROVAL_SOCIAL_POST",
            True
        )

        # ---------------------------------------------------------
        # Security Modules
        # ---------------------------------------------------------
        self.enable_prompt_guard = self._get_bool(
            "ENABLE_PROMPT_GUARD",
            True
        )

        self.enable_tool_guard = self._get_bool(
            "ENABLE_TOOL_GUARD",
            True
        )

        self.enable_action_policy = self._get_bool(
            "ENABLE_ACTION_POLICY",
            True
        )

        self.enable_audit_log = self._get_bool(
            "ENABLE_AUDIT_LOG",
            True
        )

        self.enable_security_monitor = self._get_bool(
            "ENABLE_SECURITY_MONITOR",
            True
        )

        self.enable_rate_limiter = self._get_bool(
            "ENABLE_RATE_LIMITER",
            True
        )

        self.enable_input_validator = self._get_bool(
            "ENABLE_INPUT_VALIDATOR",
            True
        )

        # ---------------------------------------------------------
        # Privacy
        # ---------------------------------------------------------
        self.enable_data_isolation = self._get_bool(
            "ENABLE_DATA_ISOLATION",
            True
        )

        self.enable_encryption = self._get_bool(
            "ENABLE_ENCRYPTION",
            True
        )

        self.enable_secret_manager = self._get_bool(
            "ENABLE_SECRETS_MANAGER",
            True
        )

        self.enable_token_manager = self._get_bool(
            "ENABLE_TOKEN_MANAGER",
            True
        )

        # ---------------------------------------------------------
        # Jarvis / Voice Privacy
        # ---------------------------------------------------------
        self.enable_jarvis_privacy_gate = self._get_bool(
            "ENABLE_JARVIS_PRIVACY_GATE",
            True
        )

        self.discard_audio_without_wake_word = self._get_bool(
            "DISCARD_AUDIO_WITHOUT_WAKE_WORD",
            True
        )

        self.jarvis_audio_retention_seconds = self._get_int(
            "JARVIS_AUDIO_RETENTION_SECONDS",
            0,
            minimum=0
        )

        # ---------------------------------------------------------
        # Browser Security
        # ---------------------------------------------------------
        self.allow_http = self._get_bool(
            "ALLOW_HTTP",
            True
        )

        self.allow_https = self._get_bool(
            "ALLOW_HTTPS",
            True
        )

        self.allow_browser_file_upload = self._get_bool(
            "ALLOW_BROWSER_FILE_UPLOAD",
            False
        )

        self.allow_browser_download = self._get_bool(
            "ALLOW_BROWSER_DOWNLOAD",
            False
        )

        # ---------------------------------------------------------
        # Authentication / Authorization
        # ---------------------------------------------------------
        self.require_authentication = self._get_bool(
            "REQUIRE_AUTHENTICATION",
            True
        )

        self.require_authorization = self._get_bool(
            "REQUIRE_AUTHORIZATION",
            True
        )

        # ---------------------------------------------------------
        # Security behavior
        # ---------------------------------------------------------
        self.block_on_security_failure = self._get_bool(
            "BLOCK_ON_SECURITY_FAILURE",
            True
        )

        self.log_security_events = self._get_bool(
            "LOG_SECURITY_EVENTS",
            True
        )

    # =============================================================
    # Environment Helpers
    # =============================================================

    @staticmethod
    def _get_int(
        name: str,
        default: int,
        minimum: int = 0
    ) -> int:
        """
        Safely read an integer environment variable.
        """

        value = os.getenv(name)

        if value is None:
            return default

        try:
            parsed_value = int(value)
        except (TypeError, ValueError):
            return default

        if parsed_value < minimum:
            return default

        return parsed_value

    @staticmethod
    def _get_bool(
        name: str,
        default: bool
    ) -> bool:
        """
        Safely read a boolean environment variable.
        """

        value = os.getenv(name)

        if value is None:
            return default

        value = value.strip().lower()

        if value in {
            "1",
            "true",
            "yes",
            "on",
            "enabled"
        }:
            return True

        if value in {
            "0",
            "false",
            "no",
            "off",
            "disabled"
        }:
            return False

        return default

    # =============================================================
    # Configuration Output
    # =============================================================

    def get_config(self) -> dict:
        """
        Return the complete security configuration.

        Sensitive credentials/tokens are never stored here.
        """

        return {
            # Application
            "app_name": self.app_name,
            "environment": self.environment,

            # Session
            "session_timeout_minutes":
                self.session_timeout_minutes,
            "max_sessions_per_user":
                self.max_sessions_per_user,

            # Rate limiting
            "max_requests":
                self.max_requests,
            "rate_limit_window_seconds":
                self.rate_limit_window_seconds,

            # Input
            "max_input_length":
                self.max_input_length,
            "max_url_length":
                self.max_url_length,

            # Approval
            "require_approval_for_email":
                self.require_approval_for_email,
            "require_approval_for_calendar":
                self.require_approval_for_calendar,
            "require_approval_for_file":
                self.require_approval_for_file,
            "require_approval_for_browser":
                self.require_approval_for_browser,
            "require_approval_for_shopping":
                self.require_approval_for_shopping,
            "require_approval_for_booking":
                self.require_approval_for_booking,
            "require_approval_for_social_post":
                self.require_approval_for_social_post,

            # Security modules
            "enable_prompt_guard":
                self.enable_prompt_guard,
            "enable_tool_guard":
                self.enable_tool_guard,
            "enable_action_policy":
                self.enable_action_policy,
            "enable_audit_log":
                self.enable_audit_log,
            "enable_security_monitor":
                self.enable_security_monitor,
            "enable_rate_limiter":
                self.enable_rate_limiter,
            "enable_input_validator":
                self.enable_input_validator,

            # Privacy
            "enable_data_isolation":
                self.enable_data_isolation,
            "enable_encryption":
                self.enable_encryption,
            "enable_secret_manager":
                self.enable_secret_manager,
            "enable_token_manager":
                self.enable_token_manager,

            # Jarvis privacy
            "enable_jarvis_privacy_gate":
                self.enable_jarvis_privacy_gate,
            "discard_audio_without_wake_word":
                self.discard_audio_without_wake_word,
            "jarvis_audio_retention_seconds":
                self.jarvis_audio_retention_seconds,

            # Browser
            "allow_http":
                self.allow_http,
            "allow_https":
                self.allow_https,
            "allow_browser_file_upload":
                self.allow_browser_file_upload,
            "allow_browser_download":
                self.allow_browser_download,

            # Authentication
            "require_authentication":
                self.require_authentication,
            "require_authorization":
                self.require_authorization,

            # Security behavior
            "block_on_security_failure":
                self.block_on_security_failure,
            "log_security_events":
                self.log_security_events
        }

    # =============================================================
    # Environment Checks
    # =============================================================

    def is_production(self) -> bool:
        return self.environment == "production"

    def is_development(self) -> bool:
        return self.environment == "development"

    def is_testing(self) -> bool:
        return self.environment in {
            "test",
            "testing"
        }

    # =============================================================
    # Approval Helper
    # =============================================================

    def requires_approval(
        self,
        action_type: str
    ) -> bool:
        """
        Check whether a specific action requires approval.
        """

        action_type = action_type.strip().lower()

        approval_map = {
            "email":
                self.require_approval_for_email,

            "calendar":
                self.require_approval_for_calendar,

            "file":
                self.require_approval_for_file,

            "browser":
                self.require_approval_for_browser,

            "shopping":
                self.require_approval_for_shopping,

            "booking":
                self.require_approval_for_booking,

            "social_post":
                self.require_approval_for_social_post
        }

        return approval_map.get(
            action_type,
            False
        )

    # =============================================================
    # Security Feature Check
    # =============================================================

    def is_security_feature_enabled(
        self,
        feature_name: str
    ) -> bool:
        """
        Check whether a security feature is enabled.
        """

        feature_map = {
            "prompt_guard":
                self.enable_prompt_guard,

            "tool_guard":
                self.enable_tool_guard,

            "action_policy":
                self.enable_action_policy,

            "tool_guard":
                self.enable_tool_guard,

            "audit_log":
                self.enable_audit_log,

            "security_monitor":
                self.enable_security_monitor,

            "rate_limiter":
                self.enable_rate_limiter,

            "input_validator":
                self.enable_input_validator,

            "data_isolation":
                self.enable_data_isolation,

            "encryption":
                self.enable_encryption,

            "secret_manager":
                self.enable_secret_manager,

            "token_manager":
                self.enable_token_manager,

            "jarvis_privacy_gate":
                self.enable_jarvis_privacy_gate
        }

        return feature_map.get(
            feature_name.strip().lower(),
            False
        )