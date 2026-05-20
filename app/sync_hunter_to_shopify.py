import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

from app.main import dashboard_shopify_safe_create_or_update

IMPORTS = Path("app/logs/imported_skus.json")

data = json.loads(IMPORTS.read_text(encoding="utf-8"))

created = 0
existing = 0
skipped = 0
failed = 0

for sku, meta in data.items():
    if meta.get("source") != "ai_hunter":
        continue

    if meta.get("product_id"):
        skipped += 1
        continue

    payload = {
        "sku": sku,
        "title": meta.get("title") or "AI Selected Pet Product",
        "shopify_title": meta.get("title") or "AI Selected Pet Product",
        "description": meta.get("description") or "AI selected product discovered by Product Hunter.",
        "price": str(meta.get("last_price") or 9.99),
        "tags": ["ai-hunter", "pet", "autonomous-commerce"],
        "image": meta.get("image") or None,
        "force_real": True
    }

    result = dashboard_shopify_safe_create_or_update(payload)

    if result.get("product_id"):
        meta["product_id"] = result.get("product_id")
        meta["shopify_status"] = result.get("status")
        meta["shopify_sync"] = result.get("mode", "created_or_existing")
        existing += 1
        continue

    product_id = (
        result.get("result", {})
        .get("response", {})
        .get("product", {})
        .get("id")
    )

    if product_id:
        meta["product_id"] = product_id
        meta["shopify_status"] = (
            result.get("result", {})
            .get("response", {})
            .get("product", {})
            .get("status")
        )
        meta["shopify_sync"] = "created"
        created += 1
    else:
        meta["shopify_sync"] = "failed"
        meta["shopify_error"] = str(result)[:1000]
        failed += 1

IMPORTS.write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)

print("HUNTER SHOPIFY SYNC")
print("CREATED:", created)
print("EXISTING:", existing)
print("SKIPPED:", skipped)
print("FAILED:", failed)
