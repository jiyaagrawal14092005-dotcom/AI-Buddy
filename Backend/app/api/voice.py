import base64

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.voice.conversation import VoiceConversation


router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)

voice_conversation = VoiceConversation()


@router.get("/status")
def voice_status():
    return {
        "success": True,
        "voice": voice_conversation.get_status()
    }


@router.post("/start")
def start_voice_conversation():
    return voice_conversation.start()


@router.post("/stop")
def stop_voice_conversation():
    return voice_conversation.stop()


@router.post("/process")
def process_voice_text(
    text: str,
    user_id: int,
    db: Session = Depends(get_db)
):
    return voice_conversation.process_input(
        text,
        user_id,
        db
    )


@router.post("/response")
def add_voice_response(response: str):
    return voice_conversation.add_response(
        response
    )


@router.post("/listening/start")
def start_listening():
    return voice_conversation.start_listening()


@router.post("/listening/stop")
def stop_listening():
    return voice_conversation.stop_listening()


@router.post("/recording/start")
def start_recording():
    return voice_conversation.start_recording()


@router.post("/recording/stop")
def stop_recording():
    result = voice_conversation.stop_recording()

    if not result.get(
        "success",
        False
    ):
        return result

    audio_data = result.get(
        "audio_data"
    )

    if isinstance(
        audio_data,
        bytes
    ):

        result["audio_data"] = (
            base64.b64encode(
                audio_data
            ).decode("utf-8")
        )

    return result


@router.post("/speech-to-text")
def speech_to_text(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Stop the current recording and convert
    the recorded audio into text.
    """

    return voice_conversation.process_recorded_audio(
        user_id,
        db
    )


@router.get("/history")
def voice_history():
    return {
        "success": True,
        "history": voice_conversation.get_history()
    }


@router.delete("/history")
def clear_voice_history():
    voice_conversation.clear_history()

    return {
        "success": True,
        "message": "Voice conversation history cleared."
    }