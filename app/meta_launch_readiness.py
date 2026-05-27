import json
from pathlib import Path
from datetime import datetime, timezone

FILES = {
    "campaigns": "app/logs/meta_campaign_registry.json",
    "adsets": "app/logs/meta_adset_live_creator.json",
    "creatives": "app/logs/meta_creative_live_creator.json",
    "ads": "app/logs/meta_ads_live_creator.json",
}

def load(path):
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

data = {k: load(v) for k, v in FILES.items()}

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "campaigns_registered": data["campaigns"].get("campaigns_registered", 0),
    "adsets_ready": data["adsets"].get("adsets_created", 0),
    "creatives_ready": data["creatives"].get("creatives_created", 0),
    "ads_ready": data["ads"].get("ads_created", 0),
    "all_statuses": {
        "campaigns": data["campaigns"].get("status"),
        "adsets": data["adsets"].get("status"),
        "creatives": data["creatives"].get("status"),
        "ads": data["ads"].get("status")
    },
    "live_money_spending": False,
    "launch_mode": "PAUSED_ONLY_SAFE_MODE",
    "status": "META_FUNNEL_READY_PAUSED" if (
        data["campaigns"].get("campaigns_registered", 0) > 0 and
        data["adsets"].get("adsets_created", 0) > 0 and
        data["creatives"].get("creatives_created", 0) > 0 and
        data["ads"].get("ads_created", 0) > 0
    ) else "META_FUNNEL_INCOMPLETE"
}

Path("app/logs/meta_launch_readiness.json").write_text(
    json.dumps(report, indent=2), encoding="utf-8"
)

print(json.dumps(report, indent=2))
