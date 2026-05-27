import os
import json
import requests
from pathlib import Path
from datetime import datetime, timezone

PAGE_ID = os.getenv("META_PAGE_ID", "1045219518685639")
TOKEN = os.getenv("META_PAGE_ACCESS_TOKEN") or os.getenv("META_ACCESS_TOKEN")
OUT = Path("app/logs/meta_page_post_result.json")

message = """Tired of your pet pushing the bowl around the floor?

This non-slip silicone feeding bowl keeps mealtime cleaner and easier. Perfect for cats and dogs.

Shop now:
https://aicommerce-test-store-2.myshopify.com

#petbowl #dogbowl #catbowl #petcare #petproducts"""

url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"

payload = {
    "message": message,
    "access_token": TOKEN
}

r = requests.post(url, data=payload, timeout=30)

result = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status_code": r.status_code,
    "response": r.json() if r.text else {},
    "status": "posted" if r.status_code in [200, 201] else "failed"
}

OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
