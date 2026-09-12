from app.integrations.base import BaseIntegration


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

    def get_status(self) -> dict:

        return {
            "name": self.name,
            "description": self.description,
            "connected": self.connected,
            "available": self.is_available(),
            "status": (
                "connected"
                if self.connected
                else "disconnected"
            )
        }

    def connect(self) -> dict:

        self.connected = True

        return {
            "success": True,
            "connected": True,
            "message": "Email provider connected successfully."
        }

    def disconnect(self) -> dict:

        self.connected = False

        return {
            "success": True,
            "connected": False,
            "message": "Email provider disconnected successfully."
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

            return {
                "success": True,
                "status": "prepared",
                "action": "send",
                "email": {
                    "recipient": recipient,
                    "subject": subject,
                    "message": message
                },
                "message": (
                    "Email send action prepared successfully."
                )
            }

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