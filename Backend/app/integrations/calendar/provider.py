
from datetime import datetime

from app.integrations.base import BaseIntegration
from app.integrations.calendar.service import GoogleCalendarService


class CalendarProvider(BaseIntegration):
    def __init__(self):
        super().__init__(
            name="calendar",
            description=(
                "Google Calendar integration for creating, "
                "listing, retrieving, and deleting calendar events."
            )
        )

        self.connected = False
        self.calendar_service = GoogleCalendarService()

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
            ),
            "service": self.calendar_service.get_status()
        }

    def connect(self, user_id: int | None = None) -> dict:
        if user_id is None:
            return {
                "success": False,
                "connected": False,
                "message": "User ID is required."
            }

        try:
            user_id = int(user_id)

        except (TypeError, ValueError):
            return {
                "success": False,
                "connected": False,
                "message": "User ID must be a valid integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "connected": False,
                "message": "User ID must be greater than zero."
            }

        calendar_result = (
            self.calendar_service.get_calendar_list(
                user_id=user_id
            )
        )

        if not calendar_result.get("success"):
            return {
                "success": False,
                "connected": False,
                "message": calendar_result.get(
                    "message",
                    "Google Calendar connection failed."
                )
            }

        self.connected = True

        return {
            "success": True,
            "connected": True,
            "provider": "google_calendar",
            "user_id": user_id,
            "calendar_count": calendar_result.get(
                "count",
                0
            ),
            "message": (
                "Google Calendar provider connected successfully."
            )
        }

    def disconnect(self) -> dict:
        self.connected = False

        return {
            "success": True,
            "connected": False,
            "message": (
                "Calendar provider disconnected successfully."
            )
        }

    def is_available(self) -> bool:
        return self.connected

    def _validate_text(
        self,
        value: str,
        field_name: str
    ) -> str:
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        value = value.strip()

        if not value:
            raise ValueError(
                f"{field_name} cannot be empty."
            )

        return value

    def _validate_date(self, date: str) -> str:
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

    def _validate_time(self, time: str) -> str:
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

    def execute(
        self,
        action: str,
        parameters: dict | None = None
    ) -> dict:

        if not isinstance(action, str):
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

        if not isinstance(parameters, dict):
            return {
                "success": False,
                "message": (
                    "Calendar parameters must be a dictionary."
                )
            }

        if not self.connected:
            return {
                "success": False,
                "message": (
                    "Calendar provider is not connected."
                )
            }

        user_id = parameters.get("user_id")

        if user_id is None:
            return {
                "success": False,
                "message": "User ID is required."
            }

        try:
            user_id = int(user_id)

        except (TypeError, ValueError):
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

        if action == "create":
            title = parameters.get(
                "title",
                parameters.get("event", "")
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

            calendar_id = parameters.get(
                "calendar_id",
                "primary"
            )

            duration_minutes = parameters.get(
                "duration_minutes",
                60
            )

            try:
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

                if not isinstance(details, str):
                    raise TypeError(
                        "Details must be a string."
                    )

                details = details.strip()

                if not isinstance(calendar_id, str):
                    raise TypeError(
                        "Calendar ID must be a string."
                    )

                calendar_id = calendar_id.strip()

                if not calendar_id:
                    calendar_id = "primary"

                duration_minutes = int(
                    duration_minutes
                )

                if duration_minutes <= 0:
                    raise ValueError(
                        "Duration must be greater than zero."
                    )

            except (TypeError, ValueError) as error:
                return {
                    "success": False,
                    "message": str(error)
                }

            return self.calendar_service.create_event(
                user_id=user_id,
                title=title,
                date=date,
                time=time,
                details=details,
                calendar_id=calendar_id,
                duration_minutes=duration_minutes
            )

        if action == "list":
            max_results = parameters.get(
                "max_results",
                10
            )

            calendar_id = parameters.get(
                "calendar_id",
                "primary"
            )

            try:
                max_results = int(
                    max_results
                )

            except (TypeError, ValueError):
                max_results = 10

            if not isinstance(calendar_id, str):
                calendar_id = "primary"

            calendar_id = calendar_id.strip()

            if not calendar_id:
                calendar_id = "primary"

            return self.calendar_service.list_events(
                user_id=user_id,
                max_results=max_results,
                calendar_id=calendar_id
            )

        if action == "get":
            event_id = parameters.get(
                "event_id",
                ""
            )

            calendar_id = parameters.get(
                "calendar_id",
                "primary"
            )

            if not isinstance(event_id, str):
                return {
                    "success": False,
                    "message": (
                        "Event ID must be a string."
                    )
                }

            event_id = event_id.strip()

            if not event_id:
                return {
                    "success": False,
                    "message": (
                        "Event ID is required."
                    )
                }

            if not isinstance(calendar_id, str):
                calendar_id = "primary"

            calendar_id = calendar_id.strip()

            if not calendar_id:
                calendar_id = "primary"

            return self.calendar_service.get_event(
                user_id=user_id,
                event_id=event_id,
                calendar_id=calendar_id
            )

        if action == "delete":
            event_id = parameters.get(
                "event_id",
                ""
            )

            calendar_id = parameters.get(
                "calendar_id",
                "primary"
            )

            if not isinstance(event_id, str):
                return {
                    "success": False,
                    "message": (
                        "Event ID must be a string."
                    )
                }

            event_id = event_id.strip()

            if not event_id:
                return {
                    "success": False,
                    "message": (
                        "Event ID is required."
                    )
                }

            if not isinstance(calendar_id, str):
                calendar_id = "primary"

            calendar_id = calendar_id.strip()

            if not calendar_id:
                calendar_id = "primary"

            return self.calendar_service.delete_event(
                user_id=user_id,
                event_id=event_id,
                calendar_id=calendar_id
            )

        if action == "calendars":
            return self.calendar_service.get_calendar_list(
                user_id=user_id
            )

        return {
            "success": False,
            "message": (
                f"Unsupported calendar action: {action}"
            )
        }

