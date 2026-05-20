import json
from pathlib import Path

IMPORTS = Path("app/logs/imported_skus.json")
BLOCKED = Path("app/logs/blocked_products.json")
PROMO = Path("app/logs/promotion_candidates.json")
ACTIONS = Path("app/logs/promotion_actions.json")
PRICING = Path("app/logs/pricing_experiments.json")
CONVERSION = Path("app/logs/conversion_watch.json")
DECISION = Path("app/logs/daily_decision_report.md")
META = Path("data/catalog/meta-products-shopify.xml")
GOOGLE = Path("data/catalog/google-merchant-products.xml")

def load_json(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default

imports = load_json(IMPORTS, {})
blocked = load_json(BLOCKED, [])
promo = load_json(PROMO, [])
actions = load_json(ACTIONS, [])
pricing = load_json(PRICING, [])
conversion = load_json(CONVERSION, [])

total = len(imports)
shopify = sum(1 for x in imports.values() if x.get("product_id"))
ebay = sum(1 for x in imports.values() if x.get("ebay_status") == "published")
hunter = sum(1 for x in imports.values() if x.get("source") == "ai_hunter")

missing_shopify = [sku for sku, x in imports.items() if not x.get("product_id")]
missing_ebay = [sku for sku, x in imports.items() if x.get("ebay_status") != "published"]

status = "OK"

checks = {
    "imports_exist": total > 0,
    "shopify_complete": shopify == total,
    "ebay_complete": ebay == total,
    "meta_feed_exists": META.exists(),
    "google_feed_exists": GOOGLE.exists(),
    "blocked_zero": len(blocked) == 0,
    "promotion_ready": len(promo) == len(actions) if promo else True,
    "pricing_ready": len(pricing) == len(promo) if promo else True,
    "conversion_ready": len(conversion) == total,
    "decision_report_exists": DECISION.exists()
}

if not all(checks.values()):
    status = "CHECK"

print("=== FINAL SYSTEM CHECK ===")
print("TOTAL SKUS:", total)
print("SHOPIFY:", shopify, "/", total)
print("EBAY:", ebay, "/", total)
print("AI HUNTER SKUS:", hunter)
print("BLOCKED:", len(blocked))
print("PROMOTION CANDIDATES:", len(promo))
print("PROMOTION ACTIONS:", len(actions))
print("PRICING EXPERIMENTS:", len(pricing))
print("CONVERSION WATCH:", len(conversion))
print("META FEED:", "OK" if META.exists() else "MISSING")
print("GOOGLE FEED:", "OK" if GOOGLE.exists() else "MISSING")
print()

for k, v in checks.items():
    print(k + ":", "OK" if v else "CHECK")

print()
print("STATUS:", status)

if missing_shopify:
    print("MISSING SHOPIFY:", missing_shopify[:10])

if missing_ebay:
    print("MISSING EBAY:", missing_ebay[:10])
