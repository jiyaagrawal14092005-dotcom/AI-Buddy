from playwright.async_api import (
    Browser,
    Page,
    Playwright,
    async_playwright,
)


class BrowserSession:

    def __init__(self):
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.page: Page | None = None

    # =================================
    # START SESSION
    # =================================

    async def start(self) -> Page:

        # Reuse the existing active page.
        if self.page is not None:

            try:
                if not self.page.is_closed():
                    return self.page

            except Exception:
                pass

        # Clean up stale objects before creating
        # a new browser session.
        await self.close()

        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(
            headless=True
        )

        self.page = await self.browser.new_page()

        return self.page

    # =================================
    # GET CURRENT PAGE
    # =================================

    def get_page(self) -> Page:

        if self.page is None:
            raise RuntimeError(
                "Browser session has not been started."
            )

        try:
            if self.page.is_closed():
                raise RuntimeError(
                    "Browser page has already been closed."
                )

        except Exception as exc:

            if isinstance(exc, RuntimeError):
                raise

            raise RuntimeError(
                "Browser page is no longer available."
            )

        return self.page

    # =================================
    # OPEN URL
    # =================================

    async def open(
        self,
        url: str
    ) -> dict:

        page = self.get_page()

        response = await page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000
        )

        return {
            "url": page.url,
            "title": await page.title(),
            "status_code": (
                response.status
                if response is not None
                else None
            )
        }

    # =================================
    # CLOSE SESSION
    # =================================

    async def close(self) -> None:

        if self.browser is not None:

            try:
                await self.browser.close()

            except Exception:
                pass

        if self.playwright is not None:

            try:
                await self.playwright.stop()

            except Exception:
                pass

        self.page = None
        self.browser = None
        self.playwright = None

    # =================================
    # SESSION STATUS
    # =================================

    def is_active(self) -> bool:

        if (
            self.playwright is None
            or self.browser is None
            or self.page is None
        ):
            return False

        try:
            return not self.page.is_closed()

        except Exception:
            return False