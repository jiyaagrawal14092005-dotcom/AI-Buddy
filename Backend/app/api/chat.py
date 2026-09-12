from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.agent.brain import AIBrain


router = APIRouter(
    tags=["Chat"]
)

brain = AIBrain()


class ChatRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        description="Message sent by the user to AI Buddy."
    )


@router.post("/chat")
def chat(request: ChatRequest):

    # ---------------------------------
    # SEND MESSAGE TO AI BRAIN
    # ---------------------------------

    result = brain.respond(
        request.message
    )

    # ---------------------------------
    # RETURN API RESPONSE
    # ---------------------------------

    return {
        "success": result.get(
            "success",
            True
        ),
        "user_message": request.message,
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