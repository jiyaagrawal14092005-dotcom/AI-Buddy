import asyncio

from app.agent.brain import AIBrain
from app.database.connection import SessionLocal


async def main():

    db = SessionLocal()

    try:

        print("\n========================================")
        print("   AI BUDDY 3-STEP BROWSER E2E TEST")
        print("========================================")

        brain = AIBrain()

        message = (
            "Zarvis, http://127.0.0.1:8765 par jao, "
            "page read karo aur AI Buddy Project Notes download karo."
        )

        print("\nUSER COMMAND:")
        print(message)

        print("\n----------------------------------------")
        print("RUNNING AI BUDDY...")
        print("----------------------------------------")

        result = await brain.respond(
            message=message,
            user_id=1,
            db=db
        )

        print("\n========================================")
        print("FINAL RESULT")
        print("========================================")

        print("\nSUCCESS:")
        print(result.get("success"))

        print("\nINTENT:")
        print(result.get("intent"))

        print("\nPLAN:")
        print(result.get("plan"))

        print("\nREASONING:")
        print(result.get("reasoning"))

        print("\nMESSAGE:")
        print(result.get("message"))

        print("\nACTION RESULT:")

        action_result = result.get("action_result")
        print(action_result)

        print("\nAPPROVAL:")
        print(result.get("approval"))

        # ---------------------------------
        # WORKFLOW DETAILS
        # ---------------------------------

        if isinstance(action_result, dict):

            workflow = action_result.get("workflow")

            if isinstance(workflow, dict):

                print("\n========================================")
                print("WORKFLOW DETAILS")
                print("========================================")

                print("\nWORKFLOW ID:")
                print(workflow.get("workflow_id"))

                print("\nSTATUS:")
                print(workflow.get("status"))

                print("\nCURRENT STEP:")
                print(workflow.get("current_step"))

                print("\nTOTAL STEPS:")
                print(workflow.get("total_steps"))

                print("\nSTEP RESULTS:")

                for step_result in workflow.get("results", []):
                    print(step_result)

        print("\n========================================")
        print("TEST FINISHED")
        print("========================================")

    finally:

        db.close()


if __name__ == "__main__":
    asyncio.run(main())