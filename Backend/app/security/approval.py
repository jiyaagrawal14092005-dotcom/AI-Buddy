import uuid
from datetime import datetime


class ApprovalManager:

    def __init__(self):

        self.requests = {}

    def create_request(
        self,
        username: str,
        action: str,
        details: dict | None = None
    ) -> dict:

        if not username:
            return {
                "success": False,
                "message": "Username is required."
            }

        if not action:
            return {
                "success": False,
                "message": "Action is required."
            }

        approval_id = str(uuid.uuid4())

        request = {
            "approval_id": approval_id,
            "username": username,
            "action": action,
            "details": details or {},
            "status": "PENDING",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        self.requests[approval_id] = request

        return {
            "success": True,
            "approval_id": approval_id,
            "status": "PENDING",
            "message": "Approval request created."
        }

    def approve(
        self,
        approval_id: str
    ) -> dict:

        request = self.requests.get(
            approval_id
        )

        if not request:
            return {
                "success": False,
                "message": "Approval request not found."
            }

        if request["status"] != "PENDING":
            return {
                "success": False,
                "message": (
                    "Only pending requests "
                    "can be approved."
                )
            }

        request["status"] = "APPROVED"
        request["updated_at"] = datetime.now().isoformat()

        return {
            "success": True,
            "approval_id": approval_id,
            "status": "APPROVED",
            "message": "Action approved successfully."
        }

    def reject(
        self,
        approval_id: str
    ) -> dict:

        request = self.requests.get(
            approval_id
        )

        if not request:
            return {
                "success": False,
                "message": "Approval request not found."
            }

        if request["status"] != "PENDING":
            return {
                "success": False,
                "message": (
                    "Only pending requests "
                    "can be rejected."
                )
            }

        request["status"] = "REJECTED"
        request["updated_at"] = datetime.now().isoformat()

        return {
            "success": True,
            "approval_id": approval_id,
            "status": "REJECTED",
            "message": "Action rejected successfully."
        }

    def get_request(
        self,
        approval_id: str
    ) -> dict:

        request = self.requests.get(
            approval_id
        )

        if not request:
            return {
                "success": False,
                "message": "Approval request not found."
            }

        return {
            "success": True,
            "request": request.copy()
        }

    def get_pending_requests(self) -> list:

        return [
            request.copy()
            for request in self.requests.values()
            if request["status"] == "PENDING"
        ]

    def get_all_requests(self) -> list:

        return [
            request.copy()
            for request in self.requests.values()
        ]