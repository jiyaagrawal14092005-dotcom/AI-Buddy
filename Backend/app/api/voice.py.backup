import base64

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.voice.conversation import VoiceConversation
from app.voice.jarvis_mode import JarvisMode


router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)


voice_conversation = VoiceConversation()

jarvis_mode = JarvisMode()


@router.get("/status")
def voice_status():
    return {
        "success": True,
        "voice": voice_conversation.get_status(),
        "jarvis": jarvis_mode.get_status()
    }


@router.post("/start")
def start_voice_conversation():
    return voice_conversation.start()


@router.post("/stop")
def stop_voice_conversation():
    return voice_conversation.stop()


@router.post("/process")
async def process_voice_text(
    text: str,
    user_id: int,
    db: Session = Depends(get_db)
):
    return await voice_conversation.process_input(
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
async def speech_to_text(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Stop the current recording and convert
    the recorded audio into text.
    """

    return await voice_conversation.process_recorded_audio(
        user_id,
        db
    )


# ==========================================================
# JARVIS MODE
# ==========================================================


@router.post("/jarvis/start")
async def start_jarvis(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Start continuous Jarvis mode.

    Jarvis continuously listens for the configured
    wake word and executes recognized commands.
    """

    return await jarvis_mode.start(
        user_id,
        db
    )


@router.post("/jarvis/stop")
async def stop_jarvis():
    """
    Stop continuous Jarvis mode.
    """

    return await jarvis_mode.stop()


@router.get("/jarvis/status")
def jarvis_status():
    """
    Return the current Jarvis mode status.
    """

    return {
        "success": True,
        "jarvis": jarvis_mode.get_status()
    }


@router.post("/jarvis/toggle")
async def toggle_jarvis(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Start Jarvis if inactive or stop it if active.
    """

    return await jarvis_mode.toggle(
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


@router.get("/jarvis/history")
def jarvis_history():
    return {
        "success": True,
        "history": jarvis_mode.get_history()
    }


@router.delete("/jarvis/history")
def clear_jarvis_history():
    jarvis_mode.clear_history()

    return {
        "success": True,
        "message": "Jarvis history cleared."
    }