from fastapi import APIRouter

from app.scheduler.scheduler import Scheduler


router = APIRouter(
    prefix="/scheduler",
    tags=["Scheduler"]
)


scheduler = Scheduler()


@router.get("/status")
def scheduler_status():

    return {
        "success": True,
        "service": "scheduler",
        "status": "ready"
    }


@router.get("/jobs")
def get_jobs():

    return {
        "success": True,
        "jobs": scheduler.get_jobs()
    }


@router.post("/start")
def start_scheduler():

    return scheduler.start()


@router.post("/stop")
def stop_scheduler():

    return scheduler.stop()


@router.get("/running")
def scheduler_running():

    return {
        "success": True,
        "running": scheduler.is_running()
    }