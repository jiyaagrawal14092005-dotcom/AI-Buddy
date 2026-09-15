import subprocess
import webbrowser


class ApplicationLauncher:

    APPLICATIONS = {
        "chrome": "chrome",
        "google chrome": "chrome",
        "edge": "msedge",
        "microsoft edge": "msedge",
        "notepad": "notepad",
        "calculator": "calc",
        "calc": "calc",
        "paint": "mspaint",
        "vs code": "code",
        "visual studio code": "code",
    }

    def __init__(self):
        self.name = "application_launcher"

    def _validate_name(self, application: str) -> str:

        if not isinstance(application, str):
            raise TypeError(
                "Application name must be a string."
            )

        application = application.strip().lower()

        if not application:
            raise ValueError(
                "Application name cannot be empty."
            )

        return application

    def open_application(
        self,
        application: str
    ) -> dict:

        try:
            application = self._validate_name(
                application
            )

        except (
            TypeError,
            ValueError
        ) as error:

            return {
                "success": False,
                "message": str(error)
            }

        command = self.APPLICATIONS.get(
            application
        )

        if command is None:
            return {
                "success": False,
                "message": (
                    f"Application '{application}' "
                    "is not supported."
                )
            }

        try:

            subprocess.Popen(
                command,
                shell=True
            )

            return {
                "success": True,
                "application": application,
                "command": command,
                "status": "opened",
                "message": (
                    f"Application '{application}' "
                    "opened successfully."
                )
            }

        except Exception as error:

            return {
                "success": False,
                "application": application,
                "message": (
                    f"Could not open "
                    f"application '{application}'."
                ),
                "error": str(error)
            }

    def open_website(
        self,
        url: str
    ) -> dict:

        if not isinstance(url, str):
            return {
                "success": False,
                "message": "URL must be a string."
            }

        url = url.strip()

        if not url:
            return {
                "success": False,
                "message": "URL cannot be empty."
            }

        if not (
            url.startswith("http://")
            or url.startswith("https://")
        ):
            return {
                "success": False,
                "message": (
                    "URL must start with "
                    "http:// or https://."
                )
            }

        try:

            webbrowser.open(url)

            return {
                "success": True,
                "url": url,
                "status": "opened",
                "message": (
                    "Website opened successfully."
                )
            }

        except Exception as error:

            return {
                "success": False,
                "url": url,
                "message": (
                    "Could not open website."
                ),
                "error": str(error)
            }

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
                    "Launcher parameters "
                    "must be a dictionary."
                )
            }

        action = parameters.get(
            "action",
            "open_application"
        )

        if action == "open_application":

            application = parameters.get(
                "application",
                parameters.get(
                    "app",
                    ""
                )
            )

            return self.open_application(
                application
            )

        if action == "open_website":

            url = parameters.get(
                "url",
                ""
            )

            return self.open_website(
                url
            )

        return {
            "success": False,
            "message": (
                "Unsupported launcher action. "
                "Use open_application or open_website."
            )
        }

    def is_available(self) -> bool:
        return True