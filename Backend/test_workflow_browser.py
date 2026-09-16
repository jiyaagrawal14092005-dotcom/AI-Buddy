import asyncio

from app.database.connection import SessionLocal
from app.workflow.engine import WorkflowEngine


async def test():
    db = SessionLocal()

    try:
        engine = WorkflowEngine()

        plan = {
            "success": True,
            "intent": "BROWSE_WEB",
            "tool": "browser",
            "parameters": {
                "action": "open",
                "url": "http://127.0.0.1:5500/test_form.html"
            }
        }

        print("STARTING WORKFLOW TEST...")

        result = await engine.create_workflow(
            plan=plan,
            user_id=1,
            db=db
        )

        print("\nWORKFLOW RESULT:")
        print(result)

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(test())