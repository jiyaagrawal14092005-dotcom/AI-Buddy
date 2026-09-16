from app.agent.brain import AIBrain
from app.database.connection import SessionLocal


TEST_URL = (
    "http://127.0.0.1:8080/"
    "test_browser_page.html"
)


def run_command(
    brain,
    db,
    command
):

    print("\n" + "=" * 50)
    print("USER COMMAND")
    print("=" * 50)

    print(command)

    result = brain.respond(
        message=command,
        user_id=1,
        db=db
    )

    print("\nBRAIN RESPONSE")
    print(result)

    return result


print("=" * 50)
print(" AI BUDDY BROWSER MULTI-ACTION E2E TEST")
print("=" * 50)


brain = AIBrain()

db = SessionLocal()


try:

    # =================================
    # 1. OPEN
    # =================================

    open_result = run_command(
        brain,
        db,
        (
            "Open the browser page "
            f"{TEST_URL}"
        )
    )

    # =================================
    # 2. FILL
    # =================================

    fill_result = run_command(
        brain,
        db,
        (
            "Fill the name field on "
            f"{TEST_URL} with AI Buddy"
        )
    )

    # =================================
    # 3. CLICK
    # =================================

    click_result = run_command(
        brain,
        db,
        (
            "Click the submit button on "
            f"{TEST_URL}"
        )
    )

    # =================================
    # 4. READ
    # =================================

    read_result = run_command(
        brain,
        db,
        (
            "Read the result from "
            f"{TEST_URL}"
        )
    )

    # =================================
    # 5. CLOSE
    # =================================

    close_result = run_command(
        brain,
        db,
        "Close the browser"
    )

    # =================================
    # VERIFICATION
    # =================================

    print("\n" + "=" * 50)
    print(" FINAL VERIFICATION")
    print("=" * 50)

    results = {
        "OPEN": open_result,
        "FILL": fill_result,
        "CLICK": click_result,
        "READ": read_result,
        "CLOSE": close_result
    }

    all_passed = True

    for action, result in results.items():

        success = (
            isinstance(result, dict)
            and result.get("success") is True
        )

        print(
            f"{action}: "
            f"{'PASS' if success else 'FAIL'}"
        )

        if not success:

            all_passed = False

    # ---------------------------------
    # CHECK READ CONTENT
    # ---------------------------------

    read_content = ""

    if isinstance(
        read_result,
        dict
    ):

        action_result = (
            read_result.get(
                "action_result"
            )
        )

        if isinstance(
            action_result,
            dict
        ):

            workflow = (
                action_result.get(
                    "workflow",
                    {}
                )
            )

            if isinstance(
                workflow,
                dict
            ):

                workflow_results = (
                    workflow.get(
                        "results",
                        []
                    )
                )

                if workflow_results:

                    last_result = (
                        workflow_results[-1]
                    )

                    if isinstance(
                        last_result,
                        dict
                    ):

                        execution_result = (
                            last_result.get(
                                "result",
                                {}
                            )
                        )

                        if isinstance(
                            execution_result,
                            dict
                        ):

                            browser_data = (
                                execution_result.get(
                                    "browser",
                                    {}
                                )
                            )

                            if isinstance(
                                browser_data,
                                dict
                            ):

                                read_content = (
                                    browser_data.get(
                                        "content",
                                        ""
                                    )
                                )

    print(
        "\nREAD CONTENT:",
        read_content
    )

    if read_content == "Hello AI Buddy!":

        print(
            "READ CONTENT CHECK: PASS"
        )

    else:

        print(
            "READ CONTENT CHECK: FAIL"
        )

        all_passed = False

    # ---------------------------------
    # FINAL RESULT
    # ---------------------------------

    print("\n" + "=" * 50)

    if all_passed:

        print(
            "BROWSER MULTI-ACTION E2E TEST: PASS"
        )

    else:

        print(
            "BROWSER MULTI-ACTION E2E TEST: FAIL"
        )

    print("=" * 50)


finally:

    db.close()