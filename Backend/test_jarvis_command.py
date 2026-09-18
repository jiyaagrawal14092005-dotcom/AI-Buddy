import asyncio

from app.voice.jarvis_mode import JarvisMode
from app.database.connection import SessionLocal


async def main():

    jarvis = JarvisMode(
        wake_word="Zarvis",
        user_id=1,
        chunk_seconds=4
    )

    db = SessionLocal()

    try:

        print("=" * 60)
        print("AI BUDDY JARVIS COMMAND TEST")
        print("=" * 60)

        print("\nStarting Jarvis...")

        start_result = await jarvis.start(
            1,
            db
        )

        print("START:", start_result)

        print("\n🎤 Speak your command now.")
        print("Example:")
        print("Zarvis set a timer for 1 minute")

        await asyncio.sleep(6)

        print("\nStopping Jarvis...")

        stop_result = await jarvis.stop()

        print("STOP:", stop_result)

        print("\nJARVIS HISTORY:")

        for item in jarvis.get_history():

            print("-" * 60)
            print("Speech:", item.get("text"))
            print(
                "Wake word detected:",
                item.get("wake_word_detected")
            )
            print(
                "Command:",
                item.get("command")
            )
            print(
                "Brain input:",
                item.get("brain_input")
            )
            print(
                "Response:",
                item.get("response")
            )

        print("\nFINAL STATUS:")
        print(jarvis.get_status())

    finally:

        db.close()


if __name__ == "__main__":
    asyncio.run(main())