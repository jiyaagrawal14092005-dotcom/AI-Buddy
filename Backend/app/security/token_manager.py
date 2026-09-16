import os
import uuid
from datetime import datetime, timezone

from app.security.encryption import EncryptionManager


class TokenManager:

    def __init__(
        self,
        encryption_secret: str | None = None
    ):
        self.tokens = {}

        environment = os.getenv(
            "AI_BUDDY_ENV",
            "development"
        ).strip().lower()

        provided_secret = (
            encryption_secret
            or os.getenv(
                "AI_BUDDY_ENCRYPTION_SECRET"
            )
        )

        if environment == "production":
            if not provided_secret:
                raise ValueError(
                    "AI_BUDDY_ENCRYPTION_SECRET is required in production."
                )

        if not provided_secret:
            provided_secret = "ai-buddy-development-key"

        self.encryption = EncryptionManager(
            provided_secret
        )

        self.environment = environment
        self.name = "token_manager"
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

    def _parse_expiry(
        self,
        expires_at: str | None
    ) -> datetime | None:

        if expires_at is None:
            return None

        if not isinstance(expires_at, str):
            return None

        value = expires_at.strip()

        if not value:
            return None

        try:
            parsed = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )

            if parsed.tzinfo is None:
                parsed = parsed.replace(
                    tzinfo=timezone.utc
                )

            return parsed

        except (ValueError, TypeError):
            return None

    def _is_expired(
        self,
        expires_at: str | None
    ) -> bool:

        expiry = self._parse_expiry(
            expires_at
        )

        if expiry is None:
            return False

        return datetime.now(
            timezone.utc
        ) >= expiry

    # ---------------------------------------------------------
    # STORE TOKEN
    # ---------------------------------------------------------

    def store_token(
        self,
        user_id: str,
        provider: str,
        access_token: str,
        refresh_token: str | None = None,
        expires_at: str | None = None
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

        if access_token is None:
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

        user_id = user_result["user_id"]
        provider = provider_result["provider"]
        access_token = access_token.strip()

        if not access_token:
            return {
                "success": False,
                "message": "Access token cannot be empty."
            }

        if refresh_token is not None:
            refresh_token = refresh_token.strip()

            if not refresh_token:
                refresh_token = None

        if expires_at is not None:

            if not isinstance(expires_at, str):
                return {
                    "success": False,
                    "message": "Expiry time must be text."
                }

            expires_at = expires_at.strip()

            if expires_at:

                parsed_expiry = self._parse_expiry(
                    expires_at
                )

                if parsed_expiry is None:
                    return {
                        "success": False,
                        "message": "Invalid expiry time format."
                    }

                if datetime.now(
                    timezone.utc
                ) >= parsed_expiry:
                    return {
                        "success": False,
                        "message": "Token is already expired."
                    }

            else:
                expires_at = None

        try:
            encrypted_access_token = (
                self.encryption.encrypt_value(
                    access_token
                )
            )

            encrypted_refresh_token = None

            if refresh_token:
                encrypted_refresh_token = (
                    self.encryption.encrypt_value(
                        refresh_token
                    )
                )

        except Exception:
            return {
                "success": False,
                "message": "Unable to encrypt token."
            }

        token_id = str(
            uuid.uuid4()
        )

        now = datetime.now(
            timezone.utc
        ).isoformat()

        token_record = {
            "token_id": token_id,
            "user_id": user_id,
            "provider": provider,
            "access_token": encrypted_access_token,
            "refresh_token": encrypted_refresh_token,
            "expires_at": expires_at,
            "created_at": now,
            "updated_at": now,
            "active": True
        }

        if user_id not in self.tokens:
            self.tokens[user_id] = {}

        # Replace existing token for the same provider.
        self.tokens[user_id][provider] = token_record

        return {
            "success": True,
            "token_id": token_id,
            "user_id": user_id,
            "provider": provider,
            "expires_at": expires_at,
            "message": "Token stored securely."
        }

    # ---------------------------------------------------------
    # GET TOKEN
    # ---------------------------------------------------------

    def get_token(
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

        user_tokens = self.tokens.get(
            user_id
        )

        if not user_tokens:
            return {
                "success": False,
                "message": "No tokens found for this user."
            }

        token = user_tokens.get(
            provider
        )

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

        # Automatically invalidate expired tokens.
        if self._is_expired(
            token.get("expires_at")
        ):
            token["active"] = False
            token["updated_at"] = datetime.now(
                timezone.utc
            ).isoformat()

            return {
                "success": False,
                "message": "Token has expired."
            }

        try:
            access_token = (
                self.encryption.decrypt_value(
                    token["access_token"]
                )
            )

            refresh_token = None

            if token["refresh_token"]:
                refresh_token = (
                    self.encryption.decrypt_value(
                        token["refresh_token"]
                    )
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

    # ---------------------------------------------------------
    # REVOKE TOKEN
    # ---------------------------------------------------------

    def revoke_token(
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

        user_tokens = self.tokens.get(
            user_id
        )

        if not user_tokens:
            return {
                "success": False,
                "message": "User tokens not found."
            }

        token = user_tokens.get(
            provider
        )

        if not token:
            return {
                "success": False,
                "message": "Token not found."
            }

        token["active"] = False
        token["updated_at"] = datetime.now(
            timezone.utc
        ).isoformat()

        return {
            "success": True,
            "user_id": user_id,
            "provider": provider,
            "token_id": token["token_id"],
            "message": "Token revoked successfully."
        }

    # ---------------------------------------------------------
    # OWNERSHIP CHECK
    # ---------------------------------------------------------

    def token_belongs_to_user(
        self,
        user_id: str,
        provider: str,
        token_id: str
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

        if not token_id or not isinstance(
            token_id,
            str
        ):
            return False

        user_id = user_result["user_id"]
        provider = provider_result["provider"]
        token_id = token_id.strip()

        user_tokens = self.tokens.get(
            user_id
        )

        if not user_tokens:
            return False

        token = user_tokens.get(
            provider
        )

        if not token:
            return False

        return (
            token["token_id"] == token_id
            and token["user_id"] == user_id
        )

    # ---------------------------------------------------------
    # USER PROVIDERS
    # ---------------------------------------------------------

    def get_user_providers(
        self,
        user_id: str
    ) -> list:

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return []

        user_id = user_result["user_id"]

        user_tokens = self.tokens.get(
            user_id,
            {}
        )

        active_providers = []

        for provider, token in user_tokens.items():

            if not token["active"]:
                continue

            if self._is_expired(
                token.get("expires_at")
            ):
                token["active"] = False
                token["updated_at"] = (
                    datetime.now(
                        timezone.utc
                    ).isoformat()
                )
                continue

            active_providers.append(
                provider
            )

        return active_providers

    # ---------------------------------------------------------
    # REMOVE ALL USER TOKENS
    # ---------------------------------------------------------

    def remove_user_tokens(
        self,
        user_id: str
    ) -> dict:

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return user_result

        user_id = user_result["user_id"]

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

    # ---------------------------------------------------------
    # TOKEN EXISTS
    # ---------------------------------------------------------

    def token_exists(
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

        user_tokens = self.tokens.get(
            user_id,
            {}
        )

        token = user_tokens.get(
            provider
        )

        if not token:
            return False

        if not token["active"]:
            return False

        if self._is_expired(
            token.get("expires_at")
        ):
            token["active"] = False
            token["updated_at"] = datetime.now(
                timezone.utc
            ).isoformat()
            return False

        return True

    # ---------------------------------------------------------
    # TOKEN COUNT
    # ---------------------------------------------------------

    def get_user_token_count(
        self,
        user_id: str
    ) -> int:

        return len(
            self.get_user_providers(
                user_id
            )
        )

    def get_total_token_count(self) -> int:

        total = 0

        for user_id in list(
            self.tokens.keys()
        ):
            total += self.get_user_token_count(
                user_id
            )

        return total

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def get_status(self) -> dict:

        total_users = len(
            self.tokens
        )

        total_tokens = 0

        active_tokens = 0
        inactive_tokens = 0
        expired_tokens = 0

        for user_tokens in self.tokens.values():

            total_tokens += len(
                user_tokens
            )

            for token in user_tokens.values():

                if self._is_expired(
                    token.get("expires_at")
                ):
                    token["active"] = False
                    expired_tokens += 1

                if token["active"]:
                    active_tokens += 1
                else:
                    inactive_tokens += 1

        return {
            "name": self.name,
            "available": True,
            "enabled": self.enabled,
            "environment": self.environment,
            "total_users": total_users,
            "total_tokens": total_tokens,
            "active_tokens": active_tokens,
            "inactive_tokens": inactive_tokens,
            "expired_tokens": expired_tokens,
            "encrypted_storage": True,
            "message": "Token manager is operational."
        }