from pathlib import Path
from datetime import datetime, timezone
import random

OUT = Path("app/logs/priority_publish_queue.txt")
OUT.parent.mkdir(parents=True, exist_ok=True)

products = [
    {
        "name": "non-slip silicone pet bowl",
        "angle": "keeps mealtime cleaner for cats and dogs",
        "hashtags": "#petbowl #dogbowl #catbowl #petcare #petproducts"
    },
    {
        "name": "foldable cat tunnel",
        "angle": "helps indoor cats stay active and entertained",
        "hashtags": "#cattoys #catlife #petcare #catproducts #indoorcats"
    },
    {
        "name": "pet grooming brush",
        "angle": "removes loose fur and keeps your sofa cleaner",
        "hashtags": "#petgrooming #dogcare #catcare #petproducts #furremoval"
    },
    {
        "name": "slow feeder dog bowl",
        "angle": "helps pets eat slower and makes feeding time easier",
        "hashtags": "#slowfeeder #dogbowl #petcare #dogproducts #healthypets"
    }
]

store_url = "https://aicommerce-test-store-2.myshopify.com"

templates = []

for p in products:
    post = f"""--- PRIORITY POST ---
PRIORITY: normal
CHANNEL WINNER: instagram

Looking for a simple upgrade for your pet?

This {p['name']} {p['angle']}.

Shop now: {store_url}?utm_source=instagram&utm_medium=social&utm_campaign={p['name'].replace(' ', '_')}

{p['hashtags']}
"""
    templates.append(post)

OUT.write_text("\n".join(templates), encoding="utf-8")

print("Queue generated:", OUT)
print("Posts created:", len(templates))
print("Created at:", datetime.now(timezone.utc).isoformat())
