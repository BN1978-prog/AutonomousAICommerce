import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/compliance_layer.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

quality = read_json("app/logs/product_quality_filter.json")
opportunities = read_json("app/logs/global_arbitrage_engine.json")

items = opportunities.get("top_opportunities", [])

restricted_keywords = [
    "drug",
    "medicine",
    "medical",
    "treatment",
    "cure",
    "weight loss",
    "supplement",
    "nicotine",
    "alcohol",
    "weapon",
    "knife",
    "gun",
    "adult",
    "casino",
    "gambling",
    "hair growth"
]

approved = []
blocked = []

for item in items:
    title = str(item.get("title", "")).lower()
    reasons = []

    for keyword in restricted_keywords:
        if keyword in title:
            reasons.append("restricted_or_sensitive_keyword_" + keyword.replace(" ", "_"))

    if reasons:
        blocked.append({
            "sku": item.get("sku"),
            "title": item.get("title"),
            "reasons": reasons,
            "status": "blocked_by_compliance"
        })
    else:
        approved.append({
            "sku": item.get("sku"),
            "title": item.get("title"),
            "status": "compliance_approved"
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "items_seen": len(items),
    "approved_count": len(approved),
    "blocked_count": len(blocked),
    "approved": approved,
    "blocked": blocked,
    "status": "COMPLIANCE_OK" if not blocked else "COMPLIANCE_BLOCKS_PRESENT"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
