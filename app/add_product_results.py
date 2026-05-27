import json
from pathlib import Path

PERFORMANCE = Path("app/logs/product_performance.json")

performance = json.loads(PERFORMANCE.read_text(encoding="utf-8-sig"))

print("Available products:")
for product_id, data in performance.items():
    print(product_id, data)

product_id = input("Product ID: ").strip()
clicks = int(input("Add clicks: ").strip() or "0")
sales = int(input("Add sales: ").strip() or "0")

if product_id not in performance:
    print("Unknown product:", product_id)
    raise SystemExit

performance[product_id]["clicks"] += clicks
performance[product_id]["sales"] += sales
performance[product_id]["score"] = (
    performance[product_id]["clicks"] +
    performance[product_id]["sales"] * 10
)

PERFORMANCE.write_text(json.dumps(performance, indent=2), encoding="utf-8")

print("Updated:")
print(json.dumps(performance[product_id], indent=2))
