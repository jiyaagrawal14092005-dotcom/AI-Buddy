import asyncio

from app.voice.conversation import VoiceConversation
from app.database.connection import SessionLocal


async def main():

    conversation = VoiceConversation(
        wake_word="ai buddy"
    )

    print("START:")
    print(
        conversation.start()
    )

    db = SessionLocal()

    test_cases = [
        "ai buddy create a task to study Python",
        "AI Buddy set a timer for 10 minutes",
    ]

    try:

        for text in test_cases:

            print()
            print("=" * 60)
            print("INPUT:", text)

            result = await conversation.process_input(
                text,
                1,
                db
            )

            print(
                "SUCCESS:",
                result.get("success")
            )

            print(
                "WAKE WORD DETECTED:",
                result.get(
                    "wake_word_detected"
                )
            )

            print(
                "BRAIN INPUT:",
                result.get(
                    "brain_input"
                )
            )

            print(
                "COMMAND:",
                result.get(
                    "command"
                )
            )

            print(
                "RESPONSE:",
                result.get(
                    "response"
                )
            )

            print(
                "MESSAGE:",
                result.get(
                    "message"
                )
            )

            print(
                "VOICE RESPONSE:",
                result.get(
                    "voice_response"
                )
            )

        print()
        print("=" * 60)
        print("HISTORY COUNT:")

        print(
            len(
                conversation.get_history()
            )
        )

        print()
        print("STATUS:")

        print(
            conversation.get_status()
        )

    finally:

        db.close()


if __name__ == "__main__":

    asyncio.run(
        main()
    )