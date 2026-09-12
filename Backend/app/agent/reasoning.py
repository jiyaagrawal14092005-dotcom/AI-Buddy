class ReasoningEngine:

    def __init__(self):

        self.executable_intents = {
            "CREATE_TASK": "task",
            "CREATE_REMINDER": "reminder",
            "SET_TIMER": "timer",
            "GET_WEATHER": "weather",
            "SEARCH_INFORMATION": "search",
            "SEND_EMAIL": "email",
            "CHECK_CALENDAR": "calendar",
            "MANAGE_FILE": "file",
            "BROWSE_WEB": "browser"
        }

        self.future_intents = {
            "SEND_NOTIFICATION",
            "VOICE_COMMAND",
            "CREATE_WORKFLOW",
            "SCHEDULE_JOB"
        }

    def _validate_intent(
        self,
        intent: dict
    ) -> dict:

        if not isinstance(
            intent,
            dict
        ):

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
            "intent": intent_name.strip().upper(),
            "parameters": parameters
        }

    def _validate_plan(
        self,
        plan: dict
    ) -> dict:

        if not isinstance(
            plan,
            dict
        ):

            return {
                "success": False,
                "tool": None,
                "parameters": {},
                "steps": []
            }

        tool = plan.get(
            "tool"
        )

        parameters = plan.get(
            "parameters",
            {}
        )

        steps = plan.get(
            "steps",
            []
        )

        if not isinstance(
            parameters,
            dict
        ):

            parameters = {}

        if not isinstance(
            steps,
            list
        ):

            steps = []

        return {
            "success": plan.get(
                "success",
                False
            ),
            "tool": tool,
            "parameters": parameters,
            "steps": steps
        }

    def analyze(
        self,
        intent: dict,
        plan: dict
    ) -> dict:

        validated_intent = self._validate_intent(
            intent
        )

        validated_plan = self._validate_plan(
            plan
        )

        intent_name = validated_intent[
            "intent"
        ]

        parameters = validated_intent[
            "parameters"
        ]

        if intent_name in {
            "GENERAL_QUERY"
        }:

            return {
                "success": True,
                "decision": "RESPOND",
                "tool": None,
                "parameters": parameters,
                "reason": (
                    "This request requires an AI response, "
                    "not a tool."
                )
            }

        if intent_name == "UNKNOWN":

            return {
                "success": False,
                "decision": "STOP",
                "tool": None,
                "parameters": parameters,
                "reason": (
                    "The user's request could not be understood."
                )
            }

        if intent_name in self.future_intents:

            return {
                "success": True,
                "decision": "WAIT",
                "tool": None,
                "parameters": parameters,
                "reason": (
                    f"Intent '{intent_name}' is reserved "
                    "for a future module."
                )
            }

        expected_tool = self.executable_intents.get(
            intent_name
        )

        if expected_tool is None:

            return {
                "success": False,
                "decision": "STOP",
                "tool": None,
                "parameters": parameters,
                "reason": (
                    f"Intent '{intent_name}' is not "
                    "supported by the reasoning engine."
                )
            }

        if not validated_plan["success"]:

            return {
                "success": False,
                "decision": "STOP",
                "tool": expected_tool,
                "parameters": parameters,
                "reason": (
                    "The planner could not create "
                    "a valid execution plan."
                )
            }

        plan_tool = validated_plan["tool"]

        if plan_tool != expected_tool:

            return {
                "success": False,
                "decision": "STOP",
                "tool": plan_tool,
                "parameters": parameters,
                "reason": (
                    f"Tool mismatch. Intent '{intent_name}' "
                    f"requires '{expected_tool}', but the "
                    f"plan selected '{plan_tool}'."
                )
            }

        if not validated_plan["steps"]:

            return {
                "success": False,
                "decision": "STOP",
                "tool": expected_tool,
                "parameters": parameters,
                "reason": (
                    "The execution plan contains no steps."
                )
            }

        return {
            "success": True,
            "decision": "EXECUTE",
            "tool": expected_tool,
            "parameters": parameters,
            "reason": (
                f"Intent '{intent_name}' can be executed "
                f"using the {expected_tool} tool."
            )
        }

    def can_execute(
        self,
        intent_name: str
    ) -> bool:

        if not isinstance(
            intent_name,
            str
        ):

            return False

        return (
            intent_name.strip().upper()
            in self.executable_intents
        )

    def is_future_intent(
        self,
        intent_name: str
    ) -> bool:

        if not isinstance(
            intent_name,
            str
        ):

            return False

        return (
            intent_name.strip().upper()
            in self.future_intents
        )