from tortoise.transactions import in_transaction
from app.app_models import User, Product
from app.cart import ShoppingCart, Product


async def create_user(full_name, email, phone, password):
    async with in_transaction():
        user = await User.create(full_name=full_name, email=email, phone=phone, password=password)
        return user


async def get_products(page=1, page_size=10):
    products = await Product.filter(is_active=True).limit(page_size).offset((page - 1) * page_size)
    return products


class CartService:
    def __init__(self):
        self.shopping_cart = ShoppingCart()

    def add_product_to_cart(self, product: Product):
        self.shopping_cart.add_product(product)

    def remove_product_from_cart(self, product: Product):
        self.shopping_cart.remove_product(product)

    def clear_cart(self):
        self.shopping_cart.clear_cart()

    def get_cart_total_price(self):
        return self.shopping_cart.get_total_price()