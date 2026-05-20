import json
from pathlib import Path
from datetime import datetime, timezone

ASSETS=Path("app/logs/meta_business_assets.json")
OUT=Path("app/logs/meta_connection_status.json")

data=json.loads(ASSETS.read_text(encoding="utf-8"))

def count_items(section):
    return len(
        data.get(section,{})
        .get("data",{})
        .get("data",[])
    )

status={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "meta_token_valid":True,
    "business_id":data.get("business_id"),
    "ad_accounts":count_items("owned_ad_accounts")+count_items("client_ad_accounts"),
    "pixels":count_items("owned_pixels"),
    "pages":count_items("owned_pages"),
    "catalogs_available":data.get("owned_product_catalogs",{}).get("ok",False),
    "status":"connected_but_assets_missing",
    "missing":[]
}

if status["ad_accounts"]==0:
    status["missing"].append("META_AD_ACCOUNT_ID")

if status["pixels"]==0:
    status["missing"].append("META_PIXEL_ID")

if status["pages"]==0:
    status["missing"].append("META_PAGE_ID")

if not status["catalogs_available"]:
    status["missing"].append("META_CATALOG_ID_OR_CATALOG_PERMISSION")

OUT.write_text(json.dumps(status,indent=2),encoding="utf-8")

print(json.dumps(status,indent=2))
