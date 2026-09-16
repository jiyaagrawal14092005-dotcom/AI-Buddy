class Planner:

    def __init__(self):

        # ---------------------------------
        # INTENT → TOOL MAPPING
        # ---------------------------------

        self.tool_map = {

            # Current executable tools
            "SET_TIMER": "timer",
            "CREATE_TASK": "task",
            "CREATE_REMINDER": "reminder",
            "GET_WEATHER": "weather",
            "OPEN_APPLICATION": "application_launcher",

            # Information / communication tools
            "SEARCH_INFORMATION": "search",
            "SEND_EMAIL": "email",
            "CHECK_CALENDAR": "calendar",
            "MANAGE_FILE": "file",
            "SEND_NOTIFICATION": "notification",

            # Browser automation
            "BROWSE_WEB": "browser"
        }

        # ---------------------------------
        # BROWSER ACTIONS
        # ---------------------------------

        self.browser_actions = {
            "open",
            "navigate",
            "click",
            "fill",
            "read",
            "close"
        }

    # =================================
    # VALIDATE INTENT
    # =================================

    def _validate_intent(
        self,
        intent: dict
    ) -> dict:

        if not isinstance(intent, dict):
            return {
                "intent": "UNKNOWN",
                "parameters": {}
            }

        intent_name = intent.get(
            "intent",
            "UNKNOWN"
        )

        if not isinstance(
            intent_name,
            str
        ) or not intent_name.strip():

            intent_name = "UNKNOWN"

        intent_name = intent_name.strip().upper()

        parameters = intent.get(
            "parameters",
            {}
        )

        if not isinstance(
            parameters,
            dict
        ):
            parameters = {}

        return {
            "intent": intent_name,
            "parameters": parameters
        }

    # =================================
    # VALIDATE BROWSER PARAMETERS
    # =================================

    def _validate_browser_parameters(
        self,
        parameters: dict
    ) -> tuple[bool, dict, str]:

        if not isinstance(
            parameters,
            dict
        ):
            return (
                False,
                {},
                "Browser parameters must be a dictionary."
            )

        validated = dict(parameters)

        action = validated.get(
            "action"
        )

        # ---------------------------------
        # ACTION REQUIRED
        # ---------------------------------

        if not isinstance(
            action,
            str
        ) or not action.strip():

            return (
                False,
                validated,
                "Browser action is required."
            )

        action = action.strip().lower()

        # ---------------------------------
        # ACTION VALIDATION
        # ---------------------------------

        if action not in self.browser_actions:

            return (
                False,
                validated,
                (
                    f"Unsupported browser action '{action}'. "
                    "Use open, navigate, click, fill, read, or close."
                )
            )

        validated["action"] = action

        # ---------------------------------
        # CLOSE DOES NOT NEED URL
        # ---------------------------------

        if action == "close":

            return (
                True,
                validated,
                "Browser parameters validated."
            )

        # ---------------------------------
        # OPEN / NAVIGATE REQUIRE URL
        # ---------------------------------

        url = validated.get(
            "url"
        )

        if action in {
            "open",
            "navigate"
        }:

            if not isinstance(
                url,
                str
            ) or not url.strip():

                return (
                    False,
                    validated,
                    f"URL is required for browser action '{action}'."
                )

            validated["url"] = url.strip()

            return (
                True,
                validated,
                "Browser parameters validated."
            )

        # ---------------------------------
        # EXISTING PAGE ACTIONS
        # ---------------------------------

        if isinstance(
            url,
            str
        ) and url.strip():

            validated["url"] = url.strip()
            validated["use_current_page"] = False

        else:

            validated.pop(
                "url",
                None
            )

            validated["use_current_page"] = True

        # ---------------------------------
        # CLICK / FILL REQUIRE SELECTOR
        # ---------------------------------

        if action in {
            "click",
            "fill"
        }:

            selector = validated.get(
                "selector"
            )

            if not isinstance(
                selector,
                str
            ) or not selector.strip():

                return (
                    False,
                    validated,
                    (
                        f"Selector is required for "
                        f"browser action '{action}'."
                    )
                )

            validated["selector"] = selector.strip()

        # ---------------------------------
        # FILL REQUIRES VALUE
        # ---------------------------------

        if action == "fill":

            value = validated.get(
                "value"
            )

            if not isinstance(
                value,
                str
            ):

                return (
                    False,
                    validated,
                    "Value is required for browser fill action."
                )

            validated["value"] = value

        # ---------------------------------
        # READ SELECTOR IS OPTIONAL
        # ---------------------------------

        if action == "read":

            selector = validated.get(
                "selector"
            )

            if selector is not None:

                if not isinstance(
                    selector,
                    str
                ) or not selector.strip():

                    return (
                        False,
                        validated,
                        "Read selector must be valid text."
                    )

                validated["selector"] = selector.strip()

        return (
            True,
            validated,
            "Browser parameters validated."
        )

    # =================================
    # CREATE SINGLE EXECUTION STEP
    # =================================

    def _create_step(
        self,
        step_number: int,
        tool: str,
        parameters: dict
    ) -> dict:

        return {
            "step": step_number,
            "tool": tool,
            "parameters": dict(parameters)
        }

    # =================================
    # CREATE SINGLE STEP LIST
    # =================================

    def _create_steps(
        self,
        tool: str,
        parameters: dict
    ) -> list:

        return [
            self._create_step(
                1,
                tool,
                parameters
            )
        ]

    # =================================
    # NORMALIZE BROWSER STEP
    # =================================

    def _normalize_browser_step(
        self,
        step,
        step_number: int
    ) -> tuple[bool, dict, str]:

        if not isinstance(
            step,
            dict
        ):

            return (
                False,
                {},
                f"Browser step {step_number} must be a dictionary."
            )

        parameters = step.get(
            "parameters",
            {}
        )

        if not isinstance(
            parameters,
            dict
        ):

            return (
                False,
                {},
                f"Browser step {step_number} parameters must be a dictionary."
            )

        valid, validated, message = (
            self._validate_browser_parameters(
                parameters
            )
        )

        if not valid:

            return (
                False,
                validated,
                f"Browser step {step_number}: {message}"
            )

        return (
            True,
            validated,
            "Browser step validated."
        )

    # =================================
    # CREATE MULTI-STEP BROWSER PLAN
    # =================================

    def _create_browser_steps(
        self,
        parameters: dict
    ) -> tuple[bool, list, str]:

        if not isinstance(
            parameters,
            dict
        ):

            return (
                False,
                [],
                "Browser parameters must be a dictionary."
            )

        # ---------------------------------
        # CHECK FOR EXPLICIT STEPS
        # ---------------------------------

        raw_steps = parameters.get(
            "steps"
        )

        if isinstance(
            raw_steps,
            list
        ) and raw_steps:

            steps = []

            for index, raw_step in enumerate(
                raw_steps,
                start=1
            ):

                valid, validated, message = (
                    self._normalize_browser_step(
                        raw_step,
                        index
                    )
                )

                if not valid:

                    return (
                        False,
                        steps,
                        message
                    )

                steps.append(
                    self._create_step(
                        index,
                        "browser",
                        validated
                    )
                )

            return (
                True,
                steps,
                "Multi-step browser plan created."
            )

        # ---------------------------------
        # SINGLE BROWSER ACTION
        # ---------------------------------

        valid, validated, message = (
            self._validate_browser_parameters(
                parameters
            )
        )

        if not valid:

            return (
                False,
                [],
                message
            )

        return (
            True,
            [
                self._create_step(
                    1,
                    "browser",
                    validated
                )
            ],
            "Single browser step created."
        )

    # =================================
    # CREATE GENERIC MULTI-STEP PLAN
    # =================================

    def _create_generic_steps(
        self,
        tool: str,
        parameters: dict
    ) -> list:

        raw_steps = parameters.get(
            "steps"
        )

        # ---------------------------------
        # EXPLICIT MULTI-STEP PLAN
        # ---------------------------------

        if isinstance(
            raw_steps,
            list
        ) and raw_steps:

            steps = []

            for index, raw_step in enumerate(
                raw_steps,
                start=1
            ):

                if not isinstance(
                    raw_step,
                    dict
                ):

                    continue

                step_tool = raw_step.get(
                    "tool",
                    tool
                )

                step_parameters = raw_step.get(
                    "parameters",
                    {}
                )

                if not isinstance(
                    step_tool,
                    str
                ):

                    step_tool = tool

                if not isinstance(
                    step_parameters,
                    dict
                ):

                    step_parameters = {}

                steps.append(
                    self._create_step(
                        index,
                        step_tool,
                        step_parameters
                    )
                )

            if steps:

                return steps

        # ---------------------------------
        # DEFAULT SINGLE STEP
        # ---------------------------------

        return self._create_steps(
            tool,
            parameters
        )

    # =================================
    # CREATE PLAN
    # =================================

    def create_plan(
        self,
        intent: dict
    ) -> dict:

        # ---------------------------------
        # VALIDATE INPUT
        # ---------------------------------

        validated = self._validate_intent(
            intent
        )

        intent_name = validated["intent"]
        parameters = validated["parameters"]

        # ---------------------------------
        # GENERAL / UNKNOWN REQUEST
        # ---------------------------------

        if intent_name in [
            "GENERAL_QUERY",
            "UNKNOWN"
        ]:

            return {
                "success": True,
                "intent": intent_name,
                "tool": None,
                "parameters": parameters,
                "steps": [],
                "message": (
                    "No tool required for this request."
                )
            }

        # ---------------------------------
        # FIND REQUIRED TOOL
        # ---------------------------------

        tool = self.tool_map.get(
            intent_name
        )

        # ---------------------------------
        # TOOL NOT AVAILABLE
        # ---------------------------------

        if not tool:

            return {
                "success": False,
                "intent": intent_name,
                "tool": None,
                "parameters": parameters,
                "steps": [],
                "message": (
                    f"No tool is mapped to "
                    f"intent '{intent_name}'."
                )
            }

        # ---------------------------------
        # BROWSER PLAN
        # ---------------------------------

        if intent_name == "BROWSE_WEB":

            valid, steps, message = (
                self._create_browser_steps(
                    parameters
                )
            )

            if not valid:

                return {
                    "success": False,
                    "intent": intent_name,
                    "tool": tool,
                    "parameters": parameters,
                    "steps": steps,
                    "message": message
                }

        else:

            # ---------------------------------
            # GENERIC PLAN
            # ---------------------------------

            steps = self._create_generic_steps(
                tool,
                parameters
            )

        # ---------------------------------
        # RETURN PLAN
        # ---------------------------------

        return {
            "success": True,
            "intent": intent_name,
            "tool": tool,
            "parameters": parameters,
            "steps": steps,
            "message": (
                f"Plan created: use {tool} tool."
            )
        }

    # =================================
    # GET TOOL FOR INTENT
    # =================================

    def get_tool(
        self,
        intent_name: str
    ):

        if not isinstance(
            intent_name,
            str
        ):

            return None

        return self.tool_map.get(
            intent_name.strip().upper()
        )

    # =================================
    # CHECK WHETHER TOOL EXISTS
    # =================================

    def has_tool(
        self,
        intent_name: str
    ) -> bool:

        return (
            self.get_tool(
                intent_name
            ) is not None
        )