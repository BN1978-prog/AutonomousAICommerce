import json
from pathlib import Path
from datetime import datetime, timezone

IMPORTS = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/order_orchestration_plan.json")

imports = json.loads(IMPORTS.read_text(encoding="utf-8")) if IMPORTS.exists() else {}

plans = []

for sku, meta in imports.items():
    sales = int(meta.get("sales", 0) or 0)

    if sales <= 0:
        continue

    sale_price = float(meta.get("last_price", 0) or 0)
    cost = float(meta.get("cost", 0) or 0)
    shipping_cost = float(meta.get("shipping_cost", 0) or 0)
    profit = sale_price - cost - shipping_cost

    action = "hold"

    if profit > 0:
        action = "ready_for_supplier_purchase"

    if profit <= 0:
        action = "blocked_no_profit"

    plans.append({
        "sku": sku,
        "sales": sales,
        "sale_price": sale_price,
        "cost": cost,
        "shipping_cost": shipping_cost,
        "estimated_profit": round(profit, 2),
        "supplier": meta.get("supplier") or "cj",
        "action": action,
        "created_at": datetime.now(timezone.utc).isoformat()
    })

OUT.write_text(
    json.dumps(plans, indent=2),
    encoding="utf-8"
)

print("ORDER ORCHESTRATION PLANS:", len(plans))
print("REPORT:", OUT)
