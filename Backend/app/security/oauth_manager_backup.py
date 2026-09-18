import uuid
from copy import deepcopy
from datetime import datetime, timezone


class OAuthManager:

    VALID_STATUSES = {
        "PENDING",
        "AUTHORIZED",
        "REVOKED"
    }

    def __init__(self):

        self.connections = {}

        self.name = "oauth_manager"
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

        if not isinstance(user_id, str):
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

        return {
            "success": True,
            "user_id": user_id
        }

    def _validate_provider(
        self,
        provider: str
    ) -> dict:

        if provider is None:
            return {
                "success": False,
                "message": "Provider is required."
            }

        if not isinstance(provider, str):
            return {
                "success": False,
                "message": "Provider must be text."
            }

        provider = provider.strip().lower()

        if not provider:
            return {
                "success": False,
                "message": "Provider cannot be empty."
            }

        return {
            "success": True,
            "provider": provider
        }

    def _validate_scopes(
        self,
        scopes: list
    ) -> dict:

        if scopes is None:
            return {
                "success": False,
                "message": "At least one OAuth scope is required."
            }

        if not isinstance(scopes, list):
            return {
                "success": False,
                "message": "OAuth scopes must be a list."
            }

        cleaned_scopes = []

        for scope in scopes:

            if not isinstance(scope, str):
                return {
                    "success": False,
                    "message": "Each OAuth scope must be text."
                }

            scope = scope.strip()

            if not scope:
                continue

            if scope not in cleaned_scopes:
                cleaned_scopes.append(scope)

        if not cleaned_scopes:
            return {
                "success": False,
                "message": "At least one valid OAuth scope is required."
            }

        return {
            "success": True,
            "scopes": cleaned_scopes
        }

    def _timestamp(self) -> str:

        return datetime.now(
            timezone.utc
        ).isoformat()

    # ---------------------------------------------------------
    # CREATE CONNECTION
    # ---------------------------------------------------------

    def create_connection(
        self,
        user_id: str,
        provider: str,
        scopes: list
    ) -> dict:

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return user_result

        provider_result = self._validate_provider(
            provider
        )

        if not provider_result["success"]:
            return provider_result

        scope_result = self._validate_scopes(
            scopes
        )

        if not scope_result["success"]:
            return scope_result

        user_id = user_result["user_id"]
        provider = provider_result["provider"]
        scopes = scope_result["scopes"]

        connection_id = str(
            uuid.uuid4()
        )

        now = self._timestamp()

        connection = {
            "connection_id": connection_id,
            "user_id": user_id,
            "provider": provider,
            "scopes": deepcopy(scopes),
            "status": "PENDING",
            "created_at": now,
            "updated_at": now
        }

        if user_id not in self.connections:
            self.connections[user_id] = {}

        self.connections[user_id][provider] = connection

        return {
            "success": True,
            "connection_id": connection_id,
            "user_id": user_id,
            "provider": provider,
            "status": "PENDING",
            "scopes": deepcopy(scopes),
            "message": "OAuth connection created."
        }

    # ---------------------------------------------------------
    # AUTHORIZE CONNECTION
    # ---------------------------------------------------------

    def authorize_connection(
        self,
        user_id: str,
        provider: str
    ) -> dict:

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return user_result

        provider_result = self._validate_provider(
            provider
        )

        if not provider_result["success"]:
            return provider_result

        user_id = user_result["user_id"]
        provider = provider_result["provider"]

        user_connections = self.connections.get(
            user_id
        )

        if not user_connections:
            return {
                "success": False,
                "message": "No OAuth connections found for this user."
            }

        connection = user_connections.get(
            provider
        )

        if not connection:
            return {
                "success": False,
                "message": "OAuth connection not found."
            }

        if connection["status"] == "AUTHORIZED":
            return {
                "success": True,
                "user_id": user_id,
                "provider": provider,
                "connection_id": connection["connection_id"],
                "status": "AUTHORIZED",
                "message": "OAuth connection is already authorized."
            }

        if connection["status"] == "REVOKED":
            return {
                "success": False,
                "message": "Revoked OAuth connection cannot be authorized."
            }

        connection["status"] = "AUTHORIZED"
        connection["updated_at"] = self._timestamp()

        return {
            "success": True,
            "user_id": user_id,
            "provider": provider,
            "connection_id": connection["connection_id"],
            "status": "AUTHORIZED",
            "message": "OAuth connection authorized."
        }

    # ---------------------------------------------------------
    # AUTHORIZE WITH ACTUAL GRANTED SCOPES
    # ---------------------------------------------------------

    def authorize_connection_with_scopes(
        self,
        user_id: str,
        provider: str,
        scopes: list
    ) -> dict:

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return user_result

        provider_result = self._validate_provider(
            provider
        )

        if not provider_result["success"]:
            return provider_result

        scope_result = self._validate_scopes(
            scopes
        )

        if not scope_result["success"]:
            return scope_result

        user_id = user_result["user_id"]
        provider = provider_result["provider"]
        scopes = scope_result["scopes"]

        user_connections = self.connections.get(
            user_id
        )

        if not user_connections:
            return {
                "success": False,
                "message": "No OAuth connections found for this user."
            }

        connection = user_connections.get(
            provider
        )

        if not connection:
            return {
                "success": False,
                "message": "OAuth connection not found."
            }

        if connection["status"] == "REVOKED":
            return {
                "success": False,
                "message": "Revoked OAuth connection cannot be authorized."
            }

        connection["scopes"] = deepcopy(
            scopes
        )

        connection["status"] = "AUTHORIZED"
        connection["updated_at"] = self._timestamp()

        return {
            "success": True,
            "user_id": user_id,
            "provider": provider,
            "connection_id": connection["connection_id"],
            "status": "AUTHORIZED",
            "scopes": deepcopy(scopes),
            "message": (
                "OAuth connection authorized with granted scopes."
            )
        }

    # ---------------------------------------------------------
    # GET CONNECTION
    # ---------------------------------------------------------

    def get_connection(
        self,
        user_id: str,
        provider: str
    ) -> dict:

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return user_result

        provider_result = self._validate_provider(
            provider
        )

        if not provider_result["success"]:
            return provider_result

        user_id = user_result["user_id"]
        provider = provider_result["provider"]

        user_connections = self.connections.get(
            user_id
        )

        if not user_connections:
            return {
                "success": False,
                "message": "No OAuth connections found."
            }

        connection = user_connections.get(
            provider
        )

        if not connection:
            return {
                "success": False,
                "message": "OAuth connection not found."
            }

        return {
            "success": True,
            "connection": deepcopy(connection)
        }

    # ---------------------------------------------------------
    # AUTHORIZATION CHECK
    # ---------------------------------------------------------

    def is_authorized(
        self,
        user_id: str,
        provider: str
    ) -> bool:

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return False

        provider_result = self._validate_provider(
            provider
        )

        if not provider_result["success"]:
            return False

        user_id = user_result["user_id"]
        provider = provider_result["provider"]

        user_connections = self.connections.get(
            user_id
        )

        if not user_connections:
            return False

        connection = user_connections.get(
            provider
        )

        if not connection:
            return False

        return connection["status"] == "AUTHORIZED"

    # ---------------------------------------------------------
    # OWNERSHIP CHECK
    # ---------------------------------------------------------

    def connection_belongs_to_user(
        self,
        user_id: str,
        provider: str,
        connection_id: str
    ) -> bool:

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return False

        provider_result = self._validate_provider(
            provider
        )

        if not provider_result["success"]:
            return False

        if not connection_id:
            return False

        if not isinstance(
            connection_id,
            str
        ):
            return False

        user_id = user_result["user_id"]
        provider = provider_result["provider"]
        connection_id = connection_id.strip()

        user_connections = self.connections.get(
            user_id
        )

        if not user_connections:
            return False

        connection = user_connections.get(
            provider
        )

        if not connection:
            return False

        return (
            connection["connection_id"] == connection_id
            and connection["user_id"] == user_id
        )

    # ---------------------------------------------------------
    # REVOKE CONNECTION
    # ---------------------------------------------------------

    def revoke_connection(
        self,
        user_id: str,
        provider: str
    ) -> dict:

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return user_result

        provider_result = self._validate_provider(
            provider
        )

        if not provider_result["success"]:
            return provider_result

        user_id = user_result["user_id"]
        provider = provider_result["provider"]

        user_connections = self.connections.get(
            user_id
        )

        if not user_connections:
            return {
                "success": False,
                "message": "User connections not found."
            }

        connection = user_connections.get(
            provider
        )

        if not connection:
            return {
                "success": False,
                "message": "OAuth connection not found."
            }

        connection["status"] = "REVOKED"
        connection["updated_at"] = self._timestamp()

        return {
            "success": True,
            "user_id": user_id,
            "provider": provider,
            "connection_id": connection["connection_id"],
            "status": "REVOKED",
            "message": "OAuth connection revoked."
        }

    # ---------------------------------------------------------
    # USER CONNECTIONS
    # ---------------------------------------------------------

    def get_user_connections(
        self,
        user_id: str
    ) -> list:

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return []

        user_id = user_result["user_id"]

        user_connections = self.connections.get(
            user_id,
            {}
        )

        return [
            {
                "connection_id": connection["connection_id"],
                "provider": connection["provider"],
                "status": connection["status"],
                "scopes": deepcopy(
                    connection["scopes"]
                ),
                "created_at": connection["created_at"],
                "updated_at": connection["updated_at"]
            }
            for connection
            in user_connections.values()
        ]

    # ---------------------------------------------------------
    # GET AUTHORIZED CONNECTIONS
    # ---------------------------------------------------------

    def get_authorized_connections(
        self,
        user_id: str
    ) -> list:

        connections = self.get_user_connections(
            user_id
        )

        return [
            connection
            for connection in connections
            if connection["status"] == "AUTHORIZED"
        ]

    # ---------------------------------------------------------
    # GET SCOPES
    # ---------------------------------------------------------

    def get_connection_scopes(
        self,
        user_id: str,
        provider: str
    ) -> list:

        result = self.get_connection(
            user_id,
            provider
        )

        if not result["success"]:
            return []

        return deepcopy(
            result["connection"]["scopes"]
        )

    # ---------------------------------------------------------
    # SCOPE CHECK
    # ---------------------------------------------------------

    def has_scope(
        self,
        user_id: str,
        provider: str,
        scope: str
    ) -> bool:

        if not isinstance(
            scope,
            str
        ):
            return False

        scope = scope.strip()

        if not scope:
            return False

        if not self.is_authorized(
            user_id,
            provider
        ):
            return False

        scopes = self.get_connection_scopes(
            user_id,
            provider
        )

        return scope in scopes

    # ---------------------------------------------------------
    # REMOVE CONNECTION
    # ---------------------------------------------------------

    def remove_connection(
        self,
        user_id: str,
        provider: str
    ) -> dict:

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return user_result

        provider_result = self._validate_provider(
            provider
        )

        if not provider_result["success"]:
            return provider_result

        user_id = user_result["user_id"]
        provider = provider_result["provider"]

        user_connections = self.connections.get(
            user_id
        )

        if not user_connections:
            return {
                "success": False,
                "message": "User connections not found."
            }

        if provider not in user_connections:
            return {
                "success": False,
                "message": "OAuth connection not found."
            }

        del user_connections[provider]

        if not user_connections:
            del self.connections[user_id]

        return {
            "success": True,
            "user_id": user_id,
            "provider": provider,
            "message": "OAuth connection removed successfully."
        }

    # ---------------------------------------------------------
    # REMOVE ALL USER CONNECTIONS
    # ---------------------------------------------------------

    def remove_user_connections(
        self,
        user_id: str
    ) -> dict:

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return user_result

        user_id = user_result["user_id"]

        if user_id not in self.connections:
            return {
                "success": False,
                "message": "User connections not found."
            }

        del self.connections[user_id]

        return {
            "success": True,
            "user_id": user_id,
            "message": "All OAuth connections removed successfully."
        }

    # ---------------------------------------------------------
    # COUNTS
    # ---------------------------------------------------------

    def get_user_connection_count(
        self,
        user_id: str
    ) -> int:

        return len(
            self.get_user_connections(
                user_id
            )
        )

    def get_total_connection_count(self) -> int:

        total = 0

        for user_connections in self.connections.values():
            total += len(
                user_connections
            )

        return total

    def get_authorized_connection_count(
        self,
        user_id: str
    ) -> int:

        return len(
            self.get_authorized_connections(
                user_id
            )
        )

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def get_status(self) -> dict:

        total_users = len(
            self.connections
        )

        total_connections = 0
        pending_connections = 0
        authorized_connections = 0
        revoked_connections = 0

        for user_connections in self.connections.values():

            total_connections += len(
                user_connections
            )

            for connection in user_connections.values():

                status = connection.get(
                    "status"
                )

                if status == "PENDING":
                    pending_connections += 1

                elif status == "AUTHORIZED":
                    authorized_connections += 1

                elif status == "REVOKED":
                    revoked_connections += 1

        return {
            "name": self.name,
            "available": True,
            "enabled": self.enabled,
            "total_users": total_users,
            "total_connections": total_connections,
            "pending_connections": pending_connections,
            "authorized_connections": authorized_connections,
            "revoked_connections": revoked_connections,
            "message": "OAuth manager is operational."
        }