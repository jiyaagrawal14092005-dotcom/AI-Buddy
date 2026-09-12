class ErrorHandler:

    # ---------------------------------
    # HANDLE ERROR
    # ---------------------------------

    def handle(
        self,
        error: Exception,
        operation: str = ""
    ) -> dict:

        if error is None:
            return {
                "success": False,
                "error_type": "UnknownError",
                "message": "An unknown error occurred."
            }

        error_type = type(error).__name__

        error_message = str(error)

        if not error_message:
            error_message = "An unexpected error occurred."

        operation = (
            operation.strip()
            if isinstance(operation, str)
            else ""
        )

        response = {
            "success": False,
            "error_type": error_type,
            "message": error_message
        }

        if operation:
            response["operation"] = operation

        return response

    # ---------------------------------
    # CREATE ERROR RESPONSE
    # ---------------------------------

    def create_error_response(
        self,
        message: str,
        error_type: str = "ApplicationError"
    ) -> dict:

        if not isinstance(message, str):
            message = str(message)

        message = message.strip()

        if not message:
            message = "An application error occurred."

        if not isinstance(error_type, str):
            error_type = "ApplicationError"

        error_type = error_type.strip()

        if not error_type:
            error_type = "ApplicationError"

        return {
            "success": False,
            "error_type": error_type,
            "message": message
        }

    # ---------------------------------
    # HANDLE VALIDATION ERROR
    # ---------------------------------

    def handle_validation_error(
        self,
        message: str
    ) -> dict:

        return self.create_error_response(
            message,
            "ValidationError"
        )

    # ---------------------------------
    # HANDLE TOOL ERROR
    # ---------------------------------

    def handle_tool_error(
        self,
        tool: str,
        error: Exception
    ) -> dict:

        if not isinstance(tool, str):
            tool = "unknown"

        tool = tool.strip()

        if not tool:
            tool = "unknown"

        error_message = str(error)

        if not error_message:
            error_message = "Tool execution failed."

        return {
            "success": False,
            "error_type": "ToolError",
            "tool": tool,
            "message": error_message
        }

    # ---------------------------------
    # HANDLE WORKFLOW ERROR
    # ---------------------------------

    def handle_workflow_error(
        self,
        workflow_id: str,
        error: Exception
    ) -> dict:

        if not isinstance(workflow_id, str):
            workflow_id = "unknown"

        workflow_id = workflow_id.strip()

        if not workflow_id:
            workflow_id = "unknown"

        error_message = str(error)

        if not error_message:
            error_message = "Workflow execution failed."

        return {
            "success": False,
            "error_type": "WorkflowError",
            "workflow_id": workflow_id,
            "message": error_message
        }

    # ---------------------------------
    # CHECK ERROR
    # ---------------------------------

    def has_error(
        self,
        result: dict
    ) -> bool:

        if not isinstance(result, dict):
            return True

        return result.get("success") is False