from app.tools.browser_tool import BrowserTool


browser_tool = BrowserTool()

test_url = "http://127.0.0.1:8080/test_browser_page.html"


print("=== BROWSER SESSION TEST ===")
print("Test URL:", test_url)


print("\n=== INITIAL SESSION STATUS ===")
print(browser_tool.is_session_active())


print("\n=== OPEN PAGE ===")
open_result = browser_tool.execute(
    {
        "action": "open",
        "url": test_url,
    }
)

print(open_result)


print("\n=== SESSION STATUS AFTER OPEN ===")
print(browser_tool.is_session_active())


print("\n=== FILL INPUT ===")
fill_result = browser_tool.execute(
    {
        "action": "fill",
        "url": test_url,
        "selector": "#name",
        "value": "AI Buddy",
    }
)

print(fill_result)


print("\n=== CLICK BUTTON ===")
click_result = browser_tool.execute(
    {
        "action": "click",
        "url": test_url,
        "selector": "#submitBtn",
    }
)

print(click_result)


print("\n=== READ RESULT ===")
read_result = browser_tool.execute(
    {
        "action": "read",
        "url": test_url,
        "selector": "#result",
    }
)

print(read_result)


print("\n=== CLOSE SESSION ===")
close_result = browser_tool.execute(
    {
        "action": "close",
    }
)

print(close_result)


print("\n=== FINAL SESSION STATUS ===")
print(browser_tool.is_session_active())