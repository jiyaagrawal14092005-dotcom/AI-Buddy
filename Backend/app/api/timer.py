from fastapi import APIRouter

from app.timer.timer_manager import TimerManager


router = APIRouter(
    prefix="/api/timer",
    tags=["Timer"]
)


timer_manager = TimerManager()


@router.get("/status")
def timer_status():

    return {
        "success": True,
        "module": "Timer",
        "status": "active",
        "active_timers": timer_manager.get_active_count(),
        "total_timers": timer_manager.get_count()
    }


@router.post("/create")
def create_timer(
    duration_seconds: float
):

    return timer_manager.create_timer(
        duration_seconds=duration_seconds
    )


@router.post("/{timer_id}/start")
def start_timer(
    timer_id: int
):

    return timer_manager.start_timer(
        timer_id=timer_id
    )


@router.post("/{timer_id}/cancel")
def cancel_timer(
    timer_id: int
):

    return timer_manager.cancel_timer(
        timer_id=timer_id
    )


@router.get("/{timer_id}")
def get_timer(
    timer_id: int
):

    return timer_manager.get_timer(
        timer_id=timer_id
    )


@router.get("/")
def get_all_timers():

    return {
        "success": True,
        "timers": timer_manager.get_all_timers()
    }


@router.delete("/{timer_id}")
def remove_timer(
    timer_id: int
):

    return timer_manager.remove_timer(
        timer_id=timer_id
    )


@router.delete("/")
def clear_all_timers():

    timer_manager.clear_all()

    return {
        "success": True,
        "message": "All timers cleared successfully."
    }