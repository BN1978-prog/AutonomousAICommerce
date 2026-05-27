import json
from pathlib import Path
from app.channels.channel_manager import run_channel_action

IN = Path("app/logs/pricing_experiments.json")
OUT = Path("app/logs/pricing_apply_safe_report.json")

items = json.loads(IN.read_text(encoding="utf-8"))
results = []

for item in items:
    sku = item["sku"]
    price = item["test_price"]

    result = run_channel_action(
        "shopify",
        "update_price",
        {
            "sku": sku,
            "price": price
        }
    )

    results.append({
        "sku": sku,
        "old_price": item["current_price"],
        "new_price": price,
        "strategy": item["strategy"],
        "result": result
    })

OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
print(json.dumps(results, indent=2))
