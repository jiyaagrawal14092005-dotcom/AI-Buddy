from app.tools.base_tool import BaseTool
from app.integrations.booking.provider import BookingProvider


class BookingTool(BaseTool):

    def __init__(self):

        super().__init__(
            name="booking",
            description=(
                "Create, list, retrieve, and cancel "
                "bookings and reservations."
            )
        )

        self.booking_provider = BookingProvider()

    # =================================
    # VALIDATE USER ID
    # =================================

    def _validate_user_id(
        self,
        user_id
    ) -> int:

        try:

            user_id = int(
                user_id
            )

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

    # =================================
    # VALIDATE TEXT
    # =================================

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

    # =================================
    # EXECUTE BOOKING ACTION
    # =================================

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
                    "Booking parameters "
                    "must be a dictionary."
                )
            }

        # ---------------------------------
        # USER ID
        # ---------------------------------

        user_id = parameters.get(
            "user_id"
        )

        try:

            user_id = self._validate_user_id(
                user_id
            )

        except ValueError as error:

            return {
                "success": False,
                "message": str(error)
            }

        # ---------------------------------
        # ACTION
        # ---------------------------------

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
                    "Booking action "
                    "must be a string."
                )
            }

        action = action.strip().lower()

        # ---------------------------------
        # CONNECT PROVIDER
        # ---------------------------------

        if not self.booking_provider.connected:

            connection_result = (
                self.booking_provider.connect()
            )

            if not connection_result.get(
                "success"
            ):

                return connection_result

        # ---------------------------------
        # CREATE BOOKING
        # ---------------------------------

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

            return self.booking_provider.execute(
                action="create",
                parameters={
                    "user_id": user_id,
                    "service": service,
                    "date": date,
                    "time": time,
                    "details": details
                }
            )

        # ---------------------------------
        # LIST BOOKINGS
        # ---------------------------------

        if action == "list":

            return self.booking_provider.execute(
                action="list",
                parameters={
                    "user_id": user_id
                }
            )

        # ---------------------------------
        # GET BOOKING
        # ---------------------------------

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

            return self.booking_provider.execute(
                action="get",
                parameters={
                    "user_id": user_id,
                    "booking_id": booking_id
                }
            )

        # ---------------------------------
        # CANCEL BOOKING
        # ---------------------------------

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
            ) as error:

                return {
                    "success": False,
                    "message": str(error)
                }

            return self.booking_provider.execute(
                action="cancel",
                parameters={
                    "user_id": user_id,
                    "booking_id": booking_id
                }
            )

        return {
            "success": False,
            "message": (
                f"Unsupported booking action: {action}"
            )
        }

    # =================================
    # TOOL AVAILABILITY
    # =================================

    def is_available(
        self
    ) -> bool:

        return True