def predict_demand(product: dict, learning: dict, strategy: dict) -> dict:
    title = (product.get("title") or "").lower()
    category = (product.get("category") or "").lower()

    historical_niches = learning.get("top_historical_niches", [])
    keyword_focus = strategy.get("strategy", {}).get("keyword_focus", [])

    demand_score = 40
    reasons = []
    niche = "general"

    if "sock" in title:
        niche = "pet socks"
        demand_score += 25
        reasons.append("matches_pet_socks_winner")
    elif "harness" in title:
        niche = "pet harness"
        demand_score += 25
        reasons.append("matches_pet_harness_winner")
    elif "shampoo" in title:
        niche = "pet shampoo"
        demand_score += 20
        reasons.append("matches_pet_shampoo_winner")
    elif "groom" in title or "brush" in title:
        niche = "pet grooming"
        demand_score += 15
        reasons.append("matches_pet_grooming")

    if "pet" in category or "pet" in title:
        demand_score += 10
        reasons.append("pet_category_confirmed")

    for item in historical_niches:
        if item.get("niche") == niche:
            wins = int(item.get("wins") or 0)
            avg_margin = float(item.get("average_margin") or 0)
            demand_score += min(wins * 5, 20)

            if avg_margin >= 75:
                demand_score += 10
                reasons.append("strong_historical_margin")

            if wins > 0:
                reasons.append("historical_winner")

    if niche in keyword_focus:
        demand_score += 10
        reasons.append("strategy_focus_niche")

    saturation_risk = "low"

    if niche == "general":
        saturation_risk = "high"
        demand_score -= 20
        reasons.append("generic_product_risk")
    elif demand_score >= 80:
        saturation_risk = "medium"

    demand_score = max(0, min(100, demand_score))

    demand_level = "low"
    if demand_score >= 80:
        demand_level = "high"
    elif demand_score >= 55:
        demand_level = "medium"

    return {
        "ok": True,
        "product": {
            "title": product.get("title"),
            "sku": product.get("sku"),
            "category": product.get("category")
        },
        "niche": niche,
        "demand_score": demand_score,
        "demand_level": demand_level,
        "saturation_risk": saturation_risk,
        "reasons": reasons,
        "recommendation": "scale" if demand_score >= 75 else "test" if demand_score >= 55 else "watch"
    }
