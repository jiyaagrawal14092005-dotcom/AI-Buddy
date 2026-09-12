from app.integrations.base import BaseIntegration


class EducationProvider(BaseIntegration):

    def __init__(self):

        super().__init__(
            name="education",
            description=(
                "Education service integration for managing "
                "learning tasks, courses, and study resources."
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
                "Education provider connected successfully."
            )
        }

    def disconnect(self) -> dict:

        self.connected = False

        return {
            "success": True,
            "connected": False,
            "message": (
                "Education provider disconnected successfully."
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
                    "Education parameters "
                    "must be a dictionary."
                )
            }

        if not self.connected:
            return {
                "success": False,
                "message": (
                    "Education provider "
                    "is not connected."
                )
            }

        if action == "create_task":

            title = parameters.get(
                "title",
                parameters.get(
                    "task",
                    ""
                )
            )

            try:

                title = self._validate_text(
                    title,
                    "Task title"
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
                "action": "create_task",
                "task": {
                    "title": title
                },
                "message": (
                    "Education task creation "
                    "prepared successfully."
                )
            }

        if action == "study":

            topic = parameters.get(
                "topic",
                ""
            )

            try:

                topic = self._validate_text(
                    topic,
                    "Study topic"
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
                "action": "study",
                "topic": topic,
                "message": (
                    "Study action prepared successfully."
                )
            }

        if action == "resource":

            resource = parameters.get(
                "resource",
                parameters.get(
                    "url",
                    ""
                )
            )

            try:

                resource = self._validate_text(
                    resource,
                    "Resource"
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
                "action": "resource",
                "resource": resource,
                "message": (
                    "Education resource action "
                    "prepared successfully."
                )
            }

        if action == "list":

            return {
                "success": True,
                "status": "prepared",
                "action": "list",
                "message": (
                    "Education resources listing "
                    "prepared successfully."
                )
            }

        return {
            "success": False,
            "message": (
                f"Unsupported education action: {action}"
            )
        }