import asyncio

from app.tools.browser_tool import BrowserTool


async def main():
    browser = BrowserTool(user_id="test_user")

    print("\n========== OPEN TEST ==========")

    open_result = await browser.execute(
        {
            "action": "open",
            "url": "https://www.w3schools.com/html/html_forms.asp",
        }
    )

    print(open_result)

    print("\n========== FILL TEST ==========")

    fill_result = await browser.execute(
        {
            "action": "fill",
            "selector": "input[name='fname']",
            "value": "Jiya",
        }
    )

    print(fill_result)

    print("\n========== READ AFTER FILL ==========")

    read_result = await browser.execute(
        {
            "action": "read",
            "selector": "body",
        }
    )

    print(read_result)

    print("\n========== CLOSE TEST ==========")

    close_result = await browser.execute(
        {
            "action": "close",
        }
    )

    print(close_result)


if __name__ == "__main__":
    asyncio.run(main())