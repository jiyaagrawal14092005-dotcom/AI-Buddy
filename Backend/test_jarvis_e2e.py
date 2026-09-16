import asyncio

from app.database.connection import SessionLocal
from app.voice.jarvis_mode import JarvisMode


async def main():

    db = SessionLocal()

    jarvis = JarvisMode(
        wake_word="ai buddy",
        user_id=1,
        chunk_seconds=5
    )

    print("=" * 60)
    print("AI BUDDY - JARVIS REAL END-TO-END TEST")
    print("=" * 60)

    print()
    print("PIPELINE")
    print("-" * 60)
    print("Microphone")
    print("    ↓")
    print("Speech-to-Text")
    print("    ↓")
    print("Wake Word Variations")
    print("    ↓")
    print("Command Extraction")
    print("    ↓")
    print("AI Brain")
    print("    ↓")
    print("Text-to-Speech")
    print("    ↓")
    print("Voice Response")
    print("-" * 60)

    print()
    print("IMPORTANT:")
    print("Speak clearly after the test starts.")
    print()
    print("Say:")
    print("AI Buddy hello")
    print()
    print("If STT changes it to something like")
    print("'hello everybody how are you',")
    print("we will inspect the result.")
    print()

    try:

        start_result = await jarvis.start(
            user_id=1,
            db=db
        )

        print("START RESULT:")
        print(start_result)
        print()

        if not start_result.get("success"):

            print("❌ Jarvis failed to start.")
            return

        print("🎙️ JARVIS LISTENING...")
        print()

        for second in range(20):

            await asyncio.sleep(1)

            status = jarvis.get_status()

            print(
                f"[{second + 1:02d}s] "
                f"Active={status['active']} | "
                f"Listening={status['listening']} | "
                f"History={status['history_count']}"
            )

        print()
        print("⏱️ 20-second test completed.")

    except Exception as error:

        print()
        print("❌ TEST ERROR:")
        print(error)

    finally:

        print()
        print("Stopping Jarvis...")

        if jarvis.active:

            try:

                stop_result = await jarvis.stop()

                print()
                print("STOP RESULT:")
                print(stop_result)

            except Exception as error:

                print()
                print("⚠️ Stop error:")
                print(error)

        print()
        print("=" * 60)
        print("FINAL STATUS")
        print("=" * 60)

        final_status = jarvis.get_status()

        print(final_status)

        print()
        print("=" * 60)
        print("COMMAND HISTORY")
        print("=" * 60)

        history = jarvis.get_history()

        if history:

            for index, item in enumerate(
                history,
                start=1
            ):

                print()
                print(f"COMMAND {index}")
                print("-" * 40)
                print(item)

        else:

            print()
            print("No wake-word command was detected.")

        print()
        print("=" * 60)

        if history:

            print("✅ JARVIS END-TO-END PIPELINE DETECTED ACTIVITY")

        else:

            print("⚠️ JARVIS START/STOP WORKS,")
            print("BUT NO WAKE-WORD COMMAND WAS DETECTED.")

        print("=" * 60)

        db.close()


if __name__ == "__main__":

    asyncio.run(main())