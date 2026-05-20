import json
from pathlib import Path

RAW_DIR = Path(r"C:\Users\omen\AutonomousAICommerce\app\logs\supplier_raw")

def main():
    print("=== PROFIT REPORT ===")

    if not RAW_DIR.exists():
        print("No supplier raw logs found.")
        return

    latest_by_sku = {}

    for file in sorted(RAW_DIR.glob("*.json")):
        try:
            raw = json.loads(file.read_text(encoding="utf-8-sig"))
            sku = raw.get("sku", "unknown")
            latest_by_sku[sku] = raw
        except Exception:
            pass

    total_profit = 0

    for sku, raw in latest_by_sku.items():
        cost = float(raw.get("price") or raw.get("cost") or 0)
        sell_price = max(cost * 1.35, cost + 5.00)
        profit = sell_price - cost
        margin = (profit / sell_price * 100) if sell_price else 0

        total_profit += profit

        print(f"{sku}: cost={cost:.2f}, sell={sell_price:.2f}, profit={profit:.2f}, margin={margin:.2f}%")

    print()
    print(f"Unique SKUs analysed: {len(latest_by_sku)}")
    print(f"Estimated total profit per 1 unit each: {total_profit:.2f}")

if __name__ == "__main__":
    main()
