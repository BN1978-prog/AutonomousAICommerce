import json
from pathlib import Path

BLOCKED_FILE = Path(r"C:\Users\omen\AutonomousAICommerce\app\logs\blocked_products.json")

def main():
    print("=== BLOCKED PRODUCTS REPORT ===")

    if not BLOCKED_FILE.exists():
        print("No blocked products found.")
        return

    data = json.loads(BLOCKED_FILE.read_text(encoding="utf-8-sig"))

    print(f"Total blocked products: {len(data)}")

    issue_counts = {}

    for item in data:
        for issue in item.get("issues", []):
            issue_counts[issue] = issue_counts.get(issue, 0) + 1

    print()
    print("=== ISSUE SUMMARY ===")

    for issue, count in issue_counts.items():
        print(f"{issue}: {count}")

    print()
    print("=== BLOCKED SKUS ===")

    for item in data:
        print(f"{item['sku']} -> {', '.join(item['issues'])}")

if __name__ == "__main__":
    main()
