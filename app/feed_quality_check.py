import json
from pathlib import Path

FILES = [
    Path("app/logs/meta_feed_seo.json"),
    Path("app/logs/google_feed_seo.json")
]

required = ["sku", "title", "description", "price", "image", "product_url"]

for file in FILES:
    data = json.loads(file.read_text(encoding="utf-8")) if file.exists() else []

    print("FEED:", file)
    print("ITEMS:", len(data))

    for item in data:
        missing = [x for x in required if item.get(x) in [None, "", []]]
        print(item.get("sku"), "ok=", len(missing) == 0, "missing=", ",".join(missing))
