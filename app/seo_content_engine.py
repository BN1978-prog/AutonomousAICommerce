
import json
import re
from pathlib import Path
from datetime import datetime, timezone

REGISTRY = Path("app/logs/imported_skus.json")
DRAFTS = Path("app/logs/universal_listing_drafts.json")
OUT = Path("app/logs/seo_content_engine.json")

def clean(v):
    v = str(v or "")
    v = re.sub(r"<[^>]+>", " ", v)
    v = re.sub(r"\s+", " ", v).strip()
    return v

def words(title):
    return [w.lower() for w in re.findall(r"[a-zA-Z0-9]+", title) if len(w) > 2]

def make_tags(title, category):
    base = []
    for w in words(title + " " + str(category or "")):
        if w not in base:
            base.append(w)
    return base[:13]

def make_description(title, category, price, profit):
    category_line = f"Category: {category}." if category else ""
    return clean(f"""
Upgrade your everyday routine with {title}.

This product is selected for practical use, strong value, and reliable dropshipping fulfillment. It is suitable for customers looking for a useful, modern, and convenient solution.

Key benefits:
- Practical and easy to use
- Selected from a verified supplier source
- Good value at the listed price
- Suitable for online marketplace customers
- Prepared for dropshipping fulfillment after paid order

{category_line}

Price: GBP {price}.
""")

def main():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8-sig")) if REGISTRY.exists() else {}
    drafts = json.loads(DRAFTS.read_text(encoding="utf-8-sig")) if DRAFTS.exists() else {}

    updated = 0
    results = []

    for sku, draft in drafts.items():
        item = registry.get(sku, {})
        title = clean(item.get("title") or draft.get("title"))
        category = item.get("category_name")
        price = item.get("price")
        profit = item.get("estimated_profit")

        seo_title = title[:120]
        seo_description = make_description(title, category, price, profit)
        seo_tags = make_tags(title, category)

        item["seo_title"] = seo_title
        item["seo_description"] = seo_description
        item["seo_tags"] = seo_tags
        item["seo_content_generated_at"] = datetime.now(timezone.utc).isoformat()

        draft["title"] = seo_title
        draft["description"] = seo_description
        draft["tags"] = seo_tags

        for channel, payload in (draft.get("marketplace_payloads") or {}).items():
            if not isinstance(payload, dict):
                continue

            if channel == "shopify":
                payload["title"] = seo_title
                payload["body_html"] = seo_description
                payload["tags"] = ", ".join(seo_tags)

            elif channel == "etsy":
                payload["title"] = seo_title[:140]
                payload["description"] = seo_description
                payload["tags"] = seo_tags[:13]

            elif channel == "ebay":
                payload["title"] = seo_title[:80]
                payload["description"] = seo_description

            elif channel == "woocommerce":
                payload["name"] = seo_title
                payload["description"] = seo_description
                payload["short_description"] = seo_description[:300]

            elif channel == "amazon":
                payload["title"] = seo_title
                payload["description"] = seo_description
                payload["keywords"] = seo_tags

        updated += 1
        results.append({
            "sku": sku,
            "title": seo_title,
            "tags": seo_tags,
            "description_length": len(seo_description)
        })

    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    DRAFTS.write_text(json.dumps(drafts, indent=2, ensure_ascii=False), encoding="utf-8")

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "SEO_CONTENT_GENERATED",
        "updated": updated,
        "results": results,
        "note": "Generated local SEO content only. No marketplace publishing performed."
    }

    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
