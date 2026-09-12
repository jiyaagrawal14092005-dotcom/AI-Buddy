class Verifier:

    def verify_action(
        self,
        action: str,
        result: dict
    ) -> dict:

        if not action:
            return {
                "success": False,
                "verified": False,
                "message": "Action name is required."
            }

        if not isinstance(result, dict):
            return {
                "success": False,
                "verified": False,
                "message": "Invalid action result."
            }

        action_success = result.get(
            "success",
            False
        )

        if action_success:

            return {
                "success": True,
                "verified": True,
                "action": action,
                "message": (
                    f"Action '{action}' "
                    "verified successfully."
                )
            }

        return {
            "success": True,
            "verified": False,
            "action": action,
            "message": (
                f"Action '{action}' "
                "could not be verified."
            )
        }

    def verify_workflow(
        self,
        workflow: dict
    ) -> dict:

        if not workflow:
            return {
                "success": False,
                "verified": False,
                "message": "Workflow data is required."
            }

        status = workflow.get(
            "status"
        )

        if status == "COMPLETED":

            return {
                "success": True,
                "verified": True,
                "message": (
                    "Workflow completed successfully."
                )
            }

        return {
            "success": True,
            "verified": False,
            "message": (
                f"Workflow status is '{status}'."
            )
        }

    def verify_response(
        self,
        response: dict
    ) -> dict:

        if not response:
            return {
                "success": False,
                "verified": False,
                "message": "Response is empty."
            }

        if "message" not in response:
            return {
                "success": False,
                "verified": False,
                "message": "Response message is missing."
            }

        return {
            "success": True,
            "verified": True,
            "message": "Response structure verified."
        }