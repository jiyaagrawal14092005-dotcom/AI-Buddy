import threading
from datetime import datetime


class Timer:

    def __init__(
        self,
        timer_id: int,
        duration_seconds: int,
        callback=None
    ):

        if not isinstance(
            timer_id,
            int
        ):
            raise TypeError(
                "Timer ID must be an integer."
            )

        if timer_id <= 0:
            raise ValueError(
                "Timer ID must be greater than zero."
            )

        if not isinstance(
            duration_seconds,
            (int, float)
        ):
            raise TypeError(
                "Duration must be a number."
            )

        if duration_seconds <= 0:
            raise ValueError(
                "Duration must be greater than zero."
            )

        if callback is not None and not callable(
            callback
        ):
            raise TypeError(
                "Callback must be callable."
            )

        self.timer_id = timer_id
        self.duration_seconds = duration_seconds
        self.callback = callback

        self.status = "created"
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None

        self._timer = None

    def start(self) -> dict:

        if self.status == "running":
            return {
                "success": False,
                "message": "Timer is already running."
            }

        if self.status == "completed":
            return {
                "success": False,
                "message": "Timer has already completed."
            }

        self.status = "running"
        self.started_at = datetime.now()

        self._timer = threading.Timer(
            self.duration_seconds,
            self._complete
        )

        self._timer.daemon = True
        self._timer.start()

        return {
            "success": True,
            "timer_id": self.timer_id,
            "status": self.status,
            "duration_seconds": self.duration_seconds,
            "message": "Timer started successfully."
        }

    def _complete(self) -> None:

        self.status = "completed"
        self.completed_at = datetime.now()

        if self.callback is not None:

            try:
                self.callback(
                    self.timer_id
                )

            except Exception:
                pass

    def cancel(self) -> dict:

        if self._timer is not None:
            self._timer.cancel()

        if self.status == "completed":
            return {
                "success": False,
                "message": "Timer has already completed."
            }

        self.status = "cancelled"

        return {
            "success": True,
            "timer_id": self.timer_id,
            "status": self.status,
            "message": "Timer cancelled successfully."
        }

    def get_status(self) -> dict:

        return {
            "timer_id": self.timer_id,
            "duration_seconds": self.duration_seconds,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "started_at": (
                self.started_at.isoformat()
                if self.started_at
                else None
            ),
            "completed_at": (
                self.completed_at.isoformat()
                if self.completed_at
                else None
            )
        }

    def is_running(self) -> bool:

        return self.status == "running"

    def is_completed(self) -> bool:

        return self.status == "completed"

    def is_cancelled(self) -> bool:

        return self.status == "cancelled"