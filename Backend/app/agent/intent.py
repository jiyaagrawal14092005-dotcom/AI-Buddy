import json
import re
from datetime import date, timedelta

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

        try:
            result = json.loads(text)

            if isinstance(result, dict):
                return result

        except json.JSONDecodeError:
            pass

        match = re.search(
            r"\{.*\}",
            text,
            flags=re.DOTALL
        )

        if match:

            json_text = match.group(0)

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
    # CALENDAR DATE EXTRACTION
    # =========================================

    def _extract_calendar_date(
        self,
        text: str
    ) -> str:

        lower_text = text.lower()

        date_match = re.search(
            r"\b(20\d{2}-\d{2}-\d{2})\b",
            text
        )

        if date_match:
            return date_match.group(1)

        if re.search(
            r"\btoday\b",
            lower_text
        ):
            return date.today().isoformat()

        if re.search(
            r"\btomorrow\b",
            lower_text
        ):
            return (
                date.today()
                + timedelta(days=1)
            ).isoformat()

        if re.search(
            r"\bday\s+after\s+tomorrow\b",
            lower_text
        ):
            return (
                date.today()
                + timedelta(days=2)
            ).isoformat()

        return ""

    # =========================================
    # CALENDAR TIME EXTRACTION
    # =========================================

    def _extract_calendar_time(
        self,
        text: str
    ) -> str:

        time_match = re.search(
            r"\b([01]?\d|2[0-3]):([0-5]\d)\b",
            text
        )

        if time_match:

            hour = int(
                time_match.group(1)
            )

            minute = time_match.group(2)

            return f"{hour:02d}:{minute}"

        am_pm_match = re.search(
            r"\b("
            r"0?[1-9]|1[0-2]"
            r")"
            r":"
            r"([0-5]\d)"
            r"\s*"
            r"(AM|PM)"
            r"\b",
            text,
            flags=re.IGNORECASE
        )

        if am_pm_match:

            hour = int(
                am_pm_match.group(1)
            )

            minute = int(
                am_pm_match.group(2)
            )

            period = (
                am_pm_match.group(3)
                .upper()
            )

            if period == "AM":

                if hour == 12:
                    hour = 0

            else:

                if hour != 12:
                    hour += 12

            return f"{hour:02d}:{minute:02d}"

        hour_only_match = re.search(
            r"\b("
            r"0?[1-9]|1[0-2]"
            r")"
            r"\s*"
            r"(AM|PM)"
            r"\b",
            text,
            flags=re.IGNORECASE
        )

        if hour_only_match:

            hour = int(
                hour_only_match.group(1)
            )

            period = (
                hour_only_match.group(2)
                .upper()
            )

            if period == "AM":

                if hour == 12:
                    hour = 0

            else:

                if hour != 12:
                    hour += 12

            return f"{hour:02d}:00"

        return ""

    # =========================================
    # CALENDAR DURATION EXTRACTION
    # =========================================

    def _extract_calendar_duration(
        self,
        text: str
    ) -> int | None:

        duration_match = re.search(
            r"\bfor\s+(\d+)\s*"
            r"(minutes?|mins?|"
            r"hours?|hrs?)\b",
            text,
            flags=re.IGNORECASE
        )

        if not duration_match:
            return None

        value = int(
            duration_match.group(1)
        )

        unit = (
            duration_match.group(2)
            .lower()
        )

        if unit.startswith(
            ("hour", "hr")
        ):
            return value * 60

        return value

    # =========================================
    # CALENDAR TITLE EXTRACTION
    # =========================================

    def _extract_calendar_title(
        self,
        text: str
    ) -> str:

        title = ""

        titled_match = re.search(
            r"\bcreate\s+(?:a\s+)?"
            r"calendar\s+event"
            r"\s+titled\s+"
            r"(.+?)"
            r"(?=\s+\b(?:on|at|for|today|tomorrow)\b)",
            text,
            flags=re.IGNORECASE
        )

        if titled_match:

            title = (
                titled_match.group(1)
                .strip()
            )

        if not title:

            date_title_match = re.search(
                r"\bcreate\s+(?:a\s+)?"
                r"calendar\s+event"
                r"(?:\s+titled)?\s+"
                r"(.+?)"
                r"\s+\bon\s+"
                r"\d{4}-\d{2}-\d{2}\b",
                text,
                flags=re.IGNORECASE
            )

            if date_title_match:

                title = (
                    date_title_match.group(1)
                    .strip()
                )

        if not title:

            general_match = re.search(
                r"\b(?:create|add|schedule|book)\s+"
                r"(?:a\s+)?"
                r"(?:calendar\s+)?event"
                r"(?:\s+titled)?\s+"
                r"(.+?)"
                r"(?=\s+\b(?:on|at|for|today|tomorrow)\b)",
                text,
                flags=re.IGNORECASE
            )

            if general_match:

                title = (
                    general_match.group(1)
                    .strip()
                )

        title = re.sub(
            r"\s+",
            " ",
            title
        ).strip(
            " .?!,"
        )

        return title

    # =========================================
    # CALENDAR PARAMETER REPAIR
    # =========================================

    def _repair_calendar_parameters(
        self,
        message: str,
        parameters: dict
    ) -> dict:

        if not isinstance(
            parameters,
            dict
        ):
            parameters = {}

        text = message.strip()

        title = parameters.get(
            "title",
            ""
        )

        extracted_title = (
            self._extract_calendar_title(
                text
            )
        )

        if extracted_title:
            title = extracted_title

        date_value = parameters.get(
            "date",
            ""
        )

        extracted_date = (
            self._extract_calendar_date(
                text
            )
        )

        if extracted_date:
            date_value = extracted_date

        time_value = parameters.get(
            "time",
            ""
        )

        extracted_time = (
            self._extract_calendar_time(
                text
            )
        )

        if extracted_time:
            time_value = extracted_time

        duration_minutes = parameters.get(
            "duration_minutes"
        )

        extracted_duration = (
            self._extract_calendar_duration(
                text
            )
        )

        if extracted_duration is not None:
            duration_minutes = extracted_duration

        details = parameters.get(
            "details",
            ""
        )

        if not details:

            details_match = re.search(
                r"\b(?:details?|description)"
                r"\s*[:\-]?\s*(.+?)"
                r"(?=\s+(?:on|at|for)\s+|$)",
                text,
                flags=re.IGNORECASE
            )

            if details_match:

                details = (
                    details_match.group(1)
                    .strip()
                )

        title = title.strip(
            " .?!,"
        )

        date_value = date_value.strip()

        time_value = time_value.strip()

        details = details.strip()

        parameters["title"] = title
        parameters["date"] = date_value
        parameters["time"] = time_value
        parameters["details"] = details

        if duration_minutes is not None:

            parameters[
                "duration_minutes"
            ] = int(
                duration_minutes
            )

        return parameters

    # =========================================
    # BOOKING DATE EXTRACTION
    # =========================================

    def _extract_booking_date(
        self,
        text: str
    ) -> str:

        lower_text = text.lower()

        date_match = re.search(
            r"\b(20\d{2}-\d{2}-\d{2})\b",
            text
        )

        if date_match:
            return date_match.group(1)

        if re.search(
            r"\btoday\b",
            lower_text
        ):
            return date.today().isoformat()

        if re.search(
            r"\btomorrow\b",
            lower_text
        ):
            return (
                date.today()
                + timedelta(days=1)
            ).isoformat()

        if re.search(
            r"\bday\s+after\s+tomorrow\b",
            lower_text
        ):
            return (
                date.today()
                + timedelta(days=2)
            ).isoformat()

        return ""

    # =========================================
    # BOOKING TIME EXTRACTION
    # =========================================

    def _extract_booking_time(
        self,
        text: str
    ) -> str:

        return self._extract_calendar_time(
            text
        )

    # =========================================
    # BOOKING SERVICE EXTRACTION
    # =========================================

    def _extract_booking_service(
        self,
        text: str
    ) -> str:

        service = ""

        patterns = [
            r"\bbook\s+(?:an?\s+)?"
            r"(?:appointment|service|reservation)"
            r"(?:\s+(?:for|at))?\s+"
            r"(.+?)"
            r"(?=\s+\b(?:on|at|for|today|tomorrow)\b|$)",

            r"\bcreate\s+(?:a\s+)?booking"
            r"(?:\s+for)?\s+"
            r"(.+?)"
            r"(?=\s+\b(?:on|at|for|today|tomorrow)\b|$)",

            r"\bbook\s+"
            r"(.+?)"
            r"(?=\s+\b(?:on|at|for|today|tomorrow)\b|$)"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            if match:

                service = (
                    match.group(1)
                    .strip()
                )

                break

        service = re.sub(
            r"\s+",
            " ",
            service
        ).strip(
            " .?!,"
        )

        return service

    # =========================================
    # BOOKING DETAILS EXTRACTION
    # =========================================

    def _extract_booking_details(
        self,
        text: str
    ) -> str:

        details_match = re.search(
            r"\b(?:details?|description)"
            r"\s*[:\-]?\s*(.+)$",
            text,
            flags=re.IGNORECASE
        )

        if details_match:

            return (
                details_match.group(1)
                .strip()
                .strip(" .?!,")
            )

        return ""

    # =========================================
    # BOOKING PARAMETER REPAIR
    # =========================================

    def _repair_booking_parameters(
        self,
        message: str,
        parameters: dict
    ) -> dict:

        if not isinstance(
            parameters,
            dict
        ):
            parameters = {}

        text = message.strip()

        service = parameters.get(
            "service",
            ""
        )

        extracted_service = (
            self._extract_booking_service(
                text
            )
        )

        if extracted_service:
            service = extracted_service

        booking_date = parameters.get(
            "date",
            ""
        )

        extracted_date = (
            self._extract_booking_date(
                text
            )
        )

        if extracted_date:
            booking_date = extracted_date

        booking_time = parameters.get(
            "time",
            ""
        )

        extracted_time = (
            self._extract_booking_time(
                text
            )
        )

        if extracted_time:
            booking_time = extracted_time

        details = parameters.get(
            "details",
            ""
        )

        extracted_details = (
            self._extract_booking_details(
                text
            )
        )

        if extracted_details:
            details = extracted_details

        parameters["service"] = (
            str(service).strip()
        )

        parameters["date"] = (
            str(booking_date).strip()
        )

        parameters["time"] = (
            str(booking_time).strip()
        )

        parameters["details"] = (
            str(details).strip()
        )

        return parameters

    # =========================================
    # SHOPPING QUERY EXTRACTION
    # =========================================

    def _extract_shopping_query(
        self,
        text: str
    ) -> str:

        query = ""

        patterns = [
            r"\bsearch\s+(?:for\s+)?"
            r"(?:a\s+|an\s+|the\s+)?"
            r"(?:product\s+)?(.+)$",

            r"\bfind\s+(?:a\s+|an\s+|the\s+)?"
            r"(?:product\s+)?(.+)$",

            r"\blook\s+for\s+"
            r"(?:a\s+|an\s+|the\s+)?"
            r"(?:product\s+)?(.+)$",

            r"\bshop\s+for\s+"
            r"(?:a\s+|an\s+|the\s+)?"
            r"(.+)$"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            if match:

                query = (
                    match.group(1)
                    .strip()
                )

                break

        if not query:

            query = text.strip()

        query = re.sub(
            r"\s+",
            " ",
            query
        ).strip(
            " .?!,"
        )

        return query

    # =========================================
    # SHOPPING PRODUCT ID EXTRACTION
    # =========================================

    def _extract_product_ids(
        self,
        text: str
    ) -> list[str]:

        product_ids = re.findall(
            r"\bp\d+\b",
            text,
            flags=re.IGNORECASE
        )

        normalized_ids = [
            product_id.upper()
            for product_id in product_ids
        ]

        # -----------------------------------------
        # PRODUCT NAME -> PRODUCT ID MAPPING
        # -----------------------------------------

        product_name_map = {
            "wireless mouse": "P001",
            "mechanical keyboard": "P002",
            "usb-c fast charger": "P003",
            "usb c fast charger": "P003",
            "fast charger": "P003",
            "laptop stand": "P004",
        }

        normalized_text = text.lower()

        for product_name, product_id in product_name_map.items():

            if product_name in normalized_text:

                if product_id not in normalized_ids:

                    normalized_ids.append(
                        product_id
                    )

        return normalized_ids

    # =========================================
    # SHOPPING QUANTITY EXTRACTION
    # =========================================

    def _extract_shopping_quantity(
        self,
        text: str
    ) -> int:

        quantity_patterns = [
            r"\bquantity\s*[:\-]?\s*(\d+)\b",
            r"\bqty\s*[:\-]?\s*(\d+)\b",
            r"\b(\d+)\s*(?:items?|pieces?|pcs?)\b",
            r"\bfor\s+(\d+)\b"
        ]

        for pattern in quantity_patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            if match:

                quantity = int(
                    match.group(1)
                )

                if quantity > 0:
                    return quantity

        return 1

    # =========================================
    # SHOPPING PARAMETER REPAIR
    # =========================================

    def _repair_shopping_parameters(
        self,
        message: str,
        parameters: dict,
        intent: str
    ) -> dict:

        if not isinstance(
            parameters,
            dict
        ):
            parameters = {}

        text = message.strip()

        if intent == "SHOPPING_SEARCH":

            query = parameters.get(
                "query",
                ""
            )

            extracted_query = (
                self._extract_shopping_query(
                    text
                )
            )

            if extracted_query:
                query = extracted_query

            parameters["query"] = (
                str(query).strip()
            )

        elif intent == "SHOPPING_COMPARE":

            products = parameters.get(
                "products",
                []
            )

            if not isinstance(
                products,
                list
            ):
                products = []

            extracted_products = (
                self._extract_product_ids(
                    text
                )
            )

            if extracted_products:
                products = extracted_products

            cleaned_products = []

            for product_id in products:

                if not isinstance(
                    product_id,
                    str
                ):
                    continue

                product_id = (
                    product_id.strip().upper()
                )

                if (
                    product_id
                    and product_id not in cleaned_products
                ):
                    cleaned_products.append(
                        product_id
                    )

            parameters["products"] = (
                cleaned_products
            )

        elif intent == "SHOPPING_CART_ADD":

            product_id = parameters.get(
                "product_id",
                ""
            )

            product_ids = (
                self._extract_product_ids(
                    text
                )
            )

            if product_ids:

                product_id = product_ids[0]

            parameters["product_id"] = (
                str(product_id).strip().upper()
            )

            quantity = parameters.get(
                "quantity",
                1
            )

            extracted_quantity = (
                self._extract_shopping_quantity(
                    text
                )
            )

            if extracted_quantity > 1:
                quantity = extracted_quantity

            try:

                quantity = int(
                    quantity
                )

            except Exception:

                quantity = 1

            if quantity <= 0:
                quantity = 1

            parameters["quantity"] = quantity

        elif intent == "SHOPPING_CART_LIST":

            parameters = {}

        elif intent == "SHOPPING_PURCHASE_PREPARE":

            parameters = {}

        return parameters

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
                ] = int(duration)

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
                        .strip(" .?!,")
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

                    recipient = match.group(0)

            parameters["recipient"] = recipient

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
                        .strip(" .?!,")
                    )

            parameters["subject"] = subject

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

            parameters = (
                self._repair_calendar_parameters(
                    message,
                    parameters
                )
            )

        # =====================================
        # BOOK SERVICE
        # =====================================

        elif intent == "BOOK_SERVICE":

            parameters = (
                self._repair_booking_parameters(
                    message,
                    parameters
                )
            )

        # =====================================
        # SHOPPING
        # =====================================

        elif intent in {
            "SHOPPING_SEARCH",
            "SHOPPING_COMPARE",
            "SHOPPING_CART_ADD",
            "SHOPPING_CART_LIST",
            "SHOPPING_PURCHASE_PREPARE"
        }:

            parameters = (
                self._repair_shopping_parameters(
                    message,
                    parameters,
                    intent
                )
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
            "BOOK_SERVICE",
            "SHOPPING_SEARCH",
            "SHOPPING_COMPARE",
            "SHOPPING_CART_ADD",
            "SHOPPING_CART_LIST",
            "SHOPPING_PURCHASE_PREPARE",
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
                .rstrip(".,?!")
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
                    .strip(" .?!,")
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

        selector_match = re.search(
            r"\b(?:selector|css)\s*[:\-]?\s*"
            r"([#.\[\]A-Za-z0-9_='\": >_-]+)",
            text,
            flags=re.IGNORECASE
        )

        if selector_match:

            selector = (
                selector_match.group(1)
                .strip(" .,!?;:")
            )

            if selector:
                return selector

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

            if re.search(
                r"\b(result|output|response)\b",
                lower_text
            ):

                return "#result"

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

        parts = re.split(
            r"\s+(?:and|then)\s+|"
            r"\s*,\s*",
            text,
            flags=re.IGNORECASE
        )

        if len(parts) < 2:
            return None

        steps = []

        known_url = ""

        for part in parts:

            segment = part.strip()

            if not segment:
                continue

            lower_segment = segment.lower()

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

                        click_parameters[
                            "use_current_page"
                        ] = True

                    steps.append(
                        click_parameters
                    )

                    continue

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

        if len(steps) < 2:
            return None

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

        multi_step_result = (
            self._local_browser_multi_step_detect(
                text
            )
        )

        if multi_step_result is not None:
            return multi_step_result

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

            url = self._extract_browser_url(text)

            selector = (
                self._extract_browser_selector(
                    text,
                    "fill"
                )
            )

            value = (
                self._extract_fill_value(text)
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

            url = self._extract_browser_url(text)

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

            url = self._extract_browser_url(text)

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

            url = self._extract_browser_url(text)

            if url:

                return {
                    "intent": "BROWSE_WEB",
                    "confidence": 0.98,
                    "parameters": {
                        "action": "navigate",
                        "url": url
                    }
                }

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

            url = self._extract_browser_url(text)

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
            self._local_browser_detect(text)
        )

        if browser_result is not None:
            return browser_result

        # =====================================
        # CALENDAR
        # =====================================

        calendar_patterns = [
            r"\bcalendar\b",
            r"\bschedule\b",
            r"\bcreate\s+(?:a\s+)?event\b",
            r"\badd\s+(?:a\s+)?event\b",
            r"\bschedule\s+(?:a\s+)?event\b",
            r"\bbook\s+(?:a\s+)?event\b",
            r"\bcalendar\s+event\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in calendar_patterns
        ):

            parameters = {
                "title": (
                    self._extract_calendar_title(
                        text
                    )
                ),
                "date": (
                    self._extract_calendar_date(
                        text
                    )
                ),
                "time": (
                    self._extract_calendar_time(
                        text
                    )
                ),
                "details": ""
            }

            duration_minutes = (
                self._extract_calendar_duration(
                    text
                )
            )

            if duration_minutes is not None:

                parameters[
                    "duration_minutes"
                ] = duration_minutes

            parameters = (
                self._repair_calendar_parameters(
                    text,
                    parameters
                )
            )

            return {
                "intent": "CHECK_CALENDAR",
                "confidence": 0.99,
                "parameters": parameters
            }

        # =====================================
        # BOOKING
        # =====================================

        booking_patterns = [
            r"\bbook\s+(?:an?\s+)?"
            r"(?:appointment|reservation|service)\b",

            r"\bcreate\s+(?:a\s+)?booking\b",

            r"\bmake\s+(?:a\s+)?booking\b",

            r"\bbook\s+"
            r"(?:a\s+)?(?:cab|taxi|ride|hotel|"
            r"flight|ticket|restaurant|table)\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in booking_patterns
        ):

            parameters = {
                "service": (
                    self._extract_booking_service(
                        text
                    )
                ),
                "date": (
                    self._extract_booking_date(
                        text
                    )
                ),
                "time": (
                    self._extract_booking_time(
                        text
                    )
                ),
                "details": (
                    self._extract_booking_details(
                        text
                    )
                )
            }

            parameters = (
                self._repair_booking_parameters(
                    text,
                    parameters
                )
            )

            return {
                "intent": "BOOK_SERVICE",
                "confidence": 0.98,
                "parameters": parameters
            }

        # =====================================
        # SHOPPING
        # =====================================

        # -------------------------------------
        # SHOPPING COMPARE
        # -------------------------------------

        shopping_compare_patterns = [
            r"\bcompare\b.*\bp\d+\b",
            r"\bcompare\b.*\bproducts?\b",
            r"\bcompare\b.*\bitems?\b",
            r"\bcomparison\b.*\bproducts?\b",
            r"\bcompare\b.*\btwo\b",
            r"\bcompare\b.*\bthese\b",
            r"\bcompare\b.*\band\b.*",
            r"\bcompare\b.*\bwith\b.*"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in shopping_compare_patterns
        ):

            products = (
                self._extract_product_ids(
                    text
                )
            )

            return {
                "intent": "SHOPPING_COMPARE",
                "confidence": 0.98,
                "parameters": {
                    "products": products
                }
            }

        # -------------------------------------
        # SHOPPING CART ADD
        # -------------------------------------

        shopping_cart_add_patterns = [
            # Product ID based commands
            r"\badd\b.*\bp\d+\b.*\b(?:cart|basket)\b",
            r"\badd\b.*\b(?:cart|basket)\b.*\bp\d+\b",
            r"\bput\b.*\bp\d+\b.*\b(?:cart|basket)\b",
            r"\bput\b.*\b(?:cart|basket)\b.*\bp\d+\b",
            r"\bbuy\b.*\bp\d+\b.*\b(?:cart|basket)\b",

            # Generic product/item commands
            r"\badd\b.*\bproduct\b.*\b(?:cart|basket)\b",
            r"\badd\b.*\bitem\b.*\b(?:cart|basket)\b",

            # Product-name based commands
            r"\badd\b.*\b(?:wireless mouse|mechanical keyboard|usb-c fast charger|usb c fast charger|fast charger|laptop stand)\b.*\b(?:cart|basket)\b",
            r"\bput\b.*\b(?:wireless mouse|mechanical keyboard|usb-c fast charger|usb c fast charger|fast charger|laptop stand)\b.*\b(?:cart|basket)\b",
            r"\b(?:wireless mouse|mechanical keyboard|usb-c fast charger|usb c fast charger|fast charger|laptop stand)\b.*\b(?:to|in|into)\b.*\b(?:cart|basket)\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in shopping_cart_add_patterns
        ):

            product_ids = (
                self._extract_product_ids(
                    text
                )
            )

            product_id = (
                product_ids[0]
                if product_ids
                else ""
            )

            quantity = (
                self._extract_shopping_quantity(
                    text
                )
            )

            return {
                "intent": "SHOPPING_CART_ADD",
                "confidence": 0.98,
                "parameters": {
                    "product_id": product_id,
                    "quantity": quantity
                }
            }

        # -------------------------------------
        # SHOPPING CART LIST
        # -------------------------------------

        shopping_cart_list_patterns = [
            r"\bshow\b.*\b(?:my\s+)?cart\b",
            r"\bview\b.*\b(?:my\s+)?cart\b",
            r"\bget\b.*\b(?:my\s+)?cart\b",
            r"\blist\b.*\b(?:my\s+)?cart\b",
            r"\bwhat(?:'s| is)\b.*\bin\s+(?:my\s+)?cart\b",
            r"\bshow\b.*\bbasket\b",
            r"\bview\b.*\bbasket\b",
            r"\bget\b.*\bbasket\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in shopping_cart_list_patterns
        ):

            return {
                "intent": "SHOPPING_CART_LIST",
                "confidence": 0.98,
                "parameters": {}
            }

        # -------------------------------------
        # SHOPPING PURCHASE PREPARATION
        # -------------------------------------

        shopping_purchase_patterns = [
            r"\bprepare\b.*\bpurchase\b",
            r"\bprepare\b.*\border\b",
            r"\bprepare\b.*\bcheckout\b",
            r"\bproceed\b.*\bcheckout\b",
            r"\bcheckout\b",
            r"\bready\b.*\bpurchase\b",
            r"\bprepare\b.*\bbuy\b",

            # Direct purchase commands
            r"\bbuy\b.*\b(?:mouse|keyboard|laptop|phone|"
            r"mobile|headphones?|earphones?|monitor|tablet|"
            r"charger|product|item)\b",

            r"\bpurchase\b.*\b(?:mouse|keyboard|laptop|phone|"
            r"mobile|headphones?|earphones?|monitor|tablet|"
            r"charger|product|item)\b",

            r"\border\b.*\b(?:mouse|keyboard|laptop|phone|"
            r"mobile|headphones?|earphones?|monitor|tablet|"
            r"charger|product|item)\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in shopping_purchase_patterns
        ):

            return {
                "intent": "SHOPPING_PURCHASE_PREPARE",
                "confidence": 0.98,
                "parameters": {}
            }

        # -------------------------------------
        # SHOPPING SEARCH
        # -------------------------------------

        shopping_search_patterns = [
            r"\bsearch\s+(?:for\s+)?"
            r"(?:a\s+|an\s+|the\s+)?"
            r"(?:product\s+)?"
            r"(?:mouse|keyboard|laptop|phone|"
            r"mobile|headphones?|earphones?|"
            r"monitor|tablet|charger|product)\b",

            r"\bfind\s+(?:a\s+|an\s+|the\s+)?"
            r"(?:product\s+)?"
            r"(?:mouse|keyboard|laptop|phone|"
            r"mobile|headphones?|earphones?|"
            r"monitor|tablet|charger|product)\b",

            r"\bshop\s+for\b",

            r"\blook\s+for\b.*\b(?:product|item)\b",

            r"\bfind\b.*\b(?:product|item)\b"
        ]

        if any(
            re.search(
                pattern,
                lower_text
            )
            for pattern in shopping_search_patterns
        ):

            query = (
                self._extract_shopping_query(
                    text
                )
            )

            return {
                "intent": "SHOPPING_SEARCH",
                "confidence": 0.97,
                "parameters": {
                    "query": query
                }
            }

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
                unit.startswith("second")
                or unit.startswith("sec")
            ):

                duration_seconds = value

            elif (
                unit.startswith("hour")
                or unit.startswith("hr")
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
                    .strip(" .?!,")
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
                    .strip(" .?!,")
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
                    .rstrip(".,?!")
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
BOOK_SERVICE
SHOPPING_SEARCH
SHOPPING_COMPARE
SHOPPING_CART_ADD
SHOPPING_CART_LIST
SHOPPING_PURCHASE_PREPARE
MANAGE_FILE
OPEN_APPLICATION
BROWSE_WEB
GENERAL_QUERY

IMPORTANT RULES:

1. Questions asking for factual or informational
knowledge should normally use SEARCH_INFORMATION.

2. Requests that explicitly ask to search for
information should use SEARCH_INFORMATION.

3. Requests to open Google, Chrome, YouTube,
a browser, or a website should use BROWSE_WEB.

4. Browser interaction requests should use BROWSE_WEB.

5. MULTI-STEP BROWSER COMMANDS:

If the user requests multiple browser actions
in one command, return a "steps" list.

6. Do NOT classify an ordinary factual question
as BROWSE_WEB.

7. Do NOT classify an ordinary factual question
as OPEN_APPLICATION.

8. For CREATE_TASK, task_name is required.

9. For CREATE_REMINDER, return the reminder text.

10. For SET_TIMER, return duration.

The duration should be in minutes unless another
unit is clearly specified.

11. For GET_WEATHER, return the city.

12. For SEARCH_INFORMATION, return the query.

13. For OPEN_APPLICATION, return application
and action.

14. For BROWSE_WEB, return action and URL.

15. For SEND_EMAIL, return recipient, subject,
and message.

16. CALENDAR RULES:

Any request to create, add, schedule, book,
or arrange an event in a calendar MUST use:

CHECK_CALENDAR

Examples:

"Create a calendar event titled AI Buddy Test on 2026-09-20 at 17:00 for 30 minutes"

"Schedule a meeting tomorrow at 10 AM"

"Add a doctor appointment to my calendar on Friday"

"Book an AI Buddy meeting for tomorrow at 5 PM"

For CHECK_CALENDAR return:

{{
    "intent": "CHECK_CALENDAR",
    "confidence": 0.99,
    "parameters": {{
        "title": "event title",
        "date": "YYYY-MM-DD",
        "time": "HH:MM",
        "details": "",
        "duration_minutes": 30
    }}
}}

IMPORTANT:

- "tomorrow" means the next calendar date.
- "today" means the current calendar date.
- Convert relative dates into YYYY-MM-DD when possible.
- Convert AM/PM times into 24-hour HH:MM format.
- Do NOT include words such as "tomorrow", "today",
  "at 10 AM", or "for 30 minutes" inside the title.
- The title must contain ONLY the event title.
- If duration is not specified, do not invent one.
- If details are not specified, use an empty string.
- A request to CREATE an event is still CHECK_CALENDAR.
- Do not classify a calendar event creation request
  as SEARCH_INFORMATION or GENERAL_QUERY.

17. BOOKING RULES:

Requests to make a reservation, appointment,
service booking, hotel booking, cab/taxi booking,
ride booking, flight booking, ticket booking,
restaurant/table reservation, or similar booking
should use:

BOOK_SERVICE

Examples:

"Book an appointment tomorrow at 11 AM"

"Create a booking for a service on 2026-09-20 at 15:00"

"Book a cab for tomorrow at 10 AM"

"Reserve a table for tonight"

For BOOK_SERVICE return:

{{
    "intent": "BOOK_SERVICE",
    "confidence": 0.98,
    "parameters": {{
        "service": "service or booking description",
        "date": "YYYY-MM-DD",
        "time": "HH:MM",
        "details": ""
    }}
}}

IMPORTANT:

- "tomorrow" means the next calendar date.
- "today" means the current calendar date.
- Convert relative dates into YYYY-MM-DD when possible.
- Convert AM/PM time into 24-hour HH:MM.
- Do not invent a date or time if the user did not provide one.
- Do not confuse calendar meetings/events with external
  service bookings.
- Calendar meetings/events MUST remain CHECK_CALENDAR.
- External reservations/bookings MUST use BOOK_SERVICE.

18. SHOPPING RULES:

Requests to search for products should use:

SHOPPING_SEARCH

Examples:

"Search for a mouse"

"Find a wireless keyboard"

"Search for laptop"

"Look for headphones"

For SHOPPING_SEARCH return:

{{
    "intent": "SHOPPING_SEARCH",
    "confidence": 0.97,
    "parameters": {{
        "query": "product search query"
    }}
}}

19. SHOPPING COMPARISON:

Requests to compare products should use:

SHOPPING_COMPARE

Examples:

"Compare P001 and P002"

"Compare these products P001 P002"

"Compare the two products"

For SHOPPING_COMPARE return:

{{
    "intent": "SHOPPING_COMPARE",
    "confidence": 0.98,
    "parameters": {{
        "products": ["P001", "P002"]
    }}
}}

20. SHOPPING CART:

Requests to add a product to the shopping cart
should use:

SHOPPING_CART_ADD

Examples:

"Add P001 to my cart"

"Put P001 in my cart"

"Add P001 to cart quantity 2"

For SHOPPING_CART_ADD return:

{{
    "intent": "SHOPPING_CART_ADD",
    "confidence": 0.98,
    "parameters": {{
        "product_id": "P001",
        "quantity": 1
    }}
}}

21. SHOPPING CART LIST:

Requests to view or list the shopping cart
should use:

SHOPPING_CART_LIST

Examples:

"Show my cart"

"View my shopping cart"

"What's in my cart?"

For SHOPPING_CART_LIST return:

{{
    "intent": "SHOPPING_CART_LIST",
    "confidence": 0.98,
    "parameters": {{}}
}}

22. SHOPPING PURCHASE:

Requests to prepare checkout, purchase, buy,
or order a product should use:

SHOPPING_PURCHASE_PREPARE

Examples:

"Prepare my purchase"

"Prepare my order"

"Proceed to checkout"

"Prepare checkout"

"Buy wireless mouse"

"Purchase a laptop"

"Order mechanical keyboard"

For SHOPPING_PURCHASE_PREPARE return:

{{
    "intent": "SHOPPING_PURCHASE_PREPARE",
    "confidence": 0.98,
    "parameters": {{}}
}}

IMPORTANT:

- Preparing a purchase is NOT the same as completing a purchase.
- Never claim that a real purchase was completed.
- The purchase preparation step must remain confirmation-based.
- Never bypass user confirmation.
- Do not request or expose payment credentials.
- Do not invent product IDs.
- Product IDs should normally look like P001, P002, etc.

23. Always return required parameters when
the intent needs them.

24. Always return ONLY valid JSON.

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
        # FAST LOCAL CALENDAR DETECTION
        # =====================================

        try:

            lower_message = message.lower()

            calendar_command = any(
                re.search(
                    pattern,
                    lower_message
                )
                for pattern in [
                    r"\bcalendar\s+event\b",
                    r"\bcreate\s+(?:a\s+)?event\b",
                    r"\bcreate\s+(?:a\s+)?calendar\b",
                    r"\badd\s+(?:a\s+)?event\b",
                    r"\bschedule\s+(?:a\s+)?event\b",
                    r"\bschedule\s+(?:a\s+)?meeting\b",
                    r"\bbook\s+(?:a\s+)?event\b",
                    r"\badd\s+.*\bcalendar\b"
                ]
            )

            if calendar_command:

                local_calendar_result = (
                    self._local_detect(
                        message
                    )
                )

                if (
                    local_calendar_result.get(
                        "intent"
                    )
                    == "CHECK_CALENDAR"
                ):

                    return self._validate_result(
                        local_calendar_result
                    )

        except Exception as error:

            print(
                "⚠️ Local calendar detection failed:"
            )

            print(
                f"Error: {error}"
            )

        # =====================================
        # FAST LOCAL BOOKING DETECTION
        # =====================================

        try:

            booking_command = any(
                re.search(
                    pattern,
                    message.lower()
                )
                for pattern in [
                    r"\bbook\s+(?:an?\s+)?"
                    r"(?:appointment|reservation|service)\b",

                    r"\bcreate\s+(?:a\s+)?booking\b",

                    r"\bmake\s+(?:a\s+)?booking\b",

                    r"\bbook\s+(?:a\s+)?"
                    r"(?:cab|taxi|ride|hotel|flight|"
                    r"ticket|restaurant|table)\b"
                ]
            )

            if booking_command:

                local_booking_result = (
                    self._local_detect(
                        message
                    )
                )

                if (
                    local_booking_result.get(
                        "intent"
                    )
                    == "BOOK_SERVICE"
                ):

                    return self._validate_result(
                        local_booking_result
                    )

        except Exception as error:

            print(
                "⚠️ Local booking detection failed:"
            )

            print(
                f"Error: {error}"
            )

        # =====================================
        # FAST LOCAL SHOPPING DETECTION
        # =====================================

        try:

            lower_message = message.lower()

            shopping_command = any(
                re.search(
                    pattern,
                    lower_message
                )
                for pattern in [

                    # ---------------------------------
                    # Search
                    # ---------------------------------

                    r"\bsearch\s+(?:for\s+)?"
                    r"(?:a\s+|an\s+|the\s+)?"
                    r"(?:product\s+)?"
                    r"(?:mouse|keyboard|laptop|phone|"
                    r"mobile|headphones?|earphones?|"
                    r"monitor|tablet|charger|product)\b",

                    r"\bfind\s+(?:a\s+|an\s+|the\s+)?"
                    r"(?:product\s+)?"
                    r"(?:mouse|keyboard|laptop|phone|"
                    r"mobile|headphones?|earphones?|"
                    r"monitor|tablet|charger|product)\b",

                    r"\bshop\s+for\b",

                    # ---------------------------------
                    # Compare
                    # ---------------------------------

                    r"\bcompare\b.*\bp\d+\b",

                    r"\bcompare\b.*\bproducts?\b",

                    r"\bcompare\b.*\bitems?\b",

                    # ---------------------------------
                    # Cart Add
                    # ---------------------------------

                    r"\badd\b.*\bp\d+\b.*"
                    r"\b(?:cart|basket)\b",

                    r"\badd\b.*\b(?:cart|basket)\b.*"
                    r"\bp\d+\b",

                    r"\bput\b.*\bp\d+\b.*"
                    r"\b(?:cart|basket)\b",

                    r"\bput\b.*\b(?:cart|basket)\b.*"
                    r"\bp\d+\b",

                    # ---------------------------------
                    # Cart List
                    # ---------------------------------

                    r"\bshow\b.*\b(?:my\s+)?cart\b",

                    r"\bview\b.*\b(?:my\s+)?cart\b",

                    r"\bget\b.*\b(?:my\s+)?cart\b",

                    r"\blist\b.*\b(?:my\s+)?cart\b",

                    r"\bwhat(?:'s| is)\b.*"
                    r"\bin\s+(?:my\s+)?cart\b",

                    r"\bshow\b.*\bbasket\b",

                    # ---------------------------------
                    # Purchase Preparation
                    # ---------------------------------

                    r"\bprepare\b.*\bpurchase\b",

                    r"\bprepare\b.*\border\b",

                    r"\bprepare\b.*\bcheckout\b",

                    r"\bproceed\b.*\bcheckout\b",

                    r"\bcheckout\b",

                    r"\bprepare\b.*\bbuy\b",

                    # Direct purchase commands
                    r"\bbuy\b.*\b(?:mouse|keyboard|laptop|phone|"
                    r"mobile|headphones?|earphones?|monitor|tablet|"
                    r"charger|product|item)\b",

                    r"\bpurchase\b.*\b(?:mouse|keyboard|laptop|phone|"
                    r"mobile|headphones?|earphones?|monitor|tablet|"
                    r"charger|product|item)\b",

                    r"\border\b.*\b(?:mouse|keyboard|laptop|phone|"
                    r"mobile|headphones?|earphones?|monitor|tablet|"
                    r"charger|product|item)\b"
                ]
            )

            if shopping_command:

                local_shopping_result = (
                    self._local_detect(
                        message
                    )
                )

                shopping_intents = {
                    "SHOPPING_SEARCH",
                    "SHOPPING_COMPARE",
                    "SHOPPING_CART_ADD",
                    "SHOPPING_CART_LIST",
                    "SHOPPING_PURCHASE_PREPARE"
                }

                if (
                    local_shopping_result.get(
                        "intent"
                    )
                    in shopping_intents
                ):

                    return self._validate_result(
                        local_shopping_result
                    )

        except Exception as error:

            print(
                "⚠️ Local shopping detection failed:"
            )

            print(
                f"Error: {error}"
            )

            return self._validate_result(
                self._local_detect(
                    message
                )
            )