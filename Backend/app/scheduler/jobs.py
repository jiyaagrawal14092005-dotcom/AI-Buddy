import uuid
from datetime import datetime


class SchedulerJob:

    VALID_STATUSES = {
        "PENDING",
        "RUNNING",
        "COMPLETED",
        "FAILED",
        "CANCELLED"
    }

    def __init__(
        self,
        name: str,
        action: str,
        parameters: dict | None = None
    ):

        if not isinstance(name, str):
            raise TypeError(
                "Job name must be text."
            )

        if not name.strip():
            raise ValueError(
                "Job name cannot be empty."
            )

        if not isinstance(action, str):
            raise TypeError(
                "Job action must be text."
            )

        if not action.strip():
            raise ValueError(
                "Job action cannot be empty."
            )

        if parameters is not None and not isinstance(
            parameters,
            dict
        ):
            raise TypeError(
                "Job parameters must be a dictionary."
            )

        self.job_id = str(uuid.uuid4())

        self.name = name.strip()

        self.action = action.strip()

        self.parameters = (
            parameters.copy()
            if parameters is not None
            else {}
        )

        self.status = "PENDING"

        self.created_at = datetime.now().isoformat()

        self.started_at = None

        self.completed_at = None

        self.result = None

        self.error = None

    # ---------------------------------
    # START JOB
    # ---------------------------------

    def start(self) -> dict:

        if self.status != "PENDING":
            return {
                "success": False,
                "message": (
                    f"Job cannot be started "
                    f"from '{self.status}' status."
                )
            }

        self.status = "RUNNING"

        self.started_at = datetime.now().isoformat()

        return {
            "success": True,
            "job_id": self.job_id,
            "status": self.status,
            "message": "Job started successfully."
        }

    # ---------------------------------
    # COMPLETE JOB
    # ---------------------------------

    def complete(
        self,
        result=None
    ) -> dict:

        if self.status != "RUNNING":
            return {
                "success": False,
                "message": (
                    f"Job cannot be completed "
                    f"from '{self.status}' status."
                )
            }

        self.status = "COMPLETED"

        self.completed_at = datetime.now().isoformat()

        self.result = result

        self.error = None

        return {
            "success": True,
            "job_id": self.job_id,
            "status": self.status,
            "message": "Job completed successfully."
        }

    # ---------------------------------
    # FAIL JOB
    # ---------------------------------

    def fail(
        self,
        error: str
    ) -> dict:

        if not isinstance(error, str):
            error = str(error)

        error = error.strip()

        if not error:
            error = "Unknown job error."

        if self.status not in {
            "PENDING",
            "RUNNING"
        }:
            return {
                "success": False,
                "message": (
                    f"Job cannot be failed "
                    f"from '{self.status}' status."
                )
            }

        self.status = "FAILED"

        self.completed_at = datetime.now().isoformat()

        self.error = error

        return {
            "success": True,
            "job_id": self.job_id,
            "status": self.status,
            "error": error,
            "message": "Job marked as failed."
        }

    # ---------------------------------
    # CANCEL JOB
    # ---------------------------------

    def cancel(self) -> dict:

        if self.status not in {
            "PENDING",
            "RUNNING"
        }:
            return {
                "success": False,
                "message": (
                    f"Job cannot be cancelled "
                    f"from '{self.status}' status."
                )
            }

        self.status = "CANCELLED"

        self.completed_at = datetime.now().isoformat()

        return {
            "success": True,
            "job_id": self.job_id,
            "status": self.status,
            "message": "Job cancelled successfully."
        }

    # ---------------------------------
    # CHECK JOB STATUS
    # ---------------------------------

    def is_completed(self) -> bool:

        return self.status == "COMPLETED"

    # ---------------------------------
    # CHECK JOB FAILURE
    # ---------------------------------

    def is_failed(self) -> bool:

        return self.status == "FAILED"

    # ---------------------------------
    # CHECK JOB CANCELLATION
    # ---------------------------------

    def is_cancelled(self) -> bool:

        return self.status == "CANCELLED"

    # ---------------------------------
    # CHECK JOB RUNNING
    # ---------------------------------

    def is_running(self) -> bool:

        return self.status == "RUNNING"

    # ---------------------------------
    # CONVERT TO DICTIONARY
    # ---------------------------------

    def to_dict(self) -> dict:

        return {
            "job_id": self.job_id,
            "name": self.name,
            "action": self.action,
            "parameters": self.parameters.copy(),
            "status": self.status,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "result": self.result,
            "error": self.error
        }