import asyncio

from app.agent.brain import AIBrain
from app.database.connection import SessionLocal


async def main():

    db = SessionLocal()

    try:

        brain = AIBrain()

        result = await brain.respond(
            "Show my upcoming calendar events.",
            user_id=2,
            db=db
        )

        print(result)

    finally:

        db.close()


asyncio.run(main())