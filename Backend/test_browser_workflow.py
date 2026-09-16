from app.workflow.executor import WorkflowExecutor
from app.database.connection import SessionLocal


class TestStep:

    def __init__(self, tool, parameters):
        self.tool = tool
        self.parameters = parameters
        self.status = "pending"
        self.result = None

    def start(self):
        self.status = "running"

    def complete(self, result):
        self.status = "completed"
        self.result = result

    def fail(self, message):
        self.status = "failed"
        self.result = {
            "success": False,
            "message": message
        }


def run_browser_step(
    executor,
    db,
    action,
    url,
    selector=None,
    value=None
):

    parameters = {
        "action": action,
        "url": url
    }

    if selector is not None:
        parameters["selector"] = selector

    if value is not None:
        parameters["value"] = value

    step = TestStep(
        tool="browser",
        parameters=parameters
    )

    result = executor.execute_step(
        step=step,
        user_id=1,
        db=db
    )

    print(f"\n=== {action.upper()} ===")
    print(result)
    print("STEP STATUS:", step.status)

    return result


print("=== BROWSER WORKFLOW EXECUTION TEST ===")

test_url = (
    "http://127.0.0.1:8080/"
    "test_browser_page.html"
)

executor = WorkflowExecutor()
db = SessionLocal()

try:

    print("\n=== OPEN PAGE ===")

    run_browser_step(
        executor,
        db,
        action="open",
        url=test_url
    )

    print("\n=== FILL INPUT ===")

    run_browser_step(
        executor,
        db,
        action="fill",
        url=test_url,
        selector="#name",
        value="AI Buddy"
    )

    print("\n=== CLICK BUTTON ===")

    run_browser_step(
        executor,
        db,
        action="click",
        url=test_url,
        selector="#submitBtn"
    )

    print("\n=== READ RESULT ===")

    read_result = run_browser_step(
        executor,
        db,
        action="read",
        url=test_url,
        selector="#result"
    )

    print("\n=== CLOSE BROWSER SESSION ===")

    close_result = executor.browser_tool.execute(
        {
            "action": "close"
        }
    )

    print(close_result)

    print("\n=== FINAL VERIFICATION ===")

    if (
        read_result.get("success") is True
        and read_result.get("browser", {}).get("content")
        == "Hello AI Buddy!"
        and close_result.get("success") is True
    ):
        print("BROWSER WORKFLOW TEST: PASS")
    else:
        print("BROWSER WORKFLOW TEST: FAIL")

finally:

    db.close()