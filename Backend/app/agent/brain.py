from google import genai

from app.agent.context import ContextManager
from app.agent.intent import IntentDetector
from app.agent.planner import Planner
from app.agent.reasoning import ReasoningEngine

from app.tools.task import TaskTool
from app.tools.reminder import ReminderTool
from app.tools.timer import TimerTool
from app.tools.weather import WeatherTool
from app.tools.search_tool import SearchTool
from app.tools.email_tool import EmailTool
from app.tools.calendar_tool import CalendarTool
from app.tools.file_tool import FileTool
from app.tools.browser_tool import BrowserTool


class AIBrain:

    def __init__(self):

        self.intent_detector = IntentDetector()

        self.planner = Planner()

        self.reasoning_engine = ReasoningEngine()

        self.context_manager = ContextManager()

        self.tools = {
            "task": TaskTool(),
            "reminder": ReminderTool(),
            "timer": TimerTool(),
            "weather": WeatherTool(),
            "search": SearchTool(),
            "email": EmailTool(),
            "calendar": CalendarTool(),
            "file": FileTool(),
            "browser": BrowserTool()
        }

        self.client = None

        try:

            self.client = genai.Client()

        except Exception:

            self.client = None

    def _execute_tool(
        self,
        tool_name: str,
        parameters: dict
    ) -> dict:

        tool = self.tools.get(
            tool_name
        )

        if tool is None:

            return {
                "success": False,
                "message": (
                    f"Tool '{tool_name}' "
                    "is not available."
                )
            }

        try:

            if tool_name == "task":

                task_name = parameters.get(
                    "task_name",
                    parameters.get(
                        "title",
                        ""
                    )
                )

                return tool.create_task(
                    task_name
                )

            if tool_name == "reminder":

                reminder_text = parameters.get(
                    "reminder",
                    parameters.get(
                        "text",
                        parameters.get(
                            "message",
                            ""
                        )
                    )
                )

                return tool.create_reminder(
                    reminder_text
                )

            if tool_name == "timer":

                duration = parameters.get(
                    "duration",
                    parameters.get(
                        "minutes",
                        0
                    )
                )

                return tool.set_timer(
                    duration
                )

            if tool_name == "weather":

                city = parameters.get(
                    "city",
                    ""
                )

                return tool.get_weather(
                    city
                )

            return tool.execute(
                parameters
            )

        except Exception as e:

            return {
                "success": False,
                "message": (
                    f"Tool execution failed: {str(e)}"
                )
            }

    def _generate_general_response(
        self,
        message: str
    ) -> str:

        if self.client is None:

            return (
                "I understand your request, "
                "but I am unable to generate "
                "an AI response right now."
            )

        try:

            response = self.client.models.generate_content(
                model="gemini-3.7-flash",
                contents=message
            )

            if response.text:

                return response.text.strip()

        except Exception:

            pass

        return (
            "I understand your request, "
            "but I could not generate a response right now."
        )

    def _build_action_message(
        self,
        action_result: dict
    ) -> str:

        if not action_result:

            return (
                "The requested action could not be processed."
            )

        if action_result.get(
            "success",
            False
        ):

            return action_result.get(
                "message",
                "Action completed successfully."
            )

        return action_result.get(
            "message",
            "The action could not be completed."
        )

    def _store_context(
        self,
        message: str,
        response_message: str
    ) -> None:

        try:

            self.context_manager.add_message(
                message,
                response_message
            )

        except Exception as e:

            print(
                f"Context storage failed: {e}"
            )

    def respond(
        self,
        message: str
    ) -> dict:

        if not isinstance(
            message,
            str
        ) or not message.strip():

            return {
                "success": False,
                "intent": None,
                "plan": None,
                "reasoning": None,
                "message": (
                    "Message cannot be empty."
                ),
                "action_result": None,
                "context": []
            }

        message = message.strip()

        try:

            intent = self.intent_detector.detect(
                message
            )

        except Exception as e:

            return {
                "success": False,
                "intent": None,
                "plan": None,
                "reasoning": None,
                "message": (
                    f"Intent detection failed: {str(e)}"
                ),
                "action_result": None,
                "context": []
            }

        try:

            plan = self.planner.create_plan(
                intent
            )

        except Exception as e:

            return {
                "success": False,
                "intent": intent,
                "plan": None,
                "reasoning": None,
                "message": (
                    f"Planning failed: {str(e)}"
                ),
                "action_result": None,
                "context": []
            }

        try:

            reasoning = self.reasoning_engine.analyze(
                intent,
                plan
            )

        except Exception as e:

            return {
                "success": False,
                "intent": intent,
                "plan": plan,
                "reasoning": None,
                "message": (
                    f"Reasoning failed: {str(e)}"
                ),
                "action_result": None,
                "context": []
            }

        intent_name = intent.get(
            "intent",
            "UNKNOWN"
        )

        action_result = None

        if intent_name == "GENERAL_QUERY":

            response_message = (
                self._generate_general_response(
                    message
                )
            )

        elif not plan.get(
            "success",
            False
        ):

            response_message = plan.get(
                "message",
                "Unable to create a plan."
            )

        elif reasoning.get(
            "decision"
        ) != "EXECUTE":

            response_message = reasoning.get(
                "reason",
                "The request cannot be executed."
            )

        else:

            steps = plan.get(
                "steps",
                []
            )

            if not steps:

                response_message = (
                    "No executable action was found "
                    "for this request."
                )

            else:

                first_step = steps[0]

                tool_name = first_step.get(
                    "tool"
                )

                parameters = first_step.get(
                    "parameters",
                    {}
                )

                action_result = self._execute_tool(
                    tool_name,
                    parameters
                )

                response_message = (
                    self._build_action_message(
                        action_result
                    )
                )

        self._store_context(
            message,
            response_message
        )

        try:

            context = self.context_manager.get_history()

        except Exception as e:

            print(
                f"Context retrieval failed: {e}"
            )

            context = []

        return {
            "success": True,
            "intent": intent,
            "plan": plan,
            "reasoning": reasoning,
            "message": response_message,
            "action_result": action_result,
            "context": context
        }