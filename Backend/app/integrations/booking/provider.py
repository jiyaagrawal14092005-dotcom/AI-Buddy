from datetime import datetime

from app.integrations.base import BaseIntegration


class BookingProvider(BaseIntegration):

    def __init__(self):

        super().__init__(
            name="booking",
            description=(
                "Booking service integration for preparing "
                "reservations and appointment actions."
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
                "Booking provider connected successfully."
            )
        }

    def disconnect(self) -> dict:

        self.connected = False

        return {
            "success": True,
            "connected": False,
            "message": (
                "Booking provider disconnected successfully."
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
                    "Booking parameters "
                    "must be a dictionary."
                )
            }

        if not self.connected:
            return {
                "success": False,
                "message": (
                    "Booking provider "
                    "is not connected."
                )
            }

        if action == "create":

            service = parameters.get(
                "service",
                parameters.get(
                    "name",
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

                service = self._validate_text(
                    service,
                    "Service"
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
                "action": "create",
                "booking": {
                    "service": service,
                    "date": date,
                    "time": time,
                    "details": details
                },
                "message": (
                    "Booking creation action "
                    "prepared successfully."
                )
            }

        if action == "cancel":

            booking_id = parameters.get(
                "booking_id",
                ""
            )

            try:

                booking_id = self._validate_text(
                    booking_id,
                    "Booking ID"
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
                "action": "cancel",
                "booking_id": booking_id,
                "message": (
                    "Booking cancellation action "
                    "prepared successfully."
                )
            }

        if action == "list":

            return {
                "success": True,
                "status": "prepared",
                "action": "list",
                "message": (
                    "Booking listing action "
                    "prepared successfully."
                )
            }

        return {
            "success": False,
            "message": (
                f"Unsupported booking action: {action}"
            )
        }