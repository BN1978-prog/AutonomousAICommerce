import json
from pathlib import Path
from datetime import datetime, timezone

SRC = Path("app/logs/social_content_enhanced.json")
OUT = Path("app/logs/meta_ad_drafts_from_content.json")

data = json.loads(SRC.read_text(encoding="utf-8-sig")) if SRC.exists() else {}

drafts = []

for p in data.get("posts", []):
    drafts.append({
        "sku": p.get("sku"),
        "platforms": ["facebook", "instagram"],
        "primary_text": p.get("post_text"),
        "headline": p.get("sku", "").replace("_", " ").title()[:40],
        "cta": "SHOP_NOW",
        "status": "PAUSED_DRAFT",
        "mode": "draft_only_no_spend"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "drafts_created": len(drafts),
    "drafts": drafts,
    "live_money_spending": False,
    "status": "META_AD_DRAFTS_FROM_CONTENT_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
