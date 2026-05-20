def round_to_99(value: float) -> float:
    if value < 1:
        return 0.99

    whole = int(value)
    return float(f"{whole}.99")


def calculate_optimized_price(cost: float, rules: dict | None = None) -> dict:
    rules = rules or {}

    min_margin = float(rules.get("min_margin", 7.0))
    min_price = float(rules.get("min_price", 9.99))

    cost = float(cost or 0)

    if cost <= 0:
        return {
            "ok": False,
            "reason": "missing_or_invalid_cost",
            "cost": cost
        }

    if cost < 5:
        multiplier = 2.8
    elif cost < 15:
        multiplier = 2.2
    elif cost < 30:
        multiplier = 1.8
    else:
        multiplier = 1.5

    raw_price = cost * multiplier
    margin_price = cost + min_margin
    final_price = max(raw_price, margin_price, min_price)
    final_price = round_to_99(final_price)

    return {
        "ok": True,
        "cost": round(cost, 2),
        "multiplier": multiplier,
        "raw_price": round(raw_price, 2),
        "min_margin_price": round(margin_price, 2),
        "optimized_price": final_price,
        "estimated_margin": round(final_price - cost, 2),
        "estimated_roi_percent": round(((final_price - cost) / cost) * 100, 2)
    }
