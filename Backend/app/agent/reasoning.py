class ReasoningEngine:

    # =================================
    # EXECUTABLE INTENTS
    # =================================

    EXECUTABLE_INTENTS = {
        "SET_TIMER",
        "CREATE_TASK",
        "CREATE_REMINDER",
        "GET_WEATHER",
        "OPEN_APPLICATION",
        "SEARCH_INFORMATION"
    }

    # =================================
    # FUTURE INTENTS
    # =================================

    FUTURE_INTENTS = {
        "SEND_EMAIL",
        "BOOK_RIDE",
        "SHOP_ONLINE",
        "POST_SOCIAL_MEDIA",
        "SUBMIT_ASSIGNMENT"
    }

    # =================================
    # EXPECTED TOOLS
    # =================================

    EXPECTED_TOOLS = {
        "SET_TIMER": "timer",
        "CREATE_TASK": "task",
        "CREATE_REMINDER": "reminder",
        "GET_WEATHER": "weather",
        "OPEN_APPLICATION": "application_launcher",
        "SEARCH_INFORMATION": "search"
    }

    # =================================
    # REQUIRED PARAMETERS
    # =================================

    REQUIRED_PARAMETERS = {
        "SET_TIMER": [
            "duration_seconds"
        ],
        "CREATE_TASK": [
            "task_name"
        ],
        "CREATE_REMINDER": [
            "reminder"
        ],
        "GET_WEATHER": [
            "city"
        ],
        "OPEN_APPLICATION": [
            "application"
        ],
        "SEARCH_INFORMATION": [
            "query"
        ]
    }

    # =================================
    # MAIN REASONING METHOD
    # =================================

    def reason(
        self,
        intent: str,
        plan: dict | None = None
    ) -> dict:

        if not isinstance(
            intent,
            str
        ):

            return {
                "success": False,
                "intent": "UNKNOWN",
                "executable": False,
                "message": (
                    "Intent must be a string."
                )
            }

        intent = intent.strip().upper()

        # ---------------------------------
        # UNKNOWN INTENT
        # ---------------------------------

        if not intent:

            return {
                "success": False,
                "intent": "UNKNOWN",
                "executable": False,
                "message": (
                    "Intent cannot be empty."
                )
            }

        # ---------------------------------
        # FUTURE INTENT
        # ---------------------------------

        if intent in self.FUTURE_INTENTS:

            return {
                "success": True,
                "intent": intent,
                "executable": False,
                "message": (
                    f"Intent '{intent}' is recognised "
                    "but its execution is not available yet."
                )
            }

        # ---------------------------------
        # NOT EXECUTABLE
        # ---------------------------------

        if intent not in self.EXECUTABLE_INTENTS:

            return {
                "success": True,
                "intent": intent,
                "executable": False,
                "message": (
                    f"Intent '{intent}' cannot "
                    "be executed by the current system."
                )
            }

        # ---------------------------------
        # PLAN VALIDATION
        # ---------------------------------

        if not isinstance(
            plan,
            dict
        ):

            return {
                "success": False,
                "intent": intent,
                "executable": False,
                "message": (
                    "Execution plan must be a dictionary."
                )
            }

        tool = plan.get(
            "tool"
        )

        parameters = plan.get(
            "parameters",
            {}
        )

        if not isinstance(
            parameters,
            dict
        ):

            parameters = {}

        expected_tool = self.EXPECTED_TOOLS.get(
            intent
        )

        # ---------------------------------
        # TOOL VALIDATION
        # ---------------------------------

        if tool != expected_tool:

            return {
                "success": False,
                "intent": intent,
                "executable": False,
                "expected_tool": expected_tool,
                "received_tool": tool,
                "message": (
                    f"Intent '{intent}' requires "
                    f"tool '{expected_tool}'."
                )
            }

        # ---------------------------------
        # REQUIRED PARAMETER VALIDATION
        # ---------------------------------

        required_parameters = (
            self.REQUIRED_PARAMETERS.get(
                intent,
                []
            )
        )

        missing_parameters = []

        for parameter in required_parameters:

            value = parameters.get(
                parameter
            )

            if value is None:

                missing_parameters.append(
                    parameter
                )

            elif isinstance(
                value,
                str
            ) and not value.strip():

                missing_parameters.append(
                    parameter
                )

        if missing_parameters:

            return {
                "success": False,
                "intent": intent,
                "executable": False,
                "missing_parameters": (
                    missing_parameters
                ),
                "message": (
                    "Required parameters are missing: "
                    + ", ".join(
                        missing_parameters
                    )
                )
            }

        # ---------------------------------
        # EXECUTABLE
        # ---------------------------------

        return {
            "success": True,
            "intent": intent,
            "executable": True,
            "tool": tool,
            "parameters": parameters,
            "message": (
                f"Intent '{intent}' can be executed "
                f"using tool '{tool}'."
            )
        }

    # =================================
    # CAN EXECUTE
    # =================================

    def can_execute(
        self,
        intent: str
    ) -> bool:

        if not isinstance(
            intent,
            str
        ):

            return False

        return (
            intent.strip().upper()
            in self.EXECUTABLE_INTENTS
        )

    # =================================
    # IS FUTURE INTENT
    # =================================

    def is_future_intent(
        self,
        intent: str
    ) -> bool:

        if not isinstance(
            intent,
            str
        ):

            return False

        return (
            intent.strip().upper()
            in self.FUTURE_INTENTS
        )