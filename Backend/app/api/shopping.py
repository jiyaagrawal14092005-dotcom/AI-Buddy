from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.integrations.shopping.provider import ShoppingProvider


router = APIRouter(
    prefix="/shopping",
    tags=["Shopping"]
)

shopping_provider = ShoppingProvider()


class ProductComparisonRequest(BaseModel):
    user_id: int = Field(
        ...,
        gt=0,
        description="ID of the user requesting product comparison."
    )
    products: list = Field(
        ...,
        min_length=1,
        description="List of product IDs or product names to compare."
    )


@router.get("/status")
def shopping_status():
    return {
        "success": True,
        "service": "shopping",
        "provider": shopping_provider.get_status()
    }


@router.post("/connect")
def connect_shopping():
    return shopping_provider.connect()


@router.post("/disconnect")
def disconnect_shopping():
    return shopping_provider.disconnect()


@router.get("/search")
def search_products(
    user_id: int,
    query: str
):
    return shopping_provider.execute(
        action="search",
        parameters={
            "user_id": user_id,
            "query": query
        }
    )


@router.post("/compare")
def compare_products(
    request: ProductComparisonRequest
):
    return shopping_provider.execute(
        action="compare",
        parameters={
            "user_id": request.user_id,
            "products": request.products
        }
    )


@router.post("/cart/add")
def add_to_cart(
    user_id: int,
    product_id: str,
    quantity: int = 1
):
    return shopping_provider.execute(
        action="cart_add",
        parameters={
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity
        }
    )


@router.get("/cart")
def get_cart(
    user_id: int
):
    return shopping_provider.execute(
        action="cart_list",
        parameters={
            "user_id": user_id
        }
    )


@router.delete("/cart/remove")
def remove_from_cart(
    user_id: int,
    product_id: str
):
    return shopping_provider.execute(
        action="cart_remove",
        parameters={
            "user_id": user_id,
            "product_id": product_id
        }
    )


@router.post("/purchase/prepare")
def prepare_purchase(
    user_id: int
):
    return shopping_provider.execute(
        action="purchase",
        parameters={
            "user_id": user_id
        }
    )