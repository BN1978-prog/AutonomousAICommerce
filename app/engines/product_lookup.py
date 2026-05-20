
import json
from pathlib import Path

def find_product_record(sku: str, channel: str="shopify"):
    path = Path("data/published_products") / f"{sku}-{channel}.json"

    if not path.exists():
        return None

    return json.loads(path.read_text(encoding="utf-8"))

