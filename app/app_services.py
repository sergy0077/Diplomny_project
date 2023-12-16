from tortoise.transactions import in_transaction
from app.app_models import User, Product
from app.cart import ShoppingCart, Product as AppProduct
from app.auth.auth_services import pwd_context


async def create_user(full_name, email, phone, password):
    async with in_transaction():
        hashed_password = pwd_context.hash(password)
        user = await User.create(full_name=full_name, email=email, phone=phone, password_hash=hashed_password)
        return user


async def create_product(name: str, price: float):
    product = Product(name=name, price=price)
    await product.save()
    return product


async def get_products(page: int, page_size: int):
    products = await Product.filter(is_active=True).limit(page_size).offset((page - 1) * page_size).all()
    return products


class CartService:
    def __init__(self):
        self.shopping_cart = ShoppingCart()

    def add_product_to_cart(self, product: AppProduct):
        self.shopping_cart.add_product(product)

    def remove_product_from_cart(self, product: AppProduct):
        self.shopping_cart.remove_product(product)

    def clear_cart(self):
        self.shopping_cart.clear_cart()

    def get_cart_total_price(self):
        return self.shopping_cart.get_total_price()