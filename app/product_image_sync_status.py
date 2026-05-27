import json
from pathlib import Path
from datetime import datetime, timezone

local_file = Path("app/logs/local_product_images.json")

local = json.loads(local_file.read_text(encoding="utf-8")) if local_file.exists() else {}

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "local_images_status": local.get("status", "MISSING"),
    "woocommerce_images_status": "NOT_UPLOADED_TO_MEDIA_LIBRARY",
    "reason": "WooCommerce has products, but WordPress Media API upload requires real WordPress admin/API credentials",
    "next_required_for_full_sync": [
        "Real WordPress/WooCommerce domain",
        "WordPress admin user",
        "WordPress Application Password",
        "WooCommerce REST API consumer key",
        "WooCommerce REST API consumer secret"
    ],
    "products": local.get("products", []),
    "status": "PRODUCT_IMAGES_READY_LOCALLY_NOT_SYNCED"
}

out = Path("app/logs/product_image_sync_status.json")
out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

print(json.dumps(report, indent=2, ensure_ascii=False))
