from app.tools.task import TaskTool
from app.tools.reminder import ReminderTool
from app.tools.timer import TimerTool
from app.tools.weather import WeatherTool


class WorkflowExecutor:

    def __init__(self):

        self.task_tool = TaskTool()
        self.reminder_tool = ReminderTool()
        self.timer_tool = TimerTool()
        self.weather_tool = WeatherTool()

        self.available_tools = {
            "task",
            "reminder",
            "timer",
            "weather"
        }

    # ---------------------------------
    # EXECUTE ONE WORKFLOW STEP
    # ---------------------------------

    def execute_step(
        self,
        step
    ) -> dict:

        if step is None:
            return {
                "success": False,
                "message": "Workflow step is required."
            }

        # Validate step attributes
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

        # Validate tool
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

        # Validate parameters
        if parameters is None:
            parameters = {}

        if not isinstance(parameters, dict):
            return {
                "success": False,
                "message": "Tool parameters must be a dictionary."
            }

        # Start step
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
                    task_name
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