import asyncio

from app.agent.brain import AIBrain
from app.database.connection import SessionLocal


TEST_URL = (
    "http://127.0.0.1:8080/"
    "test_browser_page.html"
)


print("========================================")
print(" AI BUDDY BRAIN BROWSER E2E TEST")
print("========================================")


async def main():

    brain = AIBrain()
    db = SessionLocal()

    try:

        # ---------------------------------
        # TEST COMMAND
        # ---------------------------------

        message = (
            "Open the browser page "
            "http://127.0.0.1:8080/test_browser_page.html"
        )

        print("\nUSER COMMAND:")
        print(message)

        # ---------------------------------
        # BRAIN RESPONSE
        # ---------------------------------

        result = await brain.respond(
            message=message,
            user_id=1,
            db=db
        )

        print("\n========================================")
        print("BRAIN RESPONSE")
        print("========================================")

        print(result)

        # ---------------------------------
        # INTENT
        # ---------------------------------

        print("\n========================================")
        print("DETECTED INTENT")
        print("========================================")

        intent = result.get(
            "intent"
        )

        print(intent)

        # ---------------------------------
        # PLAN
        # ---------------------------------

        print("\n========================================")
        print("PLAN")
        print("========================================")

        plan = result.get(
            "plan"
        )

        print(plan)

        # ---------------------------------
        # REASONING
        # ---------------------------------

        print("\n========================================")
        print("REASONING")
        print("========================================")

        reasoning = result.get(
            "reasoning"
        )

        print(reasoning)

        # ---------------------------------
        # ACTION RESULT
        # ---------------------------------

        print("\n========================================")
        print("ACTION RESULT")
        print("========================================")

        action_result = result.get(
            "action_result"
        )

        print(action_result)

        # ---------------------------------
        # FINAL MESSAGE
        # ---------------------------------

        print("\n========================================")
        print("FINAL MESSAGE")
        print("========================================")

        print(
            result.get(
                "message"
            )
        )

        # ---------------------------------
        # VERIFICATION
        # ---------------------------------

        print("\n========================================")
        print("FINAL VERIFICATION")
        print("========================================")

        intent_name = None

        if isinstance(
            intent,
            dict
        ):

            intent_name = intent.get(
                "intent"
            )

        elif isinstance(
            intent,
            str
        ):

            intent_name = intent

        plan_tool = None

        if isinstance(
            plan,
            dict
        ):

            plan_tool = plan.get(
                "tool"
            )

        workflow_success = False

        if isinstance(
            action_result,
            dict
        ):

            workflow_success = (
                action_result.get(
                    "success"
                ) is True
            )

        print(
            "Intent:",
            intent_name
        )

        print(
            "Plan Tool:",
            plan_tool
        )

        print(
            "Workflow Success:",
            workflow_success
        )

        # ---------------------------------
        # EXPECTED RESULT
        # ---------------------------------

        if (
            intent_name == "BROWSE_WEB"
            and plan_tool == "browser"
            and workflow_success
        ):

            print(
                "\nBRAIN → PLANNER → WORKFLOW "
                "→ BROWSER TEST: PASS"
            )

        else:

            print(
                "\nBRAIN → PLANNER → WORKFLOW "
                "→ BROWSER TEST: FAIL"
            )

    finally:

        db.close()

        # ---------------------------------
        # CLOSE BROWSER SESSION
        # ---------------------------------

        try:

            browser_tool = brain.tools.get(
                "browser"
            )

            if browser_tool is not None:

                await browser_tool.execute(
                    {
                        "action": "close",
                        "user_id": 1
                    }
                )

        except Exception as error:

            print(
                "Browser cleanup failed:",
                error
            )


if __name__ == "__main__":

    asyncio.run(
        main()
    )