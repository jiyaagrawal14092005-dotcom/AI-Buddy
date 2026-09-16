
from datetime import datetime

from app.tools.base_tool import BaseTool
from app.integrations.calendar.provider import CalendarProvider


class CalendarTool(BaseTool):

    def __init__(self):

        super().__init__(
            name="calendar",
            description=(
                "Create, list, retrieve, and delete "
                "Google Calendar events."
            )
        )

        self.calendar_provider = CalendarProvider()

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
        details: str = "",
        duration_minutes: int = 60
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

        try:

            duration_minutes = int(
                duration_minutes
            )

        except (
            TypeError,
            ValueError
        ):

            raise ValueError(
                "Duration must be a valid integer."
            )

        if duration_minutes <= 0:

            raise ValueError(
                "Duration must be greater than zero."
            )

        return {
            "title": title,
            "date": date,
            "time": time,
            "details": details,
            "duration_minutes": duration_minutes
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

        user_id = parameters.get(
            "user_id"
        )

        if user_id is None:
            return {
                "success": False,
                "message": (
                    "User ID is required."
                )
            }

        try:

            user_id = int(
                user_id
            )

        except (
            TypeError,
            ValueError
        ):

            return {
                "success": False,
                "message": (
                    "User ID must be a valid integer."
                )
            }

        if user_id <= 0:

            return {
                "success": False,
                "message": (
                    "User ID must be greater than zero."
                )
            }

        action = parameters.get(
            "action",
            "create"
        )

        if not isinstance(
            action,
            str
        ):
            return {
                "success": False,
                "message": (
                    "Action must be a string."
                )
            }

        action = action.strip().lower()

        # -----------------------------------------
        # CREATE EVENT
        # -----------------------------------------

        if action == "create":

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

            duration_minutes = parameters.get(
                "duration_minutes",
                60
            )

            try:

                event_data = self.prepare_event(
                    title,
                    date,
                    time,
                    details,
                    duration_minutes
                )

            except (
                TypeError,
                ValueError
            ) as error:

                return {
                    "success": False,
                    "message": str(error)
                }

            # Connect provider to the user's
            # real Google Calendar.

            connection_result = (
                self.calendar_provider.connect(
                    user_id
                )
            )

            if not connection_result.get(
                "success"
            ):

                return connection_result

            return self.calendar_provider.execute(
                action="create",
                parameters={
                    "user_id": user_id,
                    "title": event_data["title"],
                    "date": event_data["date"],
                    "time": event_data["time"],
                    "details": event_data["details"],
                    "duration_minutes": (
                        event_data[
                            "duration_minutes"
                        ]
                    ),
                    "calendar_id": parameters.get(
                        "calendar_id",
                        "primary"
                    )
                }
            )

        # -----------------------------------------
        # LIST EVENTS
        # -----------------------------------------

        if action == "list":

            connection_result = (
                self.calendar_provider.connect(
                    user_id
                )
            )

            if not connection_result.get(
                "success"
            ):

                return connection_result

            return self.calendar_provider.execute(
                action="list",
                parameters={
                    "user_id": user_id,
                    "max_results": parameters.get(
                        "max_results",
                        10
                    ),
                    "calendar_id": parameters.get(
                        "calendar_id",
                        "primary"
                    )
                }
            )

        # -----------------------------------------
        # GET EVENT
        # -----------------------------------------

        if action == "get":

            event_id = parameters.get(
                "event_id",
                ""
            )

            if not isinstance(
                event_id,
                str
            ) or not event_id.strip():

                return {
                    "success": False,
                    "message": (
                        "Event ID is required."
                    )
                }

            connection_result = (
                self.calendar_provider.connect(
                    user_id
                )
            )

            if not connection_result.get(
                "success"
            ):

                return connection_result

            return self.calendar_provider.execute(
                action="get",
                parameters={
                    "user_id": user_id,
                    "event_id": event_id,
                    "calendar_id": parameters.get(
                        "calendar_id",
                        "primary"
                    )
                }
            )

        # -----------------------------------------
        # DELETE EVENT
        # -----------------------------------------

        if action == "delete":

            event_id = parameters.get(
                "event_id",
                ""
            )

            if not isinstance(
                event_id,
                str
            ) or not event_id.strip():

                return {
                    "success": False,
                    "message": (
                        "Event ID is required."
                    )
                }

            connection_result = (
                self.calendar_provider.connect(
                    user_id
                )
            )

            if not connection_result.get(
                "success"
            ):

                return connection_result

            return self.calendar_provider.execute(
                action="delete",
                parameters={
                    "user_id": user_id,
                    "event_id": event_id,
                    "calendar_id": parameters.get(
                        "calendar_id",
                        "primary"
                    )
                }
            )

        # -----------------------------------------
        # CALENDAR LIST
        # -----------------------------------------

        if action == "calendars":

            connection_result = (
                self.calendar_provider.connect(
                    user_id
                )
            )

            if not connection_result.get(
                "success"
            ):

                return connection_result

            return self.calendar_provider.execute(
                action="calendars",
                parameters={
                    "user_id": user_id
                }
            )

        return {
            "success": False,
            "message": (
                f"Unsupported calendar action: {action}"
            )
        }

    def is_available(
        self
    ) -> bool:

        return True

