from fastapi import APIRouter

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
        "status": "ready"
    }


@router.get("/")
def get_workflows():

    return {
        "success": True,
        "workflows": workflow_manager.get_all_workflows()
    }


@router.post("/create")
def create_workflow(name: str):

    return workflow_manager.create_workflow(
        name
    )


@router.get("/{workflow_id}")
def get_workflow(workflow_id: int):

    return workflow_manager.get_workflow(
        workflow_id
    )


@router.delete("/{workflow_id}")
def delete_workflow(workflow_id: int):

    return workflow_manager.delete_workflow(
        workflow_id
    )