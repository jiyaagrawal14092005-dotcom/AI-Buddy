from app.tools.browser_tool import BrowserTool


browser_tool = BrowserTool()


print("=== BROWSER TOOL INFO ===")

print(
    browser_tool.get_info()
)


print("\n=== OPEN WEBSITE ===")

print(
    browser_tool.execute({
        "action": "open",
        "url": "https://www.google.com"
    })
)


print("\n=== NAVIGATE WEBSITE ===")

print(
    browser_tool.execute({
        "action": "navigate",
        "url": "https://www.github.com"
    })
)


print("\n=== INVALID URL ===")

print(
    browser_tool.execute({
        "action": "open",
        "url": "invalid-url"
    })
)


print("\n=== INVALID ACTION ===")

print(
    browser_tool.execute({
        "action": "delete",
        "url": "https://www.google.com"
    })
)


print("\n=== BROWSER AVAILABILITY ===")

print(
    browser_tool.is_available()
)