import re
import secrets
from datetime import datetime, timezone


class KeyRotationManager:

    def __init__(
        self,
        key_length: int = 32
    ):

        if not isinstance(
            key_length,
            int
        ):
            raise TypeError(
                "Key length must be an integer."
            )

        if key_length < 16:
            raise ValueError(
                "Key length must be at least 16 bytes."
            )

        self.key_length = key_length

        self._keys = {}
        self._rotation_history = {}

        self.name = "key_rotation_manager"
        self.enabled = True

    # ---------------------------------------------------------
    # VALIDATE KEY NAME
    # ---------------------------------------------------------

    def _validate_key_name(
        self,
        key_name: str
    ) -> dict:

        if key_name is None:
            return {
                "success": False,
                "message": "Key name is required."
            }

        if not isinstance(
            key_name,
            str
        ):
            return {
                "success": False,
                "message": "Key name must be text."
            }

        key_name = key_name.strip()

        if not key_name:
            return {
                "success": False,
                "message": "Key name cannot be empty."
            }

        if len(key_name) > 100:
            return {
                "success": False,
                "message": "Key name is too long."
            }

        if not re.fullmatch(
            r"[A-Za-z0-9_.-]+",
            key_name
        ):
            return {
                "success": False,
                "message": "Key name contains invalid characters."
            }

        return {
            "success": True,
            "key_name": key_name
        }

    # ---------------------------------------------------------
    # CREATE KEY VALUE
    # ---------------------------------------------------------

    def _generate_key_value(
        self
    ) -> str:

        return secrets.token_urlsafe(
            self.key_length
        )

    # ---------------------------------------------------------
    # GENERATE KEY
    # ---------------------------------------------------------

    def generate_key(
        self,
        key_name: str
    ) -> dict:

        validation = self._validate_key_name(
            key_name
        )

        if not validation["success"]:
            return validation

        key_name = validation["key_name"]

        if key_name in self._keys:
            return {
                "success": False,
                "message": "Key already exists. Use rotate_key() instead."
            }

        key_value = self._generate_key_value()

        now = datetime.now(
            timezone.utc
        ).isoformat()

        self._keys[key_name] = {
            "key": key_value,
            "created_at": now,
            "status": "active"
        }

        self._rotation_history[key_name] = [
            {
                "created_at": now,
                "status": "active"
            }
        ]

        return {
            "success": True,
            "key_name": key_name,
            "created_at": now,
            "status": "active",
            "message": "Security key generated successfully."
        }

    # ---------------------------------------------------------
    # ROTATE KEY
    # ---------------------------------------------------------

    def rotate_key(
        self,
        key_name: str
    ) -> dict:

        validation = self._validate_key_name(
            key_name
        )

        if not validation["success"]:
            return validation

        key_name = validation["key_name"]

        old_key = self._keys.get(
            key_name
        )

        if not old_key:
            return {
                "success": False,
                "message": "Key not found. Generate the key first."
            }

        old_key["status"] = "retired"

        key_value = self._generate_key_value()

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

        self._rotation_history[key_name].append(
            {
                "created_at": now,
                "status": "active"
            }
        )

        return {
            "success": True,
            "key_name": key_name,
            "created_at": now,
            "status": "active",
            "message": "Security key rotated successfully."
        }

    # ---------------------------------------------------------
    # GET ACTIVE KEY
    # ---------------------------------------------------------

    def get_key(
        self,
        key_name: str
    ) -> dict:

        validation = self._validate_key_name(
            key_name
        )

        if not validation["success"]:
            return validation

        key_name = validation["key_name"]

        key_data = self._keys.get(
            key_name
        )

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

    # ---------------------------------------------------------
    # CHECK KEY
    # ---------------------------------------------------------

    def has_key(
        self,
        key_name: str
    ) -> bool:

        validation = self._validate_key_name(
            key_name
        )

        if not validation["success"]:
            return False

        key_name = validation["key_name"]

        return (
            key_name in self._keys
            and self._keys[key_name]["status"] == "active"
        )

    # ---------------------------------------------------------
    # GET ROTATION HISTORY
    # ---------------------------------------------------------

    def get_rotation_history(
        self,
        key_name: str
    ) -> dict:

        validation = self._validate_key_name(
            key_name
        )

        if not validation["success"]:
            return validation

        key_name = validation["key_name"]

        if key_name not in self._rotation_history:
            return {
                "success": False,
                "message": "No rotation history found."
            }

        return {
            "success": True,
            "key_name": key_name,
            "rotation_count": len(
                self._rotation_history[key_name]
            ),
            "history": [
                entry.copy()
                for entry in self._rotation_history[key_name]
            ]
        }

    # ---------------------------------------------------------
    # RETIRE KEY
    # ---------------------------------------------------------

    def retire_key(
        self,
        key_name: str
    ) -> dict:

        validation = self._validate_key_name(
            key_name
        )

        if not validation["success"]:
            return validation

        key_name = validation["key_name"]

        key_data = self._keys.get(
            key_name
        )

        if not key_data:
            return {
                "success": False,
                "message": "Key not found."
            }

        if key_data["status"] != "active":
            return {
                "success": False,
                "message": "Key is already inactive."
            }

        key_data["status"] = "retired"

        now = datetime.now(
            timezone.utc
        ).isoformat()

        if key_name not in self._rotation_history:
            self._rotation_history[key_name] = []

        self._rotation_history[key_name].append(
            {
                "created_at": now,
                "status": "retired"
            }
        )

        return {
            "success": True,
            "key_name": key_name,
            "message": "Security key retired successfully."
        }

    # ---------------------------------------------------------
    # REMOVE KEY
    # ---------------------------------------------------------

    def remove_key(
        self,
        key_name: str
    ) -> dict:

        validation = self._validate_key_name(
            key_name
        )

        if not validation["success"]:
            return validation

        key_name = validation["key_name"]

        if key_name not in self._keys:
            return {
                "success": False,
                "message": "Key not found."
            }

        del self._keys[key_name]

        return {
            "success": True,
            "key_name": key_name,
            "message": "Key removed successfully."
        }

    # ---------------------------------------------------------
    # GET KEY NAMES
    # ---------------------------------------------------------

    def get_key_names(
        self
    ) -> list:

        return list(
            self._keys.keys()
        )

    # ---------------------------------------------------------
    # ACTIVE KEY COUNT
    # ---------------------------------------------------------

    def get_active_key_count(
        self
    ) -> int:

        return sum(
            1
            for key_data in self._keys.values()
            if key_data["status"] == "active"
        )

    # ---------------------------------------------------------
    # TOTAL KEY COUNT
    # ---------------------------------------------------------

    def get_total_key_count(
        self
    ) -> int:

        return len(
            self._keys
        )

    # ---------------------------------------------------------
    # CLEAR KEYS
    # ---------------------------------------------------------

    def clear_keys(
        self
    ) -> dict:

        count = len(
            self._keys
        )

        self._keys.clear()
        self._rotation_history.clear()

        return {
            "success": True,
            "cleared_keys": count,
            "message": "All security keys cleared successfully."
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
            "key_length": self.key_length,
            "total_keys": self.get_total_key_count(),
            "active_keys": self.get_active_key_count(),
            "key_values_exposed": False,
            "message": "Key rotation manager is operational."
        }