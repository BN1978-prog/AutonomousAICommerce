from dotenv import load_dotenv
from app.suppliers.real_supplier import fetch_real_supplier_products

load_dotenv()

def main():
    products = fetch_real_supplier_products()

    print(f"Fetched products: {len(products)}")

    if products:
        print()
        print("=== FIRST PRODUCT SAMPLE ===")
        print(products[0])

if __name__ == "__main__":
    main()
