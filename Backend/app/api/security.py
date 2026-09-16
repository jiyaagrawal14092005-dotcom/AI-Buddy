from fastapi import APIRouter

from app.security.shared import security_manager


router = APIRouter(
    prefix="/security",
    tags=["Security"]
)


# =========================================================
# SECURITY STATUS
# =========================================================

@router.get("/status/{user_id}")
def security_status(user_id: str):

    result = security_manager.get_security_status(
        user_id
    )

    security_manager.record_audit_log(
        username=user_id,
        action="security_status_check",
        status="success"
    )

    return result


# =========================================================
# SECURITY COMPONENTS
# =========================================================

@router.get("/components")
def security_components():

    result = {
        "success": True,
        "components": (
            security_manager.get_security_components()
        )
    }

    security_manager.record_audit_log(
        username="system",
        action="security_components_check",
        status="success"
    )

    return result


# =========================================================
# REQUEST VALIDATION
# =========================================================

@router.post("/validate-request")
def validate_request(
    user_id: str,
    prompt: str
):

    result = security_manager.validate_request(
        user_id=user_id,
        prompt=prompt
    )

    status = (
        "success"
        if result["allowed"]
        else "blocked"
    )

    security_manager.record_audit_log(
        username=user_id,
        action="request_validation",
        status=status,
        details={
            "allowed": result["allowed"],
            "stage": result.get(
                "stage",
                "security_check"
            )
        }
    )

    return result


# =========================================================
# PERMISSION — GRANT
# =========================================================

@router.post("/permission/grant")
def grant_permission(
    user_id: str,
    permission: str
):

    result = security_manager.grant_permission(
        username=user_id,
        permission=permission
    )

    security_manager.record_audit_log(
        username=user_id,
        action="permission_grant",
        status=(
            "success"
            if result.get("success")
            else "failed"
        ),
        details={
            "permission": permission
        }
    )

    return result


# =========================================================
# PERMISSION — GET
# =========================================================

@router.get("/permission/{user_id}")
def get_permissions(user_id: str):

    permissions = security_manager.get_permissions(
        username=user_id
    )

    security_manager.record_audit_log(
        username=user_id,
        action="permission_list",
        status="success"
    )

    return {
        "success": True,
        "user_id": user_id,
        "permissions": permissions
    }


# =========================================================
# PERMISSION — CHECK
# =========================================================

@router.post("/permission/check")
def check_permission(
    user_id: str,
    permission: str
):

    allowed = security_manager.check_permission(
        username=user_id,
        permission=permission
    )

    security_manager.record_audit_log(
        username=user_id,
        action="permission_check",
        status=(
            "success"
            if allowed
            else "blocked"
        ),
        details={
            "permission": permission,
            "allowed": allowed
        }
    )

    return {
        "success": True,
        "user_id": user_id,
        "permission": permission,
        "allowed": allowed,
        "message": (
            "Permission granted."
            if allowed
            else "Permission not granted."
        )
    }


# =========================================================
# PERMISSION — REVOKE
# =========================================================

@router.delete("/permission/revoke")
def revoke_permission(
    user_id: str,
    permission: str
):

    result = security_manager.revoke_permission(
        username=user_id,
        permission=permission
    )

    security_manager.record_audit_log(
        username=user_id,
        action="permission_revoke",
        status=(
            "success"
            if result.get("success")
            else "failed"
        ),
        details={
            "permission": permission
        }
    )

    return result


# =========================================================
# SESSION CREATE
# =========================================================

@router.post("/session/create")
def create_session(user_id: str):

    result = security_manager.create_user_session(
        user_id
    )

    status = (
        "success"
        if result.get("success")
        else "failed"
    )

    security_manager.record_audit_log(
        username=user_id,
        action="session_create",
        status=status
    )

    return result


# =========================================================
# SESSION VALIDATE
# =========================================================

@router.post("/session/validate")
def validate_session(
    session_id: str,
    user_id: str
):

    valid = security_manager.validate_user_session(
        session_id=session_id,
        user_id=user_id
    )

    security_manager.record_audit_log(
        username=user_id,
        action="session_validation",
        status=(
            "success"
            if valid
            else "failed"
        ),
        details={
            "valid": valid
        }
    )

    return {
        "valid": valid
    }


# =========================================================
# SESSION REVOKE
# =========================================================

@router.delete("/session/{session_id}")
def revoke_session(
    session_id: str
):

    result = security_manager.revoke_user_session(
        session_id
    )

    security_manager.record_audit_log(
        username="system",
        action="session_revoke",
        status=(
            "success"
            if result.get("success")
            else "failed"
        )
    )

    return result


# =========================================================
# AUDIT LOGS
# =========================================================

@router.get("/audit-logs")
def get_audit_logs(
    username: str | None = None
):

    return {
        "success": True,
        "logs": security_manager.get_audit_logs(
            username
        )
    }