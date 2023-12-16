from fastapi import APIRouter, Depends
from app.app_services import CartService
from app.cart import Product as AppProduct
from pydantic import BaseModel

router = APIRouter()
cart_service = CartService()


class AddToCart(BaseModel):
    product_name: str


@router.post("/add-to-cart")
async def add_to_cart(product_data: AddToCart, cart_service: CartService = Depends()):
    product = AppProduct(name=product_data.product_name, price=10.0)
    cart_service.add_product_to_cart(product)
    return {"message": f"{product_data.product_name} добавлен в корзину"}


class RemoveFromCart(BaseModel):
    product_name: str


@router.post("/remove-from-cart")
async def remove_from_cart(product_data: RemoveFromCart, cart_service: CartService = Depends()):
    product = AppProduct(name=product_data.product_name, price=10.0)
    cart_service.remove_product_from_cart(product)
    return {"message": f"{product_data.product_name} удален из корзины"}


@router.post("/clear-cart")
async def clear_cart(cart_service: CartService = Depends()):
    cart_service.clear_cart()
    return {"message": "Корзина очищена"}


@router.get("/cart-total-price")
async def get_cart_total_price(cart_service: CartService = Depends()):
    total_price = cart_service.get_cart_total_price()
    return {"total_price": total_price}
