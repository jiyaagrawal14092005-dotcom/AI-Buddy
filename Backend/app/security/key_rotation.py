import secrets
from datetime import datetime, timezone


class KeyRotationManager:

    def __init__(self):
        self._keys = {}
        self._rotation_history = {}

    def generate_key(
        self,
        key_name: str
    ) -> dict:

        if not key_name:
            return {
                "success": False,
                "message": "Key name is required."
            }

        key_value = secrets.token_urlsafe(32)

        now = datetime.now(
            timezone.utc
        ).isoformat()

        self._keys[key_name] = {
            "key": key_value,
            "created_at": now,
            "status": "active"
        }

        if key_name not in self._rotation_history:
            self._rotation_history[key_name] = []

        self._rotation_history[key_name].append({
            "created_at": now,
            "status": "active"
        })

        return {
            "success": True,
            "key_name": key_name,
            "created_at": now,
            "message": "Security key generated successfully."
        }

    def rotate_key(
        self,
        key_name: str
    ) -> dict:

        if not key_name:
            return {
                "success": False,
                "message": "Key name is required."
            }

        old_key = self._keys.get(key_name)

        if old_key:
            old_key["status"] = "retired"

        key_value = secrets.token_urlsafe(32)

        now = datetime.now(
            timezone.utc
        ).isoformat()

        self._keys[key_name] = {
            "key": key_value,
            "created_at": now,
            "status": "active"
        }

        if key_name not in self._rotation_history:
            self._rotation_history[key_name] = []

        self._rotation_history[key_name].append({
            "created_at": now,
            "status": "active"
        })

        return {
            "success": True,
            "key_name": key_name,
            "created_at": now,
            "message": "Security key rotated successfully."
        }

    def get_key(
        self,
        key_name: str
    ) -> dict:

        if not key_name:
            return {
                "success": False,
                "message": "Key name is required."
            }

        key_data = self._keys.get(key_name)

        if not key_data:
            return {
                "success": False,
                "message": "Key not found."
            }

        if key_data["status"] != "active":
            return {
                "success": False,
                "message": "Key is not active."
            }

        return {
            "success": True,
            "key_name": key_name,
            "key": key_data["key"],
            "created_at": key_data["created_at"],
            "status": key_data["status"]
        }

    def get_rotation_history(
        self,
        key_name: str
    ) -> dict:

        if key_name not in self._rotation_history:
            return {
                "success": False,
                "message": "No rotation history found."
            }

        return {
            "success": True,
            "key_name": key_name,
            "history": self._rotation_history[key_name].copy()
        }

    def remove_key(
        self,
        key_name: str
    ) -> dict:

        if key_name not in self._keys:
            return {
                "success": False,
                "message": "Key not found."
            }

        del self._keys[key_name]

        return {
            "success": True,
            "message": "Key removed successfully."
        }