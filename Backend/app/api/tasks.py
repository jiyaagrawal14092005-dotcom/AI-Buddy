from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.tools.task import TaskTool


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


task_tool = TaskTool()


# ---------------------------------
# TASK SERVICE STATUS
# ---------------------------------

@router.get("/status")
def task_status():

    return {
        "success": True,
        "service": "tasks",
        "status": "ready",
        "database": "connected"
    }


# ---------------------------------
# CREATE TASK
# ---------------------------------

@router.post("/create")
def create_task(
    task_name: str,
    user_id: int,
    db: Session = Depends(get_db)
):

    return task_tool.create_task(
        task_name,
        user_id,
        db
    )


# ---------------------------------
# GET TASKS
# ---------------------------------

@router.get("/")
def get_tasks(
    user_id: int,
    db: Session = Depends(get_db)
):

    return {
        "success": True,
        "tasks": task_tool.get_tasks(
            user_id,
            db
        )
    }


# ---------------------------------
# DELETE TASK
# ---------------------------------

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    return task_tool.delete_task(
        task_id,
        user_id,
        db
    )