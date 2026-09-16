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
        "url": "https://example.com"
    })
)


print("\n=== NAVIGATE WEBSITE ===")

print(
    browser_tool.execute({
        "action": "navigate",
        "url": "https://example.com"
    })
)


print("\n=== READ PAGE ===")

print(
    browser_tool.execute({
        "action": "read",
        "url": "https://example.com"
    })
)


print("\n=== CLICK ELEMENT ===")

print(
    browser_tool.execute({
        "action": "click",
        "url": "https://example.com",
        "selector": "a"
    })
)


print("\n=== FILL INPUT ===")

print(
    browser_tool.execute({
        "action": "fill",
        "url": "https://example.com",
        "selector": "input",
        "value": "AI Buddy"
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
        "url": "https://example.com"
    })
)


print("\n=== MISSING SELECTOR ===")

print(
    browser_tool.execute({
        "action": "click",
        "url": "https://example.com"
    })
)


print("\n=== BROWSER AVAILABILITY ===")

print(
    browser_tool.is_available()
)