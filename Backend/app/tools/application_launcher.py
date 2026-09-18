import os
import subprocess
import webbrowser


class ApplicationLauncher:
    """
    Launches commonly used applications on Windows.

    Supports:
    - Chrome
    - Microsoft Edge
    - Notepad
    - Calculator
    - Paint
    - VS Code
    - File Explorer
    """

    APPLICATIONS = {
        "chrome": "google_chrome",
        "google chrome": "google_chrome",

        "edge": "microsoft_edge",
        "microsoft edge": "microsoft_edge",

        "notepad": "notepad",

        "calculator": "calc",
        "calc": "calc",

        "paint": "mspaint",

        "vs code": "code",
        "visual studio code": "code",
        "vscode": "code",

        "file explorer": "explorer",
        "explorer": "explorer",
    }

    WINDOWS_PATHS = {
        "google_chrome": (
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        ),

        "microsoft_edge": (
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        ),
    }

    def __init__(self):
        self.name = "application_launcher"

    def _normalize_application_name(
        self,
        application: str
    ) -> str:
        if not isinstance(application, str):
            return ""

        return " ".join(
            application.strip().lower().split()
        )

    def _get_application_command(
        self,
        application: str
    ):
        normalized_application = (
            self._normalize_application_name(
                application
            )
        )

        if not normalized_application:
            return None

        application_key = self.APPLICATIONS.get(
            normalized_application
        )

        if application_key is None:
            return None

        # Known Windows executable paths
        if application_key in self.WINDOWS_PATHS:
            executable_path = self.WINDOWS_PATHS[
                application_key
            ]

            if os.path.exists(executable_path):
                return executable_path

        # Standard Windows commands
        return application_key

    def open_application(
        self,
        application: str
    ) -> dict:
        normalized_application = (
            self._normalize_application_name(
                application
            )
        )

        if not normalized_application:
            return {
                "success": False,
                "application": application,
                "message": (
                    "Application name cannot be empty."
                )
            }

        command = self._get_application_command(
            normalized_application
        )

        if command is None:
            return {
                "success": False,
                "application": normalized_application,
                "message": (
                    f"Application "
                    f"'{normalized_application}' "
                    f"is not supported."
                )
            }

        try:
            # Microsoft Edge and Chrome should be
            # launched using Windows' native process
            # launcher because their executable may
            # immediately exit when started directly.
            if normalized_application in {
                "microsoft edge",
                "edge",
                "google chrome",
                "chrome",
            }:
                subprocess.Popen(
                    [
                        "cmd",
                        "/c",
                        "start",
                        "",
                        command
                    ],
                    shell=False
                )

            elif command in {
                "notepad",
                "calc",
                "mspaint",
                "code",
                "explorer",
            }:
                subprocess.Popen(
                    command,
                    shell=True
                )

            else:
                subprocess.Popen(
                    command,
                    shell=True
                )

            return {
                "success": True,
                "application": normalized_application,
                "command": command,
                "status": "opened",
                "message": (
                    f"Application "
                    f"'{normalized_application}' "
                    f"opened successfully."
                )
            }

        except Exception as error:
            return {
                "success": False,
                "application": normalized_application,
                "command": command,
                "status": "failed",
                "message": (
                    f"Failed to open "
                    f"'{normalized_application}': "
                    f"{error}"
                )
            }

    def open_url(
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

        try:
            webbrowser.open(url)

            return {
                "success": True,
                "url": url,
                "status": "opened",
                "message": (
                    "URL opened successfully."
                )
            }

        except Exception as error:
            return {
                "success": False,
                "url": url,
                "status": "failed",
                "message": (
                    f"Failed to open URL: {error}"
                )
            }

    def execute(
        self,
        application: str
    ) -> dict:
        return self.open_application(
            application
        )

    def get_supported_applications(self) -> list:
        return list(
            self.APPLICATIONS.keys()
        )

    def is_supported(
        self,
        application: str
    ) -> bool:
        normalized_application = (
            self._normalize_application_name(
                application
            )
        )

        return (
            normalized_application
            in self.APPLICATIONS
        )