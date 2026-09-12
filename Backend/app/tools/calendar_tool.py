from datetime import datetime

from app.tools.base_tool import BaseTool


class CalendarTool(BaseTool):

    def __init__(self):

        super().__init__(
            name="calendar",
            description=(
                "Prepare a calendar event with a title, "
                "date, time, and optional details."
            )
        )

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

    def _validate_date(
        self,
        date: str
    ) -> str:

        date = self._validate_text(
            date,
            "Date"
        )

        try:

            datetime.strptime(
                date,
                "%Y-%m-%d"
            )

        except ValueError:

            raise ValueError(
                "Date must use YYYY-MM-DD format."
            )

        return date

    def _validate_time(
        self,
        time: str
    ) -> str:

        time = self._validate_text(
            time,
            "Time"
        )

        try:

            datetime.strptime(
                time,
                "%H:%M"
            )

        except ValueError:

            raise ValueError(
                "Time must use HH:MM format."
            )

        return time

    def prepare_event(
        self,
        title: str,
        date: str,
        time: str,
        details: str = ""
    ) -> dict:

        title = self._validate_text(
            title,
            "Title"
        )

        date = self._validate_date(
            date
        )

        time = self._validate_time(
            time
        )

        if not isinstance(
            details,
            str
        ):
            raise TypeError(
                "Details must be a string."
            )

        details = details.strip()

        return {
            "title": title,
            "date": date,
            "time": time,
            "details": details
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
                    "Calendar parameters must be a dictionary."
                )
            }

        title = parameters.get(
            "title",
            parameters.get(
                "event",
                ""
            )
        )

        date = parameters.get(
            "date",
            ""
        )

        time = parameters.get(
            "time",
            ""
        )

        details = parameters.get(
            "details",
            ""
        )

        try:

            event_data = self.prepare_event(
                title,
                date,
                time,
                details
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
            "event": event_data,
            "message": (
                "Calendar event prepared successfully."
            )
        }

    def is_available(self) -> bool:
        return True