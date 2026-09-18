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

        print("STARTING JARVIS...")

        start_result = await jarvis.start(
            1,
            db
        )

        print("START:", start_result)

        await asyncio.sleep(1)

        print("STATUS:", jarvis.get_status())

        print("STOPPING JARVIS...")

        stop_result = await jarvis.stop()

        print("STOP:", stop_result)

        print("FINAL STATUS:", jarvis.get_status())

    finally:

        db.close()


if __name__ == "__main__":
    asyncio.run(main())