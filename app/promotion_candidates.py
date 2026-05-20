import json
from pathlib import Path

IMPORTS = Path("app/logs/imported_skus.json")
REPORT = Path("app/logs/promotion_candidates.json")

MIN_SCORE = 80

data = json.loads(IMPORTS.read_text(encoding="utf-8"))

candidates = []

for sku, meta in data.items():
    score = int(meta.get("last_score", 0) or 0)
    sales = int(meta.get("sales", 0) or 0)
    ebay_status = meta.get("ebay_status")
    product_id = meta.get("product_id")

    if score >= MIN_SCORE and sales == 0 and ebay_status == "published":
        candidates.append({
            "sku": sku,
            "score": score,
            "price": meta.get("last_price"),
            "source": meta.get("source"),
            "ebay_status": ebay_status,
            "ebay_offer_id": meta.get("ebay_offer_id"),
            "ebay_listing_id": meta.get("ebay_listing_id"),
            "product_id": product_id
        })

candidates = sorted(
    candidates,
    key=lambda x: x.get("score", 0),
    reverse=True
)

REPORT.write_text(
    json.dumps(candidates, indent=2),
    encoding="utf-8"
)

print("PROMOTION CANDIDATES:", len(candidates))
for item in candidates[:10]:
    print(item["sku"], "score=", item["score"], "price=", item.get("price"))
