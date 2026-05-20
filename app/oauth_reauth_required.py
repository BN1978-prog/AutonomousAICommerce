import json
from pathlib import Path
from datetime import datetime, timezone

STATUS=Path("app/logs/token_manager_status.json")
OUT=Path("app/logs/oauth_reauth_required.json")

data=json.loads(STATUS.read_text(encoding="utf-8"))

items=[]

for r in data.get("results",[]):

    if r.get("ok"):
        continue

    provider=r.get("provider")
    status=r.get("status")

    if provider=="google_ads":
        items.append({
            "provider":"google_ads",
            "status":status,
            "required_env":[
                "GOOGLE_ADS_REFRESH_TOKEN",
                "GOOGLE_ADS_CLIENT_ID",
                "GOOGLE_ADS_CLIENT_SECRET",
                "GOOGLE_ADS_DEVELOPER_TOKEN",
                "GOOGLE_ADS_CUSTOMER_ID"
            ],
            "action":"complete_google_oauth_once_then_token_manager_will_auto_refresh"
        })

    elif provider=="meta":
        items.append({
            "provider":"meta",
            "status":status,
            "required_env":[
                "META_ACCESS_TOKEN",
                "META_APP_ID",
                "META_APP_SECRET",
                "META_AD_ACCOUNT_ID",
                "META_PIXEL_ID"
            ],
            "action":"generate_new_meta_token_once_then_token_manager_can_extend_if_app_credentials_exist"
        })

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "reauth_required":len(items)>0,
    "items":items
}

OUT.write_text(json.dumps(report,indent=2),encoding="utf-8")

print(json.dumps(report,indent=2))
