from app.integrations.base import BaseIntegration


class SocialProvider(BaseIntegration):

    def __init__(self):

        super().__init__(
            name="social",
            description=(
                "Social media integration for preparing "
                "post, content, and profile actions."
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
            "message": (
                "Social provider connected successfully."
            )
        }

    def disconnect(self) -> dict:

        self.connected = False

        return {
            "success": True,
            "connected": False,
            "message": (
                "Social provider disconnected successfully."
            )
        }

    def is_available(self) -> bool:
        return self.connected

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
                    "Social parameters "
                    "must be a dictionary."
                )
            }

        if not self.connected:
            return {
                "success": False,
                "message": (
                    "Social provider "
                    "is not connected."
                )
            }

        if action == "create_post":

            content = parameters.get(
                "content",
                parameters.get(
                    "text",
                    ""
                )
            )

            platform = parameters.get(
                "platform",
                ""
            )

            try:

                content = self._validate_text(
                    content,
                    "Content"
                )

                platform = self._validate_text(
                    platform,
                    "Platform"
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
                "action": "create_post",
                "post": {
                    "platform": platform,
                    "content": content
                },
                "message": (
                    "Social media post action "
                    "prepared successfully."
                )
            }

        if action == "profile":

            platform = parameters.get(
                "platform",
                ""
            )

            try:

                platform = self._validate_text(
                    platform,
                    "Platform"
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
                "action": "profile",
                "platform": platform,
                "message": (
                    "Social profile action "
                    "prepared successfully."
                )
            }

        if action == "schedule_post":

            content = parameters.get(
                "content",
                ""
            )

            platform = parameters.get(
                "platform",
                ""
            )

            scheduled_time = parameters.get(
                "scheduled_time",
                ""
            )

            try:

                content = self._validate_text(
                    content,
                    "Content"
                )

                platform = self._validate_text(
                    platform,
                    "Platform"
                )

                scheduled_time = self._validate_text(
                    scheduled_time,
                    "Scheduled time"
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
                "action": "schedule_post",
                "post": {
                    "platform": platform,
                    "content": content,
                    "scheduled_time": scheduled_time
                },
                "message": (
                    "Social media post scheduling "
                    "prepared successfully."
                )
            }

        return {
            "success": False,
            "message": (
                f"Unsupported social action: {action}"
            )
        }