from typing import Iterable

from cart import Product, Cart


class Discount:
    def __init__(self, rule: 'Rule', products: list[Product], amount: int):
        self.rule = rule
        self.products = products
        self.amount = amount


class Rule:
    def __init__(self):
        self.name: str
        self.note: str
        self.exclusiveTags = []
    def process(self, cart: Cart) -> Iterable[Discount]:
        pass


class SpecifiedXthPieceDiscountYUnitRule(Rule):
    def __init__(self, tag: str, minCount: int, discountAmount: int, exclusiveTags: list[str] = []):
        super().__init__()
        self.name = f"指定商品 {minCount} 件折扣 {discountAmount} 元"
        self.note = f"{tag}滿{minCount}件折{discountAmount}"
        self.tag = tag
        self.minCount = minCount
        self.discountAmount = discountAmount
        self.exclusiveTags = exclusiveTags

    def process(self, cart: Cart) -> list[Discount]:
        matchedProducts: list[Product] = []
        discounts: list[Discount] = []
        for p in filter(lambda p: self.tag in p['tags'], cart.getVisiblePurchasedProducts(self.exclusiveTags)):
            matchedProducts.append(p)
            if (len(matchedProducts) == self.minCount):
                # copy
                discounts.append(Discount(self, matchedProducts.copy(), self.discountAmount))
                matchedProducts.clear()
        return discounts

class SpecifiedSecondPieceDiscountYPercentRule(Rule):
    def __init__(self, tag: str, percentOff: int):
        super().__init__()
        self.name = f"指定商品第二件{10 - percentOff / 10}折"
        self.note = f"{tag}第二件{10 - percentOff / 10}折"
        self.tag = tag
        self.percentOff = percentOff

        
    def process(self, cart: Cart) -> list[Discount]:
        matchedProducts: list[Product] = []
        discounts: list[Discount] = []
        for p in filter(lambda p: self.tag in p['tags'], cart.getVisiblePurchasedProducts(self.exclusiveTags)):
            matchedProducts.append(p)
            if (len(matchedProducts) == 2):
                # copy
                discounts.append(Discount(self, matchedProducts.copy(), p['price'] * self.percentOff / 100))
                matchedProducts.clear()
        return discounts


class SpecifiedSameProductSecondPieceYUnitRule(Rule):
    def __init__(self, tag: str, amount: int, exclusiveTags: list[str] = []):
        super().__init__()
        self.name = f"同商品加購優惠"
        self.note = f"同商品第二件 {amount} 元"
        self.tag = tag
        self.amount = amount
        self.exclusiveTags = exclusiveTags

    def process(self, cart: Cart) -> list[Discount]:
        matchedProducts: list[Product] = []
        discounts: list[Discount] = []
        visiblePurchasedProducts = cart.getVisiblePurchasedProducts(self.exclusiveTags)        
        for sku in list(set(map(lambda p: p['sku'], filter(lambda p: self.tag in p['tags'], visiblePurchasedProducts)))):
            matchedProducts.clear()
            for p in filter(lambda p: p['sku'] == sku, visiblePurchasedProducts):
                matchedProducts.append(p)
                if (len(matchedProducts) == 2):
                    # copy
                    discounts.append(Discount(self, matchedProducts.copy(), p['price'] - self.amount))
                    matchedProducts.clear()        
        return discounts

class SpecifiedXthPieceDiscountYPercentRule(Rule):
    def __init__(self, tag: str, minCount: int, percentOff: int):
        super().__init__()
        self.name = f"滿件折扣"
        self.note = f"指定商品 {minCount} 件 {10 - percentOff / 10}折"
        self.tag = tag
        self.minCount = minCount
        self.percentOff = percentOff

    def process(self, cart: Cart) -> list[Discount]:
        matchedProducts: list[Product] = []
        discounts: list[Discount] = []
        for p in sorted(filter(lambda p: self.tag in p['tags'], cart.getVisiblePurchasedProducts(self.exclusiveTags)), key=lambda p: p['price'], reverse=True):
            matchedProducts.append(p)
            if (len(matchedProducts) == self.minCount):
                # copy
                discounts.append(Discount(self, matchedProducts.copy(), sum(map(lambda p: p['price'], matchedProducts)) * self.percentOff / 100))
                matchedProducts.clear()
        return discounts

class POS:
    def __init__(self):
        self.activeRules: list[Rule] = []

    def loadRules(self, rules: list[Rule]) -> None:
        self.activeRules = rules

    def process(self, cart: Cart) -> None:
        cart.appliedDiscounts = []
        cart.totalPrice = sum(map(lambda p: p['price'], cart.purchasedProducts))
        for rule in self.activeRules:
            discounts = rule.process(cart)            
            cart.appliedDiscounts.extend(discounts)
            if len(rule.exclusiveTags) > 0:
                for d in discounts:                                                        
                    for p in d.products:                        
                        p['tags'].extend(rule.exclusiveTags)                        
            cart.totalPrice -= sum(map(lambda d: d.amount, discounts))
