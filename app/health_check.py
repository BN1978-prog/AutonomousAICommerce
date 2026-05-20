import os
from dotenv import load_dotenv

from app.suppliers.import_state import load_imported_skus
from app.suppliers.stock_state import load_stock_state

load_dotenv()

def yes_no(value):
    return "OK" if value else "MISSING"

def main():
    imported = load_imported_skus()
    stock = load_stock_state()

    print("=== SYSTEM HEALTH CHECK ===")
    print(f"DRY_RUN: {os.getenv('DRY_RUN')}")
    print(f"SUPPLIER_MODE: {os.getenv('SUPPLIER_MODE')}")
    print(f"IMPORT_EXISTING_ACTION: {os.getenv('IMPORT_EXISTING_ACTION')}")
    print()
    print(f"Shopify URL: {yes_no(os.getenv('SHOPIFY_STORE_URL'))}")
    print(f"Shopify Token: {yes_no(os.getenv('SHOPIFY_ACCESS_TOKEN'))}")
    print(f"Supplier API URL: {yes_no(os.getenv('SUPPLIER_API_URL'))}")
    print()
    print(f"Imported SKUs: {len(imported)}")
    print(f"Tracked stock SKUs: {len(stock)}")

    image_failed = [
        sku for sku, item in imported.items()
        if item.get('image_status') == 'failed'
    ]

    print(f"Image failed SKUs: {len(image_failed)}")

    if image_failed:
        print()
        for sku in image_failed:
            print(f"- image review needed: {sku}")

if __name__ == '__main__':
    main()
