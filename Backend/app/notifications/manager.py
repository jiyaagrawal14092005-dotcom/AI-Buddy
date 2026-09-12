from sqlalchemy.orm import Session

from app.database.models import Notification


class NotificationManager:

    def send(
        self,
        message: str,
        user_id: int,
        db: Session,
        notification_type: str = "in_app"
    ) -> dict:

        if not isinstance(
            message,
            str
        ):
            return {
                "success": False,
                "message": "Notification message must be a string."
            }

        message = message.strip()

        if not message:
            return {
                "success": False,
                "message": "Notification message cannot be empty."
            }

        if not isinstance(
            user_id,
            int
        ):
            return {
                "success": False,
                "message": "User ID must be an integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "message": "User ID must be greater than zero."
            }

        if not isinstance(
            notification_type,
            str
        ):
            return {
                "success": False,
                "message": (
                    "Notification type must be a string."
                )
            }

        notification_type = (
            notification_type.strip().lower()
        )

        allowed_types = {
            "in_app",
            "email"
        }

        if notification_type not in allowed_types:
            return {
                "success": False,
                "message": (
                    "Unsupported notification type. "
                    "Use in_app or email."
                )
            }

        try:

            notification = Notification(
                user_id=user_id,
                notification_type=notification_type,
                message=message,
                status="created"
            )

            db.add(notification)
            db.commit()
            db.refresh(notification)

            return {
                "success": True,
                "notification": {
                    "id": notification.id,
                    "user_id": notification.user_id,
                    "type": notification.notification_type,
                    "message": notification.message,
                    "status": notification.status,
                    "created_at": notification.created_at
                },
                "message": (
                    "Notification created successfully."
                )
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "message": (
                    "Notification could not be created."
                ),
                "error": str(error)
            }

    def get_notifications(
        self,
        user_id: int,
        db: Session
    ) -> list:

        if not isinstance(
            user_id,
            int
        ):
            return []

        if user_id <= 0:
            return []

        try:

            notifications = (
                db.query(Notification)
                .filter(
                    Notification.user_id == user_id
                )
                .order_by(
                    Notification.created_at.desc()
                )
                .all()
            )

            return [
                {
                    "id": notification.id,
                    "user_id": notification.user_id,
                    "type": notification.notification_type,
                    "message": notification.message,
                    "status": notification.status,
                    "created_at": notification.created_at
                }
                for notification in notifications
            ]

        except Exception:

            return []

    def get_notification(
        self,
        notification_id: int,
        user_id: int,
        db: Session
    ) -> dict:

        if not isinstance(
            notification_id,
            int
        ):
            return {
                "success": False,
                "message": (
                    "Notification ID must be an integer."
                )
            }

        if notification_id <= 0:
            return {
                "success": False,
                "message": (
                    "Notification ID must be greater than zero."
                )
            }

        if not isinstance(
            user_id,
            int
        ):
            return {
                "success": False,
                "message": "User ID must be an integer."
            }

        try:

            notification = (
                db.query(Notification)
                .filter(
                    Notification.id == notification_id,
                    Notification.user_id == user_id
                )
                .first()
            )

            if notification is None:

                return {
                    "success": False,
                    "message": "Notification not found."
                }

            return {
                "success": True,
                "notification": {
                    "id": notification.id,
                    "user_id": notification.user_id,
                    "type": notification.notification_type,
                    "message": notification.message,
                    "status": notification.status,
                    "created_at": notification.created_at
                }
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    "Notification could not be retrieved."
                ),
                "error": str(error)
            }

    def mark_as_read(
        self,
        notification_id: int,
        user_id: int,
        db: Session
    ) -> dict:

        if not isinstance(
            notification_id,
            int
        ):
            return {
                "success": False,
                "message": (
                    "Notification ID must be an integer."
                )
            }

        if notification_id <= 0:
            return {
                "success": False,
                "message": (
                    "Notification ID must be greater than zero."
                )
            }

        if not isinstance(
            user_id,
            int
        ):
            return {
                "success": False,
                "message": "User ID must be an integer."
            }

        try:

            notification = (
                db.query(Notification)
                .filter(
                    Notification.id == notification_id,
                    Notification.user_id == user_id
                )
                .first()
            )

            if notification is None:

                return {
                    "success": False,
                    "message": "Notification not found."
                }

            notification.status = "read"

            db.commit()
            db.refresh(notification)

            return {
                "success": True,
                "notification": {
                    "id": notification.id,
                    "user_id": notification.user_id,
                    "type": notification.notification_type,
                    "message": notification.message,
                    "status": notification.status,
                    "created_at": notification.created_at
                },
                "message": (
                    "Notification marked as read."
                )
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "message": (
                    "Notification could not be updated."
                ),
                "error": str(error)
            }

    def clear(
        self,
        user_id: int,
        db: Session
    ) -> dict:

        if not isinstance(
            user_id,
            int
        ):
            return {
                "success": False,
                "message": "User ID must be an integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "message": "User ID must be greater than zero."
            }

        try:

            notifications = (
                db.query(Notification)
                .filter(
                    Notification.user_id == user_id
                )
                .all()
            )

            deleted_count = len(
                notifications
            )

            for notification in notifications:
                db.delete(notification)

            db.commit()

            return {
                "success": True,
                "deleted_count": deleted_count,
                "message": (
                    "Notifications cleared successfully."
                )
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "message": (
                    "Notifications could not be cleared."
                ),
                "error": str(error)
            }

    def get_count(
        self,
        user_id: int,
        db: Session
    ) -> int:

        if not isinstance(
            user_id,
            int
        ):
            return 0

        if user_id <= 0:
            return 0

        try:

            return (
                db.query(Notification)
                .filter(
                    Notification.user_id == user_id
                )
                .count()
            )

        except Exception:

            return 0