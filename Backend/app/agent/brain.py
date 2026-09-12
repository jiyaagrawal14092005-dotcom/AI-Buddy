import os

from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session

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
from app.tools.application_launcher import ApplicationLauncher

from app.security.security_manager import SecurityManager


load_dotenv()


class AIBrain:

    def __init__(self):

        self.intent_detector = IntentDetector()

        self.planner = Planner()

        self.reasoning_engine = ReasoningEngine()

        self.context_manager = ContextManager()

        self.security_manager = SecurityManager()

        self.tools = {
            "task": TaskTool(),
            "reminder": ReminderTool(),
            "timer": TimerTool(),
            "weather": WeatherTool(),
            "search": SearchTool(),
            "email": EmailTool(),
            "calendar": CalendarTool(),
            "file": FileTool(),
            "browser": BrowserTool(),
            "application_launcher": ApplicationLauncher
        }

        self.client = None

        try:

            api_key = os.getenv("GEMINI_API_KEY")

            if not api_key:

                print(
                    "Gemini client initialization failed: "
                    "GEMINI_API_KEY not found."
                )

            else:

                self.client = genai.Client(
                    api_key=api_key
                )

                print(
                    "Gemini client initialized successfully."
                )

        except Exception as error:

            print(
                "Gemini client initialization failed:"
            )

            print(repr(error))

            self.client = None

    def _execute_tool(
        self,
        tool_name: str,
        parameters: dict,
        user_id: int,
        db: Session
    ) -> dict:

        tool = self.tools.get(tool_name)

        if tool is None:

            return {
                "success": False,
                "message": (
                    f"Tool '{tool_name}' is not available."
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
                    task_name,
                    user_id,
                    db
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

                reminder_time = parameters.get(
                    "time"
                )

                try:

                    return tool.create_reminder(
                        reminder_text,
                        reminder_time
                    )

                except TypeError:

                    return tool.create_reminder(
                        reminder_text
                    )

            if tool_name == "timer":

                duration = parameters.get(
                    "duration_seconds",
                    parameters.get(
                        "duration",
                        parameters.get(
                            "minutes",
                            0
                        )
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

            if tool_name == "application_launcher":

                action = parameters.get(
                    "action",
                    "open_application"
                )

                if action == "open_application":

                    application = parameters.get(
                        "application",
                        parameters.get(
                            "app",
                            ""
                        )
                    )

                    return tool.open_application(
                        application
                    )

                if action == "open_website":

                    url = parameters.get(
                        "url",
                        ""
                    )

                    return tool.open_website(
                        url
                    )

                return {
                    "success": False,
                    "message": (
                        "Unsupported launcher action."
                    )
                }

            return tool.execute(
                parameters
            )

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Tool execution failed: {str(error)}"
                )
            }

    def _check_security_access(
        self,
        user_id: int,
        tool_name: str
    ) -> dict:

        security_user_id = f"user-{user_id}"

        tool_access = self.security_manager.check_tool_access(
            user_id=security_user_id,
            tool_name=tool_name,
            permission_granted=True,
            approval_granted=False
        )

        if not tool_access.get(
            "allowed",
            False
        ):

            return {
                "allowed": False,
                "stage": "tool_guard",
                "message": tool_access.get(
                    "message",
                    "Tool execution blocked by security."
                )
            }

        action_access = self.security_manager.check_action_access(
            user_id=security_user_id,
            action=tool_name,
            permission_granted=True,
            approval_granted=False
        )

        if not action_access.get(
            "allowed",
            False
        ):

            return {
                "allowed": False,
                "stage": "action_policy",
                "message": action_access.get(
                    "message",
                    "Action blocked by security policy."
                )
            }

        return {
            "allowed": True,
            "message": "Tool and action security checks passed."
        }

    def _generate_general_response(
        self,
        message: str
    ) -> str:

        fallback_message = (
            "I understand your request, but I am unable "
            "to generate an AI response right now."
        )

        if self.client is None:

            print(
                "Gemini response skipped: "
                "Gemini client is not available."
            )

            return fallback_message

        try:

            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=message
            )

            if response is None:

                print(
                    "Gemini response error: "
                    "No response object returned."
                )

                return fallback_message

            response_text = getattr(
                response,
                "text",
                None
            )

            if (
                isinstance(response_text, str)
                and response_text.strip()
            ):

                return response_text.strip()

            print(
                "Gemini response error: "
                "Response did not contain usable text."
            )

        except Exception as error:

            print(
                "Gemini response generation failed:"
            )

            print(repr(error))

        return fallback_message

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

        except Exception as error:

            print(
                f"Context storage failed: {error}"
            )

    def _prepare_reasoning_plan(
        self,
        plan: dict
    ) -> dict:

        if not isinstance(
            plan,
            dict
        ):

            return {}

        steps = plan.get(
            "steps",
            []
        )

        if (
            not isinstance(
                steps,
                list
            )
            or not steps
        ):

            return plan

        first_step = steps[0]

        if not isinstance(
            first_step,
            dict
        ):

            return plan

        tool = first_step.get(
            "tool"
        )

        parameters = first_step.get(
            "parameters",
            {}
        )

        if not isinstance(
            parameters,
            dict
        ):

            parameters = {}

        return {
            "tool": tool,
            "parameters": parameters
        }

    def _get_intent_name(
        self,
        intent
    ) -> str:

        if isinstance(
            intent,
            dict
        ):

            value = intent.get(
                "intent",
                "UNKNOWN"
            )

        elif isinstance(
            intent,
            str
        ):

            value = intent

        else:

            value = "UNKNOWN"

        if not isinstance(
            value,
            str
        ):

            return "UNKNOWN"

        return value.strip().upper()

    def respond(
        self,
        message: str,
        user_id: int,
        db: Session
    ) -> dict:

        if (
            not isinstance(
                message,
                str
            )
            or not message.strip()
        ):

            return {
                "success": False,
                "intent": None,
                "plan": None,
                "reasoning": None,
                "message": "Message cannot be empty.",
                "action_result": None,
                "context": []
            }

        if not isinstance(
            user_id,
            int
        ):

            return {
                "success": False,
                "intent": None,
                "plan": None,
                "reasoning": None,
                "message": "User ID must be an integer.",
                "action_result": None,
                "context": []
            }

        if user_id <= 0:

            return {
                "success": False,
                "intent": None,
                "plan": None,
                "reasoning": None,
                "message": (
                    "User ID must be greater than zero."
                ),
                "action_result": None,
                "context": []
            }

        if db is None:

            return {
                "success": False,
                "intent": None,
                "plan": None,
                "reasoning": None,
                "message": (
                    "Database session is required."
                ),
                "action_result": None,
                "context": []
            }

        message = message.strip()

        action_result = None

        try:

            intent = self.intent_detector.detect(
                message
            )

        except Exception as error:

            return {
                "success": False,
                "intent": None,
                "plan": None,
                "reasoning": None,
                "message": (
                    f"Intent detection failed: {str(error)}"
                ),
                "action_result": None,
                "context": []
            }

        intent_name = self._get_intent_name(
            intent
        )

        if intent_name == "GENERAL_QUERY":

            response_message = (
                self._generate_general_response(
                    message
                )
            )

            self._store_context(
                message,
                response_message
            )

            try:

                context = (
                    self.context_manager.get_history()
                )

            except Exception as error:

                print(
                    f"Context retrieval failed: {error}"
                )

                context = []

            return {
                "success": True,
                "intent": intent,
                "plan": None,
                "reasoning": None,
                "message": response_message,
                "action_result": None,
                "context": context
            }

        try:

            plan = self.planner.create_plan(
                intent
            )

        except Exception as error:

            return {
                "success": False,
                "intent": intent,
                "plan": None,
                "reasoning": None,
                "message": (
                    f"Planning failed: {str(error)}"
                ),
                "action_result": None,
                "context": []
            }

        if not isinstance(
            plan,
            dict
        ):

            plan = {
                "success": False,
                "message": (
                    "Planner returned an invalid plan."
                )
            }

        reasoning_plan = (
            self._prepare_reasoning_plan(
                plan
            )
        )

        try:

            reasoning = (
                self.reasoning_engine.reason(
                    intent_name,
                    reasoning_plan
                )
            )

        except Exception as error:

            return {
                "success": False,
                "intent": intent,
                "plan": plan,
                "reasoning": None,
                "message": (
                    f"Reasoning failed: {str(error)}"
                ),
                "action_result": None,
                "context": []
            }

        if not plan.get(
            "success",
            False
        ):

            response_message = plan.get(
                "message",
                "Unable to create a plan."
            )

        elif not reasoning.get(
            "success",
            False
        ):

            response_message = reasoning.get(
                "message",
                "The request cannot be executed."
            )

        elif not reasoning.get(
            "executable",
            False
        ):

            response_message = reasoning.get(
                "message",
                "The request cannot be executed."
            )

        else:

            steps = plan.get(
                "steps",
                []
            )

            if (
                not isinstance(
                    steps,
                    list
                )
                or not steps
            ):

                response_message = (
                    "No executable action was found "
                    "for this request."
                )

            else:

                first_step = steps[0]

                if not isinstance(
                    first_step,
                    dict
                ):

                    response_message = (
                        "The execution step is invalid."
                    )

                else:

                    tool_name = first_step.get(
                        "tool"
                    )

                    parameters = first_step.get(
                        "parameters",
                        {}
                    )

                    if not isinstance(
                        parameters,
                        dict
                    ):

                        parameters = {}

                    security_result = (
                        self._check_security_access(
                            user_id,
                            tool_name
                        )
                    )

                    if not security_result.get(
                        "allowed",
                        False
                    ):

                        response_message = (
                            security_result.get(
                                "message",
                                "Action blocked by security."
                            )
                        )

                        action_result = {
                            "success": False,
                            "security_blocked": True,
                            "stage": security_result.get(
                                "stage",
                                "security"
                            ),
                            "message": response_message
                        }

                    else:

                        action_result = (
                            self._execute_tool(
                                tool_name,
                                parameters,
                                user_id,
                                db
                            )
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

            context = (
                self.context_manager.get_history()
            )

        except Exception as error:

            print(
                f"Context retrieval failed: {error}"
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