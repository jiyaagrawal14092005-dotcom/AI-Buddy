import asyncio

from app.voice.jarvis_mode import JarvisMode
from app.database.connection import SessionLocal


async def main():
    db = SessionLocal()
    jarvis = JarvisMode(wake_word="Zarvis")

    try:
        print("=" * 60)
        print("AI BUDDY — FULL JARVIS E2E TEST")
        print("=" * 60)

        print("\nStarting Jarvis...")

        start_result = await jarvis.start(1, db)
        print(start_result)

        if not start_result.get("success"):
            print("\n❌ Jarvis could not start.")
            return

        print("\n" + "=" * 60)
        print("TEST COMMAND")
        print("=" * 60)

        print("\nSay:")
        print("Zarvis explain Python in simple words")

        print("\nExpected flow:")
        print("Voice → Wake Word → Brain → Gemini/Fallback → Answer → TTS")

        print("\nIMPORTANT:")
        print("Let AI Buddy complete the answer.")
        print("Do NOT say stop during this test.")

        print("=" * 60)

        while jarvis.active:
            await asyncio.sleep(0.2)

        print("\nJarvis finished processing.")

    except KeyboardInterrupt:
        print("\n\nKeyboard interrupt received.")

        if jarvis.active:
            print("Stopping Jarvis...")
            try:
                result = await jarvis.stop()
                print(result)
            except Exception as error:
                print("Stop error:", repr(error))

    except Exception as error:
        print("\n❌ TEST ERROR:")
        print(repr(error))

    finally:
        if jarvis.active:
            try:
                await jarvis.stop()
            except Exception:
                pass

        print("\n" + "=" * 60)
        print("FINAL STATUS")
        print("=" * 60)

        status = jarvis.get_status()
        print(status)

        db.close()

        print("\nTest finished.")


if __name__ == "__main__":
    asyncio.run(main())