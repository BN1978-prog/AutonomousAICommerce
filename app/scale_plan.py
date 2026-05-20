import json
from pathlib import Path
from datetime import datetime, timezone

BOARD=Path("app/logs/performance_board.json")
OUT=Path("app/logs/scale_plan.json")

board=json.loads(BOARD.read_text(encoding="utf-8"))

plan=[]

for item in board["winners"]:
    plan.append({
        "sku":item["sku"],
        "title":item["title"],
        "score":item["score"],
        "action":"scale",
        "budget_multiplier":1.5,
        "priority":"high",
        "channels":[
            "shopify",
            "ebay",
            "woocommerce",
            "meta_feed",
            "google_feed"
        ],
        "created_at":datetime.now(timezone.utc).isoformat()
    })

OUT.write_text(json.dumps(plan,indent=2),encoding="utf-8")

print("SCALE PLAN:",len(plan))
