from sqlalchemy.orm import Session

from app.database.models import Task


class TaskTool:

    # ---------------------------------
    # CREATE TASK
    # ---------------------------------

    def create_task(
        self,
        task_name: str,
        user_id: int,
        db: Session
    ) -> dict:

        if not task_name:
            return {
                "success": False,
                "message": "Task name is required."
            }

        if not isinstance(task_name, str):
            return {
                "success": False,
                "message": "Task name must be text."
            }

        if not isinstance(user_id, int):
            return {
                "success": False,
                "message": "User ID must be an integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "message": "User ID must be greater than zero."
            }

        task_name = task_name.strip()

        if not task_name:
            return {
                "success": False,
                "message": "Task name cannot be empty."
            }

        try:

            task = Task(
                user_id=user_id,
                title=task_name,
                status="pending"
            )

            db.add(task)
            db.commit()
            db.refresh(task)

            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "created_at": task.created_at
                },
                "message": (
                    f"Task '{task_name}' "
                    "created successfully."
                )
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "message": "Task could not be created.",
                "error": str(error)
            }

    # ---------------------------------
    # GET ALL TASKS
    # ---------------------------------

    def get_tasks(
        self,
        user_id: int,
        db: Session
    ) -> list:

        if not isinstance(user_id, int):
            return []

        if user_id <= 0:
            return []

        try:

            tasks = (
                db.query(Task)
                .filter(
                    Task.user_id == user_id
                )
                .order_by(
                    Task.created_at.desc()
                )
                .all()
            )

            return [
                {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "created_at": task.created_at
                }
                for task in tasks
            ]

        except Exception:

            return []

    # ---------------------------------
    # DELETE TASK
    # ---------------------------------

    def delete_task(
        self,
        task_id: int,
        user_id: int,
        db: Session
    ) -> dict:

        if not isinstance(task_id, int):
            return {
                "success": False,
                "message": "Task ID must be an integer."
            }

        if task_id <= 0:
            return {
                "success": False,
                "message": "Task ID must be greater than zero."
            }

        if not isinstance(user_id, int):
            return {
                "success": False,
                "message": "User ID must be an integer."
            }

        try:

            task = (
                db.query(Task)
                .filter(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
                .first()
            )

            if task is None:
                return {
                    "success": False,
                    "message": "Task not found."
                }

            task_title = task.title

            db.delete(task)
            db.commit()

            return {
                "success": True,
                "message": (
                    f"Task '{task_title}' "
                    "deleted successfully."
                )
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "message": "Task could not be deleted.",
                "error": str(error)
            }

    # ---------------------------------
    # UPDATE TASK STATUS IN DATABASE
    # ---------------------------------

    def set_task_status(
        self,
        task_id: int,
        user_id: int,
        status: str,
        db: Session
    ) -> dict:

        if not isinstance(task_id, int):
            return {
                "success": False,
                "message": "Task ID must be an integer."
            }

        if task_id <= 0:
            return {
                "success": False,
                "message": "Task ID must be greater than zero."
            }

        if not isinstance(user_id, int):
            return {
                "success": False,
                "message": "User ID must be an integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "message": "User ID must be greater than zero."
            }

        if not status:
            return {
                "success": False,
                "message": "Task status is required."
            }

        if not isinstance(status, str):
            return {
                "success": False,
                "message": "Task status must be text."
            }

        status = status.strip().lower()

        valid_statuses = {
            "pending",
            "running",
            "completed",
            "failed"
        }

        if status not in valid_statuses:
            return {
                "success": False,
                "message": (
                    "Invalid task status. "
                    "Use pending, running, "
                    "completed, or failed."
                )
            }

        try:

            task = (
                db.query(Task)
                .filter(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
                .first()
            )

            if task is None:
                return {
                    "success": False,
                    "message": "Task not found."
                }

            task.status = status

            db.commit()
            db.refresh(task)

            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "created_at": task.created_at
                },
                "message": (
                    f"Task '{task.title}' "
                    f"status updated to '{status}'."
                )
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "message": "Task status could not be updated.",
                "error": str(error)
            }

    # ---------------------------------
    # OLD STATUS VALIDATION METHOD
    # ---------------------------------

    def update_task_status(
        self,
        task_name: str,
        status: str
    ) -> dict:

        if not task_name:
            return {
                "success": False,
                "message": "Task name is required."
            }

        if not status:
            return {
                "success": False,
                "message": "Task status is required."
            }

        if not isinstance(task_name, str):
            return {
                "success": False,
                "message": "Task name must be text."
            }

        if not isinstance(status, str):
            return {
                "success": False,
                "message": "Task status must be text."
            }

        task_name = task_name.strip()
        status = status.strip().lower()

        valid_statuses = {
            "pending",
            "running",
            "completed",
            "failed"
        }

        if status not in valid_statuses:
            return {
                "success": False,
                "message": (
                    "Invalid task status. "
                    "Use pending, running, "
                    "completed, or failed."
                )
            }

        return {
            "success": True,
            "task": task_name,
            "status": status,
            "message": (
                f"Task '{task_name}' "
                f"status updated to '{status}'."
            )
        }

    # ---------------------------------
    # GET TASK STATUS
    # ---------------------------------

    def get_task_status(
        self,
        status: str
    ) -> dict:

        if not status:
            return {
                "success": False,
                "message": "Task status is required."
            }

        if not isinstance(status, str):
            return {
                "success": False,
                "message": "Task status must be text."
            }

        status = status.strip().lower()

        valid_statuses = {
            "pending",
            "running",
            "completed",
            "failed"
        }

        if status not in valid_statuses:
            return {
                "success": False,
                "message": "Invalid task status."
            }

        return {
            "success": True,
            "status": status,
            "completed": status == "completed",
            "message": (
                f"Task status is '{status}'."
            )
        }