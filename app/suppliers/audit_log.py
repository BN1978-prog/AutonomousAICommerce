import json
from datetime import datetime
from pathlib import Path

AUDIT_DIR = Path(r"C:\Users\omen\AutonomousAICommerce\app\logs\supplier_raw")

def save_supplier_raw_log(raw_product):
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    sku = raw_product.get("sku", "unknown")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = AUDIT_DIR / f"{timestamp}_{sku}.json"

    file_path.write_text(
        json.dumps(raw_product, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    return str(file_path)
