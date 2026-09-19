import asyncio

from app.voice.jarvis_mode import JarvisMode
from app.database.connection import SessionLocal


async def main():
    db = SessionLocal()
    jarvis = JarvisMode(wake_word="Zarvis")

    try:
        print("=" * 50)
        print("REAL GEMINI + JARVIS E2E TEST")
        print("=" * 50)

        print("\nStarting Jarvis...")

        result = await jarvis.start(1, db)

        print(result)

        if not result.get("success"):
            print("\n❌ Jarvis could not start.")
            return

        print("\n" + "=" * 50)
        print("REAL GEMINI TEST")
        print("=" * 50)

        print("\nSay:")
        print("Zarvis explain artificial intelligence")

        print("\nAfter AI Buddy starts speaking, say:")
        print("Zarvis stop")

        print("\nDo NOT press Ctrl+C unless the test gets stuck.")
        print("=" * 50)

        while jarvis.active:
            await asyncio.sleep(0.2)

    except KeyboardInterrupt:
        print("\n\nKeyboard interrupt received.")

        if jarvis.active:
            print("Stopping Jarvis...")
            result = await jarvis.stop()
            print(result)

    except Exception as error:
        print("\n❌ TEST ERROR:")
        print(repr(error))

        if jarvis.active:
            try:
                await jarvis.stop()
            except Exception:
                pass

    finally:
        print("\nFinal Jarvis status:")
        print(jarvis.get_status())

        db.close()

        print("\nTest finished.")


if __name__ == "__main__":
    asyncio.run(main())