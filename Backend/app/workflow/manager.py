from app.workflow.engine import WorkflowEngine


class WorkflowManager:

    def __init__(self):

        self.engine = WorkflowEngine()

        # In-memory workflow storage
        self.workflows = {}

    # ---------------------------------
    # CREATE WORKFLOW
    # ---------------------------------

    def create(
        self,
        plan: dict
    ) -> dict:

        if not isinstance(plan, dict):
            return {
                "success": False,
                "message": "Workflow plan must be a dictionary."
            }

        result = self.engine.create_workflow(
            plan
        )

        if not isinstance(result, dict):
            return {
                "success": False,
                "message": "Invalid workflow engine response."
            }

        if not result.get("success"):
            return result

        workflow = result.get(
            "workflow"
        )

        if not isinstance(workflow, dict):
            return {
                "success": False,
                "message": "Invalid workflow data."
            }

        workflow_id = workflow.get(
            "workflow_id"
        )

        if not isinstance(workflow_id, str):
            return {
                "success": False,
                "message": "Workflow ID is missing."
            }

        workflow_id = workflow_id.strip()

        if not workflow_id:
            return {
                "success": False,
                "message": "Workflow ID cannot be empty."
            }

        self.workflows[workflow_id] = workflow

        return {
            "success": True,
            "workflow": workflow
        }

    # ---------------------------------
    # GET WORKFLOW
    # ---------------------------------

    def get(
        self,
        workflow_id: str
    ) -> dict:

        if not isinstance(workflow_id, str):
            return {
                "success": False,
                "message": "Workflow ID must be text."
            }

        workflow_id = workflow_id.strip()

        if not workflow_id:
            return {
                "success": False,
                "message": "Workflow ID cannot be empty."
            }

        workflow = self.workflows.get(
            workflow_id
        )

        if workflow is None:
            return {
                "success": False,
                "message": "Workflow not found."
            }

        return {
            "success": True,
            "workflow": workflow
        }

    # ---------------------------------
    # GET ALL WORKFLOWS
    # ---------------------------------

    def get_all(self) -> list:

        return list(
            self.workflows.values()
        )

    # ---------------------------------
    # DELETE WORKFLOW
    # ---------------------------------

    def delete(
        self,
        workflow_id: str
    ) -> dict:

        if not isinstance(workflow_id, str):
            return {
                "success": False,
                "message": "Workflow ID must be text."
            }

        workflow_id = workflow_id.strip()

        if not workflow_id:
            return {
                "success": False,
                "message": "Workflow ID cannot be empty."
            }

        if workflow_id not in self.workflows:
            return {
                "success": False,
                "message": "Workflow not found."
            }

        del self.workflows[
            workflow_id
        ]

        return {
            "success": True,
            "workflow_id": workflow_id,
            "message": "Workflow deleted successfully."
        }

    # ---------------------------------
    # CLEAR ALL WORKFLOWS
    # ---------------------------------

    def clear(self) -> dict:

        count = len(
            self.workflows
        )

        self.workflows.clear()

        return {
            "success": True,
            "deleted_count": count,
            "message": "All workflows cleared successfully."
        }