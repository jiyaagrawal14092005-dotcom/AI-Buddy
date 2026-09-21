import asyncio

from app.tools.browser_tool import BrowserTool


browser_tool = BrowserTool()


async def main():

    # Test user ID
    user_id = 1

    # Set the user for the browser session
    browser_tool.set_user_id(user_id)

    print("=== BROWSER TOOL INFO ===")

    print(
        browser_tool.get_info()
    )


    print("\n=== OPEN WEBSITE ===")

    print(
        await browser_tool.execute({
            "action": "open",
            "url": "https://example.com"
        })
    )


    print("\n=== NAVIGATE WEBSITE ===")

    print(
        await browser_tool.execute({
            "action": "navigate",
            "url": "https://example.com"
        })
    )


    print("\n=== READ PAGE ===")

    print(
        await browser_tool.execute({
            "action": "read",
            "url": "https://example.com"
        })
    )


    print("\n=== CLICK ELEMENT ===")

    print(
        await browser_tool.execute({
            "action": "click",
            "url": "https://example.com",
            "selector": "a"
        })
    )


    print("\n=== FILL INPUT ===")

    print(
        await browser_tool.execute({
            "action": "fill",
            "url": "https://example.com",
            "selector": "input",
            "value": "AI Buddy"
        })
    )


    print("\n=== INVALID URL ===")

    print(
        await browser_tool.execute({
            "action": "open",
            "url": "invalid-url"
        })
    )


    print("\n=== INVALID ACTION ===")

    print(
        await browser_tool.execute({
            "action": "delete",
            "url": "https://example.com"
        })
    )


    print("\n=== MISSING SELECTOR ===")

    print(
        await browser_tool.execute({
            "action": "click",
            "url": "https://example.com"
        })
    )


    print("\n=== BROWSER AVAILABILITY ===")

    print(
        browser_tool.is_available()
    )


    print("\n=== CLOSING BROWSER SESSION ===")

    print(
        await browser_tool.close_user_session(user_id)
    )


if __name__ == "__main__":
    asyncio.run(main())