import os
import re
from copy import deepcopy


class SecretsManager:

    def __init__(self):

        self._secrets = {}

        self.name = "secrets_manager"
        self.enabled = True

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def _validate_secret_name(
        self,
        secret_name: str
    ) -> dict:

        if secret_name is None:
            return {
                "success": False,
                "message": "Secret name is required."
            }

        if not isinstance(
            secret_name,
            str
        ):
            return {
                "success": False,
                "message": "Secret name must be text."
            }

        secret_name = secret_name.strip()

        if not secret_name:
            return {
                "success": False,
                "message": "Secret name cannot be empty."
            }

        if len(secret_name) > 200:
            return {
                "success": False,
                "message": "Secret name is too long."
            }

        if not re.fullmatch(
            r"[A-Za-z0-9_.-]+",
            secret_name
        ):
            return {
                "success": False,
                "message": "Secret name contains invalid characters."
            }

        return {
            "success": True,
            "secret_name": secret_name
        }

    def _validate_secret_value(
        self,
        secret_value: str
    ) -> dict:

        if secret_value is None:
            return {
                "success": False,
                "message": "Secret value is required."
            }

        if not isinstance(
            secret_value,
            str
        ):
            return {
                "success": False,
                "message": "Secret value must be text."
            }

        if not secret_value:
            return {
                "success": False,
                "message": "Secret value cannot be empty."
            }

        return {
            "success": True,
            "secret_value": secret_value
        }

    # ---------------------------------------------------------
    # GET SECRET
    # ---------------------------------------------------------

    def get_secret(
        self,
        secret_name: str
    ) -> dict:

        name_result = self._validate_secret_name(
            secret_name
        )

        if not name_result["success"]:
            return name_result

        secret_name = name_result["secret_name"]

        # Environment variables have priority.
        environment_value = os.getenv(
            secret_name
        )

        if environment_value:
            return {
                "success": True,
                "secret": environment_value,
                "source": "environment"
            }

        if secret_name in self._secrets:

            return {
                "success": True,
                "secret": self._secrets[secret_name],
                "source": "memory"
            }

        return {
            "success": False,
            "message": "Secret not found."
        }

    # ---------------------------------------------------------
    # SET SECRET
    # ---------------------------------------------------------

    def set_secret(
        self,
        secret_name: str,
        secret_value: str
    ) -> dict:

        name_result = self._validate_secret_name(
            secret_name
        )

        if not name_result["success"]:
            return name_result

        value_result = self._validate_secret_value(
            secret_value
        )

        if not value_result["success"]:
            return value_result

        secret_name = name_result["secret_name"]
        secret_value = value_result["secret_value"]

        self._secrets[secret_name] = secret_value

        return {
            "success": True,
            "secret_name": secret_name,
            "source": "memory",
            "message": "Secret stored securely in memory."
        }

    # ---------------------------------------------------------
    # DELETE SECRET
    # ---------------------------------------------------------

    def delete_secret(
        self,
        secret_name: str
    ) -> dict:

        name_result = self._validate_secret_name(
            secret_name
        )

        if not name_result["success"]:
            return name_result

        secret_name = name_result["secret_name"]

        if secret_name in self._secrets:

            del self._secrets[secret_name]

            return {
                "success": True,
                "secret_name": secret_name,
                "message": "Secret deleted successfully."
            }

        return {
            "success": False,
            "message": "Secret not found in memory."
        }

    # ---------------------------------------------------------
    # HAS SECRET
    # ---------------------------------------------------------

    def has_secret(
        self,
        secret_name: str
    ) -> bool:

        name_result = self._validate_secret_name(
            secret_name
        )

        if not name_result["success"]:
            return False

        secret_name = name_result["secret_name"]

        if secret_name in self._secrets:
            return True

        return bool(
            os.getenv(secret_name)
        )

    # ---------------------------------------------------------
    # SECRET SOURCE
    # ---------------------------------------------------------

    def get_secret_source(
        self,
        secret_name: str
    ) -> dict:

        name_result = self._validate_secret_name(
            secret_name
        )

        if not name_result["success"]:
            return name_result

        secret_name = name_result["secret_name"]

        if os.getenv(secret_name):
            return {
                "success": True,
                "secret_name": secret_name,
                "source": "environment"
            }

        if secret_name in self._secrets:
            return {
                "success": True,
                "secret_name": secret_name,
                "source": "memory"
            }

        return {
            "success": False,
            "message": "Secret not found."
        }

    # ---------------------------------------------------------
    # MEMORY SECRET NAMES
    # ---------------------------------------------------------

    def get_memory_secret_names(
        self
    ) -> list:

        return list(
            self._secrets.keys()
        )

    # ---------------------------------------------------------
    # MEMORY SECRET COUNT
    # ---------------------------------------------------------

    def get_memory_secret_count(
        self
    ) -> int:

        return len(
            self._secrets
        )

    # ---------------------------------------------------------
    # CLEAR MEMORY SECRETS
    # ---------------------------------------------------------

    def clear_memory_secrets(
        self
    ) -> dict:

        count = len(
            self._secrets
        )

        self._secrets.clear()

        return {
            "success": True,
            "cleared_count": count,
            "message": "All memory secrets cleared successfully."
        }

    # ---------------------------------------------------------
    # EXPORT STATUS
    # ---------------------------------------------------------

    def get_status(
        self
    ) -> dict:

        return {
            "name": self.name,
            "available": True,
            "enabled": self.enabled,
            "memory_secret_count": len(
                self._secrets
            ),
            "environment_access": True,
            "secrets_exposed_in_status": False,
            "message": "Secrets manager is operational."
        }