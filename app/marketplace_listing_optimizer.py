
import json
import re
from pathlib import Path
from datetime import datetime, timezone

DRAFTS = Path("app/logs/universal_listing_drafts.json")
REGISTRY = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/marketplace_listing_optimizer.json")

def clean(v):
    v = str(v or "")
    v = re.sub(r"<[^>]+>", " ", v)
    v = re.sub(r"\s+", " ", v).strip()
    return v

def slugify(v):
    v = clean(v).lower()
    v = re.sub(r"[^a-z0-9]+", "-", v)
    return v.strip("-")[:80]

def short(v, n):
    return clean(v)[:n]

def main():
    drafts = json.loads(DRAFTS.read_text(encoding="utf-8-sig")) if DRAFTS.exists() else {}
    registry = json.loads(REGISTRY.read_text(encoding="utf-8-sig")) if REGISTRY.exists() else {}

    updated = 0
    results = []

    for sku, draft in drafts.items():
        item = registry.get(sku, {})
        payloads = draft.get("marketplace_payloads", {})

        title = clean(draft.get("title") or item.get("title"))
        desc = clean(draft.get("description") or item.get("seo_description") or title)
        tags = draft.get("tags") or item.get("seo_tags") or []
        category = item.get("category_name") or "General"

        # Shopify
        if "shopify" in payloads:
            p = payloads["shopify"]
            p["title"] = short(title, 120)
            p["body_html"] = f"<p>{desc}</p>"
            p["tags"] = ", ".join(tags[:20])
            p["seo"] = {
                "title": short(title, 70),
                "description": short(desc, 160)
            }

        # Etsy
        if "etsy" in payloads:
            p = payloads["etsy"]
            p["title"] = short(title, 140)
            p["description"] = desc
            p["tags"] = tags[:13]
            p["materials"] = []
            p["taxonomy_id"] = p.get("taxonomy_id")
            p["shipping_profile_id"] = p.get("shipping_profile_id")
            p["state"] = "draft"

        # eBay
        if "ebay" in payloads:
            p = payloads["ebay"]
            p["title"] = short(title, 80)
            p["description"] = (
                f"<h2>{short(title, 120)}</h2>"
                f"<p>{desc}</p>"
                f"<ul>"
                f"<li>Condition: New</li>"
                f"<li>Fulfillment: Dropshipping after paid order</li>"
                f"<li>SKU: {sku}</li>"
                f"</ul>"
            )
            p["item_specifics"] = {
                "Brand": "Unbranded",
                "Condition": "New",
                "Type": category.split("/")[-1].strip() if "/" in category else category
            }

        # WooCommerce
        if "woocommerce" in payloads:
            p = payloads["woocommerce"]
            p["name"] = short(title, 120)
            p["slug"] = slugify(title)
            p["description"] = desc
            p["short_description"] = short(desc, 300)
            p["categories"] = [{"name": category.split("/")[0].strip()}] if category else []
            p["attributes"] = [
                {"name": "Supplier", "options": [str(item.get("supplier", "cj"))]},
                {"name": "Fulfillment", "options": ["Dropshipping after paid order"]}
            ]

        draft["marketplace_optimized_at"] = datetime.now(timezone.utc).isoformat()
        item["marketplace_optimized"] = True
        item["marketplace_optimized_at"] = draft["marketplace_optimized_at"]

        updated += 1
        results.append({
            "sku": sku,
            "title": title,
            "channels": list(payloads.keys())
        })

    DRAFTS.write_text(json.dumps(drafts, indent=2, ensure_ascii=False), encoding="utf-8")
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "MARKETPLACE_LISTINGS_OPTIMIZED",
        "updated": updated,
        "results": results,
        "note": "Optimized drafts only. No marketplace publishing performed."
    }

    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
