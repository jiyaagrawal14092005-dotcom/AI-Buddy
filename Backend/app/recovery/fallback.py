class FallbackManager:

    def __init__(self):

        self.fallbacks = {}

    # ---------------------------------
    # REGISTER FALLBACK
    # ---------------------------------

    def register_fallback(
        self,
        operation: str,
        fallback
    ) -> dict:

        if not isinstance(operation, str):
            return {
                "success": False,
                "message": "Operation name must be text."
            }

        operation = operation.strip()

        if not operation:
            return {
                "success": False,
                "message": "Operation name cannot be empty."
            }

        if not callable(fallback):
            return {
                "success": False,
                "message": "Fallback must be callable."
            }

        self.fallbacks[operation] = fallback

        return {
            "success": True,
            "operation": operation,
            "message": "Fallback registered successfully."
        }

    # ---------------------------------
    # EXECUTE FALLBACK
    # ---------------------------------

    def execute_fallback(
        self,
        operation: str,
        *args,
        **kwargs
    ) -> dict:

        if not isinstance(operation, str):
            return {
                "success": False,
                "message": "Operation name must be text."
            }

        operation = operation.strip()

        if not operation:
            return {
                "success": False,
                "message": "Operation name cannot be empty."
            }

        fallback = self.fallbacks.get(
            operation
        )

        if fallback is None:
            return {
                "success": False,
                "operation": operation,
                "message": "No fallback registered."
            }

        try:

            result = fallback(
                *args,
                **kwargs
            )

            return {
                "success": True,
                "operation": operation,
                "result": result,
                "message": (
                    "Fallback executed successfully."
                )
            }

        except Exception as error:

            return {
                "success": False,
                "operation": operation,
                "error": str(error),
                "message": "Fallback execution failed."
            }

    # ---------------------------------
    # REMOVE FALLBACK
    # ---------------------------------

    def remove_fallback(
        self,
        operation: str
    ) -> dict:

        if not isinstance(operation, str):
            return {
                "success": False,
                "message": "Operation name must be text."
            }

        operation = operation.strip()

        if not operation:
            return {
                "success": False,
                "message": "Operation name cannot be empty."
            }

        if operation not in self.fallbacks:
            return {
                "success": False,
                "message": "Fallback not found."
            }

        del self.fallbacks[operation]

        return {
            "success": True,
            "operation": operation,
            "message": "Fallback removed successfully."
        }

    # ---------------------------------
    # LIST FALLBACKS
    # ---------------------------------

    def list_fallbacks(self) -> list:

        return list(
            self.fallbacks.keys()
        )

    # ---------------------------------
    # CLEAR FALLBACKS
    # ---------------------------------

    def clear(self) -> dict:

        self.fallbacks.clear()

        return {
            "success": True,
            "message": (
                "All fallbacks cleared successfully."
            )
        }