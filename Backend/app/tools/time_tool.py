from datetime import datetime
from zoneinfo import ZoneInfo

from app.tools.base_tool import BaseTool


class TimeTool(BaseTool):
    """
    Provides current date and time information for AI Buddy.
    """

    def __init__(self):
        super().__init__(
            name="time_tool",
            description="Provides real-time current date and time."
        )

    def get_current_time(
        self,
        timezone: str = "Asia/Kolkata"
    ) -> dict:
        """
        Get the current date and time for the given timezone.
        """

        try:
            tz = ZoneInfo(timezone)
            now = datetime.now(tz)

            return {
                "success": True,
                "timezone": timezone,
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%I:%M:%S %p"),
                "day": now.strftime("%A"),
                "formatted": now.strftime(
                    "%A, %d %B %Y, %I:%M:%S %p"
                ),
                "message": (
                    f"The current time is "
                    f"{now.strftime('%I:%M:%S %p')} "
                    f"on {now.strftime('%A, %d %B %Y')}."
                )
            }

        except Exception as error:
            return {
                "success": False,
                "timezone": timezone,
                "date": "",
                "time": "",
                "day": "",
                "formatted": "",
                "message": f"Unable to get current time: {error}"
            }

    def get_current_date(
        self,
        timezone: str = "Asia/Kolkata"
    ) -> dict:
        """
        Get the current date for the given timezone.
        """

        try:
            tz = ZoneInfo(timezone)
            now = datetime.now(tz)

            return {
                "success": True,
                "timezone": timezone,
                "date": now.strftime("%Y-%m-%d"),
                "day": now.strftime("%A"),
                "formatted": now.strftime(
                    "%A, %d %B %Y"
                ),
                "message": (
                    f"Today is "
                    f"{now.strftime('%A, %d %B %Y')}."
                )
            }

        except Exception as error:
            return {
                "success": False,
                "timezone": timezone,
                "date": "",
                "day": "",
                "formatted": "",
                "message": f"Unable to get current date: {error}"
            }

    def execute(
        self,
        action: str = "current_time",
        timezone: str = "Asia/Kolkata"
    ) -> dict:
        """
        Execute a time/date action.
        """

        if action == "current_time":
            return self.get_current_time(timezone)

        if action == "current_date":
            return self.get_current_date(timezone)

        return {
            "success": False,
            "timezone": timezone,
            "message": (
                f"Unsupported time action: {action}"
            )
        }