import asyncio

from app.tools.browser_tool import BrowserTool


async def main():
    browser = BrowserTool("demo-user")

    result = await browser.execute({
        "action": "open",
        "website_name": "GeeksforGeeks",
        "page_target": "Ring Topology"
    })

    print("\n===== BROWSER DISCOVERY TEST =====")
    print("Success:", result.get("success"))
    print("Action:", result.get("action"))
    print("URL:", result.get("url"))
    print("Message:", result.get("message"))
    print("Discovery:", result.get("discovery"))
    print("Full Result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())