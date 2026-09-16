import asyncio
import inspect
import time


class RetryManager:

    def __init__(
        self,
        max_retries: int = 3,
        delay_seconds: int | float = 1
    ):

        if not isinstance(max_retries, int):
            raise TypeError(
                "Maximum retries must be an integer."
            )

        if max_retries < 0:
            raise ValueError(
                "Maximum retries cannot be negative."
            )

        if not isinstance(
            delay_seconds,
            (int, float)
        ):
            raise TypeError(
                "Delay must be a number."
            )

        if delay_seconds < 0:
            raise ValueError(
                "Delay cannot be negative."
            )

        self.max_retries = max_retries
        self.delay_seconds = delay_seconds

    # =========================================================
    # SYNCHRONOUS RETRY
    # =========================================================

    def execute(
        self,
        operation,
        *args,
        **kwargs
    ) -> dict:

        if not callable(operation):
            return {
                "success": False,
                "attempts": 0,
                "error": "Operation is not callable.",
                "message": "Invalid operation."
            }

        last_error = None

        total_attempts = (
            self.max_retries + 1
        )

        for attempt in range(
            1,
            total_attempts + 1
        ):

            try:

                result = operation(
                    *args,
                    **kwargs
                )

                # -------------------------------------------------
                # Do not automatically treat a returned
                # {"success": False} as an exception.
                # The caller can inspect the result.
                # -------------------------------------------------

                return {
                    "success": True,
                    "attempts": attempt,
                    "result": result,
                    "message": (
                        "Operation completed successfully."
                    )
                }

            except Exception as error:

                last_error = str(error)

                if attempt < total_attempts:

                    if self.delay_seconds > 0:

                        time.sleep(
                            self.delay_seconds
                        )

        return {
            "success": False,
            "attempts": total_attempts,
            "error": last_error,
            "message": (
                "Operation failed after "
                "all retry attempts."
            )
        }

    # =========================================================
    # ASYNCHRONOUS RETRY
    # =========================================================

    async def execute_async(
        self,
        operation,
        *args,
        **kwargs
    ) -> dict:

        if not callable(operation):
            return {
                "success": False,
                "attempts": 0,
                "error": "Operation is not callable.",
                "message": "Invalid operation."
            }

        last_error = None

        total_attempts = (
            self.max_retries + 1
        )

        for attempt in range(
            1,
            total_attempts + 1
        ):

            try:

                result = operation(
                    *args,
                    **kwargs
                )

                # -------------------------------------------------
                # Support both normal and async operations.
                # -------------------------------------------------

                if inspect.isawaitable(result):
                    result = await result

                return {
                    "success": True,
                    "attempts": attempt,
                    "result": result,
                    "message": (
                        "Operation completed successfully."
                    )
                }

            except Exception as error:

                last_error = str(error)

                if attempt < total_attempts:

                    if self.delay_seconds > 0:

                        await asyncio.sleep(
                            self.delay_seconds
                        )

        return {
            "success": False,
            "attempts": total_attempts,
            "error": last_error,
            "message": (
                "Operation failed after "
                "all retry attempts."
            )
        }

    # =========================================================
    # CONFIGURATION
    # =========================================================

    def get_configuration(self) -> dict:

        return {
            "max_retries": self.max_retries,
            "delay_seconds": self.delay_seconds
        }