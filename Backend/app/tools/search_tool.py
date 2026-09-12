from urllib.parse import quote_plus

from app.tools.base_tool import BaseTool


class SearchTool(BaseTool):

    def __init__(self):

        super().__init__(
            name="search",
            description=(
                "Search for information using a web search query."
            )
        )

    # =================================
    # VALIDATE QUERY
    # =================================

    def _validate_query(
        self,
        query: str
    ) -> str:

        if not isinstance(
            query,
            str
        ):
            raise TypeError(
                "Search query must be a string."
            )

        query = query.strip()

        if not query:
            raise ValueError(
                "Search query cannot be empty."
            )

        return query

    # =================================
    # BUILD SEARCH URL
    # =================================

    def build_search_url(
        self,
        query: str
    ) -> str:

        query = self._validate_query(
            query
        )

        encoded_query = quote_plus(
            query
        )

        return (
            "https://www.google.com/search?q="
            + encoded_query
        )

    # =================================
    # EXECUTE SEARCH
    # =================================

    def execute(
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
                    "Search parameters must be a dictionary."
                )
            }

        query = parameters.get(
            "query",
            ""
        )

        try:

            query = self._validate_query(
                query
            )

        except (
            TypeError,
            ValueError
        ) as e:

            return {
                "success": False,
                "message": str(e)
            }

        search_url = self.build_search_url(
            query
        )

        return {
            "success": True,
            "query": query,
            "search_url": search_url,
            "message": (
                f"Search prepared for: {query}"
            )
        }

    # =================================
    # TOOL AVAILABILITY
    # =================================

    def is_available(self) -> bool:

        return True