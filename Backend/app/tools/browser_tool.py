from urllib.parse import urlparse

from app.tools.base_tool import BaseTool


class BrowserTool(BaseTool):

    def __init__(self):

        super().__init__(
            name="browser",
            description=(
                "Prepare browser actions such as opening "
                "a website or navigating to a URL."
            )
        )

    def _validate_url(
        self,
        url: str
    ) -> str:

        if not isinstance(
            url,
            str
        ):
            raise TypeError(
                "URL must be a string."
            )

        url = url.strip()

        if not url:
            raise ValueError(
                "URL cannot be empty."
            )

        parsed_url = urlparse(
            url
        )

        if parsed_url.scheme not in {
            "http",
            "https"
        }:
            raise ValueError(
                "URL must start with http:// or https://."
            )

        if not parsed_url.netloc:
            raise ValueError(
                "Invalid URL."
            )

        return url

    def _validate_action(
        self,
        action: str
    ) -> str:

        if not isinstance(
            action,
            str
        ):
            raise TypeError(
                "Browser action must be a string."
            )

        action = action.strip().lower()

        allowed_actions = {
            "open",
            "navigate"
        }

        if action not in allowed_actions:
            raise ValueError(
                "Unsupported browser action. "
                "Use open or navigate."
            )

        return action

    def prepare_action(
        self,
        action: str,
        url: str
    ) -> dict:

        action = self._validate_action(
            action
        )

        url = self._validate_url(
            url
        )

        return {
            "action": action,
            "url": url
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
                    "Browser parameters must be a dictionary."
                )
            }

        action = parameters.get(
            "action",
            "open"
        )

        url = parameters.get(
            "url",
            ""
        )

        try:

            browser_data = self.prepare_action(
                action,
                url
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
            "browser": browser_data,
            "message": (
                "Browser action prepared successfully."
            )
        }

    def is_available(self) -> bool:
        return True