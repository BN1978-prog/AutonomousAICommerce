import json
from pathlib import Path

IMPORTS = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/registry_quality_report.json")

data = json.loads(IMPORTS.read_text(encoding="utf-8")) if IMPORTS.exists() else {}

required_fields = [
    "title",
    "description",
    "price",
    "image",
    "product_url"
]

report = []

for sku, item in data.items():
    missing = [
        field for field in required_fields
        if item.get(field) in [None, "", []]
    ]

    report.append({
        "sku": sku,
        "ok": len(missing) == 0,
        "missing_fields": missing,
        "title": item.get("title")
    })

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print("REGISTRY QUALITY REPORT:", len(report))

for r in report:
    print(r["sku"], "ok=", r["ok"], "missing=", ",".join(r["missing_fields"]))
