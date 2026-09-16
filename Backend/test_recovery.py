import asyncio

from app.recovery.retry import RetryManager
from app.recovery.recovery import RecoveryManager


# =========================================================
# SYNC OPERATION
# =========================================================

sync_attempts = 0


def sync_operation():

    global sync_attempts

    sync_attempts += 1

    if sync_attempts < 3:
        raise RuntimeError(
            "Temporary sync failure."
        )

    return {
        "success": True,
        "message": "Sync operation succeeded."
    }


# =========================================================
# ASYNC OPERATION
# =========================================================

async_attempts = 0


async def async_operation():

    global async_attempts

    async_attempts += 1

    if async_attempts < 2:
        raise RuntimeError(
            "Temporary async failure."
        )

    return {
        "success": True,
        "message": "Async operation succeeded."
    }


# =========================================================
# MAIN TEST
# =========================================================

async def main():

    retry_manager = RetryManager(
        max_retries=3,
        delay_seconds=0
    )

    recovery_manager = RecoveryManager()

    print("\n========================================")
    print("      AI BUDDY RECOVERY TEST")
    print("========================================")

    # -----------------------------------------------------
    # SYNC RETRY
    # -----------------------------------------------------

    print("\n========== SYNC RETRY ==========")

    sync_result = retry_manager.execute(
        sync_operation
    )

    print(sync_result)

    # -----------------------------------------------------
    # ASYNC RETRY
    # -----------------------------------------------------

    print("\n========== ASYNC RETRY ==========")

    async_result = await retry_manager.execute_async(
        async_operation
    )

    print(async_result)

    # -----------------------------------------------------
    # RECOVERY AFTER RETRY
    # -----------------------------------------------------

    print("\n========== RECOVERY ==========")

    recovery_result = recovery_manager.recover(
        operation="browser.open",
        error="Temporary browser failure.",
        retry_result=async_result
    )

    print(recovery_result)

    # -----------------------------------------------------
    # FAILED RECOVERY
    # -----------------------------------------------------

    print("\n========== FAILED RECOVERY ==========")

    failed_recovery = recovery_manager.recover(
        operation="browser.click",
        error="Element could not be found."
    )

    print(failed_recovery)

    # -----------------------------------------------------
    # HISTORY
    # -----------------------------------------------------

    print("\n========== RECOVERY HISTORY ==========")

    print(
        recovery_manager.get_history()
    )

    # -----------------------------------------------------
    # COUNTS
    # -----------------------------------------------------

    print("\n========== COUNTS ==========")

    print(
        "Total:",
        recovery_manager.get_recovery_count()
    )

    print(
        "Successful:",
        len(
            recovery_manager.get_successful_recoveries()
        )
    )

    print(
        "Failed:",
        len(
            recovery_manager.get_failed_recoveries()
        )
    )

    print("\n========================================")
    print("             TEST FINISHED")
    print("========================================")


if __name__ == "__main__":
    asyncio.run(main())