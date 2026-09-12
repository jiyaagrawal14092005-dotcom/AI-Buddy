import os


class SecretsManager:

    def __init__(self):
        self._secrets = {}

    def get_secret(
        self,
        secret_name: str
    ) -> dict:

        if not secret_name:
            return {
                "success": False,
                "message": "Secret name is required."
            }

        if secret_name in self._secrets:
            return {
                "success": True,
                "secret": self._secrets[secret_name],
                "source": "memory"
            }

        secret_value = os.getenv(secret_name)

        if secret_value:

            return {
                "success": True,
                "secret": secret_value,
                "source": "environment"
            }

        return {
            "success": False,
            "message": "Secret not found."
        }

    def set_secret(
        self,
        secret_name: str,
        secret_value: str
    ) -> dict:

        if not secret_name:
            return {
                "success": False,
                "message": "Secret name is required."
            }

        if not secret_value:
            return {
                "success": False,
                "message": "Secret value is required."
            }

        self._secrets[secret_name] = secret_value

        return {
            "success": True,
            "message": "Secret stored successfully."
        }

    def delete_secret(
        self,
        secret_name: str
    ) -> dict:

        if secret_name in self._secrets:

            del self._secrets[secret_name]

            return {
                "success": True,
                "message": "Secret deleted successfully."
            }

        return {
            "success": False,
            "message": "Secret not found."
        }

    def has_secret(
        self,
        secret_name: str
    ) -> bool:

        if secret_name in self._secrets:
            return True

        return bool(os.getenv(secret_name))