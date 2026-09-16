import asyncio

from app.agent.brain import AIBrain
from app.database.connection import SessionLocal


async def main():
    db = SessionLocal()

    try:
        # -------------------------------------------------
        # 1. Create ONE Brain instance
        # -------------------------------------------------
        brain = AIBrain()

        # -------------------------------------------------
        # 2. Grant calendar permission
        # -------------------------------------------------
        permission_result = (
            brain.security_manager.grant_permission(
                "user-1",
                "calendar"
            )
        )

        print("PERMISSION RESULT:")
        print(permission_result)

        # -------------------------------------------------
        # 3. Verify calendar permission
        # -------------------------------------------------
        permission_check = (
            brain.security_manager.check_permission(
                "user-1",
                "calendar"
            )
        )

        print("\nPERMISSION CHECK:")
        print(permission_check)

        if not permission_check.get(
            "allowed",
            False
        ):
            print(
                "\nCalendar permission was not granted."
            )
            return

        # -------------------------------------------------
        # 4. Send natural-language command
        # -------------------------------------------------
        command = (
            "Create a calendar event titled "
            "AI Buddy Full E2E Test "
            "on 2026-09-22 at 17:00 "
            "for 30 minutes"
        )

        result = await brain.respond(
            command,
            user_id=1,
            db=db
        )

        print("\nFIRST E2E RESULT:")
        print(result)

        # -------------------------------------------------
        # 5. Check whether approval is required
        # -------------------------------------------------
        approval_required = result.get(
            "approval_required",
            False
        )

        approval_id = result.get(
            "approval_id"
        )

        print("\nAPPROVAL REQUIRED:")
        print(approval_required)

        print("\nAPPROVAL ID:")
        print(approval_id)

        if not approval_required:
            print(
                "\nNo approval was required."
            )
            return

        if not approval_id:
            print(
                "\nApproval was required, "
                "but no approval ID was returned."
            )
            return

        # -------------------------------------------------
        # 6. Approve the SAME approval request
        # -------------------------------------------------
        approval_result = (
            brain.security_manager.approve_action(
                approval_id
            )
        )

        print("\nAPPROVAL RESULT:")
        print(approval_result)

        if not approval_result.get(
            "success",
            False
        ):
            print(
                "\nApproval could not be granted."
            )
            return

        # -------------------------------------------------
        # 7. Execute the approved command again
        # -------------------------------------------------
        final_result = await brain.respond(
            command,
            user_id=1,
            db=db,
            approval_id=approval_id
        )

        print("\nFINAL E2E RESULT:")
        print(final_result)

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())