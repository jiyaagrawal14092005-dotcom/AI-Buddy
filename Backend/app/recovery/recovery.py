class RecoveryManager:

    def __init__(self):

        self.recovery_history = []

    # =========================================================
    # RECOVER OPERATION
    # =========================================================

    def recover(
        self,
        operation: str,
        error: str,
        fallback_result=None,
        retry_result=None
    ) -> dict:

        # -----------------------------------------------------
        # VALIDATE OPERATION
        # -----------------------------------------------------

        if not isinstance(
            operation,
            str
        ):
            return {
                "success": False,
                "recovered": False,
                "message": (
                    "Operation name must be text."
                )
            }

        operation = operation.strip()

        if not operation:

            return {
                "success": False,
                "recovered": False,
                "message": (
                    "Operation name cannot be empty."
                )
            }

        # -----------------------------------------------------
        # NORMALIZE ERROR
        # -----------------------------------------------------

        if not isinstance(
            error,
            str
        ):
            error = str(error)

        error = error.strip()

        if not error:
            error = "Unknown error."

        # -----------------------------------------------------
        # DETERMINE RECOVERY STATUS
        # -----------------------------------------------------

        retry_recovered = (
            isinstance(
                retry_result,
                dict
            )
            and retry_result.get(
                "success"
            ) is True
            and retry_result.get(
                "result",
                {}
            )
            is not None
        )

        fallback_recovered = (
            fallback_result is not None
        )

        recovered = (
            retry_recovered
            or fallback_recovered
        )

        # -----------------------------------------------------
        # RECOVERY METHOD
        # -----------------------------------------------------

        if retry_recovered:

            recovery_method = "retry"

        elif fallback_recovered:

            recovery_method = "fallback"

        else:

            recovery_method = "none"

        # -----------------------------------------------------
        # CREATE HISTORY RECORD
        # -----------------------------------------------------

        recovery_record = {
            "operation": operation,
            "error": error,
            "recovered": recovered,
            "recovery_method": recovery_method,
            "retry_result": retry_result,
            "fallback_result": fallback_result,
        }

        self.recovery_history.append(
            recovery_record.copy()
        )

        # -----------------------------------------------------
        # SUCCESSFUL RECOVERY
        # -----------------------------------------------------

        if recovered:

            response = {
                "success": True,
                "recovered": True,
                "operation": operation,
                "recovery_method": recovery_method,
                "message": (
                    f"Operation '{operation}' "
                    "recovered successfully."
                )
            }

            if retry_recovered:

                response["retry_result"] = (
                    retry_result
                )

            if fallback_recovered:

                response["fallback_result"] = (
                    fallback_result
                )

            return response

        # -----------------------------------------------------
        # RECOVERY FAILED
        # -----------------------------------------------------

        return {
            "success": False,
            "recovered": False,
            "operation": operation,
            "recovery_method": "none",
            "message": (
                f"Operation '{operation}' "
                "could not be recovered."
            )
        }

    # =========================================================
    # RECORD RETRY FAILURE
    # =========================================================

    def record_retry_failure(
        self,
        operation: str,
        error: str,
        attempts: int
    ) -> dict:

        if not isinstance(
            operation,
            str
        ):
            operation = "unknown"

        operation = operation.strip()

        if not operation:
            operation = "unknown"

        if not isinstance(
            error,
            str
        ):
            error = str(error)

        error = error.strip()

        if not error:
            error = "Unknown error."

        if not isinstance(
            attempts,
            int
        ):
            attempts = 0

        record = {
            "operation": operation,
            "error": error,
            "recovered": False,
            "recovery_method": "retry",
            "attempts": attempts,
        }

        self.recovery_history.append(
            record.copy()
        )

        return {
            "success": True,
            "recorded": True,
            "operation": operation,
            "attempts": attempts,
            "message": (
                "Retry failure recorded."
            )
        }

    # =========================================================
    # GET RECOVERY HISTORY
    # =========================================================

    def get_history(self) -> list:

        return [
            record.copy()
            for record in self.recovery_history
        ]

    # =========================================================
    # GET RECOVERY COUNT
    # =========================================================

    def get_recovery_count(self) -> int:

        return len(
            self.recovery_history
        )

    # =========================================================
    # GET SUCCESSFUL RECOVERIES
    # =========================================================

    def get_successful_recoveries(self) -> list:

        return [
            record.copy()
            for record in self.recovery_history
            if record.get(
                "recovered"
            ) is True
        ]

    # =========================================================
    # GET FAILED RECOVERIES
    # =========================================================

    def get_failed_recoveries(self) -> list:

        return [
            record.copy()
            for record in self.recovery_history
            if record.get(
                "recovered"
            ) is not True
        ]

    # =========================================================
    # CLEAR HISTORY
    # =========================================================

    def clear_history(self) -> dict:

        self.recovery_history.clear()

        return {
            "success": True,
            "message": (
                "Recovery history cleared successfully."
            )
        }