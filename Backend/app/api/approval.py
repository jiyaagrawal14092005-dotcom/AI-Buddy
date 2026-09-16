from fastapi import APIRouter

from app.security.approval import approval_manager


router = APIRouter(
    prefix="/api/approval",
    tags=["Approval"]
)


# =================================
# CREATE APPROVAL REQUEST
# =================================

@router.post("/create")
def create_approval_request(
    username: str,
    action: str,
    details: dict | None = None
):

    return approval_manager.create_request(
        username=username,
        action=action,
        details=details
    )


# =================================
# GET PENDING REQUESTS
# =================================

@router.get("/pending/all")
def get_pending_approval_requests():

    return {
        "success": True,
        "requests": (
            approval_manager.get_pending_requests()
        )
    }


# =================================
# GET ALL REQUESTS
# =================================

@router.get("/all")
def get_all_approval_requests():

    return {
        "success": True,
        "requests": (
            approval_manager.get_all_requests()
        )
    }


# =================================
# APPROVE REQUEST
# =================================

@router.post("/{approval_id}/approve")
def approve_request(
    approval_id: str
):

    return approval_manager.approve(
        approval_id
    )


# =================================
# REJECT REQUEST
# =================================

@router.post("/{approval_id}/reject")
def reject_request(
    approval_id: str
):

    return approval_manager.reject(
        approval_id
    )


# =================================
# GET SINGLE REQUEST
# =================================

@router.get("/{approval_id}")
def get_approval_request(
    approval_id: str
):

    return approval_manager.get_request(
        approval_id
    )