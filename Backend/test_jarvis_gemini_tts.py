import asyncio

from app.voice.jarvis_mode import JarvisMode
from app.database.connection import SessionLocal


async def main():
    db = SessionLocal()
    jarvis = JarvisMode(wake_word="Zarvis")

    try:
        print("=" * 60)
        print("REAL GEMINI + JARVIS + TTS TEST")
        print("=" * 60)

        print("\nStarting Jarvis...")

        result = await jarvis.start(1, db)
        print(result)

        if not result.get("success"):
            print("\n❌ Jarvis failed to start.")
            return

        print("\n" + "=" * 60)
        print("VOICE COMMAND")
        print("=" * 60)

        print("\nSay:")
        print("Zarvis what is Python")

        print("\nWait for AI Buddy to answer.")
        print("Do NOT say stop during this test.")
        print("Let the complete answer finish.")

        print("=" * 60)

        while jarvis.active:
            await asyncio.sleep(0.2)

    except KeyboardInterrupt:
        print("\n\nKeyboard interrupt received.")

    except Exception as error:
        print("\n❌ TEST ERROR:")
        print(repr(error))

    finally:
        if jarvis.active:
            print("\nStopping Jarvis...")
            try:
                result = await jarvis.stop()
                print(result)
            except Exception as error:
                print("Stop error:", repr(error))

        print("\n" + "=" * 60)
        print("FINAL JARVIS STATUS")
        print("=" * 60)

        print(jarvis.get_status())

        db.close()

        print("\nTest finished.")


if __name__ == "__main__":
    asyncio.run(main())