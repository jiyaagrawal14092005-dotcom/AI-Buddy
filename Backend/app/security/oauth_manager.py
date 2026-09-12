import uuid
from datetime import datetime


class OAuthManager:

    def __init__(self):

        self.connections = {}

    def create_connection(
        self,
        user_id: str,
        provider: str,
        scopes: list
    ) -> dict:

        if not user_id:
            return {
                "success": False,
                "message": "User ID is required."
            }

        if not provider:
            return {
                "success": False,
                "message": "Provider is required."
            }

        if not scopes:
            return {
                "success": False,
                "message": "At least one OAuth scope is required."
            }

        connection_id = str(uuid.uuid4())

        connection = {
            "connection_id": connection_id,
            "user_id": user_id,
            "provider": provider,
            "scopes": scopes,
            "status": "PENDING",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
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
            "message": "OAuth connection created."
        }

    def authorize_connection(
        self,
        user_id: str,
        provider: str
    ) -> dict:

        user_connections = self.connections.get(user_id)

        if not user_connections:
            return {
                "success": False,
                "message": "No OAuth connections found for this user."
            }

        connection = user_connections.get(provider)

        if not connection:
            return {
                "success": False,
                "message": "OAuth connection not found."
            }

        connection["status"] = "AUTHORIZED"
        connection["updated_at"] = datetime.now().isoformat()

        return {
            "success": True,
            "user_id": user_id,
            "provider": provider,
            "status": "AUTHORIZED",
            "message": "OAuth connection authorized."
        }

    def get_connection(
        self,
        user_id: str,
        provider: str
    ) -> dict:

        user_connections = self.connections.get(user_id)

        if not user_connections:
            return {
                "success": False,
                "message": "No OAuth connections found."
            }

        connection = user_connections.get(provider)

        if not connection:
            return {
                "success": False,
                "message": "OAuth connection not found."
            }

        return {
            "success": True,
            "connection": connection.copy()
        }

    def is_authorized(
        self,
        user_id: str,
        provider: str
    ) -> bool:

        user_connections = self.connections.get(user_id)

        if not user_connections:
            return False

        connection = user_connections.get(provider)

        if not connection:
            return False

        return connection["status"] == "AUTHORIZED"

    def revoke_connection(
        self,
        user_id: str,
        provider: str
    ) -> dict:

        user_connections = self.connections.get(user_id)

        if not user_connections:
            return {
                "success": False,
                "message": "User connections not found."
            }

        connection = user_connections.get(provider)

        if not connection:
            return {
                "success": False,
                "message": "OAuth connection not found."
            }

        connection["status"] = "REVOKED"
        connection["updated_at"] = datetime.now().isoformat()

        return {
            "success": True,
            "user_id": user_id,
            "provider": provider,
            "status": "REVOKED",
            "message": "OAuth connection revoked."
        }

    def get_user_connections(
        self,
        user_id: str
    ) -> list:

        user_connections = self.connections.get(
            user_id,
            {}
        )

        return [
            {
                "connection_id": connection["connection_id"],
                "provider": connection["provider"],
                "status": connection["status"],
                "scopes": connection["scopes"]
            }
            for connection in user_connections.values()
        ]

    def remove_connection(
        self,
        user_id: str,
        provider: str
    ) -> dict:

        user_connections = self.connections.get(user_id)

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

        return {
            "success": True,
            "user_id": user_id,
            "provider": provider,
            "message": "OAuth connection removed successfully."
        }