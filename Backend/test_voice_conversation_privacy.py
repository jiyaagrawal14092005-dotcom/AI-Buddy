import asyncio

from app.database.connection import SessionLocal
from app.voice.conversation import VoiceConversation


async def main():

    conversation = VoiceConversation()

    start_result = conversation.start()

    print("\nSTART RESULT:")
    print(start_result)

    db = SessionLocal()

    try:

        print("\nTEST 1: Without wake word")
        result_1 = await conversation.process_input(
            "hello AI Buddy",
            1,
            db
        )

        print(result_1)

        print("\nTEST 2: With Zarvis wake word")
        result_2 = await conversation.process_input(
            "Zarvis set a timer for 10 minutes",
            1,
            db
        )

        print(result_2)

    finally:

        db.close()


if __name__ == "__main__":
    asyncio.run(main())