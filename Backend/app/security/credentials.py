from datetime import datetime, timezone

from app.security.encryption import EncryptionManager


class CredentialManager:

    def __init__(
        self,
        encryption_secret: str = "ai-buddy-development-key"
    ):

        self.credentials = {}

        self.encryption = EncryptionManager(
            encryption_secret
        )

    def save_credential(
        self,
        service: str,
        credential: str
    ) -> dict:

        if not service:
            return {
                "success": False,
                "message": "Service name is required."
            }

        if not isinstance(service, str):
            return {
                "success": False,
                "message": "Service name must be text."
            }

        if not credential:
            return {
                "success": False,
                "message": "Credential is required."
            }

        if not isinstance(credential, str):
            return {
                "success": False,
                "message": "Credential must be text."
            }

        service = service.strip().lower()

        if not service:
            return {
                "success": False,
                "message": "Service name cannot be empty."
            }

        encrypted = self.encryption.encrypt_value(
            credential
        )

        self.credentials[service] = {
            "credential": encrypted,
            "updated_at": datetime.now(
                timezone.utc
            ).isoformat()
        }

        return {
            "success": True,
            "service": service,
            "message": "Credential saved securely."
        }

    def has_credential(
        self,
        service: str
    ) -> bool:

        if not service:
            return False

        service = service.strip().lower()

        return service in self.credentials

    def get_credential(
        self,
        service: str
    ) -> dict:

        if not service:
            return {
                "success": False,
                "message": "Service name is required."
            }

        service = service.strip().lower()

        credential_data = self.credentials.get(
            service
        )

        if not credential_data:
            return {
                "success": False,
                "message": "Credential not found."
            }

        try:

            decrypted = self.encryption.decrypt_value(
                credential_data["credential"]
            )

            return {
                "success": True,
                "service": service,
                "credential": decrypted,
                "updated_at":
                    credential_data["updated_at"]
            }

        except Exception:

            return {
                "success": False,
                "message": "Unable to decrypt credential."
            }

    def delete_credential(
        self,
        service: str
    ) -> dict:

        if not service:
            return {
                "success": False,
                "message": "Service name is required."
            }

        service = service.strip().lower()

        if service not in self.credentials:
            return {
                "success": False,
                "message": "Credential not found."
            }

        del self.credentials[service]

        return {
            "success": True,
            "message": "Credential deleted successfully."
        }

    def list_services(self) -> list:

        return list(
            self.credentials.keys()
        )

    def clear(self) -> dict:

        self.credentials.clear()

        return {
            "success": True,
            "message": "All credentials cleared."
        }