import os
from dotenv import load_dotenv

load_dotenv()

def check(name, ok, fix):
    status = "OK" if ok else "FAIL"
    print(f"{status}: {name}")
    if not ok:
        print(f"  fix: {fix}")

def main():
    print("=== RELEASE CHECKLIST ===")

    dry_run = os.getenv("DRY_RUN", "true").lower()
    supplier_mode = os.getenv("SUPPLIER_MODE", "")
    supplier_key = os.getenv("SUPPLIER_API_KEY", "")
    shopify_url = os.getenv("SHOPIFY_STORE_URL", "")
    shopify_token = os.getenv("SHOPIFY_ACCESS_TOKEN", "")

    check("Shopify URL configured", bool(shopify_url), "Set SHOPIFY_STORE_URL")
    check("Shopify token configured", bool(shopify_token), "Set SHOPIFY_ACCESS_TOKEN")
    check("DRY_RUN enabled by default", dry_run == "true", "Set DRY_RUN=true")
    check("Supplier mode selected", bool(supplier_mode), "Set SUPPLIER_MODE")
    check("Real supplier key present only when live", supplier_mode != "real" or bool(supplier_key), "Set SUPPLIER_API_KEY")
    check("Mock/sandbox cannot live run", not (dry_run == "false" and supplier_mode in ["mock_real", "sandbox"]), "Set DRY_RUN=true")

if __name__ == "__main__":
    main()
