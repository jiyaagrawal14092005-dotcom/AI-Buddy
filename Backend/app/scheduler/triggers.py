from datetime import datetime, timedelta


class TriggerManager:

    # ---------------------------------
    # CREATE DELAY TRIGGER
    # ---------------------------------

    def create_delay_trigger(
        self,
        delay_seconds: int
    ) -> dict:

        if not isinstance(delay_seconds, (int, float)):
            return {
                "success": False,
                "message": "Delay must be a number."
            }

        if delay_seconds <= 0:
            return {
                "success": False,
                "message": (
                    "Delay must be greater than 0 seconds."
                )
            }

        trigger_at = (
            datetime.now()
            + timedelta(seconds=delay_seconds)
        )

        return {
            "success": True,
            "type": "DELAY",
            "delay_seconds": delay_seconds,
            "trigger_at": trigger_at.isoformat(),
            "message": (
                f"Delay trigger created for "
                f"{delay_seconds} seconds."
            )
        }

    # ---------------------------------
    # CREATE TIME TRIGGER
    # ---------------------------------

    def create_time_trigger(
        self,
        target_time: str
    ) -> dict:

        if not isinstance(target_time, str):
            return {
                "success": False,
                "message": "Target time must be text."
            }

        target_time = target_time.strip()

        if not target_time:
            return {
                "success": False,
                "message": "Target time cannot be empty."
            }

        try:

            target = datetime.fromisoformat(
                target_time
            )

        except (ValueError, TypeError):

            return {
                "success": False,
                "message": (
                    "Invalid time format. "
                    "Use ISO format."
                )
            }

        now = datetime.now()

        delay_seconds = (
            target - now
        ).total_seconds()

        if delay_seconds <= 0:
            return {
                "success": False,
                "message": (
                    "Target time must be in the future."
                )
            }

        return {
            "success": True,
            "type": "AT_TIME",
            "target_time": target.isoformat(),
            "delay_seconds": round(
                delay_seconds
            ),
            "message": (
                "Time trigger created successfully."
            )
        }

    # ---------------------------------
    # CREATE INTERVAL TRIGGER
    # ---------------------------------

    def create_interval_trigger(
        self,
        interval_seconds: int
    ) -> dict:

        if not isinstance(interval_seconds, (int, float)):
            return {
                "success": False,
                "message": "Interval must be a number."
            }

        if interval_seconds <= 0:
            return {
                "success": False,
                "message": (
                    "Interval must be greater than 0 seconds."
                )
            }

        return {
            "success": True,
            "type": "INTERVAL",
            "interval_seconds": interval_seconds,
            "message": (
                f"Interval trigger created for "
                f"every {interval_seconds} seconds."
            )
        }