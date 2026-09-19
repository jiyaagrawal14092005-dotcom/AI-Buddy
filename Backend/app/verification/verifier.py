class Verifier:

    # =========================================================
    # ACTION VERIFICATION
    # =========================================================

    def verify_action(
        self,
        action: str,
        result: dict
    ) -> dict:

        if not isinstance(result, dict):
            return {
                "success": False,
                "verified": False,
                "action": action,
                "message": "Invalid action result."
            }

        # -----------------------------------------------------
        # RESULT EXECUTION CHECK
        # -----------------------------------------------------

        action_success = result.get(
            "success",
            False
        )

        if action_success is not True:
            return {
                "success": False,
                "verified": False,
                "action": action,
                "message": (
                    f"Action '{action}' "
                    "execution failed."
                )
            }

        # -----------------------------------------------------
        # ACTION NAME IS OPTIONAL FOR GENERIC TOOLS
        # -----------------------------------------------------

        if not action:

            return {
                "success": True,
                "verified": True,
                "action": None,
                "verification_type": "execution_success",
                "message": (
                    "Workflow step executed successfully."
                )
            }

        action = str(action).strip().lower()

        # -----------------------------------------------------
        # BROWSER ACTIONS
        # -----------------------------------------------------

        if action in {
            "open",
            "navigate",
            "click",
            "fill",
            "read",
            "close"
        }:

            return self._verify_browser_action(
                action=action,
                result=result
            )

        # -----------------------------------------------------
        # GENERIC ACTION
        # -----------------------------------------------------

        return {
            "success": True,
            "verified": True,
            "action": action,
            "verification_type": "execution_success",
            "message": (
                f"Action '{action}' "
                "verified successfully."
            )
        }

    # =========================================================
    # BROWSER ACTION VERIFICATION
    # =========================================================

    def _verify_browser_action(
        self,
        action: str,
        result: dict
    ) -> dict:

        browser = result.get(
            "browser"
        )

        if not isinstance(browser, dict):
            return {
                "success": False,
                "verified": False,
                "action": action,
                "message": (
                    "Browser verification failed: "
                    "browser result data is missing."
                )
            }

        # -----------------------------------------------------
        # OPEN / NAVIGATE
        # -----------------------------------------------------

        if action in {
            "open",
            "navigate"
        }:

            final_url = browser.get(
                "final_url"
            )

            if not final_url:
                return {
                    "success": False,
                    "verified": False,
                    "action": action,
                    "message": (
                        "Browser navigation completed "
                        "but final URL is missing."
                    )
                }

            return {
                "success": True,
                "verified": True,
                "action": action,
                "verification_type": "navigation",
                "details": {
                    "final_url": final_url,
                    "title": browser.get(
                        "title"
                    ),
                    "status_code": browser.get(
                        "status_code"
                    )
                },
                "message": (
                    f"Browser action '{action}' "
                    "verified successfully."
                )
            }

        # -----------------------------------------------------
        # CLICK
        # -----------------------------------------------------

        if action == "click":

            final_url = browser.get(
                "final_url"
            )

            return {
                "success": True,
                "verified": True,
                "action": action,
                "verification_type": "click",
                "details": {
                    "final_url": final_url,
                    "title": browser.get(
                        "title"
                    )
                },
                "message": (
                    "Browser click action "
                    "verified successfully."
                )
            }

        # -----------------------------------------------------
        # FILL
        # -----------------------------------------------------

        if action == "fill":

            value_length = browser.get(
                "value_length"
            )

            if value_length is None:
                return {
                    "success": True,
                    "verified": True,
                    "action": action,
                    "verification_type": "input_fill",
                    "details": {},
                    "message": (
                        "Browser fill action "
                        "executed successfully; "
                        "value length was not reported."
                    )
                }

            if value_length < 0:
                return {
                    "success": False,
                    "verified": False,
                    "action": action,
                    "message": (
                        "Browser fill returned "
                        "an invalid value length."
                    )
                }

            return {
                "success": True,
                "verified": True,
                "action": action,
                "verification_type": "input_fill",
                "details": {
                    "value_length": value_length
                },
                "message": (
                    "Browser fill action "
                    "verified successfully."
                )
            }

        # -----------------------------------------------------
        # READ
        # -----------------------------------------------------

        if action == "read":

            content = browser.get(
                "content"
            )

            if content is None:
                return {
                    "success": False,
                    "verified": False,
                    "action": action,
                    "message": (
                        "Browser read action "
                        "returned no content."
                    )
                }

            content = str(content)

            if not content.strip():
                return {
                    "success": False,
                    "verified": False,
                    "action": action,
                    "message": (
                        "Browser read action "
                        "returned empty content."
                    )
                }

            return {
                "success": True,
                "verified": True,
                "action": action,
                "verification_type": "page_read",
                "details": {
                    "content_length": len(content),
                    "final_url": browser.get(
                        "final_url"
                    ),
                    "title": browser.get(
                        "title"
                    )
                },
                "message": (
                    "Browser read action "
                    "verified successfully."
                )
            }

        # -----------------------------------------------------
        # CLOSE
        # -----------------------------------------------------

        if action == "close":

            return {
                "success": True,
                "verified": True,
                "action": action,
                "verification_type": "session_close",
                "details": {
                    "was_active": browser.get(
                        "was_active"
                    )
                },
                "message": (
                    "Browser close action "
                    "verified successfully."
                )
            }

        # -----------------------------------------------------
        # FALLBACK
        # -----------------------------------------------------

        return {
            "success": True,
            "verified": True,
            "action": action,
            "verification_type": "execution_success",
            "message": (
                f"Browser action '{action}' "
                "executed successfully."
            )
        }

    # =========================================================
    # WORKFLOW VERIFICATION
    # =========================================================

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

            results = workflow.get(
                "results",
                []
            )

            # -------------------------------------------------
            # COMPLETED WORKFLOW MUST HAVE RESULTS
            # -------------------------------------------------

            if not isinstance(results, list):
                return {
                    "success": False,
                    "verified": False,
                    "message": (
                        "Workflow results are invalid."
                    )
                }

            if not results:
                return {
                    "success": False,
                    "verified": False,
                    "message": (
                        "Workflow is marked COMPLETED "
                        "but contains no step results."
                    )
                }

            # -------------------------------------------------
            # VERIFY EVERY STEP RESULT
            # -------------------------------------------------

            failed_steps = []

            for index, step_result in enumerate(
                results,
                start=1
            ):

                if not isinstance(
                    step_result,
                    dict
                ):
                    failed_steps.append(index)
                    continue

                execution_result = step_result.get(
                    "result"
                )

                if not isinstance(
                    execution_result,
                    dict
                ):
                    failed_steps.append(index)
                    continue

                if execution_result.get(
                    "success"
                ) is not True:
                    failed_steps.append(index)

            if failed_steps:

                return {
                    "success": False,
                    "verified": False,
                    "message": (
                        "Workflow is marked COMPLETED "
                        "but one or more steps failed."
                    ),
                    "failed_steps": failed_steps
                }

            return {
                "success": True,
                "verified": True,
                "message": (
                    "Workflow and all step results "
                    "verified successfully."
                ),
                "total_steps": len(results)
            }

        # -----------------------------------------------------
        # WORKFLOW NOT COMPLETED
        # -----------------------------------------------------

        return {
            "success": True,
            "verified": False,
            "message": (
                f"Workflow status is '{status}'."
            )
        }

    # =========================================================
    # RESPONSE VERIFICATION
    # =========================================================

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