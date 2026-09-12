from datetime import datetime


class StatusChecker:

    def check_action_status(
        self,
        result: dict
    ) -> dict:

        if not isinstance(result, dict):
            return {
                "success": False,
                "status": "INVALID",
                "message": "Invalid action result."
            }

        if "success" not in result:
            return {
                "success": False,
                "status": "INVALID",
                "message": "Action result status is missing."
            }

        if not isinstance(result["success"], bool):
            return {
                "success": False,
                "status": "INVALID",
                "message": "Action success status must be boolean."
            }

        if result["success"] is True:
            return {
                "success": True,
                "status": "COMPLETED",
                "message": "Action completed successfully."
            }

        return {
            "success": True,
            "status": "FAILED",
            "message": result.get(
                "message",
                "Action failed."
            )
        }

    def check_workflow_status(
        self,
        workflow: dict
    ) -> dict:

        if not isinstance(workflow, dict):
            return {
                "success": False,
                "status": "INVALID",
                "message": "Invalid workflow data."
            }

        status = workflow.get("status")

        if status is None:
            return {
                "success": False,
                "status": "UNKNOWN",
                "workflow_id": workflow.get(
                    "workflow_id"
                ),
                "message": "Workflow status is missing."
            }

        if not isinstance(status, str):
            return {
                "success": False,
                "status": "INVALID",
                "workflow_id": workflow.get(
                    "workflow_id"
                ),
                "message": "Workflow status must be text."
            }

        status = status.strip().upper()

        if not status:
            return {
                "success": False,
                "status": "UNKNOWN",
                "workflow_id": workflow.get(
                    "workflow_id"
                ),
                "message": "Workflow status cannot be empty."
            }

        return {
            "success": True,
            "status": status,
            "workflow_id": workflow.get(
                "workflow_id"
            ),
            "message": (
                f"Workflow status: {status}."
            )
        }

    def create_status_record(
        self,
        operation: str,
        status: str
    ) -> dict:

        if not operation:
            return {
                "success": False,
                "message": "Operation name is required."
            }

        if not isinstance(operation, str):
            return {
                "success": False,
                "message": "Operation name must be text."
            }

        if not isinstance(status, str):
            return {
                "success": False,
                "message": "Status must be text."
            }

        operation = operation.strip()
        status = status.strip().upper()

        if not operation:
            return {
                "success": False,
                "message": "Operation name cannot be empty."
            }

        if not status:
            return {
                "success": False,
                "message": "Status cannot be empty."
            }

        return {
            "success": True,
            "operation": operation,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }

    def is_successful(
        self,
        status: str
    ) -> bool:

        if not isinstance(status, str):
            return False

        return status.strip().upper() in {
            "COMPLETED",
            "SUCCESS",
            "APPROVED"
        }

    def is_failed(
        self,
        status: str
    ) -> bool:

        if not isinstance(status, str):
            return False

        return status.strip().upper() in {
            "FAILED",
            "REJECTED",
            "CANCELLED"
        }