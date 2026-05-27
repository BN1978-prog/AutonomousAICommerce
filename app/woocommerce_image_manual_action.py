import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/woocommerce_image_manual_action.json")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "reason": "WordPress Media API returned 401 rest_cannot_create",
    "products": [
        {
            "id": 17,
            "sku": "CJJJCWMY00923",
            "title": "Eco-Friendly Cat Scratcher Toy",
            "action_required": "Upload product image manually in WordPress/WooCommerce media editor"
        },
        {
            "id": 18,
            "sku": "PET-BOWL-001",
            "title": "Non-slip silicone pet feeding bowl",
            "action_required": "Upload product image manually in WordPress/WooCommerce media editor"
        }
    ],
    "status": "WOOCOMMERCE_IMAGES_REQUIRE_MANUAL_UPLOAD"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
