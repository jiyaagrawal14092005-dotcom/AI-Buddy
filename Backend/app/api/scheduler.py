from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import ScheduledJob
from app.scheduler.scheduler import Scheduler


router = APIRouter(
    prefix="/scheduler",
    tags=["Scheduler"]
)


scheduler = Scheduler()


# ---------------------------------
# SCHEDULER STATUS
# ---------------------------------

@router.get("/status")
def scheduler_status():

    return {
        "success": True,
        "service": "scheduler",
        "status": "ready",
        "database": "connected"
    }


# ---------------------------------
# GET ALL RUNTIME JOBS
# ---------------------------------

@router.get("/jobs")
def get_jobs():

    return {
        "success": True,
        "jobs": scheduler.get_all_jobs()
    }


# ---------------------------------
# GET DATABASE JOBS
# ---------------------------------

@router.get("/database-jobs")
def get_database_jobs(
    user_id: int,
    db: Session = Depends(get_db)
):

    jobs = (
        db.query(
            ScheduledJob
        )
        .filter(
            ScheduledJob.user_id == user_id
        )
        .order_by(
            ScheduledJob.created_at.desc()
        )
        .all()
    )

    return {
        "success": True,
        "jobs": [
            {
                "id": job.id,
                "user_id": job.user_id,
                "name": job.name,
                "schedule": job.schedule,
                "status": job.status,
                "created_at": job.created_at
            }
            for job in jobs
        ]
    }


# ---------------------------------
# SCHEDULE JOB
# ---------------------------------

@router.post("/schedule")
def schedule_job(
    user_id: int,
    delay_seconds: int,
    name: str = "AI Buddy Job",
    db: Session = Depends(get_db)
):

    def callback():

        return {
            "success": True,
            "message": (
                f"Scheduled job '{name}' "
                "executed successfully."
            )
        }

    return scheduler.schedule(
        callback=callback,
        delay_seconds=delay_seconds,
        job_name=name,
        user_id=user_id,
        db=db
    )


# ---------------------------------
# GET SINGLE RUNTIME JOB
# ---------------------------------

@router.get("/jobs/{job_id}")
def get_job(
    job_id: str
):

    return scheduler.get_job(
        job_id
    )


# ---------------------------------
# CANCEL JOB
# ---------------------------------

@router.post("/jobs/{job_id}/cancel")
def cancel_job(
    job_id: str
):

    return scheduler.cancel_job(
        job_id
    )


# ---------------------------------
# REMOVE JOB
# ---------------------------------

@router.delete("/jobs/{job_id}")
def remove_job(
    job_id: str
):

    return scheduler.remove_job(
        job_id
    )   