import uuid
from datetime import datetime, timezone
from copy import deepcopy


class IdentityManager:
    """
    Manages user identities for AI Buddy.

    Responsibilities:
    - Create unique user identities
    - Resolve username to user ID
    - Resolve user ID to username
    - Activate/deactivate identities
    - Check identity status
    - Prevent duplicate usernames
    """

    def __init__(self):
        self.users = {}

    # =============================================================
    # TIMESTAMP
    # =============================================================

    def _get_timestamp(self) -> str:
        return datetime.now(
            timezone.utc
        ).isoformat()

    # =============================================================
    # NORMALIZE USERNAME
    # =============================================================

    def _normalize_username(
        self,
        username: str
    ) -> str:

        if not isinstance(
            username,
            str
        ):
            return ""

        return username.strip()

    # =============================================================
    # CREATE IDENTITY
    # =============================================================

    def create_identity(
        self,
        username: str
    ) -> dict:

        username = self._normalize_username(
            username
        )

        if not username:
            return {
                "success": False,
                "message": "Username is required."
            }

        if len(username) > 100:
            return {
                "success": False,
                "message": "Username is too long."
            }

        if username in self.users:
            return {
                "success": False,
                "message": (
                    "User identity already exists."
                )
            }

        user_id = str(
            uuid.uuid4()
        )

        identity = {
            "user_id": user_id,
            "username": username,
            "created_at": self._get_timestamp(),
            "updated_at": self._get_timestamp(),
            "active": True
        }

        self.users[username] = identity

        return {
            "success": True,
            "user_id": user_id,
            "username": username,
            "message": (
                "User identity created successfully."
            )
        }

    # =============================================================
    # GET IDENTITY BY USERNAME
    # =============================================================

    def get_identity(
        self,
        username: str
    ) -> dict:

        username = self._normalize_username(
            username
        )

        if not username:
            return {
                "success": False,
                "message": "Username is required."
            }

        identity = self.users.get(
            username
        )

        if not identity:
            return {
                "success": False,
                "message": (
                    "User identity not found."
                )
            }

        return {
            "success": True,
            "identity": deepcopy(
                identity
            )
        }

    # =============================================================
    # GET USER BY ID
    # =============================================================

    def get_user_by_id(
        self,
        user_id: str
    ) -> dict:

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
                "message": "User ID is required."
            }

        for identity in self.users.values():

            if identity["user_id"] == user_id:

                return {
                    "success": True,
                    "identity": deepcopy(
                        identity
                    )
                }

        return {
            "success": False,
            "message": (
                "User identity not found."
            )
        }

    # =============================================================
    # GET USERNAME BY ID
    # =============================================================

    def get_username(
        self,
        user_id: str
    ) -> dict:

        result = self.get_user_by_id(
            user_id
        )

        if not result["success"]:
            return result

        identity = result["identity"]

        return {
            "success": True,
            "user_id": user_id,
            "username": identity["username"],
            "message": (
                "Username resolved successfully."
            )
        }

    # =============================================================
    # GET USER ID BY USERNAME
    # =============================================================

    def get_user_id(
        self,
        username: str
    ) -> dict:

        result = self.get_identity(
            username
        )

        if not result["success"]:
            return result

        identity = result["identity"]

        return {
            "success": True,
            "username": identity["username"],
            "user_id": identity["user_id"],
            "message": (
                "User ID resolved successfully."
            )
        }

    # =============================================================
    # DEACTIVATE USER
    # =============================================================

    def deactivate_user(
        self,
        user_id: str
    ) -> dict:

        result = self.get_user_by_id(
            user_id
        )

        if not result["success"]:
            return result

        username = result["identity"]["username"]

        identity = self.users[
            username
        ]

        identity["active"] = False
        identity["updated_at"] = self._get_timestamp()

        return {
            "success": True,
            "user_id": user_id,
            "username": username,
            "active": False,
            "message": (
                "User identity deactivated."
            )
        }

    # =============================================================
    # ACTIVATE USER
    # =============================================================

    def activate_user(
        self,
        user_id: str
    ) -> dict:

        result = self.get_user_by_id(
            user_id
        )

        if not result["success"]:
            return result

        username = result["identity"]["username"]

        identity = self.users[
            username
        ]

        identity["active"] = True
        identity["updated_at"] = self._get_timestamp()

        return {
            "success": True,
            "user_id": user_id,
            "username": username,
            "active": True,
            "message": (
                "User identity activated."
            )
        }

    # =============================================================
    # CHECK ACTIVE STATUS
    # =============================================================

    def is_active(
        self,
        user_id: str
    ) -> bool:

        result = self.get_user_by_id(
            user_id
        )

        if not result["success"]:
            return False

        return bool(
            result["identity"]["active"]
        )

    # =============================================================
    # CHECK IDENTITY
    # =============================================================

    def identity_exists(
        self,
        user_id: str
    ) -> bool:

        return self.get_user_by_id(
            user_id
        )["success"]

    # =============================================================
    # GET ALL IDENTITIES
    # =============================================================

    def get_all_identities(
        self
    ) -> list:

        return [
            deepcopy(identity)
            for identity in self.users.values()
        ]

    # =============================================================
    # GET ACTIVE IDENTITIES
    # =============================================================

    def get_active_identities(
        self
    ) -> list:

        return [
            deepcopy(identity)
            for identity in self.users.values()
            if identity["active"]
        ]

    # =============================================================
    # GET IDENTITY COUNT
    # =============================================================

    def count(self) -> int:

        return len(
            self.users
        )

    # =============================================================
    # STATUS
    # =============================================================

    def get_status(
        self
    ) -> dict:

        active_count = sum(
            1
            for identity in self.users.values()
            if identity["active"]
        )

        return {
            "name": "identity",
            "available": True,
            "enabled": True,
            "total_identities": len(
                self.users
            ),
            "active_identities": active_count,
            "inactive_identities": (
                len(self.users) - active_count
            ),
            "message": (
                "Identity manager is operational."
            )
        }