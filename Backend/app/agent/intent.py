import json
import re

from google import genai


class IntentDetector:

    def __init__(self):
        self.client = None

        try:
            self.client = genai.Client()
        except Exception:
            self.client = None

    # =========================================
    # JSON CLEANER
    # =========================================

    def _clean_json_response(
        self,
        response_text: str
    ) -> dict:

        if not response_text:
            raise ValueError(
                "Empty response received."
            )

        text = response_text.strip()

        # -------------------------------------
        # Remove markdown code fences
        # -------------------------------------

        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\s*```$",
            "",
            text
        )

        text = text.strip()

        # -------------------------------------
        # Try direct JSON
        # -------------------------------------

        try:
            result = json.loads(
                text
            )

            if isinstance(result, dict):
                return result

        except json.JSONDecodeError:
            pass

        # -------------------------------------
        # Extract JSON object
        # -------------------------------------

        match = re.search(
            r"\{.*\}",
            text,
            flags=re.DOTALL
        )

        if match:

            json_text = match.group(
                0
            )

            try:

                result = json.loads(
                    json_text
                )

                if isinstance(result, dict):
                    return result

            except json.JSONDecodeError:
                pass

        raise ValueError(
            "Gemini response does not contain valid JSON."
        )

    # =========================================
    # PARAMETER REPAIR
    # =========================================

    def _repair_parameters(
        self,
        message: str,
        result: dict
    ) -> dict:

        if not isinstance(
            result,
            dict
        ):
            return result

        intent = result.get(
            "intent",
            "GENERAL_QUERY"
        )

        parameters = result.get(
            "parameters",
            {}
        )

        if not isinstance(
            parameters,
            dict
        ):
            parameters = {}

        text = message.strip()

        lower_text = text.lower()

        # =====================================
        # CREATE TASK
        # =====================================

        if intent == "CREATE_TASK":

            task_name = parameters.get(
                "task_name",
                ""
            )

            if not task_name:

                match = re.search(
                    r"(?:create|make|add)"
                    r"\s+(?:a\s+)?task"
                    r"(?:\s+(?:to|for))?\s+(.+)",
                    text,
                    flags=re.IGNORECASE
                )

                if match:

                    task_name = (
                        match.group(1)
                        .strip()
                    )

            parameters["task_name"] = (
                task_name
            )

        # =====================================
        # CREATE REMINDER
        # =====================================

        elif intent == "CREATE_REMINDER":

            reminder = parameters.get(
                "reminder",
                ""
            )

            if not reminder:

                match = re.search(
                    r"remind\s+me"
                    r"(?:\s+to)?\s+(.+)",
                    text,
                    flags=re.IGNORECASE
                )

                if match:

                    reminder = (
                        match.group(1)
                        .strip()
                    )

            parameters["reminder"] = (
                reminder
            )

        # =====================================
        # SET TIMER
        # =====================================

        elif intent == "SET_TIMER":

            duration = (
                parameters.get(
                    "duration_seconds"
                )
                or parameters.get(
                    "duration"
                )
            )

            if duration is None:

                match = re.search(
                    r"timer"
                    r"(?:\s+for)?\s+"
                    r"(\d+)"
                    r"\s*"
                    r"(seconds?|secs?|"
                    r"minutes?|mins?|"
                    r"hours?|hrs?)?",
                    lower_text
                )

                if match:

                    value = int(
                        match.group(1)
                    )

                    unit = (
                        match.group(2)
                        or "minutes"
                    )

                    if unit.startswith(
                        "second"
                    ) or unit.startswith(
                        "sec"
                    ):

                        duration = value

                    elif unit.startswith(
                        "hour"
                    ) or unit.startswith(
                        "hr"
                    ):

                        duration = (
                            value * 60 * 60
                        )

                    else:

                        duration = (
                            value * 60
                        )

            if duration is not None:

                parameters[
                    "duration_seconds"
                ] = int(
                    duration
                )

        # =====================================
        # GET WEATHER
        # =====================================

        elif intent == "GET_WEATHER":

            city = parameters.get(
                "city",
                ""
            )

            if not city:

                match = re.search(
                    r"\b(?:in|at|for)\s+"
                    r"([A-Za-z\s]+)",
                    text,
                    flags=re.IGNORECASE
                )

                if match:

                    city = (
                        match.group(1)
                        .strip(
                            " .?!,"
                        )
                    )

            parameters["city"] = city

        # =====================================
        # SEARCH INFORMATION
        # =====================================

        elif intent == "SEARCH_INFORMATION":

            query = parameters.get(
                "query",
                ""
            )

            if not query:

                match = re.search(
                    r"(?:search\s+for|"
                    r"look\s+up|search)"
                    r"\s+(.+)",
                    text,
                    flags=re.IGNORECASE
                )

                if match:

                    query = (
                        match.group(1)
                        .strip()
                    )

            parameters["query"] = query

        # =====================================
        # SEND EMAIL
        # =====================================

        elif intent == "SEND_EMAIL":

            recipient = parameters.get(
                "recipient",
                ""
            )

            if not recipient:

                match = re.search(
                    r"\b[A-Za-z0-9._%+-]+@"
                    r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
                    text
                )

                if match:

                    recipient = (
                        match.group(0)
                    )

            parameters["recipient"] = (
                recipient
            )

            subject = parameters.get(
                "subject",
                ""
            )

            if not subject:

                match = re.search(
                    r"\bsubject\s*[:\-]?\s*"
                    r"(.+?)"
                    r"(?=\s+\bmessage\b|\s*$)",
                    text,
                    flags=re.IGNORECASE
                )

                if match:

                    subject = (
                        match.group(1)
                        .strip(
                            " .?!,"
                        )
                    )

            parameters["subject"] = (
                subject
            )

            email_message = parameters.get(
                "message",
                ""
            )

            if not email_message:

                match = re.search(
                    r"\bmessage\s*[:\-]?\s*(.+)$",
                    text,
                    flags=re.IGNORECASE
                )

                if match:

                    email_message = (
                        match.group(1)
                        .strip()
                    )

            parameters["message"] = (
                email_message
            )

        # =====================================
        # CHECK CALENDAR
        # =====================================

        elif intent == "CHECK_CALENDAR":

            parameters.setdefault(
                "title",
                text
            )

            parameters.setdefault(
                "date",
                ""
            )

            parameters.setdefault(
                "time",
                ""
            )

            parameters.setdefault(
                "details",
                ""
            )

        # =====================================
        # MANAGE FILE
        # =====================================

        elif intent == "MANAGE_FILE":

            parameters.setdefault(
                "operation",
                "read"
            )

            parameters.setdefault(
                "file_path",
                ""
            )

            parameters.setdefault(
                "content",
                ""
            )

        # =====================================
        # OPEN APPLICATION
        # =====================================

        elif intent == "OPEN_APPLICATION":

            parameters.setdefault(
                "application",
                ""
            )

            parameters.setdefault(
                "action",
                "open_application"
            )

        # =====================================
        # BROWSE WEB
        # =====================================

        elif intent == "BROWSE_WEB":

            parameters.setdefault(
                "action",
                "open"
            )

            parameters.setdefault(
                "url",
                ""
            )

        result["parameters"] = parameters

        return result

    # =========================================
    # VALIDATE RESULT
    # =========================================

    def _validate_result(
        self,
        result: dict
    ) -> dict:

        if not isinstance(
            result,
            dict
        ):

            return {
                "intent": "GENERAL_QUERY",
                "confidence": 0.0,
                "parameters": {}
            }

        allowed_intents = {
            "CREATE_TASK",
            "CREATE_REMINDER",
            "SET_TIMER",
            "GET_WEATHER",
            "SEARCH_INFORMATION",
            "SEND_EMAIL",
            "CHECK_CALENDAR",
            "MANAGE_FILE",
            "OPEN_APPLICATION",
            "BROWSE_WEB",
            "GENERAL_QUERY"
        }

        intent = result.get(
            "intent",
            "GENERAL_QUERY"
        )

        if intent not in allowed_intents:

            intent = "GENERAL_QUERY"

        confidence = result.get(
            "confidence",
            0.5
        )

        try:

            confidence = float(
                confidence
            )

        except Exception:

            confidence = 0.5

        confidence = max(
            0.0,
            min(
                confidence,
                1.0
            )
        )

        parameters = result.get(
            "parameters",
            {}
        )

        if not isinstance(
            parameters,
            dict
        ):

            parameters = {}

        return {
            "intent": intent,
            "confidence": confidence,
            "parameters": parameters
        }

    # =========================================
    # BROWSER URL EXTRACTION
    # =========================================

    def _extract_browser_url(
        self,
        text: str
    ) -> str:

        url_match = re.search(
            r"https?://[^\s]+",
            text,
            flags=re.IGNORECASE
        )

        if url_match:

            return (
                url_match.group(0)
                .rstrip(
                    ".,?!"
                )
            )

        lower_text = text.lower()

        if "google" in lower_text:

            return "https://www.google.com"

        if "youtube" in lower_text:

            return "https://www.youtube.com"

        return ""

    # =========================================
    # BROWSER VALUE EXTRACTION
    # =========================================

    def _extract_fill_value(
        self,
        text: str
    ) -> str:

        patterns = [

            r"\bwith\s+(.+)$",

            r"\bas\s+(.+)$",

            r"\bto\s+(.+)$",

            r"\bvalue\s*[:\-]?\s*(.+)$",

            r"\benter\s+(.+)$",

            r"\btype\s+(.+)$"

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            if match:

                value = (
                    match.group(1)
                    .strip(
                        " .?!,"
                    )
                )

                if value:

                    return value

        return ""

    # =========================================
    # BROWSER SELECTOR EXTRACTION
    # =========================================

    def _extract_browser_selector(
        self,
        text: str,
        action: str
    ) -> str:

        lower_text = text.lower()

        # -------------------------------------
        # Explicit CSS selector
        # -------------------------------------

        selector_match = re.search(
            r"\b(?:selector|css)\s*[:\-]?\s*"
            r"([#.\[\]A-Za-z0-9_='\": >_-]+)",
            text,
            flags=re.IGNORECASE
        )

        if selector_match:

            selector = (
                selector_match.group(1)
                .strip(
                    " .,!?;:"
                )
            )

            if selector:

                return selector

        # -------------------------------------
        # Direct CSS selector
        # Example: click #submit
        # -------------------------------------

        direct_selector_match = re.search(
            r"(?:click|press|select)\s+"
            r"(?:the\s+)?([#.][A-Za-z0-9_-]+)",
            text,
            flags=re.IGNORECASE
        )

        if direct_selector_match:

            selector = (
                direct_selector_match.group(1)
                .strip()
            )

            if selector:

                return selector

        # -------------------------------------
        # Common semantic elements
        # -------------------------------------

        if action == "fill":

            if re.search(
                r"\b(name\s+field|"
                r"name\s+input|"
                r"name\s+box|"
                r"my\s+name|"
                r"name\s+textbox|"
                r"enter\s+(?:your\s+)?name)\b",
                lower_text
            ):

                return "#name"

            if re.search(
                r"\b(email\s+field|"
                r"email\s+input|"
                r"email\s+box)\b",
                lower_text
            ):

                return "#email"

            if re.search(
                r"\b(password\s+field|"
                r"password\s+input|"
                r"password\s+box)\b",
                lower_text
            ):

                return "#password"

            if re.search(
                r"\b(search\s+field|"
                r"search\s+input|"
                r"search\s+box)\b",
                lower_text
            ):

                return "#search"

        if action == "click":

            if re.search(
                r"\b(submit\s+button|"
                r"submit\s+btn|"
                r"button\s+to\s+submit|"
                r"click\s+submit)\b",
                lower_text
            ):

                return "button[type='submit']"

            if re.search(
                r"\b(login\s+button|"
                r"login\s+btn|"
                r"sign\s+in\s+button)\b",
                lower_text
            ):

                return "button:has-text('Login')"

            if re.search(
                r"\b(search\s+button|"
                r"search\s+btn)\b",
                lower_text
            ):

                return "button:has-text('Search')"

            if re.search(
                r"\b(cancel\s+button|"
                r"cancel\s+btn)\b",
                lower_text
            ):

                return "button:has-text('Cancel')"

        if action == "read":

            # ---------------------------------
            # Result / output / response
            # ---------------------------------

            if re.search(
                r"\b(result|output|response)\b",
                lower_text
            ):

                return "#result"

            # ---------------------------------
            # Message / status
            # ---------------------------------

            if re.search(
                r"\b(message|status)\b",
                lower_text
            ):

                return "#message"

        return ""

    # =========================================
    # MULTI-STEP BROWSER DETECTION
    # =========================================

    def _local_browser_multi_step_detect(
        self,
        text: str
    ) -> dict | None:

        lower_text = text.lower()

        # -------------------------------------
        # Must contain browser action language
        # -------------------------------------

        action_words = [
            "open",
            "navigate",
            "go to",
            "visit",
            "click",
            "press",
            "fill",
            "enter",
            "type",
            "read",
            "extract",
            "close"
        ]

        if not any(
            word in lower_text
            for word in action_words
        ):
            return None

        # -------------------------------------
        # Split command into action segments
        # -------------------------------------

        parts = re.split(
            r"\s+(?:and|then)\s+|"
            r"\s*,\s*",
            text,
            flags=re.IGNORECASE
        )

        if len(parts) < 2:
            return None

        steps = []

        # -------------------------------------
        # Track whether a browser page
        # has already been opened
        # -------------------------------------

        known_url = ""

        for part in parts:

            segment = part.strip()

            if not segment:
                continue

            lower_segment = segment.lower()

            # =================================
            # OPEN
            # =================================

            open_match = re.search(
                r"\bopen\s+"
                r"(https?://[^\s,]+|"
                r"(?:the\s+)?(?:google|youtube)\b)",
                segment,
                flags=re.IGNORECASE
            )

            if open_match:

                url = self._extract_browser_url(
                    segment
                )

                if url:

                    known_url = url

                    steps.append(
                        {
                            "action": "open",
                            "url": url
                        }
                    )

                    continue

            # =================================
            # NAVIGATE
            # =================================

            navigate_match = re.search(
                r"\b(?:navigate\s+to|"
                r"go\s+to|visit)\b",
                lower_segment
            )

            if navigate_match:

                url = self._extract_browser_url(
                    segment
                )

                if url:

                    known_url = url

                    steps.append(
                        {
                            "action": "navigate",
                            "url": url
                        }
                    )

                    continue

            # =================================
            # CLICK
            # =================================

            click_match = re.search(
                r"\b(?:click|press|select)\b",
                lower_segment
            )

            if click_match:

                selector = (
                    self._extract_browser_selector(
                        segment,
                        "click"
                    )
                )

                if selector:

                    click_parameters = {
                        "action": "click",
                        "selector": selector
                    }

                    if known_url:

                        click_parameters["use_current_page"] = True

                    steps.append(
                        click_parameters
                    )

                    continue

            # =================================
            # FILL
            # =================================

            fill_match = re.search(
                r"\b(?:fill|enter|type|put)\b",
                lower_segment
            )

            if fill_match:

                selector = (
                    self._extract_browser_selector(
                        segment,
                        "fill"
                    )
                )

                value = (
                    self._extract_fill_value(
                        segment
                    )
                )

                if selector and value:

                    fill_parameters = {
                        "action": "fill",
                        "selector": selector,
                        "value": value
                    }

                    if known_url:

                        fill_parameters[
                            "use_current_page"
                        ] = True

                    steps.append(
                        fill_parameters
                    )

                    continue

            # =================================
            # READ
            # =================================

            read_match = re.search(
                r"\b(?:read|extract|get)\b",
                lower_segment
            )

            if read_match:

                selector = (
                    self._extract_browser_selector(
                        segment,
                        "read"
                    )
                )

                if not selector:

                    selector = "body"

                read_parameters = {
                    "action": "read",
                    "selector": selector,
                    "use_current_page": True
                }

                steps.append(
                    read_parameters
                )

                continue

            # =================================
            # CLOSE
            # =================================

            close_match = re.search(
                r"\b(?:close|exit)\b"
                r".*\bbrowser\b",
                lower_segment
            )

            if close_match:

                steps.append(
                    {
                        "action": "close",
                        "use_current_page": True
                    }
                )

                continue

        # -------------------------------------
        # Need at least 2 valid steps
        # -------------------------------------

        if len(steps) < 2:

            return None

        # -------------------------------------
        # Convert steps to planner format
        # -------------------------------------

        planner_steps = []

        for index, step_parameters in enumerate(
            steps,
            start=1
        ):

            planner_steps.append(
                {
                    "step": index,
                    "tool": "browser",
                    "parameters": step_parameters
                }
            )

        return {
            "intent": "BROWSE_WEB",
            "confidence": 0.99,
            "parameters": {
                "steps": planner_steps
            }
        }

    # =========================================
    # LOCAL BROWSER DETECTION
    # =========================================

    def _local_browser_detect(
        self,
        text: str
    ) -> dict | None:

        lower_text = text.lower()

        # =====================================
        # MULTI-STEP BROWSER COMMAND
        # =====================================

        multi_step_result = (
            self._local_browser_multi_step_detect(
                text
            )
        )

        if multi_step_result is not None:

            return multi_step_result

        # =====================================
        # CLOSE BROWSER
        # =====================================

        close_patterns = [
            r"\bclose\s+(?:the\s+)?browser\b",
            r"\bclose\s+(?:the\s+)?web\s+browser\b",
            r"\bexit\s+(?:the\s+)?browser\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in close_patterns
        ):

            return {
                "intent": "BROWSE_WEB",
                "confidence": 0.99,
                "parameters": {
                    "action": "close",
                    "url": "",
                    "use_current_page": True
                }
            }

        # =====================================
        # FILL
        # =====================================

        fill_patterns = [
            r"\bfill\b",
            r"\benter\b.*\bfield\b",
            r"\btype\b.*\bfield\b",
            r"\bput\b.*\bfield\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in fill_patterns
        ):

            url = self._extract_browser_url(
                text
            )

            selector = (
                self._extract_browser_selector(
                    text,
                    "fill"
                )
            )

            value = (
                self._extract_fill_value(
                    text
                )
            )

            if selector and value:

                return {
                    "intent": "BROWSE_WEB",
                    "confidence": 0.98,
                    "parameters": {
                        "action": "fill",
                        "url": url,
                        "selector": selector,
                        "value": value,
                        "use_current_page": not bool(url)
                    }
                }

        # =====================================
        # CLICK
        # =====================================

        click_patterns = [
            r"\bclick\b",
            r"\bpress\b.*\bbutton\b",
            r"\bselect\b.*\bbutton\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in click_patterns
        ):

            url = self._extract_browser_url(
                text
            )

            selector = (
                self._extract_browser_selector(
                    text,
                    "click"
                )
            )

            if selector:

                return {
                    "intent": "BROWSE_WEB",
                    "confidence": 0.98,
                    "parameters": {
                        "action": "click",
                        "url": url,
                        "selector": selector,
                        "use_current_page": not bool(url)
                    }
                }

        # =====================================
        # READ PAGE
        # =====================================

        read_patterns = [
            r"\bread\s+(?:(?:the|this)\s+)?page\b",
            r"\bread\s+(?:(?:the|this)\s+)?webpage\b",
            r"\bread\s+(?:the\s+)?current\s+page\b",
            r"\bread\s+(?:the\s+)?result\b",
            r"\bread\s+(?:the\s+)?output\b",
            r"\bread\s+(?:the\s+)?response\b",
            r"\bget\s+(?:the\s+)?page\s+text\b",
            r"\bextract\s+(?:the\s+)?page\b",
            r"\bread\s+selector\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in read_patterns
        ):

            url = self._extract_browser_url(
                text
            )

            selector = (
                self._extract_browser_selector(
                    text,
                    "read"
                )
            )

            if not selector:
                selector = "body"

            return {
                "intent": "BROWSE_WEB",
                "confidence": 0.98,
                "parameters": {
                    "action": "read",
                    "url": url,
                    "selector": selector,
                    "use_current_page": not bool(url)
                }
            }

        # =====================================
        # NAVIGATE
        # =====================================

        navigate_patterns = [
            r"\bnavigate\s+to\b",
            r"\bgo\s+to\b",
            r"\bvisit\b",
            r"\bopen\s+(?:the\s+)?website\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in navigate_patterns
        ):

            url = self._extract_browser_url(
                text
            )

            if url:

                return {
                    "intent": "BROWSE_WEB",
                    "confidence": 0.98,
                    "parameters": {
                        "action": "navigate",
                        "url": url
                    }
                }

        # =====================================
        # OPEN WEBSITE / GOOGLE / YOUTUBE
        # =====================================

        open_patterns = [
            r"\bopen\s+google\b",
            r"\bopen\s+youtube\b",
            r"\bopen\s+(?:the\s+)?browser\b",
            r"\bopen\s+(?:a\s+)?website\b",
            r"\bopen\s+(?:this\s+)?url\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in open_patterns
        ):

            url = self._extract_browser_url(
                text
            )

            return {
                "intent": "BROWSE_WEB",
                "confidence": 0.98,
                "parameters": {
                    "action": "open",
                    "url": url
                }
            }

        return None

    # =========================================
    # LOCAL INTENT DETECTION
    # =========================================

    def _local_detect(
        self,
        message: str
    ) -> dict:

        text = message.strip()

        lower_text = text.lower()

        # =====================================
        # BROWSER
        # =====================================

        browser_result = (
            self._local_browser_detect(
                text
            )
        )

        if browser_result is not None:

            return browser_result

        # =====================================
        # CREATE TASK
        # =====================================

        task_patterns = [
            r"\bcreate\s+(a\s+)?task\b",
            r"\badd\s+(a\s+)?task\b",
            r"\bmake\s+(a\s+)?task\b",
            r"\btask\b.*\bto\b",
            r"\btask\b.*\bcomplete\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in task_patterns
        ):

            task_name = ""

            match = re.search(
                r"(?:task\s+(?:to\s+)?|"
                r"to\s+complete\s+)"
                r"(.+)",
                lower_text
            )

            if match:

                task_name = (
                    match.group(1)
                    .strip()
                )

            if not task_name:

                task_name = text

            return {
                "intent": "CREATE_TASK",
                "confidence": 0.9,
                "parameters": {
                    "task_name": task_name
                }
            }

        # =====================================
        # CREATE REMINDER
        # =====================================

        reminder_patterns = [
            r"\bremind\s+me\b",
            r"\bcreate\s+(a\s+)?reminder\b",
            r"\bset\s+(a\s+)?reminder\b",
            r"\badd\s+(a\s+)?reminder\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in reminder_patterns
        ):

            reminder_text = text

            match = re.search(
                r"remind\s+me\s+"
                r"(?:to\s+)?(.+)",
                lower_text
            )

            if match:

                reminder_text = (
                    match.group(1)
                    .strip()
                )

            return {
                "intent": "CREATE_REMINDER",
                "confidence": 0.9,
                "parameters": {
                    "reminder": reminder_text
                }
            }

        # =====================================
        # SET TIMER
        # =====================================

        timer_match = re.search(
            r"\b(?:set\s+)?(?:a\s+)?timer\b"
            r"(?:\s+for)?\s+(\d+)"
            r"\s*(seconds?|secs?|"
            r"minutes?|mins?|"
            r"hours?|hrs?)?",
            lower_text
        )

        if timer_match:

            value = int(
                timer_match.group(1)
            )

            unit = (
                timer_match.group(2)
                or "minutes"
            )

            unit = unit.lower()

            if (
                unit.startswith(
                    "second"
                )
                or unit.startswith(
                    "sec"
                )
            ):

                duration_seconds = value

            elif (
                unit.startswith(
                    "hour"
                )
                or unit.startswith(
                    "hr"
                )
            ):

                duration_seconds = (
                    value * 60 * 60
                )

            else:

                duration_seconds = (
                    value * 60
                )

            return {
                "intent": "SET_TIMER",
                "confidence": 0.95,
                "parameters": {
                    "duration_seconds":
                        duration_seconds
                }
            }

        # =====================================
        # GET WEATHER
        # =====================================

        weather_patterns = [
            r"\bweather\b",
            r"\btemperature\b",
            r"\bforecast\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in weather_patterns
        ):

            city = ""

            match = re.search(
                r"\b(?:in|at|for)\s+"
                r"([A-Za-z\s]+)",
                text,
                flags=re.IGNORECASE
            )

            if match:

                city = (
                    match.group(1)
                    .strip(
                        " .?!,"
                    )
                )

            return {
                "intent": "GET_WEATHER",
                "confidence": 0.9,
                "parameters": {
                    "city": city
                }
            }

        # =====================================
        # SEND EMAIL
        # =====================================

        email_patterns = [
            r"\bsend\s+(an\s+)?email\b",
            r"\bsend\s+(an\s+)?e-mail\b",
            r"\bwrite\s+(an\s+)?email\b",
            r"\bcompose\s+(an\s+)?email\b",
            r"\bemail\b.*\bto\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in email_patterns
        ):

            recipient = ""

            email_match = re.search(
                r"\b[A-Za-z0-9._%+-]+@"
                r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
                text
            )

            if email_match:

                recipient = (
                    email_match.group(0)
                )

            subject = ""

            subject_match = re.search(
                r"\bsubject\s*[:\-]?\s*"
                r"(.+?)"
                r"(?=\s+\bmessage\b|\s*$)",
                text,
                flags=re.IGNORECASE
            )

            if subject_match:

                subject = (
                    subject_match.group(1)
                    .strip(
                        " .?!,"
                    )
                )

            email_message = ""

            message_match = re.search(
                r"\bmessage\s*[:\-]?\s*(.+)$",
                text,
                flags=re.IGNORECASE
            )

            if message_match:

                email_message = (
                    message_match.group(1)
                    .strip()
                )

            if not email_message:

                fallback_message_match = re.search(
                    r"\b(?:saying|that\s+says|"
                    r"with\s+message)\s+(.+)$",
                    text,
                    flags=re.IGNORECASE
                )

                if fallback_message_match:

                    email_message = (
                        fallback_message_match
                        .group(1)
                        .strip()
                    )

            return {
                "intent": "SEND_EMAIL",
                "confidence": 0.95,
                "parameters": {
                    "recipient": recipient,
                    "subject": subject,
                    "message": email_message
                }
            }

        # =====================================
        # CHECK CALENDAR
        # =====================================

        calendar_patterns = [
            r"\bcalendar\b",
            r"\bschedule\b",
            r"\badd\b.*\bcalendar\b",
            r"\bcreate\b.*\bevent\b",
            r"\badd\b.*\bevent\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in calendar_patterns
        ):

            title = text

            match = re.search(
                r"(?:add|create)\s+(.+?)"
                r"\s+(?:to|on)\s+"
                r"(?:my\s+)?calendar",
                lower_text
            )

            if match:

                title = (
                    match.group(1)
                    .strip()
                )

            return {
                "intent": "CHECK_CALENDAR",
                "confidence": 0.9,
                "parameters": {
                    "title": title,
                    "date": "",
                    "time": "",
                    "details": ""
                }
            }

        # =====================================
        # MANAGE FILE
        # =====================================

        file_patterns = [
            r"\bcreate\s+(a\s+)?file\b",
            r"\bmake\s+(a\s+)?file\b",
            r"\bopen\s+(a\s+)?file\b",
            r"\bread\s+(a\s+)?file\b",
            r"\bupdate\s+(a\s+)?file\b",
            r"\bdelete\s+(a\s+)?file\b",
            r"\bmanage\s+(a\s+)?file\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in file_patterns
        ):

            operation = "read"

            if re.search(
                r"\b(create|make)\b.*\bfile\b",
                lower_text
            ):

                operation = "create"

            elif re.search(
                r"\b(update|edit|modify)\b.*\bfile\b",
                lower_text
            ):

                operation = "update"

            elif re.search(
                r"\b(delete|remove)\b.*\bfile\b",
                lower_text
            ):

                operation = "delete"

            file_path = ""

            file_match = re.search(
                r"\b[\w.-]+\."
                r"(txt|pdf|docx?|xlsx?|"
                r"csv|json|py|jpg|jpeg|png)\b",
                text,
                flags=re.IGNORECASE
            )

            if file_match:

                file_path = (
                    file_match.group(0)
                )

            return {
                "intent": "MANAGE_FILE",
                "confidence": 0.95,
                "parameters": {
                    "operation": operation,
                    "file_path": file_path,
                    "content": ""
                }
            }

        # =====================================
        # APPLICATION LAUNCHER
        # =====================================

        application_patterns = [
            r"\bopen\s+(calculator|calc)\b",
            r"\bopen\s+(notepad)\b",
            r"\bopen\s+(paint)\b",
            r"\bopen\s+(chrome|google\s+chrome)\b",
            r"\bopen\s+(edge|microsoft\s+edge)\b",
            r"\bopen\s+(vs\s+code|visual\s+studio\s+code)\b",
            r"\blaunch\s+(calculator|calc|"
            r"notepad|paint|chrome|google\s+chrome|"
            r"edge|microsoft\s+edge|vs\s+code|"
            r"visual\s+studio\s+code)\b",
            r"\bstart\s+(calculator|calc|"
            r"notepad|paint|chrome|google\s+chrome|"
            r"edge|microsoft\s+edge|vs\s+code|"
            r"visual\s+studio\s+code)\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in application_patterns
        ):

            application = ""

            application_match = re.search(
                r"\b(?:open|launch|start)\s+"
                r"(calculator|calc|notepad|paint|"
                r"chrome|google\s+chrome|edge|"
                r"microsoft\s+edge|vs\s+code|"
                r"visual\s+studio\s+code)\b",
                lower_text
            )

            if application_match:

                application = (
                    application_match.group(1)
                    .strip()
                )

            return {
                "intent": "OPEN_APPLICATION",
                "confidence": 0.95,
                "parameters": {
                    "application": application,
                    "action": "open_application"
                }
            }

        # =====================================
        # BROWSE WEB
        # =====================================

        browser_patterns = [
            r"\bopen\s+(google|youtube|"
            r"website|browser)\b",
            r"\bopen\s+(https?://)",
            r"\bnavigate\s+to\b",
            r"\bgo\s+to\b",
            r"\bbrowse\b",
            r"\bsearch\s+this\s+on\s+google\b",
            r"\bsearch\s+this\s+in\s+google\b",
            r"\bgoogle\s+this\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in browser_patterns
        ):

            url = ""

            url_match = re.search(
                r"https?://[^\s]+",
                text,
                flags=re.IGNORECASE
            )

            if url_match:

                url = (
                    url_match.group(0)
                    .rstrip(
                        ".,?!"
                    )
                )

            elif "google" in lower_text:

                url = (
                    "https://www.google.com"
                )

            elif "youtube" in lower_text:

                url = (
                    "https://www.youtube.com"
                )

            return {
                "intent": "BROWSE_WEB",
                "confidence": 0.95,
                "parameters": {
                    "action": "open",
                    "url": url
                }
            }

        # =====================================
        # SEARCH INFORMATION
        # =====================================

        search_patterns = [

            r"\bsearch\s+for\b",

            r"\bsearch\b",

            r"\blook\s+up\b",

            r"\bfind\s+information\b",

            r"\bfind\s+out\b",

            r"^\s*what\s+is\b",

            r"^\s*what\s+are\b",

            r"^\s*who\s+is\b",

            r"^\s*who\s+are\b",

            r"^\s*where\s+is\b",

            r"^\s*where\s+are\b",

            r"^\s*when\s+is\b",

            r"^\s*when\s+was\b",

            r"^\s*when\s+did\b",

            r"^\s*why\s+is\b",

            r"^\s*why\s+are\b",

            r"^\s*why\s+was\b",

            r"^\s*why\s+were\b",

            r"^\s*how\s+does\b",

            r"^\s*how\s+do\b",

            r"^\s*how\s+is\b",

            r"^\s*how\s+are\b",

            r"^\s*how\s+can\b",

            r"^\s*how\s+to\b",

            r"\blatest\b",

            r"\bcurrent\b",

            r"\btoday\b",

            r"\brecent\b",

            r"\bnews\b",

            r"\bupdate\b",

            r"\brecently\b",

            r"\btell\s+me\s+about\b",

            r"\bexplain\b.*"
            r"\b(?:technology|company|person|"
            r"topic|concept)\b",

            r"\binformation\s+about\b",

            r"\bdetails\s+about\b"

        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in search_patterns
        ):

            query = text

            explicit_search_match = re.search(
                r"(?:search\s+for|"
                r"look\s+up|search)\s+(.+)",
                lower_text
            )

            if explicit_search_match:

                query = (
                    explicit_search_match.group(1)
                    .strip()
                )

            else:

                about_match = re.search(
                    r"(?:tell\s+me\s+about|"
                    r"information\s+about|"
                    r"details\s+about)\s+(.+)",
                    lower_text
                )

                if about_match:

                    query = (
                        about_match.group(1)
                        .strip()
                    )

            return {
                "intent": "SEARCH_INFORMATION",
                "confidence": 0.9,
                "parameters": {
                    "query": query
                }
            }

        # =====================================
        # GENERAL QUERY
        # =====================================

        return {
            "intent": "GENERAL_QUERY",
            "confidence": 0.7,
            "parameters": {}
        }

    # =========================================
    # GEMINI INTENT DETECTION
    # =========================================

    def _detect_with_gemini(
        self,
        message: str
    ) -> dict:

        if self.client is None:

            raise RuntimeError(
                "Gemini client is unavailable."
            )

        prompt = f"""
You are the intent detection system for AI Buddy.

Identify the user's intent from the following message.

Allowed intents:

CREATE_TASK
CREATE_REMINDER
SET_TIMER
GET_WEATHER
SEARCH_INFORMATION
SEND_EMAIL
CHECK_CALENDAR
MANAGE_FILE
OPEN_APPLICATION
BROWSE_WEB
GENERAL_QUERY

IMPORTANT RULES:

1. Questions asking for factual or informational
knowledge should normally use SEARCH_INFORMATION.

Examples:

"What is Python?"
"What is machine learning?"
"Who is the CEO of Microsoft?"
"How does cloud computing work?"
"Where is Bengaluru?"
"Why is Python popular?"
"Tell me about Databricks."

2. Requests that explicitly ask to search for
information should use SEARCH_INFORMATION.

Examples:

"Search for Python"
"Look up machine learning"
"Find information about AI"

3. Requests to open Google, Chrome, YouTube,
a browser, or a website should use BROWSE_WEB.

Examples:

"Open Google"
"Open Chrome"
"Go to YouTube"
"Search this on Google"

4. Browser interaction requests should use BROWSE_WEB.

Examples:

"Fill the name field with AI Buddy"
"Fill the email field with test@example.com"
"Click the submit button"
"Read the result"
"Read the page"
"Close the browser"
"Navigate to https://example.com"

5. MULTI-STEP BROWSER COMMANDS:

If the user requests multiple browser actions
in one command, return a "steps" list.

Examples:

"Open https://example.com and read the page"

Return:

{{
    "intent": "BROWSE_WEB",
    "confidence": 0.99,
    "parameters": {{
        "steps": [
            {{
                "action": "open",
                "url": "https://example.com"
            }},
            {{
                "action": "read",
                "selector": "body",
                "use_current_page": true
            }}
        ]
    }}
}}

Another example:

"Open https://example.com and click the submit button"

Return:

{{
    "intent": "BROWSE_WEB",
    "confidence": 0.99,
    "parameters": {{
        "steps": [
            {{
                "action": "open",
                "url": "https://example.com"
            }},
            {{
                "action": "click",
                "selector": "button[type='submit']",
                "use_current_page": true
            }}
        ]
    }}
}}

Another example:

"Open https://example.com, fill the name field with Jiya, and read the page"

Return:

{{
    "intent": "BROWSE_WEB",
    "confidence": 0.99,
    "parameters": {{
        "steps": [
            {{
                "action": "open",
                "url": "https://example.com"
            }},
            {{
                "action": "fill",
                "selector": "#name",
                "value": "Jiya",
                "use_current_page": true
            }},
            {{
                "action": "read",
                "selector": "body",
                "use_current_page": true
            }}
        ]
    }}
}}

6. Do NOT classify an ordinary factual question
as BROWSE_WEB just because it could be searched
on the internet.

7. Do NOT classify an ordinary factual question as
OPEN_APPLICATION.

8. For CREATE_TASK, task_name is required.

Example:

User:
"Create a task to learn Python"

Return:

{{
    "intent": "CREATE_TASK",
    "confidence": 0.95,
    "parameters": {{
        "task_name": "learn Python"
    }}
}}

9. For CREATE_REMINDER, return:

{{
    "intent": "CREATE_REMINDER",
    "confidence": 0.9,
    "parameters": {{
        "reminder": "reminder text"
    }}
}}

10. For SET_TIMER, return:

{{
    "intent": "SET_TIMER",
    "confidence": 0.95,
    "parameters": {{
        "duration": 10
    }}
}}

The duration should be in minutes unless the
user clearly specifies another unit.

11. For GET_WEATHER, return:

{{
    "intent": "GET_WEATHER",
    "confidence": 0.9,
    "parameters": {{
        "city": "city name"
    }}
}}

12. For SEARCH_INFORMATION, return:

{{
    "intent": "SEARCH_INFORMATION",
    "confidence": 0.9,
    "parameters": {{
        "query": "user's information request"
    }}
}}

13. For OPEN_APPLICATION, return:

{{
    "intent": "OPEN_APPLICATION",
    "confidence": 0.95,
    "parameters": {{
        "application": "application name",
        "action": "open_application"
    }}
}}

14. For BROWSE_WEB single action, return:

{{
    "intent": "BROWSE_WEB",
    "confidence": 0.95,
    "parameters": {{
        "action": "open",
        "url": "website URL"
    }}
}}

15. For SEND_EMAIL, all three parameters are
required:

recipient
subject
message

Example:

User:
"Send an email to test@example.com with subject Test and message Hello from AI Buddy"

Return:

{{
    "intent": "SEND_EMAIL",
    "confidence": 0.95,
    "parameters": {{
        "recipient": "test@example.com",
        "subject": "Test",
        "message": "Hello from AI Buddy"
    }}
}}

16. Always return required parameters when
the intent needs them.

17. Return ONLY valid JSON.

User message:
{message}
"""

        response = self.client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt
        )

        response_text = getattr(
            response,
            "text",
            None
        )

        if not response_text:

            raise ValueError(
                "Empty response from Gemini."
            )

        result = self._clean_json_response(
            response_text
        )

        return self._repair_parameters(
            message,
            result
        )

    # =========================================
    # PUBLIC DETECT METHOD
    # =========================================

    def detect(
        self,
        message: str
    ) -> dict:

        if (
            not isinstance(
                message,
                str
            )
            or not message.strip()
        ):

            return {
                "intent": "GENERAL_QUERY",
                "confidence": 0.0,
                "parameters": {}
            }

        message = message.strip()

        # =====================================
        # FAST LOCAL BROWSER DETECTION
        # =====================================
        #
        # Browser commands are deterministic.
        # Detect them locally BEFORE Gemini so
        # temporary Gemini 503/429 errors do not
        # convert browser commands into GENERAL_QUERY.
        #

        try:

            local_browser_result = (
                self._local_browser_detect(
                    message
                )
            )

            if local_browser_result is not None:

                return self._validate_result(
                    local_browser_result
                )

        except Exception as error:

            print(
                "⚠️ Local browser detection failed:"
            )

            print(
                f"Error: {error}"
            )

        # =====================================
        # GEMINI DETECTION
        # =====================================

        try:

            result = self._detect_with_gemini(
                message
            )

            return self._validate_result(
                result
            )

        except Exception as e:

            print(
                "⚠️ Gemini unavailable. "
                "Using local intent detection."
            )

            print(
                f"Error: {e}"
            )

            return self._validate_result(
                self._local_detect(
                    message
                )
            )