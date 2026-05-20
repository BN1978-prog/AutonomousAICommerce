MIN_SELL_PRICE = 5.00
MAX_SELL_PRICE = 500.00
MIN_PROFIT = 5.00
MIN_MARGIN_PERCENT = 25
REQUIRE_STOCK = True
REQUIRE_IMAGE = False

def validate_product_for_import(product):
    issues = []

    cost = float(product.get("cost_price", 0))
    price = float(product.get("price", 0))
    inventory = int(product.get("inventory", 0))

    profit = price - cost
    margin_percent = (profit / price * 100) if price > 0 else 0

    if price < MIN_SELL_PRICE:
        issues.append("sell price too low")

    if price > MAX_SELL_PRICE:
        issues.append("sell price too high")

    if profit < MIN_PROFIT:
        issues.append("profit below minimum")

    if margin_percent < MIN_MARGIN_PERCENT:
        issues.append("margin percent below minimum")

    if REQUIRE_STOCK and inventory <= 0:
        issues.append("out of stock")

    if REQUIRE_IMAGE and not product.get("image"):
        issues.append("missing image")

    if not product.get("title") or len(product["title"]) < 5:
        issues.append("bad title")

    return {
        "allowed": len(issues) == 0,
        "issues": issues,
        "profit": round(profit, 2),
        "margin_percent": round(margin_percent, 2)
    }
