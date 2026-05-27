import json
from pathlib import Path
from urllib.parse import urlencode
from datetime import datetime, timezone

STORE = "https://aicommerce-test-store-2.myshopify.com"
OUT = Path("app/logs/utm_social_links.json")
TXT = Path("app/logs/social_links_to_use.txt")

campaigns = [
    {
        "product": "Non-slip silicone pet feeding bowl",
        "source": "instagram",
        "medium": "social",
        "campaign": "pet_bowl_test"
    },
    {
        "product": "Foldable Cat Tunnel Toy",
        "source": "pinterest",
        "medium": "social",
        "campaign": "cat_tunnel_test"
    },
    {
        "product": "British Style Dog Raincoat",
        "source": "facebook",
        "medium": "social",
        "campaign": "dog_raincoat_test"
    }
]

links = []

for c in campaigns:
    params = {
        "utm_source": c["source"],
        "utm_medium": c["medium"],
        "utm_campaign": c["campaign"]
    }

    url = STORE + "?" + urlencode(params)

    links.append({
        "product": c["product"],
        "source": c["source"],
        "campaign": c["campaign"],
        "url": url
    })

OUT.write_text(json.dumps({
    "created_at": datetime.now(timezone.utc).isoformat(),
    "links": links
}, indent=2), encoding="utf-8")

TXT.write_text(
    "\n\n".join([
        f"{x['product']}\n{x['source']}\n{x['url']}"
        for x in links
    ]),
    encoding="utf-8"
)

print("UTM LINKS CREATED:", len(links))
print("JSON:", OUT)
print("TEXT:", TXT)
