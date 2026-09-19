import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.workflow.manager import WorkflowManager


router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"]
)

workflow_manager = WorkflowManager()


@router.get("/status")
def workflow_status():

    return {
        "success": True,
        "service": "workflows",
        "status": "ready",
        "database": "connected"
    }


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


@router.post("/create")
async def create_workflow(
    name: str,
    tool: str,
    user_id: int,
    parameters: str | None = None,
    db: Session = Depends(get_db)
):

    # ---------------------------------
    # PARSE PARAMETERS
    # ---------------------------------

    if parameters is None or not parameters.strip():

        parsed_parameters: dict[str, Any] = {}

    else:

        try:

            parsed_parameters = json.loads(
                parameters
            )

        except json.JSONDecodeError as error:

            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": "Invalid workflow parameters JSON.",
                    "error": str(error)
                }
            )


        if not isinstance(
            parsed_parameters,
            dict
        ):

            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": (
                        "Workflow parameters "
                        "must be a JSON object."
                    )
                }
            )


    # ---------------------------------
    # BUILD WORKFLOW PLAN
    # ---------------------------------

    plan = {

        "intent": "CREATE_WORKFLOW",

        "name": name,

        "tool": tool,

        "parameters": parsed_parameters

    }


    # ---------------------------------
    # CREATE WORKFLOW
    # ---------------------------------

    return await workflow_manager.create(
        plan,
        user_id,
        db
    )


@router.delete("/clear")
def clear_workflows(
    user_id: int,
    db: Session = Depends(get_db)
):

    return workflow_manager.clear(
        user_id,
        db
    )


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