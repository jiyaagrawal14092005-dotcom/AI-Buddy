import uuid
from datetime import datetime


class ApprovalManager:
    def __init__(self):
        self.requests = {}

    # ============================================================
    # CREATE APPROVAL REQUEST
    # ============================================================

    def create_request(
        self,
        username,
        action,
        details=None
    ):
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
        now = datetime.utcnow().isoformat()

        request = {
            "approval_id": approval_id,
            "username": str(username),
            "action": str(action),
            "details": (
                details
                if isinstance(details, dict)
                else {}
            ),
            "status": "PENDING",
            "created_at": now,
            "updated_at": now
        }

        self.requests[approval_id] = request

        return {
            "success": True,
            "approval_id": approval_id,
            "status": "PENDING",
            "message": "Approval request created successfully."
        }

    # ============================================================
    # APPROVE
    # ============================================================

    def approve(
        self,
        approval_id
    ):
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
                    "Approval request is already "
                    f"{request['status']}."
                )
            }

        request["status"] = "APPROVED"
        request["updated_at"] = datetime.utcnow().isoformat()

        return {
            "success": True,
            "approval_id": approval_id,
            "status": "APPROVED",
            "message": "Action approved successfully."
        }

    # ============================================================
    # REJECT
    # ============================================================

    def reject(
        self,
        approval_id
    ):
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
                    "Approval request is already "
                    f"{request['status']}."
                )
            }

        request["status"] = "REJECTED"
        request["updated_at"] = datetime.utcnow().isoformat()

        return {
            "success": True,
            "approval_id": approval_id,
            "status": "REJECTED",
            "message": "Approval request rejected successfully."
        }

    # ============================================================
    # GET SINGLE REQUEST
    #
    # IMPORTANT:
    # Brain expects:
    # {
    #     "success": True,
    #     "request": {...}
    # }
    # ============================================================

    def get_request(
        self,
        approval_id
    ):
        request = self.requests.get(
            approval_id
        )

        if not request:
            return {
                "success": False,
                "request": None,
                "message": "Approval request not found."
            }

        return {
            "success": True,
            "request": dict(request),
            "message": "Approval request found."
        }

    # ============================================================
    # GET PENDING REQUESTS
    # ============================================================

    def get_pending_requests(
        self
    ):
        return [
            dict(request)
            for request in self.requests.values()
            if request["status"] == "PENDING"
        ]

    # ============================================================
    # GET ALL REQUESTS
    # ============================================================

    def get_all_requests(
        self
    ):
        return [
            dict(request)
            for request in self.requests.values()
        ]

    # ============================================================
    # CONSUME APPROVED REQUEST
    # ============================================================

    def consume(
        self,
        approval_id
    ):
        request = self.requests.get(
            approval_id
        )

        if not request:
            return {
                "success": False,
                "message": "Approval request not found."
            }

        if request["status"] != "APPROVED":
            return {
                "success": False,
                "message": (
                    "Approval request cannot be consumed "
                    f"because its status is {request['status']}."
                )
            }

        request["status"] = "CONSUMED"
        request["updated_at"] = datetime.utcnow().isoformat()

        return {
            "success": True,
            "approval_id": approval_id,
            "status": "CONSUMED",
            "message": "Approval request consumed successfully."
        }


# ================================================================
# SHARED APPROVAL MANAGER
# ================================================================

approval_manager = ApprovalManager()