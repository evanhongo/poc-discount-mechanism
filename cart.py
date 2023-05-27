import json

from pos import Discount


class Product:
    def __init__(self, pid: int, sku: str, name: str, price: int, tags: list[str]):
        self.id = pid
        self.sku = sku
        self.name = name
        self.price = price
        self.tags = tags


class Cart:
    def __init__(self):
        # from pos import Discount

        self.purchasedProducts: list[Product] = []
        self.appliedDiscounts: list[Discount] = []
        self.totalPrice: int = 0

    def loadProducts(self) -> None:
        with open('assets/products.json', encoding="UTF-8") as f:
            products = json.loads(f.read())
        self.purchasedProducts = products
    
    def getVisiblePurchasedProducts(self, exclusiveTags: list[str]) ->  list[Product]:                        
        return list(filter(lambda p: all(exclusiveTag not in p['tags'] for exclusiveTag in exclusiveTags) ,self.purchasedProducts)) if len(exclusiveTags) > 0 else self.purchasedProducts