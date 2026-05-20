from app.suppliers.stock_state import load_stock_state

def main():
    data = load_stock_state()

    print("=== STOCK REPORT ===")
    print(f"Tracked SKUs: {len(data)}")

    out_of_stock = []

    for sku, item in data.items():
        inventory = int(item.get("inventory", 0))
        print(f"{sku}: {inventory}")

        if inventory <= 0:
            out_of_stock.append(sku)

    if out_of_stock:
        print()
        print("Out of stock SKUs:")
        for sku in out_of_stock:
            print(f"- {sku}")

if __name__ == "__main__":
    main()
