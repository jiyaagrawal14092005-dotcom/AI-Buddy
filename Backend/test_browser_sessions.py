import asyncio

from app.tools.browser_session import BrowserSession


async def test():
    session_1 = BrowserSession()
    session_2 = BrowserSession()

    page_1 = await session_1.start()
    page_2 = await session_2.start()

    print("S1 PAGE:", page_1)
    print("S2 PAGE:", page_2)

    print("S1 ACTIVE:", session_1.is_active())
    print("S2 ACTIVE:", session_2.is_active())

    print("SAME PAGE:", page_1 is page_2)

    await session_1.close()
    await session_2.close()


if __name__ == "__main__":
    asyncio.run(test())