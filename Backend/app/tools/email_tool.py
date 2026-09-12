import re

from app.tools.base_tool import BaseTool


class EmailTool(BaseTool):

    def __init__(self):

        super().__init__(
            name="email",
            description=(
                "Prepare an email action with a recipient, "
                "subject, and message."
            )
        )

    # =================================
    # VALIDATE EMAIL
    # =================================

    def _validate_email(
        self,
        email: str
    ) -> str:

        if not isinstance(
            email,
            str
        ):
            raise TypeError(
                "Email address must be a string."
            )

        email = email.strip()

        if not email:
            raise ValueError(
                "Email address cannot be empty."
            )

        pattern = (
            r"^[A-Za-z0-9._%+-]+@"
            r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        )

        if not re.match(
            pattern,
            email
        ):
            raise ValueError(
                "Invalid email address."
            )

        return email

    # =================================
    # VALIDATE TEXT
    # =================================

    def _validate_text(
        self,
        value: str,
        field_name: str
    ) -> str:

        if not isinstance(
            value,
            str
        ):
            raise TypeError(
                f"{field_name} must be a string."
            )

        value = value.strip()

        if not value:
            raise ValueError(
                f"{field_name} cannot be empty."
            )

        return value

    # =================================
    # PREPARE EMAIL
    # =================================

    def prepare_email(
        self,
        recipient: str,
        subject: str,
        message: str
    ) -> dict:

        recipient = self._validate_email(
            recipient
        )

        subject = self._validate_text(
            subject,
            "Subject"
        )

        message = self._validate_text(
            message,
            "Message"
        )

        return {
            "recipient": recipient,
            "subject": subject,
            "message": message
        }

    # =================================
    # EXECUTE EMAIL ACTION
    # =================================

    def execute(
        self,
        parameters: dict | None = None
    ) -> dict:

        if parameters is None:
            parameters = {}

        if not isinstance(
            parameters,
            dict
        ):
            return {
                "success": False,
                "message": (
                    "Email parameters must be a dictionary."
                )
            }

        recipient = parameters.get(
            "recipient",
            parameters.get(
                "email",
                ""
            )
        )

        subject = parameters.get(
            "subject",
            ""
        )

        message = parameters.get(
            "message",
            ""
        )

        try:

            email_data = self.prepare_email(
                recipient,
                subject,
                message
            )

        except (
            TypeError,
            ValueError
        ) as e:

            return {
                "success": False,
                "message": str(e)
            }

        return {
            "success": True,
            "status": "prepared",
            "email": email_data,
            "message": (
                "Email action prepared successfully."
            )
        }

    # =================================
    # TOOL AVAILABILITY
    # =================================

    def is_available(self) -> bool:

        return True