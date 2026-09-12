import threading
import uuid
from datetime import datetime, timedelta


class Scheduler:

    def __init__(self):

        self.jobs = {}
        self.lock = threading.Lock()

    # ---------------------------------
    # SCHEDULE ONE-TIME JOB
    # ---------------------------------

    def schedule(
        self,
        callback,
        delay_seconds: int,
        job_name: str = "AI Buddy Job"
    ) -> dict:

        if not callable(callback):
            return {
                "success": False,
                "message": "Callback must be callable."
            }

        if not isinstance(delay_seconds, (int, float)):
            return {
                "success": False,
                "message": "Delay must be a number."
            }

        if delay_seconds <= 0:
            return {
                "success": False,
                "message": (
                    "Delay must be greater than 0 seconds."
                )
            }

        if not isinstance(job_name, str):
            return {
                "success": False,
                "message": "Job name must be text."
            }

        job_name = job_name.strip()

        if not job_name:
            return {
                "success": False,
                "message": "Job name cannot be empty."
            }

        job_id = str(uuid.uuid4())

        run_at = datetime.now() + timedelta(
            seconds=delay_seconds
        )

        timer = threading.Timer(
            delay_seconds,
            self._execute_job,
            args=(job_id,)
        )

        timer.daemon = True

        job = {
            "job_id": job_id,
            "job_name": job_name,
            "status": "SCHEDULED",
            "run_at": run_at.isoformat(),
            "callback": callback,
            "timer": timer
        }

        with self.lock:
            self.jobs[job_id] = job

        timer.start()

        return {
            "success": True,
            "job_id": job_id,
            "job_name": job_name,
            "status": "SCHEDULED",
            "run_at": run_at.isoformat(),
            "message": (
                f"Job '{job_name}' "
                "scheduled successfully."
            )
        }

    # ---------------------------------
    # EXECUTE JOB
    # ---------------------------------

    def _execute_job(
        self,
        job_id: str
    ):

        with self.lock:
            job = self.jobs.get(job_id)

            if not job:
                return

            if job["status"] != "SCHEDULED":
                return

            job["status"] = "RUNNING"

        try:

            callback = job["callback"]

            result = callback()

            with self.lock:
                job["result"] = result
                job["status"] = "COMPLETED"

        except Exception as error:

            with self.lock:
                job["error"] = str(error)
                job["status"] = "FAILED"

    # ---------------------------------
    # GET JOB
    # ---------------------------------

    def get_job(
        self,
        job_id: str
    ) -> dict:

        if not isinstance(job_id, str):
            return {
                "success": False,
                "message": "Job ID must be text."
            }

        job_id = job_id.strip()

        if not job_id:
            return {
                "success": False,
                "message": "Job ID cannot be empty."
            }

        with self.lock:
            job = self.jobs.get(job_id)

            if not job:
                return {
                    "success": False,
                    "message": "Job not found."
                }

            clean_job = self._clean_job(job)

        return {
            "success": True,
            "job": clean_job
        }

    # ---------------------------------
    # GET ALL JOBS
    # ---------------------------------

    def get_all_jobs(self) -> list:

        with self.lock:
            jobs = list(self.jobs.values())

            return [
                self._clean_job(job)
                for job in jobs
            ]

    # ---------------------------------
    # CANCEL JOB
    # ---------------------------------

    def cancel_job(
        self,
        job_id: str
    ) -> dict:

        if not isinstance(job_id, str):
            return {
                "success": False,
                "message": "Job ID must be text."
            }

        job_id = job_id.strip()

        if not job_id:
            return {
                "success": False,
                "message": "Job ID cannot be empty."
            }

        with self.lock:
            job = self.jobs.get(job_id)

            if not job:
                return {
                    "success": False,
                    "message": "Job not found."
                }

            if job["status"] != "SCHEDULED":
                return {
                    "success": False,
                    "message": (
                        "Only scheduled jobs "
                        "can be cancelled."
                    )
                }

            job["timer"].cancel()
            job["status"] = "CANCELLED"

        return {
            "success": True,
            "job_id": job_id,
            "message": "Job cancelled successfully."
        }

    # ---------------------------------
    # REMOVE JOB
    # ---------------------------------

    def remove_job(
        self,
        job_id: str
    ) -> dict:

        if not isinstance(job_id, str):
            return {
                "success": False,
                "message": "Job ID must be text."
            }

        job_id = job_id.strip()

        if not job_id:
            return {
                "success": False,
                "message": "Job ID cannot be empty."
            }

        with self.lock:
            job = self.jobs.get(job_id)

            if not job:
                return {
                    "success": False,
                    "message": "Job not found."
                }

            if job["status"] == "SCHEDULED":
                job["timer"].cancel()

            del self.jobs[job_id]

        return {
            "success": True,
            "job_id": job_id,
            "message": "Job removed successfully."
        }

    # ---------------------------------
    # CLEAN JOB DATA
    # ---------------------------------

    def _clean_job(
        self,
        job: dict
    ) -> dict:

        return {
            key: value
            for key, value in job.items()
            if key not in {
                "timer",
                "callback"
            }
        }