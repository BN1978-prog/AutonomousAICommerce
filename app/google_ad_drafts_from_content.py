import json
from pathlib import Path
from datetime import datetime, timezone

SRC=Path("app/logs/social_content_enhanced.json")
OUT=Path("app/logs/google_ad_drafts_from_content.json")

data=json.loads(
    SRC.read_text(encoding="utf-8-sig")
) if SRC.exists() else {}

drafts=[]

for p in data.get("posts",[]):

    sku=p["sku"]

    drafts.append({
        "sku":sku,
        "headline":sku.replace("_"," ").title()[:30],
        "description":p["post_text"][:90],
        "status":"PAUSED_DRAFT",
        "mode":"draft_only_no_spend"
    })

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "drafts_created":len(drafts),
    "drafts":drafts,
    "live_money_spending":False,
    "status":"GOOGLE_AD_DRAFTS_READY"
}

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print(json.dumps(report,indent=2))
