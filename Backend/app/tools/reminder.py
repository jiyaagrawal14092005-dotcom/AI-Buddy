from datetime import datetime


class ReminderTool:

    def create_reminder(
        self,
        reminder: str,
        time: str
    ) -> dict:

        # Validate reminder text
        if not reminder:
            return {
                "success": False,
                "message": "Reminder text is required."
            }

        if not isinstance(reminder, str):
            return {
                "success": False,
                "message": "Reminder text must be text."
            }

        reminder = reminder.strip()

        if not reminder:
            return {
                "success": False,
                "message": "Reminder text cannot be empty."
            }

        # Validate reminder time
        if not time:
            return {
                "success": False,
                "message": "Reminder time is required."
            }

        if not isinstance(time, str):
            return {
                "success": False,
                "message": "Reminder time must be text."
            }

        time = time.strip()

        if not time:
            return {
                "success": False,
                "message": "Reminder time cannot be empty."
            }

        # Validate time format
        try:
            reminder_time = datetime.fromisoformat(
                time
            )
        except ValueError:
            return {
                "success": False,
                "message": (
                    "Invalid reminder time format. "
                    "Use ISO format, for example "
                    "'2026-09-15T18:30:00'."
                )
            }

        return {
            "success": True,
            "reminder": reminder,
            "time": reminder_time.isoformat(),
            "status": "pending",
            "message": (
                f"Reminder '{reminder}' "
                f"scheduled for "
                f"{reminder_time.isoformat()}."
            )
        }