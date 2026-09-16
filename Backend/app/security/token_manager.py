import os
import uuid
from datetime import datetime, timezone

from app.database.connection import SessionLocal
from app.database.models import OAuthToken
from app.security.encryption import EncryptionManager


class TokenManager:
    """
    Secure OAuth token manager.

    OAuth tokens are encrypted before being stored in the
    database and decrypted only when they are explicitly needed.
    """

    def __init__(self):

        self.name = "token_manager"
        self.enabled = True

        self.environment = os.getenv(
            "AI_BUDDY_ENV",
            "development"
        )

        encryption_secret = os.getenv(
            "AI_BUDDY_ENCRYPTION_SECRET"
        )

        if not encryption_secret:

            if self.environment == "production":
                raise RuntimeError(
                    "AI_BUDDY_ENCRYPTION_SECRET is required "
                    "in production."
                )

            encryption_secret = (
                "ai-buddy-development-key"
            )

        self.encryption = EncryptionManager(
            encryption_secret
        )

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def _validate_user_id(self, user_id):

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):

            return {
                "success": False,
                "message": "user_id must be a valid integer."
            }

        if user_id <= 0:

            return {
                "success": False,
                "message": "user_id must be greater than zero."
            }

        return {
            "success": True,
            "user_id": user_id
        }

    def _validate_provider(self, provider):

        if not isinstance(provider, str):
            return {
                "success": False,
                "message": "provider must be text."
            }

        provider = provider.strip().lower()

        if not provider:
            return {
                "success": False,
                "message": "provider cannot be empty."
            }

        return {
            "success": True,
            "provider": provider
        }

    # ---------------------------------------------------------
    # EXPIRY
    # ---------------------------------------------------------

    def _parse_expiry(self, expires_at):

        if not expires_at:
            return None

        if isinstance(expires_at, datetime):
            expiry = expires_at

        elif isinstance(expires_at, str):

            try:
                expiry = datetime.fromisoformat(
                    expires_at.replace(
                        "Z",
                        "+00:00"
                    )
                )

            except ValueError:
                return None

        else:
            return None

        if expiry.tzinfo is None:
            expiry = expiry.replace(
                tzinfo=timezone.utc
            )

        return expiry

    def _is_expired(self, expires_at):

        expiry = self._parse_expiry(
            expires_at
        )

        if expiry is None:
            return False

        return expiry <= datetime.now(
            timezone.utc
        )

    # ---------------------------------------------------------
    # STORE TOKEN
    # ---------------------------------------------------------

    def store_token(
        self,
        user_id,
        provider,
        access_token,
        refresh_token=None,
        expires_at=None
    ):

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

        if not access_token or not isinstance(
            access_token,
            str
        ):
            return {
                "success": False,
                "message": "access_token is required."
            }

        user_id = user_result["user_id"]
        provider = provider_result["provider"]

        db = SessionLocal()

        try:

            # -------------------------------------------------
            # ENCRYPT TOKENS
            # -------------------------------------------------

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

            # -------------------------------------------------
            # CHECK EXISTING TOKEN
            # -------------------------------------------------

            existing_token = (
                db.query(OAuthToken)
                .filter(
                    OAuthToken.user_id == user_id,
                    OAuthToken.provider == provider
                )
                .first()
            )

            if existing_token:

                existing_token.encrypted_access_token = (
                    encrypted_access_token
                )

                if refresh_token:
                    existing_token.encrypted_refresh_token = (
                        encrypted_refresh_token
                    )

                existing_token.expires_at = (
                    expires_at
                )

                existing_token.active = True

                existing_token.updated_at = (
                    datetime.utcnow()
                )

                token_id = existing_token.token_id

            else:

                token_id = str(
                    uuid.uuid4()
                )

                token_record = OAuthToken(
                    user_id=user_id,
                    provider=provider,
                    token_id=token_id,
                    encrypted_access_token=(
                        encrypted_access_token
                    ),
                    encrypted_refresh_token=(
                        encrypted_refresh_token
                    ),
                    expires_at=expires_at,
                    active=True
                )

                db.add(token_record)

            db.commit()

            return {
                "success": True,
                "token_id": token_id,
                "user_id": user_id,
                "provider": provider,
                "active": True,
                "message": (
                    "OAuth token stored securely."
                )
            }

        except Exception as exc:

            db.rollback()

            return {
                "success": False,
                "message": (
                    "OAuth token storage failed."
                ),
                "error": str(exc)
            }

        finally:

            db.close()

    # ---------------------------------------------------------
    # GET TOKEN
    # ---------------------------------------------------------

    def get_token(
        self,
        user_id,
        provider
    ):

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

        db = SessionLocal()

        try:

            token_record = (
                db.query(OAuthToken)
                .filter(
                    OAuthToken.user_id == user_id,
                    OAuthToken.provider == provider
                )
                .first()
            )

            if token_record is None:

                return {
                    "success": False,
                    "message": (
                        "OAuth token was not found."
                    )
                }

            if not token_record.active:

                return {
                    "success": False,
                    "message": (
                        "OAuth token is inactive."
                    )
                }

            if self._is_expired(
                token_record.expires_at
            ):

                token_record.active = False
                token_record.updated_at = (
                    datetime.utcnow()
                )

                db.commit()

                return {
                    "success": False,
                    "message": (
                        "OAuth token has expired."
                    )
                }

            access_token = (
                self.encryption.decrypt_value(
                    token_record.encrypted_access_token
                )
            )

            refresh_token = None

            if token_record.encrypted_refresh_token:

                refresh_token = (
                    self.encryption.decrypt_value(
                        token_record.encrypted_refresh_token
                    )
                )

            return {
                "success": True,
                "token_id": token_record.token_id,
                "user_id": token_record.user_id,
                "provider": token_record.provider,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": token_record.expires_at,
                "active": token_record.active
            }

        except Exception as exc:

            return {
                "success": False,
                "message": (
                    "OAuth token retrieval failed."
                ),
                "error": str(exc)
            }

        finally:

            db.close()

    # ---------------------------------------------------------
    # REVOKE TOKEN
    # ---------------------------------------------------------

    def revoke_token(
        self,
        user_id,
        provider
    ):

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

        db = SessionLocal()

        try:

            token_record = (
                db.query(OAuthToken)
                .filter(
                    OAuthToken.user_id == user_id,
                    OAuthToken.provider == provider
                )
                .first()
            )

            if token_record is None:

                return {
                    "success": False,
                    "message": (
                        "OAuth token was not found."
                    )
                }

            token_record.active = False
            token_record.updated_at = (
                datetime.utcnow()
            )

            db.commit()

            return {
                "success": True,
                "token_id": token_record.token_id,
                "user_id": user_id,
                "provider": provider,
                "active": False,
                "message": (
                    "OAuth token revoked successfully."
                )
            }

        except Exception as exc:

            db.rollback()

            return {
                "success": False,
                "message": (
                    "OAuth token revocation failed."
                ),
                "error": str(exc)
            }

        finally:

            db.close()

    # ---------------------------------------------------------
    # TOKEN OWNERSHIP
    # ---------------------------------------------------------

    def token_belongs_to_user(
        self,
        token_id,
        user_id
    ):

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return False

        if not token_id:
            return False

        user_id = user_result["user_id"]

        db = SessionLocal()

        try:

            token_record = (
                db.query(OAuthToken)
                .filter(
                    OAuthToken.token_id == str(
                        token_id
                    ),
                    OAuthToken.user_id == user_id
                )
                .first()
            )

            return token_record is not None

        finally:

            db.close()

    # ---------------------------------------------------------
    # USER PROVIDERS
    # ---------------------------------------------------------

    def get_user_providers(
        self,
        user_id
    ):

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return user_result

        user_id = user_result["user_id"]

        db = SessionLocal()

        try:

            records = (
                db.query(OAuthToken)
                .filter(
                    OAuthToken.user_id == user_id,
                    OAuthToken.active.is_(True)
                )
                .all()
            )

            providers = [
                record.provider
                for record in records
            ]

            return {
                "success": True,
                "user_id": user_id,
                "providers": providers
            }

        finally:

            db.close()

    # ---------------------------------------------------------
    # REMOVE USER TOKENS
    # ---------------------------------------------------------

    def remove_user_tokens(
        self,
        user_id
    ):

        user_result = self._validate_user_id(
            user_id
        )

        if not user_result["success"]:
            return user_result

        user_id = user_result["user_id"]

        db = SessionLocal()

        try:

            records = (
                db.query(OAuthToken)
                .filter(
                    OAuthToken.user_id == user_id
                )
                .all()
            )

            count = len(records)

            for record in records:
                db.delete(record)

            db.commit()

            return {
                "success": True,
                "user_id": user_id,
                "removed": count,
                "message": (
                    "User OAuth tokens removed."
                )
            }

        except Exception as exc:

            db.rollback()

            return {
                "success": False,
                "message": (
                    "Unable to remove user OAuth tokens."
                ),
                "error": str(exc)
            }

        finally:

            db.close()

    # ---------------------------------------------------------
    # TOKEN EXISTS
    # ---------------------------------------------------------

    def token_exists(
        self,
        user_id,
        provider
    ):

        result = self.get_token(
            user_id=user_id,
            provider=provider
        )

        return result["success"]

    # ---------------------------------------------------------
    # TOKEN COUNTS
    # ---------------------------------------------------------

    def get_total_tokens(self):

        db = SessionLocal()

        try:
            return db.query(OAuthToken).count()
        finally:
            db.close()

    def get_active_token_count(self):

        db = SessionLocal()

        try:
            return (
                db.query(OAuthToken)
                .filter(
                    OAuthToken.active.is_(True)
                )
                .count()
            )
        finally:
            db.close()

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def get_status(self):

        db = SessionLocal()

        try:

            total_tokens = (
                db.query(OAuthToken).count()
            )

            active_tokens = (
                db.query(OAuthToken)
                .filter(
                    OAuthToken.active.is_(True)
                )
                .count()
            )

            inactive_tokens = (
                db.query(OAuthToken)
                .filter(
                    OAuthToken.active.is_(False)
                )
                .count()
            )

            expired_tokens = 0

            active_records = (
                db.query(OAuthToken)
                .filter(
                    OAuthToken.active.is_(True)
                )
                .all()
            )

            for record in active_records:

                if self._is_expired(
                    record.expires_at
                ):
                    expired_tokens += 1

            total_users = (
                db.query(
                    OAuthToken.user_id
                )
                .distinct()
                .count()
            )

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
                "storage": "database",
                "message": (
                    "Token manager is operational."
                )
            }

        finally:

            db.close()