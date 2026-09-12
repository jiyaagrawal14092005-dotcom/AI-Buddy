import uuid
from datetime import datetime


class AuthenticationManager:

    def __init__(self):

        self.sessions = {}

    def login(self, username: str) -> dict:

        if not username:
            return {
                "success": False,
                "message": "Username is required."
            }

        session_id = str(uuid.uuid4())

        self.sessions[session_id] = {
            "username": username,
            "login_time": datetime.now().isoformat(),
            "active": True
        }

        return {
            "success": True,
            "session_id": session_id,
            "username": username,
            "message": "Authentication successful."
        }

    def validate_session(
        self,
        session_id: str
    ) -> dict:

        session = self.sessions.get(
            session_id
        )

        if not session:
            return {
                "success": False,
                "authenticated": False,
                "message": "Invalid session."
            }

        if not session["active"]:
            return {
                "success": False,
                "authenticated": False,
                "message": "Session is inactive."
            }

        return {
            "success": True,
            "authenticated": True,
            "username": session["username"],
            "message": "Session is valid."
        }

    def logout(
        self,
        session_id: str
    ) -> dict:

        session = self.sessions.get(
            session_id
        )

        if not session:
            return {
                "success": False,
                "message": "Session not found."
            }

        session["active"] = False

        return {
            "success": True,
            "message": "Logout successful."
        }

    def get_active_sessions(self) -> list:

        return [
            {
                "session_id": session_id,
                "username": session["username"],
                "login_time": session["login_time"]
            }
            for session_id, session
            in self.sessions.items()
            if session["active"]
        ]