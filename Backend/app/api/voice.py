from fastapi import APIRouter

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
def process_voice_text(text: str):

    return voice_conversation.process_input(
        text
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

    return voice_conversation.stop_recording()


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