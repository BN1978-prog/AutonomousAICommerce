import json
import os
from pathlib import Path
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

wc_url = os.getenv("WOOCOMMERCE_URL","").rstrip("/")
ck = os.getenv("WOOCOMMERCE_CONSUMER_KEY","")
cs = os.getenv("WOOCOMMERCE_CONSUMER_SECRET","")

products = [
    {
        "id":17,
        "image":"https://placehold.co/800x800/png?text=Eco+Cat+Toy"
    },
    {
        "id":18,
        "image":"https://placehold.co/800x800/png?text=Pet+Bowl"
    }
]

results=[]

for p in products:
    r = requests.put(
        f"{wc_url}/wp-json/wc/v3/products/{p['id']}",
        auth=(ck,cs),
        json={
            "images":[
                {"src":p["image"]}
            ]
        },
        timeout=30
    )

    try:
        data=r.json()
    except:
        data={"raw":r.text}

    results.append({
        "id":p["id"],
        "ok":r.status_code in [200,201],
        "status_code":r.status_code,
        "images_count":len(data.get("images",[]))
    })

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "results":results,
    "status":"WOOCOMMERCE_PLACEHOLDER_IMAGES_ATTEMPTED"
}

Path("app/logs/woocommerce_placeholder_images.json").write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print(json.dumps(report,indent=2))
