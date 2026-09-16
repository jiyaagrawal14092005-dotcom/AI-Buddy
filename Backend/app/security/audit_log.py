from datetime import datetime, timezone
from copy import deepcopy


class AuditLogger:
    """
    Records security-related events performed by AI Buddy.

    Audit logs help track:
    - who performed an action
    - what action was requested
    - whether it was allowed or blocked
    - additional details
    - when the event occurred
    """

    VALID_STATUSES = {
        "allowed",
        "blocked",
        "denied",
        "success",
        "failed",
        "pending",
        "approved",
        "rejected",
        "error",
    }

    def __init__(
        self,
        max_logs: int = 1000
    ):
        if not isinstance(max_logs, int) or max_logs < 1:
            raise ValueError(
                "max_logs must be a positive integer."
            )

        self.max_logs = max_logs
        self.logs = []

    # =============================================================
    # TIMESTAMP
    # =============================================================

    def _get_timestamp(self) -> str:
        """
        Return a timezone-aware UTC timestamp.
        """

        return datetime.now(
            timezone.utc
        ).isoformat()

    # =============================================================
    # LOG EVENT
    # =============================================================

    def log(
        self,
        username: str,
        action: str,
        status: str,
        details: dict | None = None
    ) -> dict:
        """
        Record an audit event.
        """

        if not isinstance(
            action,
            str
        ):
            return {
                "success": False,
                "message": "Action must be text."
            }

        action = action.strip()

        if not action:
            return {
                "success": False,
                "message": "Action is required."
            }

        if not isinstance(
            status,
            str
        ):
            return {
                "success": False,
                "message": "Status must be text."
            }

        status = status.strip().lower()

        if not status:
            return {
                "success": False,
                "message": "Status is required."
            }

        # Unknown statuses are still allowed because future
        # AI Buddy modules may introduce new event states.
        if not isinstance(
            details,
            dict
        ) and details is not None:
            return {
                "success": False,
                "message": "Details must be a dictionary."
            }

        if username is None:
            username = "unknown"

        if not isinstance(
            username,
            str
        ):
            username = str(username)

        username = username.strip()

        if not username:
            username = "unknown"

        entry = {
            "log_id": len(self.logs) + 1,
            "username": username,
            "action": action,
            "status": status,
            "details": deepcopy(
                details or {}
            ),
            "timestamp": self._get_timestamp()
        }

        self.logs.append(entry)

        # Keep only the newest max_logs entries.
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)

        return {
            "success": True,
            "log": deepcopy(entry),
            "message": (
                "Audit log recorded successfully."
            )
        }

    # =============================================================
    # GET ALL LOGS
    # =============================================================

    def get_all(
        self
    ) -> list:
        """
        Return a copy of all audit logs.
        """

        return deepcopy(
            self.logs
        )

    # =============================================================
    # GET LOGS BY USER
    # =============================================================

    def get_by_user(
        self,
        username: str
    ) -> list:
        """
        Return all logs belonging to a specific user.
        """

        if not isinstance(
            username,
            str
        ):
            return []

        username = username.strip()

        return [
            deepcopy(log)
            for log in self.logs
            if log["username"] == username
        ]

    # =============================================================
    # GET LOGS BY ACTION
    # =============================================================

    def get_by_action(
        self,
        action: str
    ) -> list:
        """
        Return all logs for a specific action.
        """

        if not isinstance(
            action,
            str
        ):
            return []

        action = action.strip()

        return [
            deepcopy(log)
            for log in self.logs
            if log["action"] == action
        ]

    # =============================================================
    # GET LOGS BY STATUS
    # =============================================================

    def get_by_status(
        self,
        status: str
    ) -> list:
        """
        Return all logs with a specific status.
        """

        if not isinstance(
            status,
            str
        ):
            return []

        status = status.strip().lower()

        return [
            deepcopy(log)
            for log in self.logs
            if log["status"] == status
        ]

    # =============================================================
    # GET LATEST LOGS
    # =============================================================

    def get_latest(
        self,
        limit: int = 10
    ) -> list:
        """
        Return the newest audit events.
        """

        if not isinstance(
            limit,
            int
        ) or limit < 1:
            return []

        return deepcopy(
            self.logs[-limit:]
        )

    # =============================================================
    # CLEAR LOGS
    # =============================================================

    def clear(
        self
    ) -> dict:
        """
        Remove all audit logs.
        """

        self.logs.clear()

        return {
            "success": True,
            "message": (
                "Audit logs cleared successfully."
            )
        }

    # =============================================================
    # COUNT
    # =============================================================

    def count(
        self
    ) -> int:
        """
        Return the number of stored audit events.
        """

        return len(
            self.logs
        )

    # =============================================================
    # STATUS
    # =============================================================

    def get_status(
        self
    ) -> dict:
        """
        Return audit logger status.
        """

        return {
            "name": "audit_log",
            "available": True,
            "enabled": True,
            "log_count": len(
                self.logs
            ),
            "max_logs": self.max_logs,
            "message": (
                "Audit logger is operational."
            )
        }