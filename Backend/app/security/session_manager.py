import secrets
from datetime import datetime, timedelta, timezone


class SessionManager:

    def __init__(
        self,
        session_timeout_minutes: int = 60
    ):

        if not isinstance(
            session_timeout_minutes,
            int
        ):
            raise TypeError(
                "Session timeout must be an integer."
            )

        if session_timeout_minutes <= 0:
            raise ValueError(
                "Session timeout must be greater than zero."
            )

        self.session_timeout_minutes = (
            session_timeout_minutes
        )

        self.session_timeout = timedelta(
            minutes=session_timeout_minutes
        )

        self._sessions = {}

        self.name = "session_manager"
        self.enabled = True

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def _validate_user_id(
        self,
        user_id: str
    ) -> dict:

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

        if len(user_id) > 100:
            return {
                "success": False,
                "message": "User ID is too long."
            }

        return {
            "success": True,
            "user_id": user_id
        }

    def _validate_session_id(
        self,
        session_id: str
    ) -> dict:

        if session_id is None:
            return {
                "success": False,
                "message": "Session ID is required."
            }

        if not isinstance(
            session_id,
            str
        ):
            return {
                "success": False,
                "message": "Session ID must be text."
            }

        session_id = session_id.strip()

        if not session_id:
            return {
                "success": False,
                "message": "Session ID cannot be empty."
            }

        return {
            "success": True,
            "session_id": session_id
        }

    # ---------------------------------------------------------
    # CREATE SESSION
    # ---------------------------------------------------------

    def create_session(
        self,
        user_id: str
    ) -> dict:

        validation = self._validate_user_id(
            user_id
        )

        if not validation["success"]:
            return validation

        user_id = validation["user_id"]

        session_id = secrets.token_urlsafe(32)

        now = datetime.now(
            timezone.utc
        )

        expires_at = (
            now + self.session_timeout
        )

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

    # ---------------------------------------------------------
    # GET SESSION
    # ---------------------------------------------------------

    def get_session(
        self,
        session_id: str
    ) -> dict:

        validation = self._validate_session_id(
            session_id
        )

        if not validation["success"]:
            return validation

        session_id = validation["session_id"]

        session = self._sessions.get(
            session_id
        )

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
            "session": {
                "user_id": session["user_id"],
                "created_at": session["created_at"].isoformat(),
                "last_activity": session[
                    "last_activity"
                ].isoformat(),
                "expires_at": session[
                    "expires_at"
                ].isoformat(),
                "active": session["active"]
            }
        }

    # ---------------------------------------------------------
    # UPDATE ACTIVITY
    # ---------------------------------------------------------

    def update_activity(
        self,
        session_id: str
    ) -> dict:

        result = self.get_session(
            session_id
        )

        if not result["success"]:
            return result

        now = datetime.now(
            timezone.utc
        )

        session = self._sessions[
            session_id
        ]

        session["last_activity"] = now

        session["expires_at"] = (
            now + self.session_timeout
        )

        return {
            "success": True,
            "expires_at": session[
                "expires_at"
            ].isoformat(),
            "message": "Session activity updated."
        }

    # ---------------------------------------------------------
    # VALIDATE SESSION
    # ---------------------------------------------------------

    def validate_session(
        self,
        session_id: str,
        user_id: str
    ) -> bool:

        session_validation = (
            self._validate_session_id(
                session_id
            )
        )

        if not session_validation["success"]:
            return False

        user_validation = (
            self._validate_user_id(
                user_id
            )
        )

        if not user_validation["success"]:
            return False

        result = self.get_session(
            session_validation["session_id"]
        )

        if not result["success"]:
            return False

        session = result["session"]

        return (
            session["user_id"]
            == user_validation["user_id"]
        )

    # ---------------------------------------------------------
    # REVOKE SESSION
    # ---------------------------------------------------------

    def revoke_session(
        self,
        session_id: str
    ) -> dict:

        validation = self._validate_session_id(
            session_id
        )

        if not validation["success"]:
            return validation

        session_id = validation["session_id"]

        if session_id not in self._sessions:
            return {
                "success": False,
                "message": "Session not found."
            }

        session = self._sessions[
            session_id
        ]

        if not session["active"]:
            return {
                "success": False,
                "message": "Session is already inactive."
            }

        session["active"] = False

        return {
            "success": True,
            "message": "Session revoked successfully."
        }

    # ---------------------------------------------------------
    # REVOKE ALL USER SESSIONS
    # ---------------------------------------------------------

    def revoke_user_sessions(
        self,
        user_id: str
    ) -> dict:

        validation = self._validate_user_id(
            user_id
        )

        if not validation["success"]:
            return validation

        user_id = validation["user_id"]

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

    # ---------------------------------------------------------
    # CLEAN EXPIRED SESSIONS
    # ---------------------------------------------------------

    def cleanup_expired_sessions(
        self
    ) -> dict:

        expired_count = 0

        for session in self._sessions.values():

            if (
                session["active"]
                and self._is_expired(session)
            ):

                session["active"] = False
                expired_count += 1

        return {
            "success": True,
            "expired_sessions": expired_count,
            "message": "Expired sessions cleaned successfully."
        }

    # ---------------------------------------------------------
    # SESSION EXISTS
    # ---------------------------------------------------------

    def session_exists(
        self,
        session_id: str
    ) -> bool:

        validation = self._validate_session_id(
            session_id
        )

        if not validation["success"]:
            return False

        session_id = validation["session_id"]

        return session_id in self._sessions

    # ---------------------------------------------------------
    # SESSION ACTIVE
    # ---------------------------------------------------------

    def is_session_active(
        self,
        session_id: str
    ) -> bool:

        result = self.get_session(
            session_id
        )

        return result["success"]

    # ---------------------------------------------------------
    # USER SESSION COUNT
    # ---------------------------------------------------------

    def get_user_session_count(
        self,
        user_id: str
    ) -> int:

        validation = self._validate_user_id(
            user_id
        )

        if not validation["success"]:
            return 0

        user_id = validation["user_id"]

        count = 0

        for session in self._sessions.values():

            if (
                session["user_id"] == user_id
                and session["active"]
                and not self._is_expired(session)
            ):
                count += 1

        return count

    # ---------------------------------------------------------
    # ACTIVE SESSION COUNT
    # ---------------------------------------------------------

    def get_active_session_count(
        self
    ) -> int:

        count = 0

        for session in self._sessions.values():

            if (
                session["active"]
                and not self._is_expired(session)
            ):
                count += 1

        return count

    # ---------------------------------------------------------
    # TOTAL SESSION COUNT
    # ---------------------------------------------------------

    def get_total_session_count(
        self
    ) -> int:

        return len(
            self._sessions
        )

    # ---------------------------------------------------------
    # CLEAR SESSIONS
    # ---------------------------------------------------------

    def clear_sessions(
        self
    ) -> dict:

        count = len(
            self._sessions
        )

        self._sessions.clear()

        return {
            "success": True,
            "cleared_sessions": count,
            "message": "All sessions cleared successfully."
        }

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def get_status(
        self
    ) -> dict:

        return {
            "name": self.name,
            "available": True,
            "enabled": self.enabled,
            "session_timeout_minutes": (
                self.session_timeout_minutes
            ),
            "total_sessions": (
                self.get_total_session_count()
            ),
            "active_sessions": (
                self.get_active_session_count()
            ),
            "message": "Session manager is operational."
        }

    # ---------------------------------------------------------
    # EXPIRATION CHECK
    # ---------------------------------------------------------

    def _is_expired(
        self,
        session: dict
    ) -> bool:

        now = datetime.now(
            timezone.utc
        )

        return now >= session["expires_at"]