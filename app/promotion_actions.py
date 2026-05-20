import json
from pathlib import Path

CANDIDATES = Path("app/logs/promotion_candidates.json")
REPORT = Path("app/logs/promotion_actions.json")

items = json.loads(CANDIDATES.read_text(encoding="utf-8")) if CANDIDATES.exists() else []

actions = []

for item in items:
    sku = item["sku"]
    sku_actions = []

    if item.get("score", 0) >= 90:
        sku_actions.append("high_priority_product")

    if item.get("product_id") is None:
        sku_actions.append("create_or_sync_shopify_product")

    if (
        item.get("ebay_listing_id") is None
        and item.get("ebay_status") != "published"
    ):
        sku_actions.append("verify_ebay_listing_id")

    if item.get("price") and float(item["price"]) < 5:
        sku_actions.append("consider_bundle_or_upsell")

    if item.get("source") == "ai_hunter":
        sku_actions.append("promote_ai_hunter_pick")

    actions.append({
        "sku": sku,
        "score": item.get("score"),
        "actions": sku_actions
    })

REPORT.write_text(
    json.dumps(actions, indent=2),
    encoding="utf-8"
)

print("PROMOTION ACTIONS:", len(actions))
for x in actions:
    print(x["sku"], "=>", ", ".join(x["actions"]))
