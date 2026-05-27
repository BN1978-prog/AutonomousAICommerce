import csv, json, hashlib, shutil
from pathlib import Path
from datetime import datetime, timezone

PERFORMANCE = Path("app/logs/product_performance.json")
SALES_CSV = Path("app/logs/shopify_sales.csv")
IMPORT_LOG = Path("app/logs/imported_sales_files.json")
ARCHIVE_DIR = Path("app/logs/imported_sales_archive")
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

if not PERFORMANCE.exists():
    print("Missing product_performance.json")
    raise SystemExit

if not SALES_CSV.exists():
    SALES_CSV.write_text(
        "product_id,sales,clicks\n"
        "pet_bowl,0,0\n"
        "cat_tunnel,0,0\n"
        "grooming_brush,0,0\n"
        "slow_feeder,0,0\n",
        encoding="utf-8"
    )
    print("Created template:", SALES_CSV)
    raise SystemExit

raw = SALES_CSV.read_bytes()
file_hash = hashlib.sha256(raw).hexdigest()

if IMPORT_LOG.exists():
    imported = json.loads(IMPORT_LOG.read_text(encoding="utf-8-sig"))
else:
    imported = []

if file_hash in {x.get("hash") for x in imported}:
    print("Sales file already imported. Skipping:", SALES_CSV)
    raise SystemExit

performance = json.loads(PERFORMANCE.read_text(encoding="utf-8-sig"))

with SALES_CSV.open("r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        product_id = row["product_id"].strip()
        sales = int(row.get("sales") or 0)
        clicks = int(row.get("clicks") or 0)

        if product_id not in performance:
            performance[product_id] = {
                "published": 0,
                "clicks": 0,
                "sales": 0,
                "score": 0
            }

        performance[product_id]["sales"] += sales
        performance[product_id]["clicks"] += clicks
        performance[product_id]["score"] = (
            performance[product_id]["clicks"] +
            performance[product_id]["sales"] * 10
        )

PERFORMANCE.write_text(json.dumps(performance, indent=2), encoding="utf-8")

imported.append({
    "created_at": datetime.now(timezone.utc).isoformat(),
    "file": str(SALES_CSV),
    "hash": file_hash
})
IMPORT_LOG.write_text(json.dumps(imported, indent=2), encoding="utf-8")

archive_name = ARCHIVE_DIR / f"shopify_sales_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv"
shutil.copy2(SALES_CSV, archive_name)

SALES_CSV.write_text(
    "product_id,sales,clicks\n"
    "pet_bowl,0,0\n"
    "cat_tunnel,0,0\n"
    "grooming_brush,0,0\n"
    "slow_feeder,0,0\n",
    encoding="utf-8"
)

print("Imported Shopify/UTM results once and reset CSV.")
print(json.dumps(performance, indent=2))
