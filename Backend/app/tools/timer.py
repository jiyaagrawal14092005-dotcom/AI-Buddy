from app.timer.timer_manager import TimerManager


class TimerTool:

    def __init__(self):
        self.timer_manager = TimerManager()

    def set_timer(
        self,
        duration_seconds: int,
        focus_mode: bool = False
    ) -> dict:

        if not isinstance(
            duration_seconds,
            (int, float)
        ):
            return {
                "success": False,
                "message": "Timer duration must be a number."
            }

        if duration_seconds <= 0:
            return {
                "success": False,
                "message": (
                    "Timer duration must be "
                    "greater than 0 seconds."
                )
            }

        timer_result = (
            self.timer_manager.create_timer(
                duration_seconds=duration_seconds
            )
        )

        if not timer_result.get("success"):
            return timer_result

        timer_id = timer_result.get(
            "timer_id"
        )

        # -----------------------------------------
        # Store Focus Mode information
        # -----------------------------------------

        timer = self.timer_manager.timers.get(
            timer_id
        )

        if timer is not None:
            timer.focus_mode = bool(
                focus_mode
            )

        # -----------------------------------------
        # Start timer
        # -----------------------------------------

        start_result = (
            self.timer_manager.start_timer(
                timer_id=timer_id
            )
        )

        if not start_result.get("success"):
            return start_result

        if focus_mode:

            return {
                "success": True,
                "timer_id": timer_id,
                "duration_seconds": duration_seconds,
                "status": "running",
                "focus_mode": True,
                "message": (
                    "Focus Mode started "
                    f"for {duration_seconds} seconds."
                ),
                "notification": (
                    "Focus Mode started "
                    f"for {duration_seconds} seconds."
                )
            }

        return {
            "success": True,
            "timer_id": timer_id,
            "duration_seconds": duration_seconds,
            "status": "running",
            "focus_mode": False,
            "message": (
                f"Timer set for "
                f"{duration_seconds} seconds."
            )
        }

    def cancel_timer(
        self,
        timer_id: int
    ) -> dict:

        if not isinstance(
            timer_id,
            int
        ):
            return {
                "success": False,
                "message": (
                    "Timer ID must be an integer."
                )
            }

        return self.timer_manager.cancel_timer(
            timer_id=timer_id
        )

    def get_timer_status(
        self,
        timer_id: int
    ) -> dict:

        if not isinstance(
            timer_id,
            int
        ):
            return {
                "success": False,
                "message": (
                    "Timer ID must be an integer."
                )
            }

        return self.timer_manager.get_timer(
            timer_id=timer_id
        )

    def get_all_timers(self) -> dict:

        return {
            "success": True,
            "timers": (
                self.timer_manager
                .get_all_timers()
            )
        }

    def get_active_count(self) -> dict:

        return {
            "success": True,
            "active_timers": (
                self.timer_manager
                .get_active_count()
            )
        }

    def get_count(self) -> dict:

        return {
            "success": True,
            "total_timers": (
                self.timer_manager
                .get_count()
            )
        }

    def remove_timer(
        self,
        timer_id: int
    ) -> dict:

        if not isinstance(
            timer_id,
            int
        ):
            return {
                "success": False,
                "message": (
                    "Timer ID must be an integer."
                )
            }

        return self.timer_manager.remove_timer(
            timer_id=timer_id
        )

    def clear_all_timers(self) -> dict:

        self.timer_manager.clear_all()

        return {
            "success": True,
            "message": (
                "All timers cleared successfully."
            )
        }