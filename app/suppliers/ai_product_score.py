
def score_product(product):
    score = 50
    reasons = []

    title = (product.get("title") or "").lower()
    category = (
        product.get("raw", {})
        .get("categoryName", "")
        .lower()
    )

    good_keywords = [
        "premium",
        "pet",
        "glass",
        "tea",
        "cup",
        "drinkware",
        "home",
        "kitchen",
        "beauty",
        "fitness"
    ]

    for word in good_keywords:
        if word in title or word in category:
            score += 5
            reasons.append(f"good keyword: {word}")

    category_bonus = {
        "beauty": 15,
        "drinkware": 15,
        "pet": 15,
        "fitness": 10,
        "kitchen": 10,
        "home": 10,
        "electronics": 10
    }

    for k, v in category_bonus.items():
        if k in category:
            score += v
            reasons.append(f"good category: {k}")

    price = float(product.get("price", 0) or 0)

    if 5 <= price <= 50:
        score += 10
        reasons.append("good price range")

    score = max(0, min(score, 100))

    return {
        "score": score,
        "approved": score >= 60,
        "reasons": reasons
    }
