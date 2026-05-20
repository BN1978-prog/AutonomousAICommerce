import json
from pathlib import Path

from app.suppliers.normalize_product import normalize_supplier_product
from app.suppliers.seo_mapper import build_seo_tags, detect_product_type

RAW_DIR = Path(r"C:\Users\omen\AutonomousAICommerce\app\logs\supplier_raw")

def main():
    print("=== SEO REPORT ===")

    latest_by_sku = {}

    if not RAW_DIR.exists():
        print("No supplier raw logs found.")
        return

    for file in sorted(RAW_DIR.glob("*.json")):
        try:
            raw = json.loads(file.read_text(encoding="utf-8-sig"))
            sku = raw.get("sku", "unknown")
            latest_by_sku[sku] = raw
        except Exception:
            pass

    for sku, raw in latest_by_sku.items():
        try:
            normalized = normalize_supplier_product(raw)
        except Exception:
            continue
        product_type = detect_product_type(normalized)
        tags = build_seo_tags(normalized)

        print()
        print(f"SKU: {sku}")
        print(f"Title: {normalized['title']}")
        print(f"Product type: {product_type}")
        print(f"Tags: {', '.join(tags)}")

if __name__ == "__main__":
    main()
