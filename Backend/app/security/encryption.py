import base64
import hashlib

from cryptography.fernet import Fernet


class EncryptionManager:

    def __init__(self, secret_key: str):

        if not secret_key:
            raise ValueError(
                "Encryption secret key is required."
            )

        key = base64.urlsafe_b64encode(
            hashlib.sha256(
                secret_key.encode()
            ).digest()
        )

        self.cipher = Fernet(key)

    def encrypt(
        self,
        data: str
    ) -> dict:

        if not data:
            return {
                "success": False,
                "message": "Data is required."
            }

        encrypted_data = self.cipher.encrypt(
            data.encode()
        ).decode()

        return {
            "success": True,
            "encrypted_data": encrypted_data,
            "message": "Data encrypted successfully."
        }

    def decrypt(
        self,
        encrypted_data: str
    ) -> dict:

        if not encrypted_data:
            return {
                "success": False,
                "message": "Encrypted data is required."
            }

        try:

            decrypted_data = self.cipher.decrypt(
                encrypted_data.encode()
            ).decode()

            return {
                "success": True,
                "data": decrypted_data,
                "message": "Data decrypted successfully."
            }

        except Exception:

            return {
                "success": False,
                "message": "Unable to decrypt data."
            }

    def encrypt_value(
        self,
        value: str
    ) -> str:

        return self.cipher.encrypt(
            value.encode()
        ).decode()

    def decrypt_value(
        self,
        encrypted_value: str
    ) -> str:

        return self.cipher.decrypt(
            encrypted_value.encode()
        ).decode()