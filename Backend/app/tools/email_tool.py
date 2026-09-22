import re

from app.tools.base_tool import BaseTool
from app.integrations.email.gmail_service import GmailService


class EmailTool(BaseTool):

    def __init__(self):

        super().__init__(
            name="email",
            description=(
                "Send an email through the connected Gmail account "
                "using a recipient, subject, and message."
            )
        )

        self.gmail_service = GmailService()

    # =================================
    # VALIDATE USER ID
    # =================================

    def _validate_user_id(
        self,
        user_id
    ) -> int:

        if user_id is None:
            raise ValueError(
                "user_id is required for sending email."
            )

        try:
            user_id = int(user_id)

        except (
            TypeError,
            ValueError
        ):
            raise ValueError(
                "user_id must be a valid integer."
            )

        if user_id <= 0:
            raise ValueError(
                "user_id must be greater than zero."
            )

        return user_id

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
                "status": "failed",
                "message": (
                    "Email parameters must be a dictionary."
                )
            }

        # ---------------------------------
        # USER ID
        # ---------------------------------

        user_id = parameters.get(
            "user_id"
        )

        try:

            user_id = self._validate_user_id(
                user_id
            )

        except (
            TypeError,
            ValueError
        ) as error:

            return {
                "success": False,
                "status": "failed",
                "message": str(error)
            }

        # ---------------------------------
        # EMAIL PARAMETERS
        # ---------------------------------

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

        # ---------------------------------
        # VALIDATE EMAIL DATA
        # ---------------------------------

        try:

            email_data = self.prepare_email(
                recipient,
                subject,
                message
            )

        except (
            TypeError,
            ValueError
        ) as error:

            return {
                "success": False,
                "status": "failed",
                "message": str(error)
            }

        # ---------------------------------
        # SEND THROUGH GMAIL SERVICE
        # ---------------------------------

        try:

            result = self.gmail_service.send_email(
                user_id=user_id,
                recipient=email_data["recipient"],
                subject=email_data["subject"],
                message=email_data["message"]
            )

        except Exception as error:

            return {
                "success": False,
                "status": "failed",
                "action": "send",
                "recipient": email_data["recipient"],
                "subject": email_data["subject"],
                "message": (
                    "Email sending failed."
                ),
                "error": str(error)
            }

        # ---------------------------------
        # GMAIL SERVICE FAILURE
        # ---------------------------------

        if not result.get(
            "success",
            False
        ):

            return {
                "success": False,
                "status": "failed",
                "action": "send",
                "recipient": email_data["recipient"],
                "subject": email_data["subject"],
                "message": result.get(
                    "message",
                    "Failed to send email."
                ),
                "error": result.get(
                    "error"
                )
            }

        # ---------------------------------
        # SUCCESS
        # ---------------------------------

        return {
            "success": True,
            "status": "sent",
            "action": "send",
            "recipient": email_data["recipient"],
            "subject": email_data["subject"],
            "message": (
                "Email sent successfully through Gmail."
            ),
            "message_id": result.get(
                "message_id"
            ),
            "thread_id": result.get(
                "thread_id"
            ),
            "email": email_data
        }

    # =================================
    # TOOL AVAILABILITY
    # =================================

    def is_available(self) -> bool:

        try:

            return (
                self.gmail_service
                .get_status()
                .get(
                    "available",
                    False
                )
            )

        except Exception:

            return False