import json, random
from pathlib import Path
from datetime import datetime, timezone

CATALOG = Path("app/logs/product_catalog.json")
QUEUE = Path("app/logs/priority_publish_queue.txt")
PERFORMANCE = Path("app/logs/product_performance.json")
DECISIONS = Path("app/logs/autopilot_decisions.json")
EXPLORATION = Path("app/logs/exploration_candidates.json")

products = json.loads(CATALOG.read_text(encoding="utf-8-sig"))
product_map = {p["id"]: p for p in products}

performance = json.loads(PERFORMANCE.read_text(encoding="utf-8-sig")) if PERFORMANCE.exists() else {}

decisions = {}
if DECISIONS.exists():
    decisions_list = json.loads(DECISIONS.read_text(encoding="utf-8-sig"))
    decisions = {d["product_id"]: d for d in decisions_list}

if EXPLORATION.exists():
    exploration = json.loads(EXPLORATION.read_text(encoding="utf-8-sig"))
    selected_ids = [x["product_id"] for x in exploration if x["product_id"] in product_map]
else:
    selected_ids = [p["id"] for p in products[:5]]

scale_templates = [
    "Customer favorite alert\n\nThe {name} is getting attention because it {angle}.",
    "One of our top pet care picks right now.\n\nThis {name} {angle}.",
    "If you want a simple pet upgrade that actually helps, check this out.\n\nThe {name} {angle}."
]

test_templates = [
    "New pet care pick to test today.\n\nThe {name} {angle}.",
    "Looking for a useful pet product?\n\nThis {name} {angle}.",
    "Simple pet care upgrade worth checking out.\n\nThe {name} {angle}."
]

posts = []

for product_id in selected_ids:
    p = product_map[product_id]
    decision = decisions.get(product_id, {})
    action = decision.get("action", "keep_testing")

    if action == "pause":
        continue

    if action == "scale":
        count = 2
        priority = "high"
        templates = scale_templates
    else:
        count = 1
        priority = "normal"
        templates = test_templates

    for i in range(count):
        template = random.choice(templates)
        body = template.format(name=p["name"], angle=p["angle"])
        campaign = f"{product_id}_{action}_{i+1}"

        post = f"""--- PRIORITY POST ---
PRIORITY: {priority}
CHANNEL WINNER: instagram
PRODUCT ID: {product_id}
CATEGORY: {p['category']}
ACTION: {action}

{body}

Shop now: {p['url']}?utm_source=instagram&utm_medium=social&utm_campaign={campaign}

{p['hashtags']}
"""
        posts.append(post)

QUEUE.write_text("\n".join(posts), encoding="utf-8")

print("Exploration-based queue generated:", QUEUE)
print("Products selected:", len(selected_ids))
print("Posts created:", len(posts))
print("Created at:", datetime.now(timezone.utc).isoformat())
