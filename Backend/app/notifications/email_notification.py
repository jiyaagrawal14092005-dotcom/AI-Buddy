class EmailNotification:

    def __init__(self):

        self.name = "email_notification"
        self.enabled = True

    def send(
        self,
        recipient: str,
        subject: str,
        message: str
    ) -> dict:

        if not isinstance(
            recipient,
            str
        ):
            return {
                "success": False,
                "message": "Recipient must be a string."
            }

        if not isinstance(
            subject,
            str
        ):
            return {
                "success": False,
                "message": "Subject must be a string."
            }

        if not isinstance(
            message,
            str
        ):
            return {
                "success": False,
                "message": "Message must be a string."
            }

        recipient = recipient.strip()
        subject = subject.strip()
        message = message.strip()

        if not recipient:
            return {
                "success": False,
                "message": "Recipient cannot be empty."
            }

        if not subject:
            return {
                "success": False,
                "message": "Subject cannot be empty."
            }

        if not message:
            return {
                "success": False,
                "message": "Message cannot be empty."
            }

        if not self.enabled:
            return {
                "success": False,
                "message": "Email notifications are disabled."
            }

        return {
            "success": True,
            "status": "prepared",
            "notification": {
                "type": "email",
                "recipient": recipient,
                "subject": subject,
                "message": message
            },
            "message": (
                "Email notification prepared successfully."
            )
        }

    def enable(self) -> None:

        self.enabled = True

    def disable(self) -> None:

        self.enabled = False

    def is_enabled(self) -> bool:

        return self.enabled

    def get_status(self) -> dict:

        return {
            "name": self.name,
            "enabled": self.enabled
        }