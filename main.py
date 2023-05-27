from cart import Cart
from pos import POS, SpecifiedXthPieceDiscountYUnitRule, SpecifiedSecondPieceDiscountYPercentRule, SpecifiedSameProductSecondPieceYUnitRule, SpecifiedXthPieceDiscountYPercentRule


def main():
    cart = Cart()
    cart.loadProducts()
    pos = POS()
    pos.loadRules([
        SpecifiedXthPieceDiscountYUnitRule("衛生紙", 6, 100, ["ex1"]),
        SpecifiedSecondPieceDiscountYPercentRule("雞湯塊", 50),
        SpecifiedSameProductSecondPieceYUnitRule("同商品加購優惠", 10, ["ex1"]),
        SpecifiedXthPieceDiscountYPercentRule("熱銷飲品", 2, 12)
    ])
    pos.process(cart)

    print("購買商品:")
    print("---------------------------------------------------")
    for p in cart.purchasedProducts:
        print(f"- {p['id']}, [{p['sku']}] {p['name']}, {p['price']}元, 標籤:{p['tags']}")
    print("\n")
    print("折扣:")
    print("---------------------------------------------------")
    for d in cart.appliedDiscounts:
        print(f"- 折抵 {d.amount} 元, {d.rule.name} ({d.rule.note})")
        for p in d.products:
            print(f"  * 符合: {p['id']}, [{p['sku']}] {p['name']}, 標籤:{p['tags']}")
        print("\n")    
    print("---------------------------------------------------")
    print(f"結帳金額: {cart.totalPrice} 元")

    return 0


if __name__ == "__main__":
    main()
