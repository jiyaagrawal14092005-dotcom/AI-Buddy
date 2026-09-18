import asyncio

from app.database.connection import SessionLocal
from app.voice.conversation import VoiceConversation


async def main():

    conversation = VoiceConversation()

    conversation.start()

    db = SessionLocal()

    try:

        print("\nTEST: Valid Voice Timer Command")

        # Mock STT output
        conversation.voice_manager.listen = lambda audio_data: {
            "success": True,
            "text": "Zarvis, set a timer for 10 minutes",
            "message": "Mock STT result."
        }

        result = await conversation.process_audio(
            b"fake-audio-data",
            1,
            db
        )

        print(result)

    finally:

        db.close()


if __name__ == "__main__":
    asyncio.run(main())