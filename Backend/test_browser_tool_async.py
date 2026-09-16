import asyncio

from app.tools.browser_tool import BrowserTool


async def test():
    browser = BrowserTool(
        user_id=1
    )

    result = await browser.execute(
        {
            "action": "open",
            "url": "http://127.0.0.1:5500/test_form.html"
        }
    )

    print(result)

    await BrowserTool.close_user_session(
        1
    )


if __name__ == "__main__":
    asyncio.run(test())