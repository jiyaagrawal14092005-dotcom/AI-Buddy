import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken


class EncryptionManager:

    def __init__(
        self,
        secret_key: str
    ):

        if secret_key is None:
            raise ValueError(
                "Encryption secret key is required."
            )

        if not isinstance(
            secret_key,
            str
        ):
            raise TypeError(
                "Encryption secret key must be text."
            )

        secret_key = secret_key.strip()

        if not secret_key:
            raise ValueError(
                "Encryption secret key cannot be empty."
            )

        key = base64.urlsafe_b64encode(
            hashlib.sha256(
                secret_key.encode("utf-8")
            ).digest()
        )

        self.cipher = Fernet(key)

        self.name = "encryption_manager"
        self.enabled = True

    # ---------------------------------------------------------
    # ENCRYPT
    # ---------------------------------------------------------

    def encrypt(
        self,
        data: str
    ) -> dict:

        if data is None:
            return {
                "success": False,
                "message": "Data is required."
            }

        if not isinstance(
            data,
            str
        ):
            return {
                "success": False,
                "message": "Data must be text."
            }

        if not data:
            return {
                "success": False,
                "message": "Data cannot be empty."
            }

        try:

            encrypted_data = (
                self.cipher.encrypt(
                    data.encode("utf-8")
                ).decode("utf-8")
            )

            return {
                "success": True,
                "encrypted_data": encrypted_data,
                "message": "Data encrypted successfully."
            }

        except Exception:

            return {
                "success": False,
                "message": "Unable to encrypt data."
            }

    # ---------------------------------------------------------
    # DECRYPT
    # ---------------------------------------------------------

    def decrypt(
        self,
        encrypted_data: str
    ) -> dict:

        if encrypted_data is None:
            return {
                "success": False,
                "message": "Encrypted data is required."
            }

        if not isinstance(
            encrypted_data,
            str
        ):
            return {
                "success": False,
                "message": "Encrypted data must be text."
            }

        if not encrypted_data:
            return {
                "success": False,
                "message": "Encrypted data cannot be empty."
            }

        try:

            decrypted_data = (
                self.cipher.decrypt(
                    encrypted_data.encode("utf-8")
                ).decode("utf-8")
            )

            return {
                "success": True,
                "data": decrypted_data,
                "message": "Data decrypted successfully."
            }

        except InvalidToken:

            return {
                "success": False,
                "message": "Invalid or corrupted encrypted data."
            }

        except Exception:

            return {
                "success": False,
                "message": "Unable to decrypt data."
            }

    # ---------------------------------------------------------
    # ENCRYPT VALUE
    # ---------------------------------------------------------

    def encrypt_value(
        self,
        value: str
    ) -> str:

        if value is None:
            raise ValueError(
                "Value is required."
            )

        if not isinstance(
            value,
            str
        ):
            raise TypeError(
                "Value must be text."
            )

        if not value:
            raise ValueError(
                "Value cannot be empty."
            )

        return (
            self.cipher.encrypt(
                value.encode("utf-8")
            ).decode("utf-8")
        )

    # ---------------------------------------------------------
    # DECRYPT VALUE
    # ---------------------------------------------------------

    def decrypt_value(
        self,
        encrypted_value: str
    ) -> str:

        if encrypted_value is None:
            raise ValueError(
                "Encrypted value is required."
            )

        if not isinstance(
            encrypted_value,
            str
        ):
            raise TypeError(
                "Encrypted value must be text."
            )

        if not encrypted_value:
            raise ValueError(
                "Encrypted value cannot be empty."
            )

        try:

            return (
                self.cipher.decrypt(
                    encrypted_value.encode("utf-8")
                ).decode("utf-8")
            )

        except InvalidToken as exc:

            raise ValueError(
                "Invalid or corrupted encrypted value."
            ) from exc

    # ---------------------------------------------------------
    # VERIFY ENCRYPTION
    # ---------------------------------------------------------

    def verify(
        self,
        data: str
    ) -> dict:

        if data is None:
            return {
                "success": False,
                "message": "Data is required."
            }

        if not isinstance(
            data,
            str
        ):
            return {
                "success": False,
                "message": "Data must be text."
            }

        if not data:
            return {
                "success": False,
                "message": "Data cannot be empty."
            }

        try:

            encrypted = self.encrypt_value(
                data
            )

            decrypted = self.decrypt_value(
                encrypted
            )

            if decrypted != data:
                return {
                    "success": False,
                    "verified": False,
                    "message": "Encryption verification failed."
                }

            return {
                "success": True,
                "verified": True,
                "message": "Encryption verification successful."
            }

        except Exception:

            return {
                "success": False,
                "verified": False,
                "message": "Encryption verification failed."
            }

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def get_status(self) -> dict:

        return {
            "name": self.name,
            "available": True,
            "enabled": self.enabled,
            "algorithm": "Fernet",
            "message": "Encryption manager is operational."
        }