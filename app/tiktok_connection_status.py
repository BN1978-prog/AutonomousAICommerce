import json
import os
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)

OUT=Path("app/logs/tiktok_connection_status.json")

shop_required = [
"TIKTOK_SHOP_APP_KEY",
"TIKTOK_SHOP_APP_SECRET",
"TIKTOK_SHOP_ACCESS_TOKEN",
"TIKTOK_SHOP_REFRESH_TOKEN",
"TIKTOK_SHOP_ID",
"TIKTOK_SHOP_REGION"
]

ads_required = [
"TIKTOK_ADS_ACCESS_TOKEN",
"TIKTOK_ADS_ADVERTISER_ID",
"TIKTOK_ADS_PIXEL_ID"
]

shop_missing=[x for x in shop_required if not os.getenv(x)]
ads_missing=[x for x in ads_required if not os.getenv(x)]

report={
"created_at":datetime.now(timezone.utc).isoformat(),

"tiktok_shop":{
"missing":shop_missing,
"ready":len(shop_missing)==0
},

"tiktok_ads":{
"missing":ads_missing,
"ready":len(ads_missing)==0
},

"status":
"TIKTOK_FULLY_READY"
if len(shop_missing)==0 and len(ads_missing)==0
else
"TIKTOK_WAITING_CONFIGURATION"
}

OUT.write_text(
json.dumps(report,indent=2),
encoding="utf-8"
)

print(json.dumps(report,indent=2))
