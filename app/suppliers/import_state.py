import json
from pathlib import Path

IMPORT_STATE_FILE = Path(r"C:\Users\omen\AutonomousAICommerce\app\logs\imported_skus.json")

def load_imported_skus():
    if not IMPORT_STATE_FILE.exists():
        return {}

    try:
        return json.loads(IMPORT_STATE_FILE.read_text(encoding="utf-8-sig"))
    except Exception as e:
        print(f"Failed to read import state: {e}")
        return {}

def get_imported_sku(sku):
    return load_imported_skus().get(sku)

def save_imported_sku(sku, product_id=None, image_status="unknown"):
    IMPORT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = load_imported_skus()
    data[sku] = {
        "product_id": product_id,
        "status": "imported",
        "image_status": image_status
    }
    IMPORT_STATE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def sku_already_imported(sku):
    return sku in load_imported_skus()
