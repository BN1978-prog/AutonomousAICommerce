from app.suppliers.import_state import load_imported_skus

def main():
    data = load_imported_skus()

    total = len(data)
    image_failed = [
        sku for sku, item in data.items()
        if item.get("image_status") == "failed"
    ]

    print("=== IMPORT REPORT ===")
    print(f"Total imported SKUs: {total}")
    print(f"Image failed: {len(image_failed)}")

    if image_failed:
        print()
        print("SKUs requiring image review:")
        for sku in image_failed:
            print(f"- {sku}")

if __name__ == "__main__":
    main()
