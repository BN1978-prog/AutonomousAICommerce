import json
from pathlib import Path
from datetime import datetime, timezone

IMPORTS = Path("app/logs/imported_skus.json")

data = json.loads(IMPORTS.read_text(encoding="utf-8"))
now = datetime.now(timezone.utc).isoformat()

added = 0

for sku, meta in data.items():
    if "created_at" not in meta:
        meta["created_at"] = now
        added += 1

IMPORTS.write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)

print("CREATED_AT ADDED:", added)
