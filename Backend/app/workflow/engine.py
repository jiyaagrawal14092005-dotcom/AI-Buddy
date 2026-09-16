import uuid

from sqlalchemy.orm import Session

from app.workflow.state import WorkflowState
from app.workflow.steps import WorkflowStep
from app.workflow.executor import WorkflowExecutor
from app.verification.verifier import Verifier
from app.recovery.retry import RetryManager
from app.recovery.recovery import RecoveryManager


class WorkflowEngine:

    def __init__(self):
        self.executor = WorkflowExecutor()
        self.verifier = Verifier()

        # Retry and recovery managers
        self.retry_manager = RetryManager(
            max_retries=2,
            delay_seconds=1
        )

        self.recovery_manager = RecoveryManager()

    # =========================================================
    # RETRY POLICY
    # =========================================================

    def _is_retryable(
        self,
        tool: str,
        parameters: dict,
        result: dict
    ) -> bool:

        if not isinstance(result, dict):
            return True

        if result.get("success") is True:
            return False

        # -----------------------------------------------------
        # Browser actions can usually be retried because
        # temporary navigation/page failures may occur.
        # -----------------------------------------------------

        if tool == "browser":
            action = parameters.get("action")

            retryable_browser_actions = {
                "open",
                "navigate",
                "read",
                "click",
                "fill",
            }

            if action in retryable_browser_actions:
                return True

        # -----------------------------------------------------
        # Explicit retryable flag from future tools
        # -----------------------------------------------------

        if result.get("retryable") is True:
            return True

        return False

    # =========================================================
    # EXECUTE WITH RETRY + RECOVERY
    # =========================================================

    async def _execute_with_recovery(
        self,
        step: WorkflowStep,
        user_id: int,
        db: Session,
    ) -> tuple[dict, dict]:

        tool = step.tool
        parameters = step.parameters

        # -----------------------------------------------------
        # FIRST EXECUTION
        # -----------------------------------------------------

        result = await self.executor.execute_step(
            step=step,
            user_id=user_id,
            db=db,
        )

        if not isinstance(result, dict):
            result = {
                "success": False,
                "message": (
                    f"Step {step.step_id} returned "
                    "an invalid result."
                ),
            }

        # -----------------------------------------------------
        # SUCCESS
        # -----------------------------------------------------

        if result.get("success") is True:
            return result, {
                "attempted": False,
                "recovered": False,
                "recovery_method": "none",
                "message": "No recovery was required.",
            }

        # -----------------------------------------------------
        # CHECK RETRY POLICY
        # -----------------------------------------------------

        if not self._is_retryable(
            tool=tool,
            parameters=parameters,
            result=result,
        ):
            return result, {
                "attempted": False,
                "recovered": False,
                "recovery_method": "none",
                "message": "Step failure is not retryable.",
            }

        error_message = result.get(
            "message",
            f"Step {step.step_id} execution failed.",
        )

        # -----------------------------------------------------
        # RETRY OPERATION
        # -----------------------------------------------------

        async def retry_operation():
            retry_result = await self.executor.execute_step(
                step=step,
                user_id=user_id,
                db=db,
            )

            if not isinstance(retry_result, dict):
                raise RuntimeError(
                    f"Step {step.step_id} returned "
                    "an invalid result during retry."
                )

            # RetryManager retries exceptions. Therefore convert
            # an unsuccessful tool result into an exception so that
            # failed tool responses are also retried.
            if retry_result.get("success") is not True:
                raise RuntimeError(
                    retry_result.get(
                        "message",
                        f"Step {step.step_id} retry failed.",
                    )
                )

            return retry_result

        retry_result = await self.retry_manager.execute_async(
            retry_operation
        )

        # -----------------------------------------------------
        # RETRY SUCCESS
        # -----------------------------------------------------

        if retry_result.get("success") is True:

            recovery_result = self.recovery_manager.recover(
                operation=f"{tool}.{parameters.get('action', 'execute')}",
                error=str(error_message),
                retry_result=retry_result,
            )

            recovered_result = retry_result.get(
                "result"
            )

            if not isinstance(
                recovered_result,
                dict
            ):
                recovered_result = {
                    "success": True,
                    "message": (
                        "Operation recovered successfully."
                    ),
                }

            recovered_result = dict(
                recovered_result
            )

            recovered_result["recovery"] = {
                "recovered": True,
                "recovery_method": "retry",
                "attempts": retry_result.get(
                    "attempts",
                    1
                ),
            }

            return recovered_result, {
                "attempted": True,
                "recovered": True,
                "recovery_method": "retry",
                "retry_result": retry_result,
                "recovery_result": recovery_result,
                "message": "Step recovered successfully using retry.",
            }

        # -----------------------------------------------------
        # RETRY FAILED
        # -----------------------------------------------------

        retry_error = retry_result.get(
            "error",
            "Retry attempts failed."
        )

        self.recovery_manager.record_retry_failure(
            operation=f"{tool}.{parameters.get('action', 'execute')}",
            error=str(retry_error),
            attempts=retry_result.get(
                "attempts",
                0
            ),
        )

        # -----------------------------------------------------
        # FINAL FAILURE
        # -----------------------------------------------------

        final_result = dict(result)

        final_result["recovery"] = {
            "recovered": False,
            "recovery_method": "retry",
            "attempts": retry_result.get(
                "attempts",
                0
            ),
            "error": retry_error,
        }

        return final_result, {
            "attempted": True,
            "recovered": False,
            "recovery_method": "retry",
            "retry_result": retry_result,
            "message": (
                "Step could not be recovered "
                "after retry attempts."
            ),
        }

    # =========================================================
    # CREATE WORKFLOW
    # =========================================================

    async def create_workflow(
        self,
        plan: dict,
        user_id: int,
        db: Session
    ) -> dict:

        # =====================================================
        # BASIC VALIDATION
        # =====================================================

        if not isinstance(plan, dict):
            raise ValueError(
                "Plan must be a dictionary."
            )

        if not isinstance(user_id, int):
            raise ValueError(
                "user_id must be an integer."
            )

        if db is None:
            raise ValueError(
                "Database session is required."
            )

        intent = plan.get("intent")

        if not intent:
            raise ValueError(
                "Plan intent is required."
            )

        # =====================================================
        # EXTRACT WORKFLOW STEPS
        # =====================================================

        planned_steps = plan.get("steps")

        # =====================================================
        # BACKWARD COMPATIBILITY
        # =====================================================

        if not planned_steps:

            tool = plan.get("tool")

            if not tool:
                raise ValueError(
                    "Plan tool is required."
                )

            parameters = plan.get(
                "parameters",
                {}
            )

            if not isinstance(parameters, dict):
                raise ValueError(
                    "Plan parameters must be a dictionary."
                )

            # -------------------------------------------------
            # NESTED STEPS
            # -------------------------------------------------

            nested_steps = parameters.get(
                "steps"
            )

            if isinstance(
                nested_steps,
                list
            ) and nested_steps:

                planned_steps = []

                for index, item in enumerate(
                    nested_steps,
                    start=1
                ):

                    if not isinstance(
                        item,
                        dict
                    ):
                        raise ValueError(
                            f"Workflow step {index} "
                            "must be a dictionary."
                        )

                    step_tool = item.get(
                        "tool",
                        tool
                    )

                    step_parameters = item.get(
                        "parameters",
                        {}
                    )

                    if not isinstance(
                        step_parameters,
                        dict
                    ):
                        raise ValueError(
                            f"Workflow step {index} "
                            "parameters must be "
                            "a dictionary."
                        )

                    planned_steps.append(
                        {
                            "step": index,
                            "tool": step_tool,
                            "parameters": step_parameters,
                        }
                    )

            # -------------------------------------------------
            # SINGLE STEP
            # -------------------------------------------------

            else:

                planned_steps = [
                    {
                        "step": 1,
                        "tool": tool,
                        "parameters": parameters,
                    }
                ]

        # =====================================================
        # VALIDATE STEPS
        # =====================================================

        if not isinstance(
            planned_steps,
            list
        ):
            raise ValueError(
                "Plan steps must be a list."
            )

        if not planned_steps:
            raise ValueError(
                "Plan must contain at least one step."
            )

        # =====================================================
        # CREATE WORKFLOW
        # =====================================================

        workflow_id = str(
            uuid.uuid4()
        )

        state = WorkflowState(
            workflow_id
        )

        state.start(
            total_steps=len(planned_steps)
        )

        # =====================================================
        # EXECUTE STEPS SEQUENTIALLY
        # =====================================================

        for index, planned_step in enumerate(
            planned_steps,
            start=1
        ):

            # -------------------------------------------------
            # VALIDATE CURRENT STEP
            # -------------------------------------------------

            if not isinstance(
                planned_step,
                dict
            ):

                state.fail(
                    f"Step {index} is invalid."
                )

                return {
                    "success": False,
                    "workflow": state.to_dict(),
                }

            tool = planned_step.get(
                "tool"
            )

            if not tool:

                state.fail(
                    f"Step {index} does not "
                    "contain a tool."
                )

                return {
                    "success": False,
                    "workflow": state.to_dict(),
                }

            parameters = planned_step.get(
                "parameters",
                {}
            )

            if not isinstance(
                parameters,
                dict
            ):

                state.fail(
                    f"Step {index} parameters "
                    "must be a dictionary."
                )

                return {
                    "success": False,
                    "workflow": state.to_dict(),
                }

            # -------------------------------------------------
            # CREATE WORKFLOW STEP
            # -------------------------------------------------

            step = WorkflowStep(
                step_id=index,
                tool=tool,
                parameters=parameters,
            )

            # -------------------------------------------------
            # EXECUTE WITH RETRY + RECOVERY
            # -------------------------------------------------

            result, recovery = (
                await self._execute_with_recovery(
                    step=step,
                    user_id=user_id,
                    db=db,
                )
            )

            # -------------------------------------------------
            # VALIDATE EXECUTION RESULT
            # -------------------------------------------------

            if not isinstance(
                result,
                dict
            ):

                result = {
                    "success": False,
                    "message": (
                        f"Step {index} returned "
                        "an invalid result."
                    ),
                }

            # -------------------------------------------------
            # DETERMINE ACTION
            # -------------------------------------------------

            action = parameters.get(
                "action"
            )

            # -------------------------------------------------
            # VERIFY ACTION
            # -------------------------------------------------

            verification = self.verifier.verify_action(
                action=action,
                result=result,
            )

            # -------------------------------------------------
            # STORE STEP RESULT
            # -------------------------------------------------

            state.add_result(
                {
                    "step": step.to_dict(),
                    "result": result,
                    "verification": verification,
                    "recovery": recovery,
                }
            )

            # -------------------------------------------------
            # EXECUTION FAILURE
            # -------------------------------------------------

            if result.get(
                "success"
            ) is not True:

                error_message = result.get(
                    "message",
                    f"Step {index} execution failed.",
                )

                state.fail(
                    error_message
                )

                return {
                    "success": False,
                    "workflow": state.to_dict(),
                }

            # -------------------------------------------------
            # VERIFICATION FAILURE
            # -------------------------------------------------

            if verification.get(
                "verified"
            ) is not True:

                verification_message = verification.get(
                    "message",
                    f"Step {index} verification failed.",
                )

                state.fail(
                    verification_message
                )

                return {
                    "success": False,
                    "workflow": state.to_dict(),
                }

        # =====================================================
        # ALL STEPS EXECUTED AND VERIFIED
        # =====================================================

        state.complete()

        workflow_data = state.to_dict()

        # =====================================================
        # FINAL WORKFLOW VERIFICATION
        # =====================================================

        workflow_verification = (
            self.verifier.verify_workflow(
                workflow_data
            )
        )

        # -----------------------------------------------------
        # FINAL VERIFICATION FAILED
        # -----------------------------------------------------

        if workflow_verification.get(
            "verified"
        ) is not True:

            return {
                "success": False,
                "workflow": workflow_data,
                "verification": workflow_verification,
            }

        # =====================================================
        # FINAL SUCCESS
        # =====================================================

        return {
            "success": True,
            "workflow": workflow_data,
            "verification": workflow_verification,
        }