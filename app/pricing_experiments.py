import json
from pathlib import Path

CANDIDATES = Path("app/logs/promotion_candidates.json")
OUT = Path("app/logs/pricing_experiments.json")

items = json.loads(CANDIDATES.read_text(encoding="utf-8")) if CANDIDATES.exists() else []

experiments = []

for item in items:
    sku = item.get("sku")
    price = float(item.get("price") or 0)
    score = int(item.get("score") or 0)

    if price <= 0:
        continue

    if score >= 90:
        strategy = "premium_hold_or_bundle"
        test_price = round(price * 1.10, 2)
        reason = "High score product. Test higher perceived value or bundle instead of discount."
    elif score >= 80:
        strategy = "small_discount_test"
        test_price = round(price * 0.95, 2)
        reason = "Good score but no sales yet. Test small discount to improve conversion."
    else:
        strategy = "no_test"
        test_price = price
        reason = "Score below promotion threshold."

    experiments.append({
        "sku": sku,
        "score": score,
        "current_price": price,
        "test_price": test_price,
        "strategy": strategy,
        "reason": reason,
        "auto_apply": False
    })

OUT.write_text(
    json.dumps(experiments, indent=2),
    encoding="utf-8"
)

print("PRICING EXPERIMENTS:", len(experiments))

for x in experiments:
    print(
        x["sku"],
        "current=", x["current_price"],
        "test=", x["test_price"],
        "strategy=", x["strategy"]
    )
