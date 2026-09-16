from copy import deepcopy
import re


class DataIsolationManager:
    """
    Provides user-level data isolation.

    Every data item is stored under:
        user_id -> data_type -> data_id

    This prevents one user's data from being accessed
    through another user's data scope.
    """

    def __init__(self):
        self.user_data = {}

    # =============================================================
    # VALIDATION
    # =============================================================

    def _validate_identifier(
        self,
        value: str,
        name: str
    ) -> dict:

        if value is None:
            return {
                "valid": False,
                "message": f"{name} is required."
            }

        if not isinstance(
            value,
            str
        ):
            return {
                "valid": False,
                "message": f"{name} must be text."
            }

        value = value.strip()

        if not value:
            return {
                "valid": False,
                "message": f"{name} cannot be empty."
            }

        if not re.fullmatch(
            r"[A-Za-z0-9_.:-]{1,200}",
            value
        ):
            return {
                "valid": False,
                "message": f"Invalid {name} format."
            }

        return {
            "valid": True,
            "sanitized": value
        }

    # =============================================================
    # CREATE USER STORE
    # =============================================================

    def create_user_store(
        self,
        user_id: str
    ) -> dict:

        validation = self._validate_identifier(
            user_id,
            "User ID"
        )

        if not validation["valid"]:
            return validation

        user_id = validation["sanitized"]

        if user_id not in self.user_data:
            self.user_data[user_id] = {}

        return {
            "success": True,
            "user_id": user_id,
            "message": (
                "User data store created successfully."
            )
        }

    # =============================================================
    # SAVE DATA
    # =============================================================

    def save_data(
        self,
        user_id: str,
        data_type: str,
        data_id: str,
        data
    ) -> dict:

        user_validation = self._validate_identifier(
            user_id,
            "User ID"
        )

        if not user_validation["valid"]:
            return user_validation

        type_validation = self._validate_identifier(
            data_type,
            "Data type"
        )

        if not type_validation["valid"]:
            return type_validation

        id_validation = self._validate_identifier(
            data_id,
            "Data ID"
        )

        if not id_validation["valid"]:
            return id_validation

        user_id = user_validation["sanitized"]
        data_type = type_validation["sanitized"]
        data_id = id_validation["sanitized"]

        if user_id not in self.user_data:
            self.user_data[user_id] = {}

        if data_type not in self.user_data[user_id]:
            self.user_data[user_id][data_type] = {}

        # Store a deep copy so external code cannot mutate
        # the isolated data through the original reference.
        self.user_data[user_id][data_type][data_id] = (
            deepcopy(data)
        )

        return {
            "success": True,
            "user_id": user_id,
            "data_type": data_type,
            "data_id": data_id,
            "message": (
                "Data saved securely for the user."
            )
        }

    # =============================================================
    # GET DATA
    # =============================================================

    def get_data(
        self,
        user_id: str,
        data_type: str,
        data_id: str
    ) -> dict:

        user_validation = self._validate_identifier(
            user_id,
            "User ID"
        )

        if not user_validation["valid"]:
            return user_validation

        type_validation = self._validate_identifier(
            data_type,
            "Data type"
        )

        if not type_validation["valid"]:
            return type_validation

        id_validation = self._validate_identifier(
            data_id,
            "Data ID"
        )

        if not id_validation["valid"]:
            return id_validation

        user_id = user_validation["sanitized"]
        data_type = type_validation["sanitized"]
        data_id = id_validation["sanitized"]

        user_store = self.user_data.get(
            user_id
        )

        if user_store is None:
            return {
                "success": False,
                "message": (
                    "User data store not found."
                )
            }

        type_store = user_store.get(
            data_type
        )

        if type_store is None:
            return {
                "success": False,
                "message": (
                    "Data type not found."
                )
            }

        if data_id not in type_store:
            return {
                "success": False,
                "message": (
                    "Data not found."
                )
            }

        return {
            "success": True,
            "user_id": user_id,
            "data_type": data_type,
            "data_id": data_id,
            "data": deepcopy(
                type_store[data_id]
            )
        }

    # =============================================================
    # GET ALL DATA
    # =============================================================

    def get_all_data(
        self,
        user_id: str,
        data_type: str
    ) -> dict:

        user_validation = self._validate_identifier(
            user_id,
            "User ID"
        )

        if not user_validation["valid"]:
            return user_validation

        type_validation = self._validate_identifier(
            data_type,
            "Data type"
        )

        if not type_validation["valid"]:
            return type_validation

        user_id = user_validation["sanitized"]
        data_type = type_validation["sanitized"]

        user_store = self.user_data.get(
            user_id
        )

        if user_store is None:
            return {
                "success": False,
                "message": (
                    "User data store not found."
                )
            }

        data = user_store.get(
            data_type,
            {}
        )

        return {
            "success": True,
            "user_id": user_id,
            "data_type": data_type,
            "data": deepcopy(data)
        }

    # =============================================================
    # CHECK DATA OWNERSHIP
    # =============================================================

    def user_owns_data(
        self,
        user_id: str,
        data_type: str,
        data_id: str
    ) -> bool:

        user_validation = self._validate_identifier(
            user_id,
            "User ID"
        )

        if not user_validation["valid"]:
            return False

        type_validation = self._validate_identifier(
            data_type,
            "Data type"
        )

        if not type_validation["valid"]:
            return False

        id_validation = self._validate_identifier(
            data_id,
            "Data ID"
        )

        if not id_validation["valid"]:
            return False

        user_id = user_validation["sanitized"]
        data_type = type_validation["sanitized"]
        data_id = id_validation["sanitized"]

        user_store = self.user_data.get(
            user_id
        )

        if user_store is None:
            return False

        type_store = user_store.get(
            data_type
        )

        if type_store is None:
            return False

        return data_id in type_store

    # =============================================================
    # CHECK DATA ACCESS
    # =============================================================

    def check_access(
        self,
        user_id: str,
        data_type: str,
        data_id: str
    ) -> dict:

        if self.user_owns_data(
            user_id,
            data_type,
            data_id
        ):
            return {
                "allowed": True,
                "user_id": user_id,
                "data_type": data_type,
                "data_id": data_id,
                "message": (
                    "User is authorized to access this data."
                )
            }

        return {
            "allowed": False,
            "user_id": user_id,
            "data_type": data_type,
            "data_id": data_id,
            "message": (
                "Data does not belong to this user."
            )
        }

    # =============================================================
    # DELETE DATA
    # =============================================================

    def delete_data(
        self,
        user_id: str,
        data_type: str,
        data_id: str
    ) -> dict:

        if not self.user_owns_data(
            user_id,
            data_type,
            data_id
        ):
            return {
                "success": False,
                "message": (
                    "Data does not belong to this user."
                )
            }

        user_id = user_id.strip()
        data_type = data_type.strip()
        data_id = data_id.strip()

        del self.user_data[
            user_id
        ][
            data_type
        ][
            data_id
        ]

        # Remove empty data-type store.
        if not self.user_data[
            user_id
        ][
            data_type
        ]:
            del self.user_data[
                user_id
            ][
                data_type
            ]

        return {
            "success": True,
            "user_id": user_id,
            "data_type": data_type,
            "data_id": data_id,
            "message": (
                "User data deleted successfully."
            )
        }

    # =============================================================
    # CLEAR USER DATA
    # =============================================================

    def clear_user_data(
        self,
        user_id: str
    ) -> dict:

        validation = self._validate_identifier(
            user_id,
            "User ID"
        )

        if not validation["valid"]:
            return validation

        user_id = validation["sanitized"]

        if user_id not in self.user_data:
            return {
                "success": False,
                "message": (
                    "User data store not found."
                )
            }

        self.user_data[
            user_id
        ].clear()

        return {
            "success": True,
            "user_id": user_id,
            "message": (
                "All user data cleared successfully."
            )
        }

    # =============================================================
    # REMOVE USER STORE
    # =============================================================

    def remove_user_store(
        self,
        user_id: str
    ) -> dict:

        validation = self._validate_identifier(
            user_id,
            "User ID"
        )

        if not validation["valid"]:
            return validation

        user_id = validation["sanitized"]

        if user_id not in self.user_data:
            return {
                "success": False,
                "message": (
                    "User data store not found."
                )
            }

        del self.user_data[
            user_id
        ]

        return {
            "success": True,
            "user_id": user_id,
            "message": (
                "User data store removed successfully."
            )
        }

    # =============================================================
    # GET DATA TYPES
    # =============================================================

    def get_user_data_types(
        self,
        user_id: str
    ) -> list:

        validation = self._validate_identifier(
            user_id,
            "User ID"
        )

        if not validation["valid"]:
            return []

        user_id = validation["sanitized"]

        user_store = self.user_data.get(
            user_id,
            {}
        )

        return sorted(
            user_store.keys()
        )

    # =============================================================
    # GET USER DATA COUNT
    # =============================================================

    def get_user_data_count(
        self,
        user_id: str
    ) -> int:

        validation = self._validate_identifier(
            user_id,
            "User ID"
        )

        if not validation["valid"]:
            return 0

        user_id = validation["sanitized"]

        user_store = self.user_data.get(
            user_id,
            {}
        )

        return sum(
            len(type_store)
            for type_store in user_store.values()
        )

    # =============================================================
    # GET STATUS
    # =============================================================

    def get_status(
        self
    ) -> dict:

        total_users = len(
            self.user_data
        )

        total_items = sum(
            len(type_store)
            for user_store in self.user_data.values()
            for type_store in user_store.values()
        )

        return {
            "name": "data_isolation",
            "available": True,
            "enabled": True,
            "total_users": total_users,
            "total_data_items": total_items,
            "message": (
                "Data isolation manager is operational."
            )
        }