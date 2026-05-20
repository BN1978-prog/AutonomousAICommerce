def optimize_prices(product: dict, strategy: dict) -> dict:
    cost = float(product.get("cost") or product.get("cost_price") or 0)
    shipping = float(product.get("shipping_cost") or 0)
    current_price = float(product.get("price") or 0)

    mode = strategy.get("strategy_mode", "balanced")

    target_margins = {
        "safe": 55,
        "balanced": 65,
        "aggressive": 72
    }

    target_margin = target_margins.get(mode, 65)

    marketplace_fees = {
        "shopify": {"percent_fee": 2.9, "fixed_fee": 0.30},
        "woocommerce": {"percent_fee": 2.9, "fixed_fee": 0.30},
        "meta_shop": {"percent_fee": 5.0, "fixed_fee": 0.40},
        "tiktok_shop": {"percent_fee": 8.0, "fixed_fee": 0.20},
        "etsy": {"percent_fee": 9.5, "fixed_fee": 0.45},
        "google_merchant": {"percent_fee": 12.0, "fixed_fee": 0.30},
        "ebay": {"percent_fee": 13.25, "fixed_fee": 0.30},
        "walmart": {"percent_fee": 15.0, "fixed_fee": 0.00},
        "amazon": {"percent_fee": 15.0, "fixed_fee": 0.99}
    }

    optimized = {}
    base_cost = cost + shipping
    title = (product.get("title") or "").lower()

    for marketplace, fee in marketplace_fees.items():
        percent_fee = fee["percent_fee"] / 100
        fixed_fee = fee["fixed_fee"]

        denominator = 1 - percent_fee - (target_margin / 100)

        if denominator <= 0:
            suggested_price = current_price or (base_cost * 3)
        else:
            suggested_price = (base_cost + fixed_fee) / denominator

        if marketplace in ["amazon", "walmart"]:
            suggested_price *= 1.05

        if marketplace in ["tiktok_shop", "meta_shop"]:
            suggested_price *= 0.98

        if "sock" in title:
            suggested_price = min(suggested_price, 14.99)
        elif "harness" in title:
            suggested_price = min(suggested_price, 29.99)
        elif "shampoo" in title:
            suggested_price = min(suggested_price, 19.99)
        elif "groom" in title:
            suggested_price = min(suggested_price, 24.99)

        suggested_price = round(max(suggested_price, 9.99), 2)

        estimated_fee = round((suggested_price * fee["percent_fee"] / 100) + fixed_fee, 2)
        net_profit = round(suggested_price - estimated_fee - base_cost, 2)
        margin = round((net_profit / suggested_price) * 100, 2) if suggested_price > 0 else 0

        optimized[marketplace] = {
            "current_price": current_price,
            "suggested_price": suggested_price,
            "target_margin_percent": target_margin,
            "estimated_fee": estimated_fee,
            "estimated_net_profit": net_profit,
            "estimated_margin_percent": margin,
            "strategy_mode": mode
        }

    ranked = sorted(
        optimized.items(),
        key=lambda x: x[1]["estimated_net_profit"],
        reverse=True
    )

    return {
        "ok": True,
        "product": {
            "title": product.get("title"),
            "sku": product.get("sku"),
            "cost": cost,
            "shipping_cost": shipping,
            "current_price": current_price
        },
        "strategy_mode": mode,
        "optimized_prices": [
            {"marketplace": name, **data}
            for name, data in ranked
        ]
    }
