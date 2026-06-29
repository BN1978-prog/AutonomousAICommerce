
import json
import re
from pathlib import Path
from datetime import datetime, timezone

REGISTRY = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/universal_listing_builder.json")
DRAFTS = Path("app/logs/universal_listing_drafts.json")

MAX_TITLE = 120
MAX_DESCRIPTION = 1800

def clean_text(v):
    v = str(v or "")
    v = re.sub(r"<[^>]+>", " ", v)
    v = re.sub(r"\s+", " ", v).strip()
    return v

def build_listing(sku, item):
    title = clean_text(item.get("seo_title") or item.get("title"))[:MAX_TITLE]
    description = clean_text(item.get("seo_description") or item.get("description") or title)[:MAX_DESCRIPTION]

    price = float(item.get("price") or 0)
    supplier_cost = float(item.get("supplier_cost") or 0)
    shipping_cost = float(item.get("shipping_cost") or 0)
    profit = float(item.get("estimated_profit") or 0)
    margin = float(item.get("margin_percent") or 0)

    tags = item.get("seo_tags") or []
    if isinstance(tags, str):
        tags = [x.strip() for x in tags.split(",") if x.strip()]

    listing = {
        "sku": sku,
        "status": "listing_draft_ready",
        "created_at": datetime.now(timezone.utc).isoformat(),

        "title": title,
        "description": description,
        "tags": tags[:13],
        "image": item.get("image"),
        "images": [item.get("image")] if item.get("image") else [],

        "price": round(price, 2),
        "currency": item.get("currency", "GBP"),

        "supplier": item.get("supplier"),
        "supplier_product_id": item.get("supplier_product_id") or item.get("cj_product_id"),
        "supplier_variant_id": item.get("supplier_variant_id") or item.get("cj_variant_id"),
        "supplier_cost": supplier_cost,
        "shipping_cost": shipping_cost,
        "estimated_profit": profit,
        "margin_percent": margin,

        "weight": item.get("product_weight"),
        "category_name": item.get("category_name"),

        "publish_targets": item.get("publish_targets", {}),
        "channels": item.get("channels", {}),

        "risk": {
            "product_score": item.get("product_score"),
            "tier": item.get("product_score_tier"),
            "flags": item.get("product_score_flags", []),
            "reasons": item.get("product_score_reasons", [])
        },

        "fulfillment": {
            "mode": "dropshipping_after_paid_order",
            "auto_purchase_enabled": False,
            "requires_paid_order": True,
            "supplier": item.get("supplier"),
            "cj_product_id": item.get("cj_product_id"),
            "cj_variant_id": item.get("cj_variant_id")
        },

        "marketplace_payloads": {
            "shopify": {
                "title": title,
                "body_html": description,
                "vendor": "AICommerce",
                "product_type": item.get("category_name") or "General",
                "status": "draft",
                "variants": [{
                    "sku": sku,
                    "price": str(round(price, 2)),
                    "inventory_policy": "continue",
                    "fulfillment_service": "manual"
                }],
                "images": [{"src": item.get("image")}] if item.get("image") else []
            },
            "etsy": {
                "title": title[:140],
                "description": description,
                "price": round(price, 2),
                "quantity": 999,
                "who_made": "i_did",
                "when_made": "made_to_order",
                "taxonomy_id": None,
                "shipping_profile_id": None,
                "is_digital": False
            },
            "ebay": {
                "sku": sku,
                "title": title[:80],
                "description": description,
                "price": round(price, 2),
                "currency": item.get("currency", "GBP"),
                "condition": "NEW"
            },
            "woocommerce": {
                "name": title,
                "type": "simple",
                "regular_price": str(round(price, 2)),
                "description": description,
                "sku": sku,
                "images": [{"src": item.get("image")}] if item.get("image") else []
            },
            "amazon": {
                "sku": sku,
                "title": title,
                "price": round(price, 2),
                "status": "not_enabled"
            }
        }
    }

    return listing

def main():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8-sig")) if REGISTRY.exists() else {}

    drafts = {}
    skipped = []

    for sku, item in registry.items():
        if not isinstance(item, dict):
            continue

        if not item.get("publish_ready"):
            skipped.append({
                "sku": sku,
                "reason": "not_publish_ready",
                "score": item.get("product_score"),
                "flags": item.get("product_score_flags", [])
            })
            continue

        if not item.get("cj_product_id") or not item.get("cj_variant_id"):
            skipped.append({
                "sku": sku,
                "reason": "missing_cj_ids"
            })
            continue

        drafts[sku] = build_listing(sku, item)

        item["listing_draft_ready"] = True
        item["listing_draft_created_at"] = datetime.now(timezone.utc).isoformat()

    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    DRAFTS.write_text(json.dumps(drafts, indent=2, ensure_ascii=False), encoding="utf-8")

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "UNIVERSAL_LISTING_DRAFTS_CREATED",
        "drafts_created": len(drafts),
        "skipped": len(skipped),
        "draft_skus": list(drafts.keys()),
        "skipped_examples": skipped[:20],
        "note": "Drafts only. No marketplace publishing performed."
    }

    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
