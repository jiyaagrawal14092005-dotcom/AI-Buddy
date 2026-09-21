import asyncio

from app.agent.intent import IntentDetector
from app.agent.planner import Planner
from app.tools.browser_tool import BrowserTool


COMMAND = (
    "Zarvis, http://127.0.0.1:8765 par jao "
    "aur AI Buddy Project Notes download karo."
)


async def main():
    print("=== STEP 1: NATURAL LANGUAGE COMMAND ===")
    print(COMMAND)

    print("\n=== STEP 2: INTENT DETECTION ===")

    detector = IntentDetector()

    intent_result = detector.detect(COMMAND)

    print(intent_result)

    if intent_result.get("intent") != "BROWSE_WEB":
        print("\nERROR: Browser intent was not detected.")
        return

    print("\n=== STEP 3: PLANNER ===")

    planner = Planner()

    plan_result = planner.create_plan(intent_result)

    print(plan_result)

    print("\n=== STEP 4: BROWSER EXECUTION ===")

    browser_tool = BrowserTool()

    user_id = 1

    browser_tool.set_user_id(user_id)

    steps = intent_result.get(
        "parameters",
        {}
    ).get(
        "steps",
        []
    )

    if not steps:
        print("ERROR: No browser steps generated.")
        return

    for step in steps:

        print(
            f"\nExecuting step {step.get('step')}: "
            f"{step.get('parameters')}"
        )

        result = await browser_tool.execute(
            step.get("parameters", {})
        )

        print("RESULT:")
        print(result)

        if not result.get("success"):
            print("\nERROR: Browser step failed.")
            break

    print("\n=== STEP 5: CLOSE BROWSER ===")

    close_result = await browser_tool.close_user_session(
        user_id
    )

    print(close_result)


if __name__ == "__main__":
    asyncio.run(main())