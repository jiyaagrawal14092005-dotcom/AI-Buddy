import os


class SecurityConfig:

    def __init__(self):

        self.app_name = "AI Buddy"

        self.session_timeout_minutes = int(
            os.getenv(
                "SESSION_TIMEOUT_MINUTES",
                "60"
            )
        )

        self.max_requests = int(
            os.getenv(
                "MAX_REQUESTS_PER_WINDOW",
                "10"
            )
        )

        self.rate_limit_window_seconds = int(
            os.getenv(
                "RATE_LIMIT_WINDOW_SECONDS",
                "60"
            )
        )

        self.max_input_length = int(
            os.getenv(
                "MAX_INPUT_LENGTH",
                "2000"
            )
        )

        self.require_approval_for_email = True
        self.require_approval_for_calendar = True
        self.require_approval_for_file = True
        self.require_approval_for_browser = True

        self.enable_prompt_guard = True
        self.enable_tool_guard = True
        self.enable_audit_log = True
        self.enable_security_monitor = True

        self.environment = os.getenv(
            "APP_ENV",
            "development"
        )

    def get_config(self) -> dict:

        return {
            "app_name": self.app_name,
            "environment": self.environment,
            "session_timeout_minutes":
                self.session_timeout_minutes,
            "max_requests":
                self.max_requests,
            "rate_limit_window_seconds":
                self.rate_limit_window_seconds,
            "max_input_length":
                self.max_input_length,
            "require_approval_for_email":
                self.require_approval_for_email,
            "require_approval_for_calendar":
                self.require_approval_for_calendar,
            "require_approval_for_file":
                self.require_approval_for_file,
            "require_approval_for_browser":
                self.require_approval_for_browser,
            "enable_prompt_guard":
                self.enable_prompt_guard,
            "enable_tool_guard":
                self.enable_tool_guard,
            "enable_audit_log":
                self.enable_audit_log,
            "enable_security_monitor":
                self.enable_security_monitor
        }

    def is_production(self) -> bool:

        return self.environment.lower() == "production"

    def is_development(self) -> bool:

        return self.environment.lower() == "development"