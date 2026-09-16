from datetime import datetime
from uuid import uuid4

from app.integrations.base import BaseIntegration


class BookingProvider(BaseIntegration):

    def __init__(self):

        super().__init__(
            name="booking",
            description=(
                "Booking service integration for preparing "
                "and managing reservations and appointments."
            )
        )

        self.connected = False

        # Temporary in-memory booking store.
        # Real booking API/database integration will be added later.
        self.bookings = {}

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
            "booking_count": len(self.bookings)
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

    def _validate_user_id(
        self,
        user_id
    ) -> int:

        try:
            user_id = int(user_id)

        except (
            TypeError,
            ValueError
        ):
            raise ValueError(
                "User ID must be a valid integer."
            )

        if user_id <= 0:
            raise ValueError(
                "User ID must be greater than zero."
            )

        return user_id

    def _create_booking(
        self,
        user_id: int,
        parameters: dict
    ) -> dict:

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
        ) as error:

            return {
                "success": False,
                "message": str(error)
            }

        booking_id = str(uuid4())

        booking = {
            "booking_id": booking_id,
            "user_id": user_id,
            "service": service,
            "date": date,
            "time": time,
            "details": details,
            "status": "confirmed",
            "created_at": datetime.utcnow().isoformat()
        }

        self.bookings[booking_id] = booking

        return {
            "success": True,
            "status": "confirmed",
            "action": "create",
            "booking": booking,
            "message": (
                "Booking created successfully."
            )
        }

    def _cancel_booking(
        self,
        user_id: int,
        parameters: dict
    ) -> dict:

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
        ) as error:

            return {
                "success": False,
                "message": str(error)
            }

        booking = self.bookings.get(
            booking_id
        )

        if booking is None:
            return {
                "success": False,
                "message": (
                    "Booking was not found."
                )
            }

        if booking["user_id"] != user_id:
            return {
                "success": False,
                "message": (
                    "You are not authorized to "
                    "cancel this booking."
                )
            }

        if booking["status"] == "cancelled":
            return {
                "success": False,
                "message": (
                    "Booking is already cancelled."
                )
            }

        booking["status"] = "cancelled"
        booking["cancelled_at"] = (
            datetime.utcnow().isoformat()
        )

        return {
            "success": True,
            "status": "cancelled",
            "action": "cancel",
            "booking": booking,
            "message": (
                "Booking cancelled successfully."
            )
        }

    def _list_bookings(
        self,
        user_id: int
    ) -> dict:

        user_bookings = [
            booking
            for booking in self.bookings.values()
            if booking["user_id"] == user_id
        ]

        return {
            "success": True,
            "status": "listed",
            "action": "list",
            "bookings": user_bookings,
            "count": len(user_bookings),
            "message": (
                "Bookings retrieved successfully."
            )
        }

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

        try:

            user_id = self._validate_user_id(
                parameters.get("user_id")
            )

        except ValueError as error:

            return {
                "success": False,
                "message": str(error)
            }

        if action == "create":

            return self._create_booking(
                user_id=user_id,
                parameters=parameters
            )

        if action == "cancel":

            return self._cancel_booking(
                user_id=user_id,
                parameters=parameters
            )

        if action == "list":

            return self._list_bookings(
                user_id=user_id
            )

        if action == "get":

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
            ) as error:

                return {
                    "success": False,
                    "message": str(error)
                }

            booking = self.bookings.get(
                booking_id
            )

            if booking is None:
                return {
                    "success": False,
                    "message": (
                        "Booking was not found."
                    )
                }

            if booking["user_id"] != user_id:
                return {
                    "success": False,
                    "message": (
                        "You are not authorized "
                        "to view this booking."
                    )
                }

            return {
                "success": True,
                "status": "found",
                "action": "get",
                "booking": booking,
                "message": (
                    "Booking retrieved successfully."
                )
            }

        return {
            "success": False,
            "message": (
                f"Unsupported booking action: {action}"
            )
        }