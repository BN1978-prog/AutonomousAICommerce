import os, json, base64, mimetypes
from pathlib import Path
import requests

WP_BASE_URL = os.environ["WP_BASE_URL"].rstrip("/")
WP_USER = os.environ["WP_USER"]
WP_APP_PASSWORD = os.environ["WP_APP_PASSWORD"]
WC_KEY = os.environ["WC_CONSUMER_KEY"]
WC_SECRET = os.environ["WC_CONSUMER_SECRET"]

PRODUCTS = [
    {
        "id": 17,
        "sku": "CJJJCWMY00923",
        "title": "Eco-Friendly Cat Scratcher Toy",
        "image_path": "app/assets/product_images/CJJJCWMY00923.jpg"
    },
    {
        "id": 18,
        "sku": "PET-BOWL-001",
        "title": "Non-slip silicone pet feeding bowl",
        "image_path": "app/assets/product_images/PET-BOWL-001.jpg"
    }
]

def wp_headers(filename):
    token = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
    mime = mimetypes.guess_type(filename)[0] or "image/jpeg"
    return {
        "Authorization": f"Basic {token}",
        "Content-Disposition": f'attachment; filename="{Path(filename).name}"',
        "Content-Type": mime,
    }

def upload_media(image_path, title):
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    url = f"{WP_BASE_URL}/wp-json/wp/v2/media"
    response = requests.post(
        url,
        headers=wp_headers(path.name),
        data=path.read_bytes(),
        timeout=60
    )

    if response.status_code not in (200, 201):
        raise RuntimeError(f"Media upload failed {response.status_code}: {response.text}")

    media = response.json()
    return media["id"], media.get("source_url")

def update_product_image(product_id, media_id):
    url = f"{WP_BASE_URL}/wp-json/wc/v3/products/{product_id}"
    response = requests.put(
        url,
        auth=(WC_KEY, WC_SECRET),
        json={"images": [{"id": media_id}]},
        timeout=60
    )

    if response.status_code not in (200, 201):
        raise RuntimeError(f"Product update failed {response.status_code}: {response.text}")

    return response.json()

results = []

for product in PRODUCTS:
    try:
        media_id, source_url = upload_media(product["image_path"], product["title"])
        updated = update_product_image(product["id"], media_id)

        results.append({
            "product_id": product["id"],
            "sku": product["sku"],
            "title": product["title"],
            "media_id": media_id,
            "image_url": source_url,
            "status": "IMAGE_UPLOADED_AND_ASSIGNED"
        })

        print(f"OK: {product['title']} -> media {media_id}")

    except Exception as e:
        results.append({
            "product_id": product["id"],
            "sku": product["sku"],
            "title": product["title"],
            "status": "FAILED",
            "error": str(e)
        })
        print(f"FAILED: {product['title']} -> {e}")

out = Path("app/logs/woocommerce_image_auto_upload_report.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

print(json.dumps(results, indent=2, ensure_ascii=False))
