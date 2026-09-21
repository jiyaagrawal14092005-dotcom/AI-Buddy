import asyncio
from playwright.async_api import async_playwright


async def main():
    print("Starting Playwright...")

    playwright = await async_playwright().start()

    print("PLAYWRIGHT STARTED SUCCESSFULLY")

    await playwright.stop()

    print("Playwright stopped successfully")


if __name__ == "__main__":
    asyncio.run(main())