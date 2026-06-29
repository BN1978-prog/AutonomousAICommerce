
import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/sku_master_enricher.json")

MIN_PROFIT_GBP = 5.00
DEFAULT_SHIPPING_COST = 2.99
DEFAULT_SUPPLIER = "cj"

def to_float(v, default=0.0):
    try:
        return float(v or default)
    except Exception:
        return default

def estimate_supplier_cost(item):
    # Safe placeholder until real CJ product/variant cost is resolved.
    price = to_float(item.get("price") or item.get("last_price"))
    if price <= 0:
        return 0.0
    return round(price * 0.35, 2)

def enrich_item(sku, item):
    changed = False

    price = to_float(item.get("price") or item.get("last_price"))

    if not item.get("currency"):
        item["currency"] = "GBP"
        changed = True

    if not item.get("supplier"):
        item["supplier"] = DEFAULT_SUPPLIER
        changed = True

    if not item.get("supplier_cost"):
        item["supplier_cost"] = estimate_supplier_cost(item)
        changed = True

    if not item.get("shipping_cost"):
        item["shipping_cost"] = DEFAULT_SHIPPING_COST
        changed = True

    supplier_cost = to_float(item.get("supplier_cost"))
    shipping_cost = to_float(item.get("shipping_cost"))

    estimated_profit = round(price - supplier_cost - shipping_cost, 2)
    margin_percent = round((estimated_profit / price) * 100, 2) if price > 0 else 0.0

    item["estimated_profit"] = estimated_profit
    item["margin_percent"] = margin_percent
    item["profitable"] = estimated_profit >= MIN_PROFIT_GBP and margin_percent > 0

    item.setdefault("supplier_product_id", None)
    item.setdefault("supplier_variant_id", None)
    item.setdefault("cj_product_id", item.get("supplier_product_id"))
    item.setdefault("cj_variant_id", item.get("supplier_variant_id"))

    item.setdefault("inventory_supplier", None)

    item.setdefault("publish_targets", {
        "shopify": True,
        "etsy": True,
        "ebay": True,
        "woocommerce": True,
        "amazon": False
    })

    item.setdefault("channels", {})

    item["channels"].setdefault("shopify", {})
    if item.get("product_id"):
        item["channels"]["shopify"]["product_id"] = item.get("product_id")
    if item.get("product_url"):
        item["channels"]["shopify"]["product_url"] = item.get("product_url")

    item["channels"].setdefault("ebay", {})
    if item.get("ebay_offer_id"):
        item["channels"]["ebay"]["offer_id"] = item.get("ebay_offer_id")
    if item.get("ebay_listing_id"):
        item["channels"]["ebay"]["listing_id"] = item.get("ebay_listing_id")
    if item.get("ebay_status"):
        item["channels"]["ebay"]["status"] = item.get("ebay_status")

    item["channels"].setdefault("etsy", {})
    if item.get("etsy_listing_id"):
        item["channels"]["etsy"]["listing_id"] = item.get("etsy_listing_id")

    item["channels"].setdefault("woocommerce", {})
    if item.get("woocommerce_id"):
        item["channels"]["woocommerce"]["product_id"] = item.get("woocommerce_id")

    item["channels"].setdefault("amazon", {})

    item["sku_master_enriched_at"] = datetime.now(timezone.utc).isoformat()

    return changed

def main():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8-sig")) if REGISTRY.exists() else {}

    enriched = 0
    profitable = 0
    missing_supplier_ids = 0

    for sku, item in registry.items():
        if not isinstance(item, dict):
            continue

        enrich_item(sku, item)
        enriched += 1

        if item.get("profitable"):
            profitable += 1

        if not item.get("supplier_product_id") and not item.get("cj_product_id"):
            missing_supplier_ids += 1

    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "SKU_MASTER_ENRICHED",
        "total_skus": len(registry),
        "enriched": enriched,
        "profitable": profitable,
        "missing_supplier_ids": missing_supplier_ids,
        "note": "Supplier costs are estimated until real CJ product/variant mapping is resolved."
    }

    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
