import json
import os
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

wc_url = os.getenv("WOOCOMMERCE_URL", "").rstrip("/")
ck = os.getenv("WOOCOMMERCE_CONSUMER_KEY", "")
cs = os.getenv("WOOCOMMERCE_CONSUMER_SECRET", "")

OUT = Path("app/logs/woocommerce_local_image_upload.json")

items = [
    {
        "product_id": 17,
        "file": "app/generated_images/eco_cat_toy.png",
        "filename": "eco_cat_toy.png"
    },
    {
        "product_id": 18,
        "file": "app/generated_images/pet_bowl.png",
        "filename": "pet_bowl.png"
    }
]

results = []

for item in items:
    path = Path(item["file"])

    if not path.exists():
        results.append({
            "product_id": item["product_id"],
            "ok": False,
            "error": "image_file_missing"
        })
        continue

    try:
        media_url = f"{wc_url}/wp-json/wp/v2/media"

        headers = {
            "Content-Disposition": f'attachment; filename="{item["filename"]}"',
            "Content-Type": "image/png"
        }

        media_response = requests.post(
            media_url,
            auth=(ck, cs),
            headers=headers,
            data=path.read_bytes(),
            timeout=60
        )

        try:
            media_data = media_response.json()
        except:
            media_data = {"raw": media_response.text}

        media_id = media_data.get("id")
        source_url = media_data.get("source_url")

        if media_response.status_code not in [200, 201] or not media_id:
            results.append({
                "product_id": item["product_id"],
                "ok": False,
                "media_status_code": media_response.status_code,
                "media_response": media_data
            })
            continue

        product_response = requests.put(
            f"{wc_url}/wp-json/wc/v3/products/{item['product_id']}",
            auth=(ck, cs),
            json={"images": [{"id": media_id}]},
            timeout=60
        )

        try:
            product_data = product_response.json()
        except:
            product_data = {"raw": product_response.text}

        results.append({
            "product_id": item["product_id"],
            "ok": product_response.status_code in [200, 201],
            "media_id": media_id,
            "source_url": source_url,
            "product_status_code": product_response.status_code,
            "images_count": len(product_data.get("images", []))
        })

    except Exception as e:
        results.append({
            "product_id": item["product_id"],
            "ok": False,
            "error": str(e)
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "results": results,
    "status": "WOOCOMMERCE_LOCAL_IMAGE_UPLOAD_ATTEMPTED"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
