import uuid

from sqlalchemy.orm import Session

from app.workflow.state import WorkflowState
from app.workflow.steps import WorkflowStep
from app.workflow.executor import WorkflowExecutor


class WorkflowEngine:

    def __init__(self):

        self.executor = WorkflowExecutor()

    # ---------------------------------
    # CREATE WORKFLOW
    # ---------------------------------

    def create_workflow(
        self,
        plan: dict,
        user_id: int,
        db: Session
    ) -> dict:

        # ---------------------------------
        # VALIDATE PLAN
        # ---------------------------------

        if not isinstance(plan, dict):
            return {
                "success": False,
                "message": "Workflow plan must be a dictionary."
            }

        # ---------------------------------
        # VALIDATE USER ID
        # ---------------------------------

        if not isinstance(user_id, int):
            return {
                "success": False,
                "message": "User ID must be an integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "message": "User ID must be greater than zero."
            }

        # ---------------------------------
        # VALIDATE DATABASE SESSION
        # ---------------------------------

        if db is None:
            return {
                "success": False,
                "message": "Database session is required."
            }

        # ---------------------------------
        # GET TOOL
        # ---------------------------------

        tool = plan.get("tool")

        if not isinstance(tool, str):
            return {
                "success": False,
                "message": "Workflow tool must be text."
            }

        tool = tool.strip()

        if not tool:
            return {
                "success": False,
                "message": "Cannot create workflow without a tool."
            }

        # ---------------------------------
        # VALIDATE PARAMETERS
        # ---------------------------------

        parameters = plan.get(
            "parameters",
            {}
        )

        if parameters is None:
            parameters = {}

        if not isinstance(parameters, dict):
            return {
                "success": False,
                "message": "Workflow parameters must be a dictionary."
            }

        # ---------------------------------
        # CREATE WORKFLOW ID
        # ---------------------------------

        workflow_id = str(
            uuid.uuid4()
        )

        # ---------------------------------
        # CREATE WORKFLOW STEP
        # ---------------------------------

        step = WorkflowStep(
            step_id=1,
            tool=tool,
            parameters=parameters
        )

        # ---------------------------------
        # CREATE WORKFLOW STATE
        # ---------------------------------

        state = WorkflowState(
            workflow_id
        )

        state.start(
            total_steps=1
        )

        # ---------------------------------
        # EXECUTE STEP
        # ---------------------------------

        try:

            result = self.executor.execute_step(
                step,
                user_id,
                db
            )

        except Exception as error:

            state.fail(
                "Workflow execution failed."
            )

            return {
                "success": False,
                "workflow": state.to_dict(),
                "message": "Workflow execution failed.",
                "error": str(error)
            }

        # ---------------------------------
        # VALIDATE EXECUTOR RESULT
        # ---------------------------------

        if not isinstance(result, dict):

            state.fail(
                "Invalid workflow execution result."
            )

            return {
                "success": False,
                "workflow": state.to_dict(),
                "message": (
                    "Workflow executor returned "
                    "an invalid result."
                )
            }

        # ---------------------------------
        # SAVE RESULT
        # ---------------------------------

        state.add_result(
            {
                "step": step.to_dict(),
                "result": result
            }
        )

        # ---------------------------------
        # UPDATE WORKFLOW STATUS
        # ---------------------------------

        if result.get("success") is True:

            state.complete()

        else:

            state.fail(
                result.get(
                    "message",
                    "Workflow execution failed."
                )
            )

        # ---------------------------------
        # RETURN WORKFLOW
        # ---------------------------------

        return {
            "success": result.get(
                "success",
                False
            ),
            "workflow": state.to_dict()
        }