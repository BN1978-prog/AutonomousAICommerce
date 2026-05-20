import json, os, requests
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from datetime import datetime, timezone

IN = Path("app/logs/meta_campaign_live_creator.json")
GUARD = Path("app/logs/meta_api_guard.json")
OUT = Path("app/logs/meta_campaign_live_result.json")

data = json.loads(IN.read_text(encoding="utf-8"))
guard = json.loads(GUARD.read_text(encoding="utf-8"))

token = os.getenv("META_ACCESS_TOKEN")
ad_account = os.getenv("META_AD_ACCOUNT_ID")
api_version = os.getenv("META_GRAPH_API_VERSION", "v20.0")

results = []
blocked = []

if not guard.get("meta_live_api_enabled"):
    blocked.append({"reason": "meta_live_api_enabled_false"})
elif not token or not ad_account:
    blocked.append({"reason": "missing_META_ACCESS_TOKEN_or_META_AD_ACCOUNT_ID"})
else:
    for p in data.get("payloads", [])[: int(guard.get("max_campaigns_per_run", 2))]:
        budget = float(p.get("daily_budget", 0))
        if budget > float(guard.get("max_daily_budget", 5)):
            blocked.append({**p, "reason": "budget_above_limit"})
            continue

        url = f"https://graph.facebook.com/{api_version}/{ad_account}/campaigns"
        payload = {
            "name": p["campaign_name"],
            "objective": p.get("objective", "OUTCOME_SALES"),
            "status": "PAUSED",
            "is_adset_budget_sharing_enabled": False,
            "special_ad_categories": "[]",
            "access_token": token
        }

        r = requests.post(url, data=payload, timeout=30)
        results.append({
            "sku": p.get("sku"),
            "campaign_name": p["campaign_name"],
            "status_code": r.status_code,
            "ok": r.ok,
            "response": r.json() if r.text else {}
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "meta_live_api_create_paused_campaigns",
    "blocked": blocked,
    "results": results,
    "created": len([x for x in results if x.get("ok")]),
    "status": "ok" if results and all(x.get("ok") for x in results) else ("blocked" if blocked else "error")
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))


