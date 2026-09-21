import asyncio

from app.tools.browser_tool import BrowserTool


browser_tool = BrowserTool()


async def main():
    user_id = 1
    browser_tool.set_user_id(user_id)

    print("=== BROWSER DOWNLOAD TEST ===")

    print("\n=== OPEN TEST WEBSITE ===")
    result = await browser_tool.execute({
        "action": "open",
        "url": "http://127.0.0.1:8765"
    })
    print(result)

    print("\n=== DOWNLOAD FILE ===")
    result = await browser_tool.execute({
        "action": "download",
        "url": "http://127.0.0.1:8765",
        "selector": "#download-link"
    })
    print(result)

    print("\n=== CLOSE BROWSER ===")
    result = await browser_tool.close_user_session(user_id)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())