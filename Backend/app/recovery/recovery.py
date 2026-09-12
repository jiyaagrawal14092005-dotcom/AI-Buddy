class RecoveryManager:

    def __init__(self):
        self.recovery_history = []

    # ---------------------------------
    # RECOVER OPERATION
    # ---------------------------------

    def recover(
        self,
        operation: str,
        error: str,
        fallback_result=None
    ) -> dict:

        if not isinstance(operation, str):
            return {
                "success": False,
                "recovered": False,
                "message": "Operation name must be text."
            }

        operation = operation.strip()

        if not operation:
            return {
                "success": False,
                "recovered": False,
                "message": "Operation name cannot be empty."
            }

        if not isinstance(error, str):
            error = str(error)

        error = error.strip()

        if not error:
            error = "Unknown error."

        recovered = fallback_result is not None

        recovery_record = {
            "operation": operation,
            "error": error,
            "recovered": recovered,
            "fallback_result": fallback_result
        }

        self.recovery_history.append(
            recovery_record.copy()
        )

        if recovered:

            return {
                "success": True,
                "recovered": True,
                "operation": operation,
                "fallback_result": fallback_result,
                "message": (
                    f"Operation '{operation}' "
                    "recovered using fallback."
                )
            }

        return {
            "success": False,
            "recovered": False,
            "operation": operation,
            "message": (
                f"Operation '{operation}' "
                "could not be recovered."
            )
        }

    # ---------------------------------
    # GET RECOVERY HISTORY
    # ---------------------------------

    def get_history(self) -> list:

        return [
            record.copy()
            for record in self.recovery_history
        ]

    # ---------------------------------
    # GET RECOVERY COUNT
    # ---------------------------------

    def get_recovery_count(self) -> int:

        return len(
            self.recovery_history
        )

    # ---------------------------------
    # CLEAR HISTORY
    # ---------------------------------

    def clear_history(self) -> dict:

        self.recovery_history.clear()

        return {
            "success": True,
            "message": (
                "Recovery history cleared successfully."
            )
        }