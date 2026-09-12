from enum import Enum


class WorkflowStatus(str, Enum):

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PAUSED = "PAUSED"


class WorkflowState:

    def __init__(
        self,
        workflow_id: str
    ):

        self.workflow_id = workflow_id

        self.status = WorkflowStatus.PENDING

        self.current_step = 0
        self.total_steps = 0

        self.results = []

        self.error = None

    # ---------------------------------
    # START WORKFLOW
    # ---------------------------------

    def start(
        self,
        total_steps: int
    ):

        if not isinstance(total_steps, int):
            raise TypeError(
                "Total steps must be an integer."
            )

        if total_steps <= 0:
            raise ValueError(
                "Total steps must be greater than 0."
            )

        self.total_steps = total_steps
        self.current_step = 0

        self.status = WorkflowStatus.RUNNING

        self.results = []
        self.error = None

    # ---------------------------------
    # MOVE TO NEXT STEP
    # ---------------------------------

    def next_step(self):

        if self.status != WorkflowStatus.RUNNING:
            return False

        if self.current_step >= self.total_steps:
            return False

        self.current_step += 1

        return True

    # ---------------------------------
    # SAVE STEP RESULT
    # ---------------------------------

    def add_result(
        self,
        result: dict
    ):

        if not isinstance(result, dict):
            raise TypeError(
                "Step result must be a dictionary."
            )

        self.results.append(result)

    # ---------------------------------
    # COMPLETE WORKFLOW
    # ---------------------------------

    def complete(self):

        if self.status == WorkflowStatus.FAILED:
            return False

        self.current_step = self.total_steps

        self.status = WorkflowStatus.COMPLETED

        self.error = None

        return True

    # ---------------------------------
    # FAIL WORKFLOW
    # ---------------------------------

    def fail(
        self,
        error: str
    ):

        self.status = WorkflowStatus.FAILED

        self.error = (
            str(error)
            if error
            else "Workflow execution failed."
        )

        return True

    # ---------------------------------
    # PAUSE WORKFLOW
    # ---------------------------------

    def pause(self):

        if self.status != WorkflowStatus.RUNNING:
            return False

        self.status = WorkflowStatus.PAUSED

        return True

    # ---------------------------------
    # RESUME WORKFLOW
    # ---------------------------------

    def resume(self):

        if self.status != WorkflowStatus.PAUSED:
            return False

        self.status = WorkflowStatus.RUNNING

        self.error = None

        return True

    # ---------------------------------
    # STATUS CHECKS
    # ---------------------------------

    def is_running(self) -> bool:

        return self.status == WorkflowStatus.RUNNING

    def is_completed(self) -> bool:

        return self.status == WorkflowStatus.COMPLETED

    def is_failed(self) -> bool:

        return self.status == WorkflowStatus.FAILED

    def is_paused(self) -> bool:

        return self.status == WorkflowStatus.PAUSED

    # ---------------------------------
    # CONVERT STATE TO DICTIONARY
    # ---------------------------------

    def to_dict(self) -> dict:

        return {
            "workflow_id": self.workflow_id,
            "status": self.status.value,
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "results": self.results,
            "error": self.error
        }