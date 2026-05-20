import json
from pathlib import Path
from datetime import datetime, timezone

GOOGLE=Path("app/logs/google_ads_readiness.json")
META=Path("app/logs/meta_ads_readiness.json")
OUT=Path("app/logs/paid_ads_status.json")

google=json.loads(GOOGLE.read_text(encoding="utf-8")) if GOOGLE.exists() else {}
meta=json.loads(META.read_text(encoding="utf-8")) if META.exists() else {}

google_ok=google.get("ok",False)
meta_ok=meta.get("ok",False)

status={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "google_ads":{
        "ok":google_ok,
        "status":google.get("status","missing_env")
    },
    "meta_ads":{
        "ok":meta_ok,
        "status":meta.get("status","missing_env")
    },
    "paid_ads_ready":google_ok or meta_ok,
    "fully_paid_ads_ready":google_ok and meta_ok,
    "active_paid_sources":[
        x for x,ok in {
            "google_ads":google_ok,
            "meta_ads":meta_ok
        }.items()
        if ok
    ],
    "reason":"at_least_one_paid_source_ready" if (google_ok or meta_ok) else "waiting_valid_google_meta_credentials"
}

OUT.write_text(json.dumps(status,indent=2),encoding="utf-8")

print(json.dumps(status,indent=2))
