import threading
import uuid
from datetime import datetime, timedelta

from app.database.connection import SessionLocal
from app.database.models import ScheduledJob


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
        job_name: str = "AI Buddy Job",
        user_id: int | None = None,
        db=None
    ) -> dict:

        # ---------------------------------
        # VALIDATE CALLBACK
        # ---------------------------------

        if not callable(callback):

            return {
                "success": False,
                "message": "Callback must be callable."
            }

        # ---------------------------------
        # VALIDATE DELAY
        # ---------------------------------

        if not isinstance(
            delay_seconds,
            (int, float)
        ):

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

        # ---------------------------------
        # VALIDATE JOB NAME
        # ---------------------------------

        if not isinstance(
            job_name,
            str
        ):

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

        # ---------------------------------
        # VALIDATE USER ID
        # ---------------------------------

        if user_id is not None:

            if not isinstance(
                user_id,
                int
            ):

                return {
                    "success": False,
                    "message": (
                        "User ID must be an integer."
                    )
                }

            if user_id <= 0:

                return {
                    "success": False,
                    "message": (
                        "User ID must be greater than zero."
                    )
                }

        # ---------------------------------
        # CREATE JOB ID
        # ---------------------------------

        job_id = str(
            uuid.uuid4()
        )

        run_at = (
            datetime.now()
            + timedelta(
                seconds=delay_seconds
            )
        )

        # ---------------------------------
        # CREATE TIMER
        # ---------------------------------

        timer = threading.Timer(
            delay_seconds,
            self._execute_job,
            args=(job_id,)
        )

        timer.daemon = True

        # ---------------------------------
        # CREATE IN-MEMORY JOB
        # ---------------------------------

        job = {
            "job_id": job_id,
            "job_name": job_name,
            "status": "SCHEDULED",
            "run_at": run_at.isoformat(),
            "callback": callback,
            "timer": timer,
            "user_id": user_id,
            "database_id": None
        }

        # ---------------------------------
        # SAVE TO DATABASE
        # ---------------------------------

        database_id = None

        if user_id is not None:

            database = db
            close_database = False

            if database is None:

                database = SessionLocal()
                close_database = True

            try:

                scheduled_job = ScheduledJob(
                    user_id=user_id,
                    name=job_name,
                    schedule=run_at.isoformat(),
                    status="scheduled"
                )

                database.add(
                    scheduled_job
                )

                database.commit()

                database.refresh(
                    scheduled_job
                )

                database_id = scheduled_job.id

            except Exception as error:

                database.rollback()

                return {
                    "success": False,
                    "message": (
                        "Job could not be saved "
                        "to database."
                    ),
                    "error": str(error)
                }

            finally:

                if close_database:

                    database.close()

        job["database_id"] = database_id

        # ---------------------------------
        # STORE JOB
        # ---------------------------------

        with self.lock:

            self.jobs[job_id] = job

        # ---------------------------------
        # START TIMER
        # ---------------------------------

        timer.start()

        return {
            "success": True,
            "job_id": job_id,
            "job_name": job_name,
            "status": "SCHEDULED",
            "run_at": run_at.isoformat(),
            "database_id": database_id,
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

            job = self.jobs.get(
                job_id
            )

            if not job:

                return

            if job["status"] != "SCHEDULED":

                return

            job["status"] = "RUNNING"

            database_id = job.get(
                "database_id"
            )

        # ---------------------------------
        # UPDATE DATABASE → RUNNING
        # ---------------------------------

        self._update_database_status(
            database_id,
            "running"
        )

        try:

            callback = job["callback"]

            result = callback()

            with self.lock:

                job["result"] = result
                job["status"] = "COMPLETED"

            # ---------------------------------
            # UPDATE DATABASE → COMPLETED
            # ---------------------------------

            self._update_database_status(
                database_id,
                "completed"
            )

        except Exception as error:

            with self.lock:

                job["error"] = str(error)
                job["status"] = "FAILED"

            # ---------------------------------
            # UPDATE DATABASE → FAILED
            # ---------------------------------

            self._update_database_status(
                database_id,
                "failed"
            )

    # ---------------------------------
    # UPDATE DATABASE STATUS
    # ---------------------------------

    def _update_database_status(
        self,
        database_id: int | None,
        status: str
    ):

        if database_id is None:

            return

        database = SessionLocal()

        try:

            scheduled_job = (
                database.query(
                    ScheduledJob
                )
                .filter(
                    ScheduledJob.id == database_id
                )
                .first()
            )

            if scheduled_job is None:

                return

            scheduled_job.status = status

            database.commit()

        except Exception:

            database.rollback()

        finally:

            database.close()

    # ---------------------------------
    # GET SINGLE JOB
    # ---------------------------------

    def get_job(
        self,
        job_id: str
    ) -> dict:

        if not isinstance(
            job_id,
            str
        ):

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

            job = self.jobs.get(
                job_id
            )

            if not job:

                return {
                    "success": False,
                    "message": "Job not found."
                }

            clean_job = self._clean_job(
                job
            )

        return {
            "success": True,
            "job": clean_job
        }

    # ---------------------------------
    # GET ALL JOBS
    # ---------------------------------

    def get_all_jobs(
        self
    ) -> list:

        with self.lock:

            jobs = list(
                self.jobs.values()
            )

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

        if not isinstance(
            job_id,
            str
        ):

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

            job = self.jobs.get(
                job_id
            )

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

            database_id = job.get(
                "database_id"
            )

        # ---------------------------------
        # UPDATE DATABASE
        # ---------------------------------

        self._update_database_status(
            database_id,
            "cancelled"
        )

        return {
            "success": True,
            "job_id": job_id,
            "database_id": database_id,
            "status": "CANCELLED",
            "message": (
                "Job cancelled successfully."
            )
        }

    # ---------------------------------
    # REMOVE JOB
    # ---------------------------------

    def remove_job(
        self,
        job_id: str
    ) -> dict:

        if not isinstance(
            job_id,
            str
        ):

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

            job = self.jobs.get(
                job_id
            )

            if not job:

                return {
                    "success": False,
                    "message": "Job not found."
                }

            if job["status"] == "SCHEDULED":

                job["timer"].cancel()

            database_id = job.get(
                "database_id"
            )

            del self.jobs[
                job_id
            ]

        return {
            "success": True,
            "job_id": job_id,
            "database_id": database_id,
            "message": (
                "Job removed successfully."
            )
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