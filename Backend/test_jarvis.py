import asyncio
from app.voice.jarvis_mode import JarvisMode
from app.database.connection import SessionLocal

async def test():
    db = SessionLocal()

    jarvis = JarvisMode()

    print(await jarvis.start(1, db))

    await asyncio.sleep(3)

    print(jarvis.get_status())

    print(await jarvis.stop())

    db.close()

asyncio.run(test())
