from app.integrations.base import BaseIntegration
from app.integrations.email.gmail_service import GmailService


class EmailProvider(BaseIntegration):

    def __init__(self):

        super().__init__(
            name="email",
            description=(
                "Email service integration for preparing "
                "and managing email actions."
            )
        )

        self.connected = False
        self.gmail_service = GmailService()

    def get_status(self) -> dict:

        gmail_status = self.gmail_service.get_status()

        return {
            "name": self.name,
            "description": self.description,
            "connected": self.connected,
            "available": (
                self.is_available()
                and gmail_status.get("available", False)
            ),
            "status": (
                "connected"
                if self.connected
                else "disconnected"
            ),
            "gmail_service": gmail_status
        }

    def connect(
        self,
        user_id: int | None = None
    ) -> dict:

        if user_id is None:
            return {
                "success": False,
                "connected": False,
                "message": "User ID is required."
            }

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return {
                "success": False,
                "connected": False,
                "message": "User ID must be a valid integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "connected": False,
                "message": "User ID must be greater than zero."
            }

        profile_result = self.gmail_service.get_profile(
            user_id=user_id
        )

        if not profile_result.get("success"):
            return {
                "success": False,
                "connected": False,
                "message": (
                    profile_result.get(
                        "message",
                        "Gmail connection failed."
                    )
                )
            }

        self.connected = True

        return {
            "success": True,
            "connected": True,
            "provider": "gmail",
            "user_id": user_id,
            "email_address": profile_result.get(
                "email_address"
            ),
            "message": (
                "Gmail provider connected successfully."
            )
        }

    def disconnect(self) -> dict:

        self.connected = False

        return {
            "success": True,
            "connected": False,
            "message": (
                "Email provider disconnected successfully."
            )
        }

    def is_available(self) -> bool:

        return self.connected

    def execute(
        self,
        action: str,
        parameters: dict | None = None
    ) -> dict:

        if not isinstance(
            action,
            str
        ):
            return {
                "success": False,
                "message": "Action must be a string."
            }

        action = action.strip().lower()

        if not action:
            return {
                "success": False,
                "message": "Action cannot be empty."
            }

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

        if not self.connected:
            return {
                "success": False,
                "message": (
                    "Email provider is not connected."
                )
            }

        user_id = parameters.get("user_id")

        if user_id is None:
            return {
                "success": False,
                "message": "User ID is required."
            }

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return {
                "success": False,
                "message": "User ID must be a valid integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "message": "User ID must be greater than zero."
            }

        if action == "send":

            recipient = parameters.get(
                "recipient",
                ""
            )

            subject = parameters.get(
                "subject",
                ""
            )

            message = parameters.get(
                "message",
                ""
            )

            if not recipient:
                return {
                    "success": False,
                    "message": "Recipient is required."
                }

            if not subject:
                return {
                    "success": False,
                    "message": "Subject is required."
                }

            if not message:
                return {
                    "success": False,
                    "message": "Message is required."
                }

            return self.gmail_service.send_email(
                user_id=user_id,
                recipient=recipient,
                subject=subject,
                message=message
            )

        if action == "list_messages":

            max_results = parameters.get(
                "max_results",
                10
            )

            try:
                max_results = int(max_results)
            except (TypeError, ValueError):
                max_results = 10

            return self.gmail_service.list_messages(
                user_id=user_id,
                max_results=max_results
            )

        if action == "profile":

            return self.gmail_service.get_profile(
                user_id=user_id
            )

        if action == "draft":

            return {
                "success": True,
                "status": "prepared",
                "action": "draft",
                "email": parameters,
                "message": (
                    "Email draft prepared successfully."
                )
            }

        return {
            "success": False,
            "message": (
                f"Unsupported email action: {action}"
            )
        }