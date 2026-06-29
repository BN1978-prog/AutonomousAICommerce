
import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/product_scoring_engine.json")

MAX_GOOD_WEIGHT_GRAMS = 1500
MAX_ALLOWED_WEIGHT_GRAMS = 5000
MIN_PROFIT_GBP = 5.0
MIN_MARGIN_PERCENT = 25.0
MAX_SAFE_PRICE_GBP = 120.0

RISK_WORDS = [
    "knife", "gun", "weapon", "lighter", "butane", "medical", "prescription",
    "adult", "sex", "tobacco", "nicotine", "vape", "cbd", "alcohol",
    "ashes", "cremation", "funeral", "urn", "deceased", "memorial"
]

BULKY_WORDS = [
    "cabinet", "stool", "chair", "sofa", "bed", "dresser", "wardrobe",
    "table", "bookshelf", "pantry", "large", "heavy"
]

GOOD_WORDS = [
    "organizer", "storage", "holder", "stand", "rack", "brush", "light",
    "travel", "portable", "folding", "compact", "cleaning", "accessory"
]

def to_float(v, default=0.0):
    try:
        return float(v or default)
    except Exception:
        return default

def text_of(item):
    return (
        str(item.get("title", "")) + " " +
        str(item.get("description", "")) + " " +
        str(item.get("category_name", ""))
    ).lower()

def contains_any(text, words):
    return any(w in text for w in words)

def score_item(sku, item):
    price = to_float(item.get("price"))
    supplier_cost = to_float(item.get("supplier_cost"))
    shipping_cost = to_float(item.get("shipping_cost"))
    profit = to_float(item.get("estimated_profit"))
    margin = to_float(item.get("margin_percent"))
    weight = to_float(item.get("product_weight"))
    text = text_of(item)

    score = 0
    reasons = []
    flags = []

    # Profit
    if profit >= 30:
        score += 35
        reasons.append("high_profit")
    elif profit >= 15:
        score += 25
        reasons.append("good_profit")
    elif profit >= MIN_PROFIT_GBP:
        score += 15
        reasons.append("acceptable_profit")
    else:
        score -= 40
        flags.append("profit_too_low")

    # Margin
    if margin >= 50:
        score += 25
        reasons.append("strong_margin")
    elif margin >= MIN_MARGIN_PERCENT:
        score += 15
        reasons.append("acceptable_margin")
    else:
        score -= 25
        flags.append("margin_too_low")

    # Price risk
    if 10 <= price <= MAX_SAFE_PRICE_GBP:
        score += 15
        reasons.append("safe_price_range")
    elif price > MAX_SAFE_PRICE_GBP:
        score -= 15
        flags.append("high_ticket_item")
    else:
        score -= 5
        flags.append("low_price_item")

    # Weight / bulky
    if weight and weight <= MAX_GOOD_WEIGHT_GRAMS:
        score += 15
        reasons.append("lightweight")
    elif weight and weight <= MAX_ALLOWED_WEIGHT_GRAMS:
        score += 5
        reasons.append("medium_weight")
    elif weight > MAX_ALLOWED_WEIGHT_GRAMS:
        score -= 25
        flags.append("too_heavy")

    if contains_any(text, BULKY_WORDS):
        score -= 20
        flags.append("bulky_keyword")

    if contains_any(text, GOOD_WORDS):
        score += 10
        reasons.append("good_product_type")

    if contains_any(text, RISK_WORDS):
        score -= 100
        flags.append("blocked_risk_word")

    has_cj = bool(item.get("cj_product_id") and item.get("cj_variant_id"))
    if has_cj:
        score += 20
        reasons.append("real_cj_mapping")
    else:
        score -= 20
        flags.append("missing_cj_mapping")

    publish_ready = (
        score >= 60 and
        not any(f in flags for f in ["blocked_risk_word", "profit_too_low", "too_heavy"]) and
        has_cj
    )

    if score >= 80:
        tier = "A"
    elif score >= 60:
        tier = "B"
    elif score >= 40:
        tier = "C"
    else:
        tier = "D"

    return {
        "sku": sku,
        "score": score,
        "tier": tier,
        "publish_ready": publish_ready,
        "reasons": reasons,
        "flags": flags,
        "price": price,
        "supplier_cost": supplier_cost,
        "shipping_cost": shipping_cost,
        "estimated_profit": profit,
        "margin_percent": margin,
        "weight": weight,
    }

def main():
    data = json.loads(REGISTRY.read_text(encoding="utf-8-sig")) if REGISTRY.exists() else {}

    results = []
    updated = 0

    for sku, item in data.items():
        if not isinstance(item, dict):
            continue

        result = score_item(sku, item)
        results.append(result)

        item["product_score"] = result["score"]
        item["product_score_tier"] = result["tier"]
        item["publish_ready"] = result["publish_ready"]
        item["product_score_flags"] = result["flags"]
        item["product_score_reasons"] = result["reasons"]
        item["product_scored_at"] = datetime.now(timezone.utc).isoformat()
        updated += 1

    data_out = sorted(results, key=lambda x: x["score"], reverse=True)

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "PRODUCT_SCORING_COMPLETED",
        "total": len(results),
        "updated": updated,
        "publish_ready": sum(1 for x in results if x["publish_ready"]),
        "tier_counts": {
            "A": sum(1 for x in results if x["tier"] == "A"),
            "B": sum(1 for x in results if x["tier"] == "B"),
            "C": sum(1 for x in results if x["tier"] == "C"),
            "D": sum(1 for x in results if x["tier"] == "D"),
        },
        "top_products": data_out[:20],
        "blocked_or_low_score": [x for x in data_out if not x["publish_ready"]][-20:]
    }

    REGISTRY.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
