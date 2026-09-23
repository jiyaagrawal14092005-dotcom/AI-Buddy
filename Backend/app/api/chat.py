
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.agent.brain import AIBrain
from app.database.connection import get_db
from app.security.shared import security_manager


router = APIRouter(tags=["Chat"])


# =========================================================
# SHARED AI BRAIN + SHARED SECURITY MANAGER
# =========================================================

brain = AIBrain(
    security_manager=security_manager
)


# =========================================================
# CHAT REQUEST
# =========================================================

class ChatRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        description=(
            "Message sent by the user to AI Buddy."
        )
    )

    user_id: int = Field(
        ...,
        gt=0,
        description=(
            "ID of the user sending the message."
        )
    )

    approval_id: str | None = Field(
        default=None,
        description=(
            "Approval ID returned by AI Buddy "
            "when user approval is required."
        )
    )


# =========================================================
# CHAT ENDPOINT
# =========================================================

@router.post("/chat")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    security_user_id = (
        f"user-{request.user_id}"
    )

    # =====================================================
    # REQUEST SECURITY VALIDATION
    # =====================================================

    security_result = (
        security_manager.validate_request(
            user_id=security_user_id,
            prompt=request.message
        )
    )

    # =====================================================
    # BLOCK UNSAFE REQUEST
    # =====================================================

    if not security_result.get(
        "allowed",
        False
    ):

        security_manager.record_audit_log(
            username=security_user_id,
            action="chat.request_validation",
            status="blocked",
            details={
                "message": request.message,
                "stage": security_result.get(
                    "stage",
                    "request_validation"
                ),
                "reason": security_result.get(
                    "message",
                    "Request blocked by security."
                )
            }
        )

        return {
            "success": False,
            "user_message": request.message,
            "approval_required": False,
            "approval_id": None,
            "intent": None,
            "plan": None,
            "reasoning": None,
            "message": security_result.get(
                "message",
                "Request blocked by security."
            ),
            "action_result": {
                "success": False,
                "security_blocked": True,
                "stage": security_result.get(
                    "stage",
                    "request_validation"
                ),
                "message": security_result.get(
                    "message",
                    "Request blocked by security."
                )
            },

            # =================================================
            # EXECUTION WORKFLOW
            # =================================================

            "execution_workflow": [],

            "context": []
        }

    # =====================================================
    # SANITIZED MESSAGE
    # =====================================================

    sanitized_message = (
        security_result.get(
            "prompt",
            request.message
        )
    )

    # =====================================================
    # SEND REQUEST TO AI BRAIN
    # =====================================================

    result = await brain.respond(
        message=sanitized_message,
        user_id=request.user_id,
        db=db,
        approval_id=request.approval_id
    )

    # =====================================================
    # AUDIT LOG
    # =====================================================

    security_manager.record_audit_log(
        username=security_user_id,
        action="chat.request",
        status=(
            "success"
            if result.get(
                "success",
                False
            )
            else "failed"
        ),
        details={
            "message": request.message,
            "intent": (
                result.get(
                    "intent"
                )
                if isinstance(
                    result.get(
                        "intent"
                    ),
                    str
                )
                else (
                    result.get(
                        "intent",
                        {}
                    ).get(
                        "intent"
                    )
                    if isinstance(
                        result.get(
                            "intent"
                        ),
                        dict
                    )
                    else None
                )
            ),
            "approval_required": result.get(
                "approval_required",
                False
            ),
            "approval_id": result.get(
                "approval_id"
            )
        }
    )

    # =====================================================
    # RETURN RESPONSE
    # =====================================================

    return {
        "success": result.get(
            "success",
            False
        ),
        "user_message": request.message,
        "approval_required": result.get(
            "approval_required",
            False
        ),
        "approval_id": result.get(
            "approval_id"
        ),
        "intent": result.get(
            "intent"
        ),
        "plan": result.get(
            "plan"
        ),
        "reasoning": result.get(
            "reasoning"
        ),
        "message": result.get(
            "message"
        ),
        "action_result": result.get(
            "action_result"
        ),

        # =================================================
        # EXECUTION WORKFLOW
        # =================================================

        "execution_workflow": result.get(
            "execution_workflow",
            []
        ),

        "context": result.get(
            "context",
            []
        )
    }

