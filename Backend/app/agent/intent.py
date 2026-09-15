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
    # CLEAN GEMINI JSON RESPONSE
    # =========================================

    def _clean_json_response(
        self,
        response_text: str
    ) -> dict:

        if not isinstance(
            response_text,
            str
        ):

            raise ValueError(
                "Invalid AI response."
            )

        response_text = response_text.strip()

        response_text = re.sub(
            r"^```json\s*",
            "",
            response_text,
            flags=re.IGNORECASE
        )

        response_text = re.sub(
            r"^```\s*",
            "",
            response_text
        )

        response_text = re.sub(
            r"\s*```$",
            "",
            response_text
        )

        return json.loads(
            response_text
        )

    # =========================================
    # VALIDATE INTENT RESULT
    # =========================================

    def _validate_result(
        self,
        result: dict
    ) -> dict:

        if not isinstance(
            result,
            dict
        ):

            raise ValueError(
                "Intent result must be a dictionary."
            )

        intent = result.get(
            "intent",
            "GENERAL_QUERY"
        )

        confidence = result.get(
            "confidence",
            0.5
        )

        parameters = result.get(
            "parameters",
            {}
        )

        if not isinstance(
            intent,
            str
        ) or not intent.strip():

            intent = "GENERAL_QUERY"

        if not isinstance(
            confidence,
            (int, float)
        ):

            confidence = 0.5

        confidence = max(
            0.0,
            min(
                1.0,
                float(confidence)
            )
        )

        if not isinstance(
            parameters,
            dict
        ):

            parameters = {}

        return {
            "intent": intent.strip().upper(),
            "confidence": confidence,
            "parameters": parameters
        }

    # =========================================
    # REPAIR MISSING PARAMETERS
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

        # =====================================
        # CREATE TASK PARAMETER REPAIR
        # =====================================

        if intent == "CREATE_TASK":

            task_name = parameters.get(
                "task_name",
                ""
            )

            if (
                not isinstance(
                    task_name,
                    str
                )
                or not task_name.strip()
            ):

                local_result = self._local_detect(
                    message
                )

                local_parameters = local_result.get(
                    "parameters",
                    {}
                )

                if isinstance(
                    local_parameters,
                    dict
                ):

                    local_task_name = (
                        local_parameters.get(
                            "task_name",
                            ""
                        )
                    )

                    if (
                        isinstance(
                            local_task_name,
                            str
                        )
                        and local_task_name.strip()
                    ):

                        parameters["task_name"] = (
                            local_task_name.strip()
                        )

        result["parameters"] = parameters

        return result

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
                r"(?:task\s+(?:to\s+)?|to\s+complete\s+)"
                r"(.+)",
                lower_text
            )

            if match:

                task_name = match.group(
                    1
                ).strip()

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
                r"remind\s+me\s+(?:to\s+)?(.+)",
                lower_text
            )

            if match:

                reminder_text = match.group(
                    1
                ).strip()

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
            r"\s*(seconds?|secs?|minutes?|mins?|hours?|hrs?)?",
            lower_text
        )

        if timer_match:

            value = int(
                timer_match.group(
                    1
                )
            )

            unit = (
                timer_match.group(
                    2
                )
                or "minutes"
            )

            unit = unit.lower()

            if (
                unit.startswith("second")
                or unit.startswith("sec")
            ):

                duration = value / 60

            elif (
                unit.startswith("hour")
                or unit.startswith("hr")
            ):

                duration = value * 60

            else:

                duration = value

            return {
                "intent": "SET_TIMER",
                "confidence": 0.95,
                "parameters": {
                    "duration": duration
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
                r"\b(?:in|at|for)\s+([A-Za-z\s]+)",
                text,
                flags=re.IGNORECASE
            )

            if match:

                city = match.group(
                    1
                ).strip(
                    " .?!,"
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

                recipient = email_match.group(
                    0
                )

            subject = ""

            subject_match = re.search(
                r"\bsubject\s*[:\-]?\s*(.+?)"
                r"(?:\s+message\s*[:\-]?|\s*$)",
                text,
                flags=re.IGNORECASE
            )

            if subject_match:

                subject = subject_match.group(
                    1
                ).strip()

            return {
                "intent": "SEND_EMAIL",
                "confidence": 0.95,
                "parameters": {
                    "recipient": recipient,
                    "subject": subject,
                    "message": ""
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
                r"\s+(?:to|on)\s+(?:my\s+)?calendar",
                lower_text
            )

            if match:

                title = match.group(
                    1
                ).strip()

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
                r"(txt|pdf|docx?|xlsx?|csv|json|py|jpg|jpeg|png)\b",
                text,
                flags=re.IGNORECASE
            )

            if file_match:

                file_path = file_match.group(
                    0
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
            r"\blaunch\s+(calculator|calc|notepad|paint|chrome|google\s+chrome|edge|microsoft\s+edge|vs\s+code|visual\s+studio\s+code)\b",
            r"\bstart\s+(calculator|calc|notepad|paint|chrome|google\s+chrome|edge|microsoft\s+edge|vs\s+code|visual\s+studio\s+code)\b"
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
                r"(calculator|calc|notepad|paint|chrome|google\s+chrome|edge|microsoft\s+edge|vs\s+code|visual\s+studio\s+code)\b",
                lower_text
            )

            if application_match:

                application = application_match.group(
                    1
                ).strip()

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
            r"\bopen\s+(google|youtube|website|browser)\b",
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

                url = url_match.group(
                    0
                ).rstrip(
                    ".,?!"
                )

            elif "google" in lower_text:

                url = "https://www.google.com"

            elif "youtube" in lower_text:

                url = "https://www.youtube.com"

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

            # Explicit search commands

            r"\bsearch\s+for\b",
            r"\bsearch\b",
            r"\blook\s+up\b",
            r"\bfind\s+information\b",
            r"\bfind\s+out\b",

            # Information questions

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

            # Current/latest information

            r"\blatest\b",
            r"\bcurrent\b",
            r"\btoday\b",
            r"\brecent\b",
            r"\bnews\b",
            r"\bupdate\b",
            r"\brecently\b",

            # Knowledge-oriented phrases

            r"\btell\s+me\s+about\b",
            r"\bexplain\b.*\b(?:technology|company|person|topic|concept)\b",
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
                r"(?:search\s+for|look\s+up|search)\s+(.+)",
                lower_text
            )

            if explicit_search_match:

                query = explicit_search_match.group(
                    1
                ).strip()

            else:

                about_match = re.search(
                    r"(?:tell\s+me\s+about|information\s+about|details\s+about)\s+(.+)",
                    lower_text
                )

                if about_match:

                    query = about_match.group(
                        1
                    ).strip()

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

4. Do NOT classify an ordinary factual question
as BROWSE_WEB just because it could be searched
on the internet.

5. Do NOT classify an ordinary factual question as
OPEN_APPLICATION.

6. For CREATE_TASK, task_name is required.

For example:

User message:
"Create a task to learn Python"

Return:

{{
    "intent": "CREATE_TASK",
    "confidence": 0.95,
    "parameters": {{
        "task_name": "learn Python"
    }}
}}

Another example:

User message:
"Add a task to practice SQL"

Return:

{{
    "intent": "CREATE_TASK",
    "confidence": 0.95,
    "parameters": {{
        "task_name": "practice SQL"
    }}
}}

7. For CREATE_REMINDER, return:

{{
    "intent": "CREATE_REMINDER",
    "confidence": 0.9,
    "parameters": {{
        "reminder": "reminder text"
    }}
}}

8. For SET_TIMER, return:

{{
    "intent": "SET_TIMER",
    "confidence": 0.95,
    "parameters": {{
        "duration": 10
    }}
}}

The duration should be in minutes unless the
user clearly specifies another unit.

9. For GET_WEATHER, return:

{{
    "intent": "GET_WEATHER",
    "confidence": 0.9,
    "parameters": {{
        "city": "city name"
    }}
}}

10. For SEARCH_INFORMATION, return:

{{
    "intent": "SEARCH_INFORMATION",
    "confidence": 0.9,
    "parameters": {{
        "query": "user's information request"
    }}
}}

11. For OPEN_APPLICATION, return:

{{
    "intent": "OPEN_APPLICATION",
    "confidence": 0.95,
    "parameters": {{
        "application": "application name",
        "action": "open_application"
    }}
}}

12. For BROWSE_WEB, return:

{{
    "intent": "BROWSE_WEB",
    "confidence": 0.95,
    "parameters": {{
        "action": "open",
        "url": "website URL"
    }}
}}

13. Always return the required parameters
when the intent needs them.

14. Return ONLY valid JSON.

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