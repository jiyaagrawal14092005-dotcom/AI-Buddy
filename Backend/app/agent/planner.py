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

            # Future tools
            "SEARCH_INFORMATION": "search",
            "SEND_EMAIL": "email",
            "CHECK_CALENDAR": "calendar",
            "MANAGE_FILE": "file",
            "SEND_NOTIFICATION": "notification",
            "BROWSE_WEB": "browser"
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
    # CREATE EXECUTION STEPS
    # =================================

    def _create_steps(
        self,
        tool: str,
        parameters: dict
    ) -> list:

        return [
            {
                "step": 1,
                "tool": tool,
                "parameters": parameters
            }
        ]

    # =================================
    # CREATE PLAN
    # =================================

    def create_plan(
        self,
        intent: dict
    ) -> dict:

        # ---------------------------------
        # Validate input
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
        # CREATE EXECUTION STEPS
        # ---------------------------------

        steps = self._create_steps(
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