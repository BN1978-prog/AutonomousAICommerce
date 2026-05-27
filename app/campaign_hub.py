import json
from pathlib import Path
from datetime import datetime, timezone

SOCIAL=Path("app/logs/social_content_enhanced.json")
META=Path("app/logs/meta_ad_drafts_from_content.json")
GOOGLE=Path("app/logs/google_ad_drafts_from_content.json")
OUT=Path("app/logs/campaign_hub.json")

social=json.loads(SOCIAL.read_text(encoding="utf-8-sig")) if SOCIAL.exists() else {}
meta=json.loads(META.read_text(encoding="utf-8-sig")) if META.exists() else {}
google=json.loads(GOOGLE.read_text(encoding="utf-8-sig")) if GOOGLE.exists() else {}

hub=[]

all_skus=set()

for x in social.get("posts",[]):
    all_skus.add(x["sku"])

for sku in sorted(all_skus):

    social_ok=any(x["sku"]==sku for x in social.get("posts",[]))
    meta_ok=any(x["sku"]==sku for x in meta.get("drafts",[]))
    google_ok=any(x["sku"]==sku for x in google.get("drafts",[]))

    hub.append({
        "sku":sku,
        "social_content_ready":social_ok,
        "meta_draft_ready":meta_ok,
        "google_draft_ready":google_ok,
        "status":"WAITING_MANUAL_APPROVAL"
    })

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "campaigns":hub,
    "campaigns_count":len(hub),
    "status":"CAMPAIGN_HUB_READY"
}

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print(json.dumps(report,indent=2))
