import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.tools.base_tool import BaseTool


# =========================================
# LOAD ENVIRONMENT VARIABLES
# =========================================

load_dotenv()


class SearchTool(BaseTool):

    def __init__(self):

        super().__init__(
            name="search",
            description=(
                "Search for information using AI with "
                "web grounding and return an answer "
                "with real reference sources."
            )
        )

        self.client = None

        # Keep the model that is already working
        # in the current AI Buddy environment.
        self.model = "gemini-3.6-flash"

        self.available = False
        self.error = None

        self._initialize_client()

    # =========================================
    # INITIALIZE GEMINI CLIENT
    # =========================================

    def _initialize_client(self) -> None:

        try:

            api_key = os.getenv("GEMINI_API_KEY")

            if not api_key:

                self.client = None
                self.available = False
                self.error = (
                    "GEMINI_API_KEY is not configured."
                )

                return

            self.client = genai.Client(
                api_key=api_key
            )

            self.available = True
            self.error = None

        except Exception as error:

            self.client = None
            self.available = False
            self.error = str(error)

    # =========================================
    # VALIDATE SEARCH QUERY
    # =========================================

    def _validate_query(
        self,
        query: str
    ) -> str:

        if not isinstance(query, str):

            raise TypeError(
                "Search query must be a string."
            )

        query = query.strip()

        if not query:

            raise ValueError(
                "Search query cannot be empty."
            )

        return query

    # =========================================
    # EXTRACT DOMAIN
    # =========================================

    def _extract_domain(
        self,
        url: str
    ) -> str:

        if not isinstance(url, str):
            return ""

        try:

            parsed_url = urlparse(url)

            domain = parsed_url.netloc

            if domain.startswith("www."):

                domain = domain[4:]

            return domain

        except Exception:

            return ""

    # =========================================
    # EXTRACT WEB SOURCES
    # =========================================

    def _extract_sources(
        self,
        response
    ) -> list:

        sources = []

        try:

            candidates = getattr(
                response,
                "candidates",
                None
            )

            if not candidates:

                return sources

            candidate = candidates[0]

            grounding_metadata = getattr(
                candidate,
                "grounding_metadata",
                None
            )

            if grounding_metadata is None:

                return sources

            grounding_chunks = getattr(
                grounding_metadata,
                "grounding_chunks",
                None
            )

            if not grounding_chunks:

                return sources

            for chunk in grounding_chunks:

                web_chunk = getattr(
                    chunk,
                    "web",
                    None
                )

                if web_chunk is None:

                    continue

                title = getattr(
                    web_chunk,
                    "title",
                    ""
                )

                url = getattr(
                    web_chunk,
                    "uri",
                    ""
                )

                if not isinstance(
                    url,
                    str
                ) or not url.strip():

                    continue

                url = url.strip()

                domain = self._extract_domain(
                    url
                )

                source = {
                    "title": (
                        title.strip()
                        if isinstance(title, str)
                        and title.strip()
                        else "Reference source"
                    ),
                    "url": url,
                    "domain": domain
                }

                if source not in sources:

                    sources.append(source)

        except Exception as error:

            print(
                "SOURCE EXTRACTION ERROR:",
                repr(error)
            )

        return sources

    # =========================================
    # EXTRACT IMAGE SOURCES
    # =========================================

    def _extract_images(
        self,
        response
    ) -> list:

        images = []

        try:

            candidates = getattr(
                response,
                "candidates",
                None
            )

            if not candidates:

                return images

            candidate = candidates[0]

            grounding_metadata = getattr(
                candidate,
                "grounding_metadata",
                None
            )

            if grounding_metadata is None:

                return images

            grounding_chunks = getattr(
                grounding_metadata,
                "grounding_chunks",
                None
            )

            if not grounding_chunks:

                return images

            for chunk in grounding_chunks:

                image_chunk = getattr(
                    chunk,
                    "image",
                    None
                )

                if image_chunk is None:

                    continue

                image_url = getattr(
                    image_chunk,
                    "image_uri",
                    ""
                )

                source_url = getattr(
                    image_chunk,
                    "source_uri",
                    ""
                )

                title = getattr(
                    image_chunk,
                    "title",
                    ""
                )

                domain = getattr(
                    image_chunk,
                    "domain",
                    ""
                )

                if not isinstance(
                    image_url,
                    str
                ) or not image_url.strip():

                    continue

                image_url = image_url.strip()

                if not isinstance(
                    source_url,
                    str
                ):

                    source_url = ""

                source_url = source_url.strip()

                if not isinstance(
                    domain,
                    str
                ) or not domain.strip():

                    domain = self._extract_domain(
                        source_url
                    )

                else:

                    domain = domain.strip()

                image = {
                    "title": (
                        title.strip()
                        if isinstance(title, str)
                        and title.strip()
                        else "Reference image"
                    ),
                    "image_url": image_url,
                    "source_url": source_url,
                    "domain": domain
                }

                if image not in images:

                    images.append(image)

        except Exception as error:

            print(
                "IMAGE EXTRACTION ERROR:",
                repr(error)
            )

        return images

    # =========================================
    # GENERATE GROUNDED AI ANSWER
    # =========================================

    def _generate_answer(
        self,
        query: str
    ) -> dict:

        if self.client is None:

            raise RuntimeError(
                "AI search service is not available."
            )

        response = self.client.models.generate_content(
            model=self.model,
            contents=(
                "You are the search assistant inside "
                "AI Buddy.\n\n"

                "Answer the user's question clearly "
                "and accurately.\n\n"

                "Use Google Search grounding when "
                "current or external information is "
                "useful.\n\n"

                "Use reliable web information and "
                "cite the information through the "
                "available grounding system.\n\n"

                "Do not tell the user to open Google, "
                "Chrome, or another application.\n\n"

                "Do not pretend that a source exists "
                "if no source was actually retrieved.\n\n"

                "Keep the answer useful and easy to "
                "understand.\n\n"

                f"User question:\n{query}"
            ),
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    )
                ]
            )
        )

        if response is None:

            raise RuntimeError(
                "The AI model returned no response."
            )

        answer = getattr(
            response,
            "text",
            None
        )

        if not isinstance(
            answer,
            str
        ) or not answer.strip():

            raise RuntimeError(
                "The AI model returned an empty answer."
            )

        sources = self._extract_sources(
            response
        )

        images = self._extract_images(
            response
        )

        return {
            "answer": answer.strip(),
            "sources": sources,
            "images": images
        }

    # =========================================
    # EXECUTE SEARCH
    # =========================================

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
                "query": "",
                "answer": "",
                "sources": [],
                "images": [],
                "status": "failed",
                "message": (
                    "Search parameters must be "
                    "a dictionary."
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
        ) as error:

            return {
                "success": False,
                "query": "",
                "answer": "",
                "sources": [],
                "images": [],
                "status": "failed",
                "message": str(error)
            }

        # Reinitialize if client is unavailable.
        if not self.available:

            self._initialize_client()

        if not self.available:

            return {
                "success": False,
                "query": query,
                "answer": "",
                "sources": [],
                "images": [],
                "status": "failed",
                "message": (
                    "AI search service is not available."
                ),
                "error": self.error
            }

        try:

            result = self._generate_answer(
                query
            )

            return {
                "success": True,
                "query": query,
                "answer": result.get(
                    "answer",
                    ""
                ),
                "sources": result.get(
                    "sources",
                    []
                ),
                "images": result.get(
                    "images",
                    []
                ),
                "status": "answered",
                "message": (
                    "Question answered successfully."
                )
            }

        except Exception as error:

            self.error = str(error)

            print(
                "SEARCH TOOL ERROR:",
                repr(error)
            )

            return {
                "success": False,
                "query": query,
                "answer": "",
                "sources": [],
                "images": [],
                "status": "failed",
                "message": (
                    "Could not generate an answer "
                    "for the question."
                ),
                "error": self.error
            }

    # =========================================
    # CHECK AVAILABILITY
    # =========================================

    def is_available(
        self
    ) -> bool:

        if self.available:

            return True

        self._initialize_client()

        return self.available

    # =========================================
    # GET TOOL STATUS
    # =========================================

    def get_status(
        self
    ) -> dict:

        return {
            "name": self.name,
            "available": self.is_available(),
            "model": self.model,
            "error": self.error
        }