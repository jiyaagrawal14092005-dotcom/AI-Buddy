import secrets
from datetime import datetime, timedelta, timezone


class SessionManager:

    def __init__(self, session_timeout_minutes: int = 60):
        self.session_timeout = timedelta(
            minutes=session_timeout_minutes
        )

        self._sessions = {}

    def create_session(
        self,
        user_id: str
    ) -> dict:

        if not user_id:
            return {
                "success": False,
                "message": "User ID is required."
            }

        session_id = secrets.token_urlsafe(32)

        now = datetime.now(timezone.utc)
        expires_at = now + self.session_timeout

        self._sessions[session_id] = {
            "user_id": user_id,
            "created_at": now,
            "last_activity": now,
            "expires_at": expires_at,
            "active": True
        }

        return {
            "success": True,
            "session_id": session_id,
            "user_id": user_id,
            "expires_at": expires_at.isoformat(),
            "message": "Session created successfully."
        }

    def get_session(
        self,
        session_id: str
    ) -> dict:

        if not session_id:
            return {
                "success": False,
                "message": "Session ID is required."
            }

        session = self._sessions.get(session_id)

        if not session:
            return {
                "success": False,
                "message": "Session not found."
            }

        if self._is_expired(session):
            session["active"] = False

            return {
                "success": False,
                "message": "Session has expired."
            }

        if not session["active"]:
            return {
                "success": False,
                "message": "Session is inactive."
            }

        return {
            "success": True,
            "session": session
        }

    def update_activity(
        self,
        session_id: str
    ) -> dict:

        result = self.get_session(session_id)

        if not result["success"]:
            return result

        now = datetime.now(timezone.utc)

        session = self._sessions[session_id]

        session["last_activity"] = now
        session["expires_at"] = now + self.session_timeout

        return {
            "success": True,
            "message": "Session activity updated.",
            "expires_at": session["expires_at"].isoformat()
        }

    def validate_session(
        self,
        session_id: str,
        user_id: str
    ) -> bool:

        result = self.get_session(session_id)

        if not result["success"]:
            return False

        session = result["session"]

        return session["user_id"] == user_id

    def revoke_session(
        self,
        session_id: str
    ) -> dict:

        if session_id not in self._sessions:
            return {
                "success": False,
                "message": "Session not found."
            }

        self._sessions[session_id]["active"] = False

        return {
            "success": True,
            "message": "Session revoked successfully."
        }

    def revoke_user_sessions(
        self,
        user_id: str
    ) -> dict:

        if not user_id:
            return {
                "success": False,
                "message": "User ID is required."
            }

        count = 0

        for session in self._sessions.values():

            if (
                session["user_id"] == user_id
                and session["active"]
            ):
                session["active"] = False
                count += 1

        return {
            "success": True,
            "revoked_sessions": count,
            "message": "User sessions revoked successfully."
        }

    def _is_expired(
        self,
        session: dict
    ) -> bool:

        now = datetime.now(timezone.utc)

        return now >= session["expires_at"]