from datetime import datetime, timezone


class SecurityMonitor:

    def __init__(self):
        self._events = []
        self._alerts = []

        self._suspicious_events = {
            "failed_login",
            "permission_denied",
            "unauthorized_tool",
            "invalid_token",
            "prompt_blocked",
            "rate_limit_exceeded",
            "oauth_failure"
        }

    def record_event(
        self,
        user_id: str,
        event_type: str,
        details: str = "",
        severity: str = "info"
    ) -> dict:

        if not user_id:
            return {
                "success": False,
                "message": "User ID is required."
            }

        if not event_type:
            return {
                "success": False,
                "message": "Event type is required."
            }

        event = {
            "user_id": user_id,
            "event_type": event_type,
            "details": details,
            "severity": severity,
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat()
        }

        self._events.append(event)

        if event_type in self._suspicious_events:
            self._create_alert(event)

        if severity.lower() in {
            "high",
            "critical"
        }:
            self._create_alert(event)

        return {
            "success": True,
            "event": event,
            "message": "Security event recorded."
        }

    def _create_alert(
        self,
        event: dict
    ) -> None:

        alert = {
            "user_id": event["user_id"],
            "event_type": event["event_type"],
            "severity": event["severity"],
            "timestamp": event["timestamp"],
            "message": "Suspicious security activity detected."
        }

        self._alerts.append(alert)

    def get_events(
        self,
        user_id: str | None = None
    ) -> list:

        if user_id is None:
            return self._events.copy()

        return [
            event
            for event in self._events
            if event["user_id"] == user_id
        ]

    def get_alerts(
        self,
        user_id: str | None = None
    ) -> list:

        if user_id is None:
            return self._alerts.copy()

        return [
            alert
            for alert in self._alerts
            if alert["user_id"] == user_id
        ]

    def get_security_status(
        self,
        user_id: str
    ) -> dict:

        events = self.get_events(user_id)
        alerts = self.get_alerts(user_id)

        critical_alerts = [
            alert
            for alert in alerts
            if alert["severity"].lower()
            == "critical"
        ]

        high_alerts = [
            alert
            for alert in alerts
            if alert["severity"].lower()
            == "high"
        ]

        if critical_alerts:
            status = "critical"
        elif high_alerts:
            status = "warning"
        elif alerts:
            status = "suspicious"
        else:
            status = "normal"

        return {
            "success": True,
            "user_id": user_id,
            "status": status,
            "total_events": len(events),
            "total_alerts": len(alerts)
        }

    def clear_events(
        self
    ) -> dict:

        self._events.clear()
        self._alerts.clear()

        return {
            "success": True,
            "message": "Security monitoring data cleared."
        }