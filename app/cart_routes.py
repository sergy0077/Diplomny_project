from fastapi import APIRouter, Depends
from app.app_services import CartService, Product

router = APIRouter()
cart_service = CartService()


@router.post("/add-to-cart/{product_name}")
async def add_to_cart(product_name: str, cart_service: CartService = Depends()):
    product = Product(name=product_name, price=10.0)
    cart_service.add_product_to_cart(product)
    return {"message": f"{product_name} добавлен в корзину"}


@router.post("/remove-from-cart/{product_name}")
async def remove_from_cart(product_name: str, cart_service: CartService = Depends()):
    product = Product(name=product_name, price=10.0)
    cart_service.remove_product_from_cart(product)
    return {"message": f"{product_name} удален из корзины"}


@router.post("/clear-cart")
async def clear_cart(cart_service: CartService = Depends()):
    cart_service.clear_cart()
    return {"message": "Корзина очищена"}


@router.get("/cart-total-price")
async def get_cart_total_price(cart_service: CartService = Depends()):
    total_price = cart_service.get_cart_total_price()
    return {"total_price": total_price}
