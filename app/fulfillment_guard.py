def check_fulfillment_allowed(order: dict, product: dict) -> dict:
    sku = order.get("sku") or product.get("sku")

    sale_price = float(order.get("sale_price", 0) or 0)
    cost = float(product.get("cost", 0) or 0)
    shipping_cost = float(product.get("shipping_cost", 0) or 0)

    profit = sale_price - cost - shipping_cost

    if not sku:
        return {
            "allowed": False,
            "reason": "missing_sku"
        }

    if not order.get("paid"):
        return {
            "allowed": False,
            "reason": "order_not_paid"
        }

    if not order.get("shipping_address"):
        return {
            "allowed": False,
            "reason": "missing_shipping_address"
        }

    if profit <= 0:
        return {
            "allowed": False,
            "reason": "no_profit",
            "estimated_profit": round(profit, 2)
        }

    return {
        "allowed": True,
        "reason": "ok",
        "estimated_profit": round(profit, 2),
        "sku": sku
    }
