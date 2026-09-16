import re
from urllib.parse import urlparse


class InputValidator:
    """
    Validates and sanitizes user-controlled input
    before it reaches AI Buddy's agent, tools, or integrations.
    """

    def __init__(
        self,
        max_length: int = 2000
    ):
        if not isinstance(max_length, int) or max_length < 1:
            raise ValueError(
                "max_length must be a positive integer."
            )

        self.max_length = max_length

    # =============================================================
    # TEXT VALIDATION
    # =============================================================

    def validate_text(
        self,
        text: str
    ) -> dict:
        """
        Validate and sanitize general text input.
        """

        if text is None:
            return {
                "valid": False,
                "message": "Input is required."
            }

        if not isinstance(text, str):
            return {
                "valid": False,
                "message": "Input must be text."
            }

        sanitized = self.sanitize_text(text)

        if not sanitized:
            return {
                "valid": False,
                "message": "Input cannot be empty."
            }

        if len(sanitized) > self.max_length:
            return {
                "valid": False,
                "message": "Input exceeds maximum length."
            }

        return {
            "valid": True,
            "sanitized": sanitized,
            "length": len(sanitized),
            "message": "Input is valid."
        }

    # =============================================================
    # TEXT SANITIZATION
    # =============================================================

    def sanitize_text(
        self,
        text: str
    ) -> str:
        """
        Normalize whitespace and remove control characters.

        This does not attempt to rewrite the user's meaning.
        """

        if not isinstance(text, str):
            return ""

        # Remove null bytes and other ASCII control characters
        # while preserving normal whitespace.
        text = re.sub(
            r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]",
            "",
            text
        )

        text = text.strip()

        # Normalize repeated whitespace.
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text

    # =============================================================
    # USER ID VALIDATION
    # =============================================================

    def validate_user_id(
        self,
        user_id: str
    ) -> dict:
        """
        Validate a user identifier.

        Supported characters:
        letters, numbers, underscore and hyphen.
        """

        if user_id is None:
            return {
                "valid": False,
                "message": "User ID is required."
            }

        if not isinstance(user_id, str):
            return {
                "valid": False,
                "message": "User ID must be text."
            }

        user_id = user_id.strip()

        if not user_id:
            return {
                "valid": False,
                "message": "User ID cannot be empty."
            }

        if not re.fullmatch(
            r"[A-Za-z0-9_-]{3,100}",
            user_id
        ):
            return {
                "valid": False,
                "message": "Invalid user ID format."
            }

        return {
            "valid": True,
            "sanitized": user_id,
            "message": "User ID is valid."
        }

    # =============================================================
    # USERNAME VALIDATION
    # =============================================================

    def validate_username(
        self,
        username: str
    ) -> dict:
        """
        Validate a username used by authentication,
        authorization, permissions, and approval modules.
        """

        if username is None:
            return {
                "valid": False,
                "message": "Username is required."
            }

        if not isinstance(username, str):
            return {
                "valid": False,
                "message": "Username must be text."
            }

        username = username.strip()

        if not username:
            return {
                "valid": False,
                "message": "Username cannot be empty."
            }

        if not re.fullmatch(
            r"[A-Za-z0-9_.-]{3,100}",
            username
        ):
            return {
                "valid": False,
                "message": "Invalid username format."
            }

        return {
            "valid": True,
            "sanitized": username,
            "message": "Username is valid."
        }

    # =============================================================
    # EMAIL VALIDATION
    # =============================================================

    def validate_email(
        self,
        email: str
    ) -> dict:
        """
        Validate an email address.
        """

        if email is None:
            return {
                "valid": False,
                "message": "Email is required."
            }

        if not isinstance(email, str):
            return {
                "valid": False,
                "message": "Email must be text."
            }

        email = email.strip()

        if not email:
            return {
                "valid": False,
                "message": "Email cannot be empty."
            }

        if len(email) > 254:
            return {
                "valid": False,
                "message": "Email address is too long."
            }

        pattern = (
            r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
            r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}"
            r"[A-Za-z0-9])?"
            r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}"
            r"[A-Za-z0-9])?)+$"
        )

        if not re.fullmatch(
            pattern,
            email
        ):
            return {
                "valid": False,
                "message": "Invalid email format."
            }

        return {
            "valid": True,
            "sanitized": email,
            "message": "Email is valid."
        }

    # =============================================================
    # URL VALIDATION
    # =============================================================

    def validate_url(
        self,
        url: str,
        allowed_schemes: tuple[str, ...] = (
            "http",
            "https"
        )
    ) -> dict:
        """
        Validate a URL before browser/network tools use it.
        """

        if url is None:
            return {
                "valid": False,
                "message": "URL is required."
            }

        if not isinstance(url, str):
            return {
                "valid": False,
                "message": "URL must be text."
            }

        url = url.strip()

        if not url:
            return {
                "valid": False,
                "message": "URL cannot be empty."
            }

        if len(url) > 2048:
            return {
                "valid": False,
                "message": "URL exceeds maximum length."
            }

        try:
            parsed = urlparse(url)
        except ValueError:
            return {
                "valid": False,
                "message": "Invalid URL."
            }

        if parsed.scheme.lower() not in allowed_schemes:
            return {
                "valid": False,
                "message": (
                    "URL scheme is not allowed."
                )
            }

        if not parsed.netloc:
            return {
                "valid": False,
                "message": "URL host is required."
            }

        if any(
            character.isspace()
            for character in parsed.netloc
        ):
            return {
                "valid": False,
                "message": "URL host contains invalid whitespace."
            }

        return {
            "valid": True,
            "sanitized": url,
            "scheme": parsed.scheme.lower(),
            "host": parsed.hostname,
            "message": "URL is valid."
        }

    # =============================================================
    # LENGTH VALIDATION
    # =============================================================

    def validate_length(
        self,
        text: str,
        min_length: int = 1,
        max_length: int | None = None
    ) -> dict:
        """
        Validate text length.
        """

        if not isinstance(text, str):
            return {
                "valid": False,
                "message": "Input must be text."
            }

        if not isinstance(min_length, int):
            return {
                "valid": False,
                "message": "Minimum length must be an integer."
            }

        if min_length < 0:
            return {
                "valid": False,
                "message": (
                    "Minimum length cannot be negative."
                )
            }

        if max_length is None:
            max_allowed = self.max_length
        else:
            if not isinstance(max_length, int):
                return {
                    "valid": False,
                    "message": (
                        "Maximum length must be an integer."
                    )
                }

            if max_length < min_length:
                return {
                    "valid": False,
                    "message": (
                        "Maximum length cannot be less "
                        "than minimum length."
                    )
                }

            max_allowed = max_length

        sanitized = self.sanitize_text(text)
        length = len(sanitized)

        if length < min_length:
            return {
                "valid": False,
                "message": "Input is too short.",
                "length": length
            }

        if length > max_allowed:
            return {
                "valid": False,
                "message": "Input is too long.",
                "length": length
            }

        return {
            "valid": True,
            "length": length,
            "message": "Input length is valid."
        }

    # =============================================================
    # INTEGER VALIDATION
    # =============================================================

    def validate_integer(
        self,
        value,
        minimum: int | None = None,
        maximum: int | None = None
    ) -> dict:
        """
        Validate integer values used by timers,
        scheduling, pagination, and similar features.
        """

        if isinstance(value, bool) or not isinstance(value, int):
            return {
                "valid": False,
                "message": "Value must be an integer."
            }

        if minimum is not None and value < minimum:
            return {
                "valid": False,
                "message": "Value is below the minimum allowed."
            }

        if maximum is not None and value > maximum:
            return {
                "valid": False,
                "message": "Value exceeds the maximum allowed."
            }

        return {
            "valid": True,
            "value": value,
            "message": "Integer is valid."
        }

    # =============================================================
    # SAFE FIELD VALIDATION
    # =============================================================

    def validate_field(
        self,
        value,
        field_name: str,
        required: bool = True,
        max_length: int | None = None
    ) -> dict:
        """
        Generic validation helper for tool parameters.
        """

        if not isinstance(field_name, str) or not field_name.strip():
            return {
                "valid": False,
                "message": "Field name is required."
            }

        field_name = field_name.strip()

        if value is None:

            if required:
                return {
                    "valid": False,
                    "message": (
                        f"{field_name} is required."
                    )
                }

            return {
                "valid": True,
                "value": None,
                "message": (
                    f"{field_name} is optional."
                )
            }

        if isinstance(value, str):

            sanitized = self.sanitize_text(value)

            if not sanitized and required:
                return {
                    "valid": False,
                    "message": (
                        f"{field_name} cannot be empty."
                    )
                }

            if max_length is not None and len(sanitized) > max_length:
                return {
                    "valid": False,
                    "message": (
                        f"{field_name} exceeds maximum length."
                    )
                }

            return {
                "valid": True,
                "value": sanitized,
                "message": (
                    f"{field_name} is valid."
                )
            }

        return {
            "valid": True,
            "value": value,
            "message": (
                f"{field_name} is valid."
            )
        }

    # =============================================================
    # STATUS
    # =============================================================

    def get_status(self) -> dict:
        """
        Return validator configuration.
        """

        return {
            "name": "input_validator",
            "available": True,
            "max_length": self.max_length
        }