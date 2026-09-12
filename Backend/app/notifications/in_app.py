class InAppNotification:

    def __init__(self):

        self.name = "in_app_notification"
        self.enabled = True
        self.notifications = []

    def send(
        self,
        message: str,
        title: str = "AI Buddy"
    ) -> dict:

        if not isinstance(
            message,
            str
        ):
            return {
                "success": False,
                "message": "Message must be a string."
            }

        if not isinstance(
            title,
            str
        ):
            return {
                "success": False,
                "message": "Title must be a string."
            }

        message = message.strip()
        title = title.strip()

        if not message:
            return {
                "success": False,
                "message": "Message cannot be empty."
            }

        if not title:
            return {
                "success": False,
                "message": "Title cannot be empty."
            }

        if not self.enabled:
            return {
                "success": False,
                "message": (
                    "In-app notifications are disabled."
                )
            }

        notification = {
            "id": len(self.notifications) + 1,
            "title": title,
            "message": message,
            "status": "unread"
        }

        self.notifications.append(
            notification
        )

        return {
            "success": True,
            "notification": notification,
            "message": (
                "In-app notification created successfully."
            )
        }

    def get_notifications(self) -> list:

        return list(
            self.notifications
        )

    def mark_as_read(
        self,
        notification_id: int
    ) -> dict:

        for notification in self.notifications:

            if notification["id"] == notification_id:

                notification["status"] = "read"

                return {
                    "success": True,
                    "notification": notification,
                    "message": (
                        "Notification marked as read."
                    )
                }

        return {
            "success": False,
            "message": "Notification not found."
        }

    def clear(self) -> None:

        self.notifications.clear()

    def enable(self) -> None:

        self.enabled = True

    def disable(self) -> None:

        self.enabled = False

    def is_enabled(self) -> bool:

        return self.enabled

    def get_status(self) -> dict:

        return {
            "name": self.name,
            "enabled": self.enabled,
            "notification_count": len(
                self.notifications
            )
        }