import json
from pathlib import Path

IMPORTS = Path("app/logs/imported_skus.json")

data = json.loads(IMPORTS.read_text(encoding="utf-8"))

for sku, meta in data.items():
    meta["ebay_sales"] = int(meta.get("ebay_sales") or 0)
    meta["sales"] = int(meta.get("shopify_sales") or 0) + int(meta.get("ebay_sales") or 0)

IMPORTS.write_text(json.dumps(data, indent=2), encoding="utf-8")

print("EBAY SALES SYNC PLACEHOLDER OK")
print("NOTE: Real eBay order API sync can be added after verifying sell.fulfillment scope")
