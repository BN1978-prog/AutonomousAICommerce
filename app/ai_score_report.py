import json
from pathlib import Path

from app.suppliers.normalize_product import normalize_supplier_product
from app.suppliers.ai_product_score import score_product

RAW_DIR = Path(r"C:\Users\omen\AutonomousAICommerce\app\logs\supplier_raw")

def main():
    print("=== AI PRODUCT SCORE REPORT ===")

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

    approved = 0
    blocked = 0

    for sku, raw in latest_by_sku.items():
        try:
            normalized = normalize_supplier_product(raw)
            score = score_product(normalized)

            status = "APPROVED" if score["approved"] else "BLOCKED"

            if score["approved"]:
                approved += 1
            else:
                blocked += 1

            print(f"{sku}: {status} score={score['score']} reasons={', '.join(score['reasons'])}")

        except Exception as e:
            print(f"{sku}: ERROR {e}")

    print()
    print(f"Approved: {approved}")
    print(f"Blocked: {blocked}")

if __name__ == "__main__":
    main()
