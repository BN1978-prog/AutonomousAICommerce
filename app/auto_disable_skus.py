import json
from pathlib import Path

IMPORTS = Path("app/logs/imported_skus.json")
BLOCKED = Path("app/logs/blocked_products.json")
REPORT = Path("app/logs/auto_disable_report.json")

imports = json.loads(IMPORTS.read_text(encoding="utf-8"))

new_blocked = []
report = {
    "checked": 0,
    "low_score": 0,
    "out_of_stock": 0,
    "no_sales": 0,
    "blocked": 0
}

for sku, data in imports.items():
    report["checked"] += 1

    score = data.get("last_score", None)
    stock = data.get("current_inventory", data.get("inventory", 10))
    sales = int(data.get("sales", 0) or 0)

    reasons = []

    if score is not None and score < 60:
        reasons.append("low_score")
        report["low_score"] += 1

    if stock <= 0:
        reasons.append("out_of_stock")
        report["out_of_stock"] += 1

    if sales == 0:
        report["no_sales"] += 1

    if reasons:
        new_blocked.append({
            "sku": sku,
            "reasons": reasons,
            "score": score,
            "stock": stock,
            "sales": sales
        })

report["blocked"] = len(new_blocked)

BLOCKED.write_text(
    json.dumps(new_blocked, indent=2),
    encoding="utf-8"
)

REPORT.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print("CHECKED:", report["checked"])
print("LOW_SCORE:", report["low_score"])
print("OUT_OF_STOCK:", report["out_of_stock"])
print("NO_SALES:", report["no_sales"])
print("BLOCKED:", report["blocked"])
