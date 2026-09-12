from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.workflow.manager import WorkflowManager


router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"]
)


workflow_manager = WorkflowManager()


# ---------------------------------
# WORKFLOW STATUS
# ---------------------------------

@router.get("/status")
def workflow_status():

    return {
        "success": True,
        "service": "workflows",
        "status": "ready",
        "database": "connected"
    }


# ---------------------------------
# GET ALL WORKFLOWS
# ---------------------------------

@router.get("/")
def get_workflows(
    user_id: int,
    db: Session = Depends(get_db)
):

    return {
        "success": True,
        "workflows": workflow_manager.get_all(
            user_id,
            db
        )
    }


# ---------------------------------
# CREATE WORKFLOW
# ---------------------------------

@router.post("/create")
def create_workflow(
    name: str,
    tool: str,
    user_id: int,
    parameters: dict[str, Any] | None = None,
    db: Session = Depends(get_db)
):

    if parameters is None:
        parameters = {}

    plan = {
        "name": name,
        "tool": tool,
        "parameters": parameters
    }

    return workflow_manager.create(
        plan,
        user_id,
        db
    )


# ---------------------------------
# CLEAR ALL WORKFLOWS
# ---------------------------------

@router.delete("/clear")
def clear_workflows(
    user_id: int,
    db: Session = Depends(get_db)
):

    return workflow_manager.clear(
        user_id,
        db
    )


# ---------------------------------
# GET SINGLE WORKFLOW
# ---------------------------------

@router.get("/{workflow_id}")
def get_workflow(
    workflow_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    return workflow_manager.get(
        workflow_id,
        user_id,
        db
    )


# ---------------------------------
# DELETE SINGLE WORKFLOW
# ---------------------------------

@router.delete("/{workflow_id}")
def delete_workflow(
    workflow_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    return workflow_manager.delete(
        workflow_id,
        user_id,
        db
    )