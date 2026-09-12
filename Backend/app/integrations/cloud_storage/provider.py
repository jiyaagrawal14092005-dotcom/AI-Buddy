from app.integrations.base import BaseIntegration


class CloudStorageProvider(BaseIntegration):

    def __init__(self):

        super().__init__(
            name="cloud_storage",
            description=(
                "Cloud storage integration for preparing "
                "file upload, download, and listing actions."
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
                "Cloud storage provider connected successfully."
            )
        }

    def disconnect(self) -> dict:

        self.connected = False

        return {
            "success": True,
            "connected": False,
            "message": (
                "Cloud storage provider disconnected successfully."
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
                    "Cloud storage parameters "
                    "must be a dictionary."
                )
            }

        if not self.connected:
            return {
                "success": False,
                "message": (
                    "Cloud storage provider "
                    "is not connected."
                )
            }

        if action == "upload":

            file_path = parameters.get(
                "file_path",
                parameters.get(
                    "path",
                    ""
                )
            )

            try:

                file_path = self._validate_text(
                    file_path,
                    "File path"
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
                "action": "upload",
                "file_path": file_path,
                "message": (
                    "File upload action "
                    "prepared successfully."
                )
            }

        if action == "download":

            file_name = parameters.get(
                "file_name",
                parameters.get(
                    "name",
                    ""
                )
            )

            try:

                file_name = self._validate_text(
                    file_name,
                    "File name"
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
                "action": "download",
                "file_name": file_name,
                "message": (
                    "File download action "
                    "prepared successfully."
                )
            }

        if action == "list":

            return {
                "success": True,
                "status": "prepared",
                "action": "list",
                "message": (
                    "Cloud storage file listing "
                    "prepared successfully."
                )
            }

        return {
            "success": False,
            "message": (
                f"Unsupported cloud storage action: {action}"
            )
        }