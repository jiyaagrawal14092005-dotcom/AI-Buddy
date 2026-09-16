import asyncio

from app.workflow.engine import WorkflowEngine
from app.database.connection import SessionLocal


# ============================================================
# MOCK EXECUTOR
# ============================================================

class MockExecutor:

    def __init__(self):
        self.attempts = 0

    async def execute_step(
        self,
        step,
        user_id,
        db,
    ):
        self.attempts += 1

        print(
            f"EXECUTION ATTEMPT {self.attempts}"
        )

        # ----------------------------------------------------
        # First two attempts intentionally fail
        # ----------------------------------------------------

        if self.attempts < 3:

            return {
                "success": False,
                "status": "failed",
                "browser": {
                    "action": "read",
                    "final_url": "https://example.com/",
                    "title": "Example Domain",
                },
                "message": (
                    f"Temporary failure on "
                    f"attempt {self.attempts}."
                ),
            }

        # ----------------------------------------------------
        # Third attempt succeeds
        #
        # IMPORTANT:
        # Verifier expects browser data for browser actions.
        # ----------------------------------------------------

        return {
            "success": True,
            "status": "completed",
            "browser": {
                "action": "read",
                "user_id": str(user_id),
                "requested_url": None,
                "used_current_page": True,
                "final_url": "https://example.com/",
                "title": "Example Domain",
                "content": (
                    "Example Domain\n\n"
                    "This domain is for use in "
                    "documentation examples."
                ),
            },
            "message": (
                "Operation succeeded after retry."
            ),
        }


# ============================================================
# MAIN TEST
# ============================================================

async def main():

    print()
    print("=" * 55)
    print(
        "   AI BUDDY WORKFLOW RETRY + RECOVERY TEST"
    )
    print("=" * 55)

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # CREATE WORKFLOW ENGINE
        # ----------------------------------------------------

        engine = WorkflowEngine()

        # ----------------------------------------------------
        # TEMPORARILY USE MOCK EXECUTOR
        # ----------------------------------------------------

        mock_executor = MockExecutor()

        engine.executor = mock_executor

        # ----------------------------------------------------
        # TEST PLAN
        # ----------------------------------------------------

        plan = {
            "intent": "TEST_RECOVERY",
            "tool": "browser",
            "parameters": {
                "action": "read",
            },
        }

        print()
        print("TEST PLAN:")
        print(plan)

        print()
        print("-" * 55)
        print("RUNNING WORKFLOW...")
        print("-" * 55)

        # ----------------------------------------------------
        # CREATE WORKFLOW
        # ----------------------------------------------------

        result = await engine.create_workflow(
            plan=plan,
            user_id=1,
            db=db,
        )

        # ====================================================
        # FINAL RESULT
        # ====================================================

        print()
        print("=" * 55)
        print("FINAL RESULT")
        print("=" * 55)

        print()
        print("SUCCESS:")
        print(
            result.get("success")
        )

        workflow = result.get(
            "workflow",
            {}
        )

        print()
        print("WORKFLOW:")
        print(workflow)

        print()
        print("WORKFLOW STATUS:")
        print(
            workflow.get(
                "status"
            )
        )

        print()
        print("TOTAL EXECUTION ATTEMPTS:")
        print(
            mock_executor.attempts
        )

        # ====================================================
        # RECOVERY INFORMATION
        # ====================================================

        print()
        print("-" * 55)
        print("RECOVERY INFORMATION")
        print("-" * 55)

        workflow_results = workflow.get(
            "results",
            []
        )

        assert workflow_results, (
            "Workflow should contain step results."
        )

        first_step = workflow_results[0]

        print()
        print("RECOVERY:")
        print(
            first_step.get(
                "recovery"
            )
        )

        print()
        print("ACTION RESULT:")
        print(
            first_step.get(
                "result"
            )
        )

        print()
        print("VERIFICATION:")
        print(
            first_step.get(
                "verification"
            )
        )

        # ====================================================
        # RECOVERY HISTORY
        # ====================================================

        print()
        print("-" * 55)
        print("RECOVERY HISTORY")
        print("-" * 55)

        history = engine.recovery_manager.get_history()

        print()

        for record in history:
            print(record)

        # ====================================================
        # VALIDATION
        # ====================================================

        print()
        print("-" * 55)
        print("VALIDATING TEST CONDITIONS")
        print("-" * 55)

        # ----------------------------------------------------
        # Workflow success
        # ----------------------------------------------------

        assert result.get(
            "success"
        ) is True, (
            "Workflow should succeed after retry."
        )

        # ----------------------------------------------------
        # Workflow completed
        # ----------------------------------------------------

        assert workflow.get(
            "status"
        ) == "COMPLETED", (
            "Workflow should be COMPLETED."
        )

        # ----------------------------------------------------
        # Three total attempts:
        # initial + 2 retries
        # ----------------------------------------------------

        assert mock_executor.attempts == 3, (
            "Expected exactly 3 execution attempts."
        )

        # ----------------------------------------------------
        # Recovery attempted
        # ----------------------------------------------------

        recovery = first_step.get(
            "recovery",
            {}
        )

        assert recovery.get(
            "attempted"
        ) is True, (
            "Recovery should have been attempted."
        )

        # ----------------------------------------------------
        # Recovery successful
        # ----------------------------------------------------

        assert recovery.get(
            "recovered"
        ) is True, (
            "Workflow should recover successfully."
        )

        # ----------------------------------------------------
        # Recovery method
        # ----------------------------------------------------

        assert recovery.get(
            "recovery_method"
        ) == "retry", (
            "Recovery method should be retry."
        )

        # ----------------------------------------------------
        # Recovered action result
        # ----------------------------------------------------

        action_result = first_step.get(
            "result",
            {}
        )

        assert action_result.get(
            "success"
        ) is True, (
            "Recovered action should succeed."
        )

        # ----------------------------------------------------
        # Verification
        # ----------------------------------------------------

        verification = first_step.get(
            "verification",
            {}
        )

        assert verification.get(
            "verified"
        ) is True, (
            "Recovered step should be verified."
        )

        # ----------------------------------------------------
        # Recovery history
        # ----------------------------------------------------

        history = engine.recovery_manager.get_history()

        assert len(history) == 1, (
            "Exactly one recovery record expected."
        )

        assert history[0].get(
            "recovered"
        ) is True, (
            "Recovery history should record success."
        )

        assert history[0].get(
            "recovery_method"
        ) == "retry", (
            "Recovery history method should be retry."
        )

        # ====================================================
        # SUCCESS
        # ====================================================

        print()
        print("ALL ASSERTIONS PASSED")

        print()
        print("=" * 55)
        print(
            "   RETRY + RECOVERY INTEGRATION PASSED"
        )
        print("=" * 55)

    finally:

        db.close()


# ============================================================
# RUN TEST
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())