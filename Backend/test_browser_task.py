import asyncio

from app.tools.browser_tool import BrowserTool


browser_tool = BrowserTool()


async def main():
    user_id = 1
    browser_tool.set_user_id(user_id)

    print("=== STEP 1: OPEN NOTES PORTAL ===")

    result = await browser_tool.execute({
        "action": "open",
        "url": "http://127.0.0.1:8765"
    })

    print(result)

    print("\n=== STEP 2: READ PAGE ===")

    result = await browser_tool.execute({
        "action": "read",
        "use_current_page": True
    })

    print(result)

    print("\n=== STEP 3: DOWNLOAD AI BUDDY NOTES ===")

    result = await browser_tool.execute({
        "action": "download",
        "selector": "#ai-buddy-notes",
        "use_current_page": True
    })

    print(result)

    print("\n=== STEP 4: CLOSE BROWSER ===")

    result = await browser_tool.close_user_session(user_id)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())