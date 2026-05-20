import json
from pathlib import Path

IMPORTS = Path("app/logs/imported_skus.json")
BLOCKED = Path("app/logs/blocked_products.json")
STOCK = Path("app/logs/stock_state.json")
META = Path("data/catalog/meta-products-shopify.xml")
GOOGLE = Path("data/catalog/google-merchant-products.xml")

imports = json.loads(IMPORTS.read_text(encoding="utf-8")) if IMPORTS.exists() else {}
blocked = json.loads(BLOCKED.read_text(encoding="utf-8")) if BLOCKED.exists() else {}
stock = json.loads(STOCK.read_text(encoding="utf-8")) if STOCK.exists() else {}

total = len(imports)
ebay_published = sum(1 for x in imports.values() if x.get("ebay_status") == "published")
shopify_created = sum(1 for x in imports.values() if x.get("product_id"))
hunter = sum(1 for x in imports.values() if x.get("source") == "ai_hunter")
sales = sum(int(x.get("sales", 0) or 0) for x in imports.values())
revenue = sum(float(x.get("revenue", 0) or 0) for x in imports.values())
profit = sum(float(x.get("profit", 0) or 0) for x in imports.values())

print("=== CHANNEL HEALTH REPORT ===")
print("TOTAL SKUS:", total)
print("SHOPIFY PRODUCTS:", shopify_created)
print("EBAY PUBLISHED:", ebay_published)
print("AI HUNTER SKUS:", hunter)
print("BLOCKED PRODUCTS:", len(blocked))
print("TRACKED STOCK SKUS:", len(stock))
print("META FEED:", "OK" if META.exists() else "MISSING")
print("GOOGLE FEED:", "OK" if GOOGLE.exists() else "MISSING")
print("SALES:", sales)
print("REVENUE:", revenue)
print("PROFIT:", profit)

print()
print("STATUS:", "OK" if total > 0 and ebay_published > 0 and len(blocked) == 0 else "CHECK")
