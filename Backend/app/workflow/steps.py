class WorkflowStep:

    VALID_STATUSES = {
        "PENDING",
        "RUNNING",
        "COMPLETED",
        "FAILED"
    }

    def __init__(
        self,
        step_id: int,
        tool: str,
        parameters: dict | None = None
    ):

        self.step_id = step_id
        self.tool = tool
        self.parameters = parameters or {}

        self.status = "PENDING"
        self.result = None
        self.error = None

    # ---------------------------------
    # Start step
    # ---------------------------------

    def start(self):

        self.status = "RUNNING"

        self.result = None
        self.error = None

    # ---------------------------------
    # Complete step
    # ---------------------------------

    def complete(
        self,
        result: dict
    ):

        self.status = "COMPLETED"

        self.result = result

        self.error = None

    # ---------------------------------
    # Fail step
    # ---------------------------------

    def fail(
        self,
        error: str
    ):

        self.status = "FAILED"

        self.error = (
            str(error)
            if error
            else "Step execution failed."
        )

    # ---------------------------------
    # Check whether step is completed
    # ---------------------------------

    def is_completed(self) -> bool:

        return self.status == "COMPLETED"

    # ---------------------------------
    # Check whether step failed
    # ---------------------------------

    def is_failed(self) -> bool:

        return self.status == "FAILED"

    # ---------------------------------
    # Check whether step is running
    # ---------------------------------

    def is_running(self) -> bool:

        return self.status == "RUNNING"

    # ---------------------------------
    # Convert step to dictionary
    # ---------------------------------

    def to_dict(self) -> dict:

        return {
            "step_id": self.step_id,
            "tool": self.tool,
            "parameters": self.parameters,
            "status": self.status,
            "result": self.result,
            "error": self.error
        }