
class Planner:

    def __init__(self):

        # ---------------------------------
        # INTENT → TOOL MAPPING
        # ---------------------------------

        self.tool_map = {

            # Current executable tools
            "STOP": "stop",
            "SET_TIMER": "timer",
            "CREATE_TASK": "task",
            "CREATE_REMINDER": "reminder",
            "GET_WEATHER": "weather",
            "GET_TIME": "time_tool",
            "GET_DATE": "time_tool",
            "OPEN_APPLICATION": "application_launcher",

            # Information / communication tools
            "SEARCH_INFORMATION": "search",
            "SEND_EMAIL": "email",
            "CHECK_CALENDAR": "calendar",
            "BOOK_SERVICE": "booking",
            "MANAGE_FILE": "file",
            "SEND_NOTIFICATION": "notification",

            # Browser automation
            "BROWSE_WEB": "browser",

            # Shopping
            "SHOPPING_SEARCH": "shopping",
            "SHOPPING_COMPARE": "shopping",
            "SHOPPING_CART_ADD": "shopping",
            "SHOPPING_CART_REMOVE": "shopping",
            "SHOPPING_CART_LIST": "shopping",
            "SHOPPING_PURCHASE_PREPARE": "shopping"
        }

        # ---------------------------------
        # SHOPPING ACTION MAPPING
        # ---------------------------------

        self.shopping_actions = {

            "SHOPPING_SEARCH": "search",

            "SHOPPING_COMPARE": "compare",

            "SHOPPING_CART_ADD": "cart_add",

            "SHOPPING_CART_REMOVE": "cart_remove",

            "SHOPPING_CART_LIST": "cart_list",

            "SHOPPING_PURCHASE_PREPARE": "purchase"
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
            "download",
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
    # ADD SHOPPING ACTION
    # =================================

    def _prepare_shopping_parameters(
        self,
        intent_name: str,
        parameters: dict
    ) -> dict:

        validated = dict(parameters)

        action = self.shopping_actions.get(
            intent_name
        )

        if action:

            validated["action"] = action

        return validated

    # =================================
    # NORMALIZE BROWSER ACTION
    # =================================

    def _normalize_browser_action(
        self,
        action
    ) -> str | None:

        if not isinstance(
            action,
            str
        ):

            return None

        action = action.strip().lower()

        if not action:

            return None

        # ---------------------------------
        # SUPPORTED BROWSER ACTIONS
        # ---------------------------------

        if action in self.browser_actions:

            return action

        # ---------------------------------
        # DOWNLOAD ALIASES
        # ---------------------------------

        download_aliases = {
            "download_file",
            "save_file",
            "save"
        }

        if action in download_aliases:

            return "download"

        return None

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

        normalized_action = self._normalize_browser_action(
            action
        )

        if normalized_action is None:

            action_display = (
                str(action).strip().lower()
                if isinstance(action, str)
                else str(action)
            )

            return (
                False,
                validated,
                (
                    f"Unsupported browser action "
                    f"'{action_display}'. "
                    "Use open, navigate, click, fill, read, "
                    "download, or close."
                )
            )

        action = normalized_action

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
        # URL
        # ---------------------------------

        url = validated.get(
            "url"
        )

        # ---------------------------------
        # WEBSITE DISCOVERY PARAMETERS
        # ---------------------------------

        website_name = validated.get(
            "website_name"
        )

        page_target = validated.get(
            "page_target"
        )

        has_website_name = (
            isinstance(
                website_name,
                str
            )
            and bool(
                website_name.strip()
            )
        )

        has_page_target = (
            isinstance(
                page_target,
                str
            )
            and bool(
                page_target.strip()
            )
        )

        has_website_discovery = (
            has_website_name
            or has_page_target
        )

        # ---------------------------------
        # OPEN / NAVIGATE
        #
        # Supports TWO routes:
        #
        # 1. Direct URL
        #
        #    {
        #        "action": "open",
        #        "url": "https://example.com"
        #    }
        #
        # 2. Generic website discovery
        #
        #    {
        #        "action": "open",
        #        "url": "",
        #        "website_name": "GeeksforGeeks",
        #        "page_target": "Ring Topology"
        #    }
        #
        # BrowserTool will use WebsiteDiscovery
        # for route 2.
        # ---------------------------------

        if action in {
            "open",
            "navigate"
        }:

            # ---------------------------------
            # DIRECT URL
            # ---------------------------------

            if (
                isinstance(
                    url,
                    str
                )
                and url.strip()
            ):

                validated["url"] = url.strip()

                # Clean discovery fields only if
                # they are not needed for a direct URL.
                if has_website_name:

                    validated["website_name"] = (
                        website_name.strip()
                    )

                if has_page_target:

                    validated["page_target"] = (
                        page_target.strip()
                    )

                return (
                    True,
                    validated,
                    "Browser parameters validated."
                )

            # ---------------------------------
            # GENERIC WEBSITE DISCOVERY
            # ---------------------------------

            if has_website_discovery:

                # Keep URL empty.
                #
                # BrowserTool will detect the empty URL
                # together with website_name/page_target
                # and call WebsiteDiscovery.
                validated["url"] = ""

                if has_website_name:

                    validated["website_name"] = (
                        website_name.strip()
                    )

                if has_page_target:

                    validated["page_target"] = (
                        page_target.strip()
                    )

                return (
                    True,
                    validated,
                    "Browser discovery parameters validated."
                )

            # ---------------------------------
            # NOTHING PROVIDED
            # ---------------------------------

            return (
                False,
                validated,
                (
                    f"URL or website discovery information "
                    f"is required for browser action '{action}'."
                )
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
        # CLICK / FILL / DOWNLOAD REQUIRE
        # SELECTOR OR TARGET
        # ---------------------------------

        if action in {
            "click",
            "fill",
            "download"
        }:

            selector = validated.get(
                "selector"
            )

            target = validated.get(
                "target"
            )

            has_selector = (
                isinstance(
                    selector,
                    str
                )
                and bool(
                    selector.strip()
                )
            )

            has_target = (
                isinstance(
                    target,
                    str
                )
                and bool(
                    target.strip()
                )
            )

            # Generic browser actions can use
            # either a CSS selector or a semantic target.
            if not has_selector and not has_target:

                return (
                    False,
                    validated,
                    (
                        f"Selector or target is required "
                        f"for browser action '{action}'."
                    )
                )

            if has_selector:

                validated["selector"] = selector.strip()

            if has_target:

                validated["target"] = target.strip()

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
                (
                    f"Browser step {step_number} "
                    "parameters must be a dictionary."
                )
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
        # SHOPPING PLAN
        # ---------------------------------

        if intent_name in self.shopping_actions:

            parameters = (
                self._prepare_shopping_parameters(
                    intent_name,
                    parameters
                )
            )

            steps = self._create_generic_steps(
                tool,
                parameters
            )

        # ---------------------------------
        # BROWSER PLAN
        # ---------------------------------

        elif intent_name == "BROWSE_WEB":

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
