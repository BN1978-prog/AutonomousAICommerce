import json
from pathlib import Path
from datetime import datetime, timezone

IMPORTS = Path("app/logs/imported_skus.json")
SEO_RESULTS = Path("app/logs/seo_push_results.json")

META_FEED = Path("app/logs/meta_feed_seo.json")
GOOGLE_FEED = Path("app/logs/google_feed_seo.json")
OUT = Path("app/logs/feed_regeneration_results.json")

imports = json.loads(IMPORTS.read_text(encoding="utf-8")) if IMPORTS.exists() else {}
seo_results = json.loads(SEO_RESULTS.read_text(encoding="utf-8")) if SEO_RESULTS.exists() else []

eligible_skus = {
    r["sku"]
    for r in seo_results
    if r.get("ok") is True and r.get("channel") in ["meta_feed", "google_feed"]
}

meta_feed = []
google_feed = []
results = []

for sku in sorted(eligible_skus):
    item = imports.get(sku)

    if not item:
        results.append({
            "sku": sku,
            "ok": False,
            "reason": "sku_not_found_in_registry"
        })
        continue

    base = {
        "sku": sku,
        "title": item.get("title"),
        "description": item.get("description"),
        "tags": item.get("tags"),
        "price": item.get("price"),
        "image": item.get("image"),
        "product_url": item.get("product_url"),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    meta_feed.append({
        **base,
        "feed": "meta"
    })

    google_feed.append({
        **base,
        "feed": "google"
    })

    results.append({
        "sku": sku,
        "ok": True,
        "reason": "feeds_regenerated"
    })

META_FEED.write_text(json.dumps(meta_feed, indent=2), encoding="utf-8")
GOOGLE_FEED.write_text(json.dumps(google_feed, indent=2), encoding="utf-8")
OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")

print("FEED REGENERATION RESULTS:", len(results))

for r in results:
    print(r["sku"], "ok=", r["ok"], "reason=", r["reason"])
