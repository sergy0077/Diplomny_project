from typing import List


class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class ShoppingCart:
    def __init__(self):
        self.items: List[Product] = []

    def add_product(self, product: Product):
        self.items.append(product)

    def add_products(self, products: List[Product]):
        self.items.extend(products)

    def remove_product(self, product_name: str):
        self.items = [item for item in self.items if item.name != product_name]

    def clear_cart(self):
        self.items = []

    def get_total_price(self) -> float:
        return sum(product.price for product in self.items)
