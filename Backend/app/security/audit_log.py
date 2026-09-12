from datetime import datetime


class AuditLogger:

    def __init__(self, max_logs: int = 1000):

        self.max_logs = max_logs
        self.logs = []

    def log(
        self,
        username: str,
        action: str,
        status: str,
        details: dict | None = None
    ) -> dict:

        if not action:
            return {
                "success": False,
                "message": "Action is required."
            }

        entry = {
            "username": username or "unknown",
            "action": action,
            "status": status,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }

        self.logs.append(entry)

        if len(self.logs) > self.max_logs:
            self.logs.pop(0)

        return {
            "success": True,
            "log": entry,
            "message": "Audit log recorded successfully."
        }

    def get_all(self) -> list:

        return self.logs.copy()

    def get_by_user(
        self,
        username: str
    ) -> list:

        return [
            log.copy()
            for log in self.logs
            if log["username"] == username
        ]

    def get_by_action(
        self,
        action: str
    ) -> list:

        return [
            log.copy()
            for log in self.logs
            if log["action"] == action
        ]

    def clear(self) -> dict:

        self.logs.clear()

        return {
            "success": True,
            "message": "Audit logs cleared successfully."
        }

    def count(self) -> int:

        return len(self.logs)