from sqlalchemy.orm import Session

from app.database.models import Workflow
from app.workflow.engine import WorkflowEngine


class WorkflowManager:

    def __init__(self):

        self.engine = WorkflowEngine()

    # ---------------------------------
    # CREATE WORKFLOW
    # ---------------------------------

    def create(
        self,
        plan: dict,
        user_id: int,
        db: Session
    ) -> dict:

        # ---------------------------------
        # VALIDATE PLAN
        # ---------------------------------

        if not isinstance(plan, dict):

            return {
                "success": False,
                "message": (
                    "Workflow plan must be a dictionary."
                )
            }

        # ---------------------------------
        # VALIDATE USER ID
        # ---------------------------------

        if not isinstance(user_id, int):

            return {
                "success": False,
                "message": (
                    "User ID must be an integer."
                )
            }

        if user_id <= 0:

            return {
                "success": False,
                "message": (
                    "User ID must be greater than zero."
                )
            }

        # ---------------------------------
        # VALIDATE DATABASE
        # ---------------------------------

        if db is None:

            return {
                "success": False,
                "message": (
                    "Database session is required."
                )
            }

        # ---------------------------------
        # CREATE USING ENGINE
        # ---------------------------------

        result = self.engine.create_workflow(
            plan,
            user_id,
            db
        )

        if not isinstance(result, dict):

            return {
                "success": False,
                "message": (
                    "Invalid workflow engine response."
                )
            }

        if not result.get("success"):

            return result

        # ---------------------------------
        # GET ENGINE WORKFLOW
        # ---------------------------------

        workflow_data = result.get(
            "workflow"
        )

        if not isinstance(workflow_data, dict):

            return {
                "success": False,
                "message": (
                    "Invalid workflow data."
                )
            }

        # ---------------------------------
        # GET WORKFLOW ID
        # ---------------------------------

        workflow_id = workflow_data.get(
            "workflow_id"
        )

        if not isinstance(
            workflow_id,
            str
        ):

            return {
                "success": False,
                "message": (
                    "Workflow ID is missing."
                )
            }

        workflow_id = workflow_id.strip()

        if not workflow_id:

            return {
                "success": False,
                "message": (
                    "Workflow ID cannot be empty."
                )
            }

        # ---------------------------------
        # GET WORKFLOW NAME
        # ---------------------------------

        name = (
            plan.get("name")
            or plan.get("title")
            or "AI Buddy Workflow"
        )

        if not isinstance(
            name,
            str
        ):

            name = "AI Buddy Workflow"

        name = name.strip()

        if not name:

            name = "AI Buddy Workflow"

        # ---------------------------------
        # GET WORKFLOW STATUS
        # ---------------------------------

        status = workflow_data.get(
            "status",
            "created"
        )

        if not isinstance(
            status,
            str
        ):

            status = "created"

        status = status.strip().lower()

        if not status:

            status = "created"

        # ---------------------------------
        # SAVE WORKFLOW TO DATABASE
        # ---------------------------------

        try:

            workflow = Workflow(
                user_id=user_id,
                name=name,
                status=status
            )

            db.add(
                workflow
            )

            db.commit()

            db.refresh(
                workflow
            )

            # ---------------------------------
            # RETURN RESULT
            # ---------------------------------

            return {
                "success": True,
                "workflow": {
                    "id": workflow.id,
                    "user_id": workflow.user_id,
                    "name": workflow.name,
                    "status": workflow.status,
                    "created_at": workflow.created_at,
                    "workflow_id": workflow_id
                },
                "engine_workflow": workflow_data,
                "message": (
                    "Workflow created successfully."
                )
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "message": (
                    "Workflow could not be saved "
                    "to database."
                ),
                "error": str(error)
            }

    # ---------------------------------
    # GET SINGLE WORKFLOW
    # ---------------------------------

    def get(
        self,
        workflow_id: int,
        user_id: int,
        db: Session
    ) -> dict:

        if not isinstance(
            workflow_id,
            int
        ):

            return {
                "success": False,
                "message": (
                    "Workflow ID must be an integer."
                )
            }

        if workflow_id <= 0:

            return {
                "success": False,
                "message": (
                    "Workflow ID must be greater than zero."
                )
            }

        if not isinstance(
            user_id,
            int
        ):

            return {
                "success": False,
                "message": (
                    "User ID must be an integer."
                )
            }

        if user_id <= 0:

            return {
                "success": False,
                "message": (
                    "User ID must be greater than zero."
                )
            }

        try:

            workflow = (
                db.query(
                    Workflow
                )
                .filter(
                    Workflow.id == workflow_id,
                    Workflow.user_id == user_id
                )
                .first()
            )

            if workflow is None:

                return {
                    "success": False,
                    "message": (
                        "Workflow not found."
                    )
                }

            return {
                "success": True,
                "workflow": {
                    "id": workflow.id,
                    "user_id": workflow.user_id,
                    "name": workflow.name,
                    "status": workflow.status,
                    "created_at": workflow.created_at
                }
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    "Workflow could not be retrieved."
                ),
                "error": str(error)
            }

    # ---------------------------------
    # GET ALL WORKFLOWS
    # ---------------------------------

    def get_all(
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

            workflows = (
                db.query(
                    Workflow
                )
                .filter(
                    Workflow.user_id == user_id
                )
                .order_by(
                    Workflow.created_at.desc()
                )
                .all()
            )

            return [
                {
                    "id": workflow.id,
                    "user_id": workflow.user_id,
                    "name": workflow.name,
                    "status": workflow.status,
                    "created_at": workflow.created_at
                }
                for workflow in workflows
            ]

        except Exception:

            return []

    # ---------------------------------
    # DELETE SINGLE WORKFLOW
    # ---------------------------------

    def delete(
        self,
        workflow_id: int,
        user_id: int,
        db: Session
    ) -> dict:

        if not isinstance(
            workflow_id,
            int
        ):

            return {
                "success": False,
                "message": (
                    "Workflow ID must be an integer."
                )
            }

        if workflow_id <= 0:

            return {
                "success": False,
                "message": (
                    "Workflow ID must be greater than zero."
                )
            }

        if not isinstance(
            user_id,
            int
        ):

            return {
                "success": False,
                "message": (
                    "User ID must be an integer."
                )
            }

        if user_id <= 0:

            return {
                "success": False,
                "message": (
                    "User ID must be greater than zero."
                )
            }

        try:

            workflow = (
                db.query(
                    Workflow
                )
                .filter(
                    Workflow.id == workflow_id,
                    Workflow.user_id == user_id
                )
                .first()
            )

            if workflow is None:

                return {
                    "success": False,
                    "message": (
                        "Workflow not found."
                    )
                }

            db.delete(
                workflow
            )

            db.commit()

            return {
                "success": True,
                "workflow_id": workflow_id,
                "message": (
                    "Workflow deleted successfully."
                )
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "message": (
                    "Workflow could not be deleted."
                ),
                "error": str(error)
            }

    # ---------------------------------
    # CLEAR ALL WORKFLOWS
    # ---------------------------------

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
                "message": (
                    "User ID must be an integer."
                )
            }

        if user_id <= 0:

            return {
                "success": False,
                "message": (
                    "User ID must be greater than zero."
                )
            }

        try:

            workflows = (
                db.query(
                    Workflow
                )
                .filter(
                    Workflow.user_id == user_id
                )
                .all()
            )

            count = len(
                workflows
            )

            for workflow in workflows:

                db.delete(
                    workflow
                )

            db.commit()

            return {
                "success": True,
                "deleted_count": count,
                "message": (
                    "All workflows cleared successfully."
                )
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "message": (
                    "Workflows could not be cleared."
                ),
                "error": str(error)
            }