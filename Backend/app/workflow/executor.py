from sqlalchemy.orm import Session

from app.tools.task import TaskTool
from app.tools.reminder import ReminderTool
from app.tools.timer import TimerTool
from app.tools.weather import WeatherTool
from app.tools.browser_tool import BrowserTool


class WorkflowExecutor:

    def __init__(self):

        self.task_tool = TaskTool()
        self.reminder_tool = ReminderTool()
        self.timer_tool = TimerTool()
        self.weather_tool = WeatherTool()
        self.browser_tool = BrowserTool()

        self.available_tools = {
            "task",
            "reminder",
            "timer",
            "weather",
            "browser"
        }

    # ---------------------------------
    # EXECUTE ONE WORKFLOW STEP
    # ---------------------------------

    async def execute_step(
        self,
        step,
        user_id: int,
        db: Session
    ) -> dict:

        if step is None:
            return {
                "success": False,
                "message": "Workflow step is required."
            }

        # ---------------------------------
        # VALIDATE USER ID
        # ---------------------------------

        if not isinstance(user_id, int):
            return {
                "success": False,
                "message": "User ID must be an integer."
            }

        if user_id <= 0:
            return {
                "success": False,
                "message": "User ID must be greater than zero."
            }

        # ---------------------------------
        # VALIDATE DATABASE SESSION
        # ---------------------------------

        if db is None:
            return {
                "success": False,
                "message": "Database session is required."
            }

        # ---------------------------------
        # VALIDATE STEP ATTRIBUTES
        # ---------------------------------

        if not hasattr(step, "tool"):
            return {
                "success": False,
                "message": "Workflow step has no tool."
            }

        if not hasattr(step, "parameters"):
            return {
                "success": False,
                "message": "Workflow step has no parameters."
            }

        tool = step.tool
        parameters = step.parameters

        # ---------------------------------
        # VALIDATE TOOL
        # ---------------------------------

        if not isinstance(tool, str):
            return {
                "success": False,
                "message": "Tool name must be text."
            }

        tool = tool.strip().lower()

        if not tool:
            return {
                "success": False,
                "message": "Tool name cannot be empty."
            }

        if tool not in self.available_tools:
            return {
                "success": False,
                "message": (
                    f"Tool '{tool}' "
                    "is not currently available."
                )
            }

        # ---------------------------------
        # VALIDATE PARAMETERS
        # ---------------------------------

        if parameters is None:
            parameters = {}

        if not isinstance(parameters, dict):
            return {
                "success": False,
                "message": "Tool parameters must be a dictionary."
            }

        parameters = dict(parameters)

        # ---------------------------------
        # START STEP
        # ---------------------------------

        try:

            step.start()

        except Exception as error:

            return {
                "success": False,
                "message": (
                    "Unable to start workflow step."
                ),
                "error": str(error)
            }

        try:

            # -----------------------------
            # TASK
            # -----------------------------

            if tool == "task":

                task_name = parameters.get(
                    "task_name"
                )

                result = self.task_tool.create_task(
                    task_name,
                    user_id,
                    db
                )

            # -----------------------------
            # REMINDER
            # -----------------------------

            elif tool == "reminder":

                reminder = parameters.get(
                    "reminder",
                    ""
                )

                time = parameters.get(
                    "time",
                    ""
                )

                result = self.reminder_tool.create_reminder(
                    reminder,
                    time
                )

            # -----------------------------
            # TIMER
            # -----------------------------

            elif tool == "timer":

                duration_seconds = parameters.get(
                    "duration_seconds",
                    0
                )

                result = self.timer_tool.set_timer(
                    duration_seconds
                )

            # -----------------------------
            # WEATHER
            # -----------------------------

            elif tool == "weather":

                city = parameters.get(
                    "city",
                    ""
                )

                result = self.weather_tool.get_weather(
                    city
                )

            # -----------------------------
            # BROWSER
            # -----------------------------

            elif tool == "browser":

                # ---------------------------------
                # SET USER-SPECIFIC BROWSER CONTEXT
                # ---------------------------------

                try:

                    self.browser_tool.set_user_id(
                        user_id
                    )

                except Exception as error:

                    return {
                        "success": False,
                        "message": (
                            "Unable to initialize "
                            "user browser session."
                        ),
                        "error": str(error)
                    }

                # ---------------------------------
                # PASS USER ID TO BROWSER PARAMETERS
                # ---------------------------------

                browser_parameters = dict(
                    parameters
                )

                browser_parameters["user_id"] = user_id

                result = await self.browser_tool.execute(
                    browser_parameters
                )

            # -----------------------------
            # UNKNOWN TOOL
            # -----------------------------

            else:

                result = {
                    "success": False,
                    "message": (
                        f"Tool '{tool}' "
                        "is not currently available."
                    )
                }

            # ---------------------------------
            # VALIDATE RESULT
            # ---------------------------------

            if not isinstance(result, dict):

                step.fail(
                    "Tool returned an invalid result."
                )

                return {
                    "success": False,
                    "message": (
                        "Tool returned an invalid result."
                    )
                }

            # ---------------------------------
            # UPDATE STEP STATUS
            # ---------------------------------

            if result.get("success") is True:

                step.complete(
                    result
                )

            else:

                step.fail(
                    result.get(
                        "message",
                        "Tool execution failed."
                    )
                )

            return result

        except Exception as error:

            error_message = str(error)

            try:

                step.fail(
                    error_message
                )

            except Exception:
                pass

            return {
                "success": False,
                "message": (
                    "Workflow step execution failed."
                ),
                "error": error_message
            }