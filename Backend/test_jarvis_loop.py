import asyncio

from app.database.connection import SessionLocal
from app.voice.jarvis_mode import JarvisMode


async def main():

    db = SessionLocal()

    jarvis = JarvisMode(
        wake_word="ai buddy",
        user_id=1,
        chunk_seconds=3
    )

    print("=" * 60)
    print("AI BUDDY - CONTINUOUS JARVIS LOOP TEST")
    print("=" * 60)

    print()
    print("INITIAL STATUS:")
    print(jarvis.get_status())

    print()
    print("Starting Jarvis Mode...")
    print()
    print("For the test, say:")
    print("AI Buddy")
    print()
    print("You can also try:")
    print("AI Buddy hello")
    print()
    print("Jarvis will automatically stop after 15 seconds.")
    print()

    try:

        # IMPORTANT:
        # JarvisMode.start() is an async method.
        start_result = await jarvis.start(
            user_id=1,
            db=db
        )

        print("START RESULT:")
        print(start_result)

        print()
        print("✅ JARVIS MODE STARTED")
        print()

        # -----------------------------------------
        # RUN FOR 15 SECONDS
        # -----------------------------------------

        for second in range(15):

            await asyncio.sleep(1)

            status = jarvis.get_status()

            print(
                f"[{second + 1:02d}s] "
                f"Active: {status['active']} | "
                f"Listening: {status['listening']} | "
                f"History: {status['history_count']}"
            )

        print()
        print("15 seconds completed.")
        print("Stopping Jarvis Mode...")

    except Exception as error:

        print()
        print("❌ JARVIS LOOP ERROR:")
        print(error)

    finally:

        # -----------------------------------------
        # STOP JARVIS
        # -----------------------------------------

        try:

            if jarvis.active:

                stop_result = await jarvis.stop()

                print()
                print("STOP RESULT:")
                print(stop_result)

        except Exception as error:

            print()
            print("⚠️ Error while stopping Jarvis:")
            print(error)

        # -----------------------------------------
        # CLOSE DATABASE
        # -----------------------------------------

        db.close()

        print()
        print("=" * 60)
        print("JARVIS LOOP TEST FINISHED")
        print("=" * 60)

        print()
        print("FINAL STATUS:")

        print(
            jarvis.get_status()
        )

        print()
        print("COMMAND HISTORY:")

        history = jarvis.get_history()

        if history:

            for index, item in enumerate(
                history,
                start=1
            ):

                print()
                print(f"Command {index}:")
                print(item)

        else:

            print(
                "No wake-word command was detected "
                "during the test."
            )


if __name__ == "__main__":

    asyncio.run(main())