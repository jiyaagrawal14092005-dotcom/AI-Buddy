from app.integrations.base import BaseIntegration


class ShoppingProvider(BaseIntegration):

    def __init__(self):

        super().__init__(
            name="shopping",
            description=(
                "Shopping service integration for preparing "
                "product search, comparison, and cart actions."
            )
        )

        self.connected = False

    def get_status(self) -> dict:

        return {
            "name": self.name,
            "description": self.description,
            "connected": self.connected,
            "available": self.is_available(),
            "status": (
                "connected"
                if self.connected
                else "disconnected"
            )
        }

    def connect(self) -> dict:

        self.connected = True

        return {
            "success": True,
            "connected": True,
            "message": (
                "Shopping provider connected successfully."
            )
        }

    def disconnect(self) -> dict:

        self.connected = False

        return {
            "success": True,
            "connected": False,
            "message": (
                "Shopping provider disconnected successfully."
            )
        }

    def is_available(self) -> bool:
        return self.connected

    def _validate_text(
        self,
        value: str,
        field_name: str
    ) -> str:

        if not isinstance(
            value,
            str
        ):
            raise TypeError(
                f"{field_name} must be a string."
            )

        value = value.strip()

        if not value:
            raise ValueError(
                f"{field_name} cannot be empty."
            )

        return value

    def execute(
        self,
        action: str,
        parameters: dict | None = None
    ) -> dict:

        if not isinstance(
            action,
            str
        ):
            return {
                "success": False,
                "message": "Action must be a string."
            }

        action = action.strip().lower()

        if not action:
            return {
                "success": False,
                "message": "Action cannot be empty."
            }

        if parameters is None:
            parameters = {}

        if not isinstance(
            parameters,
            dict
        ):
            return {
                "success": False,
                "message": (
                    "Shopping parameters "
                    "must be a dictionary."
                )
            }

        if not self.connected:
            return {
                "success": False,
                "message": (
                    "Shopping provider "
                    "is not connected."
                )
            }

        if action == "search":

            query = parameters.get(
                "query",
                parameters.get(
                    "product",
                    ""
                )
            )

            try:

                query = self._validate_text(
                    query,
                    "Search query"
                )

            except (
                TypeError,
                ValueError
            ) as e:

                return {
                    "success": False,
                    "message": str(e)
                }

            return {
                "success": True,
                "status": "prepared",
                "action": "search",
                "query": query,
                "message": (
                    "Product search action "
                    "prepared successfully."
                )
            }

        if action == "compare":

            products = parameters.get(
                "products",
                []
            )

            if not isinstance(
                products,
                list
            ):
                return {
                    "success": False,
                    "message": (
                        "Products must be provided "
                        "as a list."
                    )
                }

            if not products:
                return {
                    "success": False,
                    "message": (
                        "At least one product "
                        "is required."
                    )
                }

            return {
                "success": True,
                "status": "prepared",
                "action": "compare",
                "products": products,
                "message": (
                    "Product comparison action "
                    "prepared successfully."
                )
            }

        if action == "cart":

            product = parameters.get(
                "product",
                ""
            )

            try:

                product = self._validate_text(
                    product,
                    "Product"
                )

            except (
                TypeError,
                ValueError
            ) as e:

                return {
                    "success": False,
                    "message": str(e)
                }

            return {
                "success": True,
                "status": "prepared",
                "action": "cart",
                "product": product,
                "message": (
                    "Cart action prepared successfully."
                )
            }

        return {
            "success": False,
            "message": (
                f"Unsupported shopping action: {action}"
            )
        }