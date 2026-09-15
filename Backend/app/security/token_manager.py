import uuid
from datetime import datetime

from app.security.encryption import EncryptionManager


class TokenManager:

    def __init__(
        self,
        encryption_secret: str = "ai-buddy-development-key"
    ):

        self.tokens = {}

        self.encryption = EncryptionManager(
            encryption_secret
        )

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

        if not isinstance(user_id, str):
            return {
                "success": False,
                "message": "User ID must be text."
            }

        if not provider:
            return {
                "success": False,
                "message": "Provider is required."
            }

        if not isinstance(provider, str):
            return {
                "success": False,
                "message": "Provider must be text."
            }

        if not access_token:
            return {
                "success": False,
                "message": "Access token is required."
            }

        if not isinstance(access_token, str):
            return {
                "success": False,
                "message": "Access token must be text."
            }

        if refresh_token is not None and not isinstance(
            refresh_token,
            str
        ):
            return {
                "success": False,
                "message": "Refresh token must be text."
            }

        user_id = user_id.strip()
        provider = provider.strip().lower()
        access_token = access_token.strip()

        if not user_id:
            return {
                "success": False,
                "message": "User ID cannot be empty."
            }

        if not provider:
            return {
                "success": False,
                "message": "Provider cannot be empty."
            }

        if not access_token:
            return {
                "success": False,
                "message": "Access token cannot be empty."
            }

        if refresh_token is not None:
            refresh_token = refresh_token.strip()

        encrypted_access_token = self.encryption.encrypt_value(
            access_token
        )

        encrypted_refresh_token = None

        if refresh_token:
            encrypted_refresh_token = self.encryption.encrypt_value(
                refresh_token
            )

        token_id = str(uuid.uuid4())

        token_record = {
            "token_id": token_id,
            "user_id": user_id,
            "provider": provider,
            "access_token": encrypted_access_token,
            "refresh_token": encrypted_refresh_token,
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
            "message": "Token stored securely."
        }

    def get_token(
        self,
        user_id: str,
        provider: str
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

        user_tokens = self.tokens.get(user_id)

        if not user_tokens:
            return {
                "success": False,
                "message": "No tokens found for this user."
            }

        provider = provider.strip().lower()

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

        try:
            access_token = self.encryption.decrypt_value(
                token["access_token"]
            )

            refresh_token = None

            if token["refresh_token"]:
                refresh_token = self.encryption.decrypt_value(
                    token["refresh_token"]
                )

            return {
                "success": True,
                "token_id": token["token_id"],
                "user_id": token["user_id"],
                "provider": token["provider"],
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": token["expires_at"]
            }

        except Exception:

            return {
                "success": False,
                "message": "Unable to decrypt token."
            }

    def revoke_token(
        self,
        user_id: str,
        provider: str
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

        user_tokens = self.tokens.get(user_id)

        if not user_tokens:
            return {
                "success": False,
                "message": "User tokens not found."
            }

        provider = provider.strip().lower()

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

        if not user_id or not provider or not token_id:
            return False

        user_tokens = self.tokens.get(user_id)

        if not user_tokens:
            return False

        provider = provider.strip().lower()

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

        if not user_id:
            return []

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

        if not user_id:
            return {
                "success": False,
                "message": "User ID is required."
            }

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