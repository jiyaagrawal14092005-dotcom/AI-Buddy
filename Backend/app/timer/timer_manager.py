from app.timer.timer import Timer


class TimerManager:

    def __init__(self):

        self.timers = {}
        self.next_timer_id = 1

    def create_timer(
        self,
        duration_seconds: int,
        callback=None
    ) -> dict:

        if not isinstance(
            duration_seconds,
            (int, float)
        ):
            return {
                "success": False,
                "message": "Duration must be a number."
            }

        if duration_seconds <= 0:
            return {
                "success": False,
                "message": (
                    "Duration must be greater than zero."
                )
            }

        timer_id = self.next_timer_id

        self.next_timer_id += 1

        timer = Timer(
            timer_id=timer_id,
            duration_seconds=duration_seconds,
            callback=callback
        )

        self.timers[timer_id] = timer

        return {
            "success": True,
            "timer_id": timer_id,
            "status": timer.status,
            "message": "Timer created successfully."
        }

    def start_timer(
        self,
        timer_id: int
    ) -> dict:

        timer = self.timers.get(
            timer_id
        )

        if timer is None:
            return {
                "success": False,
                "message": "Timer not found."
            }

        return timer.start()

    def cancel_timer(
        self,
        timer_id: int
    ) -> dict:

        timer = self.timers.get(
            timer_id
        )

        if timer is None:
            return {
                "success": False,
                "message": "Timer not found."
            }

        return timer.cancel()

    def get_timer(
        self,
        timer_id: int
    ) -> dict:

        timer = self.timers.get(
            timer_id
        )

        if timer is None:
            return {
                "success": False,
                "message": "Timer not found."
            }

        return {
            "success": True,
            "timer": timer.get_status()
        }

    def get_all_timers(self) -> list:

        return [
            timer.get_status()
            for timer in self.timers.values()
        ]

    def remove_timer(
        self,
        timer_id: int
    ) -> dict:

        timer = self.timers.get(
            timer_id
        )

        if timer is None:
            return {
                "success": False,
                "message": "Timer not found."
            }

        if timer.is_running():

            timer.cancel()

        del self.timers[timer_id]

        return {
            "success": True,
            "timer_id": timer_id,
            "message": "Timer removed successfully."
        }

    def clear_all(self) -> None:

        for timer in self.timers.values():

            if timer.is_running():
                timer.cancel()

        self.timers.clear()

    def get_active_count(self) -> int:

        return sum(
            1
            for timer in self.timers.values()
            if timer.is_running()
        )

    def get_count(self) -> int:

        return len(
            self.timers
        )