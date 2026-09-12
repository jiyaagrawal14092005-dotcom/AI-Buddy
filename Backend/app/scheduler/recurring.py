from datetime import datetime, timedelta


class RecurringSchedule:

    def __init__(
        self,
        name: str,
        interval_seconds: int
    ):
        # Validate name
        if not isinstance(name, str) or not name.strip():
            raise ValueError(
                "Schedule name must be a non-empty string."
            )

        # Validate interval
        if not isinstance(interval_seconds, int):
            raise TypeError(
                "Interval must be an integer."
            )

        if interval_seconds <= 0:
            raise ValueError(
                "Interval must be greater than 0 seconds."
            )

        self.name = name.strip()
        self.interval_seconds = interval_seconds
        self.created_at = datetime.now()

        self.next_run = (
            self.created_at
            + timedelta(seconds=interval_seconds)
        )

        self.active = True

    def get_next_run(self) -> str:
        """
        Return the next scheduled execution time.
        """

        return self.next_run.isoformat()

    def update_next_run(self) -> str:
        """
        Move the schedule to its next execution time.
        """

        if not self.active:
            return self.next_run.isoformat()

        self.next_run = (
            self.next_run
            + timedelta(
                seconds=self.interval_seconds
            )
        )

        return self.next_run.isoformat()

    def pause(self) -> dict:
        """
        Pause the recurring schedule.
        """

        self.active = False

        return {
            "success": True,
            "message": (
                f"Recurring schedule "
                f"'{self.name}' paused."
            ),
            "active": self.active
        }

    def resume(self) -> dict:
        """
        Resume the recurring schedule.
        """

        self.active = True

        return {
            "success": True,
            "message": (
                f"Recurring schedule "
                f"'{self.name}' resumed."
            ),
            "active": self.active
        }

    def is_active(self) -> bool:
        """
        Check whether the recurring schedule is active.
        """

        return self.active

    def to_dict(self) -> dict:
        """
        Return schedule information as a dictionary.
        """

        return {
            "name": self.name,
            "interval_seconds": self.interval_seconds,
            "created_at": self.created_at.isoformat(),
            "next_run": self.next_run.isoformat(),
            "active": self.active
        }