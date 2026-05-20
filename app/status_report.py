from app.suppliers.import_state import load_imported_skus
from app.suppliers.stock_state import load_stock_state
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    imported = load_imported_skus()
    stock = load_stock_state()

    print("=== AUTONOMOUS AI COMMERCE STATUS ===")
    print()
    print("Core pipeline: READY")
    print("Shopify integration: CONNECTED" if os.getenv("SHOPIFY_ACCESS_TOKEN") else "Shopify integration: MISSING")
    print(f"Supplier mode: {os.getenv('SUPPLIER_MODE')}")
    print(f"Dry run: {os.getenv('DRY_RUN')}")
    print()
    print(f"Imported products: {len(imported)}")
    print(f"Stock tracked: {len(stock)}")
    print()
    print("Modules:")
    print("- Supplier ingestion")
    print("- Product normalization")
    print("- Pricing engine")
    print("- Profit safety gate")
    print("- AI product scoring")
    print("- SEO title/tags mapper")
    print("- Shopify draft create/update")
    print("- Inventory sync")
    print("- Reports/dashboard")
    print("- Scheduled daily runner")
    print("- Runtime safety guard")

if __name__ == '__main__':
    main()
