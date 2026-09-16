class ReasoningEngine:

    EXECUTABLE_INTENTS = {
        "SET_TIMER",
        "CREATE_TASK",
        "CREATE_REMINDER",
        "GET_WEATHER",
        "OPEN_APPLICATION",
        "SEARCH_INFORMATION",
        "SEND_EMAIL",
        "BROWSE_WEB"
    }

    FUTURE_INTENTS = {
        "BOOK_RIDE",
        "SHOP_ONLINE",
        "POST_SOCIAL_MEDIA",
        "SUBMIT_ASSIGNMENT"
    }

    EXPECTED_TOOLS = {
        "SET_TIMER": "timer",
        "CREATE_TASK": "task",
        "CREATE_REMINDER": "reminder",
        "GET_WEATHER": "weather",
        "OPEN_APPLICATION": "application_launcher",
        "SEARCH_INFORMATION": "search",
        "SEND_EMAIL": "email",
        "BROWSE_WEB": "browser"
    }

    REQUIRED_PARAMETERS = {
        "SET_TIMER": ["duration_seconds"],
        "CREATE_TASK": ["task_name"],
        "CREATE_REMINDER": ["reminder"],
        "GET_WEATHER": ["city"],
        "OPEN_APPLICATION": ["application"],
        "SEARCH_INFORMATION": ["query"],
        "SEND_EMAIL": ["recipient", "subject", "message"],
        "BROWSE_WEB": ["action"]
    }

    def reason(
        self,
        intent: str,
        plan: dict | None = None
    ) -> dict:

        # =========================================
        # VALIDATE INTENT
        # =========================================

        if not isinstance(intent, str):
            return {
                "success": False,
                "intent": "UNKNOWN",
                "executable": False,
                "message": "Intent must be a string."
            }

        intent = intent.strip().upper()

        if not intent:
            return {
                "success": False,
                "intent": "UNKNOWN",
                "executable": False,
                "message": "Intent cannot be empty."
            }

        # =========================================
        # FUTURE INTENTS
        # =========================================

        if intent in self.FUTURE_INTENTS:
            return {
                "success": True,
                "intent": intent,
                "executable": False,
                "message": (
                    f"Intent '{intent}' is recognised but "
                    "its execution is not available yet."
                )
            }

        # =========================================
        # UNKNOWN / NON-EXECUTABLE INTENTS
        # =========================================

        if intent not in self.EXECUTABLE_INTENTS:
            return {
                "success": True,
                "intent": intent,
                "executable": False,
                "message": (
                    f"Intent '{intent}' cannot be executed "
                    "by the current system."
                )
            }

        # =========================================
        # VALIDATE PLAN
        # =========================================

        if not isinstance(plan, dict):
            return {
                "success": False,
                "intent": intent,
                "executable": False,
                "message": "Execution plan must be a dictionary."
            }

        tool = plan.get("tool")

        parameters = plan.get(
            "parameters",
            {}
        )

        if not isinstance(parameters, dict):
            parameters = {}

        # =========================================
        # VALIDATE EXPECTED TOOL
        # =========================================

        expected_tool = self.EXPECTED_TOOLS.get(
            intent
        )

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

        # =========================================
        # REQUIRED PARAMETERS
        # =========================================

        required_parameters = self.REQUIRED_PARAMETERS.get(
            intent,
            []
        )

        missing_parameters = []

        for parameter in required_parameters:

            # -------------------------------------
            # TIMER SPECIAL CASE
            # -------------------------------------

            if (
                intent == "SET_TIMER"
                and parameter == "duration_seconds"
            ):
                value = parameters.get(
                    "duration_seconds"
                )

                if value is None:
                    value = parameters.get(
                        "duration"
                    )

            else:
                value = parameters.get(
                    parameter
                )

            # -------------------------------------
            # CHECK MISSING VALUE
            # -------------------------------------

            if value is None:
                missing_parameters.append(
                    parameter
                )

            elif (
                isinstance(value, str)
                and not value.strip()
            ):
                missing_parameters.append(
                    parameter
                )

        # =========================================
        # BROWSER VALIDATION
        # =========================================

        if intent == "BROWSE_WEB":

            action = parameters.get(
                "action"
            )

            # -------------------------------------
            # ACTION REQUIRED
            # -------------------------------------

            if (
                not isinstance(action, str)
                or not action.strip()
            ):
                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": "Browser action is required."
                }

            action = action.strip().lower()

            # -------------------------------------
            # ALLOWED ACTIONS
            # -------------------------------------

            allowed_browser_actions = {
                "open",
                "navigate",
                "click",
                "fill",
                "read",
                "close"
            }

            if action not in allowed_browser_actions:
                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        f"Unsupported browser action "
                        f"'{action}'."
                    )
                }

            # -------------------------------------
            # URL REQUIREMENT
            #
            # open / navigate:
            # URL is required.
            #
            # click / fill / read:
            # Can operate on the current page.
            #
            # close:
            # Does not need URL.
            # -------------------------------------

            if action in {
                "open",
                "navigate"
            }:

                url = parameters.get(
                    "url"
                )

                if (
                    not isinstance(url, str)
                    or not url.strip()
                ):
                    return {
                        "success": False,
                        "intent": intent,
                        "executable": False,
                        "message": (
                            f"URL is required for "
                            f"browser action '{action}'."
                        )
                    }

            # -------------------------------------
            # CURRENT PAGE ACTIONS
            # -------------------------------------

            elif action in {
                "click",
                "fill",
                "read"
            }:

                # If URL is not supplied, explicitly
                # mark that the current browser page
                # should be used.

                if not parameters.get(
                    "url"
                ):
                    parameters["use_current_page"] = True

            # -------------------------------------
            # CLICK / FILL SELECTOR
            # -------------------------------------

            if action in {
                "click",
                "fill"
            }:

                selector = parameters.get(
                    "selector"
                )

                if (
                    not isinstance(selector, str)
                    or not selector.strip()
                ):
                    return {
                        "success": False,
                        "intent": intent,
                        "executable": False,
                        "message": (
                            f"Selector is required "
                            f"for browser action "
                            f"'{action}'."
                        )
                    }

            # -------------------------------------
            # FILL VALUE
            # -------------------------------------

            if action == "fill":

                value = parameters.get(
                    "value"
                )

                if value is None:
                    return {
                        "success": False,
                        "intent": intent,
                        "executable": False,
                        "message": (
                            "Value is required for "
                            "browser fill action."
                        )
                    }

                if not isinstance(
                    value,
                    str
                ):
                    return {
                        "success": False,
                        "intent": intent,
                        "executable": False,
                        "message": (
                            "Browser fill value "
                            "must be text."
                        )
                    }

        # =========================================
        # MISSING PARAMETERS
        # =========================================

        if missing_parameters:
            return {
                "success": False,
                "intent": intent,
                "executable": False,
                "missing_parameters": missing_parameters,
                "message": (
                    "Required parameters are missing: "
                    + ", ".join(
                        missing_parameters
                    )
                )
            }

        # =========================================
        # SUCCESS
        # =========================================

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

    # =============================================
    # CAN EXECUTE
    # =============================================

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

    # =============================================
    # FUTURE INTENT CHECK
    # =============================================

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