from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.agent.brain import AIBrain
from app.database.connection import get_db
from app.security.security_manager import SecurityManager


router = APIRouter(
    tags=["Chat"]
)


brain = AIBrain()
security_manager = SecurityManager()


class ChatRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        description="Message sent by the user to AI Buddy."
    )

    user_id: int = Field(
        ...,
        gt=0,
        description="ID of the user sending the message."
    )

    approval_id: str | None = Field(
        default=None,
        description=(
            "Approval ID returned by AI Buddy when "
            "user approval is required."
        )
    )


@router.post("/chat")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    security_user_id = (
        f"user-{request.user_id}"
    )

    # =================================
    # REQUEST SECURITY VALIDATION
    # =================================

    security_result = (
        security_manager.validate_request(
            user_id=security_user_id,
            prompt=request.message
        )
    )

    if not security_result.get(
        "allowed",
        False
    ):

        security_manager.record_audit_log(
            username=security_user_id,
            action="chat_request",
            status="blocked",
            details={
                "stage": security_result.get(
                    "stage",
                    "security_check"
                ),
                "message": security_result.get(
                    "message",
                    "Request blocked by security."
                )
            }
        )

        return {
            "success": False,
            "user_message": request.message,
            "user_id": request.user_id,
            "approval_id": request.approval_id,
            "approval_required": False,
            "intent": None,
            "plan": None,
            "reasoning": None,
            "message": security_result.get(
                "message",
                "Request blocked by security."
            ),
            "action_result": None,
            "context": []
        }

    # =================================
    # SANITIZED MESSAGE
    # =================================

    sanitized_message = (
        security_result.get(
            "prompt",
            request.message
        )
    )

    # =================================
    # BRAIN EXECUTION
    # =================================

    result = await brain.respond(
        message=sanitized_message,
        user_id=request.user_id,
        db=db,
        approval_id=request.approval_id
    )

    # =================================
    # AUDIT LOG
    # =================================

    security_manager.record_audit_log(
        username=security_user_id,
        action="chat_request",
        status=(
            "success"
            if result.get(
                "success",
                False
            )
            else "failed"
        ),
        details={
            "intent": result.get(
                "intent"
            ),
            "approval_id": result.get(
                "approval_id"
            ),
            "approval_required": result.get(
                "approval_required",
                False
            )
        }
    )

    # =================================
    # FINAL RESPONSE
    # =================================

    return {
        "success": result.get(
            "success",
            True
        ),
        "user_message": request.message,
        "user_id": request.user_id,

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
            "message",
            "No response generated."
        ),

        "action_result": result.get(
            "action_result"
        ),

        "context": result.get(
            "context",
            []
        )
    }