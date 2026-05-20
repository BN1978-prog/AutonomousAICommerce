def check_marketplace_compliance(product: dict) -> dict:
    title = (product.get("title") or "").lower()
    description = (product.get("description") or "").lower()

    text = f"{title} {description}"

    restricted_keywords = {
        "amazon": [
            "medical",
            "healing",
            "cure",
            "guaranteed",
            "weight loss",
            "supplement"
        ],
        "ebay": [
            "replica",
            "fake",
            "counterfeit",
            "weapon"
        ],
        "google_merchant": [
            "weapon",
            "adult",
            "supplement"
        ],
        "tiktok_shop": [
            "before and after",
            "miracle",
            "guaranteed"
        ]
    }

    results = {}

    for marketplace, keywords in restricted_keywords.items():
        violations = []

        for keyword in keywords:
            if keyword in text:
                violations.append(keyword)

        risk_level = "low"

        if len(violations) >= 3:
            risk_level = "high"
        elif violations:
            risk_level = "medium"

        approved = len(violations) == 0

        results[marketplace] = {
            "approved": approved,
            "risk_level": risk_level,
            "violations": violations
        }

    overall = "approved"

    high_risk = [
        m for m, data in results.items()
        if data["risk_level"] == "high"
    ]

    if high_risk:
        overall = "blocked"
    elif any(not x["approved"] for x in results.values()):
        overall = "needs_review"

    return {
        "ok": True,
        "product": {
            "title": product.get("title"),
            "sku": product.get("sku")
        },
        "overall_status": overall,
        "marketplace_compliance": results
    }
