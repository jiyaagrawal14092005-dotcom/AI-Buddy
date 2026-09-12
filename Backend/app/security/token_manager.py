import uuid
from datetime import datetime


class TokenManager:

    def __init__(self):

        self.tokens = {}

    def store_token(
        self,
        user_id: str,
        provider: str,
        access_token: str,
        refresh_token: str | None = None,
        expires_at: str | None = None
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

        if not access_token:
            return {
                "success": False,
                "message": "Access token is required."
            }

        token_id = str(uuid.uuid4())

        token_record = {
            "token_id": token_id,
            "user_id": user_id,
            "provider": provider,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at,
            "created_at": datetime.now().isoformat(),
            "active": True
        }

        if user_id not in self.tokens:
            self.tokens[user_id] = {}

        self.tokens[user_id][provider] = token_record

        return {
            "success": True,
            "token_id": token_id,
            "user_id": user_id,
            "provider": provider,
            "message": "Token stored successfully."
        }

    def get_token(
        self,
        user_id: str,
        provider: str
    ) -> dict:

        user_tokens = self.tokens.get(user_id)

        if not user_tokens:
            return {
                "success": False,
                "message": "No tokens found for this user."
            }

        token = user_tokens.get(provider)

        if not token:
            return {
                "success": False,
                "message": "Token not found for this provider."
            }

        if not token["active"]:
            return {
                "success": False,
                "message": "Token is inactive."
            }

        return {
            "success": True,
            "token_id": token["token_id"],
            "user_id": token["user_id"],
            "provider": token["provider"],
            "access_token": token["access_token"],
            "refresh_token": token["refresh_token"],
            "expires_at": token["expires_at"]
        }

    def revoke_token(
        self,
        user_id: str,
        provider: str
    ) -> dict:

        user_tokens = self.tokens.get(user_id)

        if not user_tokens:
            return {
                "success": False,
                "message": "User tokens not found."
            }

        token = user_tokens.get(provider)

        if not token:
            return {
                "success": False,
                "message": "Token not found."
            }

        token["active"] = False

        return {
            "success": True,
            "user_id": user_id,
            "provider": provider,
            "message": "Token revoked successfully."
        }

    def token_belongs_to_user(
        self,
        user_id: str,
        provider: str,
        token_id: str
    ) -> bool:

        user_tokens = self.tokens.get(user_id)

        if not user_tokens:
            return False

        token = user_tokens.get(provider)

        if not token:
            return False

        return (
            token["token_id"] == token_id
            and token["user_id"] == user_id
        )

    def get_user_providers(
        self,
        user_id: str
    ) -> list:

        user_tokens = self.tokens.get(
            user_id,
            {}
        )

        return [
            provider
            for provider, token
            in user_tokens.items()
            if token["active"]
        ]

    def remove_user_tokens(
        self,
        user_id: str
    ) -> dict:

        if user_id not in self.tokens:
            return {
                "success": False,
                "message": "User tokens not found."
            }

        del self.tokens[user_id]

        return {
            "success": True,
            "user_id": user_id,
            "message": "All user tokens removed successfully."
        }