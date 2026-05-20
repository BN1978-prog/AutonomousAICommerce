from app.suppliers.import_state import load_imported_skus
from app.suppliers.stock_state import load_stock_state
import json
from pathlib import Path

BLOCKED_FILE = Path(r"C:\Users\omen\AutonomousAICommerce\app\logs\blocked_products.json")

def main():
    imported = load_imported_skus()
    stock = load_stock_state()

    blocked = []
    if BLOCKED_FILE.exists():
        blocked = json.loads(BLOCKED_FILE.read_text(encoding="utf-8-sig"))

    image_failed = [
        sku for sku, item in imported.items()
        if item.get("image_status") == "failed"
    ]

    out_of_stock = [
        sku for sku, item in stock.items()
        if int(item.get("inventory", 0)) <= 0
    ]

    print("=== AUTONOMOUS AI COMMERCE DASHBOARD ===")
    print()
    print(f"Imported SKUs: {len(imported)}")
    print(f"Tracked stock SKUs: {len(stock)}")
    print(f"Blocked products: {len(blocked)}")
    print(f"Image failed SKUs: {len(image_failed)}")
    print(f"Out of stock SKUs: {len(out_of_stock)}")

    if image_failed:
        print()
        print("Image review needed:")
        for sku in image_failed:
            print(f"- {sku}")

    if out_of_stock:
        print()
        print("Out of stock:")
        for sku in out_of_stock:
            print(f"- {sku}")

    if blocked:
        print()
        print("Recently blocked:")
        for item in blocked[-5:]:
            print(f"- {item.get('sku')} -> {', '.join(item.get('issues', []))}")

if __name__ == "__main__":
    main()
