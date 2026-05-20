def score_item(
    title: str,
    supplier_cost: float,
    shipping_cost: float,
    expected_sale_price: float,
    demand_score: float,
    competition_score: float,
    supplier_trust_score: float,
    platform_fee_percent: float = 12,
    estimated_return_rate_percent: float = 5,
):
    platform_fee = expected_sale_price * platform_fee_percent / 100
    refund_risk = expected_sale_price * estimated_return_rate_percent / 100 * 0.35
    net_profit = expected_sale_price - supplier_cost - shipping_cost - platform_fee - refund_risk
    margin_percent = (net_profit / expected_sale_price) * 100 if expected_sale_price else 0

    opportunity_score = (
        demand_score * 0.35
        + (100 - competition_score) * 0.20
        + supplier_trust_score * 0.20
        + max(0, min(100, margin_percent * 2)) * 0.25
    )

    risk_score = (
        competition_score * 0.25
        + (100 - supplier_trust_score) * 0.35
        + estimated_return_rate_percent * 0.25
        + max(0, 25 - margin_percent) * 0.15
    )

    if net_profit <= 0 or margin_percent < 15 or risk_score > 55:
        decision = "reject"
    elif margin_percent >= 25 and opportunity_score >= 65 and risk_score <= 45:
        decision = "approve"
    else:
        decision = "watch"

    return {
        "title": title,
        "supplier_cost": round(supplier_cost, 2),
        "shipping_cost": round(shipping_cost, 2),
        "expected_sale_price": round(expected_sale_price, 2),
        "net_profit": round(net_profit, 2),
        "margin_percent": round(margin_percent, 2),
        "risk_score": round(risk_score, 2),
        "opportunity_score": round(opportunity_score, 2),
        "decision": decision,
    }
