from datetime import datetime
from uuid import uuid4

from app.integrations.base import BaseIntegration


class ShoppingProvider(BaseIntegration):

    def __init__(self):

        super().__init__(
            name="shopping",
            description=(
                "Shopping service integration for product search, "
                "comparison, cart management, and purchase preparation."
            )
        )

        self.connected = False

        # Temporary local product catalogue.
        # Real shopping APIs will be connected later.
        self.products = [
            {
                "product_id": "P001",
                "name": "Wireless Mouse",
                "category": "electronics",
                "price": 799.0,
                "currency": "INR",
                "available": True
            },
            {
                "product_id": "P002",
                "name": "Mechanical Keyboard",
                "category": "electronics",
                "price": 2499.0,
                "currency": "INR",
                "available": True
            },
            {
                "product_id": "P003",
                "name": "USB-C Fast Charger",
                "category": "electronics",
                "price": 1299.0,
                "currency": "INR",
                "available": True
            },
            {
                "product_id": "P004",
                "name": "Laptop Stand",
                "category": "accessories",
                "price": 999.0,
                "currency": "INR",
                "available": True
            }
        ]

        # Temporary in-memory cart store.
        # Structure:
        # {
        #     user_id: [
        #         {
        #             "cart_item_id": "...",
        #             "product_id": "...",
        #             "product": {...},
        #             "quantity": 1,
        #             "added_at": "..."
        #         }
        #     ]
        # }
        self.carts = {}

    # =========================================
    # STATUS
    # =========================================

    def get_status(self) -> dict:

        total_cart_items = sum(
            len(items)
            for items in self.carts.values()
        )

        return {
            "name": self.name,
            "description": self.description,
            "connected": self.connected,
            "available": self.is_available(),
            "status": (
                "connected"
                if self.connected
                else "disconnected"
            ),
            "product_count": len(self.products),
            "cart_item_count": total_cart_items
        }

    # =========================================
    # CONNECTION
    # =========================================

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

    # =========================================
    # VALIDATION
    # =========================================

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

    def _validate_user_id(
        self,
        user_id
    ) -> int:

        try:

            user_id = int(user_id)

        except (
            TypeError,
            ValueError
        ):

            raise ValueError(
                "User ID must be a valid integer."
            )

        if user_id <= 0:

            raise ValueError(
                "User ID must be greater than zero."
            )

        return user_id

    def _validate_quantity(
        self,
        quantity
    ) -> int:

        try:

            quantity = int(quantity)

        except (
            TypeError,
            ValueError
        ):

            raise ValueError(
                "Quantity must be a valid integer."
            )

        if quantity <= 0:

            raise ValueError(
                "Quantity must be greater than zero."
            )

        return quantity

    # =========================================
    # PRODUCT SEARCH
    # =========================================

    def _search_products(
        self,
        query: str
    ) -> dict:

        try:

            query = self._validate_text(
                query,
                "Search query"
            )

        except (
            TypeError,
            ValueError
        ) as error:

            return {
                "success": False,
                "message": str(error)
            }

        query_lower = query.lower()

        matched_products = [
            product
            for product in self.products
            if (
                query_lower in product["name"].lower()
                or query_lower in product["category"].lower()
            )
        ]

        return {
            "success": True,
            "status": "completed",
            "action": "search",
            "query": query,
            "products": matched_products,
            "count": len(matched_products),
            "message": (
                "Product search completed successfully."
            )
        }

    # =========================================
    # PRODUCT COMPARISON
    # =========================================

    def _compare_products(
        self,
        products
    ) -> dict:

        if not isinstance(
            products,
            list
        ):

            return {
                "success": False,
                "message": (
                    "Products must be provided as a list."
                )
            }

        if not products:

            return {
                "success": False,
                "message": (
                    "At least one product is required."
                )
            }

        comparison_products = []

        for item in products:

            if isinstance(
                item,
                dict
            ):

                product_id = item.get(
                    "product_id",
                    ""
                )

                product_name = item.get(
                    "name",
                    ""
                )

            else:

                product_id = str(item)
                product_name = ""

            matched_product = None

            for product in self.products:

                if (
                    product_id
                    and product["product_id"]
                    == product_id
                ):

                    matched_product = product
                    break

                if (
                    product_name
                    and product["name"].lower()
                    == product_name.lower()
                ):

                    matched_product = product
                    break

            if matched_product is not None:

                comparison_products.append(
                    matched_product
                )

        if not comparison_products:

            return {
                "success": False,
                "message": (
                    "No matching products found."
                )
            }

        sorted_products = sorted(
            comparison_products,
            key=lambda product: product["price"]
        )

        return {
            "success": True,
            "status": "completed",
            "action": "compare",
            "products": sorted_products,
            "count": len(sorted_products),
            "message": (
                "Product comparison completed successfully."
            )
        }

    # =========================================
    # FIND PRODUCT
    # =========================================

    def _find_product(
        self,
        product_id: str
    ):

        for product in self.products:

            if product["product_id"] == product_id:

                return product

        return None

    # =========================================
    # ADD TO CART
    # =========================================

    def _add_to_cart(
        self,
        user_id: int,
        parameters: dict
    ) -> dict:

        product_id = parameters.get(
            "product_id",
            ""
        )

        try:

            product_id = self._validate_text(
                product_id,
                "Product ID"
            )

        except (
            TypeError,
            ValueError
        ) as error:

            return {
                "success": False,
                "message": str(error)
            }

        try:

            quantity = self._validate_quantity(
                parameters.get(
                    "quantity",
                    1
                )
            )

        except ValueError as error:

            return {
                "success": False,
                "message": str(error)
            }

        product = self._find_product(
            product_id
        )

        if product is None:

            return {
                "success": False,
                "message": "Product was not found."
            }

        if not product["available"]:

            return {
                "success": False,
                "message": "Product is currently unavailable."
            }

        if user_id not in self.carts:

            self.carts[user_id] = []

        user_cart = self.carts[user_id]

        for item in user_cart:

            if item["product_id"] == product_id:

                item["quantity"] += quantity

                return {
                    "success": True,
                    "status": "added",
                    "action": "cart_add",
                    "cart_item": item,
                    "message": (
                        "Product quantity updated in cart."
                    )
                }

        cart_item = {
            "cart_item_id": str(uuid4()),
            "product_id": product_id,
            "product": product,
            "quantity": quantity,
            "added_at": datetime.utcnow().isoformat()
        }

        user_cart.append(
            cart_item
        )

        return {
            "success": True,
            "status": "added",
            "action": "cart_add",
            "cart_item": cart_item,
            "message": (
                "Product added to cart successfully."
            )
        }

    # =========================================
    # VIEW CART
    # =========================================

    def _get_cart(
        self,
        user_id: int
    ) -> dict:

        user_cart = self.carts.get(
            user_id,
            []
        )

        total = sum(
            item["product"]["price"]
            * item["quantity"]
            for item in user_cart
        )

        return {
            "success": True,
            "status": "listed",
            "action": "cart_list",
            "user_id": user_id,
            "items": user_cart,
            "count": len(user_cart),
            "total": total,
            "currency": "INR",
            "message": (
                "Shopping cart retrieved successfully."
            )
        }

    # =========================================
    # REMOVE FROM CART
    # =========================================

    def _remove_from_cart(
        self,
        user_id: int,
        parameters: dict
    ) -> dict:

        product_id = parameters.get(
            "product_id",
            ""
        )

        try:

            product_id = self._validate_text(
                product_id,
                "Product ID"
            )

        except (
            TypeError,
            ValueError
        ) as error:

            return {
                "success": False,
                "message": str(error)
            }

        user_cart = self.carts.get(
            user_id,
            []
        )

        for index, item in enumerate(
            user_cart
        ):

            if item["product_id"] == product_id:

                removed_item = user_cart.pop(
                    index
                )

                return {
                    "success": True,
                    "status": "removed",
                    "action": "cart_remove",
                    "cart_item": removed_item,
                    "message": (
                        "Product removed from cart successfully."
                    )
                }

        return {
            "success": False,
            "message": (
                "Product was not found in your cart."
            )
        }

    # =========================================
    # PURCHASE PREPARATION
    # =========================================

    def _prepare_purchase(
        self,
        user_id: int
    ) -> dict:

        user_cart = self.carts.get(
            user_id,
            []
        )

        if not user_cart:

            return {
                "success": False,
                "message": (
                    "Your shopping cart is empty."
                )
            }

        total = sum(
            item["product"]["price"]
            * item["quantity"]
            for item in user_cart
        )

        return {
            "success": True,
            "status": "prepared",
            "action": "purchase",
            "user_id": user_id,
            "items": user_cart,
            "total": total,
            "currency": "INR",
            "requires_confirmation": True,
            "message": (
                "Purchase prepared. "
                "User confirmation is required before "
                "any real purchase is attempted."
            )
        }

    # =========================================
    # MAIN EXECUTION
    # =========================================

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

        try:

            user_id = self._validate_user_id(
                parameters.get("user_id")
            )

        except ValueError as error:

            return {
                "success": False,
                "message": str(error)
            }

        if action == "search":

            query = parameters.get(
                "query",
                parameters.get(
                    "product",
                    ""
                )
            )

            return self._search_products(
                query
            )

        if action == "compare":

            products = parameters.get(
                "products",
                []
            )

            return self._compare_products(
                products
            )

        if action in (
            "cart_add",
            "add_to_cart",
            "cart"
        ):

            return self._add_to_cart(
                user_id=user_id,
                parameters=parameters
            )

        if action in (
            "cart_list",
            "list_cart"
        ):

            return self._get_cart(
                user_id=user_id
            )

        if action in (
            "cart_remove",
            "remove_from_cart"
        ):

            return self._remove_from_cart(
                user_id=user_id,
                parameters=parameters
            )

        if action in (
            "purchase",
            "buy"
        ):

            return self._prepare_purchase(
                user_id=user_id
            )

        return {
            "success": False,
            "message": (
                f"Unsupported shopping action: {action}"
            )
        }