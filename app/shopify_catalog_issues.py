import json
from pathlib import Path
from collections import Counter

src = Path("app/logs/shopify_product_report.json")
data = json.loads(src.read_text(encoding="utf-8"))

items = data.get("items", [])

title_counts = Counter(i["title"] for i in items)

problems = []

for item in items:
    flags = []

    if item.get("status") != "active":
        flags.append("NOT_ACTIVE")

    if item.get("images", 0) == 0:
        flags.append("NO_IMAGES")

    if title_counts[item["title"]] > 1:
        flags.append("DUPLICATE_TITLE")

    if flags:
        problems.append({
            **item,
            "flags": flags
        })

report = {
    "products_checked": len(items),
    "problem_products": len(problems),
    "items": problems,
    "status": "SHOPIFY_CATALOG_ISSUES_READY"
}

out = Path("app/logs/shopify_catalog_issues.json")
out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

print(json.dumps(report, indent=2, ensure_ascii=False))
