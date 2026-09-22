
from urllib.parse import urlparse, urljoin
from pathlib import Path
import re
import traceback

from app.tools.base_tool import BaseTool
from app.tools.browser_session import BrowserSession
from app.browser.website_discovery import WebsiteDiscovery


class BrowserTool(BaseTool):

    # =========================================
    # PER-USER BROWSER SESSIONS
    # =========================================

    _user_sessions: dict[str, BrowserSession] = {}

    def __init__(
        self,
        user_id: int | str | None = None,
        website_discovery: WebsiteDiscovery | None = None
    ):

        super().__init__(
            name="browser",
            description=(
                "Execute safe browser actions such as opening "
                "websites, discovering websites through search, "
                "navigating to URLs, clicking elements, filling "
                "input fields, downloading files, reading page "
                "content, and managing browser sessions."
            )
        )

        self.user_id = (
            str(user_id)
            if user_id is not None
            else None
        )

        self.session: BrowserSession | None = None

        # -----------------------------------------
        # GENERIC WEBSITE DISCOVERY
        # -----------------------------------------

        self.website_discovery = (
            website_discovery
            if website_discovery is not None
            else WebsiteDiscovery()
        )

        # -----------------------------------------
        # WINDOWS DOWNLOADS FOLDER
        #
        # Files are saved to the user's normal
        # Windows Downloads folder.
        #
        # Example:
        # C:\Users\Daksh\Downloads
        # -----------------------------------------

        self.download_root = Path.home() / "Downloads"

        # Make sure the Downloads folder exists.
        self.download_root.mkdir(
            parents=True,
            exist_ok=True
        )

        if self.user_id is not None:
            self.session = (
                self._get_or_create_session(
                    self.user_id
                )
            )

    # =========================================
    # USER SESSION MANAGEMENT
    # =========================================

    @classmethod
    def _get_or_create_session(
        cls,
        user_id: str
    ) -> BrowserSession:

        if user_id not in cls._user_sessions:

            cls._user_sessions[user_id] = (
                BrowserSession()
            )

        return cls._user_sessions[user_id]

    def set_user_id(
        self,
        user_id: int | str
    ) -> None:

        if user_id is None:
            raise ValueError(
                "User ID cannot be empty."
            )

        self.user_id = str(user_id)

        self.session = (
            self._get_or_create_session(
                self.user_id
            )
        )

    def _get_session(self) -> BrowserSession:

        if not self.user_id:

            raise ValueError(
                "Browser user ID is required."
            )

        if self.session is None:

            self.session = (
                self._get_or_create_session(
                    self.user_id
                )
            )

        return self.session

    @classmethod
    async def close_user_session(
        cls,
        user_id: int | str
    ) -> dict:

        user_key = str(user_id)

        session = cls._user_sessions.get(
            user_key
        )

        if session is None:

            return {
                "success": True,
                "status": "completed",
                "user_id": user_key,
                "was_active": False,
                "message": (
                    "No browser session exists "
                    "for this user."
                )
            }

        was_active = session.is_active()

        try:

            await session.close()

        finally:

            cls._user_sessions.pop(
                user_key,
                None
            )

        return {
            "success": True,
            "status": "completed",
            "user_id": user_key,
            "was_active": was_active,
            "message": (
                "User browser session closed successfully."
            )
        }

    @classmethod
    def get_user_session_status(
        cls,
        user_id: int | str
    ) -> dict:

        user_key = str(user_id)

        session = cls._user_sessions.get(
            user_key
        )

        if session is None:

            return {
                "success": True,
                "user_id": user_key,
                "exists": False,
                "active": False
            }

        return {
            "success": True,
            "user_id": user_key,
            "exists": True,
            "active": session.is_active()
        }

    @classmethod
    def get_active_user_sessions(
        cls
    ) -> list[str]:

        active_users = []

        for user_id, session in (
            cls._user_sessions.items()
        ):

            if session.is_active():
                active_users.append(
                    user_id
                )

        return sorted(active_users)

    # =========================================
    # WEBSITE DISCOVERY
    # =========================================

    def _discover_website_url(
        self,
        website_name: str = "",
        page_target: str = ""
    ) -> dict:

        website_name = (
            website_name.strip()
            if isinstance(
                website_name,
                str
            )
            else ""
        )

        page_target = (
            page_target.strip()
            if isinstance(
                page_target,
                str
            )
            else ""
        )

        if not website_name and not page_target:

            return {
                "success": False,
                "url": None,
                "message": (
                    "Website discovery requires "
                    "website_name or page_target."
                )
            }

        try:

            result = (
                self.website_discovery.search_website(
                    website_name=website_name,
                    page_target=page_target
                )
            )

        except Exception as error:

            return {
                "success": False,
                "url": None,
                "message": (
                    "Website discovery failed."
                ),
                "error_type": type(error).__name__,
                "error": str(error)
            }

        if not isinstance(result, dict):

            return {
                "success": False,
                "url": None,
                "message": (
                    "Website discovery returned "
                    "an invalid response."
                )
            }

        discovered_url = result.get(
            "url"
        )

        if not result.get(
            "success",
            False
        ):

            return result

        if not discovered_url:

            return {
                **result,
                "success": False,
                "url": None,
                "message": (
                    "Website discovery did not "
                    "return a usable URL."
                )
            }

        return result

    # =========================================
    # URL VALIDATION
    # =========================================

    def _validate_url(
        self,
        url: str
    ) -> str:

        if not isinstance(
            url,
            str
        ):

            raise TypeError(
                "URL must be a string."
            )

        url = url.strip()

        if not url:

            raise ValueError(
                "URL cannot be empty."
            )

        parsed_url = urlparse(
            url
        )

        if parsed_url.scheme not in {
            "http",
            "https"
        }:

            raise ValueError(
                "URL must start with "
                "http:// or https://."
            )

        if not parsed_url.netloc:

            raise ValueError(
                "Invalid URL."
            )

        return url

    # =========================================
    # ACTION VALIDATION
    # =========================================

    def _validate_action(
        self,
        action: str
    ) -> str:

        if not isinstance(
            action,
            str
        ):

            raise TypeError(
                "Browser action must be a string."
            )

        action = action.strip().lower()

        allowed_actions = {
            "open",
            "navigate",
            "click",
            "fill",
            "read",
            "download",
            "close"
        }

        if action not in allowed_actions:

            raise ValueError(
                "Unsupported browser action. "
                "Use open, navigate, click, fill, "
                "read, download, or close."
            )

        return action

    # =========================================
    # SELECTOR VALIDATION
    # =========================================

    def _validate_selector(
        self,
        selector: str
    ) -> str:

        if not isinstance(
            selector,
            str
        ):

            raise TypeError(
                "Selector must be a string."
            )

        selector = selector.strip()

        if not selector:

            raise ValueError(
                "Selector cannot be empty."
            )

        return selector

    # =========================================
    # VALUE VALIDATION
    # =========================================

    def _validate_value(
        self,
        value: str
    ) -> str:

        if not isinstance(
            value,
            str
        ):

            raise TypeError(
                "Value must be a string."
            )

        return value

    # =========================================
    # PREPARE ACTION
    # =========================================

    def prepare_action(
        self,
        action: str,
        url: str | None = None,
        selector: str | None = None,
        value: str | None = None,
        use_current_page: bool = False,
        target: str | None = None
    ) -> dict:

        action = self._validate_action(
            action
        )

        prepared_action = {
            "action": action
        }

        # -----------------------------------------
        # CLOSE
        # -----------------------------------------

        if action == "close":

            return prepared_action

        # -----------------------------------------
        # OPEN / NAVIGATE
        # -----------------------------------------

        if action in {
            "open",
            "navigate"
        }:

            if url is None:

                raise ValueError(
                    f"URL is required for '{action}' "
                    "action after discovery."
                )

            url = self._validate_url(
                url
            )

            prepared_action["url"] = url

        # -----------------------------------------
        # CLICK / FILL / READ / DOWNLOAD
        # -----------------------------------------

        elif action in {
            "download",
            "click",
            "fill",
            "read"
        }:

            if (
                isinstance(
                    url,
                    str
                )
                and url.strip()
            ):

                prepared_action["url"] = (
                    self._validate_url(
                        url
                    )
                )

                prepared_action[
                    "use_current_page"
                ] = False

            else:

                prepared_action[
                    "use_current_page"
                ] = bool(
                    use_current_page
                    or url is None
                )

        # -----------------------------------------
        # CLICK / DOWNLOAD TARGET
        # -----------------------------------------

        if action in {
            "click",
            "download"
        }:

            has_selector = (
                isinstance(
                    selector,
                    str
                )
                and selector.strip()
            )

            has_target = (
                isinstance(
                    target,
                    str
                )
                and target.strip()
            )

            if not has_selector and not has_target:

                raise ValueError(
                    f"Selector or target is required "
                    f"for '{action}' action."
                )

            if has_selector:

                prepared_action[
                    "selector"
                ] = self._validate_selector(
                    selector
                )

            if has_target:

                prepared_action[
                    "target"
                ] = target.strip()

        # -----------------------------------------
        # FILL SELECTOR
        # -----------------------------------------

        if action == "fill":

            if selector is None:

                raise ValueError(
                    "Selector is required for "
                    "'fill' action."
                )

            prepared_action[
                "selector"
            ] = self._validate_selector(
                selector
            )

        # -----------------------------------------
        # FILL VALUE
        # -----------------------------------------

        if action == "fill":

            if value is None:

                raise ValueError(
                    "Value is required for "
                    "'fill' action."
                )

            prepared_action[
                "value"
            ] = self._validate_value(
                value
            )

        # -----------------------------------------
        # READ SELECTOR OPTIONAL
        # -----------------------------------------

        if (
            action == "read"
            and selector is not None
        ):

            prepared_action[
                "selector"
            ] = self._validate_selector(
                selector
            )

        return prepared_action

    # =========================================
    # GET PAGE
    # =========================================

    async def _get_page(self):

        session = self._get_session()

        if not session.is_active():

            await session.start()

        return session.get_page()

    # =========================================
    # OPEN PAGE
    # =========================================

    async def _open_page(
        self,
        url: str
    ) -> dict:

        url = self._validate_url(
            url
        )

        session = self._get_session()

        return await session.open(
            url
        )

    # =========================================
    # CLICKABLE ELEMENT RESOLUTION
    # =========================================

    async def _resolve_clickable_element(
        self,
        target: str,
        selector: str | None = None
    ):

        page = await self._get_page()

        if selector:

            selector = (
                self._validate_selector(
                    selector
                )
            )

            element = page.locator(
                selector
            )

            if await element.count() == 0:

                raise ValueError(
                    f"No element found for selector "
                    f"'{selector}'."
                )

            return element.first

        if not target:

            raise ValueError(
                "Click target or selector is required."
            )

        target = target.strip()

        if not target:

            raise ValueError(
                "Click target cannot be empty."
            )

        normalized_target = re.sub(
            r"\b(button|link|option|tab)\b",
            " ",
            target,
            flags=re.IGNORECASE
        )

        normalized_target = re.sub(
            r"\s+",
            " ",
            normalized_target
        ).strip()

        exact_text = page.get_by_text(
            normalized_target,
            exact=True
        )

        if await exact_text.count() > 0:

            return exact_text.first

        link = page.get_by_role(
            "link",
            name=re.compile(
                re.escape(normalized_target),
                re.IGNORECASE
            )
        )

        if await link.count() > 0:

            return link.first

        button = page.get_by_role(
            "button",
            name=re.compile(
                re.escape(normalized_target),
                re.IGNORECASE
            )
        )

        if await button.count() > 0:

            return button.first

        contains_text = page.get_by_text(
            re.compile(
                re.escape(normalized_target),
                re.IGNORECASE
            )
        )

        if await contains_text.count() > 0:

            return contains_text.first

        if any(
            word in target.lower()
            for word in [
                "download",
                "pdf",
                "file",
                "cheatsheet"
            ]
        ):

            candidates = page.locator(
                "a, button, [role='button']"
            )

            count = await candidates.count()

            target_words = [
                word
                for word in re.findall(
                    r"[a-z0-9]+",
                    normalized_target.lower()
                )
                if len(word) >= 3
            ]

            best_candidate = None
            best_score = -1

            for index in range(
                min(count, 150)
            ):

                candidate = candidates.nth(
                    index
                )

                try:

                    text = (
                        await candidate.inner_text(
                            timeout=2000
                        )
                    )

                    aria = (
                        await candidate.get_attribute(
                            "aria-label"
                        )
                    )

                    title = (
                        await candidate.get_attribute(
                            "title"
                        )
                    )

                    href = (
                        await candidate.get_attribute(
                            "href"
                        )
                    )

                    combined = " ".join(
                        part
                        for part in [
                            text,
                            aria,
                            title,
                            href
                        ]
                        if part
                    ).lower()

                    score = 0

                    if "download" in combined:
                        score += 50

                    if "pdf" in combined:
                        score += 30

                    if "cheatsheet" in combined:
                        score += 30

                    if "file" in combined:
                        score += 10

                    for word in target_words:

                        if word in combined:
                            score += 8

                    if (
                        await candidate.evaluate(
                            "(el) => el.tagName.toLowerCase()"
                        )
                        in {"a", "button"}
                    ):

                        score += 5

                    if score > best_score:

                        best_score = score
                        best_candidate = candidate

                except Exception:

                    continue

            if (
                best_candidate is not None
                and best_score > 0
            ):

                return best_candidate

        raise ValueError(
            f"Could not find clickable element "
            f"for target '{target}'."
        )

    # =========================================
    # CLICK ELEMENT
    # =========================================

    async def _click_element(
        self,
        selector: str | None = None,
        target: str | None = None
    ) -> dict:

        page = await self._get_page()

        element = (
            await self._resolve_clickable_element(
                target=target or "",
                selector=selector
            )
        )

        await element.wait_for(
            state="visible",
            timeout=10000
        )

        await element.click(
            timeout=10000
        )

        return {
            "selector": selector,
            "target": target,
            "url": page.url,
            "title": await page.title()
        }

    # =========================================
    # FILL INPUT
    # =========================================

    async def _fill_input(
        self,
        selector: str,
        value: str
    ) -> dict:

        selector = self._validate_selector(
            selector
        )

        value = self._validate_value(
            value
        )

        page = await self._get_page()

        element = page.locator(
            selector
        )

        await element.first.wait_for(
            state="visible",
            timeout=10000
        )

        await element.first.fill(
            value,
            timeout=10000
        )

        return {
            "selector": selector,
            "value_length": len(value),
            "url": page.url,
            "title": await page.title()
        }

    # =========================================
    # READ PAGE
    # =========================================

    async def _read_page(
        self,
        selector: str | None = None
    ) -> dict:

        page = await self._get_page()

        if selector is not None:

            selector = (
                self._validate_selector(
                    selector
                )
            )

            element = page.locator(
                selector
            )

            if await element.count() == 0:

                raise ValueError(
                    f"Element not found for "
                    f"selector '{selector}'."
                )

            content = (
                await element.first.inner_text(
                    timeout=10000
                )
            )

        else:

            content = (
                await page.locator(
                    "body"
                ).inner_text(
                    timeout=10000
                )
            )

        content = content.strip()

        return {
            "url": page.url,
            "title": await page.title(),
            "content": content
        }

    # =========================================
    # SAFE FILENAME
    # =========================================

    def _safe_filename(
        self,
        filename: str | None
    ) -> str:

        if not filename:

            filename = "download"

        filename = Path(
            filename
        ).name

        filename = re.sub(
            r'[<>:"/\\|?*\x00-\x1f]',
            "_",
            filename
        )

        filename = (
            filename
            .strip()
            .strip(".")
        )

        if not filename:

            filename = "download"

        return filename

    # =========================================
    # UNIQUE DOWNLOAD PATH
    # =========================================

    def _get_unique_download_path(
        self,
        directory: Path,
        filename: str
    ) -> Path:

        filename = self._safe_filename(
            filename
        )

        destination = (
            directory / filename
        )

        if not destination.exists():

            return destination

        stem = destination.stem
        suffix = destination.suffix

        counter = 1

        while True:

            candidate = (
                directory
                / f"{stem}_{counter}{suffix}"
            )

            if not candidate.exists():

                return candidate

            counter += 1

    # =========================================
    # VERIFY DOWNLOADED FILE
    # =========================================

    def _verify_download_file(
        self,
        path: Path
    ) -> dict:

        path = path.resolve()

        if not path.exists():

            raise FileNotFoundError(
                "Downloaded file does not exist."
            )

        if not path.is_file():

            raise RuntimeError(
                "Downloaded path is not a file."
            )

        size = path.stat().st_size

        if size <= 0:

            raise RuntimeError(
                "Downloaded file is empty."
            )

        return {
            "path": str(path),
            "filename": path.name,
            "size": size,
            "size_bytes": size,
            "verified": True
        }

    # =========================================
    # FILE URL HELPERS
    # =========================================

    def _is_file_url(
        self,
        url: str
    ) -> bool:

        if not url:

            return False

        parsed = urlparse(
            url
        )

        path = parsed.path.lower()

        file_extensions = {
            ".pdf",
            ".txt",
            ".csv",
            ".json",
            ".xml",
            ".zip",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
            ".py",
            ".java",
            ".cpp",
            ".c",
            ".js",
            ".html"
        }

        return any(
            path.endswith(extension)
            for extension in file_extensions
        )

    def _extract_filename_from_url(
        self,
        url: str
    ) -> str:

        parsed = urlparse(
            url
        )

        filename = Path(
            parsed.path
        ).name

        if not filename:

            filename = "download"

        return self._safe_filename(
            filename
        )

    # =========================================
    # EXTRACT FILE URLS FROM HTML
    # =========================================

    def _extract_file_urls_from_html(
        self,
        html: str,
        base_url: str
    ) -> list[str]:

        if not isinstance(
            html,
            str
        ):

            return []

        found_urls = []

        href_pattern = re.compile(
            r'''href=["']([^"']+)["']''',
            re.IGNORECASE
        )

        for match in href_pattern.finditer(
            html
        ):

            raw_url = match.group(
                1
            ).strip()

            if not raw_url:
                continue

            absolute_url = urljoin(
                base_url,
                raw_url
            )

            if self._is_file_url(
                absolute_url
            ):

                found_urls.append(
                    absolute_url
                )

        src_pattern = re.compile(
            r'''src=["']([^"']+)["']''',
            re.IGNORECASE
        )

        for match in src_pattern.finditer(
            html
        ):

            raw_url = match.group(
                1
            ).strip()

            if not raw_url:
                continue

            absolute_url = urljoin(
                base_url,
                raw_url
            )

            if self._is_file_url(
                absolute_url
            ):

                found_urls.append(
                    absolute_url
                )

        unique_urls = []

        seen = set()

        for url in found_urls:

            if url not in seen:

                seen.add(url)
                unique_urls.append(url)

        return unique_urls

    # =========================================
    # SCORE FILE URL
    # =========================================

    def _score_file_url(
        self,
        url: str,
        target: str | None = None
    ) -> int:

        score = 0

        lowered = url.lower()

        if target:

            target_words = re.findall(
                r"[a-z0-9]+",
                target.lower()
            )

            for word in target_words:

                if len(word) >= 3:

                    if word in lowered:
                        score += 10

        if self._is_file_url(url):
            score += 20

        if lowered.endswith(".pdf"):
            score += 15

        if "download" in lowered:
            score += 10

        if "file" in lowered:
            score += 5

        return score

    # =========================================
    # RESOLVE DOWNLOAD URL FROM PAGE
    # =========================================

    async def _resolve_download_url_from_page(
        self,
        target: str | None = None
    ) -> str | None:

        page = await self._get_page()

        candidates = []

        links = page.locator(
            "a"
        )

        count = await links.count()

        for index in range(
            min(count, 200)
        ):

            link = links.nth(
                index
            )

            try:

                href = (
                    await link.get_attribute(
                        "href"
                    )
                )

                text = (
                    await link.inner_text(
                        timeout=2000
                    )
                )

                if not href:
                    continue

                absolute_url = urljoin(
                    page.url,
                    href
                )

                score = (
                    self._score_file_url(
                        absolute_url,
                        target
                    )
                )

                combined = (
                    f"{text} {href}"
                    .lower()
                )

                if "download" in combined:
                    score += 20

                if target:

                    for word in re.findall(
                        r"[a-z0-9]+",
                        target.lower()
                    ):

                        if (
                            len(word) >= 3
                            and word in combined
                        ):

                            score += 10

                candidates.append(
                    (
                        score,
                        absolute_url
                    )
                )

            except Exception:
                continue

        try:

            html = await page.content()

            html_urls = (
                self._extract_file_urls_from_html(
                    html,
                    page.url
                )
            )

            for url in html_urls:

                score = (
                    self._score_file_url(
                        url,
                        target
                    )
                )

                candidates.append(
                    (
                        score,
                        url
                    )
                )

        except Exception:
            pass

        if not candidates:
            return None

        candidates.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return candidates[0][1]

    # =========================================
    # DOWNLOAD FILE
    # =========================================

    async def _download_file(
        self,
        selector: str | None = None,
        target: str | None = None,
        requested_url: str | None = None,
        use_current_page: bool = True
    ) -> dict:

        page = await self._get_page()

        # -----------------------------------------
        # NAVIGATE IF REQUIRED
        # -----------------------------------------

        if (
            requested_url
            and not use_current_page
            and page.url != requested_url
        ):

            await self._open_page(
                requested_url
            )

            page = (
                self._get_session().get_page()
            )

        # -----------------------------------------
        # WINDOWS DOWNLOADS DIRECTORY
        # -----------------------------------------

        download_dir = self.download_root

        download_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # -----------------------------------------
        # EXPLICIT SELECTOR / TARGET
        # -----------------------------------------

        element = None

        if selector:

            selector = (
                self._validate_selector(
                    selector
                )
            )

            element = page.locator(
                selector
            ).first

        elif target:

            element = (
                await self._resolve_clickable_element(
                    target=target
                )
            )

        # -----------------------------------------
        # NATIVE PLAYWRIGHT DOWNLOAD
        # -----------------------------------------

        if element is not None:

            try:

                await element.wait_for(
                    state="visible",
                    timeout=10000
                )

                async with page.expect_download(
                    timeout=15000
                ) as download_info:

                    await element.click(
                        timeout=10000
                    )

                download = (
                    await download_info.value
                )

                suggested_name = (
                    self._safe_filename(
                        download.suggested_filename
                    )
                )

                destination = (
                    self._get_unique_download_path(
                        download_dir,
                        suggested_name
                    )
                )

                await download.save_as(
                    str(destination)
                )

                failure = (
                    await download.failure()
                )

                if failure:

                    raise RuntimeError(
                        f"Browser download failed: "
                        f"{failure}"
                    )

                verified = (
                    self._verify_download_file(
                        destination
                    )
                )

                return {
                    "selector": selector,
                    "target": target,
                    "url": page.url,
                    "title": await page.title(),
                    "downloads_folder": str(
                        download_dir.resolve()
                    ),
                    **verified
                }

            except Exception as native_error:

                native_download_error = (
                    repr(native_error)
                )

        else:

            native_download_error = None

        # =========================================
        # GENERIC FILE URL FALLBACK
        # =========================================

        file_url = (
            await self._resolve_download_url_from_page(
                target=target
            )
        )

        if not file_url:

            raise RuntimeError(
                "Could not resolve a downloadable "
                "file from the current page."
                + (
                    f" Native download error: "
                    f"{native_download_error}"
                    if native_download_error
                    else ""
                )
            )

        # -----------------------------------------
        # OPEN FILE URL
        # -----------------------------------------

        response = await page.request.get(
            file_url,
            timeout=30000
        )

        if not response.ok:

            raise RuntimeError(
                f"File URL returned HTTP "
                f"{response.status}."
            )

        body = await response.body()

        filename = (
            self._extract_filename_from_url(
                file_url
            )
        )

        # -----------------------------------------
        # CONTENT-DISPOSITION
        # -----------------------------------------

        content_disposition = (
            response.headers.get(
                "content-disposition",
                ""
            )
        )

        filename_match = re.search(
            r'filename=["\']?([^"\';]+)',
            content_disposition,
            re.IGNORECASE
        )

        if filename_match:

            filename = (
                self._safe_filename(
                    filename_match.group(
                        1
                    )
                )
            )

        destination = (
            self._get_unique_download_path(
                download_dir,
                filename
            )
        )

        destination.write_bytes(
            body
        )

        verified = (
            self._verify_download_file(
                destination
            )
        )

        return {
            "selector": selector,
            "target": target,
            "url": page.url,
            "title": await page.title(),
            "file_url": file_url,
            "downloads_folder": str(
                download_dir.resolve()
            ),
            **verified
        }

    # =========================================
    # CLOSE CURRENT USER SESSION
    # =========================================

    async def _close_session(self) -> dict:

        if not self.user_id:

            return {
                "was_active": False
            }

        result = (
            await self.close_user_session(
                self.user_id
            )
        )

        self.session = None

        return {
            "was_active": result.get(
                "was_active",
                False
            )
        }

    # =========================================
    # EXECUTE
    # =========================================

    async def execute(
        self,
        parameters: dict | None = None
    ) -> dict:

        if parameters is None:
            parameters = {}

        if not isinstance(
            parameters,
            dict
        ):

            return {
                "success": False,
                "message": (
                    "Browser parameters must "
                    "be a dictionary."
                )
            }

        # =========================================
        # USER ID
        # =========================================

        parameter_user_id = (
            parameters.get(
                "user_id"
            )
        )

        if parameter_user_id is not None:

            try:

                self.set_user_id(
                    parameter_user_id
                )

            except ValueError as error:

                return {
                    "success": False,
                    "message": str(error)
                }

        if not self.user_id:

            return {
                "success": False,
                "message": (
                    "Browser user ID is required."
                )
            }

        # =========================================
        # PARAMETERS
        # =========================================

        action = parameters.get(
            "action",
            "open"
        )

        url = parameters.get(
            "url"
        )

        selector = parameters.get(
            "selector"
        )

        target = parameters.get(
            "target"
        )

        value = parameters.get(
            "value"
        )

        website_name = parameters.get(
            "website_name",
            ""
        )

        page_target = parameters.get(
            "page_target",
            ""
        )

        use_current_page = parameters.get(
            "use_current_page",
            False
        )

        # =========================================
        # WEBSITE DISCOVERY
        # =========================================

        discovery_data = None

        try:

            normalized_action = (
                self._validate_action(
                    action
                )
            )

        except (
            TypeError,
            ValueError
        ) as error:

            return {
                "success": False,
                "message": str(error)
            }

        if (
            normalized_action
            in {
                "open",
                "navigate"
            }
            and not url
            and (
                website_name
                or page_target
            )
        ):

            discovery_data = (
                self._discover_website_url(
                    website_name=website_name,
                    page_target=page_target
                )
            )

            if not discovery_data.get(
                "success",
                False
            ):

                return {
                    "success": False,
                    "status": "failed",
                    "browser": {
                        "action": normalized_action,
                        "user_id": self.user_id,
                        "website_name": website_name,
                        "page_target": page_target
                    },
                    "discovery": discovery_data,
                    "message": (
                        "Website could not be "
                        "discovered."
                    )
                }

            url = discovery_data.get(
                "url"
            )

            if not url:

                return {
                    "success": False,
                    "status": "failed",
                    "browser": {
                        "action": normalized_action,
                        "user_id": self.user_id
                    },
                    "discovery": discovery_data,
                    "message": (
                        "Website discovery did not "
                        "return a valid URL."
                    )
                }

        # =========================================
        # PREPARE ACTION
        # =========================================

        try:

            browser_data = (
                self.prepare_action(
                    action=action,
                    url=url,
                    selector=selector,
                    value=value,
                    use_current_page=(
                        use_current_page
                    ),
                    target=target
                )
            )

        except (
            TypeError,
            ValueError
        ) as error:

            return {
                "success": False,
                "message": str(error),
                "discovery": discovery_data
            }

        action_name = (
            browser_data["action"]
        )

        # =========================================
        # EXECUTE ACTION
        # =========================================

        try:

            # =====================================
            # CLOSE
            # =====================================

            if action_name == "close":

                close_data = (
                    await self._close_session()
                )

                return {
                    "success": True,
                    "status": "completed",
                    "browser": {
                        "action": "close",
                        "user_id": self.user_id,
                        "was_active": (
                            close_data[
                                "was_active"
                            ]
                        )
                    },
                    "message": (
                        "Browser session closed successfully."
                    )
                }

            # =====================================
            # OPEN / NAVIGATE
            # =====================================

            if action_name in {
                "open",
                "navigate"
            }:

                await self._get_page()

                page_data = (
                    await self._open_page(
                        browser_data[
                            "url"
                        ]
                    )
                )

                browser_result = {
                    "action": action_name,
                    "user_id": self.user_id,
                    "requested_url": (
                        browser_data[
                            "url"
                        ]
                    ),
                    "final_url": (
                        page_data[
                            "url"
                        ]
                    ),
                    "title": (
                        page_data[
                            "title"
                        ]
                    ),
                    "status_code": (
                        page_data[
                            "status_code"
                        ]
                    )
                }

                if discovery_data:

                    browser_result[
                        "website_name"
                    ] = website_name

                    browser_result[
                        "page_target"
                    ] = page_target

                    browser_result[
                        "discovered_url"
                    ] = discovery_data.get(
                        "url"
                    )

                return {
                    "success": True,
                    "status": "completed",
                    "browser": browser_result,
                    "discovery": (
                        discovery_data
                        if discovery_data
                        else None
                    ),
                    "message": (
                        "Browser action executed successfully."
                    )
                }

            # =====================================
            # CLICK
            # =====================================

            if action_name == "click":

                await self._get_page()

                current_page = (
                    self._get_session().get_page()
                )

                requested_url = (
                    browser_data.get(
                        "url"
                    )
                )

                use_current = (
                    browser_data.get(
                        "use_current_page",
                        False
                    )
                )

                if (
                    requested_url
                    and not use_current
                    and current_page.url
                    != requested_url
                ):

                    await self._open_page(
                        requested_url
                    )

                click_data = (
                    await self._click_element(
                        selector=browser_data.get(
                            "selector"
                        ),
                        target=browser_data.get(
                            "target",
                            target
                        )
                    )
                )

                return {
                    "success": True,
                    "status": "completed",
                    "browser": {
                        "action": "click",
                        "user_id": self.user_id,
                        "requested_url": (
                            requested_url
                        ),
                        "used_current_page": (
                            use_current
                        ),
                        "final_url": (
                            click_data[
                                "url"
                            ]
                        ),
                        "title": (
                            click_data[
                                "title"
                            ]
                        ),
                        "selector": (
                            click_data[
                                "selector"
                            ]
                        ),
                        "target": (
                            click_data[
                                "target"
                            ]
                        )
                    },
                    "message": (
                        "Browser click executed successfully."
                    )
                }

            # =====================================
            # FILL
            # =====================================

            if action_name == "fill":

                await self._get_page()

                current_page = (
                    self._get_session().get_page()
                )

                requested_url = (
                    browser_data.get(
                        "url"
                    )
                )

                use_current = (
                    browser_data.get(
                        "use_current_page",
                        False
                    )
                )

                if (
                    requested_url
                    and not use_current
                    and current_page.url
                    != requested_url
                ):

                    await self._open_page(
                        requested_url
                    )

                fill_data = (
                    await self._fill_input(
                        selector=browser_data[
                            "selector"
                        ],
                        value=browser_data[
                            "value"
                        ]
                    )
                )

                return {
                    "success": True,
                    "status": "completed",
                    "browser": {
                        "action": "fill",
                        "user_id": self.user_id,
                        "requested_url": (
                            requested_url
                        ),
                        "used_current_page": (
                            use_current
                        ),
                        "final_url": (
                            fill_data[
                                "url"
                            ]
                        ),
                        "title": (
                            fill_data[
                                "title"
                            ]
                        ),
                        "selector": (
                            fill_data[
                                "selector"
                            ]
                        ),
                        "value_length": (
                            fill_data[
                                "value_length"
                            ]
                        )
                    },
                    "message": (
                        "Browser input filled successfully."
                    )
                }

            # =====================================
            # DOWNLOAD
            # =====================================

            if action_name == "download":

                await self._get_page()

                current_page = (
                    self._get_session().get_page()
                )

                requested_url = (
                    browser_data.get(
                        "url"
                    )
                )

                use_current = (
                    browser_data.get(
                        "use_current_page",
                        False
                    )
                )

                if (
                    requested_url
                    and not use_current
                    and current_page.url
                    != requested_url
                ):

                    await self._open_page(
                        requested_url
                    )

                download_data = (
                    await self._download_file(
                        selector=browser_data.get(
                            "selector"
                        ),
                        target=browser_data.get(
                            "target",
                            target
                        ),
                        requested_url=(
                            requested_url
                        ),
                        use_current_page=(
                            use_current
                        )
                    )
                )

                return {
                    "success": True,
                    "status": "completed",
                    "browser": {
                        "action": "download",
                        "user_id": self.user_id,
                        "requested_url": (
                            requested_url
                        ),
                        "used_current_page": (
                            use_current
                        ),
                        "final_url": (
                            download_data[
                                "url"
                            ]
                        ),
                        "title": (
                            download_data[
                                "title"
                            ]
                        ),
                        "selector": (
                            download_data.get(
                                "selector"
                            )
                        ),
                        "target": (
                            download_data.get(
                                "target"
                            )
                        ),
                        "file_url": (
                            download_data.get(
                                "file_url"
                            )
                        ),
                        "filename": (
                            download_data[
                                "filename"
                            ]
                        ),
                        "path": (
                            download_data[
                                "path"
                            ]
                        ),
                        "downloads_folder": (
                            download_data[
                                "downloads_folder"
                            ]
                        ),
                        "size_bytes": (
                            download_data[
                                "size_bytes"
                            ]
                        ),
                        "verified": (
                            download_data.get(
                                "verified",
                                True
                            )
                        )
                    },
                    "message": (
                        "Browser file downloaded successfully."
                    )
                }

            # =====================================
            # READ
            # =====================================

            if action_name == "read":

                await self._get_page()

                current_page = (
                    self._get_session().get_page()
                )

                requested_url = (
                    browser_data.get(
                        "url"
                    )
                )

                use_current = (
                    browser_data.get(
                        "use_current_page",
                        False
                    )
                )

                if (
                    requested_url
                    and not use_current
                    and current_page.url
                    != requested_url
                ):

                    await self._open_page(
                        requested_url
                    )

                read_data = (
                    await self._read_page(
                        selector=browser_data.get(
                            "selector"
                        )
                    )
                )

                return {
                    "success": True,
                    "status": "completed",
                    "browser": {
                        "action": "read",
                        "user_id": self.user_id,
                        "requested_url": (
                            requested_url
                        ),
                        "used_current_page": (
                            use_current
                        ),
                        "final_url": (
                            read_data[
                                "url"
                            ]
                        ),
                        "title": (
                            read_data[
                                "title"
                            ]
                        ),
                        "content": (
                            read_data[
                                "content"
                            ]
                        )
                    },
                    "message": (
                        "Browser page read successfully."
                    )
                }

            # =====================================
            # UNSUPPORTED
            # =====================================

            return {
                "success": False,
                "status": "failed",
                "message": (
                    "Unsupported browser action."
                )
            }

        except Exception as error:

            print(
                "\n"
                "========================================\n"
                "BROWSER TOOL FULL TRACEBACK\n"
                "========================================"
            )

            print(
                "ERROR TYPE:",
                type(error).__name__
            )

            print(
                "ERROR REPR:",
                repr(error)
            )

            print(
                "ERROR STRING:",
                str(error)
            )

            print(
                "TRACEBACK:"
            )

            traceback.print_exc()

            print(
                "========================================\n"
            )

            return {
                "success": False,
                "status": "failed",
                "browser": browser_data,
                "discovery": discovery_data,
                "error_type": (
                    type(error).__name__
                ),
                "error": repr(error),
                "message": (
                    f"Browser action failed: "
                    f"{type(error).__name__}: "
                    f"{repr(error)}"
                )
            }

    # =========================================
    # AVAILABILITY
    # =========================================

    def is_available(
        self
    ) -> bool:

        return True

    # =========================================
    # SESSION STATUS
    # =========================================

    def is_session_active(
        self
    ) -> bool:

        if not self.user_id:

            return False

        return (
            self._get_session()
            .is_active()
        )

