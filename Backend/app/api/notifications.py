from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.notifications.manager import NotificationManager


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


notification_manager = NotificationManager()


@router.get("/status")
def notification_status():

    return {
        "success": True,
        "service": "notifications",
        "status": "ready",
        "database": "connected"
    }


@router.get("/")
def get_notifications(
    user_id: int,
    db: Session = Depends(get_db)
):

    return {
        "success": True,
        "notifications": notification_manager.get_notifications(
            user_id,
            db
        )
    }


@router.post("/")
def create_notification(
    user_id: int,
    message: str,
    notification_type: str = "in_app",
    db: Session = Depends(get_db)
):

    return notification_manager.send(
        message,
        user_id,
        db,
        notification_type
    )


@router.get("/count")
def get_notification_count(
    user_id: int,
    db: Session = Depends(get_db)
):

    return {
        "success": True,
        "count": notification_manager.get_count(
            user_id,
            db
        )
    }


@router.get("/{notification_id}")
def get_notification(
    notification_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    return notification_manager.get_notification(
        notification_id,
        user_id,
        db
    )


@router.put("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    return notification_manager.mark_as_read(
        notification_id,
        user_id,
        db
    )


@router.delete("/clear")
def clear_notifications(
    user_id: int,
    db: Session = Depends(get_db)
):

    return notification_manager.clear(
        user_id,
        db
    )