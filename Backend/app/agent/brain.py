import os
from datetime import datetime, timedelta

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
from app.security.approval import approval_manager

from app.workflow.engine import WorkflowEngine


load_dotenv()


class AIBrain:

    def __init__(self):

        self.intent_detector = IntentDetector()

        self.planner = Planner()

        self.reasoning_engine = ReasoningEngine()

        self.context_manager = ContextManager()

        self.security_manager = SecurityManager()

        self.workflow_engine = WorkflowEngine()

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

            api_key = os.getenv(
                "GEMINI_API_KEY"
            )

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

            print(
                repr(error)
            )

            self.client = None

    # =================================
    # REMINDER TIME NORMALIZATION
    # =================================

    def _normalize_reminder_time(
        self,
        reminder_time
    ):

        if reminder_time is None:
            return None

        if not isinstance(
            reminder_time,
            str
        ):

            return reminder_time

        reminder_time = reminder_time.strip()

        if not reminder_time:
            return reminder_time

        try:

            datetime.fromisoformat(
                reminder_time
            )

            return reminder_time

        except ValueError:

            pass

        normalized = (
            reminder_time
            .upper()
            .replace(".", "")
            .strip()
        )

        current = datetime.now()

        formats = [
            "%I %p",
            "%I:%M %p",
            "%I%p",
            "%I:%M%p",
            "%H:%M",
            "%H",
        ]

        parsed_time = None

        for time_format in formats:

            try:

                parsed_time = datetime.strptime(
                    normalized,
                    time_format
                )

                break

            except ValueError:

                continue

        if parsed_time is None:
            return reminder_time

        target = current.replace(
            hour=parsed_time.hour,
            minute=parsed_time.minute,
            second=0,
            microsecond=0
        )

        if target <= current:

            target += timedelta(
                days=1
            )

        return target.isoformat(
            timespec="seconds"
        )

    # =================================
    # SECURITY EVENT HELPER
    # =================================

    def _record_security_event(
        self,
        user_id: int,
        event_type: str,
        action: str,
        success: bool,
        details: dict | None = None
    ) -> None:

        security_user_id = f"user-{user_id}"

        event_details = {
            "user_id": security_user_id,
            "event_type": event_type,
            "action": action,
            "success": success,
            "details": details or {}
        }

        try:

            self.security_manager._record_security_event(
                event_type=event_type,
                user_id=security_user_id,
                action=action,
                success=success,
                details=event_details
            )

        except TypeError:

            try:

                self.security_manager._record_security_event(
                    event_type,
                    security_user_id,
                    action,
                    success,
                    event_details
                )

            except Exception as error:

                print(
                    f"Security event recording failed: {error}"
                )

        except Exception as error:

            print(
                f"Security event recording failed: {error}"
            )

    # =================================
    # AUDIT LOG HELPER
    # =================================

    def _record_audit(
        self,
        user_id: int,
        action: str,
        success: bool,
        details: dict | None = None
    ) -> None:

        try:

            result = self.security_manager.record_audit_log(
                user_id=f"user-{user_id}",
                action=action,
                success=success,
                details=details or {}
            )

            if isinstance(result, dict):

                if not result.get(
                    "success",
                    True
                ):

                    print(
                        "Audit log recording failed:"
                    )

                    print(
                        result.get(
                            "message",
                            "Unknown audit error."
                        )
                    )

        except TypeError:

            try:

                result = self.security_manager.record_audit_log(
                    user_id=f"user-{user_id}",
                    action=action,
                    details={
                        "success": success,
                        **(details or {})
                    }
                )

                if isinstance(result, dict):

                    if not result.get(
                        "success",
                        True
                    ):

                        print(
                            "Audit log recording failed:"
                        )

            except Exception as error:

                print(
                    f"Audit log recording failed: {error}"
                )

        except Exception as error:

            print(
                f"Audit log recording failed: {error}"
            )

    # =================================
    # DIRECT TOOL EXECUTION
    # =================================

    def _execute_tool(
        self,
        tool_name: str,
        parameters: dict,
        user_id: int,
        db: Session
    ) -> dict:

        tool = self.tools.get(
            tool_name
        )

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

                reminder_time = (
                    self._normalize_reminder_time(
                        reminder_time
                    )
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

    # =================================
    # APPROVAL HELPERS
    # =================================

    def _create_approval_request(
        self,
        user_id: int,
        tool_name: str,
        action: str | None,
        parameters: dict
    ) -> dict:

        username = f"user-{user_id}"

        approval_action = tool_name

        if (
            tool_name == "browser"
            and action
        ):

            approval_action = (
                f"browser.{action}"
            )

        details = {
            "tool": tool_name,
            "action": action,
            "parameters": parameters
        }

        try:

            result = approval_manager.create_request(
                username=username,
                action=approval_action,
                details=details
            )

            if not isinstance(
                result,
                dict
            ):

                return {
                    "success": False,
                    "message": (
                        "Approval manager returned "
                        "an invalid response."
                    )
                }

            return result

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Approval request creation failed: {str(error)}"
                )
            }

    def _get_approved_request(
        self,
        user_id: int,
        approval_id: str,
        tool_name: str,
        action: str | None
    ) -> dict:

        if not approval_id:

            return {
                "success": False,
                "approved": False,
                "message": "Approval ID is required."
            }

        username = f"user-{user_id}"

        approval_action = tool_name

        if (
            tool_name == "browser"
            and action
        ):

            approval_action = (
                f"browser.{action}"
            )

        try:

            result = approval_manager.get_request(
                approval_id
            )

            if not result.get(
                "success",
                False
            ):

                return {
                    "success": False,
                    "approved": False,
                    "message": result.get(
                        "message",
                        "Approval request not found."
                    )
                }

            request = result.get(
                "request"
            )

            if not isinstance(
                request,
                dict
            ):

                return {
                    "success": False,
                    "approved": False,
                    "message": (
                        "Invalid approval request."
                    )
                }

            if request.get(
                "username"
            ) != username:

                return {
                    "success": False,
                    "approved": False,
                    "message": (
                        "Approval request does not "
                        "belong to this user."
                    )
                }

            if request.get(
                "action"
            ) != approval_action:

                return {
                    "success": False,
                    "approved": False,
                    "message": (
                        "Approval request does not "
                        "match this action."
                    )
                }

            if request.get(
                "status"
            ) != "APPROVED":

                return {
                    "success": False,
                    "approved": False,
                    "message": (
                        "Approval has not been granted "
                        "for this action."
                    )
                }

            return {
                "success": True,
                "approved": True,
                "approval_id": approval_id,
                "request": request,
                "message": (
                    "Approved request verified."
                )
            }

        except Exception as error:

            return {
                "success": False,
                "approved": False,
                "message": (
                    f"Approval verification failed: {str(error)}"
                )
            }

    # =================================
    # SECURITY ACCESS CHECK
    # =================================

    def _check_security_access(
        self,
        user_id: int,
        tool_name: str,
        action: str | None = None,
        approval_granted: bool = False
    ) -> dict:

        security_user_id = (
            f"user-{user_id}"
        )

        # ---------------------------------
        # TOOL PERMISSION
        # ---------------------------------

        permission_granted = False

        try:

            permission_result = (
                self.security_manager.check_permission(
                    user_id=security_user_id,
                    permission=tool_name
                )
            )

            if isinstance(
                permission_result,
                dict
            ):

                permission_granted = (
                    permission_result.get(
                        "allowed",
                        permission_result.get(
                            "granted",
                            False
                        )
                    )
                )

            else:

                permission_granted = bool(
                    permission_result
                )

        except Exception:

            permission_granted = False

        # ---------------------------------
        # TOOL GUARD
        # ---------------------------------

        tool_access = (
            self.security_manager.check_tool_access(
                user_id=security_user_id,
                tool_name=tool_name,
                permission_granted=permission_granted,
                approval_granted=approval_granted,
                action=action
            )
        )

        if not tool_access.get(
            "allowed",
            False
        ):

            return {
                "allowed": False,
                "stage": "tool_guard",
                "requires_approval": tool_access.get(
                    "requires_approval",
                    False
                ),
                "permission_granted": permission_granted,
                "message": tool_access.get(
                    "message",
                    "Tool execution blocked by security."
                )
            }

        # ---------------------------------
        # ACTION POLICY
        # ---------------------------------

        policy_action = tool_name

        if (
            tool_name == "browser"
            and action
        ):

            policy_action = (
                f"browser.{action}"
            )

        action_access = (
            self.security_manager.check_action_access(
                user_id=security_user_id,
                action=policy_action,
                permission_granted=permission_granted,
                approval_granted=approval_granted
            )
        )

        if not action_access.get(
            "allowed",
            False
        ):

            return {
                "allowed": False,
                "stage": "action_policy",
                "requires_approval": action_access.get(
                    "requires_approval",
                    False
                ),
                "permission_granted": permission_granted,
                "risk": action_access.get(
                    "risk",
                    "unknown"
                ),
                "message": action_access.get(
                    "message",
                    "Action blocked by security policy."
                )
            }

        return {
            "allowed": True,
            "tool": tool_name,
            "action": action,
            "policy_action": policy_action,
            "permission_granted": permission_granted,
            "risk": action_access.get(
                "risk",
                "unknown"
            ),
            "message": (
                "Tool and action security checks passed."
            )
        }

    # =================================
    # WORKFLOW EXECUTION
    # =================================

    async def _execute_workflow(
        self,
        plan: dict,
        user_id: int,
        db: Session
    ) -> dict:

        try:

            workflow_result = (
                await self.workflow_engine.create_workflow(
                    plan=plan,
                    user_id=user_id,
                    db=db
                )
            )

            if not isinstance(
                workflow_result,
                dict
            ):

                return {
                    "success": False,
                    "message": (
                        "Workflow engine returned "
                        "an invalid result."
                    )
                }

            return workflow_result

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Workflow execution failed: {str(error)}"
                )
            }

    # =================================
    # GENERAL AI RESPONSE
    # =================================

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

            response = (
                self.client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=message
                )
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
                isinstance(
                    response_text,
                    str
                )
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

            print(
                repr(error)
            )

        return fallback_message

    # =================================
    # ACTION MESSAGE
    # =================================

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

    # =================================
    # CONTEXT STORAGE
    # =================================

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

    # =================================
    # PREPARE REASONING PLAN
    # =================================

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

    # =================================
    # INTENT NAME
    # =================================

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

    # =================================
    # MAIN RESPONSE
    # =================================

    async def respond(
        self,
        message: str,
        user_id: int,
        db: Session,
        approval_id: str | None = None
    ) -> dict:

        # =================================
        # BASIC VALIDATION
        # =================================

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
                "approval_required": False,
                "approval_id": None,
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
                "approval_required": False,
                "approval_id": None,
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
                "approval_required": False,
                "approval_id": None,
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
                "approval_required": False,
                "approval_id": None,
                "context": []
            }

        message = message.strip()

        action_result = None

        approval_required = False
        current_approval_id = None

        security_user_id = (
            f"user-{user_id}"
        )

        # =================================
        # SECURITY — REQUEST VALIDATION
        # =================================

        try:

            security_validation = (
                self.security_manager.validate_request(
                    user_id=security_user_id,
                    message=message
                )
            )

            if not security_validation.get(
                "success",
                False
            ):

                security_message = (
                    security_validation.get(
                        "message",
                        "Request blocked by security."
                    )
                )

                self._record_security_event(
                    user_id=user_id,
                    event_type="request_blocked",
                    action="request_validation",
                    success=False,
                    details={
                        "message": security_message
                    }
                )

                self._record_audit(
                    user_id=user_id,
                    action="request.validation",
                    success=False,
                    details={
                        "stage": "request_validation",
                        "message": security_message
                    }
                )

                return {
                    "success": False,
                    "intent": None,
                    "plan": None,
                    "reasoning": None,
                    "message": security_message,
                    "action_result": {
                        "success": False,
                        "security_blocked": True,
                        "stage": "request_validation",
                        "message": security_message
                    },
                    "approval_required": False,
                    "approval_id": None,
                    "context": []
                }

        except Exception as error:

            self._record_security_event(
                user_id=user_id,
                event_type="security_failure",
                action="request_validation",
                success=False,
                details={
                    "error": str(error)
                }
            )

            self._record_audit(
                user_id=user_id,
                action="request.validation",
                success=False,
                details={
                    "stage": "security_validation",
                    "error": str(error)
                }
            )

            return {
                "success": False,
                "intent": None,
                "plan": None,
                "reasoning": None,
                "message": (
                    "Security validation failed. "
                    "Request was blocked."
                ),
                "action_result": {
                    "success": False,
                    "security_blocked": True,
                    "stage": "security_validation",
                    "message": (
                        "Security validation failed."
                    )
                },
                "approval_required": False,
                "approval_id": None,
                "context": []
            }

        # =================================
        # INTENT DETECTION
        # =================================

        try:

            intent = self.intent_detector.detect(
                message
            )

        except Exception as error:

            self._record_security_event(
                user_id=user_id,
                event_type="intent_detection_failed",
                action="intent.detect",
                success=False,
                details={
                    "error": str(error)
                }
            )

            return {
                "success": False,
                "intent": None,
                "plan": None,
                "reasoning": None,
                "message": (
                    f"Intent detection failed: {str(error)}"
                ),
                "action_result": None,
                "approval_required": False,
                "approval_id": None,
                "context": []
            }

        intent_name = self._get_intent_name(
            intent
        )

        # =================================
        # GENERAL QUERY
        # =================================

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

            self._record_audit(
                user_id=user_id,
                action="general.query",
                success=True,
                details={
                    "intent": intent_name
                }
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
                "approval_required": False,
                "approval_id": None,
                "context": context
            }

        # =================================
        # PLANNING
        # =================================

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
                "approval_required": False,
                "approval_id": None,
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

        # =================================
        # REASONING
        # =================================

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
                "approval_required": False,
                "approval_id": None,
                "context": []
            }

        # =================================
        # PLAN / REASONING VALIDATION
        # =================================

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

                    # =================================
                    # BROWSER ACTION
                    # =================================

                    browser_action = None

                    if tool_name == "browser":

                        browser_action = parameters.get(
                            "action"
                        )

                        if isinstance(
                            browser_action,
                            str
                        ):

                            browser_action = (
                                browser_action
                                .strip()
                                .lower()
                            )

                    # =================================
                    # APPROVAL VERIFICATION
                    # =================================

                    approval_granted = False

                    if approval_id:

                        approval_check = (
                            self._get_approved_request(
                                user_id=user_id,
                                approval_id=approval_id,
                                tool_name=tool_name,
                                action=browser_action
                            )
                        )

                        if approval_check.get(
                            "approved",
                            False
                        ):

                            approval_granted = True

                            current_approval_id = (
                                approval_id
                            )

                    # =================================
                    # SECURITY CHECK
                    # =================================

                    security_result = (
                        self._check_security_access(
                            user_id=user_id,
                            tool_name=tool_name,
                            action=browser_action,
                            approval_granted=approval_granted
                        )
                    )

                    if not security_result.get(
                        "allowed",
                        False
                    ):

                        # =================================
                        # APPROVAL REQUIRED
                        # =================================

                        if security_result.get(
                            "requires_approval",
                            False
                        ):

                            approval_request = (
                                self._create_approval_request(
                                    user_id=user_id,
                                    tool_name=tool_name,
                                    action=browser_action,
                                    parameters=parameters
                                )
                            )

                            if approval_request.get(
                                "success",
                                False
                            ):

                                approval_required = True

                                current_approval_id = (
                                    approval_request.get(
                                        "approval_id"
                                    )
                                )

                                response_message = (
                                    "User approval is required "
                                    "before this action can be executed."
                                )

                                action_result = {
                                    "success": False,
                                    "security_blocked": True,
                                    "requires_approval": True,
                                    "approval_required": True,
                                    "approval_id": current_approval_id,
                                    "stage": security_result.get(
                                        "stage",
                                        "security"
                                    ),
                                    "risk": security_result.get(
                                        "risk",
                                        "unknown"
                                    ),
                                    "message": response_message
                                }

                                self._record_security_event(
                                    user_id=user_id,
                                    event_type="approval_required",
                                    action=(
                                        f"{tool_name}"
                                        + (
                                            f".{browser_action}"
                                            if browser_action
                                            else ""
                                        )
                                    ),
                                    success=True,
                                    details={
                                        "approval_id": current_approval_id,
                                        "risk": security_result.get(
                                            "risk",
                                            "unknown"
                                        )
                                    }
                                )

                            else:

                                response_message = (
                                    approval_request.get(
                                        "message",
                                        "Unable to create approval request."
                                    )
                                )

                                action_result = {
                                    "success": False,
                                    "security_blocked": True,
                                    "requires_approval": True,
                                    "approval_required": True,
                                    "stage": "approval",
                                    "message": response_message
                                }

                        else:

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
                                "permission_granted": security_result.get(
                                    "permission_granted",
                                    False
                                ),
                                "message": response_message
                            }

                            self._record_security_event(
                                user_id=user_id,
                                event_type="execution_blocked",
                                action=(
                                    f"{tool_name}"
                                    + (
                                        f".{browser_action}"
                                        if browser_action
                                        else ""
                                    )
                                ),
                                success=False,
                                details={
                                    "stage": security_result.get(
                                        "stage",
                                        "security"
                                    ),
                                    "message": response_message
                                }
                            )

                    else:

                        # =================================
                        # BROWSER → WORKFLOW
                        # =================================

                        if tool_name == "browser":

                            workflow_result = (
                                await self._execute_workflow(
                                    plan=plan,
                                    user_id=user_id,
                                    db=db
                                )
                            )

                            action_result = (
                                workflow_result
                            )

                            if workflow_result.get(
                                "success",
                                False
                            ):

                                response_message = (
                                    "Browser workflow "
                                    "executed successfully."
                                )

                                # =================================
                                # CONSUME APPROVAL
                                # =================================

                                if current_approval_id:

                                    try:

                                        approval_manager.consume(
                                            current_approval_id
                                        )

                                    except Exception as error:

                                        print(
                                            "Approval consumption failed:"
                                        )

                                        print(
                                            repr(error)
                                        )

                            else:

                                response_message = (
                                    workflow_result.get(
                                        "message",
                                        "Browser workflow "
                                        "execution failed."
                                    )
                                )

                        # =================================
                        # OTHER TOOLS
                        # =================================

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

                    # =================================
                    # EXECUTION AUDIT
                    # =================================

                    execution_success = bool(
                        action_result
                        and action_result.get(
                            "success",
                            False
                        )
                    )

                    action_name = tool_name

                    if (
                        tool_name == "browser"
                        and browser_action
                    ):

                        action_name = (
                            f"browser.{browser_action}"
                        )

                    self._record_audit(
                        user_id=user_id,
                        action=action_name,
                        success=execution_success,
                        details={
                            "intent": intent_name,
                            "parameters": parameters,
                            "security": security_result
                        }
                    )

                    self._record_security_event(
                        user_id=user_id,
                        event_type=(
                            "execution_success"
                            if execution_success
                            else "execution_failed"
                        ),
                        action=action_name,
                        success=execution_success,
                        details={
                            "intent": intent_name,
                            "security": security_result
                        }
                    )

        # =================================
        # STORE CONTEXT
        # =================================

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

        # =================================
        # FINAL RESPONSE
        # =================================

        return {
            "success": True,
            "intent": intent,
            "plan": plan,
            "reasoning": reasoning,
            "message": response_message,
            "action_result": action_result,
            "approval_required": approval_required,
            "approval_id": current_approval_id,
            "context": context
        }