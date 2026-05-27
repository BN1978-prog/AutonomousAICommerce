import json
from pathlib import Path
from datetime import datetime, timezone

POSTS_FILE = Path("app/logs/daily_social_posts_ready.json")
OUT_JSON = Path("app/logs/daily_social_posts_with_utm.json")
OUT_TXT = Path("app/logs/manual_publish_queue_with_utm.txt")

utm_map = {
    "Non-slip silicone pet feeding bowl": "https://aicommerce-test-store-2.myshopify.com?utm_source=instagram&utm_medium=social&utm_campaign=pet_bowl_test",
    "Foldable Cat Tunnel Toy": "https://aicommerce-test-store-2.myshopify.com?utm_source=pinterest&utm_medium=social&utm_campaign=cat_tunnel_test",
    "British Style Dog Raincoat": "https://aicommerce-test-store-2.myshopify.com?utm_source=facebook&utm_medium=social&utm_campaign=dog_raincoat_test",
}

data = json.loads(POSTS_FILE.read_text(encoding="utf-8"))

updated = []

for post in data["posts"]:
    text = post["text"]

    for product, url in utm_map.items():
        if product.lower() in text.lower() or product.lower() in json.dumps(post).lower():
            text = text.replace("https://aicommerce-test-store-2.myshopify.com", url)

    updated.append({
        **post,
        "text": text
    })

result = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "posts": updated
}

OUT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
OUT_TXT.write_text(
    "\n\n--- POST ---\n\n".join([p["text"] for p in updated]),
    encoding="utf-8"
)

print("UPDATED POSTS:", len(updated))
print("JSON:", OUT_JSON)
print("TXT:", OUT_TXT)
