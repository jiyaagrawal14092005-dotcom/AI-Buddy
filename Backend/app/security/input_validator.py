import re


class InputValidator:

    def __init__(
        self,
        max_length: int = 2000
    ):
        self.max_length = max_length

    def validate_text(
        self,
        text: str
    ) -> dict:

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

        text = text.strip()

        if not text:
            return {
                "valid": False,
                "message": "Input cannot be empty."
            }

        if len(text) > self.max_length:
            return {
                "valid": False,
                "message": "Input exceeds maximum length."
            }

        return {
            "valid": True,
            "sanitized": text,
            "message": "Input is valid."
        }

    def sanitize_text(
        self,
        text: str
    ) -> str:

        if not isinstance(text, str):
            return ""

        text = text.strip()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text

    def validate_user_id(
        self,
        user_id: str
    ) -> dict:

        if not user_id:
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

    def validate_email(
        self,
        email: str
    ) -> dict:

        if not email:
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

        pattern = (
            r"^[A-Za-z0-9._%+-]+@"
            r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
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

    def validate_length(
        self,
        text: str,
        min_length: int = 1,
        max_length: int | None = None
    ) -> dict:

        if not isinstance(text, str):
            return {
                "valid": False,
                "message": "Input must be text."
            }

        max_allowed = (
            max_length
            if max_length is not None
            else self.max_length
        )

        length = len(text.strip())

        if length < min_length:
            return {
                "valid": False,
                "message": "Input is too short."
            }

        if length > max_allowed:
            return {
                "valid": False,
                "message": "Input is too long."
            }

        return {
            "valid": True,
            "length": length,
            "message": "Input length is valid."
        }