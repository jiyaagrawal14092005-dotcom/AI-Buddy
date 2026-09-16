from app.verification.verifier import Verifier


def main():

    verifier = Verifier()

    print("\n========================================")
    print("       AI BUDDY VERIFIER TEST")
    print("========================================")

    # ========================================================
    # OPEN TEST
    # ========================================================

    print("\n========== OPEN TEST ==========")

    open_result = {
        "success": True,
        "browser": {
            "action": "open",
            "final_url": "https://example.com/",
            "title": "Example Domain",
            "status_code": 200
        }
    }

    result = verifier.verify_action(
        action="open",
        result=open_result
    )

    print(result)

    # ========================================================
    # READ TEST
    # ========================================================

    print("\n========== READ TEST ==========")

    read_result = {
        "success": True,
        "browser": {
            "action": "read",
            "final_url": "https://example.com/",
            "title": "Example Domain",
            "content": "Example Domain\nLearn more"
        }
    }

    result = verifier.verify_action(
        action="read",
        result=read_result
    )

    print(result)

    # ========================================================
    # FILL TEST
    # ========================================================

    print("\n========== FILL TEST ==========")

    fill_result = {
        "success": True,
        "browser": {
            "action": "fill",
            "final_url": "https://example.com/",
            "title": "Example Domain",
            "value_length": 4
        }
    }

    result = verifier.verify_action(
        action="fill",
        result=fill_result
    )

    print(result)

    # ========================================================
    # FAILED ACTION TEST
    # ========================================================

    print("\n========== FAILED ACTION TEST ==========")

    failed_result = {
        "success": False,
        "message": "Browser action failed."
    }

    result = verifier.verify_action(
        action="click",
        result=failed_result
    )

    print(result)

    # ========================================================
    # WORKFLOW TEST
    # ========================================================

    print("\n========== WORKFLOW TEST ==========")

    workflow = {
        "status": "COMPLETED",
        "results": [
            {
                "step": {
                    "step_id": 1,
                    "tool": "browser",
                    "parameters": {
                        "action": "open",
                        "url": "https://example.com"
                    }
                },
                "result": {
                    "success": True,
                    "browser": {
                        "action": "open",
                        "final_url": "https://example.com/",
                        "title": "Example Domain",
                        "status_code": 200
                    }
                }
            },
            {
                "step": {
                    "step_id": 2,
                    "tool": "browser",
                    "parameters": {
                        "action": "read",
                        "selector": "body"
                    }
                },
                "result": {
                    "success": True,
                    "browser": {
                        "action": "read",
                        "final_url": "https://example.com/",
                        "title": "Example Domain",
                        "content": "Example Domain\nLearn more"
                    }
                }
            }
        ]
    }

    result = verifier.verify_workflow(
        workflow
    )

    print(result)

    # ========================================================
    # RESPONSE TEST
    # ========================================================

    print("\n========== RESPONSE TEST ==========")

    response = {
        "message": "Browser workflow executed successfully."
    }

    result = verifier.verify_response(
        response
    )

    print(result)

    # ========================================================
    # FINISHED
    # ========================================================

    print("\n========================================")
    print("             TEST FINISHED")
    print("========================================")


if __name__ == "__main__":
    main()