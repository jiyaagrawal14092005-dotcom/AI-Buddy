import uuid
from datetime import datetime


class IdentityManager:

    def __init__(self):

        self.users = {}

    def create_identity(
        self,
        username: str
    ) -> dict:

        if not username:
            return {
                "success": False,
                "message": "Username is required."
            }

        if username in self.users:

            return {
                "success": False,
                "message": "User identity already exists."
            }

        user_id = str(uuid.uuid4())

        identity = {
            "user_id": user_id,
            "username": username,
            "created_at": datetime.now().isoformat(),
            "active": True
        }

        self.users[username] = identity

        return {
            "success": True,
            "user_id": user_id,
            "username": username,
            "message": "User identity created successfully."
        }

    def get_identity(
        self,
        username: str
    ) -> dict:

        identity = self.users.get(username)

        if not identity:

            return {
                "success": False,
                "message": "User identity not found."
            }

        return {
            "success": True,
            "identity": identity.copy()
        }

    def get_user_by_id(
        self,
        user_id: str
    ) -> dict:

        for identity in self.users.values():

            if identity["user_id"] == user_id:

                return {
                    "success": True,
                    "identity": identity.copy()
                }

        return {
            "success": False,
            "message": "User identity not found."
        }

    def deactivate_user(
        self,
        user_id: str
    ) -> dict:

        for identity in self.users.values():

            if identity["user_id"] == user_id:

                identity["active"] = False

                return {
                    "success": True,
                    "message": "User identity deactivated."
                }

        return {
            "success": False,
            "message": "User identity not found."
        }

    def activate_user(
        self,
        user_id: str
    ) -> dict:

        for identity in self.users.values():

            if identity["user_id"] == user_id:

                identity["active"] = True

                return {
                    "success": True,
                    "message": "User identity activated."
                }

        return {
            "success": False,
            "message": "User identity not found."
        }

    def is_active(
        self,
        user_id: str
    ) -> bool:

        for identity in self.users.values():

            if identity["user_id"] == user_id:

                return identity["active"]

        return False