class ReasoningEngine:

    # =========================================
    # EXECUTABLE INTENTS
    # =========================================

    EXECUTABLE_INTENTS = {
        "STOP",
        "SET_TIMER",
        "CREATE_TASK",
        "CREATE_REMINDER",
        "GET_WEATHER",
        "GET_TIME",
        "GET_DATE",
        "OPEN_APPLICATION",
        "SEARCH_INFORMATION",
        "SEND_EMAIL",
        "BROWSE_WEB",
        "CHECK_CALENDAR",
        "BOOK_SERVICE",

        # Shopping
        "SHOPPING_SEARCH",
        "SHOPPING_COMPARE",
        "SHOPPING_CART_ADD",
        "SHOPPING_CART_REMOVE",
        "SHOPPING_CART_LIST",
        "SHOPPING_PURCHASE_PREPARE"
    }

    # =========================================
    # FUTURE INTENTS
    # =========================================

    FUTURE_INTENTS = {
        "BOOK_RIDE",
        "SHOP_ONLINE",
        "POST_SOCIAL_MEDIA",
        "SUBMIT_ASSIGNMENT"
    }

    # =========================================
    # EXPECTED TOOLS
    # =========================================

    EXPECTED_TOOLS = {
        "STOP": "stop",
        "SET_TIMER": "timer",
        "CREATE_TASK": "task",
        "CREATE_REMINDER": "reminder",
        "GET_WEATHER": "weather",
        "GET_TIME": "time_tool",
        "GET_DATE": "time_tool",
        "OPEN_APPLICATION": "application_launcher",
        "SEARCH_INFORMATION": "search",
        "SEND_EMAIL": "email",
        "BROWSE_WEB": "browser",
        "CHECK_CALENDAR": "calendar",
        "BOOK_SERVICE": "booking",

        # Shopping
        "SHOPPING_SEARCH": "shopping",
        "SHOPPING_COMPARE": "shopping",
        "SHOPPING_CART_ADD": "shopping",
        "SHOPPING_CART_REMOVE": "shopping",
        "SHOPPING_CART_LIST": "shopping",
        "SHOPPING_PURCHASE_PREPARE": "shopping"
    }

    # =========================================
    # REQUIRED PARAMETERS
    # =========================================

    REQUIRED_PARAMETERS = {
        "SET_TIMER": [
            "duration_seconds"
        ],

        "CREATE_TASK": [
            "task_name"
        ],

        "CREATE_REMINDER": [
            "reminder"
        ],

        "GET_WEATHER": [
            "city"
        ],

        "OPEN_APPLICATION": [
            "application"
        ],

        "SEARCH_INFORMATION": [
            "query"
        ],

        "SEND_EMAIL": [
            "recipient",
            "subject",
            "message"
        ],

        "BROWSE_WEB": [
            "action"
        ],

        "CHECK_CALENDAR": [
            "title",
            "date",
            "time"
        ],

        # =====================================
        # SHOPPING
        # =====================================

        "SHOPPING_SEARCH": [
            "query"
        ],

        "SHOPPING_COMPARE": [
            "products"
        ],

        "SHOPPING_CART_ADD": [
            "product_id"
        ],

        "SHOPPING_CART_REMOVE": [
            "product_id"
        ],

        "SHOPPING_CART_LIST": [],

        "SHOPPING_PURCHASE_PREPARE": []
    }

    # =========================================
    # REASON
    # =========================================

    def reason(
        self,
        intent: str,
        plan: dict | None = None
    ) -> dict:

        # =========================================
        # VALIDATE INTENT
        # =========================================

        if not isinstance(
            intent,
            str
        ):

            return {
                "success": False,
                "intent": "UNKNOWN",
                "executable": False,
                "message": "Intent must be a string."
            }

        intent = (
            intent
            .strip()
            .upper()
        )

        if not intent:

            return {
                "success": False,
                "intent": "UNKNOWN",
                "executable": False,
                "message": "Intent cannot be empty."
            }

        # =========================================
        # FUTURE INTENTS
        # =========================================

        if intent in self.FUTURE_INTENTS:

            return {
                "success": True,
                "intent": intent,
                "executable": False,
                "message": (
                    f"Intent '{intent}' is recognised "
                    "but its execution is not "
                    "available yet."
                )
            }

        # =========================================
        # UNKNOWN / NON-EXECUTABLE INTENTS
        # =========================================

        if intent not in self.EXECUTABLE_INTENTS:

            return {
                "success": True,
                "intent": intent,
                "executable": False,
                "message": (
                    f"Intent '{intent}' cannot be "
                    "executed by the current system."
                )
            }

        # =========================================
        # VALIDATE PLAN
        # =========================================

        if not isinstance(
            plan,
            dict
        ):

            return {
                "success": False,
                "intent": intent,
                "executable": False,
                "message": (
                    "Execution plan must be "
                    "a dictionary."
                )
            }

        tool = plan.get(
            "tool"
        )

        parameters = plan.get(
            "parameters",
            {}
        )

        if not isinstance(
            parameters,
            dict
        ):

            parameters = {}

        # =========================================
        # VALIDATE EXPECTED TOOL
        # =========================================

        expected_tool = (
            self.EXPECTED_TOOLS.get(
                intent
            )
        )

        if tool != expected_tool:

            return {
                "success": False,
                "intent": intent,
                "executable": False,
                "expected_tool": expected_tool,
                "received_tool": tool,
                "message": (
                    f"Intent '{intent}' requires "
                    f"tool '{expected_tool}'."
                )
            }

        # =========================================
        # REQUIRED PARAMETERS
        # =========================================

        required_parameters = (
            self.REQUIRED_PARAMETERS.get(
                intent,
                []
            )
        )

        missing_parameters = []

        for parameter in required_parameters:

            # -------------------------------------
            # TIMER SPECIAL CASE
            # -------------------------------------

            if (
                intent == "SET_TIMER"
                and parameter == "duration_seconds"
            ):

                value = parameters.get(
                    "duration_seconds"
                )

                if value is None:

                    value = parameters.get(
                        "duration"
                    )

            else:

                value = parameters.get(
                    parameter
                )

            # -------------------------------------
            # CHECK MISSING VALUE
            # -------------------------------------

            if value is None:

                missing_parameters.append(
                    parameter
                )

            elif (
                isinstance(
                    value,
                    str
                )
                and not value.strip()
            ):

                missing_parameters.append(
                    parameter
                )

        # =========================================
        # SHOPPING VALIDATION
        # =========================================

        if intent == "SHOPPING_SEARCH":

            query = parameters.get(
                "query"
            )

            if (
                not isinstance(
                    query,
                    str
                )
                or not query.strip()
            ):

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "Shopping search query "
                        "is required."
                    )
                }

            parameters["query"] = query.strip()

        # =========================================
        # SHOPPING COMPARE VALIDATION
        # =========================================

        if intent == "SHOPPING_COMPARE":

            products = parameters.get(
                "products"
            )

            if not isinstance(
                products,
                list
            ):

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "Products must be provided "
                        "as a list."
                    )
                }

            if not products:

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "At least one product is "
                        "required for comparison."
                    )
                }

            cleaned_products = []

            for product in products:

                if isinstance(
                    product,
                    str
                ):

                    product = product.strip()

                    if product:

                        cleaned_products.append(
                            product
                        )

                elif isinstance(
                    product,
                    dict
                ):

                    cleaned_products.append(
                        product
                    )

            if not cleaned_products:

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "No valid products were "
                        "provided for comparison."
                    )
                }

            parameters[
                "products"
            ] = cleaned_products

        # =========================================
        # SHOPPING CART ADD VALIDATION
        # =========================================

        if intent == "SHOPPING_CART_ADD":

            product_id = parameters.get(
                "product_id"
            )

            if (
                not isinstance(
                    product_id,
                    str
                )
                or not product_id.strip()
            ):

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "Product ID is required "
                        "to add a product to the cart."
                    )
                }

            parameters[
                "product_id"
            ] = product_id.strip()

            quantity = parameters.get(
                "quantity",
                1
            )

            try:

                quantity = int(
                    quantity
                )

            except (
                TypeError,
                ValueError
            ):

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "Shopping quantity must "
                        "be a valid integer."
                    )
                }

            if quantity <= 0:

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "Shopping quantity must "
                        "be greater than zero."
                    )
                }

            parameters[
                "quantity"
            ] = quantity

        # =========================================
        # SHOPPING CART REMOVE VALIDATION
        # =========================================

        if intent == "SHOPPING_CART_REMOVE":

            product_id = parameters.get(
                "product_id"
            )

            if (
                not isinstance(
                    product_id,
                    str
                )
                or not product_id.strip()
            ):

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "Product ID is required "
                        "to remove a product from the cart."
                    )
                }

            parameters[
                "product_id"
            ] = product_id.strip()

        # =========================================
        # SHOPPING CART LIST VALIDATION
        # =========================================

        if intent == "SHOPPING_CART_LIST":

            # No special parameters required.
            parameters = {}

        # =========================================
        # SHOPPING PURCHASE PREPARATION
        # =========================================

        if intent == "SHOPPING_PURCHASE_PREPARE":

            # -------------------------------------
            # IMPORTANT SECURITY RULE
            # -------------------------------------
            # This intent only prepares the purchase.
            # It does NOT perform a real purchase.

            parameters = {}

        # =========================================
        # CALENDAR VALIDATION
        # =========================================

        if intent == "CHECK_CALENDAR":

            title = parameters.get(
                "title"
            )

            date = parameters.get(
                "date"
            )

            time = parameters.get(
                "time"
            )

            # -------------------------------------
            # TITLE
            # -------------------------------------

            if (
                not isinstance(
                    title,
                    str
                )
                or not title.strip()
            ):

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "Calendar event title "
                        "is required."
                    )
                }

            # -------------------------------------
            # DATE
            # -------------------------------------

            if (
                not isinstance(
                    date,
                    str
                )
                or not date.strip()
            ):

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "Calendar event date "
                        "is required."
                    )
                }

            # -------------------------------------
            # DATE FORMAT
            # -------------------------------------

            if not re_match_date(
                date
            ):

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "Calendar event date must "
                        "use YYYY-MM-DD format."
                    )
                }

            # -------------------------------------
            # TIME
            # -------------------------------------

            if (
                not isinstance(
                    time,
                    str
                )
                or not time.strip()
            ):

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "Calendar event time "
                        "is required."
                    )
                }

            # -------------------------------------
            # TIME FORMAT
            # -------------------------------------

            if not re_match_time(
                time
            ):

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "Calendar event time must "
                        "use HH:MM format."
                    )
                }

            # -------------------------------------
            # DURATION
            # -------------------------------------

            duration = parameters.get(
                "duration_minutes"
            )

            if duration is not None:

                try:

                    duration = int(
                        duration
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    return {
                        "success": False,
                        "intent": intent,
                        "executable": False,
                        "message": (
                            "Calendar event duration "
                            "must be a number."
                        )
                    }

                if duration <= 0:

                    return {
                        "success": False,
                        "intent": intent,
                        "executable": False,
                        "message": (
                            "Calendar event duration "
                            "must be greater than zero."
                        )
                    }

                parameters[
                    "duration_minutes"
                ] = duration

            # -------------------------------------
            # DETAILS
            # -------------------------------------

            details = parameters.get(
                "details",
                ""
            )

            if details is None:

                parameters[
                    "details"
                ] = ""

            elif not isinstance(
                details,
                str
            ):

                parameters[
                    "details"
                ] = str(
                    details
                )

        # =========================================
        # BROWSER VALIDATION
        # =========================================

        if intent == "BROWSE_WEB":

            action = parameters.get(
                "action"
            )

            # -------------------------------------
            # ACTION REQUIRED
            # -------------------------------------

            if (
                not isinstance(
                    action,
                    str
                )
                or not action.strip()
            ):

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        "Browser action is required."
                    )
                }

            action = (
                action
                .strip()
                .lower()
            )

            # -------------------------------------
            # ALLOWED ACTIONS
            # -------------------------------------

            allowed_browser_actions = {
                "open",
                "navigate",
                "click",
                "fill",
                "read",
                "download",
                "close"
            }

            if action not in allowed_browser_actions:

                return {
                    "success": False,
                    "intent": intent,
                    "executable": False,
                    "message": (
                        f"Unsupported browser "
                        f"action '{action}'."
                    )
                }

            # -------------------------------------
            # URL / WEBSITE DISCOVERY REQUIREMENT
            # -------------------------------------

            if action in {
                "open",
                "navigate"
            }:

                url = parameters.get(
                    "url"
                )

                website_name = parameters.get(
                    "website_name"
                )

                page_target = parameters.get(
                    "page_target"
                )

                # ---------------------------------
                # CHECK EXPLICIT URL
                # ---------------------------------

                has_url = (
                    isinstance(
                        url,
                        str
                    )
                    and bool(
                        url.strip()
                    )
                )

                # ---------------------------------
                # CHECK WEBSITE NAME
                # ---------------------------------

                has_website_name = (
                    isinstance(
                        website_name,
                        str
                    )
                    and bool(
                        website_name.strip()
                    )
                )

                # ---------------------------------
                # CHECK PAGE TARGET
                # ---------------------------------

                has_page_target = (
                    isinstance(
                        page_target,
                        str
                    )
                    and bool(
                        page_target.strip()
                    )
                )

                # ---------------------------------
                # DIRECT URL ROUTE
                #
                # Example:
                # https://www.codewithharry.com/
                #
                # Existing direct URL behavior
                # remains unchanged.
                # ---------------------------------

                if has_url:

                    parameters[
                        "url"
                    ] = url.strip()

                # ---------------------------------
                # GENERIC WEBSITE DISCOVERY ROUTE
                #
                # Example:
                #
                # website_name = "GeeksforGeeks"
                # page_target = "Ring Topology"
                #
                # BrowserTool will pass these
                # values to WebsiteDiscovery.
                #
                # WebsiteDiscovery
                #        ↓
                # SearchTool
                #        ↓
                # Actual website URL
                # ---------------------------------

                elif (
                    has_website_name
                    or has_page_target
                ):

                    if has_website_name:

                        parameters[
                            "website_name"
                        ] = website_name.strip()

                    if has_page_target:

                        parameters[
                            "page_target"
                        ] = page_target.strip()

                    # Empty URL tells BrowserTool
                    # that URL discovery is required.

                    parameters[
                        "url"
                    ] = ""

                # ---------------------------------
                # NOTHING PROVIDED
                # ---------------------------------

                else:

                    return {
                        "success": False,
                        "intent": intent,
                        "executable": False,
                        "message": (
                            "URL or website information "
                            "is required for browser "
                            f"action '{action}'."
                        )
                    }

            # -------------------------------------
            # CURRENT PAGE ACTIONS
            # -------------------------------------

            elif action in {
                "click",
                "fill",
                "read",
                "download"
            }:

                if not parameters.get(
                    "url"
                ):

                    parameters[
                        "use_current_page"
                    ] = True

            # -------------------------------------
            # CLICK / FILL / DOWNLOAD
            # SELECTOR OR TARGET
            # -------------------------------------

            if action in {
                "click",
                "fill",
                "download"
            }:

                selector = parameters.get(
                    "selector"
                )

                target = parameters.get(
                    "target"
                )

                has_selector = (
                    isinstance(
                        selector,
                        str
                    )
                    and bool(
                        selector.strip()
                    )
                )

                has_target = (
                    isinstance(
                        target,
                        str
                    )
                    and bool(
                        target.strip()
                    )
                )

                if not has_selector and not has_target:

                    return {
                        "success": False,
                        "intent": intent,
                        "executable": False,
                        "message": (
                            f"Selector or target is "
                            f"required for browser "
                            f"action '{action}'."
                        )
                    }

                if has_selector:

                    parameters[
                        "selector"
                    ] = selector.strip()

                if has_target:

                    parameters[
                        "target"
                    ] = target.strip()

            # -------------------------------------
            # FILL VALUE
            # -------------------------------------

            if action == "fill":

                value = parameters.get(
                    "value"
                )

                if value is None:

                    return {
                        "success": False,
                        "intent": intent,
                        "executable": False,
                        "message": (
                            "Value is required for "
                            "browser fill action."
                        )
                    }

                if not isinstance(
                    value,
                    str
                ):

                    return {
                        "success": False,
                        "intent": intent,
                        "executable": False,
                        "message": (
                            "Browser fill value "
                            "must be text."
                        )
                    }

        # =========================================
        # MISSING PARAMETERS
        # =========================================

        if missing_parameters:

            return {
                "success": False,
                "intent": intent,
                "executable": False,
                "missing_parameters":
                    missing_parameters,
                "message": (
                    "Required parameters are missing: "
                    + ", ".join(
                        missing_parameters
                    )
                )
            }

        # =========================================
        # SUCCESS
        # =========================================

        return {
            "success": True,
            "intent": intent,
            "executable": True,
            "tool": tool,
            "parameters": parameters,
            "message": (
                f"Intent '{intent}' can be "
                f"executed using tool '{tool}'."
            )
        }

    # =========================================
    # CAN EXECUTE
    # =========================================

    def can_execute(
        self,
        intent: str
    ) -> bool:

        if not isinstance(
            intent,
            str
        ):

            return False

        return (
            intent.strip().upper()
            in self.EXECUTABLE_INTENTS
        )

    # =========================================
    # FUTURE INTENT CHECK
    # =========================================

    def is_future_intent(
        self,
        intent: str
    ) -> bool:

        if not isinstance(
            intent,
            str
        ):

            return False

        return (
            intent.strip().upper()
            in self.FUTURE_INTENTS
        )


# =============================================
# DATE VALIDATION HELPER
# =============================================

def re_match_date(
    value: str
) -> bool:

    import re

    return bool(
        re.fullmatch(
            r"20\d{2}-\d{2}-\d{2}",
            value.strip()
        )
    )


# =============================================
# TIME VALIDATION HELPER
# =============================================

def re_match_time(
    value: str
) -> bool:

    import re

    return bool(
        re.fullmatch(
            r"(?:[01]\d|2[0-3]):[0-5]\d",
            value.strip()
        )
    )