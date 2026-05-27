import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/pet_niche_filter.json")

REGISTRY_FILES = [
    Path("app/logs/shopify_registry_hydrator.json"),
    Path("app/logs/registry_quality_report.json")
]

pet_keywords = [
    "pet", "dog", "cat", "puppy", "kitten", "leash", "collar",
    "harness", "bowl", "feeder", "scratcher", "grooming",
    "brush", "comb", "carrier", "blanket", "bed", "toy",
    "water bottle", "raincoat", "socks", "tunnel"
]

risky_non_pet_keywords = [
    "hair growth",
    "microneedle",
    "tea cup",
    "glass tea",
    "regeneration",
    "solution"
]

def read_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return None

items = []

for f in REGISTRY_FILES:
    data = read_json(f)

    if isinstance(data, list):
        items.extend(data)

    if isinstance(data, dict):
        for key in ["items", "results", "products"]:
            if isinstance(data.get(key), list):
                items.extend(data.get(key))

seen = set()
approved = []
flagged = []

for item in items:
    sku = item.get("sku") or item.get("product_id") or item.get("id")
    title = str(item.get("title") or item.get("name") or "").lower()

    if not sku or sku in seen:
        continue

    seen.add(sku)

    pet_match = any(k in title for k in pet_keywords)
    risky_match = [k for k in risky_non_pet_keywords if k in title]

    if pet_match and not risky_match:
        approved.append({
            "sku": sku,
            "title": item.get("title") or item.get("name"),
            "status": "pet_niche_approved"
        })
    else:
        flagged.append({
            "sku": sku,
            "title": item.get("title") or item.get("name"),
            "pet_match": pet_match,
            "risky_keywords": risky_match,
            "status": "flagged_review_required"
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "review_only_no_delete_no_shopify_change",
    "items_seen": len(seen),
    "approved_count": len(approved),
    "flagged_count": len(flagged),
    "approved": approved,
    "flagged": flagged,
    "status": "PET_NICHE_FILTER_REVIEW_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
