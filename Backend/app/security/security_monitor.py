from datetime import datetime, timezone
from copy import deepcopy


class SecurityMonitor:
    """
    Monitors security-related events and generates alerts
    for suspicious or high-severity activity.
    """

    VALID_SEVERITIES = {
        "info",
        "low",
        "medium",
        "high",
        "critical",
    }

    def __init__(
        self,
        max_events: int = 5000,
        max_alerts: int = 2000
    ):
        if not isinstance(max_events, int) or max_events < 1:
            raise ValueError(
                "max_events must be a positive integer."
            )

        if not isinstance(max_alerts, int) or max_alerts < 1:
            raise ValueError(
                "max_alerts must be a positive integer."
            )

        self.max_events = max_events
        self.max_alerts = max_alerts

        self._events = []
        self._alerts = []

        self._suspicious_events = {
            "failed_login",
            "permission_denied",
            "unauthorized_tool",
            "invalid_token",
            "prompt_blocked",
            "rate_limit_exceeded",
            "oauth_failure",
            "security_violation",
            "action_blocked",
            "tool_blocked",
        }

    # =============================================================
    # TIMESTAMP
    # =============================================================

    def _get_timestamp(
        self
    ) -> str:

        return datetime.now(
            timezone.utc
        ).isoformat()

    # =============================================================
    # NORMALIZE SEVERITY
    # =============================================================

    def _normalize_severity(
        self,
        severity: str
    ) -> str:

        if not isinstance(
            severity,
            str
        ):
            return ""

        return severity.strip().lower()

    # =============================================================
    # RECORD EVENT
    # =============================================================

    def record_event(
        self,
        user_id: str,
        event_type: str,
        details: str | dict = "",
        severity: str = "info"
    ) -> dict:
        """
        Record a security event.

        Suspicious event types and high/critical severity
        automatically generate alerts.
        """

        if user_id is None:
            return {
                "success": False,
                "message": "User ID is required."
            }

        if not isinstance(
            user_id,
            str
        ):
            return {
                "success": False,
                "message": "User ID must be text."
            }

        user_id = user_id.strip()

        if not user_id:
            return {
                "success": False,
                "message": "User ID cannot be empty."
            }

        if event_type is None:
            return {
                "success": False,
                "message": "Event type is required."
            }

        if not isinstance(
            event_type,
            str
        ):
            return {
                "success": False,
                "message": "Event type must be text."
            }

        event_type = event_type.strip().lower()

        if not event_type:
            return {
                "success": False,
                "message": "Event type cannot be empty."
            }

        severity = self._normalize_severity(
            severity
        )

        if not severity:
            return {
                "success": False,
                "message": "Severity is required."
            }

        if severity not in self.VALID_SEVERITIES:
            return {
                "success": False,
                "message": "Invalid security severity.",
                "allowed_severities": sorted(
                    self.VALID_SEVERITIES
                )
            }

        if not isinstance(
            details,
            (str, dict)
        ):
            return {
                "success": False,
                "message": (
                    "Event details must be text or dictionary."
                )
            }

        event = {
            "event_id": len(self._events) + 1,
            "user_id": user_id,
            "event_type": event_type,
            "details": deepcopy(details),
            "severity": severity,
            "timestamp": self._get_timestamp()
        }

        self._events.append(
            event
        )

        if len(self._events) > self.max_events:
            self._events.pop(0)

        alert_created = False

        # Suspicious event types automatically create alerts.
        if event_type in self._suspicious_events:
            self._create_alert(
                event,
                reason="suspicious_event"
            )
            alert_created = True

        # High and critical events automatically create alerts.
        if severity in {
            "high",
            "critical"
        }:
            self._create_alert(
                event,
                reason="high_severity"
            )
            alert_created = True

        return {
            "success": True,
            "event": deepcopy(event),
            "alert_created": alert_created,
            "message": "Security event recorded."
        }

    # =============================================================
    # CREATE ALERT
    # =============================================================

    def _create_alert(
        self,
        event: dict,
        reason: str
    ) -> None:
        """
        Create a security alert for an event.
        """

        alert = {
            "alert_id": len(self._alerts) + 1,
            "user_id": event["user_id"],
            "event_id": event["event_id"],
            "event_type": event["event_type"],
            "severity": event["severity"],
            "reason": reason,
            "timestamp": event["timestamp"],
            "message": (
                "Suspicious security activity detected."
            )
        }

        self._alerts.append(
            alert
        )

        if len(self._alerts) > self.max_alerts:
            self._alerts.pop(0)

    # =============================================================
    # GET EVENTS
    # =============================================================

    def get_events(
        self,
        user_id: str | None = None
    ) -> list:

        if user_id is None:
            return deepcopy(
                self._events
            )

        if not isinstance(
            user_id,
            str
        ):
            return []

        user_id = user_id.strip()

        return [
            deepcopy(event)
            for event in self._events
            if event["user_id"] == user_id
        ]

    # =============================================================
    # GET ALERTS
    # =============================================================

    def get_alerts(
        self,
        user_id: str | None = None
    ) -> list:

        if user_id is None:
            return deepcopy(
                self._alerts
            )

        if not isinstance(
            user_id,
            str
        ):
            return []

        user_id = user_id.strip()

        return [
            deepcopy(alert)
            for alert in self._alerts
            if alert["user_id"] == user_id
        ]

    # =============================================================
    # GET ALERTS BY SEVERITY
    # =============================================================

    def get_alerts_by_severity(
        self,
        severity: str
    ) -> list:

        severity = self._normalize_severity(
            severity
        )

        if severity not in self.VALID_SEVERITIES:
            return []

        return [
            deepcopy(alert)
            for alert in self._alerts
            if alert["severity"] == severity
        ]

    # =============================================================
    # GET EVENTS BY TYPE
    # =============================================================

    def get_events_by_type(
        self,
        event_type: str
    ) -> list:

        if not isinstance(
            event_type,
            str
        ):
            return []

        event_type = event_type.strip().lower()

        if not event_type:
            return []

        return [
            deepcopy(event)
            for event in self._events
            if event["event_type"] == event_type
        ]

    # =============================================================
    # SECURITY STATUS
    # =============================================================

    def get_security_status(
        self,
        user_id: str
    ) -> dict:
        """
        Calculate the security status for a user.
        """

        if not isinstance(
            user_id,
            str
        ) or not user_id.strip():
            return {
                "success": False,
                "message": "User ID is required."
            }

        user_id = user_id.strip()

        events = self.get_events(
            user_id
        )

        alerts = self.get_alerts(
            user_id
        )

        critical_alerts = [
            alert
            for alert in alerts
            if alert["severity"] == "critical"
        ]

        high_alerts = [
            alert
            for alert in alerts
            if alert["severity"] == "high"
        ]

        medium_alerts = [
            alert
            for alert in alerts
            if alert["severity"] == "medium"
        ]

        if critical_alerts:
            status = "critical"

        elif high_alerts:
            status = "warning"

        elif medium_alerts:
            status = "elevated"

        elif alerts:
            status = "suspicious"

        else:
            status = "normal"

        return {
            "success": True,
            "user_id": user_id,
            "status": status,
            "total_events": len(events),
            "total_alerts": len(alerts),
            "critical_alerts": len(
                critical_alerts
            ),
            "high_alerts": len(
                high_alerts
            ),
            "medium_alerts": len(
                medium_alerts
            )
        }

    # =============================================================
    # GET MONITORING SUMMARY
    # =============================================================

    def get_summary(
        self
    ) -> dict:

        severity_counts = {
            severity: len(
                self.get_alerts_by_severity(
                    severity
                )
            )
            for severity
            in self.VALID_SEVERITIES
        }

        return {
            "success": True,
            "total_events": len(
                self._events
            ),
            "total_alerts": len(
                self._alerts
            ),
            "alerts_by_severity": severity_counts,
            "max_events": self.max_events,
            "max_alerts": self.max_alerts
        }

    # =============================================================
    # CLEAR MONITORING DATA
    # =============================================================

    def clear_events(
        self
    ) -> dict:

        self._events.clear()
        self._alerts.clear()

        return {
            "success": True,
            "message": (
                "Security monitoring data cleared."
            )
        }

    # =============================================================
    # STATUS
    # =============================================================

    def get_status(
        self
    ) -> dict:

        return {
            "name": "security_monitor",
            "available": True,
            "enabled": True,
            "total_events": len(
                self._events
            ),
            "total_alerts": len(
                self._alerts
            ),
            "suspicious_event_types": sorted(
                self._suspicious_events
            ),
            "severity_levels": sorted(
                self.VALID_SEVERITIES
            ),
            "message": (
                "Security monitor is operational."
            )
        }