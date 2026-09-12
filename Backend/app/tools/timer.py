import threading


class TimerTool:

    def __init__(self):
        self.active_timer = None
        self.timer_running = False

    def set_timer(
        self,
        duration_seconds: int
    ) -> dict:

        if not isinstance(duration_seconds, int):
            return {
                "success": False,
                "message": "Timer duration must be an integer."
            }

        if duration_seconds <= 0:
            return {
                "success": False,
                "message": (
                    "Timer duration must be greater "
                    "than 0 seconds."
                )
            }

        # Cancel an existing timer
        if self.active_timer is not None:
            self.active_timer.cancel()

        self.timer_running = True

        self.active_timer = threading.Timer(
            duration_seconds,
            self._timer_finished
        )

        self.active_timer.daemon = True
        self.active_timer.start()

        return {
            "success": True,
            "duration_seconds": duration_seconds,
            "status": "running",
            "message": (
                f"Timer set for "
                f"{duration_seconds} seconds."
            )
        }

    def _timer_finished(self):

        self.timer_running = False
        self.active_timer = None

        print("AI Buddy Timer Finished!")

    def cancel_timer(self) -> dict:

        if self.active_timer is None:
            return {
                "success": False,
                "message": "No active timer found."
            }

        self.active_timer.cancel()

        self.active_timer = None
        self.timer_running = False

        return {
            "success": True,
            "status": "cancelled",
            "message": "Timer cancelled successfully."
        }

    def get_timer_status(self) -> dict:

        if self.timer_running:
            return {
                "success": True,
                "status": "running",
                "message": "Timer is currently running."
            }

        return {
            "success": True,
            "status": "inactive",
            "message": "No timer is currently running."
        }