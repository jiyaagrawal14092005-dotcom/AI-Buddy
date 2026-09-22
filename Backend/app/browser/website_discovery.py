
from __future__ import annotations

import re
from urllib.parse import urlparse

from app.tools.search_tool import SearchTool


class WebsiteDiscovery:
    """
    Generic website discovery and URL validation layer.

    Responsibilities:
    - Extract explicit URLs from user input.
    - Normalize website names.
    - Build search queries.
    - Use SearchTool for real web discovery.
    - Extract URLs from SearchTool results.
    - Validate discovered URLs.
    - Score discovered URLs.
    - Prefer the likely official domain when multiple domains match.
    - Select the most relevant URL.

    This class does NOT contain hard-coded website URLs.

    Browser automation is handled separately by BrowserTool.
    """

    def __init__(
        self,
        search_tool: SearchTool | None = None
    ):
        # Use an existing SearchTool when supplied.
        # Otherwise create one automatically.
        self.search_tool = (
            search_tool
            if search_tool is not None
            else SearchTool()
        )

    # =========================================================
    # EXTRACT EXPLICIT URL
    # =========================================================

    def extract_explicit_url(
        self,
        text: str
    ) -> str:

        if not isinstance(text, str):
            return ""

        match = re.search(
            r"https?://[^\s,]+",
            text,
            flags=re.IGNORECASE
        )

        if not match:
            return ""

        url = (
            match.group(0)
            .strip()
            .rstrip(".,?!;:)")
        )

        if self.is_valid_url(url):
            return url

        return ""

    # =========================================================
    # NORMALIZE WEBSITE NAME
    # =========================================================

    def normalize_website_name(
        self,
        website_name: str
    ) -> str:

        if not isinstance(
            website_name,
            str
        ):
            return ""

        value = website_name.strip()

        value = re.sub(
            r"^(https?://)?(www\.)?",
            "",
            value,
            flags=re.IGNORECASE
        )

        value = re.sub(
            r"\.(com|org|net|in|co|io|ai)$",
            "",
            value,
            flags=re.IGNORECASE
        )

        value = re.sub(
            r"\s+",
            " ",
            value
        ).strip()

        return value

    # =========================================================
    # CREATE DISCOVERY QUERY
    # =========================================================

    def build_search_query(
        self,
        website_name: str = "",
        page_target: str = ""
    ) -> str:

        website_name = (
            self.normalize_website_name(
                website_name
            )
        )

        page_target = (
            page_target.strip()
            if isinstance(
                page_target,
                str
            )
            else ""
        )

        if website_name and page_target:
            return (
                f"{website_name} "
                f"{page_target} "
                f"official website"
            )

        if website_name:
            return (
                f"{website_name} "
                f"official website"
            )

        return page_target

    # =========================================================
    # SEARCH WEBSITE
    # =========================================================

    def search_website(
        self,
        website_name: str = "",
        page_target: str = ""
    ) -> dict:

        query = self.build_search_query(
            website_name=website_name,
            page_target=page_target
        )

        if not query:
            return {
                "success": False,
                "query": "",
                "url": "",
                "sources": [],
                "message": (
                    "Website discovery query "
                    "cannot be empty."
                )
            }

        # -----------------------------------------------------
        # Check SearchTool availability
        # -----------------------------------------------------

        try:

            if not self.search_tool.is_available():

                return {
                    "success": False,
                    "query": query,
                    "url": "",
                    "sources": [],
                    "message": (
                        "SearchTool is not available."
                    )
                }

        except Exception as error:

            return {
                "success": False,
                "query": query,
                "url": "",
                "sources": [],
                "message": (
                    "Could not check SearchTool "
                    "availability."
                ),
                "error": str(error)
            }

        # -----------------------------------------------------
        # Execute real search
        # -----------------------------------------------------

        try:

            result = self.search_tool.execute(
                {
                    "query": query
                }
            )

        except Exception as error:

            return {
                "success": False,
                "query": query,
                "url": "",
                "sources": [],
                "message": (
                    "Website discovery search failed."
                ),
                "error": str(error)
            }

        if not isinstance(
            result,
            dict
        ):

            return {
                "success": False,
                "query": query,
                "url": "",
                "sources": [],
                "message": (
                    "SearchTool returned an invalid "
                    "response."
                )
            }

        # -----------------------------------------------------
        # Extract sources
        # -----------------------------------------------------

        sources = result.get(
            "sources",
            []
        )

        # SearchTool can return an answer successfully
        # even when no grounded sources are available.
        if not isinstance(
            sources,
            list
        ):
            sources = []

        # -----------------------------------------------------
        # Discover best URL
        # -----------------------------------------------------

        best_url = self.discover_from_results(
            search_results=sources,
            website_name=website_name,
            page_target=page_target
        )

        if not best_url:

            return {
                "success": False,
                "query": query,
                "url": "",
                "sources": sources,
                "search_result": result,
                "message": (
                    "Search completed, but no suitable "
                    "website URL was discovered."
                )
            }

        return {
            "success": True,
            "query": query,
            "url": best_url,
            "sources": sources,
            "search_result": result,
            "message": (
                "Website URL discovered successfully."
            )
        }

    # =========================================================
    # SCORE DISCOVERED URL
    # =========================================================

    def score_url(
        self,
        url: str,
        website_name: str = "",
        page_target: str = ""
    ) -> int:

        if not self.is_valid_url(url):
            return 0

        parsed = urlparse(url)

        hostname = (
            parsed.hostname or ""
        ).lower()

        hostname = hostname.strip()

        score = 0

        website_name = (
            self.normalize_website_name(
                website_name
            ).lower()
        )

        website_key = re.sub(
            r"[^a-z0-9]",
            "",
            website_name
        )

        hostname_key = re.sub(
            r"[^a-z0-9]",
            "",
            hostname
        )

        # -----------------------------------------------------
        # Website-name match
        # -----------------------------------------------------

        if website_key:

            if website_key in hostname_key:
                score += 50

            # -------------------------------------------------
            # Exact hostname identity preference
            #
            # Example:
            # W3Schools
            #     w3schools.com       -> stronger
            #     w3schools.dev       -> weaker
            #
            # This is generic and does not hard-code domains.
            # -------------------------------------------------

            hostname_without_www = re.sub(
                r"^www\.",
                "",
                hostname,
                flags=re.IGNORECASE
            )

            hostname_parts = hostname_without_www.split(".")

            if hostname_parts:

                hostname_base = hostname_parts[0]

                if (
                    hostname_base
                    == website_key
                ):
                    score += 25

        # -----------------------------------------------------
        # Prefer common public website TLDs
        # -----------------------------------------------------

        common_tld_scores = {
            "com": 20,
            "org": 18,
            "net": 16,
            "in": 14,
            "co": 12,
            "io": 10,
            "ai": 8
        }

        if "." in hostname:

            tld = hostname.rsplit(
                ".",
                1
            )[-1].lower()

            score += common_tld_scores.get(
                tld,
                0
            )

        # -----------------------------------------------------
        # HTTPS preference
        # -----------------------------------------------------

        if parsed.scheme.lower() == "https":
            score += 10

        # -----------------------------------------------------
        # Avoid obvious search-engine pages
        # -----------------------------------------------------

        blocked_hosts = {
            "google.com",
            "www.google.com",
            "bing.com",
            "www.bing.com",
            "search.yahoo.com",
            "duckduckgo.com"
        }

        if hostname in blocked_hosts:
            score -= 30

        # -----------------------------------------------------
        # Page-target relevance
        # -----------------------------------------------------

        if page_target:

            normalized_target = re.sub(
                r"[^a-z0-9]+",
                " ",
                page_target.lower()
            ).strip()

            target_words = [
                word
                for word in normalized_target.split()
                if len(word) > 2
            ]

            url_text = (
                url.lower()
                .replace("-", " ")
                .replace("_", " ")
                .replace("/", " ")
            )

            for word in target_words:

                if word in url_text:
                    score += 5

        return score

    # =========================================================
    # CHOOSE BEST URL
    # =========================================================

    def choose_best_url(
        self,
        urls: list[str],
        website_name: str = "",
        page_target: str = ""
    ) -> str:

        if not isinstance(
            urls,
            list
        ):
            return ""

        valid_urls = []

        for url in urls:

            if not isinstance(
                url,
                str
            ):
                continue

            url = url.strip()

            if not self.is_valid_url(url):
                continue

            valid_urls.append(url)

        if not valid_urls:
            return ""

        scored_urls = []

        for index, url in enumerate(valid_urls):

            score = self.score_url(
                url=url,
                website_name=website_name,
                page_target=page_target
            )

            # -------------------------------------------------
            # Search-result order is used only as a tiny
            # tie-breaker. Earlier search results generally
            # have higher relevance.
            # -------------------------------------------------

            order_bonus = max(
                0,
                5 - index
            )

            score += order_bonus

            scored_urls.append(
                (
                    score,
                    -index,
                    url
                )
            )

        scored_urls.sort(
            key=lambda item: (
                item[0],
                item[1]
            ),
            reverse=True
        )

        return scored_urls[0][2]

    # =========================================================
    # VALIDATE URL
    # =========================================================

    def is_valid_url(
        self,
        url: str
    ) -> bool:

        if not isinstance(
            url,
            str
        ):
            return False

        url = url.strip()

        if not url:
            return False

        try:

            parsed = urlparse(url)

        except Exception:

            return False

        if parsed.scheme.lower() not in {
            "http",
            "https"
        }:
            return False

        if not parsed.netloc:
            return False

        hostname = (
            parsed.hostname or ""
        ).strip()

        if not hostname:
            return False

        if "." not in hostname:
            return False

        return True

    # =========================================================
    # DISCOVER FROM SEARCH RESULTS
    # =========================================================

    def discover_from_results(
        self,
        search_results,
        website_name: str = "",
        page_target: str = ""
    ) -> str:

        urls = self._extract_urls(
            search_results
        )

        return self.choose_best_url(
            urls=urls,
            website_name=website_name,
            page_target=page_target
        )

    # =========================================================
    # EXTRACT URLS FROM SEARCH RESULTS
    # =========================================================

    def _extract_urls(
        self,
        search_results
    ) -> list[str]:

        urls = []

        if search_results is None:
            return urls

        # -----------------------------------------------------
        # String result
        # -----------------------------------------------------

        if isinstance(
            search_results,
            str
        ):

            urls.extend(
                re.findall(
                    r"https?://[^\s\"'<>]+",
                    search_results,
                    flags=re.IGNORECASE
                )
            )

        # -----------------------------------------------------
        # Dictionary result
        # -----------------------------------------------------

        elif isinstance(
            search_results,
            dict
        ):

            for key in (
                "url",
                "link",
                "href",
                "source_url",
                "website"
            ):

                value = search_results.get(
                    key
                )

                if isinstance(
                    value,
                    str
                ):

                    urls.append(value)

            for value in search_results.values():

                if isinstance(
                    value,
                    (dict, list, tuple)
                ):

                    urls.extend(
                        self._extract_urls(
                            value
                        )
                    )

        # -----------------------------------------------------
        # List / tuple result
        # -----------------------------------------------------

        elif isinstance(
            search_results,
            (list, tuple)
        ):

            for item in search_results:

                urls.extend(
                    self._extract_urls(
                        item
                    )
                )

        # -----------------------------------------------------
        # Object result
        # -----------------------------------------------------

        else:

            for attribute in (
                "url",
                "link",
                "href"
            ):

                try:

                    value = getattr(
                        search_results,
                        attribute,
                        None
                    )

                except Exception:

                    value = None

                if isinstance(
                    value,
                    str
                ):

                    urls.append(value)

        # -----------------------------------------------------
        # Clean + deduplicate
        # -----------------------------------------------------

        cleaned = []

        seen = set()

        for url in urls:

            if not isinstance(
                url,
                str
            ):
                continue

            url = (
                url
                .strip()
                .rstrip(".,?!;:)")
            )

            if not self.is_valid_url(url):
                continue

            if url in seen:
                continue

            seen.add(url)

            cleaned.append(url)

        return cleaned
